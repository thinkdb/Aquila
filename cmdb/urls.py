#!/bin/env python3
# _*_ coding:utf8 _*_

from django.conf.urls import url

from cmdb import views
from django.views import View

urlpatterns = [
    url(r'^login', views.login, name='login'),
    url(r'^register', views.register, name='register'),
    url(r'^user', views.user_manager, name='user_manager'),
    #url(r'^test', views.test, name='test'),
    #url(r'^test', views.AuthAll.as_view(), name='test'),
    url(r'hostgroup_manage', views.hostgroup_manage, name='hostgroup_manage')
]