from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

import tmdbsimple as tmdb
tmdb.API_KEY = '71af347ad6265c67d36f595aa27ea28c'


class Serial(models.Model):
    serial_id = models.IntegerField()
    # poster_path = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    air_date = models.CharField(max_length=50)
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='user_serials')
    objects = models.Manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['serial_id', 'owner'], name='unique_serial_for_user')
        ]

    def last_to_air(self):
        tv = tmdb.TV(self.serial_id).info()
        if tv['last_episode_to_air']:
            result = {
                'last_date': tv['last_episode_to_air']['air_date'],
                'last_name': tv['last_episode_to_air']['name'],
                'overview': tv['last_episode_to_air']['overview'],
            }
        else:
            result = {}
        return result

    def next_to_air(self):
        tv = tmdb.TV(self.serial_id).info()
        if tv['next_episode_to_air']:
            result = {
                'next_date': tv['next_episode_to_air']['air_date'],
                'next_name': tv['next_episode_to_air']['name'],
                'overview': tv['next_episode_to_air']['overview'],
            }
        else:
            result = {}
        return result

    def serial_info(self):
        tv = tmdb.TV(self.serial_id).info()
        result = {
            'poster_path': tv['poster_path'],
        }
        return result
