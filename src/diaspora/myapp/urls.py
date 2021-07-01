from django.urls import path

from . import views

urlpatterns = [
    path('' , views.home_view, name='home'),
    path('settings/arduino' , views.settings_arduino_view, name='settings_arduino'),
    path('settings/cameras', views.settings_camera_view, name='settings_cameras'),
    path('settings/notifications', views.settings_notifications_view, name='settings_cameras'),
    path('api/arduino', views.get_sensor_data, name='api_arduino'),
]