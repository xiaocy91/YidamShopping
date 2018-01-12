#encoding:utf-8
from django.shortcuts import render,render_to_response
from django.http.response import HttpResponseRedirect,HttpResponse
from user_center.models import Userinfo
from models import Store,ProductType
import json
from seller.models import ProductSecondType, ProductAttr1,ProductAttr2, HomeType
from django.template.defaultfilters import first
from urllib2 import HTTPRedirectHandler
from models import Product,ProductImage
import os
import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from seller.models import ProductPrice
from _mysql import NULL
from django.template.context_processors import request
from seller.models import HomeProduct

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




#店铺首页
def viewStore(request):
    resData={}
    #获取店铺信息
    userid=request.session.get('userid')
    account=request.session.get('account')
    openStore=request.session.get('openStore')
    if openStore:
        storeInfo = Store.objects.filter(UserNid_id=userid)
        resData['account']=account
        resData['openStore']=openStore
        resData['storeName']=storeInfo[0].StoreName
        resData['storeAddr']=storeInfo[0].StoreAddr
        resData['storeBossName']=storeInfo[0].StoreBossName
        resData['storeId']=storeInfo[0].StoreNid
        storeid=storeInfo[0].StoreNid
    
    #获取主页
    if request.method=='GET':
        #获取主页分类
        if storeid:
            homeTypes=HomeType.objects.filter(StoreNid_id=storeid)
        secondTypeLists=[]
        for homeType in homeTypes:
            secondTypeId=homeType.SecondTypeNid_id
            secondTypeImg=homeType.SecondTypeImg
            typeOrder=homeType.TypeOrder
            if secondTypeId:
                secondTypeInfo=ProductSecondType.objects.get(SecondTypeNid=secondTypeId)
            if secondTypeInfo:
                secondTypeName=secondTypeInfo.SecondTypeName
            secondTypeList=[]
            secondTypeList.append(secondTypeId)
            secondTypeList.append(secondTypeName)
            secondTypeList.append(secondTypeImg)
            secondTypeLists.append(secondTypeList)
            typeOrder='typeOrder'+str(typeOrder)
            resData[typeOrder]=secondTypeList
        resData['secondTypeLists']=secondTypeLists
        
        #获取主页商品
        if storeid:
            homeProducts=HomeProduct.objects.filter(StoreNid_id=storeid)
        for homeProduct in homeProducts:
            productId=homeProduct.ProductNid_id
            productOrder=homeProduct.ProductOrder
            if productId:
                productInfo=Product.objects.get(Nid=productId)
                productImg=ProductImage.objects.filter(ProductNid_id=productId).last().Img
                priceObj=ProductPrice.objects.filter(ProductNid_id=productId)
                #判断是否有价格
                if priceObj:
                    productPrice=priceObj.order_by('-Price').last().Price
                else:
                    productPrice=-1
              
            
            if productInfo and productImg:
                productHead=productInfo.Head
            productList=[]
            productList.append(productId)
            productList.append(productHead)
            productList.append(productImg)
            productList.append(productPrice)
            productOrder='productOrder'+str(productOrder)
            resData[productOrder]=productList
    
    return render_to_response('store_view_index.html',resData)

#店铺分类切换
def viewType(request):
    resData={}
    #获取店铺Id和二级分类Id
    data=request.GET
    storeId=data.get('storeId')
    secondId=data.get('secondId')
    #获取店铺信息
    userid=request.session.get('userid')
    account=request.session.get('account')
    openStore=request.session.get('openStore')
    if openStore:
        storeInfo = Store.objects.filter(StoreNid=storeId)
        resData['account']=account
        resData['openStore']=openStore
        resData['storeName']=storeInfo[0].StoreName
        resData['storeAddr']=storeInfo[0].StoreAddr
        resData['storeBossName']=storeInfo[0].StoreBossName
    #获取二级分类
    if storeId:
        homeTypes=HomeType.objects.filter(StoreNid_id=storeId)
        secondTypeLists=[]
        for homeType in homeTypes:
            secondTypeId=homeType.SecondTypeNid_id
            secondTypeImg=homeType.SecondTypeImg
            typeOrder=homeType.TypeOrder
            if secondTypeId:
                secondTypeInfo=ProductSecondType.objects.get(SecondTypeNid=secondTypeId)
            if secondTypeInfo:
                secondTypeName=secondTypeInfo.SecondTypeName
            secondTypeList=[]
            secondTypeList.append(secondTypeId)
            secondTypeList.append(secondTypeName)
            secondTypeList.append(secondTypeImg)
            secondTypeLists.append(secondTypeList)
        resData['secondTypeLists']=secondTypeLists
        resData['storeId']=storeId
        resData['secondId']=secondId
        
     #获取商品
    if request.method=='GET':
        #从产品信息表获取数据
        products=Product.objects.filter(TypeNid_id=secondId).all()
        productLists=[]
        for product in products:
            proList=[]
            id=product.Nid
            head=product.Head
            proList.append(id)
            proList.append(head)
            #获取一张商品的图片或者视频信息
            proImg=ProductImage.objects.filter(ProductNid_id=id).last()
            imgPath=proImg.Img
            proList.append(imgPath)
            #获取最后一个规格尺码的价格
            proPrice=ProductPrice.objects.filter(ProductNid_id=id).order_by('-Price').last()
            if proPrice:
                print proPrice
                price=proPrice.Price
                proList.append(price)
            #将每个商品的封装列表加入到总列表
            productLists.append(proList)
       
        #进行分页    
        paginator = Paginator(productLists,settings.HOME_PER_PAGE)#每页显示多少条数据，在setting里设置
        page = request.GET.get('page')
        try:
            productLists = paginator.page(page)
        except PageNotAnInteger:
            productLists = paginator.page(1)
        except EmptyPage:
            productLists = paginator.page(paginator.num_pages)    
            
        #将商品列表加入返回的数据字典
        resData['productLists']=productLists   
            
        return render_to_response('store_view_type.html',resData)


#店铺商品切换
def viewProduct(request):
    resData={}
    #获取店铺Id和二级分类Id
    data=request.GET
    storeId=data.get('storeId')
    proId=data.get('proId')
    #获取店铺信息
    userid=request.session.get('userid')
    account=request.session.get('account')
    openStore=request.session.get('openStore')
    if openStore:
        storeInfo = Store.objects.filter(StoreNid=storeId)
        resData['account']=account
        resData['openStore']=openStore
        resData['storeName']=storeInfo[0].StoreName
        resData['storeAddr']=storeInfo[0].StoreAddr
        resData['storeBossName']=storeInfo[0].StoreBossName
    #获取二级分类
    if storeId:
        storeId=int(storeId)
        homeTypes=HomeType.objects.filter(StoreNid_id=storeId)
        secondTypeLists=[]
        for homeType in homeTypes:
            secondTypeId=homeType.SecondTypeNid_id
            if secondTypeId:
                secondTypeInfo=ProductSecondType.objects.get(SecondTypeNid=secondTypeId)
            if secondTypeInfo:
                secondTypeName=secondTypeInfo.SecondTypeName
            secondTypeList=[]
            secondTypeList.append(secondTypeId)
            secondTypeList.append(secondTypeName)
            secondTypeLists.append(secondTypeList)
        resData['secondTypeLists']=secondTypeLists
        resData['storeId']=storeId
    #获取商品详情
    product=Product.objects.get(Nid=proId)
    if product:
        resData['product']=product
        #获取图片
        productImgs=ProductImage.objects.filter(ProductNid_id=proId)
        if productImgs:
            resData['productImgs']=productImgs
        #获取规格
        productAttr1s=ProductAttr1.objects.filter(ProductNid_id=proId)
        if productAttr1s:
            resData['productAttr1s']=productAttr1s
        #商品尺码
        productAttr2s=ProductAttr2.objects.filter(ProductNid_id=proId)
        if productAttr2s:
            resData['productAttr2s']=productAttr2s
        #商品价格
        productChip=ProductPrice.objects.filter(ProductNid_id=proId).order_by('-Price').last()
        priceChip=productChip.Price
        resData['priceChip']=priceChip
    
    return render_to_response('store_view_product.html',resData)
    

    
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


def showProduct(request,secondId):
    if request.method=='GET':
        resData=getTypesData(request)
        resData['secondId']=secondId
        #从产品信息表获取数据
        products=Product.objects.filter(TypeNid_id=secondId).all()
        productLists=[]
        for product in products:
            proList=[]
            id=product.Nid
            head=product.Head
            proList.append(id)
            proList.append(head)
            
            #获取一张商品的图片或者视频信息
            proImg=ProductImage.objects.filter(ProductNid_id=id).last()
            imgPath=proImg.Img
            proList.append(imgPath)
            
            #获取最后一个规格尺码的价格
            proPrice=ProductPrice.objects.filter(ProductNid_id=id).order_by('-Price').last()
            if proPrice:
                print proPrice
                price=proPrice.Price
                proList.append(price)
            
            #将每个商品的封装列表加入到总列表
            productLists.append(proList)
        
        #进行分页    
        paginator = Paginator(productLists,settings.PER_PAGE)#每页显示多少条数据，在setting里设置
        page = request.GET.get('page')
        try:
            productLists = paginator.page(page)
        except PageNotAnInteger:
            productLists = paginator.page(1)
        except EmptyPage:
            productLists = paginator.page(paginator.num_pages)    
            
            
        #将商品列表加入返回的数据字典
        resData['productLists']=productLists   
            
        return render_to_response('store_manage_product.html',resData)
   

    
def addProduct(request,secondId):
    resData=getTypesData(request)
    if request.method=='GET':
        resData['secondId']=secondId
        return render_to_response('store_manage_addProduct.html',resData)
    if request.method=='POST':
        postfiles=request.FILES
        postData=request.POST
        head=postData.get('head')
        
        attribute1=postData.get('attribute1')
        attribute2=postData.get('attribute2')
        imgs= postfiles.getlist('img')
        
        
        #检查提交数据是否为空
        if head and attribute1 and attribute2 and imgs :
        #商品信息表添加数据
            p=Product(TypeNid_id=secondId,Head=head,AttributeName1=attribute1,AttributeName2=attribute2)
            p.save()
            for img in imgs:
                new_pm=ProductImage(ProductNid_id=p.Nid,Img=img)
                new_pm.save()
            return HttpResponseRedirect('/editProduct/%d'%p.Nid)
        else:
            resData['secondId']=secondId
            return render_to_response('store_manage_addProduct.html',resData)
        
        


def editProduct(request,id):
    resData=getTypesData(request)
    if request.method=='GET':
        product=Product.objects.get(Nid=id)
        if product:
            resData['product']=product
            #获取图片
            productImgs=ProductImage.objects.filter(ProductNid_id=id)
            if productImgs:
                resData['productImgs']=productImgs
            #获取规格
            productAttr1s=ProductAttr1.objects.filter(ProductNid_id=id)
            if productAttr1s:
                resData['productAttr1s']=productAttr1s
            #商品尺码
            productAttr2s=ProductAttr2.objects.filter(ProductNid_id=id)
            if productAttr2s:
                resData['productAttr2s']=productAttr2s
            #商品价格
            productPrices=ProductPrice.objects.filter(ProductNid_id=id)
            priceLists=[]
            if productPrices:
                for price in productPrices:
                    priceList=[]
                    #通过id，查找对应的规格、尺码的实际内容
                    id1=price.Attr1_id
                    id2=price.Attr2_id
                    priceAttr1=ProductAttr1.objects.get(Nid=id1)
                    priceAttr2=ProductAttr2.objects.get(Nid=id2)
                    attr1=priceAttr1.Attr1
                    attr2=priceAttr2.Attr2
                    price=price.Price
                    #封装数据
                    priceList.append(id)
                    priceList.append(attr1)
                    priceList.append(attr2)
                    priceList.append(price)
                    priceLists.append(priceList)
                resData['priceLists']=priceLists
            
        return render_to_response('store_manage_editProduct.html',resData)
    
    
   
  
    
def addAttr1(request):
    if request.method=='POST':
        data=request.POST
        file=request.FILES
        
        attr1=data.get('attr')
        id=data.get('id')
        img=file.get('ImgAttr1')
        
        ProductAttr1.objects.create(ProductNid_id=id,Attr1=attr1,ImgAttr1=img)
        return HttpResponse('True')
    
def addAttr2(request):
     if request.method=='POST':
        data=request.POST
        attr2=data.get('attr')
        id=data.get('id')
        ProductAttr2.objects.create(ProductNid_id=id,Attr2=attr2)
        return HttpResponse('True')  
    
def addPrice(request):
     if request.method=='POST':
        data=request.POST
        attr1=data.get('attrId1')
        attr2=data.get('attrId2')
        price=data.get('price')
        id=data.get('id')
        ProductPrice.objects.create(ProductNid_id=id,Attr1_id=attr1,Attr2_id=attr2,Price=price)
        return HttpResponse('True') 
    

#进入店铺管理主页
def manageStore(request):
    resData=getTypesData(request)
    
    if request.method=='GET':
        #获取店铺分类
        storeid=request.session.get('storeid')
        #初始化一级分类
        productTypes=ProductType.objects.filter(StoreNid_id=storeid)
        typeLists=[]
        for productType in productTypes:
            typeList=[]
            typeId=productType.TypeNid
            typeName=productType.TypeName
            typeList.append(typeId)
            typeList.append(typeName)
            typeLists.append(typeList)
        resData['typeLists']=typeLists
        
      
        storeid=request.session.get('storeid')
        
        #获取主页分类
        if storeid:
            homeTypes=HomeType.objects.filter(StoreNid_id=storeid)
        for homeType in homeTypes:
            secondTypeId=homeType.SecondTypeNid_id
            secondTypeImg=homeType.SecondTypeImg
            typeOrder=homeType.TypeOrder
            if secondTypeId:
                secondTypeInfo=ProductSecondType.objects.get(SecondTypeNid=secondTypeId)
            if secondTypeInfo:
                secondTypeName=secondTypeInfo.SecondTypeName
            homeList=[]
            homeList.append(secondTypeId)
            homeList.append(secondTypeName)
            homeList.append(secondTypeImg)
            typeOrder='typeOrder'+str(typeOrder)
            resData[typeOrder]=homeList
        
        #获取主页商品
        if storeid:
            homeProducts=HomeProduct.objects.filter(StoreNid_id=storeid)
        for homeProduct in homeProducts:
            productId=homeProduct.ProductNid_id
            productOrder=homeProduct.ProductOrder
            if productId:
                productInfo=Product.objects.get(Nid=productId)
                productImg=ProductImage.objects.filter(ProductNid_id=productId).last().Img
                priceObj=ProductPrice.objects.filter(ProductNid_id=productId)
                #判断是否有价格
                if priceObj:
                    productPrice=priceObj.last().Price
                else:
                    productPrice=-1
              
            
            if productInfo and productImg:
                productHead=productInfo.Head
            productList=[]
            productList.append(productId)
            productList.append(productHead)
            productList.append(productImg)
            productList.append(productPrice)
            productOrder='productOrder'+str(productOrder)
            resData[productOrder]=productList
               
        
        return render_to_response('store_manage_index.html',resData)
    
    


def getSecondType(request):
    if request.method=='GET':
        data=request.GET
        typeId=data.get('typeId')
        typeId=int(typeId)
        seconds = ProductSecondType.objects.filter(TypeNid_id=typeId)
        
        secondLists=[]
        for second in seconds:
            secondList=[]
            secondId=second.SecondTypeNid
            secondName=second.SecondTypeName
            secondList.append(secondId)
            secondList.append(secondName)
            secondLists.append(secondList)
        secondLists=json.dumps(secondLists)
        
        return HttpResponse(secondLists)



def getProduct(request):
    if request.method=='GET':
        data=request.GET
        secondTypeId=data.get('secondTypeId')
        secondTypeId=int(secondTypeId)
        products=Product.objects.filter(TypeNid_id=secondTypeId)
        
        productLists=[]
        for product in products:
            productList=[]
            productId=product.Nid
            productName=product.Head
            productList.append(productId)
            productList.append(productName)
            productLists.append(productList)
        productLists=json.dumps(productLists)
        
        if productLists:
            return HttpResponse(productLists)
        else:
            return 'Empty'


def addHomeType(request):
    if request.method=='POST':
        data=request.POST
        file=request.FILES
        typeId=data.get('typeId')
        secondTypeId=data.get('secondTypeId')
        typeOrder=data.get('order')
        secondTypeImg=file.get('secondTypeImg')
        
        typeId=int(typeId)
        secondTypeId=int(secondTypeId)
        typeOrder=int(typeOrder)
     
        if typeId and secondTypeImg:
            storeid=request.session.get('storeid')
            #同一个位置只能添加一次，多个位置的分类相互不重复
            homeTypes=HomeType.objects.filter(StoreNid_id=storeid)
            
            dupFlag=True
            if homeTypes:
                for homeType in homeTypes:
                    if secondTypeId==homeType.SecondTypeNid_id or typeOrder==homeType.TypeOrder:
                       dupFlag=False
            if dupFlag:
                HomeType.objects.create(StoreNid_id=storeid,SecondTypeImg=secondTypeImg,TypeNid_id=typeId,TypeOrder=typeOrder,SecondTypeNid_id=secondTypeId)
                return HttpResponse('True')
            else:
                return HttpResponse('Duplicate')
        else:
            return HttpResponse('Empty')
        
        
#首页添加商品        
def addHomeProduct(request):
    if request.method=='POST':
        data=request.POST
        productId=data.get('productId')
        productOrder=data.get('order')
        storeid=request.session.get('storeid')
        #将字符类型转为整数类型
        productId=int(productId)
        productOrder=int(productOrder)
        
        if productId and productOrder:
            homeProducts=HomeProduct.objects.filter(StoreNid_id=storeid)
            dupFlag=True
            if homeProducts:
                for homeProduct in homeProducts:
                    if productId==homeProduct.ProductNid_id or productOrder==homeProduct.ProductOrder:
                        dupFlag=False
            if dupFlag:
                HomeProduct.objects.create(ProductOrder=productOrder,ProductNid_id=productId,StoreNid_id=storeid)
                return HttpResponse('True') 
            else:
                return HttpResponse('Duplicate')
        else:
            return HttpResponse('Empty')
        
        
        