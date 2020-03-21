from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver


class Serial(models.Model):
    serial_id = models.IntegerField()
    title = models.CharField(max_length=50)
    air_date = models.CharField(max_length=50, default='N/A')
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='user_serials')
    objects = models.Manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['serial_id', 'owner'], name='unique_serial_for_user')
        ]

    # very slow page load
    # def serial_info(self):
    #     tv = tmdb.TV(self.serial_id).info()
    #     result = {'poster_path': tv['poster_path']}
    #     if tv['last_episode_to_air']:
    #         result['last_date'] = tv['last_episode_to_air']['air_date']
    #         result['last_name'] = tv['last_episode_to_air']['name']
    #         result['last_overview'] = tv['last_episode_to_air']['overview']
    #     if tv['next_episode_to_air']:
    #         result['next_date'] = tv['next_episode_to_air']['air_date']
    #         result['next_name'] = tv['next_episode_to_air']['name']
    #         result['next_overview'] = tv['next_episode_to_air']['overview']
    #     return result


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    telegram_id = models.IntegerField(blank=True, null=True, unique=True)

    def __str__(self):
        return "Profile for {}".format(self.user.username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
