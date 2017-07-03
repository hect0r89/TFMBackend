from django.db import models

from users.models import User


class Account(models.Model):
    bank = models.FloatField('Bank', blank=False, null=False)
    bookie = models.CharField('Bookie', blank=False, null=False, max_length=100)
    user = models.ForeignKey(User, blank=False, null=False)
