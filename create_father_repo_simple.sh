#!/bin/bash
# Script para crear repositorio GitHub para documentos del padre
# Ejecutar: bash create_father_repo_simple.sh

echo "👨‍🦳 CREANDO REPOSITORIO PARA DOCUMENTOS DEL PADRE"
echo "=================================================="

# Verificar si se proporcionó token
if [ -z "$1" ]; then
    echo "❌ ERROR: Necesitas proporcionar tu token GitHub"
    echo ""
    echo "📋 USO:"
    echo "  bash create_father_repo_simple.sh TU_TOKEN_GITHUB"
    echo ""
    echo "🔍 OBTENER TOKEN:"
    echo "  1. Ve a https://github.com/settings/tokens"
    echo "  2. Crea nuevo token con permisos 'repo'"
    echo "  3. Copia el token (empieza con ghp_)"
    echo ""
    echo "💡 TU TOKEN ACTUAL (preview): github_pat...WUwe"
    echo "   (Está guardado en el dashboard seguro)"
    exit 1
fi

TOKEN="$1"
REPO_NAME="father-documents"
USERNAME="cuervoc-openclaw"

echo "✅ Token proporcionado: ${TOKEN:0:15}..."
echo "📁 Repositorio: $REPO_NAME"
echo "👤 Usuario: $USERNAME"
echo ""

# 1. Verificar autenticación
echo "1. 🔐 Verificando autenticación con GitHub..."
curl -s -H "Authorization: token $TOKEN" \
     -H "Accept: application/vnd.github.v3+json" \
     https://api.github.com/user | grep -q '"login"' 

if [ $? -eq 0 ]; then
    echo "   ✅ Autenticación exitosa"
else
    echo "   ❌ Error de autenticación - Token inválido"
    exit 1
fi

# 2. Crear repositorio
echo "2. 📁 Creando repositorio '$REPO_NAME'..."
RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/github_response.json \
  -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d '{
    "name": "'"$REPO_NAME"'",
    "description": "Documentos, fotos y proyectos personales - Archivo familiar",
    "private": true,
    "auto_init": true,
    "has_issues": false,
    "has_projects": false,
    "has_wiki": false
  }' \
  https://api.github.com/user/repos)

STATUS_CODE=$(echo "$RESPONSE" | tail -n1)

if [ "$STATUS_CODE" -eq 201 ]; then
    echo "   ✅ ¡Repositorio creado exitosamente!"
    
    # Mostrar información del repo
    REPO_URL=$(cat /tmp/github_response.json | grep -o '"html_url":"[^"]*"' | cut -d'"' -f4)
    CLONE_URL=$(cat /tmp/github_response.json | grep -o '"clone_url":"[^"]*"' | cut -d'"' -f4)
    
    echo "   🔗 URL: $REPO_URL"
    echo "   📋 Clone: $CLONE_URL"
    
elif [ "$STATUS_CODE" -eq 422 ]; then
    ERROR_MSG=$(cat /tmp/github_response.json | grep -o '"message":"[^"]*"' | cut -d'"' -f4)
    if [[ "$ERROR_MSG" == *"already exists"* ]]; then
        echo "   ℹ️  El repositorio ya existe"
        REPO_URL="https://github.com/$USERNAME/$REPO_NAME"
        CLONE_URL="https://github.com/$USERNAME/$REPO_NAME.git"
        echo "   🔗 URL: $REPO_URL"
    else
        echo "   ❌ Error 422: $ERROR_MSG"
        exit 1
    fi
else
    echo "   ❌ Error $STATUS_CODE creando repositorio"
    cat /tmp/github_response.json
    exit 1
fi

# 3. Instrucciones para configurar
echo ""
echo "3. 🚀 CONFIGURACIÓN LOCAL:"
echo "   # Clonar repositorio"
echo "   cd /home/cuervoc"
echo "   git clone $CLONE_URL"
echo ""
echo "   # Crear estructura organizada"
echo "   cd $REPO_NAME"
echo "   mkdir -p documents photos projects memories backups"
echo ""
echo "   # Crear README básico (si no se creó automáticamente)"
echo "   cat > README.md << 'EOF'"
echo "# 👨‍🦳 Archivo Familiar"
echo ""
echo "Repositorio privado para documentos familiares importantes."
echo ""
echo "## 📂 Estructura"
echo "- documents/ - Documentos escaneados"
echo "- photos/ - Fotografías digitalizadas"
echo "- projects/ - Proyectos personales"
echo "- memories/ - Recuerdos e historias"
echo "- backups/ - Copias de seguridad"
echo "EOF"
echo ""
echo "   # Primer commit"
echo "   git add ."
echo "   git commit -m 'Estructura inicial para documentos familiares'"
echo "   git push origin main"
echo ""
echo "4. 📝 PRÓXIMOS PASOS:"
echo "   • Escanear documentos importantes"
echo "   • Digitalizar fotografías antiguas"
echo "   • Organizar por categorías/años"
echo "   • Agregar descripciones a cada archivo"
echo ""
echo "🎉 ¡REPOSITORIO LISTO PARA USAR!"
echo ""
echo "💡 Yo puedo ayudarte a:"
echo "   • Organizar los archivos"
echo "   • Crear índices automáticos"
echo "   • Convertir formatos si es necesario"
echo "   • Hacer backups periódicos"

# Limpiar
rm -f /tmp/github_response.json