#!/bin/bash
echo "🚀 Iniciando Sistema Simple de Credenciales"
echo "=========================================="

# Matar procesos en puertos 8080 y 8081 si existen
echo "1. Limpiando puertos anteriores..."
pkill -f "http.server 8080" 2>/dev/null
pkill -f "credentials_server.py" 2>/dev/null
sleep 2

# Verificar si los puertos están libres
check_port() {
    ss -tuln 2>/dev/null | grep ":$1 " > /dev/null
    return $?
}

# Usar puertos alternativos si los originales están ocupados
PORT_HTTP=8080
PORT_API=8081

if check_port $PORT_HTTP; then
    echo "⚠️  Puerto $PORT_HTTP ocupado, usando 8082"
    PORT_HTTP=8082
fi

if check_port $PORT_API; then
    echo "⚠️  Puerto $PORT_API ocupado, usando 8083"
    PORT_API=8083
fi

# 2. Iniciar servidor de credenciales
echo -e "\n2. Iniciando servidor de credenciales en puerto $PORT_API..."
python3 credentials_server.py $PORT_API > credentials_server.log 2>&1 &
SERVER_PID=$!
sleep 3

if check_port $PORT_API; then
    echo "✅ Servidor iniciado (PID: $SERVER_PID, Puerto: $PORT_API)"
else
    echo "❌ Error iniciando servidor"
    cat credentials_server.log
    exit 1
fi

# 3. Iniciar servidor web
echo -e "\n3. Iniciando dashboard web en puerto $PORT_HTTP..."
python3 -m http.server $PORT_HTTP --directory . > http_server.log 2>&1 &
HTTP_PID=$!
sleep 2

if check_port $PORT_HTTP; then
    echo "✅ Dashboard iniciado (PID: $HTTP_PID, Puerto: $PORT_HTTP)"
else
    echo "❌ Error iniciando dashboard"
    cat http_server.log
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

# 4. Actualizar dashboard con puertos correctos
echo -e "\n4. Configurando dashboard..."
sed -i "s/localhost:8081/localhost:$PORT_API/g" dashboard.html 2>/dev/null
sed -i "s/8081/$PORT_API/g" read_credentials.py 2>/dev/null

# 5. Mostrar URLs
echo -e "\n5. URLs de acceso:"
echo "   📊 Dashboard: http://localhost:$PORT_HTTP/dashboard.html"
echo "   🔧 Servidor API: http://localhost:$PORT_API"
echo "   🌐 Desde red: http://$(hostname -I | awk '{print $1}'):$PORT_HTTP/dashboard.html"

# 6. Script de detención
cat > stop_simple.sh << EOF
#!/bin/bash
echo "🛑 Deteniendo sistema..."
kill $SERVER_PID $HTTP_PID 2>/dev/null
echo "✅ Sistema detenido"
EOF
chmod +x stop_simple.sh

echo -e "\n6. Para detener: ./stop_simple.sh"
echo -e "\n🎉 ¡Sistema listo! Abre el dashboard en tu navegador."