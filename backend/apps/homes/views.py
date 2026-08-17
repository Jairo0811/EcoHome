from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from .models import Home, Room
from .serializers import HomeSerializer, RoomSerializer


class HomeViewSet(viewsets.ModelViewSet):
    serializer_class = HomeSerializer

    def get_queryset(self):
        queryset = Home.objects.prefetch_related("rooms").all()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer

    def get_queryset(self):
        queryset = Room.objects.select_related("home").all()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(home__owner=self.request.user)

    def perform_create(self, serializer):
        home = serializer.validated_data["home"]
        if not self.request.user.is_staff and home.owner_id != self.request.user.id:
            raise PermissionDenied("No puedes crear habitaciones en un hogar que no te pertenece.")
        serializer.save()
