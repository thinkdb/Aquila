#!/bin/env python3
# _*_ coding:utf8 _*_
#表结构信息
'''
create table mysql_physics_backup_source_info(
    id bigint unsigned not null auto_increment primary key comment '用于标识全局唯一的数据库主机,用于其他表的machine_id',
    generator_room_name varchar(30) not null comment '机房名称,拼音或英文名称,不能使用中文,参与备份片命名',
    ipaddr int unsigned not null comment 'ip 地址,使用整型存储',
    bank_port smallint unsigned not null comment '数据库端口号,可能存在多实例的情况',
    service_level tinyint unsigned not null comment '业务级别,根据业务的重要性分级别',
    back_time datetime not null comment '备份开始时间',
    transport_time datetime not null comment '备份完成后,传输备份片到备份池的时间',
    binlog_filepath varchar(100) not null comment 'binlog文件的位置,用于后期的误删除数据恢复',
    binlog_index varchar(100) not null comment 'binlog.index的文件位置',
    r_time datetime not null DEFAULT CURRENT_TIMESTAMP comment '记录生成的时间,可以标识库被创建的时间',
    unique key `u_idx_generator_ip_port` (`generator_room_name`,`ipaddr`,`bank_port`)
) engine=innodb comment 'mysql_physics_backup模块的源数据信息';

create table mysql_physics_backup_binlog_info(
    id bigint unsigned not null auto_increment primary key,
    machine_id bigint unsigned not null comment '来源于mysql_physics_backup_source_info表的id字段, 唯一的标识一台数据库',
    binlog_name varchar(50) not null comment 'binlog的文件名,例如:mysql_bin.000001',
    binlog_create_time datetime not null comment 'binlog产生的时间,用于误删除恢复时的操作记录',
    binlog_size SMALLINT not null comment 'binlog文件的大小,单位为MB',
    r_time datetime not null DEFAULT CURRENT_TIMESTAMP comment '记录生成的时间,可以标识每天备份的binlog信息',
    key idx_machine_id (machine_id, r_time)
) engine=innodb comment 'mysql_physics_backup模块binlog的备份信息';


create table mysql_physics_backup_backend_info(
    id bigint unsigned not null auto_increment primary key,
    machine_id bigint unsigned not null comment '来源于mysql_physics_backup_source_info表的id字段, 唯一的标识一台数据库',
    backup_name varchar(50) not null comment '备份片名称,命名规则:generator_room_name_ip_port',
    backup_filepath varchar(50) not null comment '备份片存放的文件位置',
    backup_duration datetime not null comment '备份耗时',
    backup_status tinyint unsigned not null comment '备份状态:',
    binlog_start varchar(50) not null comment '备份binlog开始的文件名,例如:mysql_bin.000001',
    binlog_end varchar(50) not null comment '备份binlog结束的文件名,例如:mysql_bin.000003',
    binlog_filepath varchar(50) not null comment 'binlog备份后存放的文件位置',
    binlog_status tinyint unsigned not null comment '备份binlog的状态:',
    r_time datetime not null DEFAULT CURRENT_TIMESTAMP comment '记录生成的时间,可以标识备份的完成时间',
) engine=innodb comment 'mysql_physics_backup模块的数据库备份完成信息';
'''

"""
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
"""