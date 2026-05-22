# 📓 JOURNAL.md - The Last Garrison
## Registro de Desarrollo y Memoria del Proyecto

---

## Sprint 1 (Mayo 2026): FUNDACIÓN Y ARQUITECTURA ✅
- **Módulo Completado:** Estructura base del proyecto + Soldados + Mundo + Frontend base
- **Commits:** `50a6100` (estructura inicial), `942da19` (mundo simulado + grid 20x20 + soldados CRUD)

## Sprint 4: 22/05/2026 — AGENTE GENERAL LLM + CULTIVO/GESTIÓN 🌾🎖️
- **Módulo Completado:** Agente General (IA Orquestadora), motor de simulación, sistema de cultivos y gestión de recursos

### 🆕 Archivos Creados
- **`core/llm_agent.py`** — Agente General con backend OpenAI/Anthropic/Mock
  - Análisis situacional del mundo, soldados y recursos
  - Generación de órdenes tácticas con prioridades
  - Memoria de decisiones (últimas 20)
  - Estado de ánimo del General (confianza, preocupación, frustración)
  - Backend automático: Mock por defecto, OpenAI con API key en .env
  - 3 estrategias: Defensiva 🛡️, Agresiva ⚔️, Balanceada ⚖️

- **`core/simulation.py`** — Motor de simulación temporal
  - Sistema de ticks (1 tick ~ 1 hora, 24 ticks = 1 día)
  - Consumo de comida por soldado por tick
  - Deterioro por hambre: daño a salud y pérdida de moral
  - Crecimiento de cultivos en granjas (cada 3 ticks)
  - Eventos aleatorios con pesos contextuales:
    - 📦 Suministros aliados (si comida < 20)
    - 🧳 Comerciante
    - 🐗 Jabalí en la granja
    - 🔭 Reporte de exploración
    - ⚠️ Patrulla enemiga (raro)
    - 🏃 Deserción (si moral baja)
  - Análisis automático del General cada 4 ticks
  - Log de eventos históricos

- **`api/routes/events.py`** — Endpoints REST (General + Simulación)
  - `GET /api/events/general/status` — Estado del General
  - `POST /api/events/general/analyze` — Análisis bajo demanda
  - `GET /api/events/general/memory` — Historial de decisiones
  - `POST /api/events/general/change-strategy` — Cambiar estrategia
  - `POST /api/events/simulation/tick?times=N` — Avanzar N ticks
  - `GET /api/events/simulation/summary` — Resumen completo
  - `GET /api/events/simulation/events` — Historial de eventos
  - `POST /api/events/simulation/event` — Disparar evento manual
  - `POST /api/events/simulation/reset` — Resetear simulación
  - `GET /api/events/report` — Reporte completo (panorama general)

### 🎨 Frontend Actualizado
- **War Operations Center** — Interfaz de control tipo terminal militar
- Panel de recursos con barras visuales y alertas de escasez (rojo si < 20)
- Tarjetas de soldados con stats visuales (HP, moral, hambre, energía)
- Órdenes del General con indicador de estado de ánimo y nivel de alerta
- Bitácora de eventos cronológica (scroll infinito)
- Controles: ticks 1/5/24, analizar, estrategia, eventos manuales, reset
- Sistema de flash notifications

### ⚙️ Mecánicas Implementadas
- ✅ Consumo de recursos por tick
- ✅ Hambre → daño progresivo sin comida
- ✅ Caída de moral sin alimento
- ✅ Crecimiento de cultivos automático en granjas
- ✅ Cosecha automática → recursos
- ✅ Eventos aleatorios con pesos contextuales
- ✅ Análisis del General cada 4 ticks
- ✅ 3 modos estratégicos intercambiables
- ✅ Memoria del General (últimas 20 decisiones)
- ✅ Soporte para OpenAI y Anthropic (LLM real con API key)

### 🧪 Cómo Probar
1. `POST /api/soldiers/init` — Crear soldados por defecto
2. `POST /api/events/simulation/tick?times=5` — Avanzar tiempo
3. `POST /api/events/general/analyze` — Ver qué decide el General
4. Abrir `http://localhost:8000/static` para el dashboard visual

### 📌 Notas Técnicas
- Por defecto usa backend Mock (reglas) — sin API keys necesarias
- Configurar OPENAI_API_KEY en .env activa análisis con GPT-4o-mini
- Costo ~$0.001 por análisis (modelo chato)
- La API key es opcional; el mock es funcional como sistema de reglas

---

## Roadmap Restante (versión compactada)

### Sprint 5 🎯
- Evento Comerciante completo (comprar/vender/mejoras)
- Despliegue WhatsApp + cron reporter
- Notificaciones automáticas de eventos críticos

### Sprint 6 🎯
- Evento Patrullas Enemigas con combate
- Sistema de defensa y bajas
- Polish final y deploy Coolify

## Estado de Arquitectura Actual
- **Backend:** FastAPI Python 3.10+ ✅
- **Frontend:** HTML/JS vanilla (War Operations Center) ✅
- **DB:** SQLite + SQLAlchemy ✅
- **General:** LLM Agent (Mock/OpenAI/Anthropic) ✅
- **Simulación:** Motor de ticks + eventos aleatorios + cultivos ✅
- **Infra:** Docker compose + Coolify ready ✅
- **CI/CD:** Git + commit convencional ✅

## Notas Sistema
- Memory: Ollama local + embeddings
- Modelo: DeepSeek V3 (costo eficiente)
- WhatsApp: +56949336814 configurado
- Workspace: Directorio principal