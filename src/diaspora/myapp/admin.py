from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Arduino)
admin.site.register(models.Camera)
admin.site.register(models.SensorData)
