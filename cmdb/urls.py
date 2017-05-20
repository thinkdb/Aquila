#!/bin/env python3
# _*_ coding:utf8 _*_

from django.conf.urls import url

from cmdb import views
from django.views import View

urlpatterns = [
    url(r'login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^user', views.user_manager, name='user_manager'),
    url(r'^backend/$', views.backend, name='backend'),
    url(r'^backend/hostgroup_manage.html$', views.hostgroup_manage, name='hostgroup_manage'),
    url(r'backend/hostgroup_append.html$', views.hostgroup_append, name='cmdb_hostgroup_append'),
    url(r'backend/host_manage.html$', views.host_manage, name='cmdb_host_manage'),
    url(r'backend/host_append.html$', views.host_append, name='cmdb_host_append'),
]