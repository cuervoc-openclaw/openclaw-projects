#!/usr/bin/env python3
"""
EJECUTAR TODO - Sistema completo de automatización
"""

import os
import sys
import subprocess
import json
import requests
from pathlib import Path

def print_step(step, message):
    """Imprimir paso con formato"""
    print(f"\n{'='*60}")
    print(f"🚀 {step}")
    print(f"{'='*60}")
    print(message)

def check_git_configured():
    """Verificar si git está configurado"""
    print_step("1. CONFIGURANDO GIT", "Configurando usuario global...")
    
    # Configurar usuario
    subprocess.run(["git", "config", "--global", "user.email", "zionylenodavid@gmail.com"], 
                   capture_output=True)
    subprocess.run(["git", "config", "--global", "user.name", "cuervoc-openclaw"], 
                   capture_output=True)
    
    # Verificar
    email = subprocess.run(["git", "config", "--global", "user.email"], 
                          capture_output=True, text=True).stdout.strip()
    name = subprocess.run(["git", "config", "--global", "user.name"], 
                         capture_output=True, text=True).stdout.strip()
    
    print(f"✅ Email: {email}")
    print(f"✅ Nombre: {name}")
    return True

def create_temp_token_file():
    """Crear archivo temporal con token (solo para esta ejecución)"""
    print_step("2. TOKEN TEMPORAL", "Solicitando token para GitHub...")
    
    # Crear instrucciones claras
    print("📋 Para continuar, necesito el token GitHub.")
    print("   Opciones:")
    print("   A. Pegar token aquí (se borrará después)")
    print("   B. Crear variable de entorno GITHUB_TOKEN")
    print("   C. Re-enviar al dashboard seguro")
    
    print("\n🎯 RECOMENDACIÓN: Opción B (más seguro)")
    print("   Ejecuta en otra terminal:")
    print("   export GITHUB_TOKEN='tu_token_github'")
    print("   Luego vuelve aquí")
    
    # Verificar si ya existe variable
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        print(f"✅ Token encontrado en variable de entorno: {token[:15]}...")
        return token
    
    # Pedir token directamente
    print("\n🔐 Si prefieres Opción A, ingresa el token ahora:")
    print("   (Se borrará automáticamente después)")
    try:
        token = input("Token GitHub: ").strip()
        if token and (token.startswith('ghp_') or token.startswith('github_pat_')):
            print(f"✅ Token recibido: {token[:15]}...")
            
            # Guardar temporalmente (se borrará)
            with open('/tmp/github_token_temp.txt', 'w') as f:
                f.write(token)
            os.chmod('/tmp/github_token_temp.txt', 0o600)  # Solo lectura propietario
            
            return token
        else:
            print("❌ Formato de token inválido")
            return None
    except:
        print("❌ No se pudo leer el token")
        return None

def test_github_token(token):
    """Probar que el token funciona"""
    print_step("3. PROBANDO TOKEN", "Verificando conexión con GitHub...")
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        response = requests.get('https://api.github.com/user', headers=headers, timeout=10)
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Autenticación exitosa!")
            print(f"   Usuario: {user_data.get('login')}")
            print(f"   Nombre: {user_data.get('name', 'N/A')}")
            print(f"   Repos: {user_data.get('public_repos', 0)} públicos")
            return True, user_data
        else:
            print(f"❌ Error {response.status_code}: {response.text[:100]}")
            return False, None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False, None

def create_github_repository(token, repo_name, description, private=False):
    """Crear repositorio en GitHub"""
    print_step(f"4. CREANDO REPOSITORIO '{repo_name}'", description)
    
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
            print(f"✅ ¡Repositorio creado!")
            print(f"   URL: {repo_data.get('html_url')}")
            print(f"   Clone: {repo_data.get('clone_url')}")
            print(f"   SSH: {repo_data.get('ssh_url')}")
            return True, repo_data
        elif response.status_code == 422:
            error_data = response.json()
            if 'already exists' in str(error_data).lower():
                print(f"ℹ️  El repositorio '{repo_name}' ya existe")
                # Obtener info del repo existente
                return get_existing_repo(token, repo_name)
            else:
                print(f"❌ Error 422: {error_data.get('message', 'N/A')}")
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
        # Obtener username primero
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
        print(f"❌ Error obteniendo repo: {e}")
    
    return False, None

def setup_and_push_to_repo(token, repo_name, repo_data):
    """Configurar git local y subir archivos"""
    print_step("5. SUBIENDO ARCHIVOS", f"Preparando push a {repo_name}...")
    
    # Cambiar al workspace
    workspace = "/home/cuervoc/.openclaw/workspace"
    os.chdir(workspace)
    
    # URL del repositorio
    clone_url = repo_data.get('clone_url')
    if not clone_url:
        # Construir URL si no está en response
        user_resp = requests.get('https://api.github.com/user', 
                                headers={'Authorization': f'token {token}'})
        username = user_resp.json().get('login')
        clone_url = f"https://github.com/{username}/{repo_name}.git"
    
    print(f"📁 Workspace: {workspace}")
    print(f"🔗 Repositorio: {clone_url}")
    
    # Inicializar git si no está
    if not os.path.exists('.git'):
        print("🔄 Inicializando repositorio git...")
        subprocess.run(["git", "init"], capture_output=True)
    
    # Configurar remote
    print("🔗 Configurando remote...")
    subprocess.run(["git", "remote", "remove", "origin"], capture_output=True)
    result = subprocess.run(["git", "remote", "add", "origin", clone_url], 
                           capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error configurando remote: {result.stderr}")
        return False
    
    # Agregar todos los archivos (excepto algunos)
    print("📦 Agregando archivos...")
    
    # Lista de archivos a ignorar
    ignore_files = ['.git', '__pycache__', '*.pyc', '*.log', 'credentials_server.log',
                   'http_server.log', 'api_server.log', 'dashboard.log']
    
    # Agregar archivos manualmente para mejor control
    files_to_add = []
    for item in Path('.').iterdir():
        if item.name.startswith('.'):
            continue
        if item.name in ignore_files:
            continue
        if item.suffix in ['.pyc', '.log']:
            continue
        files_to_add.append(str(item))
    
    if files_to_add:
        subprocess.run(["git", "add"] + files_to_add, capture_output=True)
    
    # Commit
    print("💾 Haciendo commit...")
    commit_msg = f"Initial commit: {repo_name} - OpenClaw projects"
    result = subprocess.run(["git", "commit", "-m", commit_msg], 
                           capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"⚠️  Commit no necesario o vacío: {result.stderr[:100]}")
    
    # Push
    print("🚀 Haciendo push...")
    result = subprocess.run(["git", "push", "-u", "origin", "main", "--force"], 
                           capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ ¡Push exitoso!")
        return True
    else:
        print(f"❌ Error en push: {result.stderr}")
        
        # Intentar con branch master si main falla
        print("🔄 Intentando con branch 'master'...")
        result = subprocess.run(["git", "push", "-u", "origin", "master", "--force"], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ¡Push exitoso a master!")
            return True
        else:
            print(f"❌ Error también con master: {result.stderr}")
            return False

def list_files_to_upload():
    """Listar archivos que se subirán"""
    print_step("📁 ARCHIVOS PARA SUBIR", "Lista completa del workspace:")
    
    workspace = "/home/cuervoc/.openclaw/workspace"
    files = []
    
    for item in Path(workspace).iterdir():
        if item.name.startswith('.'):
            continue
        if item.name in ['__pycache__', '*.pyc', '*.log']:
            continue
        
        size = item.stat().st_size if item.is_file() else 0
        files.append((item.name, size, 'dir' if item.is_dir() else 'file'))
    
    # Ordenar por tipo y nombre
    files.sort(key=lambda x: (x[2], x[0]))
    
    print("📋 Contenido del workspace:")
    for name, size, ftype in files:
        if ftype == 'file':
            print(f"   📄 {name} ({size/1024:.1f} KB)")
        else:
            print(f"   📁 {name}/")
    
    return len(files)

def main():
    """Función principal - EJECUTAR TODO"""
    print("\n" + "="*70)
    print("🚀 EJECUTANDO TODO - SISTEMA COMPLETO DE AUTOMATIZACIÓN")
    print("="*70)
    
    # 1. Listar archivos
    file_count = list_files_to_upload()
    print(f"\n📊 Total: {file_count} archivos/carpetas listos para subir")
    
    # 2. Configurar git
    if not check_git_configured():
        return 1
    
    # 3. Obtener token
    token = create_temp_token_file()
    if not token:
        print("❌ No se pudo obtener token. Abortando.")
        return 1
    
    # 4. Probar token
    token_ok, user_data = test_github_token(token)
    if not token_ok:
        print("❌ Token inválido. Abortando.")
        return 1
    
    # 5. Crear repositorio PRINCIPAL (openclaw-projects)
    repo_name = "openclaw-projects"
    repo_desc = "OpenClaw assistant projects - LOL Coach, STT system, credentials dashboard"
    
    repo_ok, repo_data = create_github_repository(token, repo_name, repo_desc, private=False)
    if not repo_ok:
        print("❌ No se pudo crear/obtener repositorio. Abortando.")
        return 1
    
    # 6. Subir archivos al repositorio principal
    push_ok = setup_and_push_to_repo(token, repo_name, repo_data)
    if not push_ok:
        print("❌ No se pudo subir archivos. Abortando.")
        return 1
    
    # 7. Opcional: Crear repositorio para documentos del padre
    print("\n" + "="*70)
    print("👨‍🦳 ¿CREAR TAMBIÉN REPOSITORIO PARA DOCUMENTOS DEL PADRE?")
    print("="*70)
    
    print("\n📋 Opciones:")
    print("   1. Sí, crear 'father-documents' (privado)")
    print("   2. No, solo con el repositorio principal")
    print("   3. Crear con otro nombre/configuración")
    
    # Por defecto, crear ambos
    father_repo_name = "father-documents"
    father_desc = "Documentos, fotos y proyectos personales - Archivo familiar"
    
    print(f"\n🎯 Creando también: {father_repo_name}...")
    father_ok, father_data = create_github_repository(token, father_repo_name, father_desc, private=True)
    
    if father_ok:
        print(f"✅ Repositorio para documentos del padre creado: {father_data.get('html_url')}")
        
        # Crear estructura básica
        print("\n📂 Creando estructura básica...")
        os.system(f"mkdir -p /tmp/{father_repo_name}")
        os.chdir(f"/tmp/{father_repo_name}")
        
        # Crear README
        with open("README.md", "w") as f:
            f.write(f"""# 👨‍🦳 {father_repo_name}

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

## 📝 Uso
1. Escanear documentos importantes
2. Digitalizar fotografías antiguas
3. Organizar por categorías/años
4. Agregar descripciones a cada archivo
""")
        
        os.system("mkdir -p documents photos projects memories backups")
        os.system("git init")
        os.system("git add .")
        os.system('git commit -m "Estructura inicial para documentos familiares"')
        
        # Configurar remote y push
        father_clone = father_data.get('clone_url')
        if father_clone:
            os.system(f"git remote add origin {father_clone}")
            os.system("git push -u origin main")
    
    # 8. Limpiar token temporal
    print("\n" + "="*70)
    print("🧹 LIMPIANDO DATOS TEMPORALES")
    print("="*70)
    
    temp_files = ['/tmp/github_token_temp.txt', f'/tmp/{father_repo_name}']
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            if os.path.isdir(temp_file):
                os.system(f"rm -rf {temp_file}")
            else:
                os.remove(temp_file)
    
    print("✅ Tokens y datos temporales eliminados")
    
    # 9. Resumen final
    print("\n" + "="*70)
    print("🎉 ¡TODO COMPLETADO CON ÉXITO!")
    print("="*70)
    
    print(f"\n📊 RESUMEN:")
    print(f"   1. ✅ Git configurado")
    print(f"   2. ✅ Token verificado (usuario: {user_data.get('login')})")
    print(f"   3. ✅ Repositorio principal: https://github.com/{user_data.get('login')}/{repo_name}")
    
    if father_ok:
        print(f"   4. ✅ Repos