import sys
sys.path.insert(0, '.')

# Parchear el handler para agregar headers CORS
import credentials_server

original_send = credentials_server.CredentialsHandler._send_response

def patched_send(self, code, data):
    self.send_response(code)
    self.send_header('Content-Type', 'application/json')
    self.send_header('Access-Control-Allow-Origin', '*')
    self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    self.end_headers()
    self.wfile.write(json.dumps(data).encode('utf-8'))

credentials_server.CredentialsHandler._send_response = patched_send

# Agregar handler OPTIONS para CORS preflight
original_do_OPTIONS = credentials_server.CredentialsHandler.do_OPTIONS if hasattr(credentials_server.CredentialsHandler, 'do_OPTIONS') else None

def do_OPTIONS(self):
    self.send_response(200)
    self.send_header('Access-Control-Allow-Origin', '*')
    self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    self.end_headers()

credentials_server.CredentialsHandler.do_OPTIONS = do_OPTIONS

print("✅ CORS configurado")
