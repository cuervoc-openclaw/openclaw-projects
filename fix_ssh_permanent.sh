#!/bin/bash
# SOLUCIÓN DEFINITIVA PARA SSH

echo "🔧 SOLUCIÓN SSH PERMANENTE"
echo "=========================="

# 1. INICIAR SSH AGENT PERSISTENTE
echo -e "\n1. 🚀 INICIANDO SSH AGENT PERSISTENTE..."
# Matar agentes anteriores
pkill ssh-agent 2>/dev/null

# Iniciar nuevo agent con persistencia
eval "$(ssh-agent -s -t 3600)"  # 1 hora de timeout

if [ -n "$SSH_AGENT_PID" ]; then
    echo "   ✅ SSH Agent iniciado (PID: $SSH_AGENT_PID, timeout: 3600s)"
else
    echo "   ❌ No se pudo iniciar SSH Agent"
    exit 1
fi

# 2. AGREGAR CLAVE CON VERBOSE
echo -e "\n2. 🔑 AGREGANDO CLAVE SSH..."
ssh-add -v ~/.ssh/github_openclaw

if [ $? -eq 0 ]; then
    echo "   ✅ Clave SSH agregada exitosamente"
else
    echo "   ❌ Error agregando clave SSH"
    echo "   💡 Verifica permisos: chmod 600 ~/.ssh/github_openclaw"
    exit 1
fi

# 3. VERIFICAR CLAVES DISPONIBLES
echo -e "\n3. 📋 CLAVES EN SSH AGENT:"
ssh-add -l

# 4. PROBAR CONEXIÓN DETALLADA
echo -e "\n4. 🧪 PROBANDO CONEXIÓN GITHUB (verbose)..."
ssh -vT git@github.com 2>&1 | tail -20

# 5. PROBAR CON COMANDO ESPECÍFICO
echo -e "\n5. 🔍 PROBANDO CON CLAVE ESPECÍFICA..."
ssh -i ~/.ssh/github_openclaw -T git@github.com 2>&1 | grep -i "success\|authenticated\|denied"

# 6. CONFIGURAR GIT PARA USAR CLAVE ESPECÍFICA
echo -e "\n6. ⚙️ CONFIGURANDO GIT CON CLAVE ESPECÍFICA..."
git config --global core.sshCommand "ssh -i ~/.ssh/github_openclaw -o IdentitiesOnly=yes"

echo "   ✅ Git configurado para usar clave específica"

# 7. PROBAR PUSH SIMULADO
echo -e "\n7. 🧪 PROBANDO PUSH SIMULADO..."
cd /tmp
rm -rf test_repo 2>/dev/null
mkdir test_repo && cd test_repo
git init
echo "# Test" > README.md
git add .
git commit -m "Test"
git remote add origin git@github.com:cuervoc-openclaw/openclaw-projects.git 2>/dev/null

echo "   Intentando push de prueba..."
GIT_SSH_COMMAND="ssh -i ~/.ssh/github_openclaw -v" git push -u origin main --force 2>&1 | tail -10

# 8. VERIFICAR CLAVE EN GITHUB
echo -e "\n8. 🔐 VERIFICACIÓN FINAL:"
echo "   La clave pública DEBE estar en: https://github.com/settings/keys"
echo ""
echo "   CLAVE PÚBLICA ACTUAL:"
cat ~/.ssh/github_openclaw.pub
echo ""
echo "   💡 Si no está agregada, cópiala y pégalas en GitHub"

# 9. CREAR SCRIPT DE RECUPERACIÓN
echo -e "\n9. 📜 CREANDO SCRIPT DE RECUPERACIÓN..."
cat > ~/.ssh/restore_ssh.sh << 'EOF'
#!/bin/bash
# Restaurar SSH agent
pkill ssh-agent 2>/dev/null
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/github_openclaw
ssh -T git@github.com
EOF

chmod +x ~/.ssh/restore_ssh.sh
echo "   ✅ Script creado: ~/.ssh/restore_ssh.sh"

echo -e "\n🎯 RESUMEN:"
echo "   Si sigue fallando, verifica:"
echo "   1. Clave agregada en GitHub Settings → SSH Keys"
echo "   2. La clave pública coincide EXACTAMENTE"
echo "   3. El repositorio existe: openclaw-projects"
echo ""
echo "   Comando rápido para probar:"
echo "   GIT_SSH_COMMAND=\"ssh -i ~/.ssh/github_openclaw\" git push"