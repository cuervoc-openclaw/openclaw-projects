#!/usr/bin/env python3
"""
Servidor simple para ver TDAH Dashboard localmente
"""

import http.server
import socketserver
import os
import webbrowser

# Configuración
PORT = 8082
DIRECTORIO = "/home/cuervoc/.openclaw/workspace/TDAH-DASHBOARD/dist"

print("🚀 INICIANDO SERVIDOR TDAH DASHBOARD")
print("=" * 40)

# Verificar que existe el directorio
if not os.path.exists(DIRECTORIO):
    print(f"❌ Error: No existe el directorio {DIRECTORIO}")
    exit(1)

if not os.path.exists(os.path.join(DIRECTORIO, "index.html")):
    print("❌ Error: No existe index.html en el directorio")
    exit(1)

print(f"📁 Directorio: {DIRECTORIO}")
print(f"🌐 Puerto: {PORT}")
print(f"🔗 URL: http://localhost:{PORT}")

# Cambiar al directorio
os.chdir(DIRECTORIO)

# Configurar handler
handler = http.server.SimpleHTTPRequestHandler

# Intentar iniciar servidor
try:
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"\n✅ Servidor iniciado en http://localhost:{PORT}")
        print("📱 Abriendo en navegador...")
        
        # Abrir en navegador
        webbrowser.open(f"http://localhost:{PORT}")
        
        print("\n🎯 TDAH DASHBOARD CARGANDO...")
        print("=" * 40)
        print("\n👀 Deberías ver en tu navegador:")
        print("   • Interfaz minimalista para TDAH")
        print("   • Temporizador Pomodoro")
        print("   • Sistema de tareas")
        print("   • Registro de hábitos")
        
        print("\n🛑 Para detener el servidor: Presiona Ctrl+C")
        print("💡 Mantén esta terminal abierta mientras usas el dashboard")
        
        # Mantener servidor corriendo
        httpd.serve_forever()
        
except OSError as e:
    if "Address already in use" in str(e):
        print(f"\n⚠️  El puerto {PORT} ya está en uso")
        print("💡 Prueba con otra URL:")
        print(f"   http://localhost:{PORT} (puede que ya esté corriendo)")
    else:
        print(f"\n❌ Error: {e}")
        
except KeyboardInterrupt:
    print("\n\n🛑 Servidor detenido")
    
except Exception as e:
    print(f"\n❌ Error inesperado: {e}")