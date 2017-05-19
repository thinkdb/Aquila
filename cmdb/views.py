from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from cmdb import forms as cmdb_forms
from django.views import View
from django.utils.decorators import method_decorator


from cmdb import models as cmdb_models
from scripts import functions
import json


def user_manager(request):
    return HttpResponse("用户管理界面尚未完成，尽情期待！！！")


# FBV
def auth(func):
    def inner(request, *args, **kwargs):
        try:
            val = request.get_signed_cookie('userinfo', salt='adfsfsdfsd')
            if not val:
                return redirect('/cmdb/login')
            return func(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return redirect('/cmdb/login')
    return inner

# CBV


@method_decorator(auth, name='dispatch')
class AuthAll(View):
    #@method_decorator(auth)
    def get(self, request):
        try:
            v = request.get_signed_cookie('userinfo', salt='adfsfsdfsd')
            if not v:
                return redirect('/cmdb/login')
            return render(request, 'index.html', {'userinfo': v})
        except Exception as e:
            return redirect('/cmdb/login')

    def post(self, request):
        try:
            v = request.get_signed_cookie('userinfo', salt='adfsfsdfsd')
            if not v:
                return redirect('/cmdb/login')
            return render(request, 'index.html', {'userinfo': v})
        except Exception as e:
            return redirect('/cmdb/login')


def get_user_cookie(request):
    user_cookie = request.get_signed_cookie('userinfo', salt='adfsfsdfsd')
    return user_cookie


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        pwd = request.POST.get('password', None)
        pass_str = functions.py_password(pwd)
        user = cmdb_models.UserInfo.objects.filter(user_name=username, user_pass=pass_str)
        if user:
            res = redirect('/dbms/index')
            res.set_signed_cookie('userinfo', username, salt='adfsfsdfsd')
            return res
        else:
            return render(request, 'login.html', {'user_error': '用户名或密码错误'})
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        user = request.POST.get('username', None)
        pwd = request.POST.get('password', None)
        email = request.POST.get('Email', None)
        user_info = cmdb_models.UserInfo.objects.filter(user_name=user)
        pass_str = functions.py_password(pwd)
        if user_info:
            # username and password is existe
            # 通过 ajax 返回账号已经存在的信息
            return render(request, 'register.html')
        else:
            cmdb_models.UserInfo.objects.create(
                user_name=user,
                user_pass=pass_str,
                user_emails=email,
                role_id=2,
                user_group_id=2,
                permission_id=2
            )
            return redirect('/cmdb/login')
    else:
        return render(request, 'register.html')


@auth
def hostgroup_manage(request):
    user_cookie = get_user_cookie(request)
    request_path = request.get_full_path()
    user_prive = cmdb_models.UserInfo.objects.filter(user_name=user_cookie).first()
    host_edit = request.POST.get('host_edit', '')
    result = cmdb_models.HostGroup.objects.all()
    hostgroup_list = []

    if result:
        hostgroup_list = result
    return render(request, 'manage.html', {'userinfo': user_prive,
                                           'hostgroup_list': hostgroup_list,
                                           'host_edit': host_edit,
                                           'request_path': request_path})


@auth
def host_manage(request):
    obj = cmdb_forms.HostAppend()
    request_path = request.get_full_path()
    user_cookie = get_user_cookie(request)
    user_prive = cmdb_models.UserInfo.objects.filter(user_name=user_cookie).first()
    result = cmdb_models.HostInfo.objects.all()
    if request.method == 'POST':
        obj = cmdb_forms.HostAppend(request.POST)
        rel = obj.is_valid()
        if rel:
            ip = obj.cleaned_data['host_ip']
            new_ip = functions.num2ip(1, ip)
            obj.cleaned_data['host_ip'] = new_ip
            exist_ip = cmdb_models.HostInfo.objects.filter(host_ip=new_ip).first()
            if exist_ip:
                ret = {'flag': 0, 'data': {'ip': '主机已经存在'}}
            else:
                ret = {'flag': 1, 'data': None}

                try:
                    cmdb_models.HostInfo.objects.create(host_ip=obj.cleaned_data['host_ip'],
                                                        app_type=obj.cleaned_data['app_type'],
                                                        host_group_id=obj.cleaned_data['host_group'],
                                                        host_pass=obj.cleaned_data['host_pass'],
                                                        host_port=obj.cleaned_data['host_port'],
                                                        host_user=obj.cleaned_data['host_user']

                                                        )
                except Exception as e:
                    print('3333', e)
            return HttpResponse(json.dumps(ret))
        else:
            ret = {'flag': 0, 'data': obj.errors}
            return HttpResponse(json.dumps(ret))
    else:
        return render(request, 'manage.html', {'userinfo': user_prive,
                                               'request_path': request_path,
                                               'host_list': result,
                                               'obj': obj})



@auth
def hostgroup_append(request):
    group_name = request.POST.get('groupname', None)
    group_desc = request.POST.get('groupdesc', None)
    group_id = request.POST.get('groupid', None)
    if group_id and group_name:
        try:
            cmdb_models.HostGroup.objects.filter(id=group_id).update(
                host_group_name=group_name,
                host_group_jd=group_desc)
            result_dict = {'flag': 1, 'msg': 'GroupName: %s update successful' % group_name}
        except Exception:
            result_dict = {'flag': 0, 'msg': 'GroupName: %s already exist' % group_name}
    elif group_name:
        result = cmdb_models.HostGroup.objects.filter(host_group_name=group_name)
        if result:
            result_dict = {'flag': 0, 'msg': 'GroupName: %s already exist' % group_name}
        else:
            cmdb_models.HostGroup.objects.create(
                host_group_name=group_name,
                host_group_jd=group_desc
            )
            result_dict = {'flag': 1, 'msg': 'GroupName: %s append successful' % group_name}
    else:
        result_dict = {'flag': 0, 'msg': 'GroupName: is None'}
    return HttpResponse(json.dumps(result_dict))


def backend(request):
    user_cookie = get_user_cookie(request)
    user_prive = cmdb_models.UserInfo.objects.filter(user_name=user_cookie).first()
    return render(request, 'backend.html', {'userinfo': user_prive})