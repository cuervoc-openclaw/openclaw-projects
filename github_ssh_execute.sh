#!/bin/bash
# Script para GitHub usando SSH (sin tokens que expiran)

echo "🚀 GITHUB CON SSH - ACCESO PERMANENTE"
echo "====================================="

# Configurar repositorio remoto
REPO_NAME="openclaw-projects"
GITHUB_USER="$1"

if [ -z "$GITHUB_USER" ]; then
    echo "❌ Necesitas proporcionar tu username de GitHub"
    echo "   Uso: bash github_ssh_execute.sh TU_USERNAME"
    exit 1
fi

echo "📁 Creando repositorio: $REPO_NAME"

# Crear repositorio vía API (necesita token temporal o web)
echo "💡 Para crear repositorio, necesitas:"
echo "   1. Token temporal (solo para crear)"
echo "   2. O crearlo manualmente en GitHub.com"
echo ""
echo "🎯 LUEGO PUEDES USAR SSH PARA SIEMPRE:"
echo "   git remote add origin git@github.com:$GITHUB_USER/$REPO_NAME.git"
echo "   git add . && git commit -m 'Initial commit'"
echo "   git push -u origin main"

echo -e "\n🔐 CON SSH:"
echo "   - Sin tokens que expiran"
echo "   - Acceso permanente"
echo "   - Más seguro"
