#!/usr/bin/env python3
"""
Script para buscar productos específicos en farmaloop.cl
y generar un archivo Excel con los resultados.
"""

import requests
import json
import csv
import re
from datetime import datetime
import time

# Lista de productos a buscar (basado en lo que envió el usuario)
productos_a_buscar = [
    # Ozempic
    {"nombre": "ozempic", "compuesto": "semaglutida", "cantidad": 14},
    # Saxenda
    {"nombre": "saxenda", "compuesto": "liraglutida", "cantidad": 8},
    # Victoza
    {"nombre": "victoza", "compuesto": "liraglutida", "cantidad": 8},
    # Rybelsus
    {"nombre": "rybelsus", "compuesto": "semaglutida", "cantidad": 9},
    # Omnitrope
    {"nombre": "omnitrope", "compuesto": "somatropina", "cantidad": 12},
    # Decapeptyl
    {"nombre": "decapeptyl", "compuesto": "triptorelina", "cantidad": 10},
    # Diphereline
    {"nombre": "diphereline", "compuesto": "triptorelina", "cantidad": 9},
    # Elonva
    {"nombre": "elonva", "compuesto": "corifolitropina alfa", "cantidad": 7},
    # Puregon
    {"nombre": "puregon", "compuesto": "folitropina", "cantidad": 9},
    # Gonal
    {"nombre": "gonal", "compuesto": "folitropina alfa", "cantidad": 8},
    # Menopur
    {"nombre": "menopur", "compuesto": "menotropina", "cantidad": 11},
    # Pergoveris
    {"nombre": "pergoveris", "compuesto": "folitropina alfa, lutropina", "cantidad": 10},
    # Bemfola
    {"nombre": "bemfola", "compuesto": "folitropina alfa", "cantidad": 9},
    # Orgalutran
    {"nombre": "orgalutran", "compuesto": "ganirelix", "cantidad": 6},
    # Rekovelle
    {"nombre": "rekovelle", "compuesto": "folitropina delta", "cantidad": 9},
    # Gonapeptyl
    {"nombre": "gonapeptyl", "compuesto": "triptorelina", "cantidad": 9},
    # Progendo
    {"nombre": "progendo", "compuesto": "progesterona", "cantidad": 8},
    # Pregabalina
    {"nombre": "pregabalina", "compuesto": "pregabalina", "cantidad": 14},
    # Prestat
    {"nombre": "prestat", "compuesto": "pregabalina", "cantidad": 4},
    # Sertralina
    {"nombre": "sertralina", "compuesto": "sertralina", "cantidad": 7},
    # Clotiazepam
    {"nombre": "clotiazepam", "compuesto": "clotiazepam", "cantidad": 7},
    # Clonazepam
    {"nombre": "clonazepam", "compuesto": "clonazepam", "cantidad": 23},
    # Zolpidem
    {"nombre": "zolpidem", "compuesto": "zolpidem", "cantidad": 16},
    # Zopiclona
    {"nombre": "zopiclona", "compuesto": "zopiclona", "cantidad": 13},
    # Eszopiclona
    {"nombre": "eszopiclona", "compuesto": "eszopiclona", "cantidad": 15},
    # Desvenlafaxina
    {"nombre": "desvenlafaxina", "compuesto": "desvenlafaxina", "cantidad": 17},
    # Escitalopram
    {"nombre": "escitalopram", "compuesto": "escitalopram", "cantidad": 18},
    # Galvus
    {"nombre": "galvus", "compuesto": "vildagliptina", "cantidad": 11},
    # Jardiance
    {"nombre": "jardiance", "compuesto": "empagliflozina", "cantidad": 11},
    # Janumet
    {"nombre": "janumet", "compuesto": "sitagliptina, metformina", "cantidad": 10},
]

def buscar_producto(producto_nombre):
    """Busca un producto en farmaloop.cl usando su API de búsqueda."""
    base_url = "https://www.farmaloop.cl"
    search_url = f"{base_url}/api/search"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Referer': base_url
    }
    
    params = {
        'q': producto_nombre,
        'limit': 50
    }
    
    try:
        print(f"🔍 Buscando: {producto_nombre}")
        response = requests.get(search_url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('products', [])
        else:
            print(f"   ❌ Error HTTP {response.status_code}")
            return []
            
    except Exception as e:
        print(f"   ❌ Error en búsqueda: {e}")
        return []

def extraer_sku_de_url(url):
    """Extrae el SKU de la URL del producto."""
    if not url:
        return ""
    
    # Buscar patrones comunes de SKU en URLs
    patterns = [
        r'/(\d{5,})/?$',  # SKU de 5+ dígitos al final
        r'sku=(\d+)',     # parámetro sku=
        r'/(\d+)-',       # dígitos antes de un guión
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return ""

def procesar_productos():
    """Procesa todos los productos y genera resultados."""
    print("🚀 INICIANDO BÚSQUEDA DE PRODUCTOS EN FARMALOOP.CL")
    print("=" * 60)
    
    resultados = []
    
    for producto_info in productos_a_buscar:
        nombre = producto_info["nombre"]
        compuesto = producto_info["compuesto"]
        cantidad = producto_info["cantidad"]
        
        productos_encontrados = buscar_producto(nombre)
        
        if productos_encontrados:
            print(f"   ✅ Encontrados {len(productos_encontrados)} productos para '{nombre}'")
            
            for i, producto in enumerate(productos_encontrados[:cantidad], 1):
                # Extraer información del producto
                producto_nombre = producto.get('name', '')
                producto_url = f"https://www.farmaloop.cl{producto.get('url', '')}"
                sku = extraer_sku_de_url(producto_url)
                
                # Buscar precio
                precio = producto.get('price', '')
                if not precio and 'variants' in producto:
                    for variant in producto['variants']:
                        if 'price' in variant:
                            precio = variant['price']
                            break
                
                # Buscar stock
                stock = producto.get('stock', '')
                if not stock and 'variants' in producto:
                    for variant in producto['variants']:
                        if 'stock' in variant:
                            stock = variant['stock']
                            break
                
                resultados.append({
                    'Nombre Producto': producto_nombre,
                    'Compuesto': compuesto,
                    'URL': producto_url,
                    'SKU': sku,
                    'Precio': precio,
                    'Stock': stock,
                    'Categoría': producto.get('category', ''),
                    'Marca': producto.get('brand', '')
                })
                
                # Pausa para no sobrecargar el servidor
                time.sleep(0.1)
        else:
            print(f"   ⚠️  No se encontraron productos para '{nombre}'")
            
            # Agregar fila vacía para mantener el formato
            for i in range(cantidad):
                resultados.append({
                    'Nombre Producto': f"{nombre} (no encontrado)",
                    'Compuesto': compuesto,
                    'URL': '',
                    'SKU': '',
                    'Precio': '',
                    'Stock': '',
                    'Categoría': '',
                    'Marca': ''
                })
        
        # Pausa entre búsquedas
        time.sleep(0.5)
    
    return resultados

def guardar_csv(resultados):
    """Guarda los resultados en un archivo CSV."""
    if not resultados:
        print("❌ No hay resultados para guardar")
        return
    
    filename = f"productos_farmaloop_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    campos = ['Nombre Producto', 'Compuesto', 'URL', 'SKU', 'Precio', 'Stock', 'Categoría', 'Marca']
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=campos)
        writer.writeheader()
        
        for resultado in resultados:
            writer.writerow(resultado)
    
    print(f"\n💾 Resultados guardados en: {filename}")
    print(f"📊 Total de registros: {len(resultados)}")
    
    return filename

def generar_resumen(resultados):
    """Genera un resumen de los resultados."""
    print("\n📈 RESUMEN DE BÚSQUEDA:")
    print("-" * 40)
    
    productos_encontrados = [r for r in resultados if r['URL']]
    productos_no_encontrados = [r for r in resultados if not r['URL']]
    
    print(f"✅ Productos encontrados: {len(productos_encontrados)}")
    print(f"❌ Productos no encontrados: {len(productos_no_encontrados)}")
    print(f"📋 Total de búsquedas realizadas: {len(resultados)}")
    
    # Agrupar por categoría de producto
    categorias = {}
    for resultado in productos_encontrados:
        cat = resultado['Categoría'] or 'Sin categoría'
        categorias[cat] = categorias.get(cat, 0) + 1
    
    if categorias:
        print("\n🏷️  Distribución por categoría:")
        for categoria, cantidad in sorted(categorias.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {categoria}: {cantidad} productos")

def main():
    """Función principal."""
    print("🌐 BUSCADOR DE PRODUCTOS FARMALOOP.CL")
    print("=" * 60)
    
    # Procesar productos
    resultados = procesar_productos()
    
    # Guardar resultados
    if resultados:
        archivo_csv = guardar_csv(resultados)
        generar_resumen(resultados)
        
        print(f"\n🎯 INSTRUCCIONES:")
        print(f"   1. El archivo '{archivo_csv}' contiene todos los resultados")
        print(f"   2. Puedes abrirlo con Excel o Google Sheets")
        print(f"   3. Columnas incluidas: Nombre, Compuesto, URL, SKU, Precio, Stock")
        print(f"\n⚠️  NOTA: Algunos productos pueden no estar disponibles en farmaloop.cl")
    else:
        print("❌ No se encontraron productos")

if __name__ == "__main__":
    main()