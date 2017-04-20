from django.shortcuts import render, redirect

# Create your views here.
from cmdb import models as cmdb_models

def host_manager(request):
    return render(request, 'base.html')



def login(request):
    if request.method == 'POST':
        user = request.POST.get('username', None)
        pwd = request.POST.get('password', None)
        user = cmdb_models.UserInfo.objects.filter(username=user, password=pwd)
        print(user)
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
        user_info = cmdb_models.UserInfo.objects.filter(username=user)
        if user_info:
            # username and password is existe
            #
            pass
        else:
            cmdb_models.UserInfo.objects.create(username=user, password=pwd, emails=email)
            return redirect('/dbms/login')
    else:
        return render(request, 'register.html')