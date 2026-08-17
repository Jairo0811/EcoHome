from datetime import timedelta
from decimal import Decimal

from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.utils import timezone

from apps.devices.models import Telemetry
from apps.homes.views import accessible_homes
from .models import ResourceLimit

RESOURCE_METRICS = (
    Telemetry.Metric.ENERGY_KWH,
    Telemetry.Metric.WATER_L,
    Telemetry.Metric.GAS_M3,
)
RANGE_DAYS = {"day": 1, "week": 7, "month": 30}


def scoped_homes(user, home_id=None):
    homes = accessible_homes(user)
    if home_id is not None:
        homes = homes.filter(id=home_id)
    return homes


def _total(queryset, metric, start, end=None) -> Decimal:
    filters = {"metric": metric, "recorded_at__gte": start}
    if end is not None:
        filters["recorded_at__lt"] = end
    value = queryset.filter(**filters).aggregate(total=Sum("value"))["total"]
    return value or Decimal("0")


def consumption_summary(user, home_id=None, range_name="day") -> dict:
    days = RANGE_DAYS.get(range_name, 1)
    now = timezone.now()
    start = now - timedelta(days=days)
    previous_start = start - timedelta(days=days)
    homes = scoped_homes(user, home_id)
    telemetry = Telemetry.objects.filter(device__home__in=homes)
    limits = ResourceLimit.objects.filter(home__in=homes, active=True, metric__in=RESOURCE_METRICS)

    response = {}
    for metric in RESOURCE_METRICS:
        current = _total(telemetry, metric, start)
        previous = _total(telemetry, metric, previous_start, start)
        daily_limit = limits.filter(metric=metric).aggregate(total=Sum("daily_limit"))["total"] or Decimal("0")
        period_limit = daily_limit * days
        change = None
        if previous > 0:
            change = float(((current - previous) / previous) * 100)
        progress = float((current / period_limit) * 100) if period_limit > 0 else None
        response[metric] = {
            "total": float(current),
            "previousTotal": float(previous),
            "changePercent": change,
            "limit": float(period_limit) if period_limit > 0 else None,
            "progressPercent": progress,
        }

    return {"range": range_name, "days": days, "resources": response}


def consumption_history(user, metric, home_id=None, days=30) -> list[dict]:
    days = min(max(int(days), 1), 90)
    start = timezone.now() - timedelta(days=days)
    homes = scoped_homes(user, home_id)
    rows = (
        Telemetry.objects.filter(device__home__in=homes, metric=metric, recorded_at__gte=start)
        .annotate(day=TruncDate("recorded_at"))
        .values("day")
        .annotate(total=Sum("value"))
        .order_by("day")
    )
    return [{"date": row["day"], "total": float(row["total"] or 0)} for row in rows]
