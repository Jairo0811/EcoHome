from rest_framework import serializers

from .models import Device, Telemetry


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            "id",
            "home",
            "room",
            "external_id",
            "name",
            "device_type",
            "status",
            "last_seen_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class TelemetrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Telemetry
        fields = ["id", "device", "metric", "value", "unit", "recorded_at"]
        read_only_fields = ["id"]
