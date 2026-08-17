from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.devices.models import Device
from apps.homes.views import accessible_homes
from .services import command_topic, ingest_message, mqtt_configuration, publish_command, telemetry_topic


@api_view(["GET"])
def configuration(request):
    return Response(mqtt_configuration())


@api_view(["GET"])
def topics(request):
    devices = Device.objects.filter(home__in=accessible_homes(request.user)).select_related("home")
    return Response([
        {"deviceId": d.id, "externalId": d.external_id, "telemetryTopic": telemetry_topic(d), "commandTopic": command_topic(d)}
        for d in devices
    ])


@api_view(["POST"])
def ingest(request, external_id: str):
    device = Device.objects.select_related("home").filter(external_id=external_id, home__in=accessible_homes(request.user)).first()
    if not device:
        return Response({"detail": "Dispositivo no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    if not device.home.user_can_manage(request.user):
        return Response({"detail": "No tienes permisos para este dispositivo."}, status=status.HTTP_403_FORBIDDEN)
    result = ingest_message(external_id, request.data)
    return Response({"deviceId": result.device_id, "telemetryId": result.telemetry_id, "status": result.status}, status=status.HTTP_202_ACCEPTED)


@api_view(["POST"])
def command(request, device_id: int):
    device = Device.objects.select_related("home").filter(id=device_id, home__in=accessible_homes(request.user)).first()
    if not device:
        return Response({"detail": "Dispositivo no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    if not device.home.user_can_manage(request.user):
        return Response({"detail": "No tienes permisos para controlar este dispositivo."}, status=status.HTTP_403_FORBIDDEN)
    publish_command(device, request.data)
    return Response({"status": "queued", "topic": command_topic(device)}, status=status.HTTP_202_ACCEPTED)
