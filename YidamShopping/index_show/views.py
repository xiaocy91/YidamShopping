#encoding:utf-8

from django.shortcuts import render,render_to_response, redirect
from seller.models import Store,HomeProduct,HomeType,ProductSecondType,Product,ProductImage,ProductPrice,\
    ProductType,ProductImage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from user_center.models import Userinfo
from models import SysStore,SysProduct
from django.http.response import HttpResponse
import json
import os
import shutil
# Create your views here.

def index(request):
    resData=getSysStore()
    
    login_status=request.session.get('login_status')
    if login_status:
        account=request.session.get('account')
        resData['account']=account
    else:
         #获取cookie，判断是否自动登录
        account=request.COOKIES.get('account')
        password=request.COOKIES.get('password')
        #判断cookie中的用户名和密码
        if account and password:
               userinfo=Userinfo.objects.filter(Account=account)
               if userinfo:
                   if password==userinfo[0].Password:
                        request.session['login_status']=True
                        request.session.set_expiry(0)
                        request.session['account']=userinfo[0].Account
                        request.session['userid']=userinfo[0].Userid
                        resData['account']=account
        
    return render_to_response('front_index.html',resData)
   


def searchStorePro(request):
    resData={}
    if request.method=='POST':
        data=request.POST
        
        #添加用户账号信息
        login_status=request.session.get('login_status')
        if login_status:
            account=request.session.get('account')
            resData['account']=account
        
        #判断类型为店铺或者商品
        type=data.get('type')
        storePro=data.get('storePro')
        #脱空格
        storePro=storePro.strip()
        #搜索商品
        if type=='1':
            productLists=[]
            proObjs=Product.objects.filter(Head__icontains=storePro)
            if proObjs:
                for pro in proObjs:
                    productList=[]
                    seconTypeId=pro.TypeNid_id
                    seconType=ProductSecondType.objects.get(SecondTypeNid=seconTypeId)
                    firstTypeId=seconType.TypeNid_id
                    firstType=ProductType.objects.get(TypeNid=firstTypeId)
                    #店铺id
                    storeId=firstType.StoreNid_id
                    #商品信息
                    proId=pro.Nid 
                    img=ProductImage.objects.filter(ProductNid_id=proId).last().Img
                    head=pro.Head
                    priceObj=ProductPrice.objects.filter(ProductNid_id=proId)
                    #商品价格存在与不存在
                    if priceObj:
                        price=priceObj.order_by("Price")[0].Price
                    else:
                        price=0
                    #封装商品数据
                    productList.append(storeId) #0
                    productList.append(proId) #1
                    productList.append(img)     #2
                    productList.append(head) #3
                    productList.append(price) #4
                    productLists.append(productList)
            #进行分页    
            paginator = Paginator(productLists,settings.PER_PAGE)#每页显示多少条数据，在setting里设置
            page = request.GET.get('page')
            try:
                productLists = paginator.page(page)
            except PageNotAnInteger:
                productLists = paginator.page(1)
            except EmptyPage:
                productLists = paginator.page(paginator.num_pages)   
            #封装数据
            resData={'productLists':productLists}
            resData['storePro']=storePro
            resData['type']=type
            return render_to_response('front_product.html',resData)
           
        #搜索店铺    
        elif type=='2':
            storeLists=[]
            if storePro:
                storeObjs=Store.objects.filter(StoreName__icontains=storePro)
                if storeObjs:
                    for store in storeObjs:
                        storeList=[]
                        storeList.append(store.StoreNid)
                        storeList.append(store.StoreName)
                        storeList.append(store.StoreBossName)
                        
                        storeId=store.StoreNid
                        types=HomeType.objects.filter(StoreNid_id=storeId)
                        typeList=[]
                        for type in types:
                            typeId=type.SecondTypeNid_id
                            seconType=ProductSecondType.objects.get(SecondTypeNid=typeId)
                            seconTypeName=seconType.SecondTypeName
                            
                            print seconTypeName
                            typeList.append(seconTypeName)
                            storeList.append(typeList)
                            
                            print storeList
                        storeLists.append(storeList)
                    #进行分页    
                paginator = Paginator(storeLists,settings.PER_PAGE)#每页显示多少条数据，在setting里设置
                page = request.GET.get('page')
                try:
                    storeLists = paginator.page(page)
                except PageNotAnInteger:
                    storeLists = paginator.page(1)
                except EmptyPage:
                    storeLists = paginator.page(paginator.num_pages)    
                #将商品列表加入返回的数据字典
                resData['stores']=storeLists  
                resData['type']=type 
                resData['storePro']=storePro
                return render_to_response('front_store.html',resData)
            else:
                return redirect('/index/')
        else:
            resData['stores']=[] 
            return render_to_response('front_store.html')
        
        
#获取首页店铺函数，被sys调用
def getSysStore():
    resData={}
    #所有店铺
    stores=SysStore.objects.all()
    for store in stores:
        storeList=[]
        id=store.SysStoreNid
        order=store.SysStoreOrder
        img=store.SysStoreImg
        order='storeOrder'+str(order)
        #封装单个店铺
        storeList.append(id)
        storeList.append(img)
        #当个店铺存入字典
        resData[order]=storeList
        
    pros=SysProduct.objects.all()
    if pros:
        for pro in pros:
            proList=[]
            storeId=pro.SysStoreNid
            proOrder=pro.SysProOrder
            proId=pro.SysProNid
            proOrder='proOrder'+str(proOrder)
            #封装单个商品
            proList.append(storeId)
            proList.append(proId)
            #查找商品图片
            img=ProductImage.objects.filter(ProductNid_id=proId).last().Img
            #查找商品标题
            head=Product.objects.get(Nid=proId).Head
            proList.append(img)
            proList.append(head)
            #当个商品存入字典
            resData[proOrder]=proList
        
    return resData
    
        
#进入系统管理        
def sys(request):
    result=False
    resData={}
    if request.method=='GET':
        sys_loginStatus=request.session.get('sys_loginStatus',False)
        if sys_loginStatus:
            sysAccount=request.session.get('sysAccount')
            #获取首页店铺
            stores=Store.objects.all()
            #获取带顺序显示的店铺
            resData=getSysStore()
            resData['sysAccount']=sysAccount
            resData['stores']=stores
            return render_to_response('sys_index.html',resData)
        else:
            return render_to_response('sys_load.html')
    if request.method=='POST':
        if request.method == 'POST':
            data=request.POST
            sysAccount=data.get('sysAccount')
            sysPassword=data.get('sysPassword')
            if sysAccount == 'admin':
                if sysAccount and sysPassword:
                    userinfo=Userinfo.objects.filter(Account=sysAccount)
                    if userinfo:
                        if sysPassword==userinfo[0].Password:
                            request.session['sys_loginStatus']=True
                            request.session['sysAccount']=sysAccount
                            #获取首页店铺
                            stores=Store.objects.all()
                            #获取带顺序显示的店铺、商品
                            resData=getSysStore()
                            resData['sysAccount']=sysAccount
                            resData['stores']=stores
                            return render_to_response('sys_index.html',resData)
                        else:
                            result='用户账号或者密码错误'
                            return render_to_response('sys_load.html',{'result':result})  
                    else:
                        result='用户账号或者密码错误'
                        return render_to_response('sys_load.html',{'result':result}) 
                else:
                    result='用户账号或者密码错误'
                    return render_to_response('sys_load.html',{'result':result})  
            else:
                result='用户账号或者密码错误'
                return render_to_response('sys_load.html',{'result':result})   
   




#退出系统管理
def sysExit(request):
    del request.session['sys_loginStatus']
    del request.session['sysAccount']
    return redirect('/sys/')





def addSysStore(request):
    if request.method == 'POST':
        data=request.POST
        file=request.FILES
        order=data.get('order')
        storeId=data.get('storeId')
        storeImg=file.get('storeImg')
        
        order=int(order)
        storeId=int(storeId)
        
        if order and storeId and storeImg:
            sysStores=SysStore.objects.all()
            if sysStores:
                for sysStore in sysStores:
                    sysOrder=sysStore.SysStoreOrder
                    sysStoreId=sysStore.SysStoreImg
                    print order,sysOrder
                    if order==sysOrder:
                        return HttpResponse('duple')
                    else:
                         #存放数据库
                        SysStore.objects.create(SysStoreOrder=order,SysStoreNid=storeId,SysStoreImg=storeImg)
                        return HttpResponse('True')
            else:
                SysStore.objects.create(SysStoreOrder=order,SysStoreNid=storeId,SysStoreImg=storeImg)
                return HttpResponse('True')
        else:
            return HttpResponse('Empty')
   

#获取店铺一级分类
def getFirstType(request):
    if request.method=='POST':
        data=request.POST
        storeId=data.get('storeId')
        types=ProductType.objects.filter(StoreNid_id=storeId)
        if types:
            typeLists=[]
            for type in types:
                typeList=[]
                typeId=type.TypeNid
                typeName=type.TypeName
                typeList.append(typeId)
                typeList.append(typeName)
                typeLists.append(typeList)
        typeLists=json.dumps(typeLists)
        return HttpResponse(typeLists)
    
    
 #添加系统首页商品   
def addSysPro(request):
    if request.method=='POST':
        data=request.POST
        sysPro=data.get('sysPro')
        sysPro=json.loads(sysPro)
        storeId=sysPro['storeId']
        proId=sysPro['proId']
        order=sysPro['order']
        
        try:
            storeId=int(storeId)
            proId=int(proId)
        except Exception:
            return HttpResponse('False')
        
        if storeId and proId and order:
            #判断order是否重复
            pros=SysProduct.objects.all()
            if pros:
                for pro in pros:
                    if order==pro.SysProOrder:
                        return HttpResponse('Duple')
                    else:
                        SysProduct.objects.create(SysStoreNid=storeId,SysProNid=proId,SysProOrder=order)
                        return HttpResponse('True')
            else:
                SysProduct.objects.create(SysStoreNid=storeId,SysProNid=proId,SysProOrder=order)
                return HttpResponse('True')


#删除系统首页店铺
def delSysStore(request):
    if request.method=='POST':
        data=request.POST
        order=data.get('order')
        if order:
            try:
                store=SysStore.objects.get(SysStoreOrder=order)
                if store:
                    img=store.SysStoreImg
                    path=str(img)
                    finalPath=structFile(path)
                    if os.path.exists(finalPath):
                            #删除文件
                            shutil.rmtree(finalPath)
                    #删除数据
                    store.delete()
            except Exception:
                return HttpResponse('False')
            return HttpResponse('True')



#删除系统首页商品
def delSysPro(request):
    if request.method=='POST':
        data=request.POST
        order=data.get('order')
        if order:
            try:
                pro=SysProduct.objects.get(SysProOrder=order)
                if pro:
                    pro.delete()
            except Exception:
                return HttpResponse('False')
            return HttpResponse('True')


















#
#重组需要删除的文件路径
#
def structFile(path):
    #list包含三个元素，分别是第一个上传位置文件夹，第二级日期文件夹，第三个.jpg名字
    pathList=path.split('/')
    folderPath=pathList[0]+'/'+pathList[1]
    #属性图片所在文件夹路径
    pathListFinal=settings.MEDIA_ROOT+'/'+folderPath
    return pathListFinal