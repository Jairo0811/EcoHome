from rest_framework import serializers
from apps.devices.models import Device
from .models import SecurityEvent, SecurityState


class SecurityStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityState
        fields = ["id", "home", "mode", "updated_at"]
        read_only_fields = ["id", "home", "updated_at"]


class SecurityEventSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source="device.name", read_only=True)
    class Meta:
        model = SecurityEvent
        fields = ["id", "home", "device", "device_name", "event_type", "severity", "message", "metadata", "occurred_at", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        device = attrs.get("device")
        home = attrs.get("home")
        if device and home and device.home_id != home.id:
            raise serializers.ValidationError({"device": "El dispositivo debe pertenecer al hogar del evento."})
        if device and device.device_type not in {Device.DeviceType.CAMERA, Device.DeviceType.MOTION_SENSOR, Device.DeviceType.DOOR_SENSOR}:
            raise serializers.ValidationError({"device": "El dispositivo no es compatible con eventos de seguridad."})
        return attrs
