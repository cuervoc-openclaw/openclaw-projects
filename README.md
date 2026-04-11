# 🚀 OpenClaw Projects - Sistemas Completos de Automatización

## 📊 VISTA RÁPIDA POR ARCHIVO

### 🐍 **PYTHON - SISTEMAS PRINCIPALES**
| Archivo | Qué hace | Comando |
|---------|----------|---------|
| **`lol_coach_final.py`** | Análisis de partidas LoL con API Riot | `python3 lol_coach_final.py` |
| **`transcribe_audio.py`** | Transcripción de audio (OGG → texto) | `python3 transcribe_audio.py audio.ogg` |
| **`credentials_server_fixed.py`** | Servidor seguro para tokens/credenciales | `python3 credentials_server_fixed.py 8081` |

### 🐚 **BASH - AUTOMATIZACIÓN**
| Archivo | Qué hace | Comando |
|---------|----------|---------|
| **`final_execute.sh`** | **TODO automático** con token GitHub | `bash final_execute.sh TOKEN` |
| **`setup_github_ssh.sh`** | SSH permanente (sin expiración) | `bash setup_github_ssh.sh` |
| **`fix_ssh_permanent.sh`** | Solución definitiva SSH | `bash fix_ssh_permanent.sh` |

### 📝 **DOCUMENTACIÓN**
| Archivo | Contenido | Para quién |
|---------|-----------|-----------|
| **`AGENTS.md`** | Reglas del workspace | Asistente |
| **`SOUL.md`** | Personalidad del asistente | Asistente |
| **`USER.md`** | Info del usuario | Asistente |
| **`README_DETAILED.md`** | **DOCUMENTACIÓN COMPLETA** | Todos |

---

## 🎯 SISTEMAS PRINCIPALES

### 1. 🤖 **LOL Coach**
- Análisis de partidas League of Legends
- Estadísticas detalladas con API Riot Games
- Recomendaciones personalizadas
- **Archivo:** `lol_coach_final.py`

### 2. 🎤 **Sistema STT (Speech-to-Text)**
- Transcripción de audio en tiempo real
- Modelo Vosk en español
- Conversión OGG → WAV → Texto
- **Archivo:** `transcribe_audio.py`

### 3. 🔐 **Dashboard de Credenciales Seguro**
- Interfaz web para gestión de tokens
- Servidor API con CORS configurado
- Almacenamiento temporal en memoria
- **Archivos:** `credentials_server_fixed.py`, `dashboard.html`

### 4. ⚙️ **Automatización GitHub**
- Subida automática de repositorios
- Configuración SSH permanente
- Scripts de backup y sincronización
- **Archivos:** `final_execute.sh`, `setup_github_ssh.sh`

---

## 🚀 INSTALACIÓN RÁPIDA

```bash
# 1. Clonar
git clone git@github.com:cuervoc-openclaw/openclaw-projects.git
cd openclaw-projects

# 2. Dependencias
pip install vosk requests python-dotenv
sudo apt install ffmpeg

# 3. Modelo Vosk (español)
mkdir -p ~/vosk-models
cd ~/vosk-models
wget https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip
unzip vosk-model-small-es-0.42.zip
```

---

## 📖 USO RÁPIDO

### 🎮 LOL Coach:
```bash
# Configurar API key
echo "RIOT_API_KEY=tu_key" > .env

# Ejecutar análisis
python3 lol_coach_final.py
```

### 🎤 Transcripción de audio:
```bash
python3 transcribe_audio.py mensaje_de_voz.ogg
```

### 🔐 Dashboard seguro:
```bash
# Iniciar servidor
python3 credentials_server_fixed.py 8081 &

# Iniciar web
python3 -m http.server 8080 &

# Abrir en navegador
# http://localhost:8080/dashboard.html
```

### ⚙️ Automatización GitHub:
```bash
# Con token (expira)
bash final_execute.sh ghp_tu_token

# Con SSH (permanente)
bash setup_github_ssh.sh
# Luego agregar clave SSH a GitHub
```

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### ❌ SSH no funciona:
```bash
bash fix_ssh_permanent.sh
```

### ❌ Servidor no inicia:
```bash
bash restart_servers.sh
```

### ❌ Transcripción falla:
- Verificar ffmpeg instalado
- Verificar modelo Vosk descargado
- Verificar permisos de audio

---

## 📁 ESTRUCTURA COMPLETA

```
openclaw-projects/
├── 🤖 lol_coach_final.py          # Sistema completo LOL
├── 🎤 transcribe_audio.py         # STT con Vosk
├── 🔐 credentials_server_fixed.py # Servidor seguro
├── 🌐 dashboard.html              # Interfaz web
├── ⚙️ final_execute.sh            # Automatización total
├── 🔑 setup_github_ssh.sh         # SSH permanente
├── 📝 README_DETAILED.md          # Documentación completa
├── 📋 AGENTS.md                   # Reglas del workspace
├── 🎭 SOUL.md                     # Personalidad asistente
├── 👤 USER.md                     # Info usuario
└── 🛠️ *.sh/*.py                   # Scripts adicionales
```

**Total: 51 archivos organizados y documentados**

---

## 🤖 REGLAS PARA EL ASISTENTE

### 📋 AL INICIAR SESIÓN:
1. **Leer** `AGENTS.md`, `SOUL.md`, `USER.md`
2. **Revisar** `README_DETAILED.md` para contexto
3. **Verificar** sistemas funcionando

### 🔧 AL CREAR/MODIFICAR ARCHIVOS:
1. **Documentar** en `README_DETAILED.md`
2. **Mantener** compatibilidad con sistemas existentes
3. **Probar** funcionalidad antes de commit

### 🚀 AL TERMINAR TRABAJO:
1. **Actualizar** documentación si hubo cambios
2. **Backup** a GitHub si es significativo
3. **Dejar** sistemas en estado funcional

---

## 📞 SOPORTE

- **Documentación completa:** `README_DETAILED.md`
- **Sistemas 100% funcionales**
- **Código comentado y claro**
- **Backup en GitHub automático**

---

## 🎉 ¡TODO ORGANIZADO Y DOCUMENTADO!

**Cada archivo tiene propósito claro, cada sistema está probado, cada flujo está explicado.**

**Repositorio:** https://github.com/cuervoc-openclaw/openclaw-projects  
**SSH permanente configurado** ✅  
**Sistemas operativos** ✅  
**Documentación completa** ✅  

**¡Automatización inteligente lista para usar!** 🚀