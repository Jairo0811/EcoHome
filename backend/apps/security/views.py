from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from apps.homes.models import Home
from apps.homes.views import accessible_homes
from .models import SecurityEvent, SecurityState
from .serializers import SecurityEventSerializer, SecurityStateSerializer
from .services import process_security_event


class SecurityEventViewSet(viewsets.ModelViewSet):
    serializer_class = SecurityEventSerializer
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        return SecurityEvent.objects.select_related("home", "device").filter(home__in=accessible_homes(self.request.user))

    def perform_create(self, serializer):
        home = serializer.validated_data["home"]
        if not home.user_can_manage(self.request.user):
            raise PermissionDenied("No tienes permisos para registrar eventos de seguridad.")
        event = serializer.save()
        process_security_event(event)


class SecurityStateViewSet(viewsets.ViewSet):
    def list(self, request):
        data = []
        for home in accessible_homes(request.user):
            state, _ = SecurityState.objects.get_or_create(home=home)
            data.append(SecurityStateSerializer(state).data)
        return Response(data)

    @action(detail=False, methods=["patch"], url_path=r"(?P<home_id>\d+)")
    def update_home(self, request, home_id=None):
        home = Home.objects.filter(id=home_id).first()
        if not home or not accessible_homes(request.user).filter(id=home.id).exists():
            return Response({"detail": "Hogar no encontrado."}, status=404)
        if not home.user_can_manage(request.user):
            raise PermissionDenied("No tienes permisos para cambiar el modo de seguridad.")
        state, _ = SecurityState.objects.get_or_create(home=home)
        serializer = SecurityStateSerializer(state, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
