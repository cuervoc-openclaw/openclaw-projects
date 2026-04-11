# 🚀 OpenClaw Projects - Documentación Completa

## 📊 TABLA DE CONTENIDOS
1. [Sistemas Principales](#-sistemas-principales)
2. [Archivo por Archivo](#-archivo-por-archivo)
3. [Flujos de Trabajo](#-flujos-de-trabajo)
4. [Reglas para el Asistente](#-reglas-para-el-asistente)
5. [Instalación Rápida](#-instalación-rápida)

---

## 🤖 SISTEMAS PRINCIPALES

### 🎮 **1. LOL Coach**
**Descripción:** Sistema completo para análisis de partidas de League of Legends usando la API oficial de Riot Games.
**Archivo principal:** `lol_coach_final.py`
**Dependencias:** `requests`, `python-dotenv`, API key Riot Games

### 🎤 **2. Sistema STT (Speech-to-Text)**
**Descripción:** Transcripción de audio en tiempo real usando el modelo Vosk en español.
**Archivo principal:** `transcribe_audio.py`
**Dependencias:** `vosk`, `ffmpeg`, modelo Vosk español

### 🔐 **3. Dashboard de Credenciales Seguro**
**Descripción:** Interfaz web y servidor API para gestión segura de tokens y credenciales.
**Archivo principal:** `credentials_server_fixed.py`
**Interfaz:** `dashboard.html`
**Puertos:** 8080 (web), 8081 (API)

### ⚙️ **4. Automatización GitHub**
**Descripción:** Scripts para automatizar subida de repositorios, configuración SSH permanente.
**Archivos principales:** `final_execute.sh`, `setup_github_ssh.sh`

---

## 📁 ARCHIVO POR ARCHIVO

### 🐍 **ARCHIVOS PYTHON (.py)**

| Archivo | Descripción | Uso |
|---------|-------------|-----|
| **`lol_coach_final.py`** | Sistema completo LOL Coach. Obtiene estadísticas de partidas, análisis de rendimiento, recomendaciones. | `python3 lol_coach_final.py` |
| **`transcribe_audio.py`** | Transcripción de audio OGG → texto. Usa Vosk modelo español, conversión con ffmpeg. | `python3 transcribe_audio.py audio.ogg` |
| **`credentials_server_fixed.py`** | Servidor seguro para tokens. API REST con CORS, almacenamiento temporal en memoria. | `python3 credentials_server_fixed.py 8081` |
| **`lol_coach.py`** | Versión anterior del LOL Coach (backup). | Backup/referencia |
| **`transcribe_latest.py`** | Transcripción del último audio recibido. | Automático para mensajes de voz |
| **`transcribe_now.py`** | Script rápido de transcripción. | Uso inmediato |
| **`create_github_repo.py`** | Crear repositorios GitHub via API. | Automatización |
| **`create_father_repo.py`** | Crear repositorio father-documents. | Automatización |
| **`credentials_server.py`** | Versión anterior del servidor (backup). | Backup |
| **`test_api.py`** | Pruebas de APIs (Riot, etc.). | Testing |
| **`test_github_token.py`** | Validación de tokens GitHub. | Verificación |
| **`test_and_fix.py`** | Diagnóstico y reparación automática. | Mantenimiento |
| **`test_connection.py`** | Pruebas de conectividad. | Diagnóstico |
| **`cors_patch.py`** | Parche para problemas CORS. | Solución específica |
| **`read_credentials.py`** | Lectura de credenciales del servidor. | Debugging |
| **`execute_everything.py`** | Ejecución completa automatizada. | Automatización total |
| **`execute_with_server_token.py`** | Ejecución con token del servidor. | Flujo seguro |

### 🐚 **SCRIPTS BASH (.sh)**

| Archivo | Descripción | Uso |
|---------|-------------|-----|
| **`final_execute.sh`** | **SCRIPT PRINCIPAL** - Ejecuta TODO automáticamente con token GitHub. | `bash final_execute.sh TOKEN` |
| **`setup_github_ssh.sh`** | Configura SSH permanente (sin expiración) para GitHub. | `bash setup_github_ssh.sh` |
| **`fix_ssh_permanent.sh`** | Solución definitiva para problemas SSH. | `bash fix_ssh_permanent.sh` |
| **`fix_ssh_agent.sh`** | Reparar SSH agent caído. | `bash fix_ssh_agent.sh` |
| **`final_push_correct.sh`** | Push corregido (rama main vs master). | `bash final_push_correct.sh` |
| **`final_upload_direct.sh`** | Subida directa sin intermediarios. | `bash final_upload_direct.sh` |
| **`upload_all_ssh.sh`** | Subida completa usando SSH. | `bash upload_all_ssh.sh` |
| **`github_ssh_execute.sh`** | Ejecución con SSH configurado. | `bash github_ssh_execute.sh USER` |
| **`automate_with_chromium.sh`** | Automatización con navegador Chromium. | `bash automate_with_chromium.sh` |
| **`browser_alternative.sh`** | Alternativas sin navegador GUI. | `bash browser_alternative.sh` |
| **`quick_transcribe.sh`** | Transcripción rápida desde terminal. | `bash quick_transcribe.sh` |
| **`do_everything_now.sh`** | Versión anterior de automatización total. | Legacy |
| **`create_father_repo_simple.sh`** | Creación simple de repositorio. | `bash create_father_repo_simple.sh` |
| **`restart_servers.sh`** | Reiniciar todos los servidores. | `bash restart_servers.sh` |
| **`start_credentials_system.sh`** | Iniciar sistema de credenciales. | `bash start_credentials_system.sh` |
| **`start_definitive.sh`** | Inicio definitivo del sistema. | `bash start_definitive.sh` |
| **`start_simple.sh`** | Inicio simple. | `bash start_simple.sh` |
| **`stop_cors.sh`** | Detener servidores CORS. | `bash stop_cors.sh` |
| **`stop_definitive.sh`** | Detener sistema definitivo. | `bash stop_definitive.sh` |
| **`stop_fixed.sh`** | Detener servidores fixed. | `bash stop_fixed.sh` |
| **`stop_simple.sh`** | Detener sistema simple. | `bash stop_simple.sh` |
| **`fix_cors.sh`** | Reparar problemas CORS. | `bash fix_cors.sh` |
| **`fix_credentials.sh`** | Reparar sistema de credenciales. | `bash fix_credentials.sh` |

### 📝 **DOCUMENTACIÓN (.md)**

| Archivo | Descripción | Contenido |
|---------|-------------|-----------|
| **`AGENTS.md`** | Guía del workspace para el asistente. | Reglas, memoria, heartbeats, comportamiento. |
| **`CREDENTIALS_SYSTEM.md`** | Documentación del sistema de credenciales. | Arquitectura, seguridad, uso. |
| **`SOUL.md`** | Personalidad y comportamiento del asistente. | Vibe, reglas, estilo de comunicación. |
| **`IDENTITY.md`** | Identidad del asistente. | Nombre, creature, emoji, avatar. |
| **`USER.md`** | Información del usuario. | Nombre, preferencias, contexto. |
| **`TOOLS.md`** | Notas locales del asistente. | Configuraciones específicas, cheat sheets. |
| **`HEARTBEAT.md`** | Tareas periódicas del asistente. | Checklist, reminders, proactive work. |
| **`BOOTSTRAP.md`** | Configuración inicial (eliminar después). | Primer inicio, configuración básica. |
| **`UPDATE_README.md`** | Instrucciones para actualizar README. | Plantilla, estructura, reglas. |
| **`README_DETAILED.md`** | **ESTE ARCHIVO** - Documentación completa. | Todo explicado en detalle. |

### 🌐 **WEB/INTERFACES**

| Archivo | Descripción | Uso |
|---------|-------------|-----|
| **`dashboard.html`** | Interfaz web del dashboard de credenciales. | Abrir en navegador: `http://localhost:8080/dashboard.html` |
| **`dashboard.js`** | JavaScript del dashboard. | Funcionalidad frontend. |

### 📄 **OTROS ARCHIVOS**

| Archivo | Descripción | Contenido |
|---------|-------------|-----------|
| **`ultima_transcripcion.txt`** | Última transcripción generada. | Texto transcrito del audio más reciente. |

---

## 🔄 FLUJOS DE TRABAJO

### 🎮 **USAR LOL COACH:**
```bash
# 1. Configurar API key Riot Games en .env
echo "RIOT_API_KEY=tu_key_aqui" > .env

# 2. Ejecutar análisis
python3 lol_coach_final.py

# 3. Ver estadísticas y recomendaciones
```

### 🎤 **TRANSCRIBIR AUDIO:**
```bash
# 1. Asegurar modelo Vosk instalado
# 2. Convertir y transcribir
python3 transcribe_audio.py mensaje.ogg

# 3. Resultado en texto plano
```

### 🔐 **USAR DASHBOARD SEGURO:**
```bash
# 1. Iniciar servidor
python3 credentials_server_fixed.py 8081 &

# 2. Iniciar servidor web
python3 -m http.server 8080 &

# 3. Abrir interfaz
# Navegar a: http://localhost:8080/dashboard.html
```

### ⚙️ **AUTOMATIZAR GITHUB:**
```bash
# Opción A: Con token (expira)
bash final_execute.sh ghp_tu_token

# Opción B: SSH permanente (recomendado)
bash setup_github_ssh.sh
# Luego agregar clave SSH a GitHub
```

---

## 🤖 REGLAS PARA EL ASISTENTE

### 📋 **REGLAS DE DOCUMENTACIÓN:**
1. **POR CADA NUEVO ARCHIVO** creado, agregar entrada en esta tabla
2. **MANTENER ACTUALIZADO** el README cuando se modifiquen archivos
3. **DOCUMENTAR DEPENDENCIAS** y requisitos claramente
4. **INCLUIR EJEMPLOS** de uso práctico
5. **MANTENER ESTRUCTURA** consistente

### 🔧 **REGLAS DE MANTENIMIENTO:**
1. **BACKUP AUTOMÁTICO** a GitHub después de cambios importantes
2. **VERSIONAR CAMBIOS** con commits descriptivos
3. **PROBAR FUNCIONALIDAD** después de modificaciones
4. **MANTENER COMPATIBILIDAD** con sistemas existentes
5. **DOCUMENTAR CAMBIOS** en README

### 🚀 **REGLAS DE AUTOMATIZACIÓN:**
1. **SSH ES PRIORITARIO** sobre tokens temporales
2. **DASHBOARD SEGURO** para manejo de credenciales
3. **SCRIPTS REUTILIZABLES** y modulares
4. **ERROR HANDLING** robusto en todos los scripts
5. **LOGGING** detallado para debugging

### 📚 **REGLAS DE CONTEXTO:**
1. **LEER ESTE README** al inicio de cada sesión relevante
2. **ACTUALIZAR MEMORIA** con aprendizajes importantes
3. **MANTENER CONTINUIDAD** entre sesiones
4. **REFERENCIAR ARCHIVOS** existentes cuando sea posible
5. **EVITAR DUPLICACIÓN** de funcionalidad

---

## ⚡ INSTALACIÓN RÁPIDA

```bash
# 1. Clonar repositorio
git clone git@github.com:cuervoc-openclaw/openclaw-projects.git
cd openclaw-projects

# 2. Instalar dependencias Python
pip install vosk requests python-dotenv

# 3. Instalar ffmpeg (para STT)
sudo apt update && sudo apt install ffmpeg

# 4. Descargar modelo Vosk español
mkdir -p ~/vosk-models
cd ~/vosk-models
wget https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip
unzip vosk-model-small-es-0.42.zip

# 5. Configurar entorno
cp .env.example .env  # Si existe
# Editar .env con tus API keys
```

---

## 📞 SOPORTE Y MANTENIMIENTO

### 🔍 **SOLUCIÓN DE PROBLEMAS:**
1. **SSH no funciona:** `bash fix_ssh_permanent.sh`
2. **Servidor no inicia:** `bash restart_servers.sh`
3. **Transcripción falla:** Verificar ffmpeg y modelo Vosk
4. **API errors:** Verificar tokens en dashboard seguro

### 📈 **MEJORAS FUTURAS:**
- [ ] Interfaz gráfica para LOL Coach
- [ ] Transcripción en tiempo real
- [ ] Más integraciones (Twitter, Instagram, etc.)
- [ ] Dashboard con estadísticas
- [ ] Sistema de plugins

### 🏆 **CRÉDITOS:**
- **Desarrollado con:** OpenClaw Assistant
- **Usuario:** cuervoc-openclaw / David Salas
- **Fecha creación:** Abril 2026
- **Última actualización:** [FECHA_ACTUAL]

---

## 🎯 ¡TODO DOCUMENTADO Y LISTO!

**Cada archivo tiene propósito claro, cada sistema está documentado, cada flujo está explicado.**

**Regla para el asistente:** Mantener esta documentación actualizada con cada cambio significativo.