from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

import tmdbsimple as tmdb
tmdb.API_KEY = '71af347ad6265c67d36f595aa27ea28c'


class Serial(models.Model):
    serial_id = models.IntegerField()
    serial_db = tmdb.TV(1412)
    response = serial_db.info()
    title = response['name']
    air_date = response['first_air_date'][0:4]
    objects = models.Manager()
