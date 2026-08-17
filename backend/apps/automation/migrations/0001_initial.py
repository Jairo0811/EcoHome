from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("devices", "0001_initial"), ("homes", "0003_homemembership"), ("resources", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Alert",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("alert_type", models.CharField(choices=[("RESOURCE_LIMIT", "Límite de consumo"), ("DEVICE_OFFLINE", "Dispositivo sin conexión"), ("AUTOMATION", "Automatización")], max_length=32)),
                ("severity", models.CharField(choices=[("INFO", "Información"), ("WARNING", "Advertencia"), ("CRITICAL", "Crítica")], default="INFO", max_length=16)),
                ("status", models.CharField(choices=[("OPEN", "Abierta"), ("ACKNOWLEDGED", "Reconocida"), ("RESOLVED", "Resuelta")], default="OPEN", max_length=16)),
                ("dedup_key", models.CharField(blank=True, db_index=True, max_length=180)),
                ("title", models.CharField(max_length=180)),
                ("message", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("resolved_at", models.DateTimeField(blank=True, null=True)),
                ("device", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="alerts", to="devices.device")),
                ("home", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="alerts", to="homes.home")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="AutomationRule",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=140)),
                ("enabled", models.BooleanField(default=True)),
                ("trigger_type", models.CharField(choices=[("RESOURCE_THRESHOLD", "Umbral de recurso"), ("DEVICE_STATUS", "Estado de dispositivo")], max_length=32)),
                ("trigger_config", models.JSONField(default=dict)),
                ("action_type", models.CharField(choices=[("DEVICE_COMMAND", "Comando de dispositivo"), ("CREATE_ALERT", "Crear alerta")], max_length=32)),
                ("action_config", models.JSONField(default=dict)),
                ("last_triggered_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("home", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="automation_rules", to="homes.home")),
            ],
            options={"ordering": ["home_id", "name"]},
        ),
        migrations.CreateModel(
            name="AutomationExecution",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(choices=[("SUCCESS", "Correcta"), ("FAILED", "Fallida")], max_length=16)),
                ("detail", models.TextField(blank=True)),
                ("payload", models.JSONField(blank=True, default=dict)),
                ("executed_at", models.DateTimeField(auto_now_add=True)),
                ("rule", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="executions", to="automation.automationrule")),
            ],
            options={"ordering": ["-executed_at"]},
        ),
        migrations.AddConstraint(model_name="automationrule", constraint=models.UniqueConstraint(fields=("home", "name"), name="uq_home_automation_name")),
        migrations.AddIndex(model_name="alert", index=models.Index(fields=["home", "status", "created_at"], name="idx_alert_home_status")),
    ]
