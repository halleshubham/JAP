#!/usr/bin/env python3
"""Replace high/medium/clearly-copyrighted article images with Wikimedia Commons images."""

import json, requests, base64, io, time
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
COMMONS_API = 'https://commons.wikimedia.org/w/api.php'
COMMONS_UA = 'JanataWeeklyImageBot/1.0 (halleshubham@gmail.com; replacing-copyrighted-images)'

SKIP_EXTS = {'.svg', '.gif', '.ogv', '.webm', '.ogg', '.mp4', '.pdf', '.tif', '.tiff'}

# post_id: (description, [search queries in priority order])
# HIGH RISK: wire/news photos | MEDIUM RISK: stock/unclear | CLEARLY COPYRIGHTED: book cover/screenshot
REPLACEMENTS = {
    # --- HIGH RISK ---
    76059: ('Pushback BSF India border',         ['India Bangladesh border fence barbed wire', 'Border Security Force India boat patrol']),
    76065: ('Delimitation India elections',       ['India election voter polling booth EVM', 'Indian election commission voting']),
    76056: ('Exam leak crisis India',             ['India students examination hall NEET', 'India student protest education']),
    76060: ('Cotton farmers India',               ['cotton farming harvest India field women', 'India cotton crop agriculture farmers']),
    76062: ('Jamia Millia Islamia Delhi',         ['Jamia Millia Islamia university Delhi', 'Jamia Millia Islamia campus gate']),
    76073: ('Gaza Palestine war',                 ['Gaza city Palestine buildings street', 'Gaza Palestine ruins destruction']),
    76081: ('Chess justice slavery',              ['slavery memorial monument Africa chains', 'abolition slavery monument sculpture']),
    76082: ('American empire US Capitol',         ['United States Capitol building Washington DC', 'US Congress Capitol Hill exterior']),
    76085: ('Ebola Congo DRC healthcare',         ['Ebola Democratic Republic Congo health worker', 'healthcare clinic Africa tropical disease']),
    76086: ('Kashmir valley India',               ['Kashmir Dal Lake Srinagar valley', 'Kashmir valley Himalayas mountains landscape']),
    76087: ('Afghanistan school girls',           ['Afghanistan school girls education classroom', 'Afghanistan children education']),
    # --- MEDIUM RISK ---
    76066: ('SIR electoral rolls India',          ['India voter registration election booth', 'India general election voting machine EVM']),
    76064: ('India workers labour',               ['India construction workers labour manual', 'India labourers workers street']),
    76057: ('India healthcare hospital',          ['India public health hospital rural clinic', 'India doctor nurse healthcare']),
    76061: ('Indus River waters treaty',          ['Indus River India Pakistan water landscape', 'Indus River valley Pakistan']),
    76055: ('Journalist press freedom India',     ['journalist reporter press conference microphone', 'press freedom journalism reporter']),
    76089: ('Disability wheelchair',              ['wheelchair disability accessibility inclusion', 'physically disabled wheelchair person']),
    76088: ('Nuclear power plant',                ['nuclear power plant cooling tower reactor', 'nuclear reactor power station cooling']),
    76090: ('Data centre AI technology',          ['data center server room rack technology', 'computer server data center cooling']),
    76095: ('Forest trees nature India',          ['tropical forest trees India nature', 'forest canopy trees green India']),
    76105: ('Qawwali sufi music',                 ['qawwali sufi music performance dargah', 'sufi singing devotional music India']),
    # --- CLEARLY COPYRIGHTED ---
    76083: ('Venezuela Caracas socialism',        ['Caracas Venezuela city socialist landscape', 'Venezuela mountains valley landscape']),
    76103: ('Labor movement socialist rally',     ['workers labor movement rally march solidarity', 'socialist workers rally protest banner']),
}


def search_wikimedia(query, limit=10):
    params = {
        'action': 'query', 'list': 'search',
        'srsearch': query, 'srnamespace': 6,
        'srlimit': limit, 'format': 'json',
    }
    try:
        r = requests.get(COMMONS_API, params=params, headers={'User-Agent': COMMONS_UA}, timeout=15)
        return [item['title'] for item in r.json().get('query', {}).get('search', [])]
    except Exception:
        return []


def get_image_url(file_title):
    params = {
        'action': 'query', 'titles': file_title,
        'prop': 'imageinfo', 'iiprop': 'url|mime|size', 'format': 'json',
    }
    try:
        r = requests.get(COMMONS_API, params=params, headers={'User-Agent': COMMONS_UA}, timeout=15)
        for page in r.json().get('query', {}).get('pages', {}).values():
            info = page.get('imageinfo', [{}])[0]
            url, mime, size = info.get('url', ''), info.get('mime', ''), info.get('size', 0)
            if url and 'image' in mime and size < 15_000_000:
                return url, mime
    except Exception:
        pass
    return None, None


def process_image(url, max_kb=800):
    r = requests.get(url, headers={'User-Agent': COMMONS_UA}, timeout=90, stream=True)
    r.raise_for_status()
    img = Image.open(io.BytesIO(r.content)).convert('RGB')
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
    print(f'    Upload error {r.status_code}: {r.text[:200]}')
    return None


def set_featured_image(post_id, media_id):
    r = requests.post(f'{WP_BASE}/posts/{post_id}', headers=WP_HEADERS,
                      json={'featured_media': media_id}, timeout=15)
    return r.status_code in (200, 201)


def delete_media(media_id):
    requests.delete(f'{WP_BASE}/media/{media_id}?force=true', headers=WP_HEADERS, timeout=15)


def find_and_download(queries):
    for query in queries:
        print(f'    Search: "{query}"')
        titles = search_wikimedia(query)
        for title in titles:
            lower = title.lower()
            ext = '.' + lower.rsplit('.', 1)[-1] if '.' in lower else ''
            if ext in SKIP_EXTS:
                continue
            url, mime = get_image_url(title)
            if not url:
                continue
            if any(x in mime for x in ('svg', 'gif', 'video', 'audio', 'text')):
                continue
            try:
                buf = process_image(url)
                return buf, title
            except Exception as e:
                print(f'    Skip {title}: {e}')
        time.sleep(0.3)
    return None, None


def main():
    print(f'Replacing images for {len(REPLACEMENTS)} posts...\n')
    ok, fail = [], []

    for post_id, (desc, queries) in sorted(REPLACEMENTS.items()):
        print(f'\nPost {post_id}: {desc}')

        r = requests.get(f'{WP_BASE}/posts/{post_id}', headers=WP_HEADERS, timeout=10)
        old_media_id = r.json().get('featured_media', 0)

        buf, wiki_title = find_and_download(queries)
        if not buf:
            print(f'  FAILED: no usable image found')
            fail.append((post_id, desc, 'no image found'))
            continue

        print(f'  Source: {wiki_title}')

        safe = ''.join(c if c.isalnum() or c == '-' else '-' for c in desc.lower())[:40]
        filename = f'p{post_id}-{safe}.jpg'
        new_media_id = upload_image(buf, filename)
        if not new_media_id:
            fail.append((post_id, desc, 'upload failed'))
            continue

        if set_featured_image(post_id, new_media_id):
            if old_media_id:
                delete_media(old_media_id)
            print(f'  Done: media {old_media_id} -> {new_media_id}')
            ok.append((post_id, desc, wiki_title))
        else:
            fail.append((post_id, desc, 'post update failed'))
            delete_media(new_media_id)

        time.sleep(0.5)

    print('\n\n=== SUMMARY ===')
    print(f'Success: {len(ok)} / {len(ok)+len(fail)}')
    for post_id, desc, title in ok:
        print(f'  OK   post={post_id}  {desc:<40} <- {title}')
    for post_id, desc, msg in fail:
        print(f'  FAIL post={post_id}  {desc:<40}: {msg}')


if __name__ == '__main__':
    main()
