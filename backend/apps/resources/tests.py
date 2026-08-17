from decimal import Decimal

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase

from apps.devices.models import Device, Telemetry
from apps.homes.models import Home, HomeMembership
from .models import ResourceLimit

User = get_user_model()


class ResourceTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user("owner", password="StrongPass123!")
        self.viewer = User.objects.create_user("viewer", password="StrongPass123!")
        self.home = Home.objects.create(owner=self.owner, name="Casa")
        HomeMembership.objects.create(home=self.home, user=self.viewer, role=HomeMembership.Role.VIEWER)
        self.device = Device.objects.create(home=self.home, external_id="energy-1", name="Medidor", device_type=Device.DeviceType.ENERGY_METER)
        Telemetry.objects.create(device=self.device, metric=Telemetry.Metric.ENERGY_KWH, value=Decimal("4.500"), unit="kWh", recorded_at=timezone.now())
        ResourceLimit.objects.create(home=self.home, metric=Telemetry.Metric.ENERGY_KWH, daily_limit=Decimal("10.000"))

    def test_summary_calculates_consumption_and_limit(self):
        self.client.force_authenticate(self.owner)
        response = self.client.get(f"/api/v1/resources/summary/?home={self.home.id}&range=day")
        self.assertEqual(response.status_code, 200)
        energy = response.data["resources"][Telemetry.Metric.ENERGY_KWH]
        self.assertEqual(energy["total"], 4.5)
        self.assertEqual(energy["limit"], 10.0)
        self.assertEqual(energy["progressPercent"], 45.0)

    def test_viewer_cannot_modify_limit(self):
        self.client.force_authenticate(self.viewer)
        response = self.client.patch(f"/api/v1/resources/limits/{ResourceLimit.objects.get().id}/", {"daily_limit": "20"}, format="json")
        self.assertEqual(response.status_code, 403)
