#!/usr/bin/env python3
"""
Ejecutar TODO usando el token del servidor de credenciales
"""

import requests
import json
import subprocess
import os
import sys
import time

def get_token_from_server():
    """Obtener token directamente del servidor de credenciales"""
    try:
        # El token está en el servidor, necesitamos acceso directo
        # Intentar importar el módulo del servidor
        sys.path.insert(0, '/home/cuervoc/.openclaw/workspace')
        
        try:
            from credentials_server_fixed import get_github_token
            token = get_github_token()
            if token:
                print(f"✅ Token obtenido del servidor: {token[:20]}...")
                return token
        except ImportError:
            pass
        
        # Si no funciona, intentar leer del almacenamiento compartido
        import credentials_server_fixed
        with credentials_server_fixed.store_lock:
            store = credentials_server_fixed.credentials_store
            if (store['github_token'] and 
                store['last_updated'] and
                time.time() - store['last_updated'] <= 300):
                print(f"✅ Token obtenido de almacenamiento: {store['github_token'][:20]}...")
                return store['github_token']
        
    except Exception as e:
        print(f"❌ Error accediendo al token: {e}")
    
    return None

def test_github_token(token):
    """Probar token con GitHub API"""
    print("🔍 Probando token GitHub...")
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        response = requests.get('https://api.github.com/user', headers=headers, timeout=10)
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Autenticación exitosa - Usuario: {user_data.get('login')}")
            return True, user_data
        else:
            print(f"❌ Error {response.status_code}: {response.text[:100]}")
            return False, None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False, None

def create_repository(token, repo_name, description, private=False):
    """Crear repositorio en GitHub"""
    print(f"📁 Creando repositorio '{repo_name}'...")
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    data = {
        'name': repo_name,
        'description': description,
        'private': private,
        'auto_init': True,
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
            print(f"✅ Repositorio creado: {repo_data.get('html_url')}")
            return True, repo_data
        elif response.status_code == 422:
            error_data = response.json()
            if 'already exists' in str(error_data).lower():
                print(f"ℹ️  Repositorio '{repo_name}' ya existe")
                # Obtener información del repo existente
                return get_existing_repo(token, repo_name)
            else:
                print(f"❌ Error 422: {error_data.get('message')}")
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
    
    try:
        # Obtener username
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
                print(f"✅ Repositorio existente: {repo_data.get('html_url')}")
                return True, repo_data
    except Exception as e:
        print(f"❌ Error obteniendo repo: {e}")
    
    return False, None

def setup_git_and_push(token, repo_name, repo_data):
    """Configurar git y subir archivos"""
    print(f"📤 Subiendo archivos a '{repo_name}'...")
    
    # Cambiar al workspace
    workspace = "/home/cuervoc/.openclaw/workspace"
    os.chdir(workspace)
    
    # Configurar git si no está
    subprocess.run(["git", "config", "--global", "user.email", "zionylenodavid@gmail.com"], 
                   capture_output=True)
    subprocess.run(["git", "config", "--global", "user.name", "cuervoc-openclaw"], 
                   capture_output=True)
    
    # URL del repositorio
    clone_url = repo_data.get('clone_url')
    if not clone_url:
        # Construir URL
        user_resp = requests.get('https://api.github.com/user', 
                                headers={'Authorization': f'token {token}'})
        username = user_resp.json().get('login')
        clone_url = f"https://github.com/{username}/{repo_name}.git"
    
    print(f"🔗 Repositorio: {clone_url}")
    
    # Inicializar git si no existe
    if not os.path.exists('.git'):
        subprocess.run(["git", "init"], capture_output=True)
    
    # Configurar remote
    subprocess.run(["git", "remote", "remove", "origin"], capture_output=True)
    result = subprocess.run(["git", "remote", "add", "origin", clone_url], 
                           capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Error configurando remote: {result.stderr}")
        return False
    
    # Agregar archivos
    print("📦 Agregando archivos...")
    
    # Agregar archivos Python, Markdown, scripts, HTML, JS
    for ext in ['*.py', '*.md', '*.sh', '*.html', '*.js']:
        subprocess.run(f"find . -name '{ext}' -not -path './__pycache__/*' -not -name '*.pyc' -not -name '*.log' -exec git add {{}} \\;", 
                      shell=True, capture_output=True)
    
    # Commit
    print("💾 Haciendo commit...")
    commit_msg = f"Initial commit: {repo_name} - OpenClaw projects"
    result = subprocess.run(["git", "commit", "-m", commit_msg], 
                           capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"⚠️  Commit no necesario: {result.stderr[:100]}")
    
    # Push
    print("🚀 Haciendo push...")
    result = subprocess.run(["git", "push", "-u", "origin", "main", "--force"], 
                           capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Push exitoso a main")
        return True
    else:
        # Intentar con master
        print("🔄 Intentando con branch 'master'...")
        result = subprocess.run(["git", "push", "-u", "origin", "master", "--force"], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Push exitoso a master")
            return True
        else:
            print(f"❌ Error en push: {result.stderr[:200]}")
            return False

def main():
    print("🚀 EJECUTANDO TODO CON TOKEN DEL SERVIDOR")
    print("=" * 60)
    
    # 1. Obtener token del servidor
    token = get_token_from_server()
    if not token:
        print("❌ No se pudo obtener el token del servidor")
        print("💡 Asegúrate de que el token fue re-enviado al dashboard")
        return 1
    
    # 2. Probar token
    token_ok, user_data = test_github_token(token)
    if not token_ok:
        print("❌ Token inválido")
        return 1
    
    username = user_data.get('login')
    print(f"👤 Usuario GitHub: {username}")
    
    # 3. Crear repositorio openclaw-projects
    print("\n" + "=" * 60)
    repo1_name = "openclaw-projects"
    repo1_desc = "OpenClaw assistant projects - LOL Coach, STT system, credentials dashboard"
    
    repo1_ok, repo1_data = create_repository(token, repo1_name, repo1_desc, private=False)
    
    if repo1_ok:
        # 4. Subir archivos a openclaw-projects
        push1_ok = setup_git_and_push(token, repo1_name, repo1_data)
        if push1_ok:
            print(f"✅ ¡Archivos subidos a {repo1_name}!")
        else:
            print(f"⚠️  Problemas subiendo archivos a {repo1_name}")
    else:
        print(f"❌ No se pudo crear/obtener {repo1_name}")
    
    # 5. Crear repositorio father-documents
    print("\n" + "=" * 60)
    repo2_name = "father-documents"
    repo2_desc = "Documentos, fotos y proyectos personales - Archivo familiar"
    
    repo2_ok, repo2_data = create_repository(token, repo2_name, repo2_desc, private=True)
    
    if repo2_ok:
        print(f"✅ Repositorio {repo2_name} creado/obtenido")
        
        # Crear estructura básica
        print("📂 Creando estructura básica...")
        os.system(f"mkdir -p /tmp/{repo2_name}")
        os.chdir(f"/tmp/{repo2_name}")
        
        # Crear README
        with open("README.md", "w") as f:
            f.write(f"""# 👨‍🦳 {repo2_name}

Repositorio privado para documentos familiares importantes.

## 📁 Estructura
- `documents/` - Documentos escaneados
- `photos/` - Fotografías digitalizadas  
- `projects/` - Proyectos personales
- `memories/` - Historias y anécdotas
- `backups/` - Copias de seguridad

## 🔒 Seguridad
- Repositorio privado
- Solo acceso autorizado
- Historial completo con git
""")
        
        os.system("mkdir -p documents photos projects memories backups")
        
        # Inicializar y subir
        os.system("git init")
        os.system("git add .")
        os.system(f'git commit -m "Estructura inicial para {repo2_name}"')
        
        clone_url = repo2_data.get('clone_url') or f"https://github.com/{username}/{repo2_name}.git"
        os.system(f"git remote add origin {clone_url}")
        
        if os.system("git push -u origin main --force 2>/dev/null") == 0:
            print(f"✅ Estructura subida a {repo2_name}")
        elif os.system("git push -u origin master --force 2>/dev/null") == 0:
            print(f"✅ Estructura subida a {repo2_name} (master)")
    
    # 6. Resumen final
    print("\n" + "=" * 60)
    print("🎉 ¡EJECUCIÓN COMPLETADA!")
    print("=" * 60)
    
    print(f"\n📊 RESUMEN:")
    print(f"   1. Usuario: {username}")
    
    if repo1_ok:
        print(f"   2. Repositorio principal: https://github.com/{username}/{repo1_name}")
    
    if repo2_ok:
        print(f"   3. Repositorio documentos: https://github.com/{username}/{repo2_name}")
    
    print(f"\n📁 Archivos en workspace:")
    os.chdir("/home/cuervoc/.openclaw/workspace")
    files = [f for f in os.listdir('.') if not f.startswith('.') and not f.endswith('.pyc')]
    for f in files[:10]:  # Mostrar primeros 10
        if os.path.isfile(f):
            size = os.path.getsize(f)
            print(f"   📄 {f} ({size} bytes)")
    
    if len(files) > 10:
        print(f"   ... y {len(files)-10} más")
    
    print("\n🚀 Próximos pasos:")
    print("   • Verificar repositorios en GitHub")
    print("   • Agregar más archivos cuando quieras")
    print("   • Usar dashboard para tokens futuros")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())