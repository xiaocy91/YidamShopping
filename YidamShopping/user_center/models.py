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
