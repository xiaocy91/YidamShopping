#encoding:utf-8
from django.shortcuts import render,render_to_response
from django.http.response import HttpResponseRedirect
from user_center.models import Userinfo
from models import Store


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
            
            Store.objects.create(Userid_id=userid,StoreName=storeName,StoreAddr=storeAddr,StoreBossName=storeBossName,StoreBossIndentity=storeBossIndentity)
            #注册店铺后，将用户信息表中，注册店铺状态改为True
            Userinfo.objects.filter(Userid=userid).update(OpenStore=True)
            #返回用户基本数据，以及状态数据
            request.session['openStore']=True
            
            resData={'account':account,'openStore':True,'storeName':storeName,'storeAddr':storeAddr,'storeBossName':storeBossName}
            return render_to_response('register_store_info.html',resData)
        else:
            return render_to_response('register_store.html',resData)
    
    #若不是POST方法，直接返回注册页面    
    return render_to_response('register_store.html',resData)

#查看店铺信息
def searchStore(request):
    userid=request.session.get('userid')
    account=request.session.get('account')
    openStore=request.session.get('openStore')
    storeInfo = Store.objects.filter(Userid_id=userid)
    userinfo=Userinfo.objects.filter(Userid=userid)
    resData={'account':account,'openStore':openStore,'storeName':storeInfo[0].StoreName,'storeAddr':storeInfo[0].StoreAddr,'storeBossName':storeInfo[0].StoreBossName}
    return render_to_response('register_store_info.html',resData)

def manageStore(request):
    
    return render_to_response('manage_store_index.html')
