from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from apps.homes.views import accessible_homes
from .models import Alert, AutomationRule
from .serializers import AlertSerializer, AutomationExecutionSerializer, AutomationRuleSerializer
from .services import execute_rule


class AlertViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AlertSerializer

    def get_queryset(self):
        queryset = Alert.objects.select_related("home", "device").filter(home__in=accessible_homes(self.request.user))
        status_filter = self.request.query_params.get("status")
        return queryset.filter(status=status_filter) if status_filter in Alert.Status.values else queryset

    @action(detail=True, methods=["post"])
    def acknowledge(self, request, pk=None):
        alert = self.get_object()
        alert.status = Alert.Status.ACKNOWLEDGED
        alert.save(update_fields=["status", "updated_at"])
        return Response(self.get_serializer(alert).data)

    @action(detail=True, methods=["post"])
    def resolve(self, request, pk=None):
        alert = self.get_object()
        alert.status = Alert.Status.RESOLVED
        alert.resolved_at = timezone.now()
        alert.save(update_fields=["status", "resolved_at", "updated_at"])
        return Response(self.get_serializer(alert).data)


class AutomationRuleViewSet(viewsets.ModelViewSet):
    serializer_class = AutomationRuleSerializer

    def get_queryset(self):
        return AutomationRule.objects.prefetch_related("executions").filter(home__in=accessible_homes(self.request.user))

    def _ensure_manage(self, home):
        if not home.user_can_manage(self.request.user):
            raise PermissionDenied("No tienes permisos para modificar automatizaciones en este hogar.")

    def perform_create(self, serializer):
        self._ensure_manage(serializer.validated_data["home"])
        serializer.save()

    def perform_update(self, serializer):
        self._ensure_manage(serializer.instance.home)
        serializer.save()

    def perform_destroy(self, instance):
        self._ensure_manage(instance.home)
        instance.delete()

    @action(detail=True, methods=["post"])
    def execute(self, request, pk=None):
        rule = self.get_object()
        self._ensure_manage(rule.home)
        execution = execute_rule(rule, force=True)
        if not execution:
            return Response({"status": "not_executed", "detail": "La regla está deshabilitada."}, status=status.HTTP_409_CONFLICT)
        return Response(AutomationExecutionSerializer(execution).data, status=status.HTTP_202_ACCEPTED)
