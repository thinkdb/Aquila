from django.shortcuts import render, redirect
# -*- coding:utf8-*-
# Create your views here.
from django.shortcuts import HttpResponse
from dbms import models as dbms_models
from scripts import functions
from cmdb.views import auth
from cmdb.views import get_user_cookie
from .models import InceptionAuditDetail

@auth
def index(request):
    # 获取用户的 cookie,如果没有，则不能登录
    #user_cookie = request.get_signed_cookie('userinfo', salt='adfsfsdfsd')
    user_cookie = get_user_cookie(request)
    # if user_cookie:
    #     return render(request, 'index.html', {'userinfo': user_cookie})
    # else:
    #     return redirect('/cmdb/login')

    return render(request, 'index.html', {'userinfo': user_cookie})


@auth
def inception(request):
    user_cookie = get_user_cookie(request)
    review_users = ['think', 'zhangsan', '2343', '23423', '23423423']

    if request.method == 'POST':
        host_ip = request.POST.get('dbhost', None)
        db_name = request.POST.get('dbname', None)
        db_port = request.POST.get('dbport', 3306)
        review_user = request.POST.get('select_user', None)
        sql_content = 'use ' + db_name + '; ' + request.POST.get('sql_area', None)

        # 检测表单内容是否有空值
        if host_ip and db_name and db_port and review_user and sql_content:
            # 审核 sql
            sql_content = sql_content.rstrip()
            result = functions.ince_run_sql(host_ip, sql_content, port=db_port)

            # 检查语法问题
            if type(result) == tuple:
                # 工单信息入库
                w_id = functions.get_uuid()
                work_user = 'think'
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
                print(result)
                # for item in result:
                #     # 修改数据类型， str to  int
                #     sql_sid = item[0]
                #     status = item[1]
                #     err_id = item[2]
                #     stage_status = item[3]
                #     error_msg = item[4]
                #     sql_content = item[5]
                #     aff_row = item[6]
                #     rollback_ip = item[7]
                #     backup_dbname = item[8]
                #     execute_time = item[9]
                #     sql_hash = item[10]
                #     new = InceptionAuditDetail()
                #     new.work_order_id = w_id
                #     new.sql_sid = sql_sid
                #     new.status = status
                #     new.err_id = err_id
                #     new.stage_status = stage_status
                #     new.error_msg = error_msg
                #     new.sql_conten = sql_conten
                #     new.aff_row = aff_row
                #     new.rollback_id = rollback_ip
                #     new.backup_dbname = backup_dbname
                #     new.execute_time = execute_time
                #     new.sql_hash = sql_hash
                #     new.save()

                return render(request, 'inception.html', {'ince_result': result, 'review_users': review_users, 'userinfo': user_cookie})
            else:
                context = (('None', 0, 0, 0, "语法错误", sql_content),)
                return render(request, 'inception.html', {'ince_result': context, 'review_users': review_users, 'userinfo': user_cookie})
        else:
            return render(request, 'inception.html', {'review_users': review_users, 'userinfo': user_cookie})
    else:
        return render(request, 'inception.html', {'review_users': review_users, 'userinfo': user_cookie})

@auth
def backup(request):
    return HttpResponse('backup')

@auth
def install(request):
    return HttpResponse('install')
