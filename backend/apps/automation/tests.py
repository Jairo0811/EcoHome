from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase

from apps.devices.models import Device, Telemetry
from apps.homes.models import Home
from apps.resources.models import ResourceLimit
from .models import Alert, AutomationExecution, AutomationRule
from .services import evaluate_home, evaluate_resource_limits, execute_rule

User = get_user_model()


class AutomationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("owner", password="StrongPass123!")
        self.home = Home.objects.create(owner=self.user, name="Casa")
        self.device = Device.objects.create(home=self.home, external_id="plug-1", name="Enchufe", device_type=Device.DeviceType.SMART_PLUG, status=Device.Status.ONLINE)
        self.meter = Device.objects.create(home=self.home, external_id="energy-1", name="Medidor", device_type=Device.DeviceType.ENERGY_METER)
        self.client.force_authenticate(self.user)

    def test_resource_limit_creates_warning_alert(self):
        ResourceLimit.objects.create(home=self.home, metric=Telemetry.Metric.ENERGY_KWH, daily_limit=Decimal("10"), warning_percent=80)
        Telemetry.objects.create(device=self.meter, metric=Telemetry.Metric.ENERGY_KWH, value=Decimal("9"), unit="kWh", recorded_at=timezone.now())
        alerts = evaluate_resource_limits(self.home)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].severity, Alert.Severity.WARNING)

    def test_resource_rule_creates_alert_execution(self):
        Telemetry.objects.create(device=self.meter, metric=Telemetry.Metric.ENERGY_KWH, value=Decimal("6"), unit="kWh", recorded_at=timezone.now())
        rule = AutomationRule.objects.create(home=self.home, name="Aviso energía", trigger_type=AutomationRule.TriggerType.RESOURCE_THRESHOLD, trigger_config={"metric": "ENERGY_KWH", "threshold": 5}, action_type=AutomationRule.ActionType.CREATE_ALERT, action_config={"title": "Consumo alto", "severity": "WARNING"})
        execution = execute_rule(rule)
        self.assertEqual(execution.status, AutomationExecution.Status.SUCCESS)
        self.assertTrue(Alert.objects.filter(alert_type=Alert.AlertType.AUTOMATION).exists())

    @patch("apps.automation.services.publish_command")
    def test_manual_device_automation_publishes_command(self, publish):
        rule = AutomationRule.objects.create(home=self.home, name="Apagar", trigger_type=AutomationRule.TriggerType.DEVICE_STATUS, trigger_config={"deviceId": self.device.id, "status": "ONLINE"}, action_type=AutomationRule.ActionType.DEVICE_COMMAND, action_config={"deviceId": self.device.id, "command": {"action": "TURN_OFF"}})
        execution = execute_rule(rule, force=True)
        self.assertEqual(execution.status, AutomationExecution.Status.SUCCESS)
        publish.assert_called_once()
