#!/bin/env python3
# _*_ coding:utf8 _*_

from django.conf import settings
import pymysql as pymysqldb
import paramiko
import socket
import struct
import re
import time
import hashlib


class DBAPI(object):
    def __init__(self, host, user, password, port, database):
        self.conn = pymysqldb.connect(host=host, user=user, passwd=password, port=int(port),
                                       database=database, autocommit=1, charset='utf8')
        self.cur = self.conn.cursor()

    def conn_query(self, sql):
        try:
            rel = self.cur.execute(sql)
            result = self.cur.fetchall()
        except Exception as e:
            result = e
        return result

    def conn_dml(self, sql):
        try:
            rel = self.cur.execute(sql)
            if rel:
                pass
            else:
                return rel
        except Exception as e:
            return e

    def dml_commit(self):
        self.conn.commit()

    def dml_rollback(self):
        self.conn.rollback()

    def close(self):
        self.cur.close()
        self.conn.close()


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


def inception_sql(db_host, db_user, db_passwd, sql_content, db_port=3306,
                  enable_check=1, enable_execute=0, enable_split=0,
                  enable_ignore_warnings=0, sleep=500):
    """
    :param db_host: DB_HOST where the database server is located
    :param db_user: DB_USER to log in as
    :param db_passwd: DB_PASSWD to use
    :param db_port: MySQL port to use, default is usually OK. (default: 3306)
    :param sql_content: SQL content to execute
    :param enable_check: Default is 1, audit the SQL_CONTENT
    :param enable_execute: Default is 0, Audit not execute the SQL_CONTENT
    :param enable_split: Default is 1, split the DDL and DML
    :param enable_ignore_warnings: Default is 0, skip warning is not allowed
    :param sleep: Defaults is 0.5s, After each SQL execution sleep seconds and then continue
    :return: Returns a SQL content that can be supported by Inception
    """
    ince_run_sql = """/*--user=%s;--password=%s;--host=%s;--port=%s;--enable-check=%s;--enable-execute=%s;
            --enable-ignore-warnings=%s;--sleep=%s;--enable-split=%s;*/
            inception_magic_start;
            %s
            inception_magic_commit;
            """ % (db_user, db_passwd, db_host, db_port, enable_check,
                   enable_execute, enable_ignore_warnings, sleep, enable_split, sql_content)
    return ince_run_sql


def ince_run_sql(db_host, sql_content, db_user, db_passwd, db_port=3306, enable_check=1,
                 enable_execute=0, enable_split=0, enable_ignore_warnings=0, sleep=500):
    """
    Connect Inception to execute SQL
    :param db_host:  DB_HOST where the database server is located
    :param sql_content: SQL content to execute
    :param port: MySQL port to use, default is usually OK. (default: 3306)
    :return:
    """
    ince_host = getattr(settings, 'INCEPTION')['default']['INCEPTION_HOST']
    ince_port = int(getattr(settings, 'INCEPTION')['default']['INCEPTION_PORT'])
    run_sql = inception_sql(db_user=db_user, db_passwd=db_passwd, db_host=db_host, sql_content=sql_content, db_port=db_port,
                            enable_check=enable_check, enable_execute=enable_execute, enable_split=enable_split,
                            enable_ignore_warnings=enable_ignore_warnings, sleep=sleep)
    try:
        db = DBAPI(host=ince_host, user='', password='', database='', port=ince_port)
        result = db.conn_query(run_sql)
    except Exception as e:
        result = e
    return result


def get_uuid():
    """
    Generate unique work order number
    """
    import random
    st = int(time.time() * 1000)
    i = random.randrange(100000, 999999)
    return int(str(st)+str(i))


def get_ip():
    """
    Get IP address
    """
    ip = socket.gethostbyname_ex(socket.gethostname())[2][0]
    aid = re.sub('\.', '_', ip)
    return aid


def num2ip(arg, int_ip):
    """
    IP address and number conversion
    """
    if arg == 'ip':
        ip = socket.inet_ntoa(struct.pack('I', socket.htonl(int_ip)))
    else:
        ip = str(socket.ntohl(struct.unpack('I', socket.inet_aton(int_ip))[0]))
    return ip


def py_password(argv):
    """
    Generate an encrypted string
    """
    h = hashlib.md5(bytes('3df6a1341e8b', encoding="utf-8"))
    h.update(bytes(argv, encoding="utf-8"))
    pass_str = h.hexdigest()
    return pass_str


def get_config():
    flag = hasattr(settings, 'INCEPTION')
    if flag:
        incepiton_cnf = getattr(settings, 'INCEPTION')
        return incepiton_cnf

