from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from apps.devices.models import Device,Telemetry
from apps.homes.models import Home
User=get_user_model()
class SimulatorTests(APITestCase):
 def test_run_creates_deterministic_telemetry(self):
  u=User.objects.create_user('owner',password='StrongPass123!');h=Home.objects.create(owner=u,name='Casa');Device.objects.create(home=h,external_id='energy-sim',name='Medidor',device_type=Device.DeviceType.ENERGY_METER);self.client.force_authenticate(u);r=self.client.post('/api/v1/simulator/run/',{'home':h.id,'steps':3,'seed':7},format='json');self.assertEqual(r.status_code,201);self.assertEqual(r.data['telemetryCreated'],3);self.assertEqual(Telemetry.objects.count(),3)
