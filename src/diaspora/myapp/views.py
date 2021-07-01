from os import listdir
import os

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from . import models


@login_required
def home_view(request):
    print(os.getcwd())
    images = listdir('myapp/static/camera_images/')
    images.sort()
    images.reverse()
    
    context = {
        'images': images[:10]
    }

    return render(request, 'home.html', context)


@login_required
def settings_arduino_view(request):
    return render(request, 'settings-arduino.html')


@login_required
def settings_camera_view(request):
    return render(request, 'settings-camera.html')


@login_required
def settings_notifications_view(request):
    return render(request, 'settings-notifications.html')


def get_sensor_data(request):
    gas = [0] * 50
    sensors = list(models.SensorData.objects.all())
    for i, s in enumerate(sensors[:50]):
        gas[i] = s.gas
    return JsonResponse({"data": gas})