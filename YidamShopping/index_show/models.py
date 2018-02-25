from __future__ import unicode_literals

from django.db import models

from  seller.models import Store

class SysStore(models.Model):
    Nid=models.AutoField(primary_key=True)
    SysStoreNid=models.IntegerField()
    SysStoreImg=models.ImageField(upload_to='SysStoreImg/%Y%m%d%H%M%S')
    SysStoreOrder=models.IntegerField()
    
class SysProduct(models.Model):
    Nid=models.AutoField(primary_key=True)
    SysStoreNid=models.IntegerField()
    SysProNid=models.IntegerField()
    SysProOrder=models.IntegerField()
    