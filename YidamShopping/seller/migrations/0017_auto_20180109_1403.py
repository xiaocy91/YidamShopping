# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-01-09 06:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0016_homeproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeproduct',
            name='ProductNid',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='seller.Product'),
        ),
    ]
