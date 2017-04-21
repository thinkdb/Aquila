from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
# Create your views here.
from cmdb import models as cmdb_models


def host_manager(request):
    return HttpResponse("主机管理界面尚未完成，尽情期待！！！")


def user_manager(request):
    return HttpResponse("用户管理界面尚未完成，尽情期待！！！")


def login(request):
    if request.method == 'POST':
        user = request.POST.get('username', None)
        pwd = request.POST.get('password', None)
        user = cmdb_models.UserInfo.objects.filter(user_name=user, user_pass=pwd)
        if user:
            return redirect("/dbms/index")
        else:
            return redirect("http://www.bing.com")
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        user = request.POST.get('username', None)
        pwd = request.POST.get('password', None)
        email = request.POST.get('Email', None)
        user_info = cmdb_models.UserInfo.objects.filter(user_name=user)
        if user_info:
            # username and password is existe
            #
            pass
        else:
            cmdb_models.UserInfo.objects.create(
                user_name=user,
                user_pass=pwd,
                user_emails=email,
                role_id = 5,
                user_group_id = 2,
                permission_id = 1
            )
            return redirect('/cmdb/login')
    else:
        return render(request, 'register.html')