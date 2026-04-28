#!/bin/bash
# Script para instalar Coolify
# Ejecutar con: sudo bash instalar-coolify.sh

echo "🚀 INSTALADOR DE COOLIFY"
echo "========================"
echo ""
echo "Este script instalará Coolify en tu servidor."
echo "Coolify es un panel de control para gestionar servidores y aplicaciones."
echo ""
echo "📋 REQUISITOS:"
echo "• Ubuntu/Debian (recomendado)"
echo "• 2GB RAM mínimo"
echo "• Docker instalado"
echo "• Puerto 8000 disponible"
echo ""
echo "📊 TU SISTEMA:"
echo "• SO: $(lsb_release -ds 2>/dev/null || cat /etc/os-release | grep PRETTY_NAME | cut -d= -f2 | tr -d '\"')"
echo "• Kernel: $(uname -r)"
echo "• Memoria: $(free -h | awk '/^Mem:/ {print $2}')"
echo "• Docker: $(docker --version 2>/dev/null || echo 'No instalado')"
echo ""
echo "⚠️  ADVERTENCIA:"
echo "• Esta instalación modificará configuraciones del sistema"
echo "• Se instalarán contenedores Docker"
echo "• Se abrirá el puerto 8000"
echo ""
read -p "¿Continuar con la instalación? (s/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo "❌ Instalación cancelada"
    exit 1
fi

echo "🔄 INICIANDO INSTALACIÓN..."
echo ""

# Descargar script oficial
echo "📥 Descargando instalador oficial..."
curl -fsSL https://cdn.coollabs.io/coolify/install.sh -o /tmp/install-coolify.sh
chmod +x /tmp/install-coolify.sh

echo "📦 Ejecutando instalador..."
echo "⚠️  Esto puede tomar varios minutos..."
echo ""

# Ejecutar instalador
/tmp/install-coolify.sh

echo ""
echo "🔍 VERIFICANDO INSTALACIÓN..."
sleep 10

# Verificar contenedores
echo ""
echo "📊 CONTENEDORES DOCKER:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -i coolify || echo "No se encontraron contenedores de Coolify"

# Obtener IP del servidor
IP=$(hostname -I | awk '{print $1}')
echo ""
echo "🌐 ACCESO A COOLIFY:"
echo "   URL: http://$IP:8000"
echo "   Usuario: admin@coolify.local"
echo "   Contraseña: password"
echo ""
echo "🔧 CONFIGURACIÓN INICIAL RECOMENDADA:"
echo "   1. Acceder a http://$IP:8000"
echo "   2. Cambiar contraseña del admin"
echo "   3. Configurar dominio (opcional)"
echo "   4. Agregar servidores/proyectos"
echo ""
echo "📝 COMANDOS ÚTILES:"
echo "   • Ver logs: docker logs coolify"
echo "   • Reiniciar: docker restart coolify"
echo "   • Detener: docker stop coolify"
echo "   • Iniciar: docker start coolify"
echo ""
echo "✅ INSTALACIÓN COMPLETADA"
echo "📋 Guarda esta información para acceder a Coolify"