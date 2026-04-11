#!/bin/bash
# ARREGLAR SSH AGENT Y VERIFICAR CONEXIÓN GITHUB

echo "🔧 ARREGLANDO SSH AGENT PARA GITHUB"
echo "==================================="

# 1. INICIAR SSH AGENT
echo -e "\n1. 🚀 INICIANDO SSH AGENT..."
eval "$(ssh-agent -s)" > /dev/null 2>&1

if [ -n "$SSH_AGENT_PID" ]; then
    echo "   ✅ SSH Agent iniciado (PID: $SSH_AGENT_PID)"
else
    echo "   ❌ No se pudo iniciar SSH Agent"
    exit 1
fi

# 2. AGREGAR CLAVE SSH
echo -e "\n2. 🔑 AGREGANDO CLAVE SSH..."
SSH_KEY="$HOME/.ssh/github_openclaw"

if [ -f "$SSH_KEY" ]; then
    ssh-add "$SSH_KEY" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "   ✅ Clave SSH agregada: $SSH_KEY"
    else
        echo "   ❌ No se pudo agregar clave SSH"
        echo "   💡 Intenta manualmente: ssh-add $SSH_KEY"
    fi
else
    echo "   ❌ Clave SSH no encontrada: $SSH_KEY"
    exit 1
fi

# 3. VERIFICAR CLAVES DISPONIBLES
echo -e "\n3. 📋 CLAVES SSH DISPONIBLES:"
ssh-add -l

# 4. PROBAR CONEXIÓN A GITHUB
echo -e "\n4. 🧪 PROBANDO CONEXIÓN GITHUB..."
echo "   Esto puede tomar unos segundos..."

# Probar con timeout
timeout 10 ssh -T git@github.com 2>&1 | tee /tmp/github_test.txt

RESULT=$?
GITHUB_OUTPUT=$(cat /tmp/github_test.txt)

echo -e "\n5. 📊 RESULTADO:"

if echo "$GITHUB_OUTPUT" | grep -qi "successfully authenticated"; then
    echo "   ✅ ¡CONEXIÓN SSH EXITOSA!"
    echo "   $GITHUB_OUTPUT"
    
    # Extraer username
    USERNAME=$(echo "$GITHUB_OUTPUT" | grep -o "Hi [^!]*" | cut -d' ' -f2)
    echo "   👤 Usuario GitHub: $USERNAME"
    
elif [ $RESULT -eq 124 ]; then
    echo "   ⏱️ Timeout - GitHub no respondió"
    echo "   💡 Verifica conexión a internet"
    
elif echo "$GITHUB_OUTPUT" | grep -qi "Permission denied"; then
    echo "   ❌ PERMISSION DENIED"
    echo "   Posibles causas:"
    echo "   1. Clave SSH no agregada a GitHub"
    echo "   2. Clave incorrecta en GitHub"
    echo "   3. Problema de permisos en clave"
    
    echo -e "\n   🔍 VERIFICAR CLAVE PÚBLICA:"
    echo "   La clave que agregaste a GitHub debe ser:"
    cat "$SSH_KEY.pub"
    
else
    echo "   ❌ Error desconocido:"
    echo "   $GITHUB_OUTPUT"
fi

# 6. VERIFICAR CONFIGURACIÓN GIT
echo -e "\n6. ⚙️ VERIFICANDO CONFIGURACIÓN GIT:"
git config --global --get url.git@github.com:.insteadof

if [ $? -eq 0 ]; then
    echo "   ✅ Git configurado para usar SSH"
else
    echo "   ⚠️ Git NO configurado para SSH"
    echo "   💡 Configura con:"
    echo "   git config --global url.\"git@github.com:\".insteadOf \"https://github.com/\""
fi

# 7. RESUMEN Y PRÓXIMOS PASOS
echo -e "\n7. 🎯 PRÓXIMOS PASOS:"

if echo "$GITHUB_OUTPUT" | grep -qi "successfully authenticated"; then
    echo "   ✅ ¡TODO LISTO! Puedes ejecutar:"
    echo "   cd /home/cuervoc/.openclaw/workspace"
    echo "   bash github_ssh_execute.sh $USERNAME"
else
    echo "   🔧 Para arreglar:"
    echo "   1. Asegúrate de haber agregado la clave SSH correcta a GitHub"
    echo "   2. La clave pública debe ser EXACTAMENTE:"
    cat "$SSH_KEY.pub"
    echo ""
    echo "   3. Verifica en: https://github.com/settings/keys"
    echo "   4. Luego ejecuta este script nuevamente"
fi

echo -e "\n💡 Si sigue fallando, podemos usar token temporal como alternativa"