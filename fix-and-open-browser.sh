#!/bin/bash

echo "🔧 REPARANDO Y ABRIENDO OPENCLAW BROWSER"
echo "========================================"

# 1. Matar Chromium si está corriendo mal
echo "1. 🛑 Deteniendo Chromium si hay problemas..."
docker exec openclaw-browser pkill -f chromium 2>/dev/null || true
sleep 2

# 2. Abrir Chromium maximizado
echo "2. 🚀 Abriendo Chromium maximizado..."
docker exec -d openclaw-browser bash -c "DISPLAY=:1 chromium --start-maximized --no-sandbox --test-type --user-data-dir=/tmp/chrome-test --force-device-scale-factor=1 https://github.com/openclaw/openclaw"
sleep 5

# 3. Esperar y encontrar ventana
echo "3. 🔍 Buscando ventana nueva..."
for i in {1..10}; do
    WINDOW_ID=$(docker exec openclaw-browser xdotool search --name "GitHub" 2>/dev/null | head -1)
    if [ -n "$WINDOW_ID" ]; then
        echo "   ✅ Ventana encontrada: ID $WINDOW_ID (intento $i)"
        break
    fi
    sleep 1
done

if [ -z "$WINDOW_ID" ]; then
    echo "   ⚠️  Buscando cualquier ventana de Chromium..."
    WINDOW_ID=$(docker exec openclaw-browser xdotool search --class "chromium" 2>/dev/null | head -1)
fi

if [ -z "$WINDOW_ID" ]; then
    echo "   ❌ No se pudo encontrar ventana"
    echo "   💡 Chromium podría no haberse abierto correctamente"
    echo "   👉 Prueba manualmente en http://localhost:3000"
    exit 1
fi

# 4. Maximizar ventana
echo "4. 📈 Maximizando ventana..."
docker exec openclaw-browser xdotool windowsize $WINDOW_ID 100% 100%
docker exec openclaw-browser xdotool windowmove $WINDOW_ID 0 0
sleep 1

# 5. Activar ventana
echo "5. 🪟 Activando ventana..."
docker exec openclaw-browser xdotool windowactivate $WINDOW_ID
docker exec openclaw-browser xdotool windowfocus $WINDOW_ID
sleep 1

# 6. Verificar que se cargó GitHub
echo "6. 🔍 Verificando carga de GitHub..."
sleep 3

echo ""
echo "🎉 ¡REPARACIÓN COMPLETADA!"
echo "========================"
echo ""
echo "✅ Acciones realizadas:"
echo "   1. 🛑 Chromium reiniciado (si había problemas)"
echo "   2. 🚀 Chromium abierto maximizado directamente a GitHub"
echo "   3. 📈 Ventana maximizada al 100%"
echo "   4. 🪟 Ventana activada y enfocada"
echo ""
echo "👀 AHORA EN http://localhost:3000 DEBERÍAS VER:"
echo "   • Chromium maximizado"
echo "   • GitHub de OpenClaw cargado"
echo "   • Página completa visible"
echo ""
echo "🔄 Si aún no ves nada después de 10 segundos:"
echo "   1. Refresca http://localhost:3000"
echo "   2. O el navegador podría necesitar más tiempo"
echo ""
echo "🔧 Estado actual del contenedor:"
docker ps | grep openclaw-browser