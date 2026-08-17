from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase
from apps.devices.models import Device,Telemetry
from apps.homes.models import Home
User=get_user_model()

class ReportsTests(APITestCase):
 def setUp(self):
  self.user=User.objects.create_user('owner',password='StrongPass123!');self.home=Home.objects.create(owner=self.user,name='Casa');self.device=Device.objects.create(home=self.home,external_id='m1',name='Medidor',device_type=Device.DeviceType.ENERGY_METER);Telemetry.objects.create(device=self.device,metric=Telemetry.Metric.ENERGY_KWH,value='2.5',unit='kWh',recorded_at=timezone.now());self.client.force_authenticate(self.user)
 def test_overview_contains_trend(self):
  r=self.client.get('/api/v1/reports/overview/?days=30');self.assertEqual(r.status_code,200);self.assertEqual(r.data['homes'],1);self.assertEqual(len(r.data['trends']['ENERGY_KWH']),1)
 def test_csv_export(self):
  r=self.client.get('/api/v1/reports/consumption.csv');self.assertEqual(r.status_code,200);self.assertIn('text/csv',r['Content-Type'])
