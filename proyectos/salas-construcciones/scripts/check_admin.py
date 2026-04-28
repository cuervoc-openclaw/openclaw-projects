#!/usr/bin/env python3
import json, urllib.request, urllib.error
import http.cookiejar, re

cj = http.cookiejar.MozillaCookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

LOGIN_URL = "https://api.salasconstrucciones.com/wp-login.php"
login_data = "log=cuervoc&pwd=vdw8QL4s67i^v2Qs&wp-submit=Entrar&redirect_to=%2Fwp-admin%2F&testcookie=1"
opener.open(urllib.request.Request(LOGIN_URL, data=login_data.encode(), method='POST'))

# Get admin page
req = urllib.request.Request("https://api.salasconstrucciones.com/wp-admin/")
resp = opener.open(req)
html = resp.read().decode(errors='replace')

# Find admin menu items
menu_items = re.findall(
    r'<div class="wp-menu-name[^"]*"[^>]*>(.*?)</div>',
    html, re.DOTALL
)
print("=== Admin Menu Items ===")
for item in menu_items:
    name = re.sub(r'<[^>]+>', '', item).strip()
    if name:
        print(f"  {name}")

# Get plugins
req2 = urllib.request.Request(
    "https://api.salasconstrucciones.com/wp-admin/plugins.php?plugin_status=active"
)
resp2 = opener.open(req2)
html2 = resp2.read().decode(errors='replace')

plugin_names = re.findall(
    r'class="plugin-title"[^>]*>.*?<strong>(.*?)</strong>',
    html2, re.DOTALL
)
print(f"\n=== Active Plugins ({len(plugin_names)}) ===")
for p in plugin_names:
    name = re.sub(r'<[^>]+>', '', p).strip()
    if name:
        print(f"  {name}")

# Get theme info
req3 = urllib.request.Request("https://api.salasconstrucciones.com/wp-admin/themes.php")
resp3 = opener.open(req3)
html3 = resp3.read().decode(errors='replace')

theme_match = re.search(r'theme-name[^>]*>\s*([^<]+)', html3)
if theme_match:
    print(f"\nActive Theme: {theme_match.group(1).strip()}")

# Check admin for custom options pages related to landing/contact
all_links = re.findall(
    r'<a[^>]*href="([^"]*)"[^>]*>([^<]+)</a>',
    html, re.DOTALL
)
print("\n=== Links with 'salas' or 'landing' or 'contact' ===")
for href, text in all_links:
    text_clean = re.sub(r'<[^>]+>', '', text).strip()
    if any(x in href.lower() or x in text_clean.lower() 
           for x in ['salas', 'landing', 'contact', 'hero', 'slider', 'csalas']):
        print(f"  {text_clean}: admin.php?{href.split('admin.php?')[-1] if 'admin.php?' in href else href}")
