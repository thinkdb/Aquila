#!/bin/env python3
# _*_ coding:utf8 _*_
import os
import sys
import django
current_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
path = os.path.dirname(current_path)
sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] ='Aquila.settings'
django.setup()
from cmdb import models

# 初始化角色
models.UserRole.objects.create(user_role_name='dba', user_role_jd='数据库管理员')
models.UserRole.objects.create(user_role_name='qa', user_role_jd='测试')
models.UserRole.objects.create(user_role_name='dev', user_role_jd='开发')
models.UserRole.objects.create(user_role_name='admin', user_role_jd='管理员')
models.UserRole.objects.create(user_role_name='users', user_role_jd='普通员工,默认值')


# 初始化用户组
models.UserGroup.objects.create(user_group_name='user', user_group_jd='普通用户组, 默认组')
models.UserGroup.objects.create(user_group_name='admin', user_group_jd='管理员组')
models.UserGroup.objects.create(user_group_name='dba', user_group_jd='数据库管理员组')

# 初始化主机组
models.HostGroup.objects.create(host_group_name='db', host_group_jd='数据主机组')
models.HostGroup.objects.create(host_group_name='java', host_group_jd='java主机组')