from django.db import models

from apps.devices.models import Device
from apps.homes.models import Home


class Alert(models.Model):
    class AlertType(models.TextChoices):
        RESOURCE_LIMIT = "RESOURCE_LIMIT", "Límite de consumo"
        DEVICE_OFFLINE = "DEVICE_OFFLINE", "Dispositivo sin conexión"
        AUTOMATION = "AUTOMATION", "Automatización"

    class Severity(models.TextChoices):
        INFO = "INFO", "Información"
        WARNING = "WARNING", "Advertencia"
        CRITICAL = "CRITICAL", "Crítica"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Abierta"
        ACKNOWLEDGED = "ACKNOWLEDGED", "Reconocida"
        RESOLVED = "RESOLVED", "Resuelta"

    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name="alerts")
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True, related_name="alerts")
    alert_type = models.CharField(max_length=32, choices=AlertType.choices)
    severity = models.CharField(max_length=16, choices=Severity.choices, default=Severity.INFO)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.OPEN)
    dedup_key = models.CharField(max_length=180, blank=True, db_index=True)
    title = models.CharField(max_length=180)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["home", "status", "created_at"], name="idx_alert_home_status")]

    def __str__(self) -> str:
        return f"{self.home} · {self.title}"


class AutomationRule(models.Model):
    class TriggerType(models.TextChoices):
        RESOURCE_THRESHOLD = "RESOURCE_THRESHOLD", "Umbral de recurso"
        DEVICE_STATUS = "DEVICE_STATUS", "Estado de dispositivo"

    class ActionType(models.TextChoices):
        DEVICE_COMMAND = "DEVICE_COMMAND", "Comando de dispositivo"
        CREATE_ALERT = "CREATE_ALERT", "Crear alerta"

    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name="automation_rules")
    name = models.CharField(max_length=140)
    enabled = models.BooleanField(default=True)
    trigger_type = models.CharField(max_length=32, choices=TriggerType.choices)
    trigger_config = models.JSONField(default=dict)
    action_type = models.CharField(max_length=32, choices=ActionType.choices)
    action_config = models.JSONField(default=dict)
    last_triggered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["home_id", "name"]
        constraints = [models.UniqueConstraint(fields=["home", "name"], name="uq_home_automation_name")]

    def __str__(self) -> str:
        return f"{self.home} · {self.name}"


class AutomationExecution(models.Model):
    class Status(models.TextChoices):
        SUCCESS = "SUCCESS", "Correcta"
        FAILED = "FAILED", "Fallida"

    rule = models.ForeignKey(AutomationRule, on_delete=models.CASCADE, related_name="executions")
    status = models.CharField(max_length=16, choices=Status.choices)
    detail = models.TextField(blank=True)
    payload = models.JSONField(default=dict, blank=True)
    executed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-executed_at"]

    def __str__(self) -> str:
        return f"{self.rule} · {self.status}"
