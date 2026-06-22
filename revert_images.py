#!/usr/bin/env python3
"""Revert post featured images to the original article images from the images folder."""

import json, requests, base64, io, os
from PIL import Image

with open('article_publishing/Configs/jap_config.json') as f:
    cfg = json.load(f)

WP_BASE = 'https://janataweekly.org/wp-json/wp/v2'
_token = base64.b64encode(f"{cfg['wp_username']}:{cfg['wp_app_password']}".encode()).decode()
WP_HEADERS = {
    'Authorization': f'Basic {_token}',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
}

IMAGES_DIR = '/home/shubhamshack/Downloads/janata/images/'

# article_number -> post_id  (only articles whose images were replaced)
ARTICLE_TO_POST = {
    1:  76066,
    2:  76059,
    3:  76065,
    4:  76064,
    5:  76056,
    6:  76057,
    8:  76060,
    9:  76061,
    10: 76062,
    11: 76055,
    13: 76073,
    14: 76081,
    15: 76082,
    18: 76083,
    19: 76085,
    20: 76086,
    21: 76087,
    22: 76089,
    23: 76088,
    24: 76090,
    25: 76095,
    26: 76103,
    27: 76105,
}


def process_image(path, max_kb=800):
    img = Image.open(path).convert('RGB')
    if img.width > 1920 or img.height > 1920:
        img.thumbnail((1920, 1920), Image.LANCZOS)
    quality = 85
    while True:
        buf = io.BytesIO()
        img.save(buf, 'JPEG', quality=quality, optimize=True)
        if buf.tell() / 1024 <= max_kb or quality <= 30:
            break
        quality -= 5
    buf.seek(0)
    return buf


def upload_image(buf, filename):
    headers = {
        'Authorization': WP_HEADERS['Authorization'],
        'User-Agent': WP_HEADERS['User-Agent'],
        'Content-Disposition': f'attachment; filename="{filename}"',
        'Content-Type': 'image/jpeg',
    }
    r = requests.post(f'{WP_BASE}/media', headers=headers, data=buf.read(), timeout=90)
    if r.status_code in (200, 201):
        return r.json()['id']
    print(f'  Upload error {r.status_code}: {r.text[:200]}')
    return None


def set_featured_image(post_id, media_id):
    r = requests.post(f'{WP_BASE}/posts/{post_id}', headers=WP_HEADERS,
                      json={'featured_media': media_id}, timeout=15)
    return r.status_code in (200, 201)


def delete_media(media_id):
    r = requests.delete(f'{WP_BASE}/media/{media_id}?force=true', headers=WP_HEADERS, timeout=15)
    return r.status_code == 200


def main():
    ok, fail = [], []

    for article_num in sorted(ARTICLE_TO_POST.keys()):
        post_id = ARTICLE_TO_POST[article_num]
        img_path = os.path.join(IMAGES_DIR, f'{article_num}.jpg')

        print(f'Article {article_num} (post {post_id}): {img_path}')

        if not os.path.exists(img_path):
            print(f'  SKIP: image file not found')
            fail.append((article_num, post_id, 'image file not found'))
            continue

        # Get current (Wikimedia) featured media to delete after
        r = requests.get(f'{WP_BASE}/posts/{post_id}', headers=WP_HEADERS, timeout=10)
        old_media_id = r.json().get('featured_media', 0)

        buf = process_image(img_path)
        new_media_id = upload_image(buf, f'article-{article_num}.jpg')
        if not new_media_id:
            fail.append((article_num, post_id, 'upload failed'))
            continue

        if set_featured_image(post_id, new_media_id):
            if old_media_id:
                deleted = delete_media(old_media_id)
                print(f'  Done: media {old_media_id} -> {new_media_id} (old deleted: {deleted})')
            else:
                print(f'  Done: media -> {new_media_id}')
            ok.append((article_num, post_id, new_media_id))
        else:
            print(f'  FAIL: could not update post')
            delete_media(new_media_id)
            fail.append((article_num, post_id, 'post update failed'))

    print(f'\n=== SUMMARY ===')
    print(f'Reverted: {len(ok)} / {len(ok)+len(fail)}')
    for n, p, m in ok:
        print(f'  OK   article={n} post={p} new_media={m}')
    for n, p, msg in fail:
        print(f'  FAIL article={n} post={p}: {msg}')


if __name__ == '__main__':
    main()
