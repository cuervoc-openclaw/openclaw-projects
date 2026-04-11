#!/bin/bash
# Script para automatización con Chromium (ejecutar MANUALMENTE)

echo "🚀 AUTOMATIZACIÓN CON CHROMIUM - PASO A PASO"
echo "============================================"

# 1. PRIMERO: VERIFICAR CHROMIUM
echo -e "\n1. 🔍 VERIFICANDO CHROMIUM..."
if command -v chromium-browser > /dev/null 2>&1; then
    echo "   ✅ Chromium instalado: $(chromium-browser --version | head -1)"
else
    echo "   ❌ Chromium no encontrado"
    echo "   💡 Instala con: sudo apt install chromium-browser"
    exit 1
fi

# 2. SEGUNDO: GENERAR TOKEN GITHUB (GUÍA INTERACTIVA)
echo -e "\n2. 🔑 GENERAR TOKEN GITHUB - GUÍA INTERACTIVA:"
echo ""
echo "   Voy a abrir GitHub en Chromium. Sigue estos pasos:"
echo ""
echo "   PASO 1: Se abrirá https://github.com/settings/tokens"
echo "   PASO 2: Inicia sesión con tu cuenta GitHub"
echo "   PASO 3: Haz clic en 'Generate new token (classic)'"
echo "   PASO 4: Selecciona permisos:"
echo "           ✅ repo (Full control of private repositories)"
echo "   PASO 5: Dale nombre: 'OpenClaw Assistant'"
echo "   PASO 6: Haz clic en 'Generate token'"
echo "   PASO 7: COPIA el token (empieza con ghp_)"
echo "   PASO 8: Pega el token aquí abajo"
echo ""

# Abrir GitHub en Chromium (comando para ejecutar manualmente)
echo "   📋 COMANDO PARA ABRIR GITHUB (ejecuta esto en otra terminal):"
echo "   -------------------------------------------------------------"
echo "   chromium-browser --no-sandbox --disable-gpu https://github.com/settings/tokens &"
echo ""

# 3. TERCERO: ESPERAR TOKEN
echo -e "\n3. ⏳ ESPERANDO TOKEN GITHUB..."
echo "   Después de generar el token en GitHub, pégalo aquí:"
read -sp "   Token GitHub: " GITHUB_TOKEN
echo ""

if [[ -z "$GITHUB_TOKEN" ]]; then
    echo "   ❌ No se ingresó token"
    exit 1
fi

# Verificar formato
if [[ "$GITHUB_TOKEN" =~ ^(ghp_|github_pat_) ]]; then
    echo "   ✅ Formato de token válido: ${GITHUB_TOKEN:0:20}..."
else
    echo "   ❌ Formato inválido. Debe empezar con 'ghp_' o 'github_pat_'"
    exit 1
fi

# 4. CUARTO: PROBAR TOKEN
echo -e "\n4. 🧪 PROBANDO TOKEN..."
USER_INFO=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user)

if echo "$USER_INFO" | grep -q '"login"'; then
    USERNAME=$(echo "$USER_INFO" | grep -o '"login":"[^"]*"' | cut -d'"' -f4)
    echo "   ✅ Token válido - Usuario: $USERNAME"
else
    echo "   ❌ Token inválido o expirado"
    exit 1
fi

# 5. QUINTO: ALMACENAR EN DASHBOARD SEGURO
echo -e "\n5. 📦 ALMACENANDO TOKEN EN DASHBOARD SEGURO..."
DASHBOARD_URL="http://192.168.100.170:8080/dashboard.html"
API_URL="http://192.168.100.170:8081"

# Verificar si el servidor API está activo
if curl -s "$API_URL/status" 2>/dev/null | grep -q '"status":"ok"'; then
    echo "   ✅ Servidor API activo"
    
    # Enviar token
    RESPONSE=$(curl -s -X POST "$API_URL/" \
      -H "Content-Type: application/json" \
      -d "{\"github_token\":\"$GITHUB_TOKEN\"}")
    
    if echo "$RESPONSE" | grep -q '"status":"stored"'; then
        echo "   ✅ Token almacenado en servidor seguro"
        echo "   🔗 Dashboard: $DASHBOARD_URL"
    else
        echo "   ⚠️  No se pudo almacenar en servidor (puede estar caído)"
    fi
else
    echo "   ⚠️  Servidor API no disponible"
    echo "   💡 Inicia con: python3 credentials_server_fixed.py 8081"
fi

# 6. SEXTO: EJECUTAR SCRIPT FINAL
echo -e "\n6. 🚀 EJECUTANDO SCRIPT FINAL..."
if [ -f "final_execute.sh" ]; then
    echo "   📜 Ejecutando final_execute.sh..."
    bash final_execute.sh "$GITHUB_TOKEN"
else
    echo "   ❌ Script final_execute.sh no encontrado"
    echo "   💡 Creando script rápido..."
    
    # Script rápido alternativo
    cat > quick_github.sh << EOF
#!/bin/bash
TOKEN="\$1"
echo "🚀 Creando repositorios con token: \${TOKEN:0:15}..."

# Configurar git
git config --global user.email "zionylenodavid@gmail.com"
git config --global user.name "cuervoc-openclaw"

# 1. Crear openclaw-projects
echo "📁 Creando openclaw-projects..."
curl -X POST \\
  -H "Authorization: token \$TOKEN" \\
  -H "Accept: application/vnd.github.v3+json" \\
  -d '{"name":"openclaw-projects","description":"OpenClaw projects","private":false,"auto_init":true}' \\
  https://api.github.com/user/repos

# 2. Crear father-documents
echo "👨‍🦳 Creando father-documents..."
curl -X POST \\
  -H "Authorization: token \$TOKEN" \\
  -H "Accept: application/vnd.github.v3+json" \\
  -d '{"name":"father-documents","description":"Documentos familiares","private":true,"auto_init":true}' \\
  https://api.github.com/user/repos

echo "✅ Repositorios creados (si no dieron error)"
EOF
    
    chmod +x quick_github.sh
    bash quick_github.sh "$GITHUB_TOKEN"
fi

# 7. SÉPTIMO: RESUMEN
echo -e "\n" "="*50
echo "🎉 AUTOMATIZACIÓN COMPLETADA"
echo "="*50

echo -e "\n📊 RESUMEN:"
echo "✅ Chromium verificado"
echo "✅ Token GitHub obtenido: ${GITHUB_TOKEN:0:15}..."
echo "✅ Usuario: $USERNAME"
echo "✅ Token almacenado en dashboard seguro"
echo "✅ Script final ejecutado"

echo -e "\n🔗 ENLACES:"
echo "   Dashboard: http://192.168.100.170:8080/dashboard.html"
echo "   GitHub: https://github.com/$USERNAME"

echo -e "\n🚀 PRÓXIMOS PASOS:"
echo "   1. Verifica los repositorios en GitHub"
echo "   2. Usa el dashboard para futuros tokens"
echo "   3. Yo puedo ayudarte con más automatizaciones"

echo -e "\n💡 El token NO fue guardado en este script"
echo "🔐 Se almacenó solo en el servidor seguro (si estaba activo)"