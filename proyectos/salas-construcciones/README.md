# 🏗️ Salas Construcciones

*Creado: 2026-04-26 | Última actualización: 2026-04-28*

## URLs

| Frontend | Backend (API) |
|---|---|
| https://salasconstrucciones.com | https://api.salasconstrucciones.com |

## Stack técnico

- **Frontend**: Astro
- **Backend**: WordPress Headless (REST API)
- **API**: `csalas/v1` namespace custom
- **Hosting**: LiteSpeed Web Server

## Estado

- ✅ Frontend online
- ✅ API WordPress operativa
- ✅ Contenido poblado (ver WP-SETUP.md)
- ❌ Frontend no sincronizado con API

## Conexión

Para operar el WordPress via API necesitas:
1. Ir a Perfil > Application Passwords
2. Generar password para la app
3. Usar autenticación Basic + nonce

## Scripts

- `scripts/update_services.py` — Actualizar servicios vía API

## Pendientes

- [ ] Agregar datos de contacto reales
- [ ] Subir imágenes de proyectos realizados
- [ ] Sincronizar frontend Astro con datos de la API
- [ ] Configurar SEO (meta tags, OG, schema)
