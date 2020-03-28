# Generated by Django 3.0.4 on 2020-03-04 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Serial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_id', models.IntegerField()),
                ('title', models.CharField(max_length=250)),
                ('air_date', models.CharField(max_length=250)),
                ('slug', models.SlugField(max_length=250)),
            ],
        ),
    ]
