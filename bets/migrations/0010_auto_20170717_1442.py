# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-17 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0009_auto_20170717_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bet',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
    ]
