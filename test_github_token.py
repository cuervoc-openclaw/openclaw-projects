#!/usr/bin/env python3
"""
Testear acceso al token GitHub de forma segura
"""

import requests
import json
import sys

def get_token_from_server():
    """Obtener token del servidor de forma segura"""
    try:
        # Leer directamente del módulo del servidor (mismo proceso)
        from credentials_server_fixed import get_github_token
        token = get_github_token()
        if token:
            return token
    except ImportError as e:
        print(f"❌ Error importando: {e}")
    
    # Fallback: leer del almacenamiento compartido
    try:
        # El servidor almacena en memoria global
        import credentials_server_fixed
        with credentials_server_fixed.store_lock:
            store = credentials_server_fixed.credentials_store
            if (store['github_token'] and 
                store['last_updated'] and
                time.time() - store['last_updated'] <= 300):
                return store['github_token']
    except:
        pass
    
    return None

def test_github_api(token):
    """Probar que el token funciona con GitHub API"""
    print("🔍 Probando token GitHub...")
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # 1. Verificar autenticación
    try:
        response = requests.get(
            'https://api.github.com/user',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Autenticación exitosa")
            print(f"   Usuario: {user_data.get('login', 'N/A')}")
            print(f"   Nombre: {user_data.get('name', 'N/A')}")
            print(f"   Email: {user_data.get('email', 'N/A')}")
            return True, user_data
        else:
            print(f"❌ Error {response.status_code}: {response.text[:100]}")
            return False, None
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False, None

def main():
    print("🔐 Test de Token GitHub Seguro")
    print("=" * 50)
    
    # Obtener token
    token = get_token_from_server()
    
    if not token:
        print("❌ No se pudo obtener el token GitHub")
        print("\n💡 Posibles causas:")
        print("   1. El token expiró (5 minutos)")
        print("   2. El servidor se reinició")
        print("   3. Error de importación")
        
        # Intentar leer del endpoint HTTP
        print("\n🔍 Intentando vía HTTP...")
        try:
            response = requests.get('http://192.168.100.170:8081/get', timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   Estado: {data.get('status')}")
                print(f"   GitHub disponible: {data.get('has_github')}")
                if data.get('github_preview'):
                    print(f"   Preview: {data.get('github_preview')}")
        except Exception as e:
            print(f"   Error HTTP: {e}")
        
        return 1
    
    print(f"✅ Token obtenido: {token[:20]}...")
    
    # Probar con GitHub API
    success, user_data = test_github_api(token)
    
    if success:
        print("\n🎉 ¡TOKEN GITHUB FUNCIONAL!")
        print(f"\n📋 Información del usuario:")
        print(f"   Login: {user_data.get('login')}")
        print(f"   ID: {user_data.get('id')}")
        print(f"   Tipo: {user_data.get('type')}")
        print(f"   Repos públicos: {user_data.get('public_repos', 0)}")
        
        # Verificar permisos
        print(f"\n🔧 Permisos del token:")
        # Los tokens PAT tienen scope 'repo' por defecto si se crearon con ese permiso
        print("   (Asumiendo permisos 'repo' para crear repositorios)")
        
        return 0
    else:
        print("\n❌ El token no es funcional o no tiene permisos suficientes")
        return 1

if __name__ == "__main__":
    import time
    sys.exit(main())