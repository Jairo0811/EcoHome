from django.urls import path

from .views import command, configuration, ingest, topics

urlpatterns = [
    path("config/", configuration, name="iot-config"),
    path("topics/", topics, name="iot-topics"),
    path("ingest/<str:external_id>/", ingest, name="iot-ingest"),
    path("devices/<int:device_id>/command/", command, name="iot-command"),
]
