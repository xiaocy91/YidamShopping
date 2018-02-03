#encoding:utf-8

from django.shortcuts import render,render_to_response
from seller.models import Store,HomeProduct,HomeType,ProductSecondType,Product,ProductImage,ProductPrice,\
    ProductType,ProductImage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from user_center.models import Userinfo
from models import SysStore,SysProduct
from django.http.response import HttpResponse
import json

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
   


def searchStore(request):
    resData={}
    if request.method=='POST':
        data=request.POST
        
        #添加用户账号信息
        login_status=request.session.get('login_status')
        if login_status:
            account=request.session.get('account')
            resData['account']=account
        
        storeName=data.get('storeName')
        storeLists=[]
        
        if storeName:
            storeObjs=Store.objects.filter(StoreName__contains=storeName)
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
            
                
                
                
                
            return render_to_response('front_store.html',resData)
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
    for pro in pros:
        proList=[]
        storeId=pro.SysStoreNid
        proOrder=pro.SysStoreOrder
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
   




#退出系统管理
def sysExit(request):
    del request.session['sys_loginStatus']
    del request.session['sysAccount']
    return render_to_response('sys_load.html')





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
                    if order==pro.SysStoreOrder:
                        return HttpResponse('Duple')
                    else:
                        SysProduct.objects.create(SysStoreNid=storeId,SysProNid=proId,SysStoreOrder=order)
                        return HttpResponse('True')
            else:
                SysProduct.objects.create(SysStoreNid=storeId,SysProNid=proId,SysStoreOrder=order)
                return HttpResponse('True')
