import os, re

ARTICLES = [
    'best-bone-conduction-headphones-2026',
    'best-budget-headphones-2026',
    'best-gaming-headsets-2026',
    'best-noise-canceling-headphones-under-200',
    'best-running-headphones-2026',
    'best-sports-headphones-2026',
    'best-headphones-for-small-ears',
    'best-wireless-earbuds-under-100',
    'best-wireless-earbuds-under-200',
]

BASE = r'C:\Users\Administrator\gearwisehub\static\reviews'

for slug in ARTICLES:
    path = os.path.join(BASE, slug, 'index.html')
    if not os.path.exists(path):
        print(f'MISSING: {slug}')
        continue
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    title_m = re.search(r'<title>([^<]+)</title>', content)
    desc_m = re.search(r'<meta name="description" content="([^"]+)"', content)
    img_m = re.search(r'<meta property="og:image" content="([^"]+)"', content)
    lang_m = re.search(r'<html[^>]*lang="([^"]+)"', content)

    title = title_m.group(1) if title_m else 'Unknown'
    desc = desc_m.group(1)[:120] if desc_m else 'No description'
    img = img_m.group(1) if img_m else ''
    lang = lang_m.group(1) if lang_m else 'en'

    print(f'{slug} | {lang} | {title[:70]}')
    if lang != 'en':
        print(f'  WARNING: lang={lang}, needs translation!')
