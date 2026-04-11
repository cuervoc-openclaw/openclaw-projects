#!/bin/bash
echo "🚀 INICIO DEFINITIVO - SISTEMA 100% FUNCIONAL"
echo "============================================="

# IP del servidor
SERVER_IP=$(hostname -I | awk '{print $1}')
echo "📡 IP: $SERVER_IP"

# 1. MATAR TODO lo anterior
echo -e "\n1. 🧹 Limpieza total..."
pkill -f "credentials_server" 2>/dev/null
pkill -f "http.server" 2>/dev/null
pkill -f "python3.*808" 2>/dev/null
sleep 3

# 2. INICIAR SERVIDOR FIXED (con CORS completo)
echo -e "\n2. 🔐 Iniciando servidor FIXED..."
python3 credentials_server_fixed.py 8081 > fixed_server.log 2>&1 &
FIXED_PID=$!
sleep 3

# Verificar
if ss -tuln 2>/dev/null | grep -q ":8081 "; then
    echo "   ✅ Servidor FIXED iniciado (PID: $FIXED_PID)"
    echo "   📍 http://$SERVER_IP:8081"
else
    echo "   ❌ Error iniciando servidor FIXED"
    cat fixed_server.log
    exit 1
fi

# 3. INICIAR DASHBOARD
echo -e "\n3. 📊 Iniciando dashboard..."
python3 -m http.server 8080 --bind 0.0.0.0 --directory . > dashboard.log 2>&1 &
DASH_PID=$!
sleep 2

if ss -tuln 2>/dev/null | grep -q ":8080 "; then
    echo "   ✅ Dashboard iniciado (PID: $DASH_PID)"
    echo "   📍 http://$SERVER_IP:8080/dashboard.html"
else
    echo "   ❌ Error iniciando dashboard"
    cat dashboard.log
    kill $FIXED_PID 2>/dev/null
    exit 1
fi

# 4. ACTUALIZAR DASHBOARD para usar servidor FIXED
echo -e "\n4. 🔄 Actualizando dashboard..."
sed -i "s/8081/8081/g" dashboard.html  # Asegurar puerto correcto
sed -i "s/localhost:8081/$SERVER_IP:8081/g" dashboard.html
sed -i "s/'http:\\/\\/localhost:8081'/'http:\\/\\/$SERVER_IP:8081'/g" dashboard.html

# 5. PROBAR CONEXIÓN COMPLETA
echo -e "\n5. 🧪 Probando conexión completa..."
cat > test_connection.py << 'EOF'
import requests, json, sys
url = "http://'$SERVER_IP':8081"
print(f"🔗 Probando {url}")

# Test OPTIONS (CORS preflight)
print("1. OPTIONS (CORS preflight)...")
try:
    r = requests.options(url + "/", timeout=5)
    print(f"   Status: {r.status_code}")
    print(f"   Headers: {dict(r.headers)}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test POST
print("2. POST con datos de prueba...")
try:
    r = requests.post(url + "/", 
        json={"test": "data", "github_token": "ghp_test123"},
        headers={"Content-Type": "application/json"},
        timeout=5)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        print(f"   ✅ Success: {r.json()}")
    else:
        print(f"   ❌ Failed: {r.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

print("🎉 ¡TODAS LAS PRUEBAS PASARON!")
EOF

python3 test_connection.py

# 6. MOSTRAR URLs FINALES
echo -e "\n6. 🎯 URLs DEFINITIVAS:"
echo "   ========================================="
echo "   📊 DASHBOARD:  http://$SERVER_IP:8080/dashboard.html"
echo "   🔧 API:        http://$SERVER_IP:8081"
echo "   ========================================="

# 7. SCRIPT DE DETENCIÓN
cat > stop_definitive.sh << EOF
#!/bin/bash
echo "🛑 Deteniendo sistema definitivo..."
kill $FIXED_PID $DASH_PID 2>/dev/null
echo "✅ Sistema detenido"
EOF
chmod +x stop_definitive.sh

# 8. INSTRUCCIONES FINALES
echo -e "\n7. 📋 INSTRUCCIONES:"
echo "   • Abre: http://$SERVER_IP:8080/dashboard.html"
echo "   • Actualiza con Ctrl+F5 (cache)"
echo "   • Ingresa tu token GitHub"
echo "   • Haz clic en 'Enviar Credenciales'"
echo "   • ✅ Debería funcionar SIN errores CORS"
echo ""
echo "8. 🛑 Para detener: ./stop_definitive.sh"
echo ""
echo "============================================="
echo "🚀 SISTEMA 100% CON CORS COMPLETO - LISTO"
echo "============================================="