# API de EcoHome 1.0

Base URL: `/api/v1`

Salvo health/readiness y autenticación inicial, los endpoints requieren `Authorization: Bearer <access-token>`.

## Identidad

- `POST /auth/register/` — crear usuario.
- `POST /auth/token/` — obtener access/refresh JWT.
- `POST /auth/token/refresh/` — renovar access token.
- `GET/PATCH /auth/me/` — perfil actual.

## Hogares y dispositivos

- `/homes/` — CRUD de hogares accesibles.
- `/rooms/` — CRUD de habitaciones.
- `/devices/` — CRUD de dispositivos.
- `/telemetry/` — lectura/ingesta autorizada de telemetría.
- `/homes/{id}/members/` — miembros y roles del hogar.

## IoT

- `GET /iot/config/` — configuración pública no sensible del broker.
- `GET /iot/topics/` — tópicos disponibles para dispositivos accesibles.
- `POST /iot/ingest/{external_id}/` — ingesta HTTP compatible con la tubería MQTT.
- `POST /iot/devices/{id}/command/` — publicar comando al dispositivo.

Tópicos principales:

```text
ecohome/{home_id}/devices/{external_id}
ecohome/{home_id}/devices/{external_id}/commands
```

## Recursos

- `GET /resources/summary/?range=day|week|month`
- `GET /resources/history/?metric=ENERGY_KWH&days=30`
- `/resources/limits/` — límites por hogar/recurso.

## Automatización y seguridad

- `/automation/alerts/`
- `/automation/rules/`
- `POST /automation/rules/{id}/execute/`
- `/security/events/`
- `/security/states/`
- `PATCH /security/states/{home_id}/`

## Analítica y recomendaciones

- `GET /reports/overview/?days=30`
- `GET /reports/consumption.csv`
- `/recommendations/`
- `POST /recommendations/refresh/`
- `POST /recommendations/{id}/apply/`
- `POST /recommendations/{id}/dismiss/`

## Simulador

- `POST /simulator/run/`

Ejemplo:

```json
{
  "steps": 10,
  "seed": 42
}
```

Si no se proporciona `home`, el backend selecciona el primer hogar accesible que el usuario pueda administrar.

## Operación

- `GET /health/` — liveness/version.
- `GET /health/ready/` — readiness con comprobación de base de datos.
