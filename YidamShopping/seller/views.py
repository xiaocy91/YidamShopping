#encoding:utf-8
from django.shortcuts import render,render_to_response
from django.http.response import HttpResponseRedirect,HttpResponse
from user_center.models import Userinfo
from models import Store,ProductType
import json
from seller.models import ProductSecondType


#进入卖家中心首页
def sellerIndex(request):
    
    #对session进入卖家中心的学习
    
    login_status=request.session.get('login_status',False)
   
    if login_status:
        account=request.session.get('account')
        userinfos=Userinfo.objects.filter(Account=account)
        openStore=userinfos[0].OpenStore
        
        
        request.session['openStore']=openStore
        
        
        resData={'account':account,'openStore':openStore}
        return render_to_response('seller_index.html',resData)
    else:
        return HttpResponseRedirect('/load/')



#注册店铺    
def registerStore(request):
    openStore=request.session.get('openStore')
   
    account=request.session.get('account')
    
   
        
    resData={'account':account,'openStore':openStore}
    
    #开始判断注册店铺的数据
    if request.method=='POST':
        data=request.POST
        storeName=data.get('storeName')
        storeAddr=data.get('storeAddr')
        storeBossName=data.get('storeBossName')
        storeBossIndentity=data.get('storeBossIndentity')
        
        if storeName and storeAddr and storeBossName and storeBossIndentity:
            #开始注册
            userid=request.session.get('userid')
            userid=int(userid)
            
            Store.objects.create(UserNid_id=userid,StoreName=storeName,StoreAddr=storeAddr,StoreBossName=storeBossName,StoreBossIndentity=storeBossIndentity)
            #注册店铺后，将用户信息表中，注册店铺状态改为True
            Userinfo.objects.filter(Userid=userid).update(OpenStore=True)
            #返回用户基本数据，以及状态数据
            request.session['openStore']=True
            #创建一个默认店铺
            defaultStore(request)
            
            resData={'account':account,'openStore':True,'storeName':storeName,'storeAddr':storeAddr,'storeBossName':storeBossName}
            return render_to_response('store_view_index.html',resData)
        else:
            return render_to_response('register_store.html',resData)
    
    #若不是POST方法，直接返回注册页面    
    return render_to_response('register_store.html',resData)




#查看店铺信息
def searchStore(request):
    userid=request.session.get('userid')
    account=request.session.get('account')
    openStore=request.session.get('openStore')
   
    if openStore:
        storeInfo = Store.objects.filter(UserNid_id=userid)
        resData={'account':account,'openStore':openStore,'storeName':storeInfo[0].StoreName,'storeAddr':storeInfo[0].StoreAddr,'storeBossName':storeInfo[0].StoreBossName}
        return render_to_response('store_view_index.html',resData)

def manageStore(request):
    
    typeDic={}
    openStore=request.session.get('openStore')
    userid=request.session.get('userid')
    account=request.session.get('account')
    if openStore:
        store=Store.objects.filter(UserNid=userid)
        #将sotreid添加到session中，方便使用
        storeid=store[0].StoreNid
        request.session['storeid']=storeid
        
        #获取店铺中的分类信息
        types=ProductType.objects.filter(StoreNid_id=storeid)
        for type in types:
            secondTypeDic=[]
            typeName=type.TypeName
           # typeList.append(typename)
           
            secondTypes=ProductSecondType.objects.filter(TypeNid_id=type.TypeNid)
            
            
            for secondType in secondTypes:
                secondTypeDic.append(secondType.SecondTypeName)
                 
            typeDic[typeName]=secondTypeDic
        
       
        #获取店铺名称
        storeName=store[0].StoreName
        #封装返回数据
        resData={'storeName':storeName,'account':account,'typeDic':typeDic}
        return render_to_response('store_manage_index.html',resData)
    
#创建默认店铺信息    
def defaultStore(request):
    userid=request.session.get('userid')
    userid=int(userid)
    
    store=Store.objects.filter(UserNid_id=userid)
    storeid=store[0].StoreNid
    #设置默认 的一级分类
    ProductType.objects.create(StoreNid_id=storeid,TypeName='女装')
    ProductType.objects.create(StoreNid_id=storeid,TypeName='男装')
    #设置默认的二级分类
    productType=ProductType.objects.filter(TypeName='女装')
    typeid=productType[0].TypeNid
    ProductSecondType.objects.create(TypeNid_id=typeid,SecondTypeName='女羽绒服')
    ProductSecondType.objects.create(TypeNid_id=typeid,SecondTypeName='女外套')
    ProductSecondType.objects.create(TypeNid_id=typeid,SecondTypeName='女毛衣')
    ProductSecondType.objects.create(TypeNid_id=typeid,SecondTypeName='女休闲裤')
    ProductSecondType.objects.create(TypeNid_id=typeid,SecondTypeName='女打底裤')
    ProductSecondType.objects.create(TypeNid_id=typeid,SecondTypeName='女鞋')
    productType=ProductType.objects.filter(TypeName='男装')
    typeid=productType[0].TypeNid
    ProductSecondType.objects.create(TypeNid_id=typeid,SecondTypeName='男棉衣')
    ProductSecondType.objects.create(TypeNid_id=typeid,SecondTypeName='男卫衣')
    ProductSecondType.objects.create(TypeNid_id=typeid,SecondTypeName='男运动裤')
    ProductSecondType.objects.create(TypeNid_id=typeid,SecondTypeName='男休闲裤')
    ProductSecondType.objects.create(TypeNid_id=typeid,SecondTypeName='男鞋')

