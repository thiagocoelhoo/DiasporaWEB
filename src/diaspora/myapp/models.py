from django.db import models

# Create your models here.

class SensorData(models.Model):
    gas = models.IntegerField()
    temp = models.FloatField()
