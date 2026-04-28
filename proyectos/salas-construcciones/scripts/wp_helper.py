#!/usr/bin/env python3
"""Helper to update WordPress options and check what's available"""
import json, urllib.request, urllib.error
import http.cookiejar, re

cj = http.cookiejar.MozillaCookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

LOGIN = "https://api.salasconstrucciones.com/wp-login.php"
login_data = "log=cuervoc&pwd=vdw8QL4s67i^v2Qs&wp-submit=Entrar&redirect_to=%2Fwp-admin%2F&testcookie=1"
opener.open(urllib.request.Request(LOGIN, data=login_data.encode(), method='POST'))

# Try to fetch options directly via REST (custom endpoint)
API = "https://api.salasconstrucciones.com/?rest_route="

# 1. Let's check the landing again
req = urllib.request.Request(f"{API}/csalas/v1/landing")
resp = opener.open(req)
landing = json.loads(resp.read().decode())
print("=== Current Landing Data ===")
print(json.dumps(landing, indent=2, ensure_ascii=False)[:2000])

# 2. Try to see what options exist via WP CLI equivalent
# Check if there's an ACF options page
req = urllib.request.Request(f"{API}/acf/v3/options/options")
req.add_header('Content-Type', 'application/json')
try:
    resp = opener.open(req)
    print("\n=== ACF Options ===")
    print(json.dumps(json.loads(resp.read().decode()), indent=2, ensure_ascii=False)[:1000])
except urllib.error.HTTPError as e:
    body = e.read().decode()
    if 'rest_no_route' in body:
        print("\nNo ACF REST endpoint")
    else:
        print(f"\nACF error: {body[:200]}")

# 3. See if the landing endpoint accepts POST to save
test_data = json.dumps({"test": "hello"}).encode()
req = urllib.request.Request(f"{API}/csalas/v1/landing", data=test_data, method='POST')
req.add_header('Content-Type', 'application/json')
# Get nonce
req_nonce = urllib.request.Request("https://api.salasconstrucciones.com/wp-admin/profile.php")
resp_nonce = opener.open(req_nonce)
html = resp_nonce.read().decode()
m = re.search(r'wpApiSettings\s*=\s*({[^;]+})', html)
if m:
    nonce = json.loads(m.group(1))['nonce']
    req.add_header('X-WP-Nonce', nonce)
try:
    resp = opener.open(req)
    print(f"\n=== POST to landing: {resp.status} ===")
    print(resp.read().decode()[:500])
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"\n=== POST to landing: {e.code} ===")
    print(body[:500])

