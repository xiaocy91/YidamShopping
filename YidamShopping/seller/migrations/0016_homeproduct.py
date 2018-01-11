# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-01-09 04:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0015_auto_20180109_1153'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeProduct',
            fields=[
                ('HomeProductNid', models.AutoField(primary_key=True, serialize=False)),
                ('ProductOrder', models.IntegerField()),
                ('ProductNid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.Product')),
                ('StoreNid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.Store')),
            ],
        ),
    ]