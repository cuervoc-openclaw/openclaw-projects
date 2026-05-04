#!/usr/bin/env python3
"""
Script básico para consultar la API de Riot Games
Nivel 1 - Consultas manuales
"""

import os
import requests
import json
from datetime import datetime

# Configuración
RIOT_API_KEY = "RGAPI-cac59e60-e6be-4f24-80bd-03052ab4b3d9"
REGION = "las1"  # Latinoamérica Sur
SUMMONER_NAME = "cuervoc"
SUMMONER_TAG = "LAS"

# Headers para la API
headers = {
    "X-Riot-Token": RIOT_API_KEY,
    "User-Agent": "LoLCoach/1.0"
}

def get_summoner_by_riot_id(name, tag):
    """Obtener información de invocador por Riot ID"""
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener Riot ID: {e}")
        if hasattr(e.response, 'status_code'):
            print(f"Código de error: {e.response.status_code}")
            print(f"Respuesta: {e.response.text}")
        return None

def get_summoner_by_puuid(puuid):
    """Obtener información de invocador por PUUID"""
    url = f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener summoner: {e}")
        return None

def get_match_history(puuid, count=5):
    """Obtener historial de partidas"""
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    params = {
        "start": 0,
        "count": count
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener historial: {e}")
        return None

def get_match_details(match_id):
    """Obtener detalles de una partida específica"""
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener partida {match_id}: {e}")
        return None

def get_league_entries(summoner_id):
    """Obtener información de ranked"""
    url = f"https://{REGION}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener ranked: {e}")
        return None

def analyze_match_for_summoner(match_data, puuid):
    """Analizar una partida para un jugador específico"""
    # Encontrar al jugador en la partida
    for participant in match_data.get('info', {}).get('participants', []):
        if participant.get('puuid') == puuid:
            return participant
    return None

def format_time(timestamp):
    """Formatear timestamp a fecha legible"""
    if timestamp:
        dt = datetime.fromtimestamp(timestamp / 1000)
        return dt.strftime("%Y-%m-%d %H:%M")
    return "N/A"

def main():
    print("=" * 60)
    print("LOLLC COACH - CONSULTA BÁSICA DE API")
    print("=" * 60)
    
    # 1. Obtener Riot ID
    print(f"\n1. Buscando Riot ID: {SUMMONER_NAME}#{SUMMONER_TAG}")
    riot_account = get_summoner_by_riot_id(SUMMONER_NAME, SUMMONER_TAG)
    
    if not riot_account:
        print("❌ No se pudo encontrar el Riot ID")
        return
    
    puuid = riot_account.get('puuid')
    game_name = riot_account.get('gameName')
    tag_line = riot_account.get('tagLine')
    
    print(f"   ✅ Encontrado: {game_name}#{tag_line}")
    print(f"   PUUID: {puuid[:8]}...")
    
    # 2. Obtener información de summoner
    print(f"\n2. Obteniendo información de summoner...")
    summoner = get_summoner_by_puuid(puuid)
    
    if not summoner:
        print("❌ No se pudo obtener información del summoner")
        return
    
    summoner_id = summoner.get('id')
    summoner_level = summoner.get('summonerLevel')
    profile_icon = summoner.get('profileIconId')
    
    print(f"   ✅ Nivel: {summoner_level}")
    print(f"   ✅ Icono de perfil: {profile_icon}")
    print(f"   ✅ Última actualización: {format_time(summoner.get('revisionDate'))}")
    
    # 3. Obtener información de ranked
    print(f"\n3. Obteniendo información de ranked...")
    league_entries = get_league_entries(summoner_id)
    
    if league_entries:
        for entry in league_entries:
            queue_type = entry.get('queueType', 'Desconocido')
            tier = entry.get('tier', 'Unranked')
            rank = entry.get('rank', '')
            lp = entry.get('leaguePoints', 0)
            wins = entry.get('wins', 0)
            losses = entry.get('losses', 0)
            winrate = (wins / (wins + losses)) * 100 if (wins + losses) > 0 else 0
            
            print(f"   📊 {queue_type.replace('_', ' ').title()}:")
            print(f"      Tier: {tier} {rank}")
            print(f"      LP: {lp}")
            print(f"      Record: {wins}W - {losses}L")
            print(f"      Winrate: {winrate:.1f}%")
    else:
        print("   ℹ️  No hay información de ranked disponible")
    
    # 4. Obtener historial de partidas
    print(f"\n4. Obteniendo últimas 5 partidas...")
    match_ids = get_match_history(puuid, 5)
    
    if match_ids:
        print(f"   ✅ Partidas encontradas: {len(match_ids)}")
        
        for i, match_id in enumerate(match_ids[:3], 1):  # Solo analizar 3 para no exceder rate limit
            print(f"\n   🎮 Partida {i}: {match_id[:8]}...")
            match_data = get_match_details(match_id)
            
            if match_data:
                participant = analyze_match_for_summoner(match_data, puuid)
                
                if participant:
                    champion = participant.get('championName', 'Desconocido')
                    kills = participant.get('kills', 0)
                    deaths = participant.get('deaths', 0)
                    assists = participant.get('assists', 0)
                    cs = participant.get('totalMinionsKilled', 0)
                    cs_per_min = cs / (match_data['info']['gameDuration'] / 60) if match_data['info']['gameDuration'] > 0 else 0
                    win = participant.get('win', False)
                    
                    print(f"      Campeón: {champion}")
                    print(f"      KDA: {kills}/{deaths}/{assists}")
                    print(f"      CS: {cs} ({cs_per_min:.1f}/min)")
                    print(f"      Resultado: {'✅ Victoria' if win else '❌ Derrota'}")
                    print(f"      Duración: {match_data['info']['gameDuration'] // 60}:{match_data['info']['gameDuration'] % 60:02d}")
    else:
        print("   ❌ No se pudo obtener historial de partidas")
    
    print("\n" + "=" * 60)
    print("CONSULTA COMPLETADA")
    print("=" * 60)
    
    # Mostrar uso de rate limit
    print("\n📊 **Resumen de consultas realizadas:**")
    print("   1. Riot ID")
    print("   2. Summoner info")
    print("   3. League entries")
    print("   4. Match history")
    print("   5-7. Match details (3 partidas)")
    print(f"\n⚠️  **Rate limit:** 20 requests/minuto, 100 requests/2min")
    print("   Consultas usadas: ~7")

if __name__ == "__main__":
    main()