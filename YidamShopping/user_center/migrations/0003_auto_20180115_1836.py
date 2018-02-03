# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-01-15 10:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_center', '0002_shopcar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopcar',
            old_name='ProductImg',
            new_name='AttrImg1',
        ),
        migrations.RenameField(
            model_name='shopcar',
            old_name='ProductPrice',
            new_name='Price',
        ),
        migrations.AddField(
            model_name='shopcar',
            name='AttrId1',
            field=models.ImageField(default=1, upload_to=b''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shopcar',
            name='AttrId2',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shopcar',
            name='AttrName1',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shopcar',
            name='AttrName2',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shopcar',
            name='PriceId',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]