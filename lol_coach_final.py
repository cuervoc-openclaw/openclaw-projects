#!/usr/bin/env python3
"""
LOLLC COACH - Script final para API de Riot Games
Consulta básica de datos de League of Legends
"""

import requests
import json
from datetime import datetime

# Configuración
API_KEY = "RGAPI-cac59e60-e6be-4f24-80bd-03052ab4b3d9"
RIOT_ID_NAME = "msf cuervoc"
RIOT_ID_TAG = "LAS"
REGION = "la2"  # LAS = la2 (Latinoamérica Sur 2)

headers = {"X-Riot-Token": API_KEY}

def print_header(text):
    """Imprimir encabezado formateado"""
    print("\n" + "=" * 60)
    print(f"📊 {text}")
    print("=" * 60)

def print_success(text):
    """Imprimir mensaje de éxito"""
    print(f"   ✅ {text}")

def print_info(text):
    """Imprimir información"""
    print(f"   ℹ️  {text}")

def print_error(text):
    """Imprimir mensaje de error"""
    print(f"   ❌ {text}")

def get_riot_account():
    """Obtener cuenta por Riot ID"""
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{RIOT_ID_NAME}/{RIOT_ID_TAG}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print_error(f"Error {response.status_code}: {response.text[:100]}")
            return None
    except Exception as e:
        print_error(f"Conexión fallida: {e}")
        return None

def get_summoner_by_puuid(puuid):
    """Obtener summoner por PUUID"""
    url = f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print_error(f"Error {response.status_code} al obtener summoner")
            return None
    except Exception as e:
        print_error(f"Conexión fallida: {e}")
        return None

def get_ranked_info(summoner_id):
    """Obtener información de ranked"""
    url = f"https://{REGION}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return []  # Puede estar unranked
    except:
        return []

def get_match_history(puuid, count=3):
    """Obtener historial de partidas (limitado para no exceder rate limit)"""
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    params = {"start": 0, "count": count}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print_error(f"Error {response.status_code} al obtener historial")
            return []
    except:
        return []

def get_match_details(match_id):
    """Obtener detalles de una partida"""
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

def analyze_match_for_player(match_data, puuid):
    """Analizar partida para jugador específico"""
    for participant in match_data.get('info', {}).get('participants', []):
        if participant.get('puuid') == puuid:
            return participant
    return None

def calculate_kda(kills, deaths, assists):
    """Calcular ratio KDA"""
    if deaths == 0:
        return kills + assists
    return (kills + assists) / deaths

def main():
    print_header("LOLLC COACH - ANÁLISIS DE CUENTA")
    
    # 1. Obtener cuenta Riot
    print(f"\n🔍 Buscando: {RIOT_ID_NAME}#{RIOT_ID_TAG}")
    account = get_riot_account()
    
    if not account:
        print_error("No se pudo encontrar la cuenta")
        return
    
    puuid = account.get('puuid')
    game_name = account.get('gameName')
    tag_line = account.get('tagLine')
    
    print_success(f"Cuenta encontrada: {game_name}#{tag_line}")
    print_info(f"PUUID: {puuid[:12]}...")
    
    # 2. Obtener información de summoner
    print("\n👤 Obteniendo información del summoner...")
    summoner = get_summoner_by_puuid(puuid)
    
    if not summoner:
        print_error("No se pudo obtener información del summoner")
        return
    
    summoner_id = summoner.get('id')
    summoner_level = summoner.get('summonerLevel', 0)
    profile_icon = summoner.get('profileIconId', 0)
    
    print_success(f"Nivel: {summoner_level}")
    print_success(f"Icono: {profile_icon}")
    
    # 3. Obtener información de ranked
    print("\n🏆 Información de Ranked:")
    ranked_info = get_ranked_info(summoner_id)
    
    if ranked_info:
        for queue in ranked_info:
            queue_type = queue.get('queueType', '')
            tier = queue.get('tier', 'UNRANKED')
            rank = queue.get('rank', '')
            lp = queue.get('leaguePoints', 0)
            wins = queue.get('wins', 0)
            losses = queue.get('losses', 0)
            
            # Traducir tipo de cola
            if queue_type == "RANKED_SOLO_5x5":
                queue_name = "Solo/Duo"
            elif queue_type == "RANKED_FLEX_SR":
                queue_name = "Flexible"
            else:
                queue_name = queue_type.replace('_', ' ').title()
            
            # Calcular winrate
            total_games = wins + losses
            winrate = (wins / total_games * 100) if total_games > 0 else 0
            
            print(f"   📈 {queue_name}:")
            print(f"      • Tier: {tier} {rank}")
            print(f"      • LP: {lp}")
            print(f"      • Record: {wins}W - {losses}L")
            print(f"      • Winrate: {winrate:.1f}%")
    else:
        print_info("No hay información de ranked (posiblemente unranked)")
    
    # 4. Obtener últimas partidas
    print("\n🎮 Últimas partidas:")
    match_ids = get_match_history(puuid, 3)
    
    if match_ids:
        for i, match_id in enumerate(match_ids, 1):
            print(f"\n   Partida {i}:")
            match_data = get_match_details(match_id)
            
            if match_data:
                player_data = analyze_match_for_player(match_data, puuid)
                
                if player_data:
                    champion = player_data.get('championName', 'Desconocido')
                    kills = player_data.get('kills', 0)
                    deaths = player_data.get('deaths', 0)
                    assists = player_data.get('assists', 0)
                    cs = player_data.get('totalMinionsKilled', 0)
                    gold = player_data.get('goldEarned', 0)
                    win = player_data.get('win', False)
                    
                    # Calcular CS/min
                    game_duration = match_data['info']['gameDuration'] / 60  # minutos
                    cs_per_min = cs / game_duration if game_duration > 0 else 0
                    
                    # Calcular KDA
                    kda_ratio = calculate_kda(kills, deaths, assists)
                    
                    print(f"      • Campeón: {champion}")
                    print(f"      • KDA: {kills}/{deaths}/{assists} (Ratio: {kda_ratio:.2f})")
                    print(f"      • CS: {cs} ({cs_per_min:.1f}/min)")
                    print(f"      • Oro: {gold:,}")
                    print(f"      • Resultado: {'✅ VICTORIA' if win else '❌ DERROTA'}")
                    print(f"      • Duración: {int(game_duration)}:{int((game_duration % 1) * 60):02d}")
                else:
                    print_error("No se pudo encontrar datos del jugador en la partida")
            else:
                print_error("No se pudieron obtener detalles de la partida")
    else:
        print_info("No se encontraron partidas recientes")
    
    # 5. Recomendaciones básicas
    print_header("🎯 RECOMENDACIONES INICIALES")
    
    print("\n1. **Farmeo (CS):**")
    print("   • Objetivo: 7-8 CS/min en línea")
    print("   • Practica last hitting en custom games")
    print("   • Mejora gestión de waves")
    
    print("\n2. **Map Awareness:**")
    print("   • Mira el minimapa cada 5-10 segundos")
    print("   • Usa pings para comunicarte")
    print("   • Trackea al jungler enemigo")
    
    print("\n3. **Visión:**")
    print("   • Compra 2 wards cada back")
    print("   • Controla objetivos con visión")
    print("   • Barre wards enemigos")
    
    print("\n4. **Siguientes pasos:**")
    print("   • Graba 2-3 partidas para análisis")
    print("   • Enfócate en 2-3 campeones máximo")
    print("   • Establece objetivos semanales")
    
    print_header("📊 RESUMEN DE CONSULTAS")
    print("\n✅ API funcionando correctamente")
    print(f"✅ Cuenta: {game_name}#{tag_line}")
    print(f"✅ Nivel: {summoner_level}")
    print(f"✅ Partidas analizadas: {len(match_ids)}")
    print("\n⚠️  **Rate Limit:** 20 req/min, 100 req/2min")
    print("   Consultas usadas: ~6-8")

if __name__ == "__main__":
    main()