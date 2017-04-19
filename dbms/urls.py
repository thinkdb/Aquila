#!/bin/env python3
# _*_ coding:utf8 _*_
from django.conf.urls import url

from dbms import views
urlpatterns = [
    url(r'^login', views.login, name='login'),
    url(r'^register', views.register, name='register'),
    url(r'^index', views.index, name='index'),
    url(r'^inception', views.inception, name='inception'),
    url(r'^backup', views.backup, name='backup'),
    url(r'^install', views.install, name='install'),

]