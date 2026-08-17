# Política de seguridad de EcoHome

## Versiones soportadas

| Versión | Soporte |
|---|---|
| 1.0.x | ✅ Activo |
| < 1.0 | ❌ No soportado |

## Reporte responsable

No publiques credenciales, secretos, tokens JWT, datos personales, direcciones del hogar ni información de dispositivos IoT en issues públicos.

Ante una vulnerabilidad, documenta como mínimo el componente afectado, pasos de reproducción, impacto esperado y una prueba de concepto no destructiva. Evita explotar sistemas o dispositivos que no sean de tu propiedad o para los que no tengas autorización.

## Controles incluidos

EcoHome 1.0 incorpora autenticación JWT, autorización por hogar, throttling de API, cookies seguras según entorno, HSTS configurable, `X-Frame-Options`, `nosniff`, política de referer, separación de secretos por variables de entorno y ejecución no-root del backend en Docker.

## Producción

Para despliegues reales habilita TLS, utiliza contraseñas únicas para PostgreSQL y MQTT, reemplaza todos los secretos de ejemplo, desactiva `DEBUG`, limita `ALLOWED_HOSTS`, protege el broker MQTT con autenticación/TLS y evita exponer PostgreSQL a Internet.
