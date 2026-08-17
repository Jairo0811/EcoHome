from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("homes", "0002_home_owner")]

    operations = [
        migrations.CreateModel(
            name="HomeMembership",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(choices=[("ADMIN", "Administrador"), ("MEMBER", "Miembro"), ("VIEWER", "Consulta")], default="MEMBER", max_length=16)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("home", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="memberships", to="homes.home")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="ecohome_memberships", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["home_id", "user_id"]},
        ),
        migrations.AddConstraint(model_name="homemembership", constraint=models.UniqueConstraint(fields=("home", "user"), name="uq_home_membership")),
    ]
