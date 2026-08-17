from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.devices.models import Telemetry
from apps.homes.models import Home


class ResourceLimit(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name="resource_limits")
    metric = models.CharField(max_length=32, choices=Telemetry.Metric.choices)
    daily_limit = models.DecimalField(max_digits=12, decimal_places=3)
    warning_percent = models.PositiveSmallIntegerField(
        default=80,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["home_id", "metric"]
        constraints = [
            models.UniqueConstraint(fields=["home", "metric"], name="uq_home_resource_limit")
        ]

    def __str__(self) -> str:
        return f"{self.home} · {self.metric}: {self.daily_limit}"
