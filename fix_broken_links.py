import re, os

BASE = r'C:\Users\Administrator\gearwisehub'

# Products with broken ASINs - replace with search links
BROKEN_ASINS = {
    'B08R5WRY6J': ('Shokz OpenSwim', 'https://www.amazon.com/s?k=Shokz+OpenSwim&tag=cfqclaw-20'),
    'B0D5TP8LR2': ('Razer BlackShark V2 Pro', 'https://www.amazon.com/s?k=Razer+BlackShark+V2+Pro&tag=cfqclaw-20'),
    'B0D6H3XK2M': ('Edifier W820NB Plus', 'https://www.amazon.com/s?k=Edifier+W820NB+Plus&tag=cfqclaw-20'),
    'B08B43KB47': ('Adidas RPT-01', 'https://www.amazon.com/s?k=Adidas+RPT-01+headphones&tag=cfqclaw-20'),
    # Also fix the Space Q45 old ASIN
    'B0BJ682ZKT': ('Soundcore Space Q45', 'https://www.amazon.com/dp/B0FWJY183S?tag=cfqclaw-20'),
}

SLUGS_TO_FIX = {
    'best-bone-conduction-headphones-2026': ['B08R5WRY6J'],
    'best-gaming-headsets-2026': ['B0D5TP8LR2'],
    'best-noise-canceling-headphones-under-200': ['B0D6H3XK2M'],
    'best-running-headphones-2026': ['B08B43KB47'],
    'soundcore-space-q45-review': ['B0BJ682ZKT'],
}

for slug, asins in SLUGS_TO_FIX.items():
    path = os.path.join(BASE, 'static', 'reviews', slug, 'index.html')
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()

    original = c
    for asin in asins:
        name, search_url = BROKEN_ASINS[asin]
        # Replace the specific Amazon dp link
        old_link = f'amazon.com/dp/{asin}?tag=cfqclaw-20'
        new_link = search_url
        if old_link in c:
            c = c.replace(old_link, new_link)
            print(f'{slug}: Replaced {asin} ({name}) with search link')
        else:
            print(f'{slug}: {asin} not found in Amazon dp link format - checking ASIN pattern')
            # Try to find any occurrence
            if asin in c:
                count = c.count(asin)
                print(f'  Found {asin} {count} times - needs manual review')
                # Find context
                idx = c.find(asin)
                print(f'  Context: ...{c[max(0,idx-50):idx+80]}...')

    if c != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)

print('\nDone fixing broken links')
