# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-01-25 17:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0018_product_procontent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='ProContent',
            field=models.TextField(blank=True, null=True),
        ),
    ]
