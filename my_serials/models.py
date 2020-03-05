from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Serial(models.Model):
    poster_path = models.CharField(max_length=100)
    serial_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=50)
    air_date = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('my_serials:serial_details',
                       args=[self.serial_id, self.slug])
