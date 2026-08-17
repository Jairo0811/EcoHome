# Despliegue de EcoHome 1.0

## Inicio rápido con Docker

Requisitos: Docker Engine/Desktop con Docker Compose v2.

```bash
cp .env.example .env
docker compose up --build -d
docker compose ps
```

La aplicación web queda publicada por defecto en `http://localhost:8080` y MQTT en el puerto `1883`.

## Servicios

| Servicio | Función |
|---|---|
| `frontend` | Nginx + build estático React |
| `backend` | Django/DRF servido por Gunicorn |
| `db` | PostgreSQL 16 |
| `mqtt` | Eclipse Mosquitto 2 |
| `mqtt-listener` | Consumidor de telemetría MQTT |

## Variables críticas

Antes de producción configura valores únicos y secretos para:

- `DJANGO_SECRET_KEY`
- `POSTGRES_PASSWORD`
- credenciales MQTT cuando se habilite autenticación
- `DJANGO_ALLOWED_HOSTS`

Mantén `DJANGO_DEBUG=false`. Habilita `DJANGO_SECURE_SSL_REDIRECT=true` únicamente cuando el tráfico llegue por HTTPS y el proxy preserve `X-Forwarded-Proto`.

## TLS y broker MQTT

El `mosquitto.conf` incluido está preparado para desarrollo y permite conexiones anónimas. **No debe exponerse a Internet tal como está.** En producción configura usuarios/ACL, certificados TLS y restringe el puerto mediante firewall o red privada.

Para HTTP, termina TLS en un reverse proxy, balanceador o servicio administrado y reenvía tráfico a `frontend`. Nginx ya enruta `/api/` hacia el backend.

## Comprobaciones

```bash
curl http://localhost:8080/api/v1/health/
curl http://localhost:8080/api/v1/health/ready/
docker compose logs -f backend
docker compose logs -f mqtt-listener
```

## Actualización

```bash
git pull --ff-only
docker compose build --pull
docker compose up -d
docker compose ps
```

Las migraciones se ejecutan al iniciar el servicio `backend`.

## Checklist de producción

1. Secretos reales fuera del repositorio.
2. PostgreSQL y MQTT no expuestos públicamente sin necesidad.
3. TLS habilitado.
4. Broker MQTT con autenticación, ACL y TLS.
5. Backups automáticos de PostgreSQL.
6. Logs y métricas enviados a un sistema persistente.
7. Health/readiness integrados con el orquestador.
8. CI verde antes de desplegar.
