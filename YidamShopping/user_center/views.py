#encoding: utf-8

from django.shortcuts import render, render_to_response,HttpResponseRedirect
from models import Userinfo,ShopCar,Order,OrderProduct
from seller.models import Store,Product,ProductAttr2,ProductAttr1,ProductPrice

import json
import re
import os
import time
import datetime
from django.conf import settings
from django.http.response import HttpResponse
from test.test_datetime import DAY


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
          #计算总金额
        price=int(price)
        mount=int(mount)
        sum=price*mount
        
        #查询添加的商品，购物车中是否已经存在
        carObj=ShopCar.objects.filter(UserNid_id=userId,StoreId=storeId,ProductId=productId,AttrId1=attrId1,AttrId2=attrId2)
        if carObj:
            #若存在
            carExist=ShopCar.objects.get(UserNid_id=userId,StoreId=storeId,ProductId=productId,AttrId1=attrId1,AttrId2=attrId2)
            num=carExist.Mount
            num+=long(mount)
            carExist.Mount=num
            sumPrice=carExist.SumPrice
            sumPrice+=sum
            carExist.SumPrice=sumPrice
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
                                   AttrName2=attrName2,PriceId=priceId,Price=price,Mount=mount,SumPrice=sum)
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
        resData['userId']=userId
    #获取用户购物车信息
        shopcars=ShopCar.objects.filter(UserNid_id=userId)
        #将店铺的id筛选出来放在lists中
        lists=[]
        for shopcar in shopcars:
            storeId=shopcar.StoreId
            if storeId not in lists:
                lists.append(storeId)
        carLists=[]
        for id in lists:
            carList=[]
            pros=ShopCar.objects.filter(UserNid_id=userId,StoreId=id)
            storeName=pros[0].StoreName
            carList.append(id)
            carList.append(storeName)
            proLists=[]
            for pro in pros:
                proList=[]
                proid=pro.ProductId
                proHead=pro.ProductHead
                proAttrId1=pro.AttrId1
                proAttrName1=pro.AttrName1
                proAttrImg1=pro.AttrImg1
                proAttrId2=pro.AttrId2
                proAttrName2=pro.AttrName2
                proPriceId=pro.PriceId
                proPrice=pro.Price
                proMount=pro.Mount
                carId=pro.Nid
                proSumPrice=pro.SumPrice
                proList.append(proid)  #0
                proList.append(proHead) #1
                proList.append(proAttrId1) #2
                proList.append(proAttrName1) #3
                proList.append(proAttrImg1) #4
                proList.append(proAttrId2) #5
                proList.append(proAttrName2) #6
                proList.append(proPriceId) #7
                proList.append(proPrice) #8
                proList.append(proMount) #9
                proList.append(carId) #10
                proList.append(proSumPrice) #11
                proLists.append(proList)
            carList.append(proLists)
            carLists.append(carList)
            
    
        resData['carLists']=carLists
        
       
        return render_to_response('user_car_index.html',resData)
    else:
        return HttpResponseRedirect('/load/')
    






#修改购物车数量
def modifyMount(request):
     if request.method=='POST':
        data=request.POST
        addData=data.get('addData')
        addData=json.loads(addData)
        
        #addData数据格式：{u'mount': 4, u'nid': 34} 
        mount=addData['mount']
        nid=addData['nid']
        #修改数据库对应的mount
        if mount>=1:
            pro=ShopCar.objects.get(Nid=nid)
            price=pro.Price
            sumPrice=price*mount
            pro.Mount=mount
            pro.SumPrice=sumPrice
            pro.save()
            return HttpResponse(sumPrice)
        else:
            return HttpResponse(-1)
 
       


def userCenter(request):
    resData={}
    #用户登录信息
    login_status=request.session.get('login_status',False)
    if login_status:
        account=request.session.get('account')
        userId=request.session.get('userid')
        resData['account']=account
        resData['userId']=userId
    
        return render_to_response('user_center_index.html',resData)
    else:
        return HttpResponseRedirect('/load/')
 
 
#添加订单 
#数据结构[{"storeId":"5","proArry":["43","44","47"],"itemTotalPrice":2660},]如此 
def addOrder(request):
    if request.method=='POST':
        data=request.POST
        order=data.get('order')
        order=json.loads(order)
        
        
        orders=[]
        for store in order:
            #店铺信息
            storeList=[]
            storeId=store['storeId']
            proArry=store['proArry']
            itemTotalPrice=store['itemTotalPrice']
            #店铺名
            storeName=ShopCar.objects.filter(StoreId=storeId)[0].StoreName
            
            storeList.append(storeId) #0
            storeList.append(storeName) #1
            storeList.append(itemTotalPrice) #2
            #店铺商品信息
            prolist=[]
            for id  in proArry:
                pro=ShopCar.objects.get(Nid=id)
                prolist.append(pro) #3
            storeList.append(prolist)
            #封装到订单
            orders.append(storeList)  
            
            if len(orders)>1:
                length=True
            else:
                length=False
            
    return render_to_response('user_center_orderConfirm.html',{'orders':orders,'len':length})


#提交订单
#提交数据格式{"storeId":1,"proArry":["49","50"]}
def submitOrder(request):
    if request.method=='POST':
        data=request.POST
        order=data.get('order')
        order=json.loads(order)
        #获取请求数据
        storeId=order['storeId']
        total=order['total']
        proArry=order['proArry']
        
        #判断是否可以提交订单,出错后进入出错页面
        for id in proArry:
            try:
                ShopCar.objects.get(Nid=id)
            except Exception:  
                return render_to_response('user_center_orderWrong.html',{'wrongInfo':'购物车没有对应商品'})
        
        #获取店铺名称
        storeName=ShopCar.objects.filter(StoreId=storeId)[0].StoreName
        #用户Id
        userId=request.session.get('userid')
        #当前时间
        t=datetime.datetime.now()
        #订单号为日期+用户ID
        #用户id为5位，不够用0补充
        userStr=str(userId)
        userStr=userStr.zfill(5)
        dateStr=t.strftime('%y%m%d%H%M%S')
        #合成订单号
        orderNum=dateStr+userStr
        #生成订单
        Order.objects.create(OrderNum=orderNum,DateTime=t,StoreId=storeId,
                            StoreName=storeName,UserId_id=userId,Total=total)
        #获取生成的订单中的Nid号
        orderId=Order.objects.get(OrderNum=orderNum).Nid
        #生成订单中商品
        for id in proArry:
            #获取购物车对应商品
            pro=ShopCar.objects.get(Nid=id)
            #添加进订单对应商品
            OrderProduct.objects.create(OrderId_id=orderId,ProductId=id,
                                        ProductHead=pro.ProductHead,AttrName1=pro.AttrName1,
                                        AttrImg1=pro.AttrImg1,AttrName2=pro.AttrName2,
                                        Price=pro.Price,Mount=pro.Mount,SumPrice=pro.SumPrice)
            #删除对应购物车商品
            pro.delete()
        
    return render_to_response('user_center_orderSuccess.html')
   
    
    
def showOrderFinal(request):
    if request.method=='GET':
        #用户Id
        userId=request.session.get('userid')
        #获取用户订单
        orders=Order.objects.filter(UserId_id=userId)
        orderLists=[]
        for order in orders:
            orderList=[]
            id=order.Nid
            orderNum=order.OrderNum 
            storeId=order.StoreId 
            storeName=order.StoreName 
            dateTime=order.DateTime 
            year=dateTime.year
            month=dateTime.month
            day=dateTime.day
            dateStr='%d-%d-%d'%(year,month,day) 
            total=order.Total  
            #封装订单店铺数据
            orderList.append(orderNum) #0
            orderList.append(storeId) #1
            orderList.append(storeName) #2
            orderList.append(dateStr) #3
            orderList.append(total) #4
            #获取店铺商品
            pros=OrderProduct.objects.filter(OrderId_id=id)
            proLists=[]
            for pro in pros:
                proList=[]
                proId=pro.ProductId 
                proHead=pro.ProductHead 
                name1=pro.AttrName1 
                img1=pro.AttrImg1  
                name2=pro.AttrName2 
                price=pro.Price 
                mount=pro.Mount  
                sum=pro.SumPrice
                #封装数据
                proList.append(proId) #0
                proList.append(proHead) #1
                proList.append(name1) #2
                proList.append(img1) #3
                proList.append(name2) #4
                proList.append(price) #5
                proList.append(mount) #6
                proList.append(sum)  #7
                proLists.append(proList)
            orderList.append(proLists)
            orderLists.append(orderList)
        
            
    
    return render_to_response('user_center_orderFinal.html',{'orderLists':orderLists})