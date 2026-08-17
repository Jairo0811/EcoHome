from rest_framework import viewsets

from .models import Device, Telemetry
from .serializers import DeviceSerializer, TelemetrySerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.select_related("home", "room").all()
    serializer_class = DeviceSerializer


class TelemetryViewSet(viewsets.ModelViewSet):
    queryset = Telemetry.objects.select_related("device").all()
    serializer_class = TelemetrySerializer
