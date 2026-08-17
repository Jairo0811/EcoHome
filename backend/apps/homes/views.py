from rest_framework import viewsets

from .models import Home, Room
from .serializers import HomeSerializer, RoomSerializer


class HomeViewSet(viewsets.ModelViewSet):
    queryset = Home.objects.prefetch_related("rooms").all()
    serializer_class = HomeSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.select_related("home").all()
    serializer_class = RoomSerializer
