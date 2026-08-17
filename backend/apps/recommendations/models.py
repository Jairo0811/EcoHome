from django.db import models
from apps.homes.models import Home


class Recommendation(models.Model):
    class Category(models.TextChoices):
        ENERGY = "ENERGY", "Energía"
        WATER = "WATER", "Agua"
        GAS = "GAS", "Gas"
        DEVICES = "DEVICES", "Dispositivos"
        SECURITY = "SECURITY", "Seguridad"

    class Priority(models.TextChoices):
        LOW = "LOW", "Baja"
        MEDIUM = "MEDIUM", "Media"
        HIGH = "HIGH", "Alta"

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Activa"
        DISMISSED = "DISMISSED", "Descartada"
        APPLIED = "APPLIED", "Aplicada"

    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name="recommendations")
    key = models.CharField(max_length=160)
    category = models.CharField(max_length=20, choices=Category.choices)
    priority = models.CharField(max_length=16, choices=Priority.choices, default=Priority.MEDIUM)
    title = models.CharField(max_length=180)
    description = models.TextField()
    estimated_savings_percent = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    generated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-generated_at"]
        constraints = [models.UniqueConstraint(fields=["home", "key"], name="uq_home_recommendation_key")]
