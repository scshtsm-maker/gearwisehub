import re, os, urllib.request, urllib.error, time

BASE = r'C:\Users\Administrator\gearwisehub'
REVIEWS = os.path.join(BASE, 'static', 'reviews')

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36'}
TIMEOUT = 4

def check_url(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS, method='GET')
        resp = urllib.request.urlopen(req, timeout=TIMEOUT)
        return resp.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return None

# Known bad ASINs
DISCONTINUED = {'B08R5WRY6J','B0D5TP8LR2','B0D6H3XK2M','B08B43KB47','B0BJ682ZKT'}
KNOWN_GOOD = {'B09BVXT8TJ','B0FNWCYLZN','B0BS1PRC4L','B0FWJY183S','B0F1CL7LTD',
              'B0D1S7D9YX','B0DQQT2ZS3','B07W6H7PY2','B08SHZW9MF','B083JRW96J',
              'B0FHW4CF51','B0F2QWR3FB','B0GLX2GZ7P','B07MSLF5YC','B0D6MR7RBD',
              'B0F9HTKWRD','B0D1J8KX2M','B0B7Q5XK8L','B0BR4D5YQH','B0D3HFRM2Q',
              'B08F7PTF53','B0FNWJ4FV3','B0C33XXS56','B0CN9FTKJ4','B07JL1K193',
              'B08Q8P69JZ','B0GXW4KNPB','B0F7M3HPBD','B0F3PQHWTZ','B0F3QJLD3B',
              'B0B7Q5XK8L','B0D8QJN5VX','B0CJL3ZJBM','B0BDHWDR9X'}

slugs = sorted(os.listdir(REVIEWS))
out = []
out.append(f'Total articles: {len(slugs)}\n{"="*60}\n')

for slug in slugs:
    path = os.path.join(REVIEWS, slug, 'index.html')
    if not os.path.isfile(path):
        out.append(f'SKIP: {slug} (no index.html)\n')
        continue

    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()

    issues = []

    # --- Amazon links ---
    amazon_links = re.findall(r'https?://[^\s"\'<>]*amazon[^\s"\'<>]+', c)
    asins_found = {}
    for url in amazon_links:
        asin_m = re.search(r'/(?:dp|exec/obidos/ASIN)/([A-Z0-9]{10})', url)
        tag_m = re.search(r'tag=([a-z0-9_-]+)', url)
        if asin_m:
            asin = asin_m.group(1)
            tag = tag_m.group(1) if tag_m else 'NONE'
            asins_found[asin] = (url[:80], tag)
            if tag != 'cfqclaw-20':
                issues.append(f'  [TAG] Wrong tag={tag} for {asin}')
            if asin in DISCONTINUED:
                issues.append(f'  [ASIN] Discontinued ASIN {asin} still in URL!')

    # Spot-check 1 Amazon link (fast)
    if amazon_links:
        status = check_url(amazon_links[0])
        if status and status not in (200, 301, 302):
            issues.append(f'  [HTTP] {status} for {amazon_links[0][:60]}')

    # --- Images ---
    img_links = re.findall(r'https?://[^\s"\'<>]*(?:unsplash|pexels|picsum)[^\s"\'<>]+', c)
    if not img_links:
        issues.append(f'  [IMAGE] No images found!')
    else:
        # Check 1 image
        status = check_url(img_links[0])
        if status and status not in (200,):
            issues.append(f'  [IMAGE HTTP {status}] {img_links[0][:60]}')

    # --- Internal links ---
    internal = re.findall(r'href="(/[^\s"\'<>]+)"', c)
    for link in internal[:3]:
        if link.startswith('//'): continue
        if link.startswith('http'): continue
        full = f'https://cfqclaw.dpdns.org{link}'
        status = check_url(full)
        if status and status not in (200, 301, 302, 400):
            issues.append(f'  [INTERNAL HTTP {status}] {link}')

    # --- HTML structure ---
    if '<html' not in c.lower():
        issues.append('  [HTML] Missing <html> tag')
    if 'lang="en"' not in c and "lang='en'" not in c:
        issues.append('  [LANG] Not lang="en"')
    if '<main' not in c:
        issues.append('  [HTML] Missing <main> tag')
    if '<title' not in c.lower():
        issues.append('  [SEO] Missing <title>')
    if 'schema.org' not in c and 'schema\.org' not in c:
        issues.append('  [SEO] Missing JSON-LD schema')

    # --- Encoding ---
    if '&lt;' in c or '&gt;' in c:
        issues.append('  [ENCODING] HTML entities in content (&lt; &gt;)')
    if '&#' in c:
        issues.append('  [ENCODING] Numeric HTML entities in content')

    # --- Amazon ASIN count (reasonable range) ---
    asins = list(asins_found.keys())
    if len(asins) == 0:
        issues.append('  [ASIN] No Amazon links found!')

    # --- Report ---
    if issues:
        out.append(f'❌ {slug} ({len(asins)} ASINs)\n')
        for i in issues:
            out.append(i + '\n')
    else:
        out.append(f'✅ {slug} ({len(asins)} ASINs)\n')

out.append(f'\n{"="*60}\n')
out.append(f'Done. Check lines starting with ❌ above.')

result = ''.join(out)
print(result)

with open(os.path.join(BASE, 'audit_results.txt'), 'w', encoding='utf-8') as f:
    f.write(result)
