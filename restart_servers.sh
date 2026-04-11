#!/bin/bash
# Reiniciar todos los servidores

echo "🔄 REINICIANDO SISTEMA COMPLETO"
echo "================================"

# Matar procesos anteriores
echo "1. 🧹 Limpiando procesos anteriores..."
pkill -f "credentials_server" 2>/dev/null
pkill -f "http.server" 2>/dev/null
pkill -f "python3.*808" 2>/dev/null
sleep 2

# 2. Iniciar servidor de credenciales
echo "2. 🔐 Iniciando servidor de credenciales..."
cd /home/cuervoc/.openclaw/workspace
nohup python3 credentials_server_fixed.py 8081 > credentials.log 2>&1 &
sleep 3

# Verificar
if curl -s http://192.168.100.170:8081/status 2>/dev/null | grep -q '"status":"ok"'; then
    echo "   ✅ Servidor API iniciado en puerto 8081"
else
    echo "   ❌ Error iniciando servidor API"
    exit 1
fi

# 3. Iniciar dashboard web
echo "3. 📊 Iniciando dashboard web..."
nohup python3 -m http.server 8080 --bind 0.0.0.0 --directory . > dashboard.log 2>&1 &
sleep 2

if curl -s -I http://192.168.100.170:8080/dashboard.html 2>/dev/null | grep -q "200 OK"; then
    echo "   ✅ Dashboard iniciado en puerto 8080"
else
    echo "   ❌ Error iniciando dashboard"
    exit 1
fi

# 4. Mostrar estado
echo -e "\n4. 📡 ESTADO ACTUAL:"
echo "   Dashboard: http://192.168.100.170:8080/dashboard.html"
echo "   Servidor API: http://192.168.100.170:8081"
echo "   Logs: credentials.log, dashboard.log"

# 5. Verificar si hay tokens almacenados
echo -e "\n5. 🔍 VERIFICANDO TOKENS ALMACENADOS..."
CREDS=$(curl -s http://192.168.100.170:8081/get 2>/dev/null)
if echo "$CREDS" | grep -q '"has_github":true'; then
    PREVIEW=$(echo "$CREDS" | grep -o '"github_preview":"[^"]*"' | cut -d'"' -f4)
    echo "   ✅ Token GitHub almacenado: $PREVIEW"
else
    echo "   ❌ No hay token GitHub almacenado"
    echo "   💡 Envía uno al dashboard o genera nuevo"
fi

echo -e "\n🎯 SISTEMA REINICIADO - LISTO PARA USAR"
echo "🚀 Para ejecutar todo: bash final_execute.sh TU_TOKEN_GITHUB"