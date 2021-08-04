from django.urls import path

from myapp import consumers

ws_urlpatterns = [
    path('consumers/arduino', consumers.ArduinoConsumer.as_asgi()),
    path('consumers/notifications', consumers.NotifycationConsumer.as_asgi()),
    path('consumers/videostream', consumers.VideoStreamConsumer.as_asgi()),
]
