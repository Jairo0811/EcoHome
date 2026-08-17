from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):
    dependencies = [("homes", "0003_homemembership")]

    operations = [
        migrations.CreateModel(
            name="ResourceLimit",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("metric", models.CharField(choices=[("ENERGY_KWH", "Energía (kWh)"), ("WATER_L", "Agua (L)"), ("GAS_M3", "Gas (m³)"), ("TEMPERATURE_C", "Temperatura (°C)"), ("HUMIDITY_PCT", "Humedad (%)")], max_length=32)),
                ("daily_limit", models.DecimalField(decimal_places=3, max_digits=12)),
                ("warning_percent", models.PositiveSmallIntegerField(default=80, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ("active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("home", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="resource_limits", to="homes.home")),
            ],
            options={"ordering": ["home_id", "metric"]},
        ),
        migrations.AddConstraint(model_name="resourcelimit", constraint=models.UniqueConstraint(fields=("home", "metric"), name="uq_home_resource_limit")),
    ]
