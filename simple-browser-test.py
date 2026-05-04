#!/usr/bin/env python3
"""
Script simple para controlar OpenClaw Browser
"""

import time
import subprocess
import webbrowser

print("🌐 OPENCLAW BROWSER DEMO")
print("=" * 40)

# 1. Verificar que está corriendo
print("1. 🔍 Verificando OpenClaw Browser...")
result = subprocess.run(["docker", "ps", "|", "grep", "openclaw"], 
                       shell=True, capture_output=True, text=True)

if "openclaw-browser" in result.stdout:
    print("   ✅ OpenClaw Browser está corriendo")
    print("   🔗 URL: http://localhost:3000")
else:
    print("   ❌ OpenClaw Browser NO está corriendo")
    print("   💡 Ejecuta: docker start openclaw-browser")
    exit(1)

# 2. Abrir en navegador local
print("\n2. 🚀 Abriendo http://localhost:3000 en tu navegador...")
webbrowser.open("http://localhost:3000")

print("\n3. 📋 Instrucciones:")
print("   - Verás una pantalla en blanco (navegador vacío)")
print("   - El navegador está listo para ser controlado")
print("   - Para controlarlo programáticamente necesitas Puppeteer/Playwright")

print("\n4. 🎯 Ejemplo de control con Puppeteer:")
print("""
   const puppeteer = require('puppeteer');
   
   async function controlBrowser() {
     const browser = await puppeteer.connect({
       browserWSEndpoint: 'ws://localhost:3000'
     });
     
     const page = await browser.newPage();
     await page.goto('https://www.google.com');
     // Ahora verás Google en http://localhost:3000
   }
""")

print("\n5. 🛠️ Comandos útiles:")
print("   - Ver logs: docker logs openclaw-browser")
print("   - Reiniciar: docker restart openclaw-browser")
print("   - Detener: docker stop openclaw-browser")

print("\n" + "=" * 40)
print("👀 Ahora abre http://localhost:3000 para ver el navegador")
print("   (Puede estar en blanco hasta que lo controles programáticamente)")