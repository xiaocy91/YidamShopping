# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-01-05 08:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0010_remove_hometype_productnid'),
    ]

    operations = [
        migrations.AddField(
            model_name='hometype',
            name='TypeOrder',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
