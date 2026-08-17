# Arquitectura de EcoHome 1.0

## Visión general

EcoHome utiliza una arquitectura web modular cliente-servidor. React/TypeScript entrega la experiencia de usuario; Django REST Framework expone la API y concentra reglas de negocio; PostgreSQL persiste el estado; Mosquitto transporta mensajes MQTT entre EcoHome y dispositivos IoT.

```text
┌───────────────────────────────┐
│ React 19 + TypeScript + Vite │
└──────────────┬────────────────┘
               │ HTTPS / JSON
               ▼
┌───────────────────────────────┐
│ Django 5 + DRF + SimpleJWT   │
├───────────────────────────────┤
│ accounts        homes         │
│ devices         iot           │
│ resources       automation    │
│ security        reports       │
│ recommendations simulator     │
│ dashboard       core          │
└───────┬────────────────┬──────┘
        │                │ MQTT
        ▼                ▼
┌──────────────┐   ┌──────────────┐
│ PostgreSQL   │   │ Mosquitto    │
└──────────────┘   └──────┬───────┘
                          ▼
                    Dispositivos IoT
```

## Módulos

- `accounts`: registro, login JWT, refresh y perfil autenticado.
- `homes`: hogares, habitaciones, membresías y roles de acceso.
- `devices`: dispositivos y telemetría normalizada.
- `iot`: tópicos MQTT, listener, ingesta y comandos.
- `resources`: límites y analítica de electricidad, agua y gas.
- `automation`: alertas, reglas, acciones y ejecuciones.
- `security`: modos de seguridad y eventos de cámaras/sensores.
- `reports`: KPIs, históricos y exportaciones.
- `recommendations`: reglas de optimización y sugerencias accionables.
- `simulator`: generación determinística de telemetría sintética.
- `dashboard`: agregación de información operativa para la UI.
- `core`: health checks, readiness y utilidades transversales.

## Flujo de telemetría

1. Un dispositivo publica telemetría al broker MQTT.
2. `run_mqtt_listener` consume el tópico correspondiente.
3. `iot.ingest_message` valida el dispositivo, actualiza estado y persiste la lectura.
4. La nueva lectura alimenta recursos, alertas y automatizaciones.
5. Dashboard, reportes y recomendaciones consultan los datos consolidados.

El simulador utiliza exactamente el mismo servicio de ingesta para evitar una ruta de negocio paralela.

## Autorización

Cada hogar tiene un propietario y puede tener miembros `ADMIN`, `MEMBER` o `VIEWER`. Los querysets se filtran mediante `accessible_homes`, evitando que un usuario consulte hogares ajenos. Las operaciones destructivas o de control requieren propietario/administrador según el caso.

## Escalabilidad

La separación por aplicaciones Django permite evolucionar módulos de forma independiente. PostgreSQL, el listener MQTT y el frontend se ejecutan como servicios separados en Docker Compose, permitiendo escalar procesos de aplicación o mensajería sin acoplarlos a la interfaz.
