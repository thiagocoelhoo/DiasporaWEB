from os import listdir
import os

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import StreamingHttpResponse

from . import models
from . import forms

import os
import re
import mimetypes
from wsgiref.util import FileWrapper

from django.http.response import StreamingHttpResponse


range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)


class RangeFileWrapper(object):
    def __init__(self, filelike, blksize=1024, offset=0, length=None):
        self.filelike = filelike
        self.filelike.seek(offset, os.SEEK_SET)
        self.remaining = length
        self.blksize = blksize

    def close(self):
        if hasattr(self.filelike, 'close'):
            self.filelike.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining is None:
            # If remaining is None, we're reading the entire file.
            data = self.filelike.read(self.blksize)
            if data:
                return data
            raise StopIteration()
        else:
            if self.remaining <= 0:
                raise StopIteration()
            data = self.filelike.read(min(self.remaining, self.blksize))
            if not data:
                raise StopIteration()
            self.remaining -= len(data)
            return data


def stream_video(request):
    path = 'myapp/static/video.mp4'

    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = range_re.match(range_header)
    size = os.path.getsize(path)
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(RangeFileWrapper(open(path, 'rb'), offset=first_byte, length=length), status=206, content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    
    return resp


def read_video(offset=0, chunksize=1024):
    path = 'myapp/static/video.mp4'
    video = open(path, 'rb')
    video.seek(offset, os.SEEK_SET)
    yield video.read(chunksize)
    video.close()


def mystream_video(request):
    range_header = request.META.get('HTTP_RANGE', '').strip()
    print("range header:", range_header)
    return StreamingHttpResponse(read_video(), status=206)


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
    arduinos = models.Arduino.objects.all()
    context = {
        'add_arduino_form': forms.AddArduinoForm(),
        'arduinos': arduinos
    }
    
    return render(request, 'settings-arduino.html', context)


@login_required
def settings_camera_view(request):
    return render(request, 'settings-camera.html')


@login_required
def settings_notifications_view(request):
    return render(request, 'settings-notifications.html')


@login_required
def get_sensor_data(request):
    gas = [0] * 50
    sensors = list(models.SensorData.objects.all())
    for i, s in enumerate(sensors[:50]):
        gas[i] = s.gas
    return JsonResponse({"data": gas})


@login_required
@require_POST
def add_arduino(request):
    form  = forms.AddArduinoForm(request.POST)
    
    if form.is_valid():
        form.save()
        return HttpResponse('Success.')

    return HttpResponse('Invalid data.')


@login_required
def remove_arduino(request, pk):
    try:
        arduino = models.Arduino.objects.get(id=pk)
        arduino.delete()
    except:
        return HttpResponse('Invalid data.')
    finally:
        return HttpResponse('Sucess.')


@login_required
def update_arduinos(request):
    pass


@login_required
@require_POST
def add_camera(request):
    form  = forms.AddCameraForm(request.POST)
    
    if form.is_valid():
        form.save()
        return HttpResponse('Success.')

    return HttpResponse('Invalid data.')


@login_required
def remove_camera(request, pk):
    try:
        cam = models.Camera.objects.get(id=pk)
        cam.delete()
    except:
        return HttpResponse('Invalid data.')
    finally:
        return HttpResponse('Sucess.')


@login_required
def update_cameras(request):
    pass
