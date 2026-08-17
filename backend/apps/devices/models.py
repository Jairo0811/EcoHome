from django.db import models

from apps.homes.models import Home, Room


class Device(models.Model):
    class DeviceType(models.TextChoices):
        LIGHT = "LIGHT", "Iluminación"
        THERMOSTAT = "THERMOSTAT", "Termostato"
        CAMERA = "CAMERA", "Cámara"
        SMART_PLUG = "SMART_PLUG", "Enchufe inteligente"
        ENERGY_METER = "ENERGY_METER", "Medidor eléctrico"
        WATER_METER = "WATER_METER", "Medidor de agua"
        GAS_METER = "GAS_METER", "Medidor de gas"
        MOTION_SENSOR = "MOTION_SENSOR", "Sensor de movimiento"
        DOOR_SENSOR = "DOOR_SENSOR", "Sensor de puerta"
        OTHER = "OTHER", "Otro"

    class Status(models.TextChoices):
        ONLINE = "ONLINE", "En línea"
        OFFLINE = "OFFLINE", "Fuera de línea"
        WARNING = "WARNING", "Advertencia"

    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name="devices")
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name="devices")
    external_id = models.CharField(max_length=120, unique=True)
    name = models.CharField(max_length=120)
    device_type = models.CharField(max_length=32, choices=DeviceType.choices)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.OFFLINE)
    last_seen_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Telemetry(models.Model):
    class Metric(models.TextChoices):
        ENERGY_KWH = "ENERGY_KWH", "Energía (kWh)"
        WATER_L = "WATER_L", "Agua (L)"
        GAS_M3 = "GAS_M3", "Gas (m³)"
        TEMPERATURE_C = "TEMPERATURE_C", "Temperatura (°C)"
        HUMIDITY_PCT = "HUMIDITY_PCT", "Humedad (%)"

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="telemetry")
    metric = models.CharField(max_length=32, choices=Metric.choices)
    value = models.DecimalField(max_digits=12, decimal_places=3)
    unit = models.CharField(max_length=16)
    recorded_at = models.DateTimeField()

    class Meta:
        ordering = ["-recorded_at"]
        indexes = [
            models.Index(fields=["device", "metric", "recorded_at"], name="idx_telemetry_device_metric_time")
        ]

    def __str__(self) -> str:
        return f"{self.device.name}: {self.metric}={self.value} {self.unit}"
