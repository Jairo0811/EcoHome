from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Home",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("address", models.CharField(blank=True, max_length=255)),
                ("timezone", models.CharField(default="America/Santo_Domingo", max_length=64)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Room",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("home", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="rooms", to="homes.home")),
            ],
            options={"ordering": ["home_id", "name"]},
        ),
        migrations.AddConstraint(
            model_name="room",
            constraint=models.UniqueConstraint(fields=("home", "name"), name="uq_room_home_name"),
        ),
    ]
