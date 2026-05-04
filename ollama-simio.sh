#!/bin/bash
# 🐒 SCRIPT PARA SIMIO - OLLAMA GRATIS
# Para tareas simples y ahorrar tokens

echo "🔪 CUCHILLO GRATIS ACTIVADO"
echo "==========================="

# Configuración
OLLAMA_URL="http://localhost:11435"
MODEL="tinyllama"

# Función para preguntar a Ollama
preguntar_ollama() {
    local pregunta="$1"
    echo "🤔 Pregunta: $pregunta"
    echo ""
    
    curl -s "$OLLAMA_URL/api/generate" -d "{
        \"model\": \"$MODEL\",
        \"prompt\": \"$pregunta\",
        \"stream\": false,
        \"options\": {
            \"temperature\": 0.7,
            \"max_tokens\": 100
        }
    }" | jq -r '.response'
}

# Función para procesar texto
procesar_texto() {
    local texto="$1"
    local accion="$2"
    
    case $accion in
        "resumir")
            preguntar_ollama "Resume este texto en 3 puntos: $texto"
            ;;
        "traducir")
            preguntar_ollama "Traduce al español: $texto"
            ;;
        "corregir")
            preguntar_ollama "Corrige la gramática de: $texto"
            ;;
        *)
            preguntar_ollama "$accion: $texto"
            ;;
    esac
}

# Menú principal
echo ""
echo "🍌 ¿QUÉ QUIERES HACER?"
echo "1. Hacer una pregunta simple"
echo "2. Resumir texto"
echo "3. Traducir texto"
echo "4. Corregir gramática"
echo "5. Probar conexión"
echo "6. Salir"
echo ""

read -p "Elige una opción (1-6): " opcion

case $opcion in
    1)
        read -p "📝 Tu pregunta: " pregunta
        preguntar_ollama "$pregunta"
        ;;
    2)
        read -p "📄 Texto a resumir: " texto
        procesar_texto "$texto" "resumir"
        ;;
    3)
        read -p "🌍 Texto a traducir: " texto
        procesar_texto "$texto" "traducir"
        ;;
    4)
        read -p "✏️ Texto a corregir: " texto
        procesar_texto "$texto" "corregir"
        ;;
    5)
        echo "🔍 Probando conexión a Ollama..."
        curl -s "$OLLAMA_URL/api/version"
        echo ""
        echo "📦 Modelos disponibles:"
        curl -s "$OLLAMA_URL/api/tags" | jq -r '.models[].name'
        ;;
    6)
        echo "👋 ¡Hasta luego, Simio!"
        ;;
    *)
        echo "❌ Opción no válida"
        ;;
esac

echo ""
echo "🎯 Recuerda: Esto es GRATIS, no gasta tokens"
echo "💰 Ahorras dinero usando Ollama para tonterías"