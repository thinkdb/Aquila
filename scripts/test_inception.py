#!/bin/env python3
# _*_ coding:utf8 _*_

import pymysql
sql="""
/*--user=root;--password=123456;--host=192.168.1.6;--port=3306;--enable-check=1;--enable-execute=0;
            --enable-ignore-warnings=0;--sleep=500;--enable-split=0;*/
            inception_magic_start;
            use test;create table ince(id int);
            inception_magic_commit;
"""
# try:
#     conn = pymysql.connect(host='192.168.1.6', user='', passwd='', db='', port=6669)
#     cur = conn.cursor()
#     ret = cur.execute(sql)
#     a = cur.Warning()
#     print(a)
#     result = cur.fetchall()
#     num_fields = len(cur.description)
#     field_names = [i[0] for i in cur.description]
#     print(field_names)
#     for row in result:
#         print(row[0], "|", row[1], "|", row[2], "|", row[3], "|", row[4], "|",
#               row[5], "|", row[6], "|", row[7], "|", row[8], "|", row[9], "|", row[10])
#     cur.close()
#     conn.close()
# except pymysql.Error as e:
#      print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
#

import pymysql as pymysqldb
class DBAPI(object):
    def __init__(self, host, user, password, port, database):
        self.conn = pymysqldb.connect(host=host, user=user, passwd=password, port=int(port),
                                       database=database, autocommit=1, charset='utf8')
        try:
            self.conn.select_db(database)
        except:
            pass
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


sql="""
/*--user=root;--password=123456;--host=192.168.1.6;--port=3306;--enable-check=1;--enable-execute=0;
            --enable-ignore-warnings=0;--sleep=500;--enable-split=0;*/
            inception_magic_start;
            use test;create table ince(id int);
            inception_magic_commit;
"""

db = DBAPI(host='192.168.1.6', user='', password='', database='', port=6669)
r = db.conn_query(sql)
print(r)