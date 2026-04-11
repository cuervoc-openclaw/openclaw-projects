#!/bin/bash
# Script para iniciar el sistema completo de credenciales seguras

echo "🚀 Iniciando Sistema de Credenciales Seguras OpenClaw"
echo "======================================================"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para verificar si un puerto está en uso
check_port() {
    netstat -tuln 2>/dev/null | grep ":$1 " > /dev/null
    return $?
}

# 1. Iniciar servidor de credenciales (puerto 8081)
echo -e "\n${BLUE}1. Iniciando servidor de credenciales seguras...${NC}"
if check_port 8081; then
    echo -e "${YELLOW}⚠️  El puerto 8081 ya está en uso${NC}"
    echo "   ¿Quieres detener el servidor existente? (s/n)"
    read -r response
    if [[ "$response" =~ ^[Ss]$ ]]; then
        echo "   Buscando proceso en puerto 8081..."
        PID=$(lsof -ti:8081 2>/dev/null | head -1)
        if [ -n "$PID" ]; then
            kill $PID
            echo "   Proceso $PID detenido"
            sleep 2
        fi
    else
        echo "   Usando servidor existente"
    fi
fi

# Iniciar servidor en segundo plano
echo "   Iniciando servidor Python en puerto 8081..."
python3 credentials_server.py > credentials_server.log 2>&1 &
SERVER_PID=$!
sleep 3

if check_port 8081; then
    echo -e "${GREEN}✅ Servidor iniciado (PID: $SERVER_PID)${NC}"
    echo "   Logs: credentials_server.log"
else
    echo -e "${RED}❌ Error iniciando servidor${NC}"
    echo "   Revisa credentials_server.log para detalles"
    exit 1
fi

# 2. Iniciar servidor web para dashboard (puerto 8080)
echo -e "\n${BLUE}2. Iniciando dashboard web...${NC}"
if check_port 8080; then
    echo -e "${YELLOW}⚠️  El puerto 8080 ya está en uso${NC}"
    echo "   ¿Quieres detener el servidor existente? (s/n)"
    read -r response
    if [[ "$response" =~ ^[Ss]$ ]]; then
        echo "   Buscando proceso en puerto 8080..."
        PID=$(lsof -ti:8080 2>/dev/null | head -1)
        if [ -n "$PID" ]; then
            kill $PID
            echo "   Proceso $PID detenido"
            sleep 2
        fi
    else
        echo "   Usando servidor existente"
    fi
fi

# Iniciar servidor HTTP simple
echo "   Iniciando servidor web en puerto 8080..."
python3 -m http.server 8080 --directory . > http_server.log 2>&1 &
HTTP_PID=$!
sleep 2

if check_port 8080; then
    echo -e "${GREEN}✅ Dashboard web iniciado (PID: $HTTP_PID)${NC}"
    echo "   Logs: http_server.log"
else
    echo -e "${RED}❌ Error iniciando servidor web${NC}"
    echo "   Revisa http_server.log para detalles"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

# 3. Mostrar URLs de acceso
echo -e "\n${BLUE}3. URLs de acceso:${NC}"
echo -e "${GREEN}   Dashboard:${NC} http://localhost:8080/dashboard.html"
echo -e "${GREEN}   Servidor API:${NC} http://localhost:8081"
echo -e "${GREEN}   Desde red local:${NC} http://$(hostname -I | awk '{print $1}'):8080/dashboard.html"

# 4. Mostrar endpoints disponibles
echo -e "\n${BLUE}4. Endpoints del servidor:${NC}"
echo "   GET  http://localhost:8081/status    - Estado del servidor"
echo "   GET  http://localhost:8081/get       - Obtener credenciales (preview)"
echo "   POST http://localhost:8081/          - Almacenar credenciales"
echo "   GET  http://localhost:8081/clear     - Borrar credenciales"

# 5. Scripts de utilidad
echo -e "\n${BLUE}5. Scripts disponibles:${NC}"
echo "   python3 read_credentials.py      - Leer credenciales (asistente)"
echo "   python3 credentials_server.py    - Servidor standalone"
echo "   ./start_credentials_system.sh    - Este script"

# 6. Comandos para usar credenciales
echo -e "\n${BLUE}6. Ejemplos de uso:${NC}"
echo "   # Crear repo GitHub con token seguro"
echo "   python3 -c \""
echo "   import requests"
echo "   from read_credentials import get_github_token"
echo "   token = get_github_token()"
echo "   if token:"
echo "       requests.post('https://api.github.com/user/repos',"
echo "           headers={'Authorization': f'token {token}'},"
echo "           json={'name': 'my-repo'})"
echo "   \""

# 7. Información de seguridad
echo -e "\n${BLUE}7. Información de seguridad:${NC}"
echo "   🔒 Credenciales almacenadas solo en memoria RAM"
echo "   ⏱️  Auto-expiración después de 5 minutos"
echo "   🌐 Solo accesible desde localhost"
echo "   🚫 Nunca se escriben en disco"

# 8. Comando para detener
echo -e "\n${BLUE}8. Para detener el sistema:${NC}"
echo "   ./stop_credentials_system.sh"
echo "   o"
echo "   kill $SERVER_PID $HTTP_PID"

# Crear script de detención
cat > stop_credentials_system.sh << 'EOF'
#!/bin/bash
echo "🛑 Deteniendo Sistema de Credenciales Seguras..."
echo "================================================"

# Detener servidor de credenciales
echo "1. Deteniendo servidor de credenciales (puerto 8081)..."
PID1=$(lsof -ti:8081 2>/dev/null | head -1)
if [ -n "$PID1" ]; then
    kill $PID1
    echo "   Servidor detenido (PID: $PID1)"
else
    echo "   Servidor no encontrado"
fi

# Detener servidor web
echo "2. Deteniendo dashboard web (puerto 8080)..."
PID2=$(lsof -ti:8080 2>/dev/null | head -1)
if [ -n "$PID2" ]; then
    kill $PID2
    echo "   Dashboard detenido (PID: $PID2)"
else
    echo "   Dashboard no encontrado"
fi

echo -e "\n✅ Sistema detenido correctamente"
EOF

chmod +x stop_credentials_system.sh

echo -e "\n${GREEN}======================================================${NC}"
echo -e "${GREEN}✅ Sistema de credenciales iniciado correctamente${NC}"
echo -e "${GREEN}======================================================${NC}"
echo ""
echo "📝 Pasos siguientes:"
echo "   1. Abre http://localhost:8080/dashboard.html en tu navegador"
echo "   2. Ingresa tus tokens en el formulario seguro"
echo "   3. Haz clic en 'Enviar Credenciales al Asistente'"
echo "   4. Yo podré usarlas de forma segura por 5 minutos"
echo ""
echo "🚀 ¡Listo para usar!"