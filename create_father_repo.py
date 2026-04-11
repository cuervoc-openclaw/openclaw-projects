#!/usr/bin/env python3
"""
Crear repositorio para documentos del padre
"""

import requests
import json
import sys
import os

def create_repository_for_father():
    """Crear repositorio especial"""
    print("👨‍🦳 CREANDO REPOSITORIO PARA DOCUMENTOS DEL PADRE")
    print("=" * 60)
    
    # Información del repositorio
    repo_config = {
        'name': 'father-documents',  # Puedes cambiarlo
        'description': 'Documentos, fotos y proyectos personales - Archivo familiar',
        'private': True,  # RECOMENDADO: privado para documentos personales
        'auto_init': True,  # Crear con README inicial
        'has_issues': False,  # No necesitamos issues
        'has_projects': False,  # No necesitamos projects
        'has_wiki': False,  # No necesitamos wiki
        'is_template': False
    }
    
    print("📋 Configuración del repositorio:")
    print(f"   Nombre: {repo_config['name']}")
    print(f"   Descripción: {repo_config['description']}")
    print(f"   Privado: {'✅ Sí (recomendado)' if repo_config['private'] else '❌ No'}")
    print(f"   Auto-inicializar: {'✅ Sí' if repo_config['auto_init'] else '❌ No'}")
    
    print("\n🔐 Necesito el token GitHub para crear el repositorio.")
    print("   El token está almacenado de forma segura en el dashboard.")
    
    print("\n" + "=" * 60)
    print("🚀 COMANDOS PARA CREAR EL REPOSITORIO:")
    print("=" * 60)
    
    # Comando 1: Crear repositorio
    print("\n1. 📁 CREAR REPOSITORIO (ejecuta esto):")
    print("```bash")
    print("curl -X POST \\")
    print("  -H 'Authorization: token TU_TOKEN_GITHUB' \\")
    print("  -H 'Accept: application/vnd.github.v3+json' \\")
    print("  -d '" + json.dumps(repo_config, ensure_ascii=False) + "' \\")
    print("  https://api.github.com/user/repos")
    print("```")
    
    # Comando 2: Verificar creación
    print("\n2. ✅ VERIFICAR CREACIÓN:")
    print("```bash")
    print("# Después de crear, verifica que existe:")
    print("curl -H 'Authorization: token TU_TOKEN_GITHUB' \\")
    print("     https://api.github.com/repos/cuervoc-openclaw/father-documents")
    print("```")
    
    # Comando 3: Estructura inicial sugerida
    print("\n3. 📂 ESTRUCTURA INICIAL SUGERIDA:")
    print("```bash")
    print("# Clonar el repositorio (después de crearlo)")
    print("cd /home/cuervoc")
    print("git clone https://github.com/cuervoc-openclaw/father-documents.git")
    print("cd father-documents")
    print("")
    print("# Crear estructura de carpetas")
    print("mkdir -p documents photos projects memories backups")
    print("")
    print("# Crear README explicativo")
    print("cat > README.md << 'EOF'")
    print("# 👨‍🦳 Archivo Familiar - Documentos del Padre")
    print("")
    print("Repositorio privado para almacenar y organizar documentos familiares.")
    print("")
    print("## 📁 Estructura")
    print("- `documents/` - Documentos importantes (escaneados)")
    print("- `photos/` - Fotografías digitalizadas")
    print("- `projects/` - Proyectos personales")
    print("- `memories/` - Recuerdos, historias, anécdotas")
    print("- `backups/` - Copias de seguridad")
    print("")
    print("## 🔒 Seguridad")
    print("- Repositorio privado")
    print("- Solo acceso autorizado")
    print("- Historial de cambios con git")
    print("EOF")
    print("")
    print("# Primer commit con estructura")
    print("git add .")
    print("git commit -m 'Estructura inicial: documentos familiares'")
    print("git push origin main")
    print("```")
    
    # Información adicional
    print("\n" + "=" * 60)
    print("💡 RECOMENDACIONES:")
    print("=" * 60)
    
    print("\n📄 TIPOS DE DOCUMENTOS A GUARDAR:")
    print("   • Documentos de identidad (escaneados)")
    print("   • Certificados, títulos, diplomas")
    print("   • Recetas médicas importantes")
    print("   • Documentos legales (testamentos, poderes)")
    print("   • Fotografías familiares digitalizadas")
    print("   • Cartas, diarios, escritos personales")
    print("   • Árbol genealógico")
    print("   • Historias y anécdotas grabadas/escritas")
    
    print("\n🔐 VENTAJAS DE USAR GITHUB:")
    print("   ✅ Historial de cambios (sabes qué cambió y cuándo)")
    print("   ✅ Acceso desde cualquier lugar")
    print("   ✅ Copias de seguridad automáticas")
    print("   ✅ Organización con carpetas y archivos")
    print("   ✅ Privacidad (repositorio privado)")
    print("   ✅ Colaboración familiar (si agregas a otros)")
    
    print("\n🔄 PRÓXIMOS PASOS:")
    print("   1. Ejecuta el comando de creación (reemplaza TU_TOKEN_GITHUB)")
    print("   2. Clona el repositorio en tu servidor")
    print("   3. Crea la estructura de carpetas")
    print("   4. Comienza a subir documentos escaneados")
    print("   5. Yo puedo ayudarte a organizar y categorizar")
    
    return repo_config

def alternative_simple_script():
    """Script simple que puedes ejecutar con token"""
    print("\n" + "=" * 60)
    print("📜 SCRIPT SIMPLE PARA EJECUTAR:")
    print("=" * 60)
    
    script_content = '''#!/bin/bash
# Script para crear repositorio del padre
# Guarda como: create_father_repo.sh
# Ejecuta: bash create_father_repo.sh TU_TOKEN

TOKEN="$1"
if [ -z "$TOKEN" ]; then
    echo "❌ Error: Necesitas proporcionar el token"
    echo "Uso: bash create_father_repo.sh TU_TOKEN_GITHUB"
    exit 1
fi

echo "🚀 Creando repositorio 'father-documents'..."
curl -X POST \\
  -H "Authorization: token $TOKEN" \\
  -H "Accept: application/vnd.github.v3+json" \\
  -d '{"name":"father-documents","description":"Documentos familiares - Archivo personal","private":true,"auto_init":true}' \\
  https://api.github.com/user/repos

if [ $? -eq 0 ]; then
    echo "✅ Repositorio creado (si no da error)"
    echo ""
    echo "📁 Para clonar y configurar:"
    echo "cd /home/cuervoc"
    echo "git clone https://github.com/cuervoc-openclaw/father-documents.git"
    echo "cd father-documents"
    echo "mkdir -p documents photos projects memories"
else
    echo "❌ Error creando repositorio"
fi
'''
    
    print("\nGuarda este contenido como `create_father_repo.sh`:")
    print("```bash")
    print(script_content)
    print("```")
    
    print("\nLuego ejecuta:")
    print("```bash")
    print("chmod +x create_father_repo.sh")
    print("./create_father_repo.sh TU_TOKEN_GITHUB")
    print("```")

def main():
    # Mostrar opciones principales
    create_repository_for_father()
    
    # También ofrecer script simple
    print("\n" + "=" * 60)
    print("🎯 ¿QUÉ PREFIERES?")
    print("=" * 60)
    
    print("\nA. Ejecutas el comando curl manualmente")
    print("B. Usas el script simple que te proporciono")
    print("C. Cambiamos el nombre/configuración primero")
    print("D. Otra idea")
    
    print("\n💭 Mi recomendación: Opción B (script simple)")
    print("   Es más fácil y menos propenso a errores.")
    
    # Generar el script
    alternative_simple_script()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())