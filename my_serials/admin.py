from django.contrib import admin
from . import models


@admin.register(models.Serial)
class SerialAdmin(admin.ModelAdmin):
    list_display = ('title', 'serial_id', 'air_date')
    # list_display = ('title', 'slug', 'material_type', 'status', 'publish')
    # list_filter = ('status', 'created', 'publish', 'material_type')
    # search_fields = ('title', 'body')
    # prepopulated_fields = {'slug': ('title', )}
    # date_hierarchy = 'publish'
    # ordering = ('status', 'publish')
