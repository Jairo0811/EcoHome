from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase
from apps.automation.models import Alert
from apps.devices.models import Device
from apps.homes.models import Home
from .models import SecurityState

User = get_user_model()


class SecurityTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("owner", password="StrongPass123!")
        self.home = Home.objects.create(owner=self.user, name="Casa")
        self.camera = Device.objects.create(home=self.home, external_id="cam-1", name="Entrada", device_type=Device.DeviceType.CAMERA)
        self.client.force_authenticate(self.user)

    def test_armed_security_event_creates_alert(self):
        SecurityState.objects.create(home=self.home, mode=SecurityState.Mode.AWAY)
        response = self.client.post("/api/v1/security/events/", {"home": self.home.id, "device": self.camera.id, "event_type": "CAMERA_ACTIVITY", "severity": "CRITICAL", "message": "Movimiento detectado", "occurred_at": timezone.now().isoformat()}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Alert.objects.count(), 1)

    def test_owner_can_change_security_mode(self):
        response = self.client.patch(f"/api/v1/security/states/{self.home.id}/", {"mode": "HOME"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["mode"], "HOME")
