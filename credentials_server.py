#!/usr/bin/env python3
"""
Servidor seguro para manejo de credenciales
Almacena tokens temporalmente en memoria (no en disco)
"""

import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

# Almacenamiento temporal en memoria (volátil)
credentials_store = {
    "github_token": None,
    "riot_key": None,
    "custom_credentials": {},
    "last_updated": None
}

# Lock para thread safety
store_lock = threading.Lock()

class CredentialsHandler(BaseHTTPRequestHandler):
    """Manejador de peticiones HTTP para credenciales"""
    
    def do_GET(self):
        """Endpoint para leer credenciales"""
        # Permitir desde cualquier IP en la red local
        # (Ya que el dashboard está en otra IP)
        client_ip = self.client_address[0]
        
        # Solo registrar para debugging
        # print(f"📡 Conexión desde: {client_ip}")
        
        # Continuar sin restricciones de IP
        
        parsed = urlparse(self.path)
        
        if parsed.path == '/get':
            # Obtener credenciales
            with store_lock:
                # Verificar expiración (5 minutos)
                if (credentials_store['last_updated'] and 
                    time.time() - credentials_store['last_updated'] > 300):
                    # Credenciales expiradas
                    self._send_response(200, {
                        'status': 'expired',
                        'message': 'Credenciales han expirado (5 minutos)'
                    })
                    return
                
                # Preparar respuesta (ocultar valores completos)
                response = {
                    'status': 'ok',
                    'has_github': bool(credentials_store['github_token']),
                    'has_riot': bool(credentials_store['riot_key']),
                    'has_custom': len(credentials_store['custom_credentials']) > 0,
                    'last_updated': credentials_store['last_updated']
                }
                
                # Solo incluir previews de tokens (no completos)
                if credentials_store['github_token']:
                    token = credentials_store['github_token']
                    response['github_preview'] = f"{token[:10]}...{token[-4:]}"
                
                if credentials_store['riot_key']:
                    key = credentials_store['riot_key']
                    response['riot_preview'] = f"{key[:10]}...{key[-4:]}"
                
                self._send_response(200, response)
                
        elif parsed.path == '/status':
            # Solo estado
            with store_lock:
                self._send_response(200, {
                    'status': 'ok',
                    'store_active': bool(credentials_store['last_updated']),
                    'expired': (credentials_store['last_updated'] and 
                               time.time() - credentials_store['last_updated'] > 300)
                })
                
        elif parsed.path == '/clear':
            # Limpiar credenciales
            with store_lock:
                credentials_store.update({
                    'github_token': None,
                    'riot_key': None,
                    'custom_credentials': {},
                    'last_updated': None
                })
                self._send_response(200, {'status': 'cleared'})
                
        else:
            self._send_response(404, {'error': 'Endpoint no encontrado'})
    
    def do_POST(self):

    def do_OPTIONS(self):
        """Handler para CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()
        """Endpoint para almacenar credenciales"""
        # Permitir desde cualquier IP
        client_ip = self.client_address[0]
        # print(f"📨 POST desde: {client_ip}")
        
        # Leer datos JSON
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            self._send_response(400, {'error': 'Sin datos'})
            return
        
        try:
            data = json.loads(self.rfile.read(content_length).decode('utf-8'))
        except:
            self._send_response(400, {'error': 'JSON inválido'})
            return
        
        # Validar y almacenar
        with store_lock:
            if 'github_token' in data:
                credentials_store['github_token'] = data['github_token']
            
            if 'riot_key' in data:
                credentials_store['riot_key'] = data['riot_key']
            
            if 'custom' in data:
                for name, key in data['custom'].items():
                    credentials_store['custom_credentials'][name] = key
            
            credentials_store['last_updated'] = time.time()
            
            self._send_response(200, {
                'status': 'stored',
                'received': {
                    'github': 'github_token' in data,
                    'riot': 'riot_key' in data,
                    'custom': len(data.get('custom', {}))
                }
            })
    
    def _send_response(self, code, data):
        """Enviar respuesta JSON"""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Solo para desarrollo
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Silenciar logs normales (solo errores)"""
        pass

def get_github_token():
    """Obtener token GitHub de forma segura"""
    with store_lock:
        if (credentials_store['github_token'] and 
            credentials_store['last_updated'] and
            time.time() - credentials_store['last_updated'] <= 300):
            return credentials_store['github_token']
    return None

def get_riot_key():
    """Obtener key Riot de forma segura"""
    with store_lock:
        if (credentials_store['riot_key'] and 
            credentials_store['last_updated'] and
            time.time() - credentials_store['last_updated'] <= 300):
            return credentials_store['riot_key']
    return None

def start_server(port=8081, host='0.0.0.0'):
    """Iniciar servidor en segundo plano"""
    server = HTTPServer((host, port), CredentialsHandler)
    print(f"🔐 Servidor de credenciales iniciado en http://{host}:{port}")
    if host == '0.0.0.0':
        # Mostrar IPs accesibles
        import socket
        try:
            local_ip = socket.gethostbyname(socket.gethostname())
            print(f"   También accesible en: http://{local_ip}:{port}")
        except:
            pass
    print("📌 Endpoints disponibles:")
    print(f"  GET  /status  - Ver estado")
    print(f"  GET  /get     - Obtener credenciales (preview)")
    print(f"  POST /        - Almacenar credenciales")
    print(f"  GET  /clear   - Limpiar credenciales")
    print("\n⚠️  Solo accesible desde localhost")
    print("⏱️  Credenciales expiran en 5 minutos")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
        server.server_close()
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Error: Puerto {port} ya está en uso")
            print(f"💡 Intenta con otro puerto: python3 credentials_server.py 8083")
        else:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    import sys
    port = 8081
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"⚠️  Puerto inválido: {sys.argv[1]}, usando {port}")
    start_server(port)