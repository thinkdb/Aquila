#!/bin/env python3
# _*_ coding:utf8 _*_
from django.conf.urls import url

from dbms import views
urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^inception/sql_reviews', views.sql_reviews, name='dbms_sql_reviews'),
    url(r'^inception/sql_audit/', views.sql_audit, name='dbms_sql_audit'),
    url(r'^inception/sql_audit_detail-(?P<wid>\d+)/', views.sql_audit_detail, name='dbms_sql_audit_details'),
    url(r'^backup/', views.backup, name='backup'),
    url(r'^install/', views.install, name='install'),

]