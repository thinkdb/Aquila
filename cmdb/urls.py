#!/bin/env python3
# _*_ coding:utf8 _*_

from django.conf.urls import url

from cmdb import views

urlpatterns = [
    url(r'^login', views.login, name='login'),
    url(r'^register', views.register, name='register'),
    url(r'^host/', views.host_manager, name='host_manager'),

]