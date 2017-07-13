import datetime
from django.db import models

from accounts.models import Account
from users.models import User


class Bet(models.Model):
    PENDING = "P"
    WIN = "W"
    LOST = "L"
    NULL = "N"
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (WIN, 'Win'),
        (LOST, 'Lost'),
        (NULL, 'Null')
    )

    event = models.CharField('Event', blank=True, null=True, max_length=50)
    type = models.CharField('Type', blank=True, null=True, max_length=50)
    pick = models.CharField('Pick', blank=False, null=False, max_length=200, default="Default")
    account = models.ForeignKey(Account, blank=False, null=False)
    stake = models.FloatField('Stake', blank=False, null=False, default=0.1)
    amount = models.FloatField('Amount', blank=False, null=False, default=50)
    odds = models.FloatField('Odds', blank=False, null=False, default=1.85)
    status = models.CharField('State', choices=STATUS_CHOICES, default=PENDING, blank=False, null=False, max_length=1)
    user = models.ForeignKey(User, blank=False, null=False)
    month_year = models.CharField("Month-Year", default='{}-{}'.format(datetime.datetime.now().month, datetime.datetime.now().year), max_length=7)
    month = models.IntegerField("Month", default=datetime.datetime.now().month)
    tipster = models.CharField("Tipster", blank=True, null=True, max_length=100)
    created_at = models.DateTimeField("Created at", auto_now_add=True)

