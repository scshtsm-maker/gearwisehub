import os, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = r'C:\Users\Administrator\gearwisehub'
REVIEWS = os.path.join(BASE, 'static', 'reviews')

# Fix 1: Remaining duplicate in best-running-headphones-2026
print('=== Fixing best-running-headphones-2026 duplicate ===')
slug = 'best-running-headphones-2026'
path = os.path.join(REVIEWS, slug, 'index.html')
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()

paras = list(re.finditer(r'<p[^>]*>(.*?)</p>', c, re.DOTALL))
seen = {}
for pm in paras:
    p_text = re.sub(r'<[^>]+>', '', pm.group(1)).strip()
    if len(p_text) < 60: continue
    key = p_text[:150]
    if key in seen:
        prev = seen[key]
        print(f'  Duplicate: para at pos {prev} == pos {pm.start()}')
        print(f'  Text: "{p_text[:100]}"')
        # Remove this duplicate
        c = c[:pm.start()] + c[pm.end():]
        print(f'  Removed duplicate at {pm.start()}')
    else:
        seen[key] = pm

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

# Verify
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    c2 = f.read()
paras2 = list(re.finditer(r'<p[^>]*>(.*?)</p>', c2, re.DOTALL))
seen2 = {}
dupes = 0
for pm in paras2:
    p_text = re.sub(r'<[^>]+>', '', pm.group(1)).strip()
    if len(p_text) < 60: continue
    key = p_text[:150]
    if key in seen2: dupes += 1
    seen2[key] = 1
print(f'  Remaining duplicates: {dupes}')

# Fix 2: Check product unavailable in best-wireless-earbuds-under-100
print('\n=== Checking best-wireless-earbuds-under-100 ===')
slug = 'best-wireless-earbuds-under-100'
path = os.path.join(REVIEWS, slug, 'index.html')
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()

matches = re.findall(r'.{80}(unavailable|not available).{80}', c, re.I)
for i, m in enumerate(matches):
    clean = re.sub(r'\s+', ' ', m).strip()
    print(f'  Match {i+1}: ...{clean}...')

print('\nDone!')
