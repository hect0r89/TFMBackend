# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-03 09:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20170703_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='_user_subscribers_+', to=settings.AUTH_USER_MODEL),
        ),
    ]
