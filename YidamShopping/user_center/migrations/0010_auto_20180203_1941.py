# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-02-03 19:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_center', '0009_auto_20180202_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='Total',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='SumPrice',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='shopcar',
            name='SumPrice',
            field=models.FloatField(),
        ),
    ]
