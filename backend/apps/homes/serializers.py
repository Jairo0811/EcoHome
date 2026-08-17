from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Home, HomeMembership, Room

User = get_user_model()


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "home", "name", "created_at"]
        read_only_fields = ["id", "created_at"]


class MembershipSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source="user", queryset=User.objects.all(), write_only=True)

    class Meta:
        model = HomeMembership
        fields = ["id", "home", "user_id", "username", "email", "role", "created_at"]
        read_only_fields = ["id", "home", "username", "email", "created_at"]


class HomeSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)
    memberships = MembershipSerializer(many=True, read_only=True)
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Home
        fields = ["id", "owner", "name", "address", "timezone", "created_at", "updated_at", "rooms", "memberships"]
        read_only_fields = ["id", "owner", "created_at", "updated_at"]
