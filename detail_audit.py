import os, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = r'C:\Users\Administrator\gearwisehub'
REVIEWS = os.path.join(BASE, 'static', 'reviews')

# === Issue 1: Nav menu leaked into <p> tag ===
print("=" * 60)
print("ISSUE 1: Nav menu leaking into <p> tags")
print("=" * 60)

nav_leak_slugs = [
    'apple-airpods-pro-2-review',
    'best-noise-canceling-headphones-under-200',
    'best-wireless-earbuds-under-100',
    'best-wireless-earbuds-under-200',
    'sony-wh-1000xm5',
]

for slug in nav_leak_slugs:
    path = os.path.join(REVIEWS, slug, 'index.html')
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    
    # Find the leaking <p> tag
    paras = re.findall(r'<p[^>]*>(.*?)</p>', c, re.DOTALL)
    for i, p in enumerate(paras[:5]):
        p_text = re.sub(r'<[^>]+>', '', p).strip()
        if 'Home' in p_text and len(p_text) > 10:
            print(f'\n--- {slug} (para {i}) ---')
            # Show raw HTML of this paragraph
            print(f'Raw HTML (first 300 chars):')
            print(p[:300])
            break

# === Issue 2: Duplicate paragraphs ===
print("\n" + "=" * 60)
print("ISSUE 2: Duplicate paragraphs")
print("=" * 60)

dupe_slugs = ['best-bone-conduction-headphones-2026', 'best-flagship-noise-canceling-earbuds-2026', 'best-running-headphones-2026']

for slug in dupe_slugs:
    path = os.path.join(REVIEWS, slug, 'index.html')
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    
    paras = re.findall(r'<p[^>]*>(.*?)</p>', c, re.DOTALL)
    body_paras = [(i, re.sub(r'<[^>]+>', '', p).strip()) for i, p in enumerate(paras) if len(re.sub(r'<[^>]+>', '', p).strip()) > 60]
    
    seen = {}
    for idx, text in body_paras:
        short = text[:100]
        if short in seen:
            prev_idx = seen[short]
            print(f'\n--- {slug} ---')
            print(f'  Para {prev_idx} == Para {idx} (dupe)')
            print(f'  Text: "{text[:120]}..."')
        else:
            seen[short] = idx

# === Issue 3: Missing spaces around year numbers ===
print("\n" + "=" * 60)
print("ISSUE 3: Broken spacing around year/numbers")
print("=" * 60)

for slug in ['best-over-ear-noise-canceling-headphones-2026', 'best-running-headphones-2026']:
    path = os.path.join(REVIEWS, slug, 'index.html')
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    
    # Show examples of broken spacing
    matches = re.findall(r'.{20}(?:\d{4}[A-Z]|[a-z]\d{4}[A-Z]|\d{4}Year).{20}', c)
    print(f'\n--- {slug} ({len(matches)} instances) ---')
    for m in matches[:5]:
        clean = re.sub(r'\s+', ' ', m).strip()
        print(f'  ...{clean}...')

# === Issue 4: Product unavailable warnings ===
print("\n" + "=" * 60)
print("ISSUE 4: Product unavailable text")
print("=" * 60)

path = os.path.join(REVIEWS, 'best-wireless-earbuds-under-100', 'index.html')
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()

matches = re.findall(r'.{50}(unavailable|not available|discontinued).{50}', c, re.I)
for m in matches:
    clean = re.sub(r'\s+', ' ', m).strip()
    print(f'  ...{clean}...')
