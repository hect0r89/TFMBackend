# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-08 16:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0007_bet_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='month',
            field=models.IntegerField(default=7, verbose_name='Month'),
        ),
    ]