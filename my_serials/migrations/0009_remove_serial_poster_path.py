# Generated by Django 3.0.4 on 2020-03-16 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_serials', '0008_auto_20200316_1511'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serial',
            name='poster_path',
        ),
    ]
