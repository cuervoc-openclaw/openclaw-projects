#!/bin/bash

echo "🎮 CONTROL ROBUSTO DE OPENCLAW BROWSER"
echo "======================================"

# 1. Encontrar ventana de Chromium
echo "1. 🔍 Buscando ventana de Chromium..."
WINDOW_ID=$(docker exec openclaw-browser xdotool search --name "Chromium" 2>/dev/null | head -1)

if [ -z "$WINDOW_ID" ]; then
    echo "   ⚠️  No se encontró por nombre, buscando por clase..."
    WINDOW_ID=$(docker exec openclaw-browser xdotool search --class "chromium" 2>/dev/null | head -1)
fi

if [ -z "$WINDOW_ID" ]; then
    echo "   ⚠️  No se encontró Chromium, buscando cualquier ventana..."
    WINDOW_ID=$(docker exec openclaw-browser xdotool search --onlyvisible "." 2>/dev/null | head -1)
fi

if [ -z "$WINDOW_ID" ]; then
    echo "   ❌ No se puede encontrar ninguna ventana"
    echo "   💡 El navegador podría estar minimizado o cerrado"
    echo "   🛠️  Intentando abrir Chromium desde cero..."
    docker exec openclaw-browser bash -c "DISPLAY=:1 chromium --start-maximized --no-sandbox --test-type --user-data-dir=/tmp/chrome-test &" &
    sleep 5
    WINDOW_ID=$(docker exec openclaw-browser xdotool search --name "Chromium" 2>/dev/null | head -1)
fi

if [ -z "$WINDOW_ID" ]; then
    echo "   ❌ No se pudo controlar el navegador"
    echo "   👉 Prueba manualmente en http://localhost:3000"
    exit 1
fi

echo "   ✅ Ventana encontrada: ID $WINDOW_ID"

# 2. Obtener tamaño de la ventana
echo "2. 📏 Obteniendo tamaño de ventana..."
WINDOW_GEOM=$(docker exec openclaw-browser xdotool getwindowgeometry $WINDOW_ID 2>/dev/null)
echo "   📐 Geometría: $WINDOW_GEOM"

# 3. Hacer clic en el centro de la ventana (para activar)
echo "3. 🖱️ Haciendo clic en el centro de la ventana..."
docker exec openclaw-browser xdotool mousemove --window $WINDOW_ID 500 300
docker exec openclaw-browser xdotool click 1
sleep 1

# 4. Ir a barra de direcciones (Ctrl+L)
echo "4. 🔗 Activando barra de direcciones (Ctrl+L)..."
docker exec openclaw-browser xdotool key --window $WINDOW_ID ctrl+l
sleep 1

# 5. Limpiar barra de direcciones (si hay algo)
echo "5. 🧹 Limpiando barra de direcciones..."
docker exec openclaw-browser xdotool key --window $WINDOW_ID ctrl+a
docker exec openclaw-browser xdotool key --window $WINDOW_ID Delete
sleep 0.5

# 6. Escribir URL de GitHub
echo "6. 🐙 Escribiendo URL de GitHub..."
docker exec openclaw-browser xdotool type --window $WINDOW_ID --delay 100 "https://github.com/openclaw/openclaw"
sleep 1

# 7. Presionar Enter
echo "7. ⏎ Presionando Enter..."
docker exec openclaw-browser xdotool key --window $WINDOW_ID Return

echo ""
echo "🎉 ¡CONTROL COMPLETADO!"
echo "======================"
echo ""
echo "📋 Resumen de acciones:"
echo "   1. ✅ Ventana encontrada y activada"
echo "   2. ✅ Clic en centro de ventana"
echo "   3. ✅ Barra de direcciones activada (Ctrl+L)"
echo "   4. ✅ Barra limpiada (Ctrl+A + Delete)"
echo "   5. ✅ URL escrita: https://github.com/openclaw/openclaw"
echo "   6. ✅ Enter presionado"
echo ""
echo "👀 EN http://localhost:3000 DEBERÍAS VER AHORA:"
echo "   • GitHub de OpenClaw cargándose"
echo "   • Página principal de OpenClaw en GitHub"
echo ""
echo "⏳ Espera 5-10 segundos para que cargue completamente..."
echo ""
echo "🔄 Si no ves cambios después de 10 segundos:"
echo "   1. Refresca la página http://localhost:3000"
echo "   2. O prueba MANUALMENTE:"
echo "      - Haz clic en la pantalla"
echo "      - Presiona Ctrl+L"
echo "      - Escribe: https://github.com/openclaw/openclaw"
echo "      - Presiona Enter"
echo ""
echo "🔧 Para más control:"
echo "   - Puedes usar el teclado/mouse desde http://localhost:3000"
echo "   - Es como un escritorio remoto completo"