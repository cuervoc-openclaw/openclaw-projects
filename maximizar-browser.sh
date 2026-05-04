#!/bin/bash
echo "📈 MAXIMIZANDO OPENCLAW BROWSER"
echo "==============================="

# Encontrar y maximizar todas las ventanas de Chromium
WINDOWS=$(docker exec openclaw-browser xdotool search --name "Chromium" 2>/dev/null)

if [ -z "$WINDOWS" ]; then
    echo "❌ No se encontraron ventanas de Chromium"
    echo "💡 Buscando por clase..."
    WINDOWS=$(docker exec openclaw-browser xdotool search --class "chromium" 2>/dev/null)
fi

if [ -z "$WINDOWS" ]; then
    echo "❌ No hay ventanas visibles"
    echo "🔄 Abriendo Chromium nuevo..."
    docker exec -d openclaw-browser bash -c "DISPLAY=:1 chromium --start-maximized --no-sandbox https://github.com/openclaw/openclaw"
    sleep 3
    WINDOWS=$(docker exec openclaw-browser xdotool search --name "Chromium" 2>/dev/null)
fi

echo "🔍 Ventanas encontradas:"
for WINDOW_ID in $WINDOWS; do
    echo "   📊 Ventana ID: $WINDOW_ID"
    
    # Maximizar
    docker exec openclaw-browser xdotool windowsize $WINDOW_ID 100% 100% 2>/dev/null
    docker exec openclaw-browser xdotool windowmove $WINDOW_ID 0 0 2>/dev/null
    
    # Activar
    docker exec openclaw-browser xdotool windowactivate $WINDOW_ID 2>/dev/null
    docker exec openclaw-browser xdotool windowfocus $WINDOW_ID 2>/dev/null
    
    echo "   ✅ Maximizada y activada"
done

echo ""
echo "🎉 ¡VENTANAS MAXIMIZADAS!"
echo "========================"
echo "👀 Ahora en http://localhost:3000 deberías ver:"
echo "   • Chromium en pantalla completa"
echo "   • Si no, refresca la página"
echo ""
echo "🛑 PARA NO MINIMIZAR DE NUEVO:"
echo "   • NO uses el botón [-] de la ventana"
echo "   • Usa F11 para pantalla completa"
echo "   • O deja que yo lo controle"