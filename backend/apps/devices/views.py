from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from .models import Device, Telemetry
from .serializers import DeviceSerializer, TelemetrySerializer


class DeviceViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        queryset = Device.objects.select_related("home", "room").all()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(home__owner=self.request.user)

    def perform_create(self, serializer):
        home = serializer.validated_data["home"]
        if not self.request.user.is_staff and home.owner_id != self.request.user.id:
            raise PermissionDenied("No puedes registrar dispositivos en un hogar que no te pertenece.")
        serializer.save()


class TelemetryViewSet(viewsets.ModelViewSet):
    serializer_class = TelemetrySerializer

    def get_queryset(self):
        queryset = Telemetry.objects.select_related("device", "device__home").all()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(device__home__owner=self.request.user)

    def perform_create(self, serializer):
        device = serializer.validated_data["device"]
        if not self.request.user.is_staff and device.home.owner_id != self.request.user.id:
            raise PermissionDenied("No puedes registrar telemetría para este dispositivo.")
        serializer.save()
