#!/usr/bin/env python3
"""
Servidor de credenciales CON CORS COMPLETAMENTE FUNCIONAL
"""

import json
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sys

# Almacenamiento temporal en memoria
credentials_store = {
    "github_token": None,
    "riot_key": None,
    "custom_credentials": {},
    "last_updated": None
}

store_lock = threading.Lock()

class FixedCredentialsHandler(BaseHTTPRequestHandler):
    """Handler con CORS completamente funcional"""
    
    def _set_cors_headers(self):
        """Configurar headers CORS para todas las respuestas"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
        self.send_header('Access-Control-Max-Age', '86400')
    
    def do_OPTIONS(self):
        """Handler para CORS preflight - REQUERIDO por navegadores"""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """Endpoint GET"""
        parsed = urlparse(self.path)
        
        if parsed.path == '/status':
            with store_lock:
                data = {
                    'status': 'ok',
                    'store_active': bool(credentials_store['last_updated']),
                    'expired': (credentials_store['last_updated'] and 
                               time.time() - credentials_store['last_updated'] > 300)
                }
                self._send_json(200, data)
                
        elif parsed.path == '/get':
            with store_lock:
                if (credentials_store['last_updated'] and 
                    time.time() - credentials_store['last_updated'] > 300):
                    self._send_json(200, {'status': 'expired'})
                    return
                
                response = {
                    'status': 'ok',
                    'has_github': bool(credentials_store['github_token']),
                    'has_riot': bool(credentials_store['riot_key']),
                    'has_custom': len(credentials_store['custom_credentials']) > 0,
                    'last_updated': credentials_store['last_updated']
                }
                
                if credentials_store['github_token']:
                    token = credentials_store['github_token']
                    response['github_preview'] = f"{token[:10]}...{token[-4:]}"
                
                if credentials_store['riot_key']:
                    key = credentials_store['riot_key']
                    response['riot_preview'] = f"{key[:10]}...{key[-4:]}"
                
                self._send_json(200, response)
                
        elif parsed.path == '/clear':
            with store_lock:
                credentials_store.update({
                    'github_token': None,
                    'riot_key': None,
                    'custom_credentials': {},
                    'last_updated': None
                })
                self._send_json(200, {'status': 'cleared'})
                
        else:
            self._send_json(404, {'error': 'Not found'})
    
    def do_POST(self):
        """Endpoint POST para almacenar credenciales"""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            self._send_json(400, {'error': 'No data'})
            return
        
        try:
            data = json.loads(self.rfile.read(content_length).decode('utf-8'))
        except:
            self._send_json(400, {'error': 'Invalid JSON'})
            return
        
        with store_lock:
            if 'github_token' in data:
                credentials_store['github_token'] = data['github_token']
            
            if 'riot_key' in data:
                credentials_store['riot_key'] = data['riot_key']
            
            if 'custom' in data:
                for name, key in data['custom'].items():
                    credentials_store['custom_credentials'][name] = key
            
            credentials_store['last_updated'] = time.time()
            
            self._send_json(200, {
                'status': 'stored',
                'received': {
                    'github': 'github_token' in data,
                    'riot': 'riot_key' in data,
                    'custom': len(data.get('custom', {}))
                }
            })
    
    def _send_json(self, code, data):
        """Enviar respuesta JSON con CORS"""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Silenciar logs normales"""
        pass

def get_github_token():
    """Obtener token GitHub"""
    with store_lock:
        if (credentials_store['github_token'] and 
            credentials_store['last_updated'] and
            time.time() - credentials_store['last_updated'] <= 300):
            return credentials_store['github_token']
    return None

def get_riot_key():
    """Obtener key Riot"""
    with store_lock:
        if (credentials_store['riot_key'] and 
            credentials_store['last_updated'] and
            time.time() - credentials_store['last_updated'] <= 300):
            return credentials_store['riot_key']
    return None

def start_server(port=8081, host='0.0.0.0'):
    """Iniciar servidor"""
    server = HTTPServer((host, port), FixedCredentialsHandler)
    print(f"🔐 Servidor FIXED iniciado en http://{host}:{port}")
    print("📌 Endpoints (con CORS completo):")
    print(f"  OPTIONS /     - CORS preflight")
    print(f"  GET    /status - Estado")
    print(f"  GET    /get    - Credenciales")
    print(f"  POST   /       - Almacenar")
    print(f"  GET    /clear  - Limpiar")
    print("\n✅ CORS completamente funcional")
    print("✅ Listo para navegadores")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
        server.server_close()

if __name__ == '__main__':
    port = 8081
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except:
            pass
    start_server(port)