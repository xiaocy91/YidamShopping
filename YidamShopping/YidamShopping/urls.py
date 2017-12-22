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
from user_center.views import register,load,loginOut
from index_show.views import index
from seller.views import sellerIndex,registerStore,searchStore,manageStore,editTypes,delSecondName
from seller.views import delFirstName,addSecond,editSecond,editFirst,addFirst


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/$', register),
    url(r'^load/$', load),
    url(r'^index/$', index),
    url(r'^sellerIndex/$', sellerIndex),
    url(r'^loginOut/$', loginOut),
    url(r'^registerStore/$', registerStore),
    url(r'^searchStore/$', searchStore), 
    url(r'^manageStore/$', manageStore), 
    url(r'^editTypes/$', editTypes), 
    url(r'^delSecondName/$', delSecondName),  
    url(r'^delFirstName/$', delFirstName),
    url(r'^addSecond/$', addSecond),
    url(r'^editSecond/$', editSecond),
    url(r'^editFirst/$', editFirst),
    url(r'^addFirst/$', addFirst),
    
    
    
    
    
    
]
