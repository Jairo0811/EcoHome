from unittest.mock import patch

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apps.devices.models import Device, Telemetry
from apps.homes.models import Home

User = get_user_model()


class IotTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("owner", password="StrongPass123!")
        self.home = Home.objects.create(owner=self.user, name="Casa")
        self.device = Device.objects.create(home=self.home, external_id="meter-1", name="Medidor", device_type=Device.DeviceType.ENERGY_METER)
        self.client.force_authenticate(self.user)

    def test_ingest_updates_device_and_creates_telemetry(self):
        response = self.client.post("/api/v1/iot/ingest/meter-1/", {"metric": "ENERGY_KWH", "value": "1.25", "unit": "kWh"}, format="json")
        self.assertEqual(response.status_code, 202)
        self.device.refresh_from_db()
        self.assertEqual(self.device.status, Device.Status.ONLINE)
        self.assertEqual(Telemetry.objects.count(), 1)

    @patch("apps.iot.views.publish_command")
    def test_command_is_published_for_owner(self, publish):
        response = self.client.post(f"/api/v1/iot/devices/{self.device.id}/command/", {"action": "TURN_ON"}, format="json")
        self.assertEqual(response.status_code, 202)
        publish.assert_called_once()
