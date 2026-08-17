from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [("homes", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Device",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("external_id", models.CharField(max_length=120, unique=True)),
                ("name", models.CharField(max_length=120)),
                ("device_type", models.CharField(choices=[("LIGHT", "Iluminación"), ("THERMOSTAT", "Termostato"), ("CAMERA", "Cámara"), ("SMART_PLUG", "Enchufe inteligente"), ("ENERGY_METER", "Medidor eléctrico"), ("WATER_METER", "Medidor de agua"), ("GAS_METER", "Medidor de gas"), ("MOTION_SENSOR", "Sensor de movimiento"), ("DOOR_SENSOR", "Sensor de puerta"), ("OTHER", "Otro")], max_length=32)),
                ("status", models.CharField(choices=[("ONLINE", "En línea"), ("OFFLINE", "Fuera de línea"), ("WARNING", "Advertencia")], default="OFFLINE", max_length=16)),
                ("last_seen_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("home", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="devices", to="homes.home")),
                ("room", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="devices", to="homes.room")),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Telemetry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("metric", models.CharField(choices=[("ENERGY_KWH", "Energía (kWh)"), ("WATER_L", "Agua (L)"), ("GAS_M3", "Gas (m³)"), ("TEMPERATURE_C", "Temperatura (°C)"), ("HUMIDITY_PCT", "Humedad (%)")], max_length=32)),
                ("value", models.DecimalField(decimal_places=3, max_digits=12)),
                ("unit", models.CharField(max_length=16)),
                ("recorded_at", models.DateTimeField()),
                ("device", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="telemetry", to="devices.device")),
            ],
            options={"ordering": ["-recorded_at"]},
        ),
        migrations.AddIndex(
            model_name="telemetry",
            index=models.Index(fields=["device", "metric", "recorded_at"], name="idx_telemetry_device_metric_time"),
        ),
    ]
