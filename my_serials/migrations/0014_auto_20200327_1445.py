# Generated by Django 3.0.4 on 2020-03-27 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_serials', '0013_auto_20200327_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serial',
            name='air_date',
            field=models.CharField(max_length=4),
        ),
    ]