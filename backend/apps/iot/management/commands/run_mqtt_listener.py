import logging

from django.core.management.base import BaseCommand

from apps.iot.services import build_client, ingest_message, mqtt_configuration, parse_payload

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Escucha telemetría MQTT de dispositivos EcoHome."

    def handle(self, *args, **options):
        config = mqtt_configuration()
        client = build_client("ecohome-listener")

        def on_connect(mqtt_client, userdata, flags, reason_code, properties):
            if reason_code == 0:
                self.stdout.write(self.style.SUCCESS("Conectado al broker MQTT"))
                mqtt_client.subscribe("ecohome/+/devices/+", qos=1)
            else:
                logger.error("Conexión MQTT rechazada: %s", reason_code)

        def on_message(mqtt_client, userdata, message):
            try:
                external_id = message.topic.split("/")[-1]
                ingest_message(external_id, parse_payload(message.payload))
            except Exception:
                logger.exception("No se pudo procesar el mensaje MQTT %s", message.topic)

        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(config["host"], config["port"], keepalive=60)
        client.loop_forever()
