# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-12-31 05:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0004_auto_20171230_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='productprice',
            name='ProductNid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='seller.Product'),
            preserve_default=False,
        ),
    ]
