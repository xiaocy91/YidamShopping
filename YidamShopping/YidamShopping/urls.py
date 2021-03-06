"""YidamShopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from user_center.views import register,load,loginOut,addCar,showCar,modifyMount,userCenter,showOrderFinal
from user_center.views import addOrder,submitOrder,buyPro,submitBuyOrder,addHeadPhoto
from user_center.views import checkOldPwd,modifyNewPwd,modifyBaseInfo
from index_show.views import index,searchStorePro,sys,sysExit,addSysStore,getFirstType,addSysPro
from index_show.views import delSysStore,delSysPro
from seller.views import sellerIndex,registerStore,viewStore,manageStore,editTypes,delSecondName
from seller.views import delFirstName,addSecond,editSecond,editFirst,addFirst,addProduct,showProduct
from seller.views import editProduct,addAttr1,addAttr2,addPrice,addHomeType,getSecondType,getProduct
from seller.views import addHomeProduct,viewType,viewProduct,getSelectPrice,saveProContent,soldOrder
from seller.views import modifyStore,delAllType,delHomeType,delHomeProduct,delePro,delTypeAllPro



#use for media and picture show
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/$', register),
    url(r'^load/$', load),
    url(r'^index/$', index),
    url(r'^$', index),
    url(r'^sellerIndex/$', sellerIndex),
    url(r'^loginOut/$', loginOut),
    url(r'^registerStore/$', registerStore),
    url(r'^viewStore/$', viewStore),
    url(r'^viewType/$', viewType),
    url(r'^viewProduct/$', viewProduct),
    url(r'^manageStore/$', manageStore), 
    url(r'^editTypes/$', editTypes), 
    url(r'^delSecondName/$', delSecondName),  
    url(r'^delFirstName/$', delFirstName),
    url(r'^addSecond/$', addSecond),
    url(r'^editSecond/$', editSecond),
    url(r'^editFirst/$', editFirst),
    url(r'^addFirst/$', addFirst),
    url(r'^showProduct/(\d+)/$', showProduct),
    url(r'^addProduct/(\d+)/$', addProduct),
    url(r'^editProduct/(\d+)/$', editProduct),
    url(r'^addAttr1/$', addAttr1),
    url(r'^addAttr2/$', addAttr2),
    url(r'^addPrice/$', addPrice),
    url(r'^addHomeType/$', addHomeType),
    url(r'^getSecondType/$', getSecondType),
    url(r'^getProduct/$', getProduct),
    url(r'^addHomeProduct/$', addHomeProduct),
    url(r'^getSelectPrice/$', getSelectPrice),
    url(r'^searchStorePro/$', searchStorePro),
    url(r'^addCar/$', addCar),
    url(r'^showCar/$', showCar),
    url(r'^modifyMount/$', modifyMount),
    url(r'^userCenter/$', userCenter),
    url(r'^showOrderFinal/$', showOrderFinal),
    url(r'^addOrder/$', addOrder),
    url(r'^submitOrder/$', submitOrder),
    url(r'^sys/$', sys),
    url(r'^sysExit/$', sysExit),
    url(r'^addSysStore/$', addSysStore),
    url(r'^saveProContent/$', saveProContent),
    url(r'^getFirstType/$', getFirstType),
    url(r'^addSysPro/$', addSysPro),
    url(r'^buyPro/$', buyPro),
    url(r'^submitBuyOrder/$', submitBuyOrder),
    url(r'^soldOrder/$', soldOrder),
    url(r'^addHeadPhoto/$', addHeadPhoto),
    url(r'^checkOldPwd/$', checkOldPwd),
    url(r'^modifyNewPwd/$', modifyNewPwd),
    url(r'^modifyBaseInfo/$', modifyBaseInfo),
    url(r'^modifyStore/$', modifyStore),
    url(r'^delAllType/$', delAllType),
    url(r'^delHomeType/$', delHomeType),
    url(r'^delHomeProduct/$', delHomeProduct),
    url(r'^delSysStore/$', delSysStore),
    url(r'^delSysPro/$', delSysPro),
    url(r'^delePro/$', delePro),
    url(r'^delTypeAllPro/$', delTypeAllPro),
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#'+static'use for media and picture show