#encoding:utf-8

from django.shortcuts import render,render_to_response
from seller.models import Store,HomeProduct,HomeType,ProductSecondType,Product,ProductImage,ProductPrice
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

# Create your views here.

def index(request):
    login_status=request.session.get('login_status')
    if login_status:
        account=request.session.get('account')
        return render_to_response('front_index.html',{'account':account})
    else:
        return render_to_response('front_index.html')


def searchStore(request):
    resData={}
    if request.method=='POST':
        data=request.POST
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
