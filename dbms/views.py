from django.shortcuts import render, redirect
# -*- coding:utf8-*-
# Create your views here.
from django.shortcuts import HttpResponse
from dbms import models as dbms_models
from dbms import forms as dbms_forms
from cmdb import models as cmdb_models
from django import forms
from scripts import functions
from cmdb.views import auth
from cmdb.views import get_user_cookie
import json


@auth
def index(request):
    user_cookie = get_user_cookie(request)
    user_prive = cmdb_models.UserInfo.objects.filter(user_name=user_cookie).first()
    return render(request, 'index.html', {'userinfo': user_prive})


@auth
def sql_reviews(request):
    ince_form_obj = dbms_forms.InceForm()
    user_cookie = get_user_cookie(request)
    user_prive = cmdb_models.UserInfo.objects.filter(user_name=user_cookie).first()
    ret = {'ince_form': ince_form_obj, 'userinfo': user_prive, 'app_err': '', 'ince_result': ''}
    result = ''
    if request.method == 'POST':
        ince_form_obj = dbms_forms.InceForm(request.POST)
        ret['ince_form'] = ince_form_obj
        if ince_form_obj.is_valid():
            check_flag = ince_form_obj.cleaned_data['check_flag']
            db_host_info = cmdb_models.HostInfoAuth.objects.filter(host_id=ince_form_obj.cleaned_data['db_ip']).all().values('app_pass', 'app_user', 'app_port', 'host__host_ip')
            if db_host_info:
                for item in db_host_info:
                    sql_content = 'use ' + ince_form_obj.cleaned_data['db_name'] + ';' + ince_form_obj.cleaned_data['sql_text']
                    app_user = item['app_user']
                    app_pass = item['app_pass']
                    app_port = item['app_port']
                    host_ip = item['host__host_ip']
                    result = functions.ince_run_sql(host_ip, sql_content, db_port=int(app_port), db_user=app_user,
                                                     db_passwd=app_pass)
                tran_result = functions.tran_audit_result(result)
                ret['ince_result'] = tran_result
                if check_flag:
                    # 判断是否审核结果是否需要入库
                    r = cmdb_models.UserInfo.objects.filter(id=ince_form_obj.cleaned_data['review_user']).first()
                    ince_insert_db(tran_result, user_cookie, host_ip, r, ince_form_obj.cleaned_data['db_name'], sql_content)
            else:
                ret['app_err'] = '主机未配置账号密码, 请联系管理员'
        return render(request, 'inception.html', ret)
    else:
        return render(request, 'inception.html', ret)


@auth
def sql_audit(request):
    user_cookie = get_user_cookie(request)
    user_prive = cmdb_models.UserInfo.objects.filter(user_name=user_cookie).first()
    user_work_order_list = dbms_models.InceptionWorkOrderInfo.objects.filter(review_user=user_cookie).all()
    # 使用多表关联， __ 反向查找
    return render(request, 'ince_sql_audit.html', {'userinfo': user_prive, 'work_order_list': user_work_order_list})

@auth
def sql_audit_detail(request, wid):
    work_details = dbms_models.InceptionAuditDetail.objects.filter(work_order_id=wid)
    work_info = dbms_models.InceptionWorkOrderInfo.objects.filter(work_order_id=wid)
    # for lines in work_details:
    #     print(lines)

    return render(request, 'audit_details.html', {'detail_result': work_details, "work_info": work_info})


@auth
def backup(request):
    return HttpResponse('backup')

@auth
def install(request):
    return HttpResponse('install')


def ince_insert_db(result_dict, user_cookie, host_ip, review_user, db_name, sql_content):
    w_id = functions.get_uuid()
    work_user = user_cookie
    dbms_models.InceptionWorkOrderInfo.objects.create(
        work_order_id=w_id,
        work_user=work_user,
        review_user=review_user,
        db_host=host_ip,
        db_name=db_name
    )
    dbms_models.InceptionWorkSQL.objects.create(
        sql_content=sql_content,
        work_order_id=w_id
    )
    for item in result_dict.values():
        sql_sid = item['sql_sid']
        if item['status'] == 'CHECKED':
            status = 0
        elif item['status'] == 'EXECUTED':
            status = 1
        elif item['status'] == 'RERUN':
            status = 2
        else:
            status = 3
        err_id = item['err_id']

        if item['stage_status'] == 'Audit completed':
            stage_status = 0
        elif item['stage_status'] == 'Execute failed':
            stage_status = 1
        elif item['stage_status'] == 'Execute Successfully':
            stage_status = 2
        elif item['stage_status'] == 'Execute Successfully\nBackup successfully':
            stage_status = 3
        else:
            stage_status = 4
        # 需要单独处理
        error_msg = item['error_msg']['status']
        if error_msg:
            error_msg = item['error_msg']['error_msgs']
        else:
            error_msg = 'None'

        sql_content = item['sql_content']
        aff_row = item['aff_row']
        rollback_ip = item['rollback_id']
        backup_dbname = item['backup_dbname']
        execute_time = int(float(item['execute_time']) * 1000)
        sql_hash = item['sql_hash']
        new = dbms_models.InceptionAuditDetail()
        new.work_order_id = w_id
        new.sql_sid = sql_sid
        new.status = status
        new.err_id = err_id
        new.stage_status = stage_status
        new.error_msg = error_msg
        new.sql_content = sql_content
        new.aff_row = aff_row
        new.rollback_id = rollback_ip
        new.backup_dbname = backup_dbname
        new.execute_time = execute_time
        new.sql_hash = sql_hash
        new.save()


def work_review():
    """
    公共信息
    work_order_id
    work_user

    查看工单，只能查看自己提前的工单信息

    sql_fulltext
    db_host
    db_name
    review_user
    review_status
    work_status
    r_time

    工单详情

    sql_sid
    status
    err
    stage_status
    error_msg
    sql_content
    aff_row
    execute_time
    rollback_id
    sql_hash
    r_time
    :return:
    """
    pass