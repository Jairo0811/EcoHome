from django.conf import settings
from django.db import models


class Home(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ecohome_homes",
    )
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=255, blank=True)
    timezone = models.CharField(max_length=64, default="America/Santo_Domingo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Room(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name="rooms")
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["home_id", "name"]
        constraints = [
            models.UniqueConstraint(fields=["home", "name"], name="uq_room_home_name")
        ]

    def __str__(self) -> str:
        return f"{self.home.name} · {self.name}"
