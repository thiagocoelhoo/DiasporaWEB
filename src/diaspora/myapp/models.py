from django.contrib.auth import decorators
from django.db import models


class Arduino(models.Model):
    name = models.CharField(max_length=12)
    path = models.CharField(max_length=12)
    description = models.TextField(max_length=40, blank=True)

    def __str__(self):
        return self.name


class Camera(models.Model):
    name = models.CharField(max_length=12)
    path = models.CharField(max_length=12)
    description = models.TextField(max_length=40, blank=True)

    def __str__(self):
        return self.name


class SensorData(models.Model):
    gas = models.IntegerField()
    temp = models.FloatField()


class Settings(models.Model):
    image_store_limit = models.FloatField()
    max_temperature = models.FloatField()
    min_distance_people = models.FloatField()
    min_rate_gases = models.IntegerField()
