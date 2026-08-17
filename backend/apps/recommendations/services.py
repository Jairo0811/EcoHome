from datetime import timedelta
from django.db.models import Sum
from django.utils import timezone
from apps.devices.models import Device,Telemetry
from apps.resources.models import ResourceLimit
from apps.security.models import SecurityState
from .models import Recommendation


def _sum(home,metric):
 since=timezone.now()-timedelta(hours=24);return Telemetry.objects.filter(device__home=home,metric=metric,recorded_at__gte=since).aggregate(total=Sum('value'))['total'] or 0

def _upsert(home,key,**data):
 obj,created=Recommendation.objects.get_or_create(home=home,key=key,defaults=data)
 if not created and obj.status==Recommendation.Status.ACTIVE:
  for k,v in data.items(): setattr(obj,k,v)
  obj.save()
 return obj

def generate_for_home(home):
 result=[]
 specs=[(Telemetry.Metric.ENERGY_KWH,Recommendation.Category.ENERGY,'energy','Reduce consumos eléctricos en horas de baja actividad','Revisa enchufes y cargas que permanecen activos sin necesidad.',12),(Telemetry.Metric.WATER_L,Recommendation.Category.WATER,'water','Optimiza el consumo de agua','El consumo está cerca de tu límite; revisa fugas y rutinas de uso.',10),(Telemetry.Metric.GAS_M3,Recommendation.Category.GAS,'gas','Ajusta el uso de gas','El consumo de gas puede optimizarse revisando horarios y equipos.',8)]
 for metric,category,key,title,description,savings in specs:
  total=float(_sum(home,metric));limit=ResourceLimit.objects.filter(home=home,metric=metric,active=True).first()
  if limit and float(limit.daily_limit)>0 and total/float(limit.daily_limit)>=.75:
   result.append(_upsert(home,f'limit-{key}',category=category,priority=Recommendation.Priority.HIGH if total>=float(limit.daily_limit) else Recommendation.Priority.MEDIUM,title=title,description=description,estimated_savings_percent=savings))
 offline=Device.objects.filter(home=home,status=Device.Status.OFFLINE).count()
 if offline:
  result.append(_upsert(home,'offline-devices',category=Recommendation.Category.DEVICES,priority=Recommendation.Priority.MEDIUM,title='Revisa dispositivos desconectados',description=f'Hay {offline} dispositivo(s) sin conexión. Verificar conectividad mejora automatizaciones y monitoreo.',estimated_savings_percent=0))
 state=SecurityState.objects.filter(home=home).first()
 if not state or state.mode==SecurityState.Mode.DISARMED:
  result.append(_upsert(home,'security-mode',category=Recommendation.Category.SECURITY,priority=Recommendation.Priority.LOW,title='Configura un modo de seguridad',description='Activa En casa o Fuera para aprovechar cámaras, sensores y alertas.',estimated_savings_percent=0))
 return result
