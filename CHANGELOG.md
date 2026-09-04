# Changelog

Todos los cambios relevantes de EcoHome se documentan en este archivo.

## [1.1.0] - 2026-09-04

### Calidad
- Se incorpora Vitest con Testing Library para pruebas automatizadas del frontend.
- Se añaden pruebas del flujo de autenticación y de las etiquetas de estado de dispositivos IoT.
- El CI ahora ejecuta typecheck, pruebas frontend, auditoría de dependencias de producción y build de Vite.
- Se añade Dependabot para dependencias Python, npm, GitHub Actions y Docker.

### Accesibilidad
- Se mejora la semántica de la pantalla de inicio de sesión con `aria-labelledby`, `aria-busy`, contenido decorativo oculto a lectores de pantalla y errores anunciados con `role="alert"`.

### Alcance
- EcoHome se mantiene como proyecto académico evolucionado y proyecto de portafolio; esta versión refuerza calidad y mantenibilidad sin convertirlo en un producto comercial.

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
