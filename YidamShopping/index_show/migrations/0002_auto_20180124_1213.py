# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-01-24 12:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index_show', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sysstore',
            old_name='StoreNid',
            new_name='SysStoreNid',
        ),
        migrations.RenameField(
            model_name='sysstore',
            old_name='StoreOrder',
            new_name='SysStoreOrder',
        ),
    ]