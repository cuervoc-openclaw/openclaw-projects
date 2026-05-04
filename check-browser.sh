#!/bin/bash

echo "🔍 Verificando estado de OpenClaw Browser..."
echo "=========================================="

# Verificar si Docker está corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker no está corriendo"
    echo "Inicia Docker con: sudo systemctl start docker"
    exit 1
fi
echo "✅ Docker está corriendo"

# Verificar si la imagen existe
if docker images | grep -q "coollabsio/openclaw-browser"; then
    echo "✅ Imagen OpenClaw Browser encontrada"
    IMAGE_EXISTS=true
else
    echo "⚠️  Imagen no encontrada, descargando..."
    docker pull coollabsio/openclaw-browser:latest &
    DOWNLOAD_PID=$!
    echo "📥 Descargando imagen (PID: $DOWNLOAD_PID)..."
    IMAGE_EXISTS=false
fi

# Verificar si el contenedor está corriendo
if docker ps | grep -q "openclaw-browser"; then
    echo "✅ Contenedor OpenClaw Browser corriendo"
    CONTAINER_RUNNING=true
else
    echo "⚠️  Contenedor no corriendo"
    CONTAINER_RUNNING=false
    
    # Intentar iniciar si la imagen existe
    if [ "$IMAGE_EXISTS" = true ]; then
        echo "🚀 Iniciando OpenClaw Browser..."
        docker run -d -p 3000:3000 --name openclaw-browser coollabsio/openclaw-browser:latest
        sleep 5
    fi
fi

# Verificar conexión
echo "🔗 Probando conexión..."
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ OpenClaw Browser accesible en http://localhost:3000"
    echo "🎉 ¡Listo para usar!"
    
    # Mostrar información del contenedor
    echo ""
    echo "📊 Información del contenedor:"
    docker ps | grep openclaw-browser
    
    echo ""
    echo "🚀 Comandos útiles:"
    echo "  • Ver logs: docker logs openclaw-browser"
    echo "  • Detener: docker stop openclaw-browser"
    echo "  • Eliminar: docker rm openclaw-browser"
    echo "  • Reiniciar: docker restart openclaw-browser"
    
else
    echo "❌ No se puede conectar a OpenClaw Browser"
    echo "Esperando a que la imagen se descargue..."
    
    if [ "$IMAGE_EXISTS" = false ] && [ -n "$DOWNLOAD_PID" ]; then
        echo "⏳ Esperando descarga (puede tomar varios minutos)..."
        wait $DOWNLOAD_PID
        echo "✅ Descarga completada, intentando iniciar..."
        docker run -d -p 3000:3000 --name openclaw-browser coollabsio/openclaw-browser:latest
        sleep 10
        
        if curl -s http://localhost:3000 > /dev/null 2>&1; then
            echo "✅ ¡OpenClaw Browser iniciado exitosamente!"
        else
            echo "❌ Aún no se puede conectar"
            echo "Revisa los logs: docker logs openclaw-browser"
        fi
    fi
fi

echo ""
echo "🔗 Para usar con Puppeteer/Playwright:"
echo "  WebSocket endpoint: ws://localhost:3000"
echo "  HTTP endpoint: http://localhost:3000"
echo ""
echo "🎯 Listo para integración con GitHub + Lovable"