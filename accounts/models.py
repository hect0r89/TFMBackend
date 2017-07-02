from django.db import models


class Account(models.Model):
    bank = models.FloatField('Bank', blank=False, null=False)
    bookie = models.CharField('Bookie', blank=False, null=False, max_length=100)
