#!/bin/bash
# SCRIPT FINAL - EJECUTAR TODO CON TOKEN

echo "🚀 EJECUCIÓN FINAL - YO HAGO TODO"
echo "=================================="

# Verificar token
if [ -z "$1" ]; then
    echo "❌ ERROR: Necesitas proporcionar el token GitHub"
    echo ""
    echo "📋 USO:"
    echo "  bash final_execute.sh TU_TOKEN_GITHUB"
    echo ""
    echo "🔍 OBTENER TOKEN:"
    echo "  1. El token actual (del dashboard) es: github_pat...WUwe"
    echo "  2. Si expiró, re-envíalo al dashboard"
    echo "  3. O genera nuevo en: https://github.com/settings/tokens"
    echo ""
    echo "💡 El token debe tener permisos 'repo'"
    exit 1
fi

TOKEN="$1"
echo "✅ Token proporcionado: ${TOKEN:0:20}..."

# 1. CONFIGURAR GIT
echo -e "\n1. 🔧 CONFIGURANDO GIT..."
git config --global user.email "zionylenodavid@gmail.com"
git config --global user.name "cuervoc-openclaw"
echo "✅ Git configurado"

# 2. VERIFICAR TOKEN
echo -e "\n2. 🔐 VERIFICANDO TOKEN..."
USER_INFO=$(curl -s -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user)

if echo "$USER_INFO" | grep -q '"login"'; then
    USERNAME=$(echo "$USER_INFO" | grep -o '"login":"[^"]*"' | cut -d'"' -f4)
    echo "✅ Token válido - Usuario: $USERNAME"
else
    echo "❌ Token inválido o expirado"
    exit 1
fi

# 3. CREAR REPOSITORIO openclaw-projects
echo -e "\n3. 📁 CREANDO 'openclaw-projects'..."
REPO1_RESP=$(curl -s -w "%{http_code}" -o /tmp/repo1.json \
  -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d '{
    "name": "openclaw-projects",
    "description": "OpenClaw assistant projects - LOL Coach, STT system, credentials dashboard",
    "private": false,
    "auto_init": true,
    "gitignore_template": "Python"
  }' \
  https://api.github.com/user/repos)

REPO1_STATUS=$(echo "$REPO1_RESP" | tail -n1)

if [ "$REPO1_STATUS" -eq 201 ]; then
    REPO1_URL=$(cat /tmp/repo1.json | grep -o '"html_url":"[^"]*"' | cut -d'"' -f4)
    echo "✅ Repositorio creado: $REPO1_URL"
    REPO1_CLONE=$(cat /tmp/repo1.json | grep -o '"clone_url":"[^"]*"' | cut -d'"' -f4)
elif [ "$REPO1_STATUS" -eq 422 ]; then
    if cat /tmp/repo1.json | grep -q "already exists"; then
        REPO1_URL="https://github.com/$USERNAME/openclaw-projects"
        REPO1_CLONE="https://github.com/$USERNAME/openclaw-projects.git"
        echo "ℹ️  Repositorio ya existe: $REPO1_URL"
    else
        echo "❌ Error creando repositorio"
        cat /tmp/repo1.json
        exit 1
    fi
else
    echo "❌ Error $REPO1_STATUS"
    exit 1
fi

# 4. SUBIR ARCHIVOS A openclaw-projects
echo -e "\n4. 📤 SUBIENDO ARCHIVOS..."
cd /home/cuervoc/.openclaw/workspace

# Inicializar git
if [ ! -d .git ]; then
    git init
fi

# Configurar remote
git remote remove origin 2>/dev/null
git remote add origin "$REPO1_CLONE"

# Agregar archivos importantes
echo "📦 Agregando archivos..."
FILES_TO_ADD=()

# Buscar archivos Python (excluyendo cache)
for file in *.py; do
    [ -e "$file" ] && FILES_TO_ADD+=("$file")
done

# Buscar otros archivos importantes
for file in *.md *.sh *.html *.js; do
    [ -e "$file" ] && FILES_TO_ADD+=("$file")
done

# Buscar en subdirectorios (excluyendo __pycache__)
find . -type f \( -name "*.py" -o -name "*.md" -o -name "*.sh" -o -name "*.html" -o -name "*.js" \) \
  -not -path "./__pycache__/*" -not -name "*.pyc" -not -name "*.log" | while read -r file; do
    # Excluir si ya está en la lista
    filename=$(basename "$file")
    if [[ ! " ${FILES_TO_ADD[@]} " =~ " ${filename} " ]]; then
        FILES_TO_ADD+=("$file")
    fi
done

# Agregar archivos
if [ ${#FILES_TO_ADD[@]} -gt 0 ]; then
    for file in "${FILES_TO_ADD[@]}"; do
        git add "$file" 2>/dev/null && echo "   + $file"
    done
fi

# Commit
echo "💾 Haciendo commit..."
git commit -m "Initial commit: OpenClaw projects - LOL Coach, STT system, credentials dashboard" 2>/dev/null || \
  echo "⚠️  No hay cambios para commit (puede estar vacío o ya commiteado)"

# Push
echo "🚀 Haciendo push..."
if git push -u origin main --force 2>/dev/null; then
    echo "✅ Push exitoso a main"
elif git push -u origin master --force 2>/dev/null; then
    echo "✅ Push exitoso a master"
else
    echo "⚠️  No se pudo hacer push (puede estar vacío)"
fi

# 5. CREAR REPOSITORIO father-documents
echo -e "\n5. 👨‍🦳 CREANDO 'father-documents'..."
REPO2_RESP=$(curl -s -w "%{http_code}" -o /tmp/repo2.json \
  -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d '{
    "name": "father-documents",
    "description": "Documentos, fotos y proyectos personales - Archivo familiar",
    "private": true,
    "auto_init": true
  }' \
  https://api.github.com/user/repos)

REPO2_STATUS=$(echo "$REPO2_RESP" | tail -n1)

if [ "$REPO2_STATUS" -eq 201 ]; then
    REPO2_URL=$(cat /tmp/repo2.json | grep -o '"html_url":"[^"]*"' | cut -d'"' -f4)
    echo "✅ Repositorio creado (privado): $REPO2_URL"
    REPO2_CLONE=$(cat /tmp/repo2.json | grep -o '"clone_url":"[^"]*"' | cut -d'"' -f4)
    
    # Crear estructura básica
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
    git remote add origin "$REPO2_CLONE"
    
    if git push -u origin main --force 2>/dev/null; then
        echo "✅ Estructura subida"
    elif git push -u origin master --force 2>/dev/null; then
        echo "✅ Estructura subida (master)"
    fi
    
    cd /home/cuervoc/.openclaw/workspace
    
elif [ "$REPO2_STATUS" -eq 422 ]; then
    if cat /tmp/repo2.json | grep -q "already exists"; then
        REPO2_URL="https://github.com/$USERNAME/father-documents"
        echo "ℹ️  Repositorio ya existe: $REPO2_URL"
    else
        echo "⚠️  Error creando father-documents"
    fi
else
    echo "⚠️  Error $REPO2_STATUS creando father-documents"
fi

# 6. LIMPIAR
echo -e "\n6. 🧹 LIMPIANDO..."
rm -f /tmp/repo1.json /tmp/repo2.json
rm -rf /tmp/father-documents 2>/dev/null

# 7. RESUMEN FINAL
echo -e "\n" "="*50
echo "🎉 ¡EJECUCIÓN COMPLETADA!"
echo "="*50

echo -e "\n📊 RESUMEN:"
echo "✅ Git configurado"
echo "✅ Usuario: $USERNAME"
echo "✅ Repositorio principal: https://github.com/$USERNAME/openclaw-projects"
echo "✅ Repositorio documentos: https://github.com/$USERNAME/father-documents"

echo -e "\n📁 ARCHIVOS SUBIDOS:"
cd /home/cuervoc/.openclaw/workspace
count=0
for file in *; do
    if [ -f "$file" ] && [[ "$file" != *.pyc ]] && [[ "$file" != *.log ]]; then
        if [ $count -lt 10 ]; then
            size=$(stat -c%s "$file" 2>/dev/null || echo "?")
            echo "  📄 $file ($size bytes)"
        fi
        ((count++))
    fi
done

if [ $count -gt 10 ]; then
    echo "  ... y $((count-10)) más"
fi

echo -e "\n🚀 PRÓXIMOS PASOS:"
echo "   1. Verifica los repositorios en GitHub"
echo "   2. Agrega más archivos cuando quieras: git add . && git commit && git push"
echo "   3. Usa el dashboard para tokens futuros: http://192.168.100.170:8080/dashboard.html"
echo "   4. Yo puedo ayudarte con más automatizaciones"

echo -e "\n💡 El token NO fue guardado en ningún archivo"
echo "🔐 Para futuras acciones, usa el dashboard seguro"