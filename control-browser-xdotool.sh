#!/bin/bash

echo "🎮 CONTROLANDO OPENCLAW BROWSER VIA XDOTOOL"
echo "=========================================="

# 1. Encontrar la ventana de Chromium
echo "1. 🔍 Buscando ventana de Chromium..."
WINDOW_ID=$(docker exec openclaw-browser xdotool search --name "Chromium" 2>/dev/null | head -1)

if [ -z "$WINDOW_ID" ]; then
    echo "   ❌ No se encontró ventana de Chromium"
    echo "   💡 Intentando buscar por clase..."
    WINDOW_ID=$(docker exec openclaw-browser xdotool search --class "chromium" 2>/dev/null | head -1)
fi

if [ -z "$WINDOW_ID" ]; then
    echo "   ❌ No se puede encontrar Chromium"
    echo "   ℹ️  El navegador podría estar minimizado o no tener ventana"
    exit 1
fi

echo "   ✅ Ventana encontrada: ID $WINDOW_ID"

# 2. Activar la ventana
echo "2. 🪟 Activando ventana..."
docker exec openclaw-browser xdotool windowactivate $WINDOW_ID
sleep 1

# 3. Ir a la barra de direcciones (Ctrl+L)
echo "3. 🔗 Yendo a barra de direcciones (Ctrl+L)..."
docker exec openclaw-browser xdotool key --window $WINDOW_ID ctrl+l
sleep 1

# 4. Escribir URL de GitHub
echo "4. 🐙 Escribiendo URL de GitHub..."
docker exec openclaw-browser xdotool type --window $WINDOW_ID "https://github.com/openclaw/openclaw"
sleep 1

# 5. Presionar Enter
echo "5. ⏎ Presionando Enter..."
docker exec openclaw-browser xdotool key --window $WINDOW_ID Return

echo ""
echo "🎉 ¡COMANDOS ENVIADOS!"
echo "====================="
echo ""
echo "👀 Ahora en http://localhost:3000 deberías ver:"
echo "   1. Barra de direcciones activada"
echo "   2. URL de GitHub escrita"
echo "   3. GitHub cargándose"
echo ""
echo "⏳ Espera 5-10 segundos para que cargue..."
echo ""
echo "🔧 Si no funciona, prueba manualmente en http://localhost:3000:"
echo "   1. Haz clic en la pantalla"
echo "   2. Presiona Ctrl+L"
echo "   3. Escribe: https://github.com/openclaw/openclaw"
echo "   4. Presiona Enter"