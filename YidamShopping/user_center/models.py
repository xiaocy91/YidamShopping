from __future__ import unicode_literals

from django.db import models



# Create your models here.

class Userinfo(models.Model):
    Userid=models.AutoField(primary_key=True)
    Account=models.CharField(max_length=20)
    Password=models.CharField(max_length=20)
    Phone=models.CharField(max_length=11,null=True)
    Nickname=models.CharField(max_length=20,null=True)
    Headphoto=models.CharField(max_length=255,null=True)
    Email=models.CharField(max_length=20,null=True)
    OpenStore=models.BooleanField(default=False)
    
    
class ShopCar(models.Model):
    Nid=models.AutoField(primary_key=True)
    UserNid=models.ForeignKey(Userinfo)
    StoreId=models.IntegerField()
    StoreName=models.CharField(max_length=60)
    ProductId=models.IntegerField()
    ProductHead=models.CharField(max_length=200)
    AttrId1=models.IntegerField()
    AttrName1=models.CharField(max_length=200)
    AttrImg1=models.ImageField()
    AttrId2=models.CharField(max_length=200)
    AttrName2=models.CharField(max_length=200)
    PriceId=models.IntegerField()
    Price=models.IntegerField()
    SumPrice=models.IntegerField()
    Mount=models.IntegerField()

class Order(models.Model):
    Nid=models.AutoField(primary_key=True)
    OrderNum=models.CharField(max_length=17)
    DateTime=models.DateTimeField()
    StoreId=models.IntegerField()
    StoreName=models.CharField(max_length=60)
    UserId=models.ForeignKey(Userinfo)
    Total=models.IntegerField()
    
class OrderProduct(models.Model):
    Nid=models.AutoField(primary_key=True)
    OrderId=models.ForeignKey(Order)
    ProductId=models.IntegerField()
    ProductHead=models.CharField(max_length=200)
    AttrName1=models.CharField(max_length=200)
    AttrImg1=models.ImageField()
    AttrName2=models.CharField(max_length=200)
    Price=models.IntegerField()
    Mount=models.IntegerField()
    SumPrice=models.IntegerField()
    
    