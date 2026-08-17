from datetime import timedelta

from django.db.models import Sum
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.devices.models import Device, Telemetry
from apps.homes.models import Home


def metric_total(metric: str, since) -> float:
    value = (
        Telemetry.objects.filter(metric=metric, recorded_at__gte=since)
        .aggregate(total=Sum("value"))
        .get("total")
    )
    return float(value or 0)


@api_view(["GET"])
def summary(request):
    since = timezone.now() - timedelta(hours=24)
    recent_devices = Device.objects.select_related("room").order_by("-last_seen_at")[:5]

    return Response(
        {
            "homes": Home.objects.count(),
            "devices": {
                "total": Device.objects.count(),
                "online": Device.objects.filter(status=Device.Status.ONLINE).count(),
                "warning": Device.objects.filter(status=Device.Status.WARNING).count(),
            },
            "consumption24h": {
                "energyKwh": metric_total(Telemetry.Metric.ENERGY_KWH, since),
                "waterLiters": metric_total(Telemetry.Metric.WATER_L, since),
                "gasM3": metric_total(Telemetry.Metric.GAS_M3, since),
            },
            "recentDevices": [
                {
                    "id": device.id,
                    "name": device.name,
                    "type": device.device_type,
                    "status": device.status,
                    "room": device.room.name if device.room else None,
                    "lastSeenAt": device.last_seen_at,
                }
                for device in recent_devices
            ],
        }
    )
