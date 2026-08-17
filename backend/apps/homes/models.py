from django.conf import settings
from django.db import models


class Home(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="ecohome_homes")
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=255, blank=True)
    timezone = models.CharField(max_length=64, default="America/Santo_Domingo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def user_role(self, user):
        if not user or not user.is_authenticated:
            return None
        if user.is_staff or self.owner_id == user.id:
            return "OWNER"
        membership = self.memberships.filter(user=user).first()
        return membership.role if membership else None

    def user_can_manage(self, user) -> bool:
        return self.user_role(user) in {"OWNER", HomeMembership.Role.ADMIN}


class HomeMembership(models.Model):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        MEMBER = "MEMBER", "Miembro"
        VIEWER = "VIEWER", "Consulta"

    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ecohome_memberships")
    role = models.CharField(max_length=16, choices=Role.choices, default=Role.MEMBER)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["home_id", "user_id"]
        constraints = [models.UniqueConstraint(fields=["home", "user"], name="uq_home_membership")]

    def __str__(self) -> str:
        return f"{self.home} · {self.user} · {self.role}"


class Room(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name="rooms")
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["home_id", "name"]
        constraints = [models.UniqueConstraint(fields=["home", "name"], name="uq_room_home_name")]

    def __str__(self) -> str:
        return f"{self.home.name} · {self.name}"
