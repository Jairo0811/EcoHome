from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Home, HomeMembership, Room
from .serializers import HomeSerializer, MembershipSerializer, RoomSerializer


def accessible_homes(user):
    queryset = Home.objects.all()
    if user.is_staff:
        return queryset
    return queryset.filter(Q(owner=user) | Q(memberships__user=user)).distinct()


class HomeViewSet(viewsets.ModelViewSet):
    serializer_class = HomeSerializer

    def get_queryset(self):
        return accessible_homes(self.request.user).prefetch_related("rooms", "memberships__user")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        if not serializer.instance.user_can_manage(self.request.user):
            raise PermissionDenied("Solo propietarios o administradores pueden modificar el hogar.")
        serializer.save()

    def perform_destroy(self, instance):
        if not (self.request.user.is_staff or instance.owner_id == self.request.user.id):
            raise PermissionDenied("Solo el propietario puede eliminar el hogar.")
        instance.delete()

    @action(detail=True, methods=["get", "post"], url_path="members")
    def members(self, request, pk=None):
        home = self.get_object()
        if request.method == "GET":
            return Response(MembershipSerializer(home.memberships.select_related("user"), many=True).data)
        if not home.user_can_manage(request.user):
            raise PermissionDenied("No tienes permisos para administrar miembros.")
        serializer = MembershipSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if user.id == home.owner_id:
            return Response({"detail": "El propietario ya tiene acceso total."}, status=status.HTTP_400_BAD_REQUEST)
        membership, created = HomeMembership.objects.update_or_create(home=home, user=user, defaults={"role": serializer.validated_data["role"]})
        return Response(MembershipSerializer(membership).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=["delete"], url_path=r"members/(?P<user_id>[^/.]+)")
    def remove_member(self, request, pk=None, user_id=None):
        home = self.get_object()
        if not home.user_can_manage(request.user):
            raise PermissionDenied("No tienes permisos para administrar miembros.")
        deleted, _ = home.memberships.filter(user_id=user_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT if deleted else status.HTTP_404_NOT_FOUND)


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer

    def get_queryset(self):
        return Room.objects.select_related("home").filter(home__in=accessible_homes(self.request.user))

    def _ensure_manage(self, home):
        if not home.user_can_manage(self.request.user):
            raise PermissionDenied("No tienes permisos para modificar habitaciones en este hogar.")

    def perform_create(self, serializer):
        self._ensure_manage(serializer.validated_data["home"])
        serializer.save()

    def perform_update(self, serializer):
        self._ensure_manage(serializer.instance.home)
        serializer.save()

    def perform_destroy(self, instance):
        self._ensure_manage(instance.home)
        instance.delete()
