# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-03 14:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0003_bet_tipster'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bet',
            name='month',
        ),
        migrations.AddField(
            model_name='bet',
            name='month_year',
            field=models.CharField(default='7-2017', max_length=7, verbose_name='Mes'),
        ),
    ]
