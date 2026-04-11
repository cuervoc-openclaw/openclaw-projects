#!/usr/bin/env python3
"""
Crear repositorio GitHub usando el token almacenado
"""

import requests
import json
import sys
import os
import time

def get_github_token_direct():
    """Obtener token directamente del servidor"""
    try:
        # Intentar conectar al servidor y leer credenciales
        response = requests.get('http://192.168.100.170:8081/get', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('has_github') and data.get('status') == 'ok':
                # El token real está en el servidor, necesitamos acceso directo
                # Por ahora, vamos a pedir que se reenvíe o usar otro método
                print("✅ Token GitHub disponible en servidor")
                print(f"   Preview: {data.get('github_preview', 'N/A')}")
                
                # Para este caso, vamos a crear un método alternativo
                return "USE_TOKEN_FROM_SERVER"
    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")
    
    return None

def create_github_repository(token, repo_name, description, private=False):
    """Crear repositorio en GitHub"""
    print(f"🚀 Creando repositorio '{repo_name}'...")
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    data = {
        'name': repo_name,
        'description': description,
        'private': private,
        'auto_init': True,  # Crear con README
        'gitignore_template': 'Python'
    }
    
    try:
        response = requests.post(
            'https://api.github.com/user/repos',
            headers=headers,
            json=data,
            timeout=15
        )
        
        if response.status_code == 201:
            repo_data = response.json()
            print(f"✅ ¡Repositorio creado exitosamente!")
            print(f"   Nombre: {repo_data.get('full_name')}")
            print(f"   URL: {repo_data.get('html_url')}")
            print(f"   SSH: {repo_data.get('ssh_url')}")
            print(f"   HTTPS: {repo_data.get('clone_url')}")
            return True, repo_data
        elif response.status_code == 401:
            print(f"❌ Error 401: Token inválido o expirado")
            print(f"   Mensaje: {response.json().get('message', 'N/A')}")
            return False, None
        elif response.status_code == 422:
            error_data = response.json()
            print(f"❌ Error 422: {error_data.get('message', 'N/A')}")
            if 'errors' in error_data:
                for err in error_data['errors']:
                    print(f"   - {err.get('message', 'N/A')}")
            
            # Si el repo ya existe, podemos usarlo
            if 'name already exists' in str(error_data).lower():
                print("💡 El repositorio ya existe, obteniendo información...")
                return get_existing_repo(token, repo_name)
            return False, None
        else:
            print(f"❌ Error {response.status_code}: {response.text[:200]}")
            return False, None
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False, None

def get_existing_repo(token, repo_name):
    """Obtener información de repositorio existente"""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Primero obtener el username
    try:
        user_resp = requests.get('https://api.github.com/user', headers=headers, timeout=10)
        if user_resp.status_code == 200:
            username = user_resp.json().get('login')
            
            # Obtener repo
            repo_resp = requests.get(
                f'https://api.github.com/repos/{username}/{repo_name}',
                headers=headers,
                timeout=10
            )
            
            if repo_resp.status_code == 200:
                repo_data = repo_resp.json()
                print(f"✅ Repositorio existente encontrado")
                print(f"   URL: {repo_data.get('html_url')}")
                return True, repo_data
    except Exception as e:
        print(f"❌ Error obteniendo repo existente: {e}")
    
    return False, None

def setup_git_and_push():
    """Configurar git y subir archivos"""
    print("\n📁 Configurando git local...")
    
    # Configurar usuario
    os.system('git config --global user.email "zionylenodavid@gmail.com"')
    os.system('git config --global user.name "cuervoc-openclaw"')
    
    # Inicializar repo
    os.system('git init')
    os.system('git add .')
    os.system('git commit -m "Initial commit: OpenClaw projects"')
    
    print("✅ Git configurado localmente")
    return True

def main():
    print("🚀 CREACIÓN DE REPOSITORIO GITHUB")
    print("=" * 50)
    
    # 1. Verificar token
    token_status = get_github_token_direct()
    
    if token_status != "USE_TOKEN_FROM_SERVER":
        print("❌ No se puede acceder al token de forma segura")
        print("\n💡 SOLUCIONES:")
        print("   1. Re-enviar el token desde el dashboard")
        print("   2. Usar token temporal por línea de comandos")
        print("   3. Crear nuevo token con permisos 'repo'")
        
        # Opción: pedir token manualmente (solo para desarrollo)
        print("\n🔧 Opción temporal (solo para pruebas):")
        print("   Ejecuta esto en el servidor:")
        print("   curl -X POST http://192.168.100.170:8081/ \\")
        print("     -H 'Content-Type: application/json' \\")
        print("     -d '{\"github_token\": \"TU_TOKEN_AQUI\"}'")
        
        return 1
    
    # 2. Para continuar, necesitamos el token real
    print("\n📋 Para crear el repositorio, necesito el token real.")
    print("   Opciones:")
    print("   A. Pegar token aquí (NO RECOMENDADO por seguridad)")
    print("   B. Configurar variable de entorno temporal")
    print("   C. Yo te doy los comandos para que los ejecutes tú")
    
    print("\n🎯 RECOMENDACIÓN (Opción C - Más segura):")
    print("   Yo genero los comandos, tú los ejecutas")
    
    # Generar comandos para ejecutar manualmente
    print("\n" + "=" * 50)
    print("📝 COMANDOS PARA EJECUTAR MANUALMENTE:")
    print("=" * 50)
    
    print("\n1. Verificar token (desde tu máquina):")
    print("   curl -H 'Authorization: token TU_TOKEN' \\")
    print("        https://api.github.com/user")
    
    print("\n2. Crear repositorio:")
    print("   curl -X POST \\")
    print("     -H 'Authorization: token TU_TOKEN' \\")
    print("     -H 'Accept: application/vnd.github.v3+json' \\")
    print("     -d '{\"name\":\"openclaw-projects\",\"description\":\"OpenClaw assistant projects\",\"private\":false,\"auto_init\":true}' \\")
    print("     https://api.github.com/user/repos")
    
    print("\n3. Configurar git y subir:")
    print("   cd /home/cuervoc/.openclaw/workspace")
    print("   git config --global user.email 'zionylenodavid@gmail.com'")
    print("   git config --global user.name 'cuervoc-openclaw'")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial commit: OpenClaw projects'")
    print("   git remote add origin https://github.com/cuervoc-openclaw/openclaw-projects.git")
    print("   git push -u origin main")
    
    print("\n" + "=" * 50)
    print("💡 ¿Prefieres que genere un script automático o ejecutas los comandos?")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())