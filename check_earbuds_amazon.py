import re, urllib.parse, os

for slug in ['best-wireless-earbuds-under-100', 'best-wireless-earbuds-under-200']:
    path = os.path.join(os.path.dirname(__file__), 'static', 'reviews', slug, 'index.html')
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    amazon_links = re.findall(r'(https?://[^\s<>"\']+amazon[^\s<>"\']+)', c)
    print(f'{slug}:')
    for l in amazon_links[:10]:
        decoded = urllib.parse.unquote(l)
        asin = re.search(r'/dp/([A-Z0-9]{10})', decoded)
        tag_m = re.search(r'tag=([a-z0-9_-]+)', decoded)
        if asin:
            print(f'  ASIN={asin.group(1)} tag={tag_m.group(1) if tag_m else "NONE"} | {decoded[:100]}')
        else:
            print(f'  (no ASIN) | {decoded[:100]}')
    print()
