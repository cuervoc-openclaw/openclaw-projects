#!/usr/bin/env python3
"""
Script de prueba simple para API de Riot
"""

import requests
import json

API_KEY = "RGAPI-cac59e60-e6be-4f24-80bd-03052ab4b3d9"
headers = {"X-Riot-Token": API_KEY}

print("Probando conexión con API de Riot...")

# Probar endpoint de América (debería funcionar para todas las regiones)
test_url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/cuervoc/LAS"

try:
    print(f"Consultando: {test_url}")
    response = requests.get(test_url, headers=headers, timeout=10)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ ¡Conexión exitosa!")
        print(f"Riot ID encontrado: {data.get('gameName', 'N/A')}#{data.get('tagLine', 'N/A')}")
        print(f"PUUID: {data.get('puuid', 'N/A')}")
    elif response.status_code == 403:
        print("❌ Error 403: API Key inválida o expirada")
        print("Posibles causas:")
        print("1. La API Key ha expirado (duran 24 horas por defecto)")
        print("2. La API Key no está activada para desarrollo")
        print("3. Límite de rate excedido")
    elif response.status_code == 404:
        print("❌ Error 404: Riot ID no encontrado")
    else:
        print(f"❌ Error {response.status_code}: {response.text[:200]}")
        
except requests.exceptions.RequestException as e:
    print(f"❌ Error de conexión: {e}")
    print("\nPosibles soluciones:")
    print("1. Verifica tu conexión a internet")
    print("2. La API Key podría haber expirado (genera una nueva)")
    print("3. Espera 1-2 minutos si excediste rate limit")