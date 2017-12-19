from __future__ import unicode_literals

from django.db import models
from user_center.models import Userinfo

# Create your models here.

class Store(models.Model):
    StoreNid=models.AutoField(primary_key=True)
    UserNid=models.ForeignKey(Userinfo)
    StoreName=models.CharField(max_length=60)
    StoreAddr=models.CharField(max_length=60)
    StoreScore=models.FloatField(default=0)
    StoreBossName=models.CharField(max_length=30)
    StoreBossIndentity=models.CharField(max_length=11)
    


class ProductType(models.Model):
    TypeNid=models.AutoField(primary_key=True)
    StoreNid=models.ForeignKey(Store)
    TypeName=models.CharField(max_length=150)

class ProductSecondType(models.Model):
        SecondTypeNid=models.AutoField(primary_key=True)
        TypeNid=models.ForeignKey(ProductType)
        SecondTypeName=models.CharField(max_length=150)
    
class ProductHome(models.Model):  
      HomeNid=models.AutoField(primary_key=True)
      StoreNid=models.ForeignKey(Store)
      TypeNid=models.ForeignKey(ProductType)
      