# Changelog

Todos los cambios relevantes de EcoHome se documentan en este archivo.

## [1.0.0] - 2026-08-17

### Añadido
- Autenticación JWT, perfiles y aislamiento de datos por usuario.
- Gestión multiusuario de hogares, habitaciones y dispositivos con roles.
- Integración IoT mediante MQTT, listener de telemetría y comandos remotos.
- Monitoreo de electricidad, agua y gas con límites, históricos y comparativas.
- Alertas, automatizaciones y registro de ejecuciones.
- Seguridad inteligente con cámaras, sensores, modos de armado y eventos.
- Dashboard avanzado, analítica histórica y exportación CSV.
- Motor de recomendaciones basado en consumo, conectividad y seguridad.
- Simulador IoT integrado con la misma tubería de telemetría real.
- Contenedores Docker para frontend/backend, PostgreSQL, Mosquitto y listener MQTT.
- Health/readiness checks, throttling, cabeceras y cookies de seguridad, logging y CI.
- Documentación técnica de arquitectura, API y despliegue.
- Refinamiento final responsive y de accesibilidad de la interfaz.

### Producción
- Versión estable inicial: `1.0.0`.
- Backend servido con Gunicorn y frontend con Nginx.
- Validación CI de backend, frontend y Docker Compose.
