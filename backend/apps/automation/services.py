from datetime import timedelta
from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone

from apps.devices.models import Device, Telemetry
from apps.iot.services import publish_command
from apps.resources.models import ResourceLimit
from .models import Alert, AutomationExecution, AutomationRule


def upsert_alert(*, home, alert_type, severity, title, message, dedup_key, device=None) -> Alert:
    alert = Alert.objects.filter(
        home=home,
        dedup_key=dedup_key,
        status__in=[Alert.Status.OPEN, Alert.Status.ACKNOWLEDGED],
    ).first()
    if alert:
        alert.alert_type = alert_type
        alert.severity = severity
        alert.title = title
        alert.message = message
        alert.device = device
        alert.status = Alert.Status.OPEN
        alert.resolved_at = None
        alert.save(update_fields=["alert_type", "severity", "title", "message", "device", "status", "resolved_at", "updated_at"])
        return alert
    return Alert.objects.create(home=home, device=device, alert_type=alert_type, severity=severity, title=title, message=message, dedup_key=dedup_key)


def _metric_total(home, metric) -> Decimal:
    since = timezone.now() - timedelta(hours=24)
    total = Telemetry.objects.filter(device__home=home, metric=metric, recorded_at__gte=since).aggregate(total=Sum("value"))["total"]
    return total or Decimal("0")


def evaluate_resource_limits(home) -> list[Alert]:
    alerts = []
    for limit in ResourceLimit.objects.filter(home=home, active=True, metric__in=[Telemetry.Metric.ENERGY_KWH, Telemetry.Metric.WATER_L, Telemetry.Metric.GAS_M3]):
        total = _metric_total(home, limit.metric)
        if limit.daily_limit <= 0:
            continue
        percent = (total / limit.daily_limit) * 100
        if percent < limit.warning_percent:
            continue
        severity = Alert.Severity.CRITICAL if percent >= 100 else Alert.Severity.WARNING
        label = dict(Telemetry.Metric.choices).get(limit.metric, limit.metric)
        alert = upsert_alert(
            home=home,
            alert_type=Alert.AlertType.RESOURCE_LIMIT,
            severity=severity,
            title=f"Consumo de {label} al {percent:.0f}%",
            message=f"El consumo acumulado es {total} frente a un límite diario de {limit.daily_limit}.",
            dedup_key=f"resource-limit:{limit.id}",
        )
        alerts.append(alert)
    return alerts


def _trigger_matches(rule: AutomationRule) -> bool:
    config = rule.trigger_config
    if rule.trigger_type == AutomationRule.TriggerType.RESOURCE_THRESHOLD:
        metric = config.get("metric")
        threshold = Decimal(str(config.get("threshold", "0")))
        value = _metric_total(rule.home, metric)
        operator = config.get("operator", "gte")
        return value >= threshold if operator == "gte" else value <= threshold
    if rule.trigger_type == AutomationRule.TriggerType.DEVICE_STATUS:
        device = Device.objects.filter(id=config.get("deviceId"), home=rule.home).first()
        return bool(device and device.status == config.get("status"))
    return False


def _execute_action(rule: AutomationRule) -> dict:
    config = rule.action_config
    if rule.action_type == AutomationRule.ActionType.DEVICE_COMMAND:
        device = Device.objects.get(id=config["deviceId"], home=rule.home)
        command = config["command"]
        publish_command(device, command)
        return {"deviceId": device.id, "command": command}

    severity = config.get("severity", Alert.Severity.INFO)
    if severity not in Alert.Severity.values:
        severity = Alert.Severity.INFO
    alert = upsert_alert(
        home=rule.home,
        alert_type=Alert.AlertType.AUTOMATION,
        severity=severity,
        title=config.get("title", rule.name),
        message=config.get("message", "Regla de automatización activada."),
        dedup_key=f"automation:{rule.id}",
    )
    return {"alertId": alert.id}


def execute_rule(rule: AutomationRule, *, force=False):
    if not rule.enabled:
        return None
    cooldown = int(rule.trigger_config.get("cooldownMinutes", 5))
    if not force and rule.last_triggered_at and rule.last_triggered_at >= timezone.now() - timedelta(minutes=max(cooldown, 0)):
        return None
    if not force and not _trigger_matches(rule):
        return None

    try:
        payload = _execute_action(rule)
        execution = AutomationExecution.objects.create(rule=rule, status=AutomationExecution.Status.SUCCESS, payload=payload)
        rule.last_triggered_at = timezone.now()
        rule.save(update_fields=["last_triggered_at", "updated_at"])
        return execution
    except Exception as exc:
        return AutomationExecution.objects.create(rule=rule, status=AutomationExecution.Status.FAILED, detail=str(exc))


def evaluate_home(home) -> dict:
    alerts = evaluate_resource_limits(home)
    executions = []
    for rule in AutomationRule.objects.filter(home=home, enabled=True):
        execution = execute_rule(rule)
        if execution:
            executions.append(execution)
    return {"alerts": len(alerts), "executions": len(executions)}
