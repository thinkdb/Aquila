from django.shortcuts import render, redirect
# -*- coding:utf8-*-
# Create your views here.
from django.shortcuts import HttpResponse
from dbms import models as dbms_models
from dbms import forms as dbms_forms
from cmdb import models as cmdb_models
from scripts import functions
from cmdb.views import auth
from cmdb.views import get_user_cookie
import datetime
import threading

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
                # 分析出主从关系
                master_ip = functions.get_master(host_ip, app_user, app_pass, app_port, '')
                result = functions.ince_run_sql(master_ip, sql_content, db_port=int(app_port), db_user=app_user,
                                                 db_passwd=app_pass)
                tran_result = functions.tran_audit_result(result)
                ret['ince_result'] = tran_result
                if check_flag == '1':
                    # 判断是否审核结果是否需要入库
                    r = cmdb_models.UserInfo.objects.filter(id=ince_form_obj.cleaned_data['review_user']).first()
                    if r == user_prive:
                        ret['app_err'] = '自己不能审核自己的工单'
                        return render(request, 'inception.html', ret)
                    ince_insert_db(tran_result, user_cookie, master_ip, r, ince_form_obj.cleaned_data['db_name'], sql_content)
            else:
                ret['app_err'] = '主机未配置账号密码, 请联系管理员'
        return render(request, 'inception.html', ret)
    else:
        return render(request, 'inception.html', ret)


@auth
def sql_audit(request):
    """
    审核列表页面
    """
    user_cookie = get_user_cookie(request)
    user_prive = cmdb_models.UserInfo.objects.filter(user_name=user_cookie).first()
    user_work_order_list = dbms_models.InceptionWorkOrderInfo.objects.filter(review_user=user_cookie, review_status=10).all()
    return render(request, 'ince_sql_audit.html', {'userinfo': user_prive, 'work_order_list': user_work_order_list})


@auth
def sql_audit_commit(request):
    """
    工单审核通过与否
    """
    work_id = request.POST.get('work_id', None)
    user_cookie = get_user_cookie(request)
    user_prive = cmdb_models.UserInfo.objects.filter(user_name=user_cookie).first()
    user_work_order_list = dbms_models.InceptionWorkOrderInfo.objects.filter(review_user=user_cookie).all()
    if request.POST.get('1', None):
        status = 0
    else:
        status = 1
    review_time = datetime.datetime.now()
    dbms_models.InceptionWorkOrderInfo.objects.filter(work_order_id=work_id).update(review_status=status, review_time=review_time)
    return redirect('sql_audit.html', {'userinfo': user_prive, 'work_order_list': user_work_order_list})

@auth
def sql_audit_detail(request, wid):
    """
    审核详情页
    """
    work_details = dbms_models.InceptionAuditDetail.objects.filter(work_order_id=wid)
    work_info = dbms_models.InceptionWorkOrderInfo.objects.filter(work_order_id=wid)
    return render(request, 'audit_details.html', {'detail_result': work_details, "work_info": work_info})


@auth
def backup(request):
    return HttpResponse('backup')

@auth
def install(request):
    return HttpResponse('install')


def ince_insert_db(result_dict, user_cookie, host_ip, review_user, db_name, sql_content, wid=0):
    """
    工单审核信息入库
    """
    w_id = wid
    if w_id:
        work_status = 0
        for k in result_dict:
            if result_dict[k]['stage_status'] == 'Execute Successfully' \
                    or result_dict[k]['stage_status'] == 'Execute Successfully\nBackup successfully':
                work_status = 0
            else:
                work_status = 1
                break
        end_time = datetime.datetime.now()

        dbms_models.InceptionWorkOrderInfo.objects.filter(work_order_id=wid).update(work_status=work_status, end_time=end_time)

    else:
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

@auth
def work_reviews(request):
    """
    工单查询
    """
    user_cookie = get_user_cookie(request)
    user_name = cmdb_models.UserInfo.objects.filter(user_name=user_cookie).first()
    ret = dbms_models.InceptionWorkOrderInfo.objects.filter(work_user=user_name).all()
    return render(request, 'work_reviews.html', {'work_obj': ret, 'userinfo': user_name})


@auth
def work_detail(request, wid):
    """
    查看工单的详情页面
    """
    user_cookie = get_user_cookie(request)
    user_name = cmdb_models.UserInfo.objects.filter(user_name=user_cookie).first()
    work_details = dbms_models.InceptionAuditDetail.objects.filter(work_order_id=wid)
    work_info = dbms_models.InceptionWorkOrderInfo.objects.filter(work_order_id=wid)
    return render(request, 'work_details.html', {'detail_result': work_details, "work_info": work_info, 'userinfo': user_name})


@auth
def work_runing(request):
    user_cookie = get_user_cookie(request)
    user_name = cmdb_models.UserInfo.objects.filter(user_name=user_cookie).first()
    # 获取当前用户所有的已经审核成功的工单
    all_work = dbms_models.InceptionWorkOrderInfo.objects.filter(work_user=user_name, review_status=0, work_status=10).all()
    if request.method == 'GET':
        return render(request, 'work_runing.html', {'userinfo': user_name, 'all_work': all_work})

    if request.method == 'POST':

        wid = request.POST.get('wid', None)
        sql_content = request.POST.get('sql_content', None)
        host_ip = request.POST.get('host_ip', None)
        r = cmdb_models.HostInfo.objects.filter(host_ip=host_ip).all()
        for row in r:
            app_pass = row.hostinfoauth_set.all()[0].app_pass
            app_user = row.hostinfoauth_set.all()[0].app_user
            app_port = row.hostinfoauth_set.all()[0].app_port

        # 优化成任务计划来执行，提交后直接返回提交成功，执行结果需要在工单查询中查看
        # 添加任务表，
            master_ip = functions.get_master(host_ip, app_user, app_pass, app_port, '')

            dbms_models.WorkOrderTask.objects.create(wid=wid, app_user=app_user, app_pass=app_pass, host_ip=master_ip, app_port=app_port)
            dbms_models.InceptionWorkOrderInfo.objects.filter(work_order_id=wid).update(work_status=2)

            t = threading.Thread(target=Task())
            t.start()
        return HttpResponse(1)


def Task():
    task_all = dbms_models.WorkOrderTask.objects.all()
    if task_all:
        for item in task_all:
            master_ip = item.host_ip
            app_port = item.app_port
            app_user = item.app_user
            app_pass = item.app_pass
            wid = item.wid
            sql_content = dbms_models.InceptionWorkSQL.objects.filter(work_order_id=wid).first().sql_content

            dbms_models.InceptionWorkOrderInfo.objects.filter(work_order_id=wid).update(work_status=3)
            result = functions.ince_run_sql(master_ip, sql_content, db_port=app_port, db_user=app_user,
                                        db_passwd=app_pass, enable_check=0, enable_execute=1, enable_ignore_warnings=1)
            tran_result = functions.tran_audit_result(result)
            ince_insert_db(result_dict=tran_result, user_cookie='', host_ip='', review_user='', db_name='',
                       sql_content=sql_content, wid=wid)

            dbms_models.WorkOrderTask.objects.filter(wid=wid).delete()
