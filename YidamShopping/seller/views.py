#encoding:utf-8
from django.shortcuts import render,render_to_response
from django.http.response import HttpResponseRedirect,HttpResponse
from user_center.models import Userinfo
from models import Store,ProductType
import json
from seller.models import ProductSecondType
from django.template.defaultfilters import first
from urllib2 import HTTPRedirectHandler


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

#进入店铺管理主页
def manageStore(request):
    resData=getTypesData(request)
    return render_to_response('store_manage_index.html',resData)
    
#创建默认店铺信息 ,该函数为封装的方法，在注册店铺的时候被调用   
def defaultStore(request):
    userid=request.session.get('userid')
    userid=int(userid)
    
    store=Store.objects.filter(UserNid_id=userid)
    storeid=store[0].StoreNid
    #设置默认 的一级分类
    ProductType.objects.create(StoreNid_id=storeid,TypeName='女装')
    ProductType.objects.create(StoreNid_id=storeid,TypeName='男装')
    #设置默认的二级分类
    productType=ProductType.objects.filter(StoreNid_id=storeid,TypeName='女装')
    typeid=productType[0].TypeNid
    ProductSecondType.objects.create(TypeNid_id=typeid,SecondTypeName='女羽绒服')
    ProductSecondType.objects.create(TypeNid_id=typeid,SecondTypeName='女外套')
    ProductSecondType.objects.create(TypeNid_id=typeid,SecondTypeName='女毛衣')
    ProductSecondType.objects.create(TypeNid_id=typeid,SecondTypeName='女休闲裤')
    ProductSecondType.objects.create(TypeNid_id=typeid,SecondTypeName='女打底裤')
    ProductSecondType.objects.create(TypeNid_id=typeid,SecondTypeName='女鞋')
    productType=ProductType.objects.filter(StoreNid_id=storeid,TypeName='男装')
    typeid=productType[0].TypeNid
    ProductSecondType.objects.create(TypeNid_id=typeid,SecondTypeName='男棉衣')
    ProductSecondType.objects.create(TypeNid_id=typeid,SecondTypeName='男卫衣')
    ProductSecondType.objects.create(TypeNid_id=typeid,SecondTypeName='男运动裤')
    ProductSecondType.objects.create(TypeNid_id=typeid,SecondTypeName='男休闲裤')
    ProductSecondType.objects.create(TypeNid_id=typeid,SecondTypeName='男鞋')


#封装获取商品分类的方法，被其他方法调用
def getTypesData(request):
    account=request.session.get('account')
    storeid=request.session.get('storeid')
    openStore=request.session.get('openStore')
    userid=request.session.get('userid')
    
    typeDic={}
    if openStore:
        store=Store.objects.filter(UserNid=userid)
        #将sotreid添加到session中，方便使用
        storeid=store[0].StoreNid
        request.session['storeid']=storeid
        
        #获取店铺中的一级分类信息
        types=ProductType.objects.filter(StoreNid_id=storeid)
        for type in types:
            #封装一级分类到列表
            typeName=type.TypeName
            typeid=type.TypeNid
            firstItemTup=(typeid,typeName)
           #获取二级分类信息
            secondTypes=ProductSecondType.objects.filter(TypeNid_id=typeid)
            secondItemDic=[]
            secondDic=[]
            for secondType in secondTypes:
                secondItemDic=[secondType.SecondTypeNid,secondType.SecondTypeName]
                secondDic.append(secondItemDic)
                
            #将二级分类信息放入相应的一级分类信息中
            typeDic[firstItemTup]=secondDic
            
        #获取店铺名称
        storeName=store[0].StoreName
        #封装返回数据
        resData={'storeName':storeName,'account':account,'typeDic':typeDic}
        return resData


#获取并进入商品分类编辑页面
def editTypes(request): 
    resData=getTypesData(request)
    return render_to_response('store_manage_types.html',resData)


#删除二级商品分类
def delSecondName(request):
    if request.method=='POST':
        data=request.POST
        secondJson=data.get('secondJson')
        secondJson=json.loads(secondJson)
        
        for i in secondJson:
            ProductSecondType.objects.filter(SecondTypeNid=int(i)).delete()
        return HttpResponse('True')

#删除一级标题，以及一级标题对应的二级标题
def delFirstName(request):
    if request.method=='POST':
        data=request.POST
        firstId=data.get('firstId')
        
        #先删除一级对应的所有二级标题
        ProductSecondType.objects.filter(TypeNid_id=firstId).delete()
        #删除一级标题
        ProductType.objects.filter(TypeNid=firstId).delete()
        
        return HttpResponse('True')
    
def addSecond(request):
     if request.method=='POST':
        data=request.POST
        typeName=data.get('typeName')
        key=data.get('key')
        key=int(key)
        ProductSecondType.objects.create(SecondTypeName=typeName,TypeNid_id=key)
        return HttpResponseRedirect('/editTypes/')

def editSecond(request):
     if request.method=='POST':
        data=request.POST
        typeName=data.get('typeName')
        key=data.get('key')
        key=int(key)
        ProductSecondType.objects.filter(SecondTypeNid=key).update(SecondTypeName=typeName)
        return HttpResponseRedirect('/editTypes/')

def editFirst(request):
     if request.method=='POST':
        data=request.POST
        typeName=data.get('typeName')
        key=data.get('key')
        key=int(key)
        ProductType.objects.filter(TypeNid=key).update(TypeName=typeName)
        return HttpResponseRedirect('/editTypes/')
    
def addFirst(request):
     if request.method=='POST':
        data=request.POST
        typeName=data.get('typeName')
        #获取店铺id
        userid=request.session.get('userid')
        store=Store.objects.filter(UserNid_id=userid)
        storeid=store[0].StoreNid
        ProductType.objects.create(TypeName=typeName,StoreNid_id=storeid)
        return HttpResponseRedirect('/editTypes/')