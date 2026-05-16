import re, os

BASE = r'C:\Users\Administrator\gearwisehub'

SLUGS = [
    'best-bone-conduction-headphones-2026',
    'best-gaming-headsets-2026',
    'best-wireless-earbuds-under-200',
    'best-wireless-earbuds-under-100',
]

# Products with no Amazon replacement
NO_REPLACEMENT = {
    'B08R5WRY6J': 'Shokz OpenSwim - discontinued',
    'B0D5TP8LR2': 'Razer BlackShark V2 Pro 2026 - discontinued',
    'B0D6H3XK2M': 'Edifier W820NB Plus - discontinued',
    'B08B43KB47': 'Adidas RPT-01 - discontinued',
}

for slug in SLUGS:
    path = os.path.join(BASE, 'static', 'reviews', slug, 'index.html')
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()

    # Find Amazon links
    links = re.findall(r'(amazon\.com/[^\s"\'<>]+)', c)
    asins_in_links = []
    for l in links:
        a = re.search(r'/(?:dp|exec/obidos/ASIN)/([A-Z0-9]{10})', l)
        if a:
            asins_in_links.append(a.group(1))

    print(f'\n{slug}:')
    for a in set(asins_in_links):
        if a in NO_REPLACEMENT:
            print(f'  {a} -> NO REPLACEMENT ({NO_REPLACEMENT[a]}) - may be broken!')
        else:
            print(f'  {a} -> OK')
