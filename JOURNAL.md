# 📓 JOURNAL.md - The Last Garrison
## Registro de Desarrollo y Memoria del Proyecto

---

## Sprint 1: 11/05/2026 - FUNDACIÓN Y ARQUITECTURA
- **Módulo Completado:** Estructura base del proyecto
- **Estado Actual:** Estructura creada, documentación inicial, configuración Docker
- **Siguiente Sprint:** Entidades Soldado y sistema de estado básico

## Roadmap Completo - 10 Sprints

### Sprint 1 ✅ [11/05/2026]
- Setup inicial - Carpeta estructura - README - JOURNAL - Docker base - Git init

### Sprint 2 [12/05/2026]
- **Entidades Soldado**
  - Modelo de datos básico (health, morale, hunger)
  - Sistema de persistencia SQLite
  - API endpoints CRUD soldados

### Sprint 3 [13/05/2026]
- **Entorno Simulado**
  - Grilla 2D del patio/area
  - Sistema de coordenadas
  - Backend de mapeo del terreno

### Sprint 4 [14/05/2026]
- **Frontend God View**
  - Interfaz HTML/JS básica
  - Renderizado de la grilla
  - Estado de recursos visible

### Sprint 5 [15/05/2026]
- **Agente General (IA Orquestadora)**
  - Integración con LLM
  - Análisis situacional
  - API de toma decisiones estratégicas

### Sprint 6 [16/05/2026]
- **Sistema de Cultivos**
  - Mecánica de cosecha
  - Ciclos de crecimiento
  - Inventario de recursos

### Sprint 7 [17/05/2026]
- **Evento Comerciante**
  - Sistema de eventos aleatorios
  - Integración con inventario
  - API de transacción

### Sprint 8 [18/05/2026]
- **Evento Patrullas Enemigas**
  - Sistema de riesgo
  - Decisiones tácticas de General
  - Estados de alerta

### Sprint 9 [19/05/2026]
- **Sistema de Reportes**
  - Integración WhatsApp Evolution API
  - cron reporter.py
  - Notificaciones de sprint completion

### Sprint 10 [20/05/2026]
- **Polish y Despliegue**
  - Testing end-to-end
  - Configuración Coolify final
  - Deploy y documentación completa

---

## Estado de Arquitectura Actual
- **Backend:** FastAPI Python 3.10+ ✅
- **Frontend:** HTML/JS vanilla ✅
- **DB:** SQLite + volumen Docker ✅
- **Infra:** Docker compose base ✅
- **CI/CD:** Git + commit convencional ✅

## Tareas del Día
1. Estructura de carpetas
2. README.md completo
3. Configuración Docker
4. .env.example
5. Primer commit
6. Preparar reporter.py mock

## Notas Sistema
- Memory: Ollama local + embeddings
- Modelo: DeepSeek V3 (costo eficiente)
- WhatsApp: +56949336814 configurado
- Workspace: Directorio principal

## Log de Cambios
- 11/05 01:45 - Sprint 1 iniciado
- 11/05 01:46 - JOURNAL.md creado con roadmap