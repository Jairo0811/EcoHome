from decimal import Decimal
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase
from apps.devices.models import Device,Telemetry
from apps.homes.models import Home
from apps.resources.models import ResourceLimit
from .models import Recommendation
from .services import generate_for_home
User=get_user_model()
class RecommendationTests(APITestCase):
 def test_high_consumption_generates_recommendation(self):
  u=User.objects.create_user('owner',password='StrongPass123!');h=Home.objects.create(owner=u,name='Casa');d=Device.objects.create(home=h,external_id='m',name='Medidor',device_type=Device.DeviceType.ENERGY_METER);ResourceLimit.objects.create(home=h,metric=Telemetry.Metric.ENERGY_KWH,daily_limit=Decimal('10'));Telemetry.objects.create(device=d,metric=Telemetry.Metric.ENERGY_KWH,value=Decimal('8'),unit='kWh',recorded_at=timezone.now());generate_for_home(h);self.assertTrue(Recommendation.objects.filter(home=h,key='limit-energy').exists())
