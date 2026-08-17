from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from apps.homes.views import accessible_homes
from .models import Device, Telemetry
from .serializers import DeviceSerializer, TelemetrySerializer


class DeviceViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return Device.objects.select_related("home", "room").filter(home__in=accessible_homes(self.request.user))

    def _ensure_manage(self, home):
        if not home.user_can_manage(self.request.user):
            raise PermissionDenied("No tienes permisos para modificar dispositivos en este hogar.")

    def perform_create(self, serializer):
        self._ensure_manage(serializer.validated_data["home"])
        serializer.save()

    def perform_update(self, serializer):
        self._ensure_manage(serializer.instance.home)
        serializer.save()

    def perform_destroy(self, instance):
        self._ensure_manage(instance.home)
        instance.delete()


class TelemetryViewSet(viewsets.ModelViewSet):
    serializer_class = TelemetrySerializer
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        return Telemetry.objects.select_related("device", "device__home").filter(device__home__in=accessible_homes(self.request.user))

    def perform_create(self, serializer):
        device = serializer.validated_data["device"]
        if not device.home.user_can_manage(self.request.user):
            raise PermissionDenied("No tienes permisos para registrar telemetría en este hogar.")
        serializer.save()
