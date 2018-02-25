from __future__ import unicode_literals

from django.db import models




class Userinfo(models.Model):
    Userid=models.AutoField(primary_key=True)
    Account=models.CharField(max_length=30)
    Password=models.CharField(max_length=30)
    Phone=models.CharField(max_length=11,null=True)
    Nickname=models.CharField(max_length=30,null=True)
    Headphoto=models.ImageField(upload_to='headPhoto/%Y%m%d%H%M%S')
    Email=models.CharField(max_length=30,null=True)
    OpenStore=models.BooleanField(default=False)
    
#upload='/',is to say no upload   
class ShopCar(models.Model):
    Nid=models.AutoField(primary_key=True)
    UserNid=models.ForeignKey(Userinfo)
    StoreId=models.IntegerField()
    StoreName=models.CharField(max_length=60)
    ProductId=models.IntegerField()
    ProductHead=models.CharField(max_length=200)
    AttrId1=models.IntegerField()
    AttrName1=models.CharField(max_length=200)
    AttrImg1=models.ImageField(upload_to='/')
    AttrId2=models.CharField(max_length=200)
    AttrName2=models.CharField(max_length=200)
    PriceId=models.IntegerField()
    Price=models.IntegerField()
    SumPrice=models.FloatField()
    Mount=models.IntegerField()
   

#order num
class Order(models.Model):
    Nid=models.AutoField(primary_key=True)
    OrderNum=models.CharField(max_length=17)
    DateTime=models.DateTimeField()
    StoreId=models.IntegerField()
    StoreName=models.CharField(max_length=60)
    UserId=models.ForeignKey(Userinfo)
    Total=models.FloatField()
    
#order product
#upload='/',is to say no upload 
class OrderProduct(models.Model):
    Nid=models.AutoField(primary_key=True)
    OrderId=models.ForeignKey(Order)
    ProductId=models.IntegerField()
    ProductHead=models.CharField(max_length=200)
    AttrName1=models.CharField(max_length=200)
    AttrImg1=models.ImageField(upload_to='/')
    AttrName2=models.CharField(max_length=200)
    Price=models.FloatField()
    Mount=models.IntegerField()
    SumPrice=models.FloatField()
    
    