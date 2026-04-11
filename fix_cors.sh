#!/bin/bash
echo "🔧 Reparando CORS y conexión del dashboard"
echo "=========================================="

# Obtener IP del servidor
SERVER_IP=$(hostname -I | awk '{print $1}')
echo "IP del servidor: $SERVER_IP"

# 1. Detener servidores anteriores
echo "1. Deteniendo servidores anteriores..."
pkill -f "credentials_server.py" 2>/dev/null
pkill -f "http.server" 2>/dev/null
sleep 2

# 2. Actualizar dashboard para usar IP en lugar de localhost
echo "2. Actualizando dashboard..."
sed -i "s/localhost:8081/$SERVER_IP:8081/g" dashboard.html
sed -i "s/'http:\\/\\/localhost:8081'/'http:\\/\\/$SERVER_IP:8081'/g" dashboard.html
sed -i "s/\"http:\\/\\/localhost:8081\"/\"http:\\/\\/$SERVER_IP:8081\"/g" dashboard.html

# 3. Actualizar read_credentials.py
echo "3. Actualizando cliente Python..."
sed -i "s/localhost:8081/$SERVER_IP:8081/g" read_credentials.py
sed -i "s/'http:\\/\\/localhost:8081'/'http:\\/\\/$SERVER_IP:8081'/g" read_credentials.py

# 4. Iniciar servidor API (escuchando en todas las interfaces)
echo "4. Iniciando servidor API en $SERVER_IP:8081..."
python3 credentials_server.py 8081 > api_server.log 2>&1 &
API_PID=$!
sleep 3

# Verificar
if ss -tuln 2>/dev/null | grep -q ":8081 "; then
    echo "   ✅ Servidor API iniciado (PID: $API_PID)"
    echo "   📍 Escuchando en: 0.0.0.0:8081"
else
    echo "   ❌ Error iniciando API"
    cat api_server.log
    exit 1
fi

# 5. Iniciar dashboard HTTP
echo "5. Iniciando dashboard en $SERVER_IP:8080..."
python3 -m http.server 8080 --bind 0.0.0.0 --directory . > http_server.log 2>&1 &
HTTP_PID=$!
sleep 2

if ss -tuln 2>/dev/null | grep -q ":8080 "; then
    echo "   ✅ Dashboard iniciado (PID: $HTTP_PID)"
    echo "   📍 Escuchando en: 0.0.0.0:8080"
else
    echo "   ❌ Error iniciando dashboard"
    cat http_server.log
    kill $API_PID 2>/dev/null
    exit 1
fi

# 6. Agregar headers CORS al servidor Python
echo "6. Configurando CORS..."
cat > cors_patch.py << 'EOF'
import sys
sys.path.insert(0, '.')

# Parchear el handler para agregar headers CORS
import credentials_server

original_send = credentials_server.CredentialsHandler._send_response

def patched_send(self, code, data):
    self.send_response(code)
    self.send_header('Content-Type', 'application/json')
    self.send_header('Access-Control-Allow-Origin', '*')
    self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    self.end_headers()
    self.wfile.write(json.dumps(data).encode('utf-8'))

credentials_server.CredentialsHandler._send_response = patched_send

# Agregar handler OPTIONS para CORS preflight
original_do_OPTIONS = credentials_server.CredentialsHandler.do_OPTIONS if hasattr(credentials_server.CredentialsHandler, 'do_OPTIONS') else None

def do_OPTIONS(self):
    self.send_response(200)
    self.send_header('Access-Control-Allow-Origin', '*')
    self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    self.end_headers()

credentials_server.CredentialsHandler.do_OPTIONS = do_OPTIONS

print("✅ CORS configurado")
EOF

python3 cors_patch.py

# 7. Mostrar URLs finales
echo -e "\n7. 🎉 URLs CORREGIDAS:"
echo "   📊 Dashboard: http://$SERVER_IP:8080/dashboard.html"
echo "   🔧 Servidor API: http://$SERVER_IP:8081"
echo "   🔄 El dashboard ahora se conectará correctamente"

# 8. Script de detención
cat > stop_cors.sh << EOF
#!/bin/bash
echo "🛑 Deteniendo sistema con CORS..."
kill $API_PID $HTTP_PID 2>/dev/null
echo "✅ Sistema detenido"
EOF
chmod +x stop_cors.sh

echo -e "\n8. Para detener: ./stop_cors.sh"
echo -e "\n⚠️  IMPORTANTE:"
echo "   • Usa la NUEVA URL: http://$SERVER_IP:8080/dashboard.html"
echo "   • Actualiza la página (Ctrl+F5) si ya la tenías abierta"
echo "   • El error 'ERR_CONNECTION_REFUSED' debería desaparecer"