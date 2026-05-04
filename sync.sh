#!/bin/bash
# Convenience script to stage and commit context files
cd "$(dirname "$0")"

FILES=(
  .gitignore AGENTS.md SOUL.md USER.md TOOLS.md IDENTITY.md MEMORY.md
  HEARTBEAT.md
  memory/*.md
  proyectos/*/README.md
  docs/*.md
  skills/*/SKILL.md
  README_DETAILED.md CREDENTIALS_SYSTEM.md UPDATE_README.md
)

for f in "${FILES[@]}"; do
  [ -f "$f" ] && git add "$f"
done

git commit -m "auto: sync workspace context" && git push origin master
