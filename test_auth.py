"""
Quick test: verifies WordPress Application Password auth is working.
Run from the repo root: python test_auth.py
"""
import base64
import json
import os
import sys
import requests

CREDS_PATH = './article_publishing/Configs/jap_config.json'
WP_BASE = 'https://janataweekly.org/wp-json/wp/v2'

def load_creds():
    if not os.path.exists(CREDS_PATH):
        print(f"ERROR: {CREDS_PATH} not found.")
        print("Copy jap_config.sample.json to jap_config.json and fill in your credentials.")
        sys.exit(1)
    with open(CREDS_PATH) as f:
        creds = json.load(f)
    for key in ('wp_username', 'wp_app_password'):
        if key not in creds:
            print(f"ERROR: '{key}' missing from jap_config.json")
            sys.exit(1)
    return creds

def make_auth_header(creds):
    token = base64.b64encode(
        f"{creds['wp_username']}:{creds['wp_app_password']}".encode()
    ).decode()
    return {
        'Authorization': f'Basic {token}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
    }

def test_whoami(headers):
    r = requests.get(f'{WP_BASE}/users/me', headers=headers)
    if r.status_code == 200:
        u = r.json()
        print(f"[PASS] Authenticated as: {u.get('name')} (id={u.get('id')}, roles={u.get('roles')})")
        return True
    else:
        print(f"[FAIL] /users/me returned {r.status_code}: {r.text[:200]}")
        return False

def test_list_posts(headers):
    r = requests.get(f'{WP_BASE}/posts?status=draft&per_page=1', headers=headers)
    if r.status_code == 200:
        print(f"[PASS] Can read draft posts (count in response: {len(r.json())})")
        return True
    else:
        print(f"[FAIL] /posts returned {r.status_code}: {r.text[:200]}")
        return False

def test_list_media(headers):
    r = requests.get(f'{WP_BASE}/media?per_page=1', headers=headers)
    if r.status_code == 200:
        print(f"[PASS] Can access media library")
        return True
    else:
        print(f"[FAIL] /media returned {r.status_code}: {r.text[:200]}")
        return False

if __name__ == '__main__':
    creds = load_creds()
    headers = make_auth_header(creds)

    print(f"\nTesting WordPress Application Password auth for: {creds['wp_username']}")
    print(f"Site: {WP_BASE}\n")

    results = [
        test_whoami(headers),
        test_list_posts(headers),
        test_list_media(headers),
    ]

    print()
    if all(results):
        print("All checks passed. Auth is working correctly.")
    else:
        print("Some checks failed. See details above.")
        sys.exit(1)
