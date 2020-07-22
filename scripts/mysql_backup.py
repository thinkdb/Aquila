#!/bin/env python3
# _*_ coding:utf8 _*_
#表结构信息
"""
create table mysql_physics_backup_source_info(
    id int unsigned not null auto_increment primary key comment '用于标识全局唯一的数据库主机,用于其他表的machine_id',
    generator_room_name varchar(30) not null comment '机房名称,拼音或英文名称,不能使用中文,参与备份片命名',
    ipaddr int unsigned not null comment 'ip 地址,使用整型存储',
    port smallint unsigned not null comment '数据库端口号,可能存在多实例的情况',
    service_level tinyint unsigned not null comment '业务级别,根据业务的重要性分级别',
    defaults_file varchar(100) not null default 'etc_my.cnf'  comment '数据库配置文件位置',
    back_time datetime not null comment '备份开始时间',
    transport_time datetime not null comment '备份完成后,传输备份片到备份池的时间',
    is_transport tinyint not null default 0 comment '0备份后不传输,输1备份后传',
    back_pool_id tinyint not null default 0 comment '备份需要传输到哪个备份池中',
    r_time datetime not null DEFAULT CURRENT_TIMESTAMP comment '记录生成的时间,可以标识库被创建的时间',
    unique key `u_idx_generator_ip_port` (`generator_room_name`,`ipaddr`,`bank_port`)
) engine=innodb comment 'mysql_physics_backup模块的源数据信息';


create table backup_pool_info(
    id tinyint not null auto_increment primary key,
    pool_name varchar(50) not null comment '备份池名称',
    ipaddr int unsigned not null comment '备份池ip 地址,使用整型存储',
    port smallint unsigned not null comment '传输使用的端口号， 默认使用22端口',
    passwd varchar(50) not null comment '传输使用的密码',
    username varchar(50) not null comment '传输使用的用户名'
)engine=innodb comment 'mysql_physics_backup模块的备份池信息';

create table mysql_physics_backup_binlog_info(
    id bigint unsigned not null auto_increment primary key,
    machine_id int unsigned not null comment '来源于mysql_physics_backup_source_info表的id字段, 唯一的标识一台数据库',
    binlog_name varchar(50) not null comment 'binlog的文件名,例如:mysql_bin.000001',
    binlog_create_time datetime not null comment 'binlog产生的时间,用于误删除恢复时的操作记录',
    binlog_size SMALLINT not null comment 'binlog文件的大小,单位为MB',
    r_time datetime not null DEFAULT CURRENT_TIMESTAMP comment '记录生成的时间,可以标识每天备份的binlog信息',
    key idx_machine_id (machine_id, r_time)
) engine=innodb comment 'mysql_physics_backup模块binlog的备份信息';


create table mysql_physics_backup_backend_info(
    id bigint unsigned not null auto_increment primary key,
    machine_id int unsigned not null comment '来源于mysql_physics_backup_source_info表的id字段, 唯一的标识一台数据库',
    backup_name varchar(100) not null comment '备份片名称,命名规则:generator_room_name_ip_port',
    backup_filepath varchar(50) not null comment '备份片存放的文件位置',
    backup_duration smallint not null comment '备份耗时, 存放秒数',
    backup_status tinyint unsigned not null comment '备份状态:',
    binlog_filepath varchar(100) not null default 'log_bin_basename' comment '存放binlog文件的路径,用于后期的误删除数据恢复',
    binlog_index varchar(100) not null default 'log_bin_index' comment 'binlog.index的文件位置',
    binlog_start varchar(50) not null comment '备份binlog开始的文件名,例如:mysql_bin.000001',
    binlog_end varchar(50) not null comment '备份binlog结束的文件名,例如:mysql_bin.000003',
    binlog_filepath varchar(50) not null comment 'binlog备份后存放的文件位置',
    binlog_status tinyint unsigned not null comment '备份binlog的状态:',
    r_time datetime not null DEFAULT CURRENT_TIMESTAMP comment '记录生成的时间,可以标识备份的完成时间',
) engine=innodb comment 'mysql_physics_backup模块的数据库备份完成信息';


备份：
    全量 + binlog
        备份成功后 flush logs
        apply-log成功之后，标识备份成功， 否则标识应用日志失败
        解析 mysql-bin.index，cp 到n-1 个binlog位置，记录下一次开始cp的位置

恢复：
    找到要恢复的备份片，解压到指定目录，修改my.cnf， 启数据库， 判断是否需要应用binlog，应用到哪一个binlog

    误删除数据恢复：
        每个binlog的生成的时间
        找到给定的时间范围内的单表操delete/update/insert内容，
        
恢复可以在备份池恢复，也可以在业务主机上恢复
"""

import os
import sys
import re
import time
import pickle
import paramiko
import subprocess
import configparser
import socket
import tarfile


def get_config(group, config_name):
    config = configparser.ConfigParser()
    config.read("../etc/db.conf")
    config_values = config.get(group, config_name).strip("\'")
    return config_values


# 获取 mysql 相关信息
mysql_bin = get_config('mysql', 'mysql_bin')
mysql_user = get_config('mysql', 'mysql_user')
mysql_passwd = get_config('mysql', 'mysql_passwd')
mysql_host = get_config('mysql', 'mysql_host')
mysql_port = get_config('mysql', 'mysql_port')
mysql_config = get_config('mysql', 'mysql_config')
backup_dir = get_config('mysql', 'backup_dir')
innobackup_cmd = get_config('mysql', 'innobackup_command')
current_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
path = os.path.dirname(current_path)
backup_logfile = path + '/logs/bak.log'
cur_date = time.strftime('%Y%m%d_%H%M%S', time.localtime())

tar_file_path = get_config('ftp', 'tar_file_path')
transport_flag = get_config('ftp', 'transport_flag')


def get_ip():
    """
    获取ip地址
    """
    ip = socket.gethostbyname_ex(socket.gethostname())[2][0]
    a = re.sub('\.', '_', ip)
    return a


def check():
    """
    检查配置文件中的信息是否正确
    :return:
    """
    cmd = mysql_bin + '/mysql --user=' + mysql_user + ' --password=' + mysql_passwd + \
          ' --port=' + mysql_port + ' --host=' + mysql_host + ' -e "select 1;"'
    ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for i in ret.stdout:
        status = str(i, encoding='utf8')
    if status != '1':
        return status
    file_check = os.path.isfile(mysql_config)
    if not file_check:
        return "ERROR. %s don't find." % mysql_config
    file_check = os.path.isfile(innobackup_cmd)
    if not file_check:
        return "ERROR. %s don't find." % innobackup_cmd
    file_check = os.path.isdir(backup_dir)
    if not file_check:
        return "ERROR. %s not exists." % backup_dir
    return "success"


def full_backup():
    """
    生成全备命令
    :return:
    """
    ip = get_ip()
    file_name = ip + '_' + cur_date + "_full"
    backup = backup_dir + '/' + file_name
    cmd_1 = innobackup_cmd + ' --defaults-file=' + mysql_config + ' --user=' + mysql_user
    cmd_2 = ' --password=' + mysql_passwd + ' --host=' + mysql_host + ' --port=' + mysql_port
    cmd_3 = ' --subordinate-info ' + backup + ' &> ' + backup_logfile + ' &'
    cmd = cmd_1 + cmd_2 + cmd_3
    run(0, cmd)


def inc_backup(num):
    """
    生成增量备份命令
    :param num: 备份级别
    :return:
    """
    ip = get_ip()
    scn = load_scn()
    flag = 10
    try:
        if len(scn) > 0 and type(scn) == dict:
            # 循环获取最近的一个备份集,如果没有找到，则执行全备
            for i in range(1, 8):
                flag = scn.get(num - i)
                if not flag:
                    continue
                else:
                    flag = num - i
                    to_scn = scn[flag]['lsn']
                    back_file_name = scn[flag]['back_file_name']
                    break
    except:
        pass
    if flag == 10:
        full_backup()
    else:
        try:
            # file = load_scn()
            # back_file_name = file[num]['back_file_name']
            file_name = back_file_name + "_inc_%s" % num
        except:
            file_name = ip + '_' + cur_date + "_inc_%s" % num

        backup = backup_dir + '/' + file_name
        cmd_1 = innobackup_cmd + ' --defaults-file=' + mysql_config + ' --user=' + mysql_user
        cmd_2 = ' --password=' + mysql_passwd + ' --host=' + mysql_host + ' --port=' + mysql_port
        cmd_3 = ' --subordinate-info --incremental --incremental-lsn=%s ' % to_scn
        cmd_4 = backup + ' &> ' + backup_logfile + ' &'
        cmd = cmd_1 + cmd_2 + cmd_3 + cmd_4
        run(num, cmd)


def check_backup_log(num, backup_log):
    """
    检测备份日志是否返回成功, 并记录备份后的 lsn 号
    :param backup_log: 备份日志的文件路径
    :return:
    """
    back_dir = ''
    with open(backup_log, 'r') as f:
        for i in f.readlines():
            backup_status = i
            dir_flag = re.search("Backup created in directory", backup_status)
            if dir_flag:
                back_dir = backup_status.split()[6].strip("\'")

    back_is_ok = re.search("completed OK", backup_status)

    if back_is_ok:
        print("ok")
        durability(num, back_dir)
        tar_backup_file(back_dir)
    else:
        print("Error,bakcup error......")


def get_back_info(args):
    """
    获取备份开始和结束，备份时的lsn号
    :param args: 备份文件的全路径
    :return:
        {'back_file_name': '192_168_1_6_20161209_133032_inc_4',
        'end_time': '2016-12-09 13:30:56',
        'innodb_to_lsn': 2144828180,
        'start_time': '2016-12-09 13:30:32',
        'innodb_from_lsn': 2144828180,
        'elapsed_time': 24.0}
    """
    back_info_dict = {}
    with open('%s' % args + '/xtrabackup_info', 'r') as f:
        for line in f.readlines():
            start_flag = re.search("start_time", line)
            end_flag = re.search("end_time", line)
            from_lsn_flag = re.search("innodb_from_lsn", line)
            to_lsn_flag = re.search("innodb_to_lsn", line)
            back_file_name_flag = re.search("tool_command", line)
            if start_flag:
                back_info_dict["start_time"] = line.split("=")[1].strip()
            if end_flag:
                back_info_dict["end_time"] = line.split("=")[1].strip()
            if from_lsn_flag:
                back_info_dict["innodb_from_lsn"] = int(line.split("=")[1].strip())
            if to_lsn_flag:
                back_info_dict["innodb_to_lsn"] = int(line.split("=")[1].strip())
            if back_file_name_flag:
                back_info_dict["back_file_name"] = line.split()[-1].strip().split("/")[-1]
    end_time = back_info_dict["end_time"]
    start_time = back_info_dict["start_time"]
    end_ctime = time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))
    start_ctime = time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
    elapsed_time = end_ctime - start_ctime
    back_info_dict["elapsed_time"] = elapsed_time
    return back_info_dict


def run(num, cmd):
    """
    执行备份命令，并监控是否执行完成
    :param num: 备份级别
    :param cmd: 备份命令
    """
    result = subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result == 0:
        check_log_flag = 1
        while check_log_flag:
            xtr_pid = subprocess.Popen("ps -ef | grep innobackupex | grep -v grep | wc -l", shell=True,
                                       stdout=subprocess.PIPE)
            for i in xtr_pid.stdout.readlines():
                if int(i) == 1:
                    continue
                else:
                    check_log_flag = 0
                    check_backup_log(num, backup_logfile)


def durability(num, back_dir):
    """
    备份后的信息入盘， 保证下次使用增量备份时，能正常找到上一备份集的信息
    :param num: 备份级别，用于保存当前级别的信息
    :param back_dir: 备份文件，用于获取备份时的数据信息
    """
    info = get_back_info(back_dir)
    to_lsn = info["innodb_to_lsn"]
    elapsed_time = info["elapsed_time"]
    back_file_name = info["back_file_name"]
    inner_dict = {'lsn': to_lsn, 'elapsed_time': elapsed_time, 'back_file_name': back_file_name}
    scn_dict = load_scn()
    if num == 0:
        scn_dict = {}
    if type(scn_dict) == dict:
        scn_dict[num] = inner_dict
    else:
        scn_dict = {}
        scn_dict[num] = inner_dict
    dump_scn(scn_dict)


def dump_scn(scn):
    f = open('../core/data_dic', 'wb')
    pickle.dump(scn, f)
    f.close()


def load_scn():
    try:
        f = open('../core/data_dic', 'rb')
        scn = pickle.load(f)
        f.close()
    except Exception as e:
        scn = e
    return scn


class FtpServer(object):
    def __init__(self, ip, user_name, passwd, port, comm=0, local_files=0, remote_files=0):
        self.host = ip
        self.user_name = user_name
        self.passwd = passwd
        self.port = port
        self.comm = comm
        self.local_files = local_files
        self.remote_files = remote_files

    # put the files
    def putfiles(self):
        t = paramiko.Transport(self.host, self.port)
        t.connect(username=self.user_name, password=self.passwd)
        sftp = paramiko.SFTPClient.from_transport(t)
        remotepath = self.remote_files
        localpath = self.local_files
        sftp.put(localpath, remotepath)
        t.close()

    # get the files
    def getfiles(self):
        t = paramiko.Transport(self.host, self.port)
        t.connect(username=self.user_name, password=self.passwd)
        sftp = paramiko.SFTPClient.from_transport(t)
        remotepath = self.remote_files
        localpath = self.local_files
        sftp.get(remotepath, localpath)
        t.close()


def tar_backup_file(backup_file):
    file_name = backup_file.split('/')[:-1][-1]
    tar_file_name = tar_file_path + '/' + file_name + '.tar.gz'
    tar = tarfile.open(tar_file_name, 'w|gz')
    tar.add(backup_file)
    tar.close()
    if transport_flag == '1':
        remote_file_path = get_config('ftp', 'remote_file_path')
        host = get_config('ftp', 'host')
        user = get_config('ftp', 'user')
        port = get_config('ftp', 'port')
        passwd = get_config('ftp', 'passwd')
        remote_file_path = remote_file_path + '/' + file_name + '.tar.gz'
        ftp_tools = FtpServer(host, user, passwd, int(port), local_files=tar_file_name, remote_files=remote_file_path)
        ftp_tools.putfiles()