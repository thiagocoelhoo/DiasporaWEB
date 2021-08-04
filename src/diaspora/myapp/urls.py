from django.urls import path

from . import views

urlpatterns = [
    path('' , views.home_view, name='home'),
    path('settings/arduino' , views.settings_arduino_view, name='settings_arduino'),
    path('settings/cameras', views.settings_camera_view, name='settings_cameras'),
    path('settings/notifications', views.settings_notifications_view, name='settings_cameras'),
    path('api/arduino', views.get_sensor_data, name='api_arduino'),
    path('arduino/add/', views.add_arduino, name='add_arduino'),
    path('arduino/remove/<int:pk>/', views.remove_arduino, name='remove_arduino'),
    path('arduino/update/', views.update_arduinos, name='update_arduinos'),
    path('camera/add/', views.add_camera, name='add_camera'),
    path('camera/remove/<int:pk>/', views.remove_camera, name='remove_camera'),
    path('camera/update/', views.update_cameras, name='update_cameras'),
    path('video', views.stream_video)
]