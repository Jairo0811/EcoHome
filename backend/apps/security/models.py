from django.db import models
from apps.devices.models import Device
from apps.homes.models import Home


class SecurityState(models.Model):
    class Mode(models.TextChoices):
        DISARMED = "DISARMED", "Desarmado"
        HOME = "HOME", "En casa"
        AWAY = "AWAY", "Fuera de casa"

    home = models.OneToOneField(Home, on_delete=models.CASCADE, related_name="security_state")
    mode = models.CharField(max_length=16, choices=Mode.choices, default=Mode.DISARMED)
    updated_at = models.DateTimeField(auto_now=True)


class SecurityEvent(models.Model):
    class EventType(models.TextChoices):
        MOTION = "MOTION", "Movimiento"
        DOOR_OPEN = "DOOR_OPEN", "Puerta abierta"
        CAMERA_ACTIVITY = "CAMERA_ACTIVITY", "Actividad de cámara"
        TAMPER = "TAMPER", "Manipulación"

    class Severity(models.TextChoices):
        INFO = "INFO", "Información"
        WARNING = "WARNING", "Advertencia"
        CRITICAL = "CRITICAL", "Crítica"

    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name="security_events")
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True, related_name="security_events")
    event_type = models.CharField(max_length=32, choices=EventType.choices)
    severity = models.CharField(max_length=16, choices=Severity.choices, default=Severity.INFO)
    message = models.CharField(max_length=255, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    occurred_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-occurred_at"]
        indexes = [models.Index(fields=["home", "occurred_at"], name="idx_security_home_time")]
