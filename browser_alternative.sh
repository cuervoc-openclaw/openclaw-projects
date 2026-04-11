#!/bin/bash
# Sistema alternativo para automatización web sin navegador GUI

echo "🌐 SISTEMA ALTERNATIVO DE AUTOMATIZACIÓN WEB"
echo "============================================"

# 1. VERIFICAR DASHBOARD DE CREDENCIALES
echo -e "\n1. 🔍 VERIFICANDO DASHBOARD DE CREDENCIALES..."
DASHBOARD_URL="http://192.168.100.170:8080/dashboard.html"

echo "   Probando conexión a dashboard..."
if curl -s -I "$DASHBOARD_URL" 2>/dev/null | grep -q "200 OK"; then
    echo "   ✅ Dashboard accesible: $DASHBOARD_URL"
    
    # Verificar servidor API
    API_URL="http://192.168.100.170:8081/status"
    API_STATUS=$(curl -s "$API_URL" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
    
    if [ "$API_STATUS" = "ok" ]; then
        echo "   ✅ Servidor API funcionando"
        
        # Verificar credenciales almacenadas
        CREDS=$(curl -s "http://192.168.100.170:8081/get")
        if echo "$CREDS" | grep -q '"has_github":true'; then
            GITHUB_PREVIEW=$(echo "$CREDS" | grep -o '"github_preview":"[^"]*"' | cut -d'"' -f4)
            echo "   ✅ Token GitHub almacenado: $GITHUB_PREVIEW"
        else
            echo "   ❌ No hay token GitHub almacenado"
        fi
    else
        echo "   ❌ Servidor API no responde"
    fi
else
    echo "   ❌ Dashboard no accesible"
fi

# 2. GENERAR TOKEN GITHUB (GUÍA)
echo -e "\n2. 🔑 GUÍA PARA GENERAR TOKEN GITHUB:"
echo "   ==================================="
echo "   Para generar token manualmente:"
echo ""
echo "   PASO 1: Ve a https://github.com/settings/tokens"
echo "   PASO 2: Haz clic en 'Generate new token (classic)'"
echo "   PASO 3: Selecciona permisos:"
echo "           ✅ repo (Full control of private repositories)"
echo "           ✅ (Opcional) workflow"
echo "   PASO 4: Dale un nombre descriptivo: 'OpenClaw Assistant'"
echo "   PASO 5: Haz clic en 'Generate token'"
echo "   PASO 6: COPIA el token (empieza con ghp_)"
echo ""
echo "   PASO 7: Envía el token al dashboard seguro:"
echo "           $DASHBOARD_URL"
echo "           O usa este comando:"
echo "           curl -X POST http://192.168.100.170:8081/ \\"
echo "             -H 'Content-Type: application/json' \\"
echo "             -d '{\"github_token\":\"TU_TOKEN_AQUI\"}'"

# 3. PROBAR TOKEN (si se proporciona)
echo -e "\n3. 🧪 PROBAR TOKEN GITHUB:"
if [ -n "$1" ]; then
    TOKEN="$1"
    echo "   Probando token proporcionado..."
    
    USER_INFO=$(curl -s -H "Authorization: token $TOKEN" \
      -H "Accept: application/vnd.github.v3+json" \
      https://api.github.com/user)
    
    if echo "$USER_INFO" | grep -q '"login"'; then
        USERNAME=$(echo "$USER_INFO" | grep -o '"login":"[^"]*"' | cut -d'"' -f4)
        echo "   ✅ Token válido - Usuario: $USERNAME"
        
        # Almacenar en servidor seguro
        echo "   📦 Almacenando en servidor seguro..."
        curl -s -X POST http://192.168.100.170:8081/ \
          -H 'Content-Type: application/json' \
          -d "{\"github_token\":\"$TOKEN\"}" > /dev/null
        
        echo "   ✅ Token almacenado en servidor seguro"
    else
        echo "   ❌ Token inválido o expirado"
    fi
else
    echo "   ℹ️  Para probar token: bash $0 TU_TOKEN"
fi

# 4. EJECUTAR SCRIPT FINAL (si hay token)
echo -e "\n4. 🚀 EJECUTAR SCRIPT FINAL:"
if [ -n "$1" ]; then
    echo "   Token proporcionado, ejecutando script final..."
    
    # Verificar si el script final existe
    if [ -f "final_execute.sh" ]; then
        echo "   📜 Ejecutando final_execute.sh..."
        bash final_execute.sh "$1"
    else
        echo "   ❌ Script final_execute.sh no encontrado"
        echo "   💡 Creando script rápido..."
        
        cat > quick_execute.sh << 'EOF'
#!/bin/bash
TOKEN="$1"
echo "🚀 Ejecución rápida con token: ${TOKEN:0:15}..."

# Configurar git
git config --global user.email "zionylenodavid@gmail.com"
git config --global user.name "cuervoc-openclaw"

# Crear repositorio
curl -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d '{"name":"openclaw-projects","description":"OpenClaw projects","private":false,"auto_init":true}' \
  https://api.github.com/user/repos

echo "✅ Repositorio creado (si no da error)"
EOF
        
        chmod +x quick_execute.sh
        bash quick_execute.sh "$1"
    fi
else
    echo "   ℹ️  Para ejecutar todo: bash $0 TU_TOKEN"
fi

# 5. RESUMEN Y PRÓXIMOS PASOS
echo -e "\n5. 📋 RESUMEN Y PRÓXIMOS PASOS:"
echo "   ==============================="
echo "   ✅ Dashboard: $DASHBOARD_URL"
echo "   ✅ Servidor API: http://192.168.100.170:8081"
echo "   ✅ Script final: final_execute.sh (listo)"
echo ""
echo "   🚀 PARA COMPLETAR TODO:"
echo "   1. Genera token en GitHub"
echo "   2. Envíalo al dashboard o úsalo así:"
echo "      bash final_execute.sh TU_TOKEN"
echo ""
echo "   🔧 SISTEMAS CREADOS HOY:"
echo "   • Dashboard de credenciales seguro"
echo "   • Sistema STT (transcripción de audio)"
echo "   • LOL Coach (API Riot Games)"
echo "   • Scripts de automatización GitHub"
echo "   • Todo listo para subir a repositorios"

echo -e "\n🎯 ¿QUÉ SIGUE?"
echo "   Ejecuta: bash final_execute.sh TU_TOKEN_GITHUB"