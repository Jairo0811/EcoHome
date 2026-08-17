from rest_framework import serializers

from apps.devices.models import Device, Telemetry
from .models import Alert, AutomationExecution, AutomationRule


class AlertSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source="device.name", read_only=True)

    class Meta:
        model = Alert
        fields = ["id", "home", "device", "device_name", "alert_type", "severity", "status", "title", "message", "created_at", "updated_at", "resolved_at"]
        read_only_fields = fields


class AutomationExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutomationExecution
        fields = ["id", "rule", "status", "detail", "payload", "executed_at"]
        read_only_fields = fields


class AutomationRuleSerializer(serializers.ModelSerializer):
    recent_executions = AutomationExecutionSerializer(source="executions", many=True, read_only=True)

    class Meta:
        model = AutomationRule
        fields = ["id", "home", "name", "enabled", "trigger_type", "trigger_config", "action_type", "action_config", "last_triggered_at", "created_at", "updated_at", "recent_executions"]
        read_only_fields = ["id", "last_triggered_at", "created_at", "updated_at", "recent_executions"]

    def validate(self, attrs):
        trigger_type = attrs.get("trigger_type", getattr(self.instance, "trigger_type", None))
        trigger = attrs.get("trigger_config", getattr(self.instance, "trigger_config", {}))
        action_type = attrs.get("action_type", getattr(self.instance, "action_type", None))
        action = attrs.get("action_config", getattr(self.instance, "action_config", {}))

        if trigger_type == AutomationRule.TriggerType.RESOURCE_THRESHOLD:
            if trigger.get("metric") not in {Telemetry.Metric.ENERGY_KWH, Telemetry.Metric.WATER_L, Telemetry.Metric.GAS_M3} or "threshold" not in trigger:
                raise serializers.ValidationError({"trigger_config": "Se requieren metric de recurso y threshold."})
        elif trigger_type == AutomationRule.TriggerType.DEVICE_STATUS:
            if "deviceId" not in trigger or trigger.get("status") not in Device.Status.values:
                raise serializers.ValidationError({"trigger_config": "Se requieren deviceId y status válidos."})

        if action_type == AutomationRule.ActionType.DEVICE_COMMAND:
            if "deviceId" not in action or not isinstance(action.get("command"), dict):
                raise serializers.ValidationError({"action_config": "Se requieren deviceId y command."})
        return attrs
