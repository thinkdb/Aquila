#!/bin/env python3
# _*_ coding:utf8 _*_

from django.conf.urls import url

from cmdb import views
from django.views import View

urlpatterns = [
    url(r'^login', views.login, name='login'),
    url(r'^register', views.register, name='register'),
    url(r'^host', views.host_manager, name='host_manager'),
    url(r'^user', views.user_manager, name='user_manager'),
    #url(r'^test', views.test, name='test'),
    url(r'^test', views.AuthAll.as_view(), name='test'),
]