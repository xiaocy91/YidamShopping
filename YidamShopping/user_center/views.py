#encoding: utf-8

from django.shortcuts import render, render_to_response,HttpResponseRedirect
from models import Userinfo,ShopCar
from seller.models import Store,Product,ProductAttr2,ProductAttr1,ProductPrice

import json
import re
import os
import time
from django.conf import settings
from django.http.response import HttpResponse

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

#添加购物车
def addCar(request):
    #格式{"storeId":1,"productId":78,"attrId2":"3","attrId1":"3","priceId":"4","mount":"1"}
    if request.method=='POST':
        data=request.POST
        carData=data.get('carData')
        carData=json.loads(carData)
        #获取详细信息
        storeId=carData.get('storeId')
        productId=carData.get('productId')
        attrId2=carData.get('attrId2')
        attrId1=carData.get('attrId1')
        priceId=carData.get('priceId')
        mount=carData.get('mount')
        #获取用户id
        userId=request.session.get('userid')
       
        
        #准备数据
        storeName=Store.objects.get(StoreNid=storeId).StoreName
        productHead=Product.objects.get(Nid=productId).Head
        attrName2=ProductAttr2.objects.get(Nid=attrId2).Attr2
        attrObj1=ProductAttr1.objects.get(Nid=attrId1)
        attrName1=attrObj1.Attr1
        attrImg1=attrObj1.ImgAttr1
        price=ProductPrice.objects.get(Attr1_id=attrId1,Attr2_id=attrId2).Price
        
        #查询添加的商品，购物车中是否已经存在
        carObj=ShopCar.objects.filter(UserNid_id=userId,StoreId=storeId,ProductId=productId,AttrId1=attrId1,AttrId2=attrId2)
        if carObj:
            #若存在
            carExist=ShopCar.objects.get(UserNid_id=userId,StoreId=storeId,ProductId=productId,AttrId1=attrId1,AttrId2=attrId2)
            num=carExist.Mount
            num+=long(mount)
            carExist.Mount=num
            carExist.save()
        else:   
            #若不存在
            #将商品规格图保存到用户userProImg目录下
            attrImg1=str(attrImg1)
            f1=open(settings.MEDIA_ROOT+'/'+attrImg1,'rb')
            filename='userProImg/'+time.strftime('%Y%m%d_%H%M%S',time.localtime())+'.jpg'
            filePath=settings.MEDIA_ROOT+'/'+filename
            f2=open(filePath,'wb')
            while True:
                line=f1.readline()
                if len(line)==0:
                    break
                f2.write(line)
            f1.close()
            f2.close()
            #开始添加数据库
            ShopCar.objects.create(UserNid_id=userId,StoreId=storeId,StoreName=storeName,
                                   ProductId=productId,ProductHead=productHead,AttrId1=attrId1,
                                   AttrName1=attrName1,AttrImg1=filename,AttrId2=attrId2,
                                   AttrName2=attrName2,PriceId=priceId,Price=price,Mount=mount)
        return HttpResponse(True)


#展示购物车  
def showCar(request):
    resData={}
    #用户登录信息
    login_status=request.session.get('login_status',False)
    if login_status:
        account=request.session.get('account')
        userId=request.session.get('userid')
        resData['account']=account
    #获取用户购物车信息
       
        return render_to_response('user_car.html',resData)
    else:
        return HttpResponseRedirect('/load/')
    

