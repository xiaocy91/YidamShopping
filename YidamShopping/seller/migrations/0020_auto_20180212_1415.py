# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-02-12 14:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0019_auto_20180125_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productattr1',
            name='ImgAttr1',
            field=models.ImageField(upload_to='proMinImg/%Y%m%d%H%M%S'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='Img',
            field=models.ImageField(upload_to='proImg/%Y%m%d%H%M%S'),
        ),
    ]
