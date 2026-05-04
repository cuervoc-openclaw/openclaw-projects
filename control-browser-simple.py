#!/usr/bin/env python3
"""
Script para controlar OpenClaw Browser via WebDriver
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

print("🚀 CONTROLANDO OPENCLAW BROWSER")
print("=" * 40)

# Configurar Chrome para conectar al navegador remoto
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "localhost:3000")

try:
    print("1. 🔗 Conectando al navegador en localhost:3000...")
    
    # Intentar conectar al Chrome remoto
    driver = webdriver.Chrome(options=chrome_options)
    
    print("✅ Conectado exitosamente!")
    print("🌐 Abre http://localhost:3000 para ver en vivo")
    
    # Paso 1: Ir a Google
    print("\n2. 🔍 Navegando a Google...")
    driver.get("https://www.google.com")
    time.sleep(3)  # Esperar para que cargue
    
    print("✅ Google cargado")
    print("👀 Deberías ver Google en http://localhost:3000")
    
    # Paso 2: Buscar algo
    print("\n3. 🔍 Buscando 'OpenClaw'...")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("OpenClaw")
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)
    
    print("✅ Búsqueda completada")
    
    # Paso 3: Mostrar información
    print(f"\n4. 📄 Título actual: {driver.title}")
    print(f"   🔗 URL actual: {driver.current_url}")
    
    # Paso 4: Ir a GitHub
    print("\n5. 🐙 Navegando a GitHub OpenClaw...")
    driver.get("https://github.com/openclaw/openclaw")
    time.sleep(3)
    
    print("✅ GitHub cargado")
    
    print("\n" + "=" * 40)
    print("🎉 ¡NAVEGACIÓN COMPLETADA!")
    print("=" * 40)
    print("\n👀 Ahora en http://localhost:3000 deberías ver:")
    print("   1. Google")
    print("   2. Resultados de búsqueda 'OpenClaw'")
    print("   3. GitHub de OpenClaw")
    print("\n⏳ Manteniendo navegador abierto por 60 segundos...")
    print("   (Abre http://localhost:3000 ahora para ver)")
    
    time.sleep(60)  # Mantener abierto 60 segundos
    
    print("\n🔒 Cerrando conexión...")
    driver.quit()
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Posibles soluciones:")
    print("   1. OpenClaw Browser necesita estar en modo 'debug'")
    print("   2. El puerto 3000 podría no ser para WebDriver")
    print("   3. Podría necesitar configuración especial")
    
    print("\n🔍 Verificando qué hay en http://localhost:3000...")
    import requests
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        print(f"   HTTP {response.status_code}")
        if "html" in response.text[:100].lower():
            print("   ✅ Hay HTML (probablemente streaming UI)")
            print("   👉 Abre http://localhost:3000 manualmente")
        else:
            print("   ❌ No es HTML esperado")
    except:
        print("   ❌ No se puede conectar")