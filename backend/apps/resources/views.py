from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from apps.devices.models import Telemetry
from apps.homes.views import accessible_homes
from .models import ResourceLimit
from .serializers import ResourceLimitSerializer
from .services import RANGE_DAYS, consumption_history, consumption_summary


class ResourceLimitViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceLimitSerializer

    def get_queryset(self):
        return ResourceLimit.objects.select_related("home").filter(home__in=accessible_homes(self.request.user))

    def _ensure_manage(self, home):
        if not home.user_can_manage(self.request.user):
            raise PermissionDenied("No tienes permisos para modificar los límites de este hogar.")

    def perform_create(self, serializer):
        self._ensure_manage(serializer.validated_data["home"])
        serializer.save()

    def perform_update(self, serializer):
        self._ensure_manage(serializer.instance.home)
        serializer.save()

    def perform_destroy(self, instance):
        self._ensure_manage(instance.home)
        instance.delete()


@api_view(["GET"])
def summary(request):
    range_name = request.query_params.get("range", "day")
    if range_name not in RANGE_DAYS:
        return Response({"detail": "range debe ser day, week o month."}, status=status.HTTP_400_BAD_REQUEST)
    home_id = request.query_params.get("home")
    return Response(consumption_summary(request.user, home_id, range_name))


@api_view(["GET"])
def history(request):
    metric = request.query_params.get("metric", Telemetry.Metric.ENERGY_KWH)
    if metric not in {Telemetry.Metric.ENERGY_KWH, Telemetry.Metric.WATER_L, Telemetry.Metric.GAS_M3}:
        return Response({"detail": "Métrica de recurso no válida."}, status=status.HTTP_400_BAD_REQUEST)
    home_id = request.query_params.get("home")
    try:
        days = int(request.query_params.get("days", "30"))
    except ValueError:
        return Response({"detail": "days debe ser un número entero."}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"metric": metric, "days": min(max(days, 1), 90), "history": consumption_history(request.user, metric, home_id, days)})
