# 🏗️ Salas Construcciones

*Creado: 2026-04-26 | Última actualización: 2026-04-26*

## URLs

| Frontend | Backend (API) |
|---|---|
| https://salasconstrucciones.com | https://api.salasconstrucciones.com |

## Stack técnico

- **Frontend**: Astro
- **Backend**: WordPress Headless (API REST)
- **WordPress API**: Responde en `https://api.salasconstrucciones.com/?rest_route=/`
- **Namespace personalizado**: `csalas/v1` (creado previamente)
- **Autenticación**: Application Passwords disponible

## Estado del sitio

- Frontend online ✅ (tema con servicios y presupuestos)
- API WordPress online ✅
- WordPress REST API funciona con `?rest_route=` en lugar de `/wp-json/` (configuración del servidor LiteSpeed)
- Hosting: LiteSpeed Web Server

## Historial

- Se subió información al WordPress anteriormente (contenido, servicios, etc.)

## Pendientes

- [ ] Revisar contenido actual del WordPress
- [ ] Sincronizar frontend con los datos de la API
- [ ] Documentar endpoints del namespace `csalas/v1`
