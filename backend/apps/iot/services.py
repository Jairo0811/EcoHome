import json
import os
import ssl
from dataclasses import dataclass

import paho.mqtt.client as mqtt
from django.utils import timezone

from apps.devices.models import Device, Telemetry


@dataclass(frozen=True)
class IngestResult:
    device_id: int
    telemetry_id: int | None
    status: str


def telemetry_topic(device: Device) -> str:
    return f"ecohome/{device.home_id}/devices/{device.external_id}"


def command_topic(device: Device) -> str:
    return f"ecohome/{device.home_id}/devices/{device.external_id}/commands"


def mqtt_configuration() -> dict:
    return {
        "host": os.getenv("MQTT_HOST", "localhost"),
        "port": int(os.getenv("MQTT_PORT", "1883")),
        "tls": os.getenv("MQTT_TLS", "false").lower() == "true",
        "username": os.getenv("MQTT_USERNAME", ""),
    }


def build_client(client_id: str = "ecohome-api") -> mqtt.Client:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
    username = os.getenv("MQTT_USERNAME")
    password = os.getenv("MQTT_PASSWORD")
    if username:
        client.username_pw_set(username, password)
    if os.getenv("MQTT_TLS", "false").lower() == "true":
        client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
    return client


def parse_payload(raw: str | bytes) -> dict:
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("El payload MQTT debe ser un objeto JSON.")
    return value


def ingest_message(external_id: str, payload: dict) -> IngestResult:
    device = Device.objects.select_related("home").get(external_id=external_id)
    status = payload.get("status", Device.Status.ONLINE)
    if status not in Device.Status.values:
        status = Device.Status.WARNING
    device.status = status
    device.last_seen_at = timezone.now()
    device.save(update_fields=["status", "last_seen_at", "updated_at"])

    telemetry = None
    metric = payload.get("metric")
    value = payload.get("value")
    if metric in Telemetry.Metric.values and value is not None:
        telemetry = Telemetry.objects.create(
            device=device,
            metric=metric,
            value=value,
            unit=payload.get("unit", ""),
            recorded_at=payload.get("recorded_at") or timezone.now(),
        )
    return IngestResult(device.id, telemetry.id if telemetry else None, device.status)


def publish_command(device: Device, payload: dict) -> None:
    config = mqtt_configuration()
    client = build_client(f"ecohome-command-{device.id}")
    client.connect(config["host"], config["port"], keepalive=20)
    info = client.publish(command_topic(device), json.dumps(payload), qos=1)
    info.wait_for_publish(timeout=5)
    client.disconnect()
