#!/bin/bash
echo "🔧 Reparando Sistema de Credenciales"
echo "===================================="

# Matar procesos anteriores
echo "1. Limpiando procesos anteriores..."
pkill -f "http.server" 2>/dev/null
pkill -f "credentials_server.py" 2>/dev/null
pkill -f "python3 -m http.server" 2>/dev/null
sleep 2

# Encontrar puertos libres
find_free_port() {
    for port in {8080..8090}; do
        if ! ss -tuln 2>/dev/null | grep -q ":$port "; then
            echo $port
            return
        fi
    done
    echo 8080
}

HTTP_PORT=$(find_free_port)
API_PORT=$((HTTP_PORT + 1))

echo "2. Usando puertos: HTTP=$HTTP_PORT, API=$API_PORT"

# Actualizar configuración
echo "3. Actualizando configuración..."
sed -i "s/localhost:[0-9]\+/localhost:$API_PORT/g" dashboard.html 2>/dev/null
sed -i "s/8081/$API_PORT/g" read_credentials.py 2>/dev/null

# Iniciar servidor API
echo "4. Iniciando servidor API en puerto $API_PORT..."
python3 credentials_server.py $API_PORT > api_server.log 2>&1 &
API_PID=$!
sleep 3

# Verificar API
if ss -tuln 2>/dev/null | grep -q ":$API_PORT "; then
    echo "   ✅ Servidor API iniciado (PID: $API_PID)"
else
    echo "   ❌ Error iniciando API. Ver api_server.log"
    cat api_server.log
    exit 1
fi

# Iniciar servidor HTTP
echo "5. Iniciando dashboard en puerto $HTTP_PORT..."
python3 -m http.server $HTTP_PORT --directory . > http_server.log 2>&1 &
HTTP_PID=$!
sleep 2

# Verificar HTTP
if ss -tuln 2>/dev/null | grep -q ":$HTTP_PORT "; then
    echo "   ✅ Dashboard iniciado (PID: $HTTP_PID)"
else
    echo "   ❌ Error iniciando dashboard. Ver http_server.log"
    cat http_server.log
    kill $API_PID 2>/dev/null
    exit 1
fi

# Mostrar URLs
echo -e "\n6. 🎉 URLs actualizadas:"
echo "   📊 Dashboard: http://localhost:$HTTP_PORT/dashboard.html"
echo "   🔧 Servidor API: http://localhost:$API_PORT"
echo "   🌐 Desde red: http://$(hostname -I | awk '{print $1}'):$HTTP_PORT/dashboard.html"

# Script de detención
cat > stop_fixed.sh << EOF
#!/bin/bash
echo "🛑 Deteniendo sistema reparado..."
kill $API_PID $HTTP_PID 2>/dev/null
echo "✅ Sistema detenido"
EOF
chmod +x stop_fixed.sh

echo -e "\n7. Para detener: ./stop_fixed.sh"
echo -e "\n⚠️  IMPORTANTE: Usa la nueva URL del dashboard"
echo -e "   🔄 Actualiza la página si ya la tenías abierta\n"