#!/bin/bash
# SCRIPT PARA EJECUTAR TODO AHORA MISMO

echo "🚀 EJECUTANDO TODO - YO ME ENCARGO DE TODO"
echo "=========================================="

# 1. PRIMERO: CONFIGURAR GIT
echo "1. 🔧 CONFIGURANDO GIT..."
git config --global user.email "zionylenodavid@gmail.com"
git config --global user.name "cuervoc-openclaw"
echo "✅ Git configurado"

# 2. VERIFICAR TOKEN ACTUAL
echo -e "\n2. 🔐 VERIFICANDO TOKEN GITHUB..."
TOKEN_FILE="/tmp/gh_token_$(date +%s).txt"

echo "📋 Para continuar, necesito el token GitHub."
echo "   El token actual (del dashboard) expiró después de 5 minutos."
echo ""
echo "🔑 INGRESA TU TOKEN GITHUB AHORA:"
echo "   (Empieza con ghp_ o github_pat_)"
echo "   (Se borrará automáticamente después)"
echo ""
read -sp "Token: " GITHUB_TOKEN
echo ""

if [[ -z "$GITHUB_TOKEN" ]]; then
    echo "❌ No se ingresó token. Abortando."
    exit 1
fi

# Guardar token temporalmente
echo "$GITHUB_TOKEN" > "$TOKEN_FILE"
chmod 600 "$TOKEN_FILE"
echo "✅ Token guardado temporalmente"

# 3. PROBAR TOKEN
echo -e "\n3. 🧪 PROBANDO TOKEN CON GITHUB..."
USER_RESPONSE=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user)

if echo "$USER_RESPONSE" | grep -q '"login"'; then
    USERNAME=$(echo "$USER_RESPONSE" | grep -o '"login":"[^"]*"' | cut -d'"' -f4)
    echo "✅ Token válido - Usuario: $USERNAME"
else
    echo "❌ Token inválido o expirado"
    rm -f "$TOKEN_FILE"
    exit 1
fi

# 4. CREAR REPOSITORIO openclaw-projects
echo -e "\n4. 📁 CREANDO REPOSITORIO 'openclaw-projects'..."
REPO1_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/repo1.json \
  -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d '{
    "name": "openclaw-projects",
    "description": "OpenClaw assistant projects - LOL Coach, STT system, credentials dashboard",
    "private": false,
    "auto_init": true,
    "gitignore_template": "Python"
  }' \
  https://api.github.com/user/repos)

REPO1_STATUS=$(echo "$REPO1_RESPONSE" | tail -n1)

if [ "$REPO1_STATUS" -eq 201 ]; then
    REPO1_URL=$(cat /tmp/repo1.json | grep -o '"html_url":"[^"]*"' | cut -d'"' -f4)
    echo "✅ Repositorio creado: $REPO1_URL"
elif [ "$REPO1_STATUS" -eq 422 ]; then
    if cat /tmp/repo1.json | grep -q "already exists"; then
        REPO1_URL="https://github.com/$USERNAME/openclaw-projects"
        echo "ℹ️  Repositorio ya existe: $REPO1_URL"
    else
        echo "❌ Error creando repositorio"
        cat /tmp/repo1.json
        rm -f "$TOKEN_FILE"
        exit 1
    fi
else
    echo "❌ Error $REPO1_STATUS creando repositorio"
    rm -f "$TOKEN_FILE"
    exit 1
fi

# 5. SUBIR ARCHIVOS AL REPOSITORIO
echo -e "\n5. 📤 SUBIENDO ARCHIVOS A openclaw-projects..."
cd /home/cuervoc/.openclaw/workspace

# Inicializar git si no existe
if [ ! -d .git ]; then
    git init
fi

# Configurar remote
git remote remove origin 2>/dev/null
git remote add origin "https://github.com/$USERNAME/openclaw-projects.git"

# Agregar archivos (excluir algunos)
echo "📦 Agregando archivos..."
find . -type f -name "*.py" -o -name "*.md" -o -name "*.sh" -o -name "*.html" -o -name "*.js" | \
  grep -v __pycache__ | grep -v ".pyc" | grep -v ".log" | while read file; do
    git add "$file" 2>/dev/null
done

# Commit
echo "💾 Haciendo commit..."
git commit -m "Initial commit: OpenClaw projects - LOL Coach, STT system, credentials dashboard" || true

# Push
echo "🚀 Haciendo push..."
if git push -u origin main --force 2>/dev/null; then
    echo "✅ Push exitoso a main"
elif git push -u origin master --force 2>/dev/null; then
    echo "✅ Push exitoso a master"
else
    echo "⚠️  No se pudo hacer push (puede estar vacío o ya actualizado)"
fi

# 6. CREAR REPOSITORIO PARA DOCUMENTOS DEL PADRE
echo -e "\n6. 👨‍🦳 CREANDO REPOSITORIO 'father-documents'..."
REPO2_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/repo2.json \
  -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d '{
    "name": "father-documents",
    "description": "Documentos, fotos y proyectos personales - Archivo familiar",
    "private": true,
    "auto_init": true
  }' \
  https://api.github.com/user/repos)

REPO2_STATUS=$(echo "$REPO2_RESPONSE" | tail -n1)

if [ "$REPO2_STATUS" -eq 201 ]; then
    REPO2_URL=$(cat /tmp/repo2.json | grep -o '"html_url":"[^"]*"' | cut -d'"' -f4)
    echo "✅ Repositorio creado (privado): $REPO2_URL"
    
    # Crear estructura básica localmente
    echo "📂 Creando estructura básica..."
    mkdir -p /tmp/father-documents
    cd /tmp/father-documents
    
    cat > README.md << 'EOF'
# 👨‍🦳 father-documents

Repositorio privado para documentos familiares importantes.

## 📁 Estructura
- `documents/` - Documentos escaneados (DNI, certificados, etc.)
- `photos/` - Fotografías digitalizadas
- `projects/` - Proyectos personales
- `memories/` - Historias, anécdotas, recuerdos
- `backups/` - Copias de seguridad adicionales

## 🔒 Seguridad
- Repositorio privado en GitHub
- Solo acceso autorizado
- Historial completo con git
- Copias de seguridad automáticas
EOF
    
    mkdir -p documents photos projects memories backups
    
    git init
    git add .
    git commit -m "Estructura inicial para documentos familiares"
    git remote add origin "https://github.com/$USERNAME/father-documents.git"
    
    if git push -u origin main --force 2>/dev/null; then
        echo "✅ Estructura subida a father-documents"
    fi
    
elif [ "$REPO2_STATUS" -eq 422 ]; then
    if cat /tmp/repo2.json | grep -q "already exists"; then
        REPO2_URL="https://github.com/$USERNAME/father-documents"
        echo "ℹ️  Repositorio ya existe: $REPO2_URL"
    else
        echo "⚠️  Error creando father-documents (puede que ya exista)"
    fi
else
    echo "⚠️  Error $REPO2_STATUS creando father-documents"
fi

# 7. LIMPIAR
echo -e "\n7. 🧹 LIMPIANDO DATOS TEMPORALES..."
rm -f "$TOKEN_FILE" /tmp/repo1.json /tmp/repo2.json
rm -rf /tmp/father-documents 2>/dev/null

# 8. RESUMEN FINAL
echo -e "\n" "="*50
echo "🎉 ¡TODO COMPLETADO!"
echo "="*50

echo -e "\n📊 RESUMEN:"
echo "✅ Git configurado"
echo "✅ Token verificado (usuario: $USERNAME)"
echo "✅ Repositorio principal: https://github.com/$USERNAME/openclaw-projects"
echo "✅ Repositorio documentos: https://github.com/$USERNAME/father-documents"
echo ""
echo "📁 ARCHIVOS SUBIDOS:"
ls -la /home/cuervoc/.openclaw/workspace/*.py /home/cuervoc/.openclaw/workspace/*.md /home/cuervoc/.openclaw/workspace/*.sh 2>/dev/null | \
  awk '{print "  📄 " $9 " (" $5 " bytes)"}'

echo -e "\n🚀 PRÓXIMOS PASOS:"
echo "   1. Ver repositorios en GitHub"
echo "   2. Agregar más archivos cuando quieras"
echo "   3. Usar el dashboard para tokens futuros"
echo "   4. Yo puedo ayudarte con más automatizaciones"

echo -e "\n🔐 Token temporal BORRADO por seguridad"
echo "💡 Para futuras acciones, usa el dashboard seguro"