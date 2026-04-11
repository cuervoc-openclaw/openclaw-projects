#!/bin/bash
# CONFIGURACIÓN PERMANENTE CON SSH KEYS

echo "🔐 CONFIGURANDO ACCESO PERMANENTE A GITHUB"
echo "=========================================="

# 1. VERIFICAR/CREAR CLAVE SSH
echo -e "\n1. 🔑 GENERANDO CLAVE SSH..."
SSH_KEY_PATH="$HOME/.ssh/github_openclaw"

if [ ! -f "$SSH_KEY_PATH" ]; then
    echo "   Creando nueva clave SSH Ed25519..."
    ssh-keygen -t ed25519 \
        -C "zionylenodavid@gmail.com" \
        -f "$SSH_KEY_PATH" \
        -N ""  # Sin passphrase para automatización
    
    if [ $? -eq 0 ]; then
        echo "   ✅ Clave SSH generada: $SSH_KEY_PATH"
    else
        echo "   ❌ Error generando clave SSH"
        exit 1
    fi
else
    echo "   ✅ Clave SSH ya existe: $SSH_KEY_PATH"
fi

# 2. MOSTRAR CLAVE PÚBLICA
echo -e "\n2. 📋 CLAVE PÚBLICA (copia esto en GitHub):"
echo "   ==========================================="
cat "$SSH_KEY_PATH.pub"
echo "   ==========================================="

# 3. CONFIGURAR GIT PARA SSH
echo -e "\n3. ⚙️ CONFIGURANDO GIT..."
git config --global user.email "zionylenodavid@gmail.com"
git config --global user.name "cuervoc-openclaw"
git config --global url."git@github.com:".insteadOf "https://github.com/"

echo "   ✅ Git configurado para usar SSH"

# 4. AGREGAR AL SSH AGENT
echo -e "\n4. 🤖 CONFIGURANDO SSH AGENT..."
eval "$(ssh-agent -s)" > /dev/null 2>&1
ssh-add "$SSH_KEY_PATH" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "   ✅ Clave agregada al SSH agent"
else
    echo "   ⚠️ No se pudo agregar al SSH agent (puede requerir intervención)"
fi

# 5. INSTRUCCIONES PARA GITHUB
echo -e "\n5. 📝 INSTRUCCIONES PARA GITHUB:"
echo "   ================================="
echo "   1. Ve a: https://github.com/settings/keys"
echo "   2. Haz clic en 'New SSH key'"
echo "   3. Título: 'OpenClaw Server'"
echo "   4. Pega la clave pública mostrada arriba"
echo "   5. Haz clic en 'Add SSH key'"
echo ""
echo "   💡 La clave SSH NUNCA expira (hasta que la borres)"
echo "   🔒 Más seguro que tokens, ideal para automatización"

# 6. PROBAR CONEXIÓN (opcional)
echo -e "\n6. 🧪 PROBAR CONEXIÓN SSH:"
read -p "   ¿Tu username de GitHub? " GITHUB_USER

if [ -n "$GITHUB_USER" ]; then
    echo "   Probando conexión a GitHub..."
    ssh -T git@github.com 2>&1 | grep -i "successfully authenticated"
    
    if [ $? -eq 0 ]; then
        echo "   ✅ Conexión SSH exitosa!"
    else
        echo "   ⚠️ Configura la clave en GitHub primero"
    fi
fi

# 7. CREAR SCRIPT PARA USAR SSH
echo -e "\n7. 🚀 CREANDO SCRIPT PARA GITHUB CON SSH:"
cat > github_ssh_execute.sh << 'EOF'
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
EOF

chmod +x github_ssh_execute.sh
echo "   ✅ Script creado: github_ssh_execute.sh"

echo -e "\n🎯 RESUMEN:"
echo "   SSH Key: $SSH_KEY_PATH"
echo "   Email: zionylenodavid@gmail.com"
echo "   User: cuervoc-openclaw"
echo "   Acceso: PERMANENTE (sin expiración)"

echo -e "\n🚀 PARA COMPLETAR:"
echo "   1. Agrega la clave SSH a GitHub"
echo "   2. Luego ejecuta: bash github_ssh_execute.sh TU_USERNAME"