from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    subscribers = models.ManyToManyField('self', blank=True)
    color = models.CharField(blank=True, null=True, max_length=6)

