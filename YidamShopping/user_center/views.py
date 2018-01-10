#encoding: utf-8

from django.shortcuts import render, render_to_response
from models import Userinfo

describe={'empty':'用户名或密码不能为空','success':'注册成功','wrong':'注册失败',
          'repete':'该用户已经注册，请换个账号注册'}



#注册用户
def register(request):
    #执行注册，默认的的结果为假
    result=False
    if request.method == 'POST':
        data=request.POST
        account=data.get('account')
        password=data.get('password')
        
        if account and password:
            #账号已经注册过
            userinfo=Userinfo.objects.filter(Account=account)
            if userinfo:
                result=describe['repete']
                return render_to_response('reg.html',{'result':result})
            #账号没注册过，现在开始注册
            else:
                #昵称默认为账户名
                result=Userinfo.objects.create(Account=account,Password=password,Nickname=account)
                result=describe['success']
                return render_to_response('reg_success.html',{'result':result,'account':account})
        #账号或密码为空
        else:
            result=describe['empty']  
            
    return render_to_response('reg.html',{'result':result})


def load(request):
    result=False
    if request.method == 'POST':
        data=request.POST
        account=data.get('account')
        password=data.get('password')
        
        if account and password:
            userinfo=Userinfo.objects.filter(Account=account)
            if userinfo:
                if password==userinfo[0].Password:
                    result=userinfo[0].Account
                    
                    #用户进入卖家中心的学习
                    request.session['login_status']=True
                    request.session['account']=userinfo[0].Account
                    request.session['userid']=userinfo[0].Userid
                    request.session.set_expiry(0)
                    return render_to_response('front_index.html',{'account':account})
                else:
                    reslut='用户账号或者密码错误'
            else:
                result='用户账号或者密码错误'
            
    return render_to_response('load.html',{'result':result})


def loginOut(request):
    del request.session['login_status']
    del request.session['account']
    del request.session['userid']
    return render_to_response('front_index.html')

