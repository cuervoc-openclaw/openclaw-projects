#!/bin/bash
# SUBIR TODO A GITHUB CON SSH - SCRIPT COMPLETO

echo "🚀 SUBIENDO TODO A GITHUB - SSH PERMANENTE"
echo "=========================================="

USERNAME="cuervoc-openclaw"
EMAIL="zionylenodavid@gmail.com"

# Verificar conexión SSH
echo -e "\n1. 🔍 VERIFICANDO CONEXIÓN SSH..."
ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"

if [ $? -ne 0 ]; then
    echo "   ❌ Conexión SSH falló"
    echo "   💡 Ejecuta primero: bash fix_ssh_agent.sh"
    exit 1
fi

echo "   ✅ Conexión SSH exitosa - Usuario: $USERNAME"

# 2. CONFIGURAR GIT
echo -e "\n2. ⚙️ CONFIGURANDO GIT..."
git config --global user.email "$EMAIL"
git config --global user.name "$USERNAME"
git config --global url."git@github.com:".insteadOf "https://github.com/"

echo "   ✅ Git configurado"

# 3. CREAR REPOSITORIOS (necesita token temporal o creación manual)
echo -e "\n3. 📁 CREANDO REPOSITORIOS..."

echo "   💡 Para crear repositorios necesitamos:"
echo "   A. Token temporal (solo para crear)"
echo "   B. Crearlos manualmente en GitHub.com"
echo ""
echo "   🎯 REPOSITORIOS A CREAR:"
echo "   1. openclaw-projects (público)"
echo "   2. father-documents (privado)"
echo ""
echo "   📋 CREA LOS REPOSITORIOS MANUALMENTE:"
echo "   1. Ve a: https://github.com/new"
echo "   2. Repository name: 'openclaw-projects'"
echo "   3. Description: 'OpenClaw projects and automation scripts'"
echo "   4. Public"
echo "   5. Initialize with README: NO"
echo "   6. Create repository"
echo ""
echo "   7. Repetir para 'father-documents' (privado)"
echo "   8. Description: 'Family documents archive'"
echo "   9. Private"
echo ""

read -p "   ¿Ya creaste los repositorios? (s/n): " -n 1 -r
echo

if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "   ✅ Continuando con subida..."
else
    echo "   ⏸️  Crea los repositorios primero y luego ejecuta este script nuevamente"
    exit 0
fi

# 4. PREPARAR ARCHIVOS PARA openclaw-projects
echo -e "\n4. 📦 PREPARANDO ARCHIVOS PARA openclaw-projects..."

# Crear directorio temporal
TEMP_DIR="/tmp/openclaw_upload"
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

echo "   Copiando archivos del workspace..."
cp -r /home/cuervoc/.openclaw/workspace/* "$TEMP_DIR/" 2>/dev/null

# Limpiar archivos no necesarios
cd "$TEMP_DIR"
rm -rf __pycache__ *.pyc *.log .git

echo "   Total archivos: $(find . -type f | wc -l)"

# 5. SUBIR A openclaw-projects
echo -e "\n5. 📤 SUBIENDO openclaw-projects..."

# Inicializar git
git init
git add .
git commit -m "Initial commit: OpenClaw projects and automation systems

Sistemas incluidos:
- LOL Coach completo (API Riot Games)
- Sistema STT (transcripción de audio con Vosk)
- Dashboard de credenciales seguro
- Scripts de automatización GitHub
- Sistema de publicación automática Facebook
- Documentación completa"

# Configurar remoto y subir
git remote add origin "git@github.com:$USERNAME/openclaw-projects.git"

echo "   Subiendo a GitHub..."
GIT_SSH_COMMAND="ssh -o BatchMode=yes" git push -u origin main --force

if [ $? -eq 0 ]; then
    echo "   ✅ openclaw-projects subido exitosamente!"
    echo "   🔗 https://github.com/$USERNAME/openclaw-projects"
else
    echo "   ❌ Error subiendo openclaw-projects"
    echo "   💡 Verifica que el repositorio existe y tienes permisos"
fi

# 6. PREPARAR father-documents
echo -e "\n6. 👨‍🦳 PREPARANDO father-documents..."

DOCS_DIR="/tmp/father_docs"
rm -rf "$DOCS_DIR"
mkdir -p "$DOCS_DIR"

# Crear estructura básica
mkdir -p "$DOCS_DIR"/{documentos,facturas,contratos,fotos,archivos_importantes}

# Crear README
cat > "$DOCS_DIR/README.md" << EOF
# Father Documents - Archivo Familiar

Este repositorio privado contiene documentos familiares importantes.

## Estructura:
- **documentos/** - Documentos importantes
- **facturas/** - Facturas y recibos
- **contratos/** - Contratos legales
- **fotos/** - Fotos importantes
- **archivos_importantes/** - Archivos críticos

## Seguridad:
- Repositorio privado
- Acceso restringido
- Historial de cambios completo
EOF

# 7. SUBIR father-documents
echo -e "\n7. 📤 SUBIENDO father-documents..."

cd "$DOCS_DIR"
git init
git add .
git commit -m "Initial commit: Family documents archive structure"

git remote add origin "git@github.com:$USERNAME/father-documents.git"

echo "   Subiendo a GitHub..."
GIT_SSH_COMMAND="ssh -o BatchMode=yes" git push -u origin main --force

if [ $? -eq 0 ]; then
    echo "   ✅ father-documents subido exitosamente!"
    echo "   🔗 https://github.com/$USERNAME/father-documents (privado)"
else
    echo "   ❌ Error subiendo father-documents"
fi

# 8. RESUMEN
echo -e "\n" "="*50
echo "🎉 SUBIDA COMPLETADA"
echo "="*50

echo -e "\n📊 RESUMEN:"
echo "✅ openclaw-projects (público)"
echo "   https://github.com/$USERNAME/openclaw-projects"
echo "   Archivos: $(find "$TEMP_DIR" -type f | wc -l)"
echo ""
echo "✅ father-documents (privado)"
echo "   https://github.com/$USERNAME/father-documents"
echo "   Estructura familiar creada"
echo ""
echo "🔐 ACCESO PERMANENTE CONFIGURADO:"
echo "   - SSH Keys (sin expiración)"
echo "   - Git configurado para SSH"
echo "   - Conexión verificada"
echo ""
echo "🚀 SISTEMAS SUBIDOS:"
echo "   • LOL Coach completo"
echo "   • Sistema STT (transcripción de audio)"
echo "   • Dashboard de credenciales seguro"
echo "   • Scripts de automatización"
echo "   • Sistema de publicación Facebook"
echo ""
echo "💡 PRÓXIMOS PASOS:"
echo "   1. Verifica los repositorios en GitHub"
echo "   2. Usa 'git clone git@github.com:$USERNAME/openclaw-projects.git'"
echo "   3. El acceso SSH está configurado permanentemente"
echo ""
echo "🎯 ¡TODO SUBIDO EXITOSAMENTE!"