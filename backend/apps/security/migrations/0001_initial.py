from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("devices", "0001_initial"), ("homes", "0003_homemembership")]
    operations = [
        migrations.CreateModel(name="SecurityState", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("mode", models.CharField(choices=[("DISARMED", "Desarmado"), ("HOME", "En casa"), ("AWAY", "Fuera de casa")], default="DISARMED", max_length=16)),
            ("updated_at", models.DateTimeField(auto_now=True)),
            ("home", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="security_state", to="homes.home")),
        ]),
        migrations.CreateModel(name="SecurityEvent", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("event_type", models.CharField(choices=[("MOTION", "Movimiento"), ("DOOR_OPEN", "Puerta abierta"), ("CAMERA_ACTIVITY", "Actividad de cámara"), ("TAMPER", "Manipulación")], max_length=32)),
            ("severity", models.CharField(choices=[("INFO", "Información"), ("WARNING", "Advertencia"), ("CRITICAL", "Crítica")], default="INFO", max_length=16)),
            ("message", models.CharField(blank=True, max_length=255)),
            ("metadata", models.JSONField(blank=True, default=dict)),
            ("occurred_at", models.DateTimeField()),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("device", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="security_events", to="devices.device")),
            ("home", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="security_events", to="homes.home")),
        ], options={"ordering": ["-occurred_at"]}),
        migrations.AddIndex(model_name="securityevent", index=models.Index(fields=["home", "occurred_at"], name="idx_security_home_time")),
    ]
