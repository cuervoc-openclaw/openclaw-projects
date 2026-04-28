      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm run build
      - uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: ./frontend

  deploy-backend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm run build
      - uses: railway/action@v1
        with:
          service: neuroasistente-backend
          token: ${{ secrets.RAILWAY_TOKEN }}
```

### 6.3 Monitoreo y Alertas
```yaml
# Configuración básica de monitoreo
monitoring:
  uptime: uptimerobot.com  # Monitoreo de uptime
  errors: sentry.io        # Tracking de errores
  analytics: plausible.io  # Analytics simple y privado
  logs: logtail.com        # Centralización de logs
  
alerts:
  - channel: telegram      # Alertas al equipo
    conditions:
      - error_rate > 5%
      - response_time > 3000ms
      - uptime < 99%
```

### 6.4 Backup y Recuperación
```bash
#!/bin/bash
# scripts/backup.sh
BACKUP_DIR="./backups/$(date +%Y-%m-%d)"
mkdir -p $BACKUP_DIR

# Backup de base de datos
pg_dump $DATABASE_URL > $BACKUP_DIR/database.sql

# Backup de archivos de usuario
tar -czf $BACKUP_DIR/uploads.tar.gz ./uploads

# Backup de configuración
cp .env $BACKUP_DIR/
cp docker-compose.yml $BACKUP_DIR/

# Subir a Backblaze B2
b2 upload-file neuroasistente-backups $BACKUP_DIR/database.sql database-$(date +%s).sql

# Limpiar backups antiguos (mantener últimos 30 días)
find ./backups -type d -mtime +30 -exec rm -rf {} \;
```

---

## 7. SEGURIDAD Y PRIVACIDAD

### 7.1 Medidas de Seguridad
- **Autenticación:** JWT con refresh tokens rotativos
- **Autorización:** RBAC (Role-Based Access Control)
- **Encriptación:** TLS 1.3, datos en reposo encriptados
- **Rate limiting:** 100 requests/minuto por usuario
- **CORS:** Orígenes permitidos explícitamente
- **Sanitización:** Input validation con Zod

### 7.2 Cumplimiento GDPR
```typescript
// Política de privacidad implementada
class PrivacyService {
  async exportUserData(userId: string) {
    // Exportar todos los datos del usuario en formato estándar
    const data = await this.getAllUserData(userId);
    return {
      user: data.user,
      tasks: data.tasks,
      habits: data.habits,
      achievements: data.achievements,
      metadata: {
        exportedAt: new Date(),
        format: 'GDPR Article 20'
      }
    };
  }
  
  async deleteUserData(userId: string) {
    // Borrado completo (GDPR "right to be forgotten")
    await this.anonymizeUser(userId);
    await this.deleteUserRecords(userId);
    await this.logDeletion(userId, 'GDPR_REQUEST');
  }
}
```

### 7.3 Consideraciones Éticas (IA)
- **Transparencia:** Usuario sabe cuándo se usa IA
- **Control:** Usuario puede desactivar funciones de IA
- **Sesgo:** Monitoreo continuo de sesgos en recomendaciones
- **Privacidad:** Datos de usuario nunca usados para entrenar modelos

---

## 8. ROADMAP DE IMPLEMENTACIÓN

### Fase 1 (Semanas 1-2): MVP Básico
- [ ] Setup del proyecto (frontend + backend)
- [ ] Autenticación básica
- [ ] CRUD de tareas
- [ ] Temporizador Pomodoro simple
- [ ] Despliegue inicial

### Fase 2 (Semanas 3-4): Funcionalidades TDAH
- [ ] Sistema de hábitos
- [ ] Desglose de tareas con IA
- [ ] Recordatorios en-app
- [ ] Sistema de logros
- [ ] Integración WhatsApp básica

### Fase 3 (Semanas 5-6): Refinamiento
- [ ] PWA completa (offline, installable)
- [ ] Accesibilidad WCAG 2.1 AA
- [ ] Temas (claro/oscuro/alto contraste)
- [ ] Sincronización multi-dispositivo
- [ ] Analytics básico

### Fase 4 (Semanas 7-8): Escalabilidad
- [ ] Sistema de agentes OpenClaw
- [ ] Actualización mensual automatizada
- [ ] Comunidad de usuarios
- [ ] Documentación completa
- [ ] Plan de mantenimiento

---

## 9. CONCLUSIÓN

### 9.1 Resumen Arquitectónico
Esta arquitectura proporciona:
- **Frontend minimalista** diseñado específicamente para TDAH
- **Backend escalable** con separación de responsabilidades
- **Sistema de agentes** autónomo para desarrollo y mantenimiento
- **Actualización continua** basada en investigación
- **Infraestructura costo-cero** para usuarios

### 9.2 Próximos Pasos Inmediatos
1. **Crear repositorio GitHub** con estructura de carpetas
2. **Implementar MVP** (tareas + Pomodoro + autenticación)
3. **Configurar agentes OpenClaw** para desarrollo paralelo
4. **Desplegar versión inicial** para testing
5. **Iniciar ciclo de feedback** con usuarios TDAH

### 9.3 Métricas de Éxito
- **Usabilidad:** Tiempo para primera tarea completada < 2 minutos
- **Adopción:** 100 usuarios en primer mes
- **Retención:** 40% de usuarios activos después de 30 días
- **Impacto:** Mejora reportada en gestión diaria por 70% de usuarios
- **Accesibilidad:** Puntuación Lighthouse > 90 en todas las categorías

---

**🎯 ARQUITECTURA COMPLETA DEFINIDA**

**Documentos generados:**
1. `/home/cuervoc/.openclaw/workspace/docs/analisis_inicial_tdah.md`
2. `/home/cuervoc/.openclaw/workspace/docs/arquitectura_dashboard.md`

**¿Procedemos con la Fase 2 (Desarrollo del MVP)?** 🚀