from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.utils.safestring import mark_safe
from django.views import View
from django.utils.decorators import method_decorator

# Create your views here.
from cmdb import models as cmdb_models


def host_manager(request):
    return HttpResponse("主机管理界面尚未完成，尽情期待！！！")


def user_manager(request):
    return HttpResponse("用户管理界面尚未完成，尽情期待！！！")


# FBV
def auth(func):
    def inner(request, *args, **kwargs):
        #val = request.COOKIES.get('userinfo')
        try:
            val = request.get_signed_cookie('userinfo', salt='adfsfsdfsd')
            if not val:
                return redirect('/cmdb/login')
            return func(request, *args, **kwargs)
        except Exception as e:
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
    # print(type(request))
    # #print(request.environ)
    # print(request.COOKIES)
    # for k, v in request.environ.items():
    #     print(k, v)
    if request.method == 'POST':
        username = request.POST.get('username', None)
        pwd = request.POST.get('password', None)
        user = cmdb_models.UserInfo.objects.filter(user_name=username, user_pass=pwd)
        if user:
            # 设置用户的 cookie 値，以一个 dict 形式存放在浏览器中
            res = redirect('/dbms/index')
            # res.set_cookie('userinfo', username)  # 明文方式
            res.set_signed_cookie('userinfo', username, salt='adfsfsdfsd') # 加密方式
            # request.get_signed_cookie('userinfo', salt='adfsfsdfsd') #　解密
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
        if user_info:
            # username and password is existe
            # 通过 ajax 返回账号已经存在的信息
            return render(request, 'register.html')
        else:
            cmdb_models.UserInfo.objects.create(
                user_name=user,
                user_pass=pwd,
                user_emails=email,
                role_id=2,
                user_group_id=2,
                permission_id=2
            )
            return redirect('/cmdb/login')
    else:
        return render(request, 'register.html')


# 生成测试数据
data_li = []
for i in range(100):
    data_li.append(i)


def test(request):

    # 获取当前要查看的页数
    page_size = 6                             # 每页面显示的数量
    count_datas = len(data_li)                # 总数据量
    current_page = request.GET.get('p')
    current_page = int(current_page)          # 当前第几页
    start_pages = (current_page-1)*page_size   # 数据的开始
    end_pages = current_page * page_size       # 数据的结束
    data = data_li[start_pages:end_pages]       # 分页的数据
    page_buttons = 11                         # 显示的按钮数

    # 后台获取分页的总数

    count_pages, add_item = divmod(count_datas, page_size)
    if add_item:
        count_pages += 1                       # 总的页数

    # 生成分页按钮

    page_list = []
    if count_pages < page_buttons:
        start_page = 1
        end_page = page_buttons + 1
    else:
        if current_page <= int((page_buttons+1)/2):
            start_page = 1
            end_page = page_buttons + 1
        elif current_page > int((page_buttons+1)/2):
            start_page = current_page - int((page_buttons - 1)/2)
            if current_page + 5 >= count_pages:
                end_page = count_pages + 1
                start_page = count_pages - page_buttons + 1
            else:
                end_page = current_page + int((page_buttons - 1)/2)

    page_html = '<a class="page_button" href="/cmdb/test/?p=%s">上一页</a>' % (current_page -1)
    page_list.append(page_html)
    for i in range(start_page, end_page):
        if i == current_page:
            page_html = '<a class="page_button active" href="/cmdb/test/?p=%s">%s</a>' %(i, i)
        else:
            page_html = '<a class="page_button" href="/cmdb/test/?p=%s">%s</a>' % (i, i)
        page_list.append(page_html)

    # page_html = ''.join(page_list) 前台需要做 filter处理，page_html|safe
    page_html = '<a class="page_button" href="/cmdb/test/?p=%s">下一页</a>' % (current_page + 1)
    page_list.append(page_html)
    page_html = mark_safe(''.join(page_list))

    # 这一步是让 浏览器 确认收到的 包含html文本的内容 为正常的内容，不是外部来攻击的内容，不加的话，会原封不动把上面html文件内容在浏览器上显示出来
    return render(request, 'test.html', {'data_page': data, 'page_str': page_html})


def hostgroup_manage(request):

    user_cookie = get_user_cookie(request)
    host_edit = request.POST.get('host_edit', '' )
    result = cmdb_models.HostGroup.objects.all()
    hostgroup_list = []

    if result:
        hostgroup_list = result
    return render(request, 'hostgroup_manage.html', {'userinfo': user_cookie, 'hostgroup_list': hostgroup_list, 'host_edit': host_edit  })


def hostgroup_append(request):
    group_name = request.POST.get('groupname', None)
    group_desc = request.POST.get('groupdesc', None)
    import json
    if group_name:
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