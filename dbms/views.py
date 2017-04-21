from django.shortcuts import render, redirect
# -*- coding:utf8-*-
# Create your views here.
from django.shortcuts import HttpResponse
from dbms import models as dbms_models
from scripts import functions


def index(request):
    return render(request, 'index.html')


def inception(request):
    review_users = ['think', 'zhangsan', '2343', '23423', '23423423']
    if request.method == 'POST':
        host_ip = request.POST.get('dbhost', None)
        db_name = request.POST.get('dbname', None)
        db_port = request.POST.get('dbport', 3306)
        review_user = request.POST.get('select_user', None)
        sql_content = 'use ' + db_name + '; ' + request.POST.get('sql_area', None)
        if host_ip and db_name and db_port and review_user and sql_content:
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
            result = functions.ince_run_sql(host_ip, sql_content, port=db_port)
            return render(request, 'inception.html', {'ince_result': result, 'review_users': review_users})
    else:
        return render(request, 'inception.html', {'review_users': review_users})


def backup(request):
    return HttpResponse('backup')


def install(request):
    return HttpResponse('install')
