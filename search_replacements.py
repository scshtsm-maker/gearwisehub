import sys, re, urllib.request, urllib.parse, json, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

def search_asin(product_name, safe_name=None):
    """Search Amazon and return first relevant ASIN"""
    if safe_name:
        query = urllib.parse.quote(safe_name)
    else:
        query = urllib.parse.quote(product_name)
    url = f'https://www.amazon.com/s?k={query}&tag=cfqclaw-20'
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        html = resp.read().decode('utf-8', errors='ignore')
        # Find ASINs
        asins = re.findall(r'"asin":"([A-Z0-9]{10})"', html)
        if asins:
            seen = set()
            for a in asins:
                if a not in seen and a not in ('title', 'brand', 'price'):
                    seen.add(a)
            if seen:
                return list(seen)[0], f'https://www.amazon.com/s?k={query}&tag=cfqclaw-20'
    except Exception as e:
        pass
    return None, None

# Product mapping from the audit
products_to_find = [
    # (article, old_asin, product_name, search_query)
    ('best-headphones-for-small-ears', 'B0BDHWDR9X', 'Samsung Galaxy Buds2 Pro', 'Samsung Galaxy Buds2 Pro'),
    ('best-headphones-for-small-ears', 'B0B7Q5XK8L', 'Sony LinkBuds S', 'Sony LinkBuds S'),
    ('best-running-headphones-2026', 'B0B7Q4HXK2', 'Jabra Elite 4 Active', 'Jabra Elite 4 Active'),
    ('best-sports-headphones-2026', 'B0D1J8KX2M', 'Soundcore Spirit C30 NC', 'Soundcore Spirit C30 NC'),
    ('best-sports-headphones-2026', 'B08F7PTF53', 'Soundcore Spirit Dot 2', 'Soundcore Spirit Dot 2 NC'),
    ('best-sports-headphones-2026', 'B0BR4D5YQH', 'JBL Vibe Buds 2', 'JBL Vibe Buds 2'),
    ('best-sports-headphones-2026', 'B0B7Q5XK8L', 'Sony LinkBuds S (sports)', 'Sony LinkBuds S'),
    ('best-sports-headphones-2026', 'B0D3HFRM2Q', 'Bose Ultra Open Earbuds', 'Bose Ultra Open Earbuds'),
    ('best-wireless-earbuds-under-200', 'B0CJL3ZJBM', 'Soundcore Liberty 3 Pro', 'Soundcore Liberty 3 Pro'),
]

print('Searching for replacement ASINs...')
print('=' * 80)

results = {}  # article -> [(old_asin, new_asin_or_None, search_url, product)]

for article, old_asin, product_name, search_query in products_to_find:
    print(f'\nSearching: {product_name}')
    new_asin, search_url = search_asin(product_name, search_query)
    if new_asin:
        print(f'  -> Found ASIN: {new_asin}')
        results.setdefault(article, []).append((old_asin, new_asin, None, product_name))
    else:
        print(f'  -> Not found, will use search link')
        results.setdefault(article, []).append((old_asin, None, search_url, product_name))
    time.sleep(1)

# Write results
with open(r'C:\Users\Administrator\gearwisehub\asin_fix_plan.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print('\n=== Results Summary ===')
for article, fixes in results.items():
    print(f'\n{article}:')
    for old, new, search, prod in fixes:
        if new:
            print(f'  {old} -> {new} ({prod})')
        else:
            print(f'  {old} -> SEARCH LINK ({prod})')
