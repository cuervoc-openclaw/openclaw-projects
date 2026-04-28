#!/usr/bin/env python3
import json, urllib.request, urllib.error
import http.cookiejar, re

cj = http.cookiejar.MozillaCookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

LOGIN = "https://api.salasconstrucciones.com/wp-login.php"
login_data = "log=cuervoc&pwd=vdw8QL4s67i^v2Qs&wp-submit=Entrar&redirect_to=%2Fwp-admin%2F&testcookie=1"
opener.open(urllib.request.Request(LOGIN, data=login_data.encode(), method='POST'))

API = "https://api.salasconstrucciones.com/?rest_route=/wp/v2"

req = urllib.request.Request("https://api.salasconstrucciones.com/wp-admin/profile.php")
resp = opener.open(req)
html = resp.read().decode()
m = re.search(r'wpApiSettings\s*=\s*({[^;]+})', html)
nonce = json.loads(m.group(1))['nonce']
print(f"Nonce: {nonce}")

def wp_put(type_name, id, data):
    url = f"{API}/{type_name}/{id}"
    req = urllib.request.Request(url, data=json.dumps(data).encode(), method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-WP-Nonce', nonce)
    try:
        resp = opener.open(req)
        r = json.loads(resp.read().decode())
        print(f"  [{r.get('id')}] {r.get('title',{}).get('rendered', '?')} - updated")
        return r
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        print(f"  ERROR {e.code}: {body[:200]}")
        return None

# Update services
services = [
    {"id": 11, "title": "Mantenimiento General",
     "meta": {"icon_slug": "tools", "csalas_price_base": 35000, "csalas_price_unit": "hora", "csalas_price_min": 25000, "csalas_price_note": "M\u00ednimo 1 hora. Incluye mano de obra. Materiales no incluidos."}},
    {"id": 10, "title": "Construcci\u00f3n y Remodelaci\u00f3n",
     "meta": {"icon_slug": "hammer", "csalas_price_base": 0, "csalas_price_unit": "m2", "csalas_price_min": 0, "csalas_price_note": "Presupuesto personalizado seg\u00fan proyecto. Incluye visita t\u00e9cnica sin costo."}},
    {"id": 9, "title": "Certificaci\u00f3n de Planos El\u00e9ctricos",
     "meta": {"icon_slug": "file-certificate", "csalas_price_base": 150000, "csalas_price_unit": "proyecto", "csalas_price_min": 120000, "csalas_price_note": "Incluye visita t\u00e9cnica, elaboraci\u00f3n de planos y tr\u00e1mites SEC."}},
    {"id": 8, "title": "Electricidad Residencial",
     "meta": {"icon_slug": "zap", "csalas_price_base": 0, "csalas_price_unit": "visita", "csalas_price_min": 0, "csalas_price_note": "Presupuesto sin compromiso. Incluye revisi\u00f3n completa de la instalaci\u00f3n."}}
]
print("=== Updating services ===")
for s in services:
    sid = s.pop("id")
    wp_put("servicio", sid, s)

# Update hero slides
slides = [
    {"id": 21, "title": "Expertos en Construcci\u00f3n y Electricidad",
     "content": "M\u00e1s de 30 a\u00f1os construyendo confianza en Santiago y regiones. Servicios profesionales con garant\u00eda.",
     "meta": {"cta_text": "Solicitar presupuesto", "cta_url": "#contacto"}},
    {"id": 22, "title": "Certificaci\u00f3n SEC Profesional",
     "content": "Regularizamos tus instalaciones el\u00e9ctricas con rapidez y respaldo. Proceso completo en 5 a 10 d\u00edas.",
     "meta": {"cta_text": "Cotizar certificaci\u00f3n", "cta_url": "#contacto"}},
    {"id": 23, "title": "Mantenimiento para tu Hogar",
     "content": "Prevenci\u00f3n y reparaciones r\u00e1pidas. Mant\u00e9n tu hogar en \u00f3ptimas condiciones durante todo el a\u00f1o.",
     "meta": {"cta_text": "Agendar visita t\u00e9cnica", "cta_url": "#contacto"}}
]
print("\n=== Updating hero slides ===")
for s in slides:
    sid = s.pop("id")
    wp_put("hero_slide", sid, s)

# Update site title/description
print("\n=== Updating site settings ===")
settings = {
    "title": "Salas Construcciones - Construcci\u00f3n y Electricidad en Santiago",
    "description": "M\u00e1s de 30 a\u00f1os de experiencia en construcci\u00f3n, electricidad y mantenimiento en Santiago y regiones. Certificaci\u00f3n SEC, ampliaciones, remodelaciones y servicios profesionales."
}
req = urllib.request.Request(f"{API}/settings", data=json.dumps(settings).encode(), method='POST')
req.add_header('Content-Type', 'application/json')
req.add_header('X-WP-Nonce', nonce)
resp = opener.open(req)
r = json.loads(resp.read().decode())
print(f"  Site title: {r.get('title')}")

print("\n=== Done! ===")
