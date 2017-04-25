#!/bin/env python3
# _*_ coding:utf8 _*_

import pymysql
sql='/*--user=think;--password=123456;--host=192.168.1.6;--execute=1;--port=3306;*/\
inception_magic_start;\
use aquila;\
CREATE TABLE adaptive_office(id int);\
CREATE TAE adaptive_office(id int);\
CREATE TABLE adaptive_office(id int);\
inception_magic_commit;'
try:
    conn = pymysql.connect(host='192.168.1.6', user='', passwd='', db='', port=6669)
    cur = conn.cursor()
    ret = cur.execute(sql)
    a = cur.Warning()
    print(a)
    result = cur.fetchall()
    num_fields = len(cur.description)
    field_names = [i[0] for i in cur.description]
    print(field_names)
    for row in result:
        print(row[0], "|", row[1], "|", row[2], "|", row[3], "|", row[4], "|",
              row[5], "|", row[6], "|", row[7], "|", row[8], "|", row[9], "|", row[10])
    cur.close()
    conn.close()
except pymysql.Error as e:
     print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
