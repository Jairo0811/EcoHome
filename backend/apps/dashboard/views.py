from datetime import timedelta

from django.db.models import Sum
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.devices.models import Device, Telemetry
from apps.homes.views import accessible_homes


def metric_total(queryset, metric: str, since) -> float:
    value = queryset.filter(metric=metric, recorded_at__gte=since).aggregate(total=Sum("value")).get("total")
    return float(value or 0)


@api_view(["GET"])
def summary(request):
    since = timezone.now() - timedelta(hours=24)
    homes = accessible_homes(request.user)
    devices = Device.objects.select_related("room", "home").filter(home__in=homes)
    telemetry = Telemetry.objects.select_related("device", "device__home").filter(device__home__in=homes)
    recent_devices = devices.order_by("-last_seen_at")[:5]
    return Response({
        "homes": homes.count(),
        "devices": {"total": devices.count(), "online": devices.filter(status=Device.Status.ONLINE).count(), "warning": devices.filter(status=Device.Status.WARNING).count()},
        "consumption24h": {
            "energyKwh": metric_total(telemetry, Telemetry.Metric.ENERGY_KWH, since),
            "waterLiters": metric_total(telemetry, Telemetry.Metric.WATER_L, since),
            "gasM3": metric_total(telemetry, Telemetry.Metric.GAS_M3, since),
        },
        "recentDevices": [{"id": d.id, "name": d.name, "type": d.device_type, "status": d.status, "room": d.room.name if d.room else None, "lastSeenAt": d.last_seen_at} for d in recent_devices],
    })
