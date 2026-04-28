# 🔐 Sistema de Credenciales Seguras OpenClaw

Sistema completo para manejar tokens, API keys y credenciales de forma segura sin exponerlas en chat.

## 🎯 Objetivo

Permitir que el asistente OpenClaw acceda a credenciales (GitHub tokens, API keys, etc.) de forma segura:
- **Sin** compartir en texto plano en chat
- **Sin** almacenar en disco
- **Con** auto-expiración (5 minutos)
- **Solo** accesible desde localhost

## 📁 Estructura del Sistema

```
.
├── dashboard.html              # Interfaz web para ingresar credenciales
├── credentials_server.py       # Servidor backend seguro (puerto 8081)
├── read_credentials.py         # Cliente para leer credenciales (asistente)
├── dashboard.js               # Cliente JavaScript para el dashboard
├── start_credentials_system.sh # Script de inicio completo
├── stop_credentials_system.sh  # Script de detención
└── CREDENTIALS_SYSTEM.md      # Esta documentación
```

## 🚀 Inicio Rápido

### Método 1: Script completo
```bash
cd /home/cuervoc/.openclaw/workspace
./start_credentials_system.sh
```

### Método 2: Manual
```bash
# 1. Iniciar servidor de credenciales
python3 credentials_server.py &
# (Verifica que esté en puerto 8081)

# 2. Iniciar servidor web
python3 -m http.server 8080 --directory . &
# (Dashboard en puerto 8080)

# 3. Abrir dashboard
# Navega a: http://localhost:8080/dashboard.html
```

## 🌐 URLs de Acceso

- **Dashboard:** http://localhost:8080/dashboard.html
- **Servidor API:** http://localhost:8081
- **Desde red local:** http://[TU_IP]:8080/dashboard.html

## 🔧 Endpoints del Servidor

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/status` | Estado del servidor |
| GET | `/get` | Obtener credenciales (solo preview) |
| POST | `/` | Almacenar credenciales |
| GET | `/clear` | Borrar todas las credenciales |

## 📋 Flujo de Trabajo

### Para el Usuario:
1. **Abrir dashboard** en navegador
2. **Ingresar tokens** en formulario seguro
3. **Hacer clic** en "Enviar Credenciales al Asistente"
4. **Credenciales disponibles** por 5 minutos

### Para el Asistente (OpenClaw):
1. **Importar** `read_credentials.py`
2. **Llamar** `get_github_token()` o `get_riot_key()`
3. **Usar token** en scripts/API calls
4. **Token expira** automáticamente en 5 minutos

## 💻 Uso en Scripts Python

```python
# Ejemplo: Crear repositorio GitHub con token seguro
from read_credentials import get_github_token
import requests

token = get_github_token()
if token:
    response = requests.post(
        'https://api.github.com/user/repos',
        headers={'Authorization': f'token {token}'},
        json={'name': 'my-new-repo', 'private': False}
    )
    print(f"Repo creado: {response.status_code}")
```

## 🔐 Características de Seguridad

### ✅ Implementadas:
- **Almacenamiento en memoria RAM** (no en disco)
- **Auto-expiración** (5 minutos)
- **Solo localhost** (no accesible desde internet)
- **Preview limitado** en endpoints HTTP
- **Borrado seguro** con script `stop_credentials_system.sh`

### 🚫 Prevenidas:
- ❌ Tokens en logs de chat
- ❌ Tokens en archivos de texto
- ❌ Acceso desde IPs externas
- ❌ Persistencia indefinida

## 🛠️ Scripts de Utilidad

### `read_credentials.py`
```bash
# Ver estado y credenciales disponibles
python3 read_credentials.py

# Salida ejemplo:
# 🔐 OpenClaw Credentials Reader
# ==================================================
# ✅ Servidor activo: ok
# 📊 Almacenamiento activo: True
# ⏱️  Expirado: False
# 📋 Credenciales disponibles:
#    GitHub: ✅
#      Preview: ghp_abc123...xyz9
#    Riot Games: ✅
#      Preview: RGAPI-1234...abcd
```

### `credentials_server.py` (standalone)
```bash
# Iniciar servidor manualmente
python3 credentials_server.py
# Escucha en http://localhost:8081
```

## 📊 Dashboard Web

Interfaz visual con:
- ✅ Validación de formato de tokens
- ✅ Preview seguro (primeros y últimos caracteres)
- ✅ Indicador de conexión al servidor
- ✅ Botón para borrar credenciales
- ✅ Información de seguridad en tiempo real

## 🚨 Solución de Problemas

### Servidor no inicia:
```bash
# Verificar puertos en uso
netstat -tuln | grep :8080
netstat -tuln | grep :8081

# Ver logs
tail -f credentials_server.log
tail -f http_server.log
```

### Dashboard no carga:
1. Verificar que ambos servidores estén corriendo
2. Verificar firewall/localhost restrictions
3. Probar con `curl http://localhost:8081/status`

### Tokens no accesibles:
1. Verificar que no hayan expirado (5 minutos)
2. Re-enviar desde dashboard
3. Verificar formato de tokens

## 🔄 Integración con OpenClaw

El asistente puede usar las credenciales para:
1. **GitHub:** Crear repos, push código, manejar issues
2. **Riot API:** Acceder a datos de League of Legends
3. **APIs personalizadas:** Cualquier servicio que requiera tokens
4. **Automatizaciones seguras** sin exponer credenciales

## 📝 Mejores Prácticas

1. **Usar tokens temporales** (GitHub PATs con expiración)
2. **Scope mínimo necesario** (ej: solo `public_repo` en GitHub)
3. **Borrar después de usar** con `/clear` endpoint
4. **No reutilizar tokens** entre sesiones
5. **Monitorizar logs** de acceso

## 🎯 Casos de Uso

### 1. GitHub Automation
```python
# Subir proyectos a repositorio
token = get_github_token()
if token:
    # Inicializar repo, commit, push
    pass
```

### 2. Riot Games API
```python
# Acceder a datos de League of Legends
key = get_riot_key()
if key:
    # Consultar estadísticas, partidas, etc.
    pass
```

### 3. APIs de Terceros
```python
# Cualquier API que requiera autenticación
# Configurar en dashboard como "Custom API"
```

## 🔮 Roadmap Futuro

- [ ] Encriptación en memoria
- [ ] Auditoría de acceso
- [ ] Rotación automática de tokens
- [ ] Integración con vaults externos (Hashicorp, AWS)
- [ ] Dashboard con más servicios preconfigurados

## 📞 Soporte

Para problemas o preguntas:
1. Revisar logs en `credentials_server.log` y `http_server.log`
2. Verificar que los puertos 8080 y 8081 estén libres
3. Probar con `curl http://localhost:8081/status`
4. Reiniciar con `./stop_credentials_system.sh && ./start_credentials_system.sh`

---

**⚠️ ADVERTENCIA:** Este sistema es para desarrollo/local. No usar para credenciales de producción críticas sin medidas de seguridad adicionales.