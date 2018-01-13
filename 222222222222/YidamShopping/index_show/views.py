#encoding:utf-8

from django.shortcuts import render,render_to_response
from seller.models import Store,HomeProduct,HomeType,ProductSecondType,Product,ProductImage,ProductPrice

# Create your views here.

def index(request):
    login_status=request.session.get('login_status')
    if login_status:
        account=request.session.get('account')
        return render_to_response('front_index.html',{'account':account})
    else:
        return render_to_response('front_index.html')


def searchStore(request):
    if request.method=='POST':
        data=request.POST
        storeName=data.get('storeName')
        
        print storeName
       
        storeObjs=Store.objects.filter(StoreName__contains=storeName)
        return render_to_response('front_store.html',{'stores':storeObjs})

