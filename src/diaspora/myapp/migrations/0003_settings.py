# Generated by Django 3.2.5 on 2021-08-05 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_arduino_camera'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_store_limit', models.FloatField()),
                ('max_temperature', models.FloatField()),
                ('min_distance_people', models.FloatField()),
                ('min_rate_gases', models.IntegerField()),
            ],
        ),
    ]
