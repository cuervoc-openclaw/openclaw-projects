#!/usr/bin/env python3
"""
Script para leer credenciales del servidor seguro
Usado por el asistente OpenClaw para acceder a tokens de forma segura
"""

import requests
import json
import time
import sys

def get_server_url():
    """Obtener URL del servidor (configurable)"""
    # Intentar puertos comunes
    ports = [8081, 8083, 8085, 8087]
    for port in ports:
        url = f"http://localhost:{port}"
        try:
            response = requests.get(f"{url}/status", timeout=2)
            if response.status_code == 200:
                return url
        except:
            continue
    # Default
    return "http://192.168.100.170:8081"

SERVER_URL = get_server_url()

def check_server():
    """Verificar si el servidor está activo"""
    try:
        response = requests.get(f"{SERVER_URL}/status", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None

def get_credentials():
    """Obtener credenciales del servidor"""
    try:
        response = requests.get(f"{SERVER_URL}/get", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error conectando al servidor: {e}")
        return None

def get_github_token():
    """Obtener token GitHub específico"""
    try:
        # Importar del módulo del servidor si está corriendo
        from credentials_server import get_github_token as server_get_token
        token = server_get_token()
        if token:
            return token
    except ImportError:
        pass
    
    # Fallback: leer del servidor HTTP
    creds = get_credentials()
    if creds and creds.get('status') == 'ok' and creds.get('has_github'):
        # Nota: El endpoint /get solo devuelve preview, no el token completo
        # Para obtener el token completo, necesitamos acceso directo al módulo
        print("⚠️  Token GitHub disponible pero no accesible via HTTP")
        print(f"   Preview: {creds.get('github_preview', 'N/A')}")
        return None
    
    return None

def get_riot_key():
    """Obtener key Riot específica"""
    try:
        from credentials_server import get_riot_key as server_get_key
        key = server_get_key()
        if key:
            return key
    except ImportError:
        pass
    
    creds = get_credentials()
    if creds and creds.get('status') == 'ok' and creds.get('has_riot'):
        print("⚠️  Key Riot disponible pero no accesible via HTTP")
        print(f"   Preview: {creds.get('riot_preview', 'N/A')}")
        return None
    
    return None

def main():
    """Función principal - mostrar estado y credenciales"""
    print("🔐 OpenClaw Credentials Reader")
    print("=" * 50)
    
    # Verificar servidor
    status = check_server()
    if not status:
        print("❌ Servidor de credenciales no disponible")
        print("\n💡 Para iniciar el servidor:")
        print("   python3 credentials_server.py")
        return 1
    
    print(f"✅ Servidor activo: {status.get('status', 'unknown')}")
    print(f"📊 Almacenamiento activo: {status.get('store_active', False)}")
    print(f"⏱️  Expirado: {status.get('expired', False)}")
    
    # Obtener credenciales
    creds = get_credentials()
    if not creds:
        print("\n❌ No se pudieron obtener credenciales")
        return 1
    
    print("\n📋 Credenciales disponibles:")
    print(f"   GitHub: {'✅' if creds.get('has_github') else '❌'}")
    if creds.get('github_preview'):
        print(f"     Preview: {creds.get('github_preview')}")
    
    print(f"   Riot Games: {'✅' if creds.get('has_riot') else '❌'}")
    if creds.get('riot_preview'):
        print(f"     Preview: {creds.get('riot_preview')}")
    
    print(f"   Custom APIs: {creds.get('has_custom', False)}")
    
    if creds.get('last_updated'):
        last_update = time.strftime('%Y-%m-%d %H:%M:%S', 
                                   time.localtime(creds['last_updated']))
        time_diff = time.time() - creds['last_updated']
        expires_in = max(0, 300 - time_diff)  # 5 minutos
        
        print(f"\n⏰ Última actualización: {last_update}")
        print(f"   Expira en: {int(expires_in // 60)}:{int(expires_in % 60):02d} minutos")
    
    # Intentar obtener tokens completos (solo funciona si estamos en el mismo proceso)
    print("\n🔧 Acceso directo a tokens:")
    github_token = get_github_token()
    riot_key = get_riot_key()
    
    print(f"   GitHub Token: {'✅ Disponible' if github_token else '❌ No accesible'}")
    print(f"   Riot API Key: {'✅ Disponible' if riot_key else '❌ No accesible'}")
    
    if github_token or riot_key:
        print("\n🚀 Credenciales listas para usar en scripts")
        
        # Ejemplo de uso
        if github_token:
            print(f"\n📁 Ejemplo - Crear repo GitHub:")
            print(f"   curl -H 'Authorization: token {github_token[:10]}...' \\")
            print(f"        https://api.github.com/user/repos")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())