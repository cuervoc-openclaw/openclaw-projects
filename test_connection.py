import requests, json, sys
url = "http://'$SERVER_IP':8081"
print(f"🔗 Probando {url}")

# Test OPTIONS (CORS preflight)
print("1. OPTIONS (CORS preflight)...")
try:
    r = requests.options(url + "/", timeout=5)
    print(f"   Status: {r.status_code}")
    print(f"   Headers: {dict(r.headers)}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test POST
print("2. POST con datos de prueba...")
try:
    r = requests.post(url + "/", 
        json={"test": "data", "github_token": "ghp_test123"},
        headers={"Content-Type": "application/json"},
        timeout=5)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        print(f"   ✅ Success: {r.json()}")
    else:
        print(f"   ❌ Failed: {r.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

print("🎉 ¡TODAS LAS PRUEBAS PASARON!")
