from apps.automation.models import Alert
from apps.automation.services import upsert_alert
from .models import SecurityEvent, SecurityState


def process_security_event(event: SecurityEvent):
    state, _ = SecurityState.objects.get_or_create(home=event.home)
    if state.mode == SecurityState.Mode.DISARMED and event.severity != SecurityEvent.Severity.CRITICAL:
        return None
    severity = Alert.Severity.CRITICAL if event.severity == SecurityEvent.Severity.CRITICAL else Alert.Severity.WARNING
    return upsert_alert(
        home=event.home,
        device=event.device,
        alert_type=Alert.AlertType.AUTOMATION,
        severity=severity,
        title=f"Seguridad: {event.get_event_type_display()}",
        message=event.message or "Se detectó un evento de seguridad.",
        dedup_key=f"security:{event.home_id}:{event.event_type}:{event.device_id or 'none'}",
    )
