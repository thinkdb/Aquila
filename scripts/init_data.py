#!/bin/env python3
# _*_ coding:utf8 _*_
import os
import sys
import django
from scripts import functions
current_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
path = os.path.dirname(current_path)
sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] ='Aquila.settings'
django.setup()
from cmdb import models

# 初始化角色
models.UserRole.objects.create(id=1, user_role_name='admin', user_role_jd='管理员')
models.UserRole.objects.create(id=2, user_role_name='users', user_role_jd='普通员工,默认值')
models.UserRole.objects.create(id=3, user_role_name='qa', user_role_jd='测试')
models.UserRole.objects.create(id=4, user_role_name='dev', user_role_jd='开发')
models.UserRole.objects.create(id=5, user_role_name='dba', user_role_jd='数据库管理员')


# 初始化用户组
models.UserGroup.objects.create(id=1, user_group_name='admin', user_group_jd='管理员组')
models.UserGroup.objects.create(id=2, user_group_name='user', user_group_jd='普通用户组, 默认组')
models.UserGroup.objects.create(id=3, user_group_name='dba', user_group_jd='数据库管理员组')

# 初始化主机组
models.HostGroup.objects.create(id=1, host_group_name='db', host_group_jd='数据主机组')
models.HostGroup.objects.create(id=2, host_group_name='java', host_group_jd='java主机组')


# 初始化权限
models.AuthPermissions.objects.create(
    id=1,
    select_host=1,
    update_host=1,
    insert_host=1,
    delete_host=1,
    select_user=1,
    update_user=1,
    delete_user=1,
    insert_user=1
)
models.AuthPermissions.objects.create(
    id=2,
    select_host=1,
    update_host=0,
    insert_host=0,
    delete_host=0,
    select_user=1,
    update_user=0,
    delete_user=0,
    insert_user=0
)

# 初始化管理员用户
pass_str = functions.py_password('123456')
models.UserInfo.objects.create(
    id=1,
    user_name='admin',
    user_pass=pass_str,
    user_emails='996846239@qq.com',
    role_id=1,
    user_group_id=1,
    permission_id=1
)