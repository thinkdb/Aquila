from django.shortcuts import render, redirect
# -*- coding:utf8-*-
# Create your views here.
from django.shortcuts import HttpResponse
from dbms import models as dbms_models
from cmdb import models as cmdb_models
from scripts import functions
from cmdb.views import auth
from cmdb.views import get_user_cookie
import json

@auth
def index(request):
    user_cookie = get_user_cookie(request)
    return render(request, 'index.html', {'userinfo': user_cookie})


@auth
def sql_reviews(request):
    user_cookie = get_user_cookie(request)
    review_users = ['admin', '2343', '23423', '23423423']
    if request.method == 'POST':
        host_ip = request.POST.get('dbhost', None)
        db_name = request.POST.get('dbname', None)
        db_port = request.POST.get('dbport', 3306)
        review_user = request.POST.get('select_user', None)
        sql_content = 'use ' + db_name + '; ' + request.POST.get('sql_area', None)
        try:
            result_db = request.POST.get('result_db', None)
        except:
            result_db = 0

        # 检测表单内容是否有空值
        if host_ip and db_name and db_port and review_user and sql_content:
            # 审核 sql
            sql_content = sql_content.rstrip()
            result1 = functions.ince_run_sql(host_ip, sql_content, db_port=db_port, db_user='think', db_passwd='123456')

            #functions.tran_audit_result(result)
            # 检查语法问题
            if type(result1) == tuple:
                result = functions.tran_audit_result(result1)
                if result_db:  # 提交审核
                    w_id = functions.get_uuid()
                    work_user = user_cookie
                    db_ip = functions.num2ip('num', host_ip)
                    dbms_models.InceptionWorkOrderInfo.objects.create(
                        work_order_id=w_id,
                        work_user=work_user,
                        review_user=review_user,
                        db_host=db_ip,
                        db_name=db_name
                    )
                    dbms_models.InceptionWorkSQL.objects.create(
                        sql_content=sql_content,
                        work_order_id=w_id
                    )
                    for item in result.values():
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
                        new.error_msg = json.dumps(error_msg).encode('utf-8')
                        new.sql_content = sql_content
                        new.aff_row = aff_row
                        new.rollback_id = rollback_ip
                        new.backup_dbname = backup_dbname
                        new.execute_time = execute_time
                        new.sql_hash = sql_hash
                        new.save()

                    result_dict = {'flag': 1, 'msg': '提交成功'}

                    return HttpResponse(json.dumps(result_dict))
                return render(request, 'inception.html', {'ince_result': result, 'review_users': review_users, 'userinfo': user_cookie})
            else:
                context = (('None', 0, 0, 0, result1, sql_content),)
                return render(request, 'inception.html', {'ince_result': context, 'review_users': review_users, 'userinfo': user_cookie})
        else:
            return render(request, 'inception.html', {'review_users': review_users, 'userinfo': user_cookie})
    else:
        return render(request, 'inception.html', {'review_users': review_users, 'userinfo': user_cookie})


@auth
def sql_audit(request):
    user_name = get_user_cookie(request)
    user_work_order_list = dbms_models.InceptionWorkOrderInfo.objects.filter(review_user=user_name)
    # 使用多表关联， __ 反向查找
    return render(request, 'ince_sql_audit.html', {'userinfo': user_name, 'work_order_list': user_work_order_list})

@auth
def sql_audit_detail(request, wid):
    work_details = dbms_models.InceptionAuditDetail.objects.filter(work_order_id=wid)
    for lines in work_details:
        # 修改
        print(lines.error_msg, type(lines.error_msg), json.loads((lines.error_msg).decode("utf-8")))
    return HttpResponse('ok')


@auth
def backup(request):
    return HttpResponse('backup')

@auth
def install(request):
    return HttpResponse('install')
