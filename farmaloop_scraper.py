#!/usr/bin/env python3
"""
Web scraping básico de farmaloop.cl
"""

import requests
from bs4 import BeautifulSoup
import json

def scrape_farmaloop():
    print("🌐 WEB SCRAPING DE FARMALOOP.CL")
    print("=" * 40)
    
    url = "https://www.farmaloop.cl"
    
    try:
        # Headers para simular navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print(f"📥 Conectando a: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        print(f"✅ Conexión exitosa (Status: {response.status_code})")
        
        # Parsear HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraer información básica
        print("\n📊 INFORMACIÓN EXTRAÍDA:")
        print("-" * 30)
        
        # 1. Título
        title = soup.title.string if soup.title else "No encontrado"
        print(f"🔹 Título: {title}")
        
        # 2. Meta descripción
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            print(f"🔹 Descripción: {meta_desc.get('content', 'No encontrada')}")
        
        # 3. Encabezados principales
        print("\n🔹 Encabezados principales:")
        for i, h1 in enumerate(soup.find_all('h1')[:3], 1):
            print(f"   H1-{i}: {h1.get_text(strip=True)}")
        
        # 4. Enlaces de navegación
        print("\n🔹 Enlaces principales (primeros 15):")
        links = []
        for link in soup.find_all('a', href=True)[:15]:
            href = link['href']
            text = link.get_text(strip=True)
            if text and len(text) < 50:  # Filtrar textos muy largos
                links.append({'text': text, 'url': href})
                print(f"   • {text[:40]:40} → {href[:60]}")
        
        # 5. Buscar productos o categorías
        print("\n🔹 Posibles productos/categorías:")
        product_keywords = ['producto', 'medicamento', 'farmacia', 'categoría', 'shop', 'comprar']
        for link in links:
            if any(keyword in link['text'].lower() for keyword in product_keywords):
                print(f"   ⚕️ {link['text']}")
        
        # 6. Información de contacto
        print("\n🔹 Información de contacto:")
        contact_texts = ['contacto', 'teléfono', 'email', 'dirección', 'sucursal']
        for text in soup.stripped_strings:
            if any(contact in text.lower() for contact in contact_texts):
                if len(text) < 100:  # Filtrar textos largos
                    print(f"   📞 {text}")
        
        # 7. Estructura del sitio
        print("\n🔹 Estructura del sitio:")
        print(f"   • Total de enlaces: {len(soup.find_all('a'))}")
        print(f"   • Total de imágenes: {len(soup.find_all('img'))}")
        print(f"   • Total de formularios: {len(soup.find_all('form'))}")
        
        # Guardar resultados en JSON
        results = {
            'url': url,
            'title': title,
            'meta_description': meta_desc.get('content', '') if meta_desc else '',
            'links_count': len(soup.find_all('a')),
            'sample_links': links[:10]
        }
        
        with open('farmaloop_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Resultados guardados en: farmaloop_results.json")
        print("\n✅ Web scraping completado exitosamente!")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    scrape_farmaloop()