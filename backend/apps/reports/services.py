from datetime import timedelta
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone
from apps.automation.models import Alert, AutomationExecution
from apps.devices.models import Device, Telemetry
from apps.homes.views import accessible_homes
from apps.security.models import SecurityEvent

RESOURCE_METRICS=(Telemetry.Metric.ENERGY_KWH,Telemetry.Metric.WATER_L,Telemetry.Metric.GAS_M3)


def dashboard_report(user, days=30):
    days=min(max(int(days),1),90);start=timezone.now()-timedelta(days=days);homes=accessible_homes(user)
    devices=Device.objects.filter(home__in=homes);telemetry=Telemetry.objects.filter(device__home__in=homes,recorded_at__gte=start)
    trends={}
    for metric in RESOURCE_METRICS:
        rows=(telemetry.filter(metric=metric).annotate(day=TruncDate('recorded_at')).values('day').annotate(total=Sum('value')).order_by('day'))
        trends[metric]=[{"date":r['day'],"total":float(r['total'] or 0)} for r in rows]
    return {
      "periodDays":days,"homes":homes.count(),"devices":{"total":devices.count(),"online":devices.filter(status=Device.Status.ONLINE).count()},
      "alerts":{"open":Alert.objects.filter(home__in=homes,status=Alert.Status.OPEN).count(),"critical":Alert.objects.filter(home__in=homes,status=Alert.Status.OPEN,severity=Alert.Severity.CRITICAL).count()},
      "securityEvents":SecurityEvent.objects.filter(home__in=homes,occurred_at__gte=start).count(),
      "automationExecutions":AutomationExecution.objects.filter(rule__home__in=homes,executed_at__gte=start).count(),
      "trends":trends,
    }
