from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Serial(models.Model):
    serial_id = models.IntegerField(unique=True)
    poster_path = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    air_date = models.CharField(max_length=50)
    objects = models.Manager()
