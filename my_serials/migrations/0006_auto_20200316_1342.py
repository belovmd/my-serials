# Generated by Django 3.0.4 on 2020-03-16 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_serials', '0005_auto_20200309_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serial',
            name='air_date',
            field=models.CharField(default='N/A', max_length=50),
        ),
    ]
