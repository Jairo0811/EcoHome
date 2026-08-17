import random
from decimal import Decimal
from django.utils import timezone
from apps.devices.models import Device,Telemetry
from apps.iot.services import ingest_message

METRIC_BY_TYPE={Device.DeviceType.ENERGY_METER:(Telemetry.Metric.ENERGY_KWH,'kWh',(0.08,0.65)),Device.DeviceType.WATER_METER:(Telemetry.Metric.WATER_L,'L',(1.0,18.0)),Device.DeviceType.GAS_METER:(Telemetry.Metric.GAS_M3,'m³',(0.01,0.15)),Device.DeviceType.THERMOSTAT:(Telemetry.Metric.TEMPERATURE_C,'°C',(20.0,28.0))}

def simulate_step(home,seed=None):
 rng=random.Random(seed);created=[]
 for device in Device.objects.filter(home=home):
  spec=METRIC_BY_TYPE.get(device.device_type)
  if not spec: continue
  metric,unit,bounds=spec;value=Decimal(str(round(rng.uniform(*bounds),3)))
  result=ingest_message(device.external_id,{"status":Device.Status.ONLINE,"metric":metric,"value":str(value),"unit":unit,"recorded_at":timezone.now()});created.append(result.telemetry_id)
 return [x for x in created if x]

def simulate(home,steps=1,seed=None):
 ids=[]
 for index in range(max(1,min(int(steps),100))): ids.extend(simulate_step(home,None if seed is None else seed+index))
 return ids
