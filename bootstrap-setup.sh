#!/bin/bash
# bootstrap-setup.sh — Configura OpenClaw desde el workspace repo
# Ejecutar después de clonar: bash bootstrap-setup.sh

set -e

echo "=== OpenClaw Bootstrap ==="

# 1. Verificar que estamos en el workspace correcto
if [ ! -f "SOUL.md" ] || [ ! -f "USER.md" ]; then
  echo "ERROR: Ejecuta este script desde la raíz del workspace (openclaw-projects)"
  exit 1
fi

echo "✓ Workspace detectado"

# 2. Enlazar SOUL, USER, AGENTS, TOOLS, MEMORY
mkdir -p ~/.openclaw/workspace
ln -sf "$PWD/SOUL.md" ~/.openclaw/workspace/SOUL.md 2>/dev/null || true
ln -sf "$PWD/USER.md" ~/.openclaw/workspace/USER.md 2>/dev/null || true
ln -sf "$PWD/AGENTS.md" ~/.openclaw/workspace/AGENTS.md 2>/dev/null || true
ln -sf "$PWD/TOOLS.md" ~/.openclaw/workspace/TOOLS.md 2>/dev/null || true
ln -sf "$PWD/IDENTITY.md" ~/.openclaw/workspace/IDENTITY.md 2>/dev/null || true
ln -sf "$PWD/MEMORY.md" ~/.openclaw/workspace/MEMORY.md 2>/dev/null || true
ln -sf "$PWD/HEARTBEAT.md" ~/.openclaw/workspace/HEARTBEAT.md 2>/dev/null || true

# 3. Enlazar skills
mkdir -p ~/.openclaw/workspace/skills
for skill in skills/*/; do
  if [ -d "$skill" ]; then
    name=$(basename "$skill")
    ln -sf "$PWD/$skill" ~/.openclaw/workspace/skills/"$name" 2>/dev/null || true
    echo "  skill: $name"
  fi
done

# 4. Restaurar memoria
mkdir -p ~/.openclaw/workspace/memory
cp -n memory/*.md ~/.openclaw/workspace/memory/ 2>/dev/null || true
echo "✓ Memoria restaurada"

echo ""
echo "=== Bootstrap completo ==="
echo "OpenClaw debería estar listo. Corre: openclaw gateway restart"
