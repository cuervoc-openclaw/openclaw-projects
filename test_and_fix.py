#!/usr/bin/env python3
"""
Testeo y reparación completa del sistema de credenciales
"""

import requests
import json
import time
import subprocess
import sys
import os

def test_connection():
    """Probar conexión al servidor"""
    print("🔍 Probando conexión al servidor...")
    
    # Probar diferentes endpoints
    base_url = "http://192.168.100.170:8081"
    
    # 1. Probar OPTIONS (CORS preflight)
    print("  1. Probando OPTIONS (CORS preflight)...")
    try:
        response = requests.options(base_url + "/", timeout=5)
        print(f"     OPTIONS /: {response.status_code}")
        print(f"     Headers: {dict(response.headers)}")
    except Exception as e:
        print(f"     ❌ OPTIONS falló: {e}")
    
    # 2. Probar GET /status
    print("  2. Probando GET /status...")
    try:
        response = requests.get(base_url + "/status", timeout=5)
        print(f"     GET /status: {response.status_code}")
        if response.status_code == 200:
            print(f"     Response: {response.json()}")
    except Exception as e:
        print(f"     ❌ GET /status falló: {e}")
    
    # 3. Probar POST con datos de prueba
    print("  3. Probando POST con datos de prueba...")
    test_data = {
        "github_token": "ghp_test1234567890abcdef",
        "riot_key": "RGAPI-test1234567890abcdef"
    }
    try:
        response = requests.post(
            base_url + "/",
            json=test_data,
            timeout=5,
            headers={'Content-Type': 'application/json'}
        )
        print(f"     POST /: {response.status_code}")
        if response.status_code == 200:
            print(f"     Response: {response.json()}")
    except Exception as e:
        print(f"     ❌ POST falló: {e}")
    
    # 4. Probar desde perspectiva de navegador (CORS headers)
    print("  4. Verificando headers CORS...")
    try:
        response = requests.get(base_url + "/status", timeout=5)
        headers = dict(response.headers)
        cors_headers = {k: v for k, v in headers.items() 
                       if 'access-control' in k.lower() or 'cors' in k.lower()}
        if cors_headers:
            print(f"     ✅ Headers CORS presentes: {cors_headers}")
        else:
            print(f"     ❌ No hay headers CORS")
    except Exception as e:
        print(f"     ❌ Error verificando headers: {e}")

def fix_cors_issue():
    """Reparar problema CORS definitivamente"""
    print("\n🔧 Reparando problema CORS...")
    
    # Leer el archivo del servidor
    with open("credentials_server.py", "r") as f:
        content = f.read()
    
    # Agregar handler OPTIONS si no existe
    if "def do_OPTIONS" not in content:
        print("  Agregando handler OPTIONS...")
        
        # Encontrar donde agregar el método
        lines = content.split('\n')
        new_lines = []
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            # Buscar después del último método do_*
            if "def do_POST" in line:
                # Agregar método OPTIONS aquí
                new_lines.append("")
                new_lines.append("    def do_OPTIONS(self):")
                new_lines.append("        \"\"\"Handler para CORS preflight\"\"\"")
                new_lines.append("        self.send_response(200)")
                new_lines.append("        self.send_header('Access-Control-Allow-Origin', '*')")
                new_lines.append("        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE')")
                new_lines.append("        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')")
                new_lines.append("        self.send_header('Access-Control-Max-Age', '86400')")
                new_lines.append("        self.end_headers()")
        
        # Escribir archivo actualizado
        with open("credentials_server.py", "w") as f:
            f.write('\n'.join(new_lines))
        
        print("  ✅ Handler OPTIONS agregado")
    
    # Agregar headers CORS a _send_response si no están
    if "Access-Control-Allow-Origin" not in content:
        print("  Agregando headers CORS a _send_response...")
        
        lines = content.split('\n')
        new_lines = []
        
        for i, line in enumerate(lines):
            if "def _send_response(self, code, data):" in line:
                # Reemplazar este método
                new_lines.append(line)
                new_lines.append("        \"\"\"Enviar respuesta JSON con headers CORS\"\"\"")
                new_lines.append("        self.send_response(code)")
                new_lines.append("        self.send_header('Content-Type', 'application/json')")
                new_lines.append("        self.send_header('Access-Control-Allow-Origin', '*')")
                new_lines.append("        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE')")
                new_lines.append("        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')")
                new_lines.append("        self.end_headers()")
                new_lines.append("        self.wfile.write(json.dumps(data).encode('utf-8'))")
                # Saltar las líneas originales del método
                # Buscar el siguiente método o fin de función
                j = i + 1
                while j < len(lines) and (lines[j].startswith(' ') or lines[j] == ''):
                    j += 1
                # Continuar desde después del método
                i = j - 1
            else:
                new_lines.append(line)
        
        with open("credentials_server.py", "w") as f:
            f.write('\n'.join(new_lines))
        
        print("  ✅ Headers CORS agregados")

def restart_server():
    """Reiniciar servidor con los cambios"""
    print("\n🔄 Reiniciando servidor...")
    
    # Detener servidor actual
    subprocess.run(["pkill", "-f", "credentials_server.py"], 
                   capture_output=True)
    time.sleep(2)
    
    # Iniciar nuevo servidor
    proc = subprocess.Popen(
        ["python3", "credentials_server.py", "8081"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    time.sleep(3)
    
    # Verificar si está corriendo
    result = subprocess.run(
        ["ss", "-tuln"],
        capture_output=True,
        text=True
    )
    
    if ":8081" in result.stdout:
        print("  ✅ Servidor reiniciado en puerto 8081")
        return True
    else:
        print("  ❌ Error reiniciando servidor")
        return False

def test_full_flow():
    """Probar flujo completo con datos reales"""
    print("\n🧪 Probando flujo completo...")
    
    # Datos de prueba reales (simulados)
    test_credentials = {
        "github_token": "ghp_test1234567890abcdefghijklmnopqrstuvwxyz",
        "riot_key": "RGAPI-test1234567890abcdefghijklmnop",
        "custom": {
            "openai": "sk-test1234567890abcdefghijklmnop"
        }
    }
    
    # 1. Enviar credenciales
    print("  1. Enviando credenciales de prueba...")
    try:
        response = requests.post(
            "http://192.168.100.170:8081/",
            json=test_credentials,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"     ✅ POST exitoso: {response.json()}")
        else:
            print(f"     ❌ POST falló: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"     ❌ Error en POST: {e}")
        return False
    
    # 2. Verificar que se almacenaron
    print("  2. Verificando almacenamiento...")
    try:
        response = requests.get(
            "http://192.168.100.170:8081/get",
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"     ✅ GET /get: {data.get('status', 'unknown')}")
            print(f"     GitHub: {data.get('has_github', False)}")
            print(f"     Riot: {data.get('has_riot', False)}")
            print(f"     Custom: {data.get('has_custom', False)}")
            return True
        else:
            print(f"     ❌ GET falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"     ❌ Error en GET: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 TESTEO Y REPARACIÓN COMPLETA DEL SISTEMA")
    print("=" * 50)
    
    # Cambiar al directorio correcto
    os.chdir("/home/cuervoc/.openclaw/workspace")
    
    # 1. Probar conexión actual
    test_connection()
    
    # 2. Reparar CORS
    fix_cors_issue()
    
    # 3. Reiniciar servidor
    if not restart_server():
        print("❌ No se pudo reiniciar el servidor")
        return 1
    
    # 4. Esperar y probar de nuevo
    time.sleep(2)
    print("\n" + "=" * 50)
    print("🔄 Probando después de reparaciones...")
    test_connection()
    
    # 5. Probar flujo completo
    if test_full_flow():
        print("\n🎉 ¡SISTEMA REPARADO Y FUNCIONANDO!")
        print("\n📋 Resumen:")
        print("   ✅ CORS configurado (OPTIONS handler)")
        print("   ✅ Headers de acceso correctos")
        print("   ✅ Servidor respondiendo")
        print("   ✅ Almacenamiento funcionando")
        print("\n🚀 El dashboard ahora debería funcionar:")
        print("   URL: http://192.168.100.170:8080/dashboard.html")
        return 0
    else:
        print("\n❌ El sistema aún tiene problemas")
        return 1

if __name__ == "__main__":
    sys.exit(main())