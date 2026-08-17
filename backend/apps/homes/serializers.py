from rest_framework import serializers

from .models import Home, Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "home", "name", "created_at"]
        read_only_fields = ["id", "created_at"]


class HomeSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)

    class Meta:
        model = Home
        fields = ["id", "name", "address", "timezone", "created_at", "updated_at", "rooms"]
        read_only_fields = ["id", "created_at", "updated_at"]
