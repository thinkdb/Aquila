#!/bin/env python3
# _*_ coding:utf8 _*_
from django.conf.urls import url

from dbms import views
urlpatterns = [
    url(r'^index.html$', views.index, name='index'),
    url(r'^inception/sql_reviews.html$', views.sql_reviews, name='dbms_sql_reviews'),
    url(r'^inception/sql_audit.html$', views.sql_audit, name='dbms_sql_audit'),
    url(r'^inception/sql_audit_commit.html$', views.sql_audit_commit, name='sql_audit_commit'),
    url(r'^inception/work_reviews.html$', views.work_reviews, name='dbms_work_reviews'),
    url(r'^inception/work_detail-(?P<wid>\d+).html$', views.work_detail, name='dbms_work_details'),
    url(r'^inception/sql_audit_detail-(?P<wid>\d+).html$', views.sql_audit_detail, name='dbms_sql_audit_details'),

    url(r'^inception/work_runing.html$', views.work_runing, name='dbms_work_runing'),


    url(r'^backup/', views.backup, name='backup'),
    url(r'^install/', views.install, name='install'),

]