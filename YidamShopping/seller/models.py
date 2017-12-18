from __future__ import unicode_literals

from django.db import models
from user_center.models import Userinfo

# Create your models here.

class Store(models.Model):
    StoreNid=models.AutoField(primary_key=True)
    Userid=models.ForeignKey(Userinfo)
    StoreName=models.CharField(max_length=60)
    StoreAddr=models.CharField(max_length=60)
    StoreScore=models.FloatField(default=0)
    StoreBossName=models.CharField(max_length=30)
    StoreBossIndentity=models.CharField(max_length=11)