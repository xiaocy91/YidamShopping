# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-12-18 11:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_center', '0002_userinfo_openstore'),
    ]

    operations = [
        migrations.CreateModel(
            name='store',
            fields=[
                ('StoreNid', models.AutoField(primary_key=True, serialize=False)),
                ('StoreName', models.CharField(max_length=60)),
                ('StoreAddr', models.CharField(max_length=60)),
                ('StoreScore', models.FloatField(default=0)),
                ('StoreBossName', models.CharField(max_length=30)),
                ('StoreBossIndentity', models.CharField(max_length=11)),
                ('Userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_center.Userinfo')),
            ],
        ),
    ]
