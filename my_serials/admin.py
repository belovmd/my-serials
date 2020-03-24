from django.contrib import admin
from . import models


@admin.register(models.Serial)
class SerialAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'serial_id', 'air_date', 'owner')


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
