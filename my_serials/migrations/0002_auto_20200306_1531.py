# Generated by Django 3.0.4 on 2020-03-06 12:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my_serials', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serial',
            name='slug',
        ),
        migrations.AddField(
            model_name='serial',
            name='owner',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='user_serials', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='serial',
            name='poster_path',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='serial',
            name='air_date',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='serial',
            name='serial_id',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='serial',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
