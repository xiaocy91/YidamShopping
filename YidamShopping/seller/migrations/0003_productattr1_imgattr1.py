# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-12-29 12:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0002_auto_20171229_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='productattr1',
            name='ImgAttr1',
            field=models.ImageField(default=1, upload_to='minImg/%Y%m%d%H%M%S'),
            preserve_default=False,
        ),
    ]
