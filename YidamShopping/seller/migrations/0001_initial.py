# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-12-27 10:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_center', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('Nid', models.AutoField(primary_key=True, serialize=False)),
                ('Head', models.CharField(max_length=200)),
                ('AttributeName1', models.CharField(default='foobar', max_length=200)),
                ('AttributeName2', models.CharField(default='2', max_length=200)),
                ('DefaultImg', models.IntegerField(blank=True, null=True)),
                ('DefaultPrice', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductHome',
            fields=[
                ('HomeNid', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('Nid', models.AutoField(primary_key=True, serialize=False)),
                ('Img', models.ImageField(upload_to='img/%Y%m%d%H%M%S')),
                ('ProductNid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.Product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSecondType',
            fields=[
                ('SecondTypeNid', models.AutoField(primary_key=True, serialize=False)),
                ('SecondTypeName', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('TypeNid', models.AutoField(primary_key=True, serialize=False)),
                ('TypeName', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('StoreNid', models.AutoField(primary_key=True, serialize=False)),
                ('StoreName', models.CharField(max_length=60)),
                ('StoreAddr', models.CharField(max_length=60)),
                ('StoreScore', models.FloatField(default=0)),
                ('StoreBossName', models.CharField(max_length=30)),
                ('StoreBossIndentity', models.CharField(max_length=11)),
                ('UserNid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_center.Userinfo')),
            ],
        ),
        migrations.AddField(
            model_name='producttype',
            name='StoreNid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.Store'),
        ),
        migrations.AddField(
            model_name='productsecondtype',
            name='TypeNid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.ProductType'),
        ),
        migrations.AddField(
            model_name='producthome',
            name='StoreNid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.Store'),
        ),
        migrations.AddField(
            model_name='producthome',
            name='TypeNid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.ProductType'),
        ),
        migrations.AddField(
            model_name='product',
            name='TypeNid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.ProductSecondType'),
        ),
    ]
