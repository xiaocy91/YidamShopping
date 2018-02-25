# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-02-20 17:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index_show', '0004_sysproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sysproduct',
            name='SysProNid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.Product'),
        ),
        migrations.AlterField(
            model_name='sysstore',
            name='SysStoreNid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.Store'),
        ),
    ]