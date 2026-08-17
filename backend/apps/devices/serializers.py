from rest_framework import serializers

from .models import Device, Telemetry


class DeviceSerializer(serializers.ModelSerializer):
    room_name = serializers.CharField(source="room.name", read_only=True)

    class Meta:
        model = Device
        fields = ["id", "home", "room", "room_name", "external_id", "name", "device_type", "status", "last_seen_at", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        home = attrs.get("home") or getattr(self.instance, "home", None)
        room = attrs.get("room")
        if room and home and room.home_id != home.id:
            raise serializers.ValidationError({"room": "La habitación debe pertenecer al mismo hogar del dispositivo."})
        return attrs


class TelemetrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Telemetry
        fields = ["id", "device", "metric", "value", "unit", "recorded_at"]
        read_only_fields = ["id"]
