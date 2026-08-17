from rest_framework import serializers

from .models import ResourceLimit


class ResourceLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceLimit
        fields = ["id", "home", "metric", "daily_limit", "warning_percent", "active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_daily_limit(self, value):
        if value <= 0:
            raise serializers.ValidationError("El límite diario debe ser mayor que cero.")
        return value
