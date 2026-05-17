import os, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = r'C:\Users\Administrator\gearwisehub'
REVIEWS = os.path.join(BASE, 'static', 'reviews')

slug = 'apple-airpods-pro-2-review'
path = os.path.join(REVIEWS, slug, 'index.html')
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()

# Get ALL <p> tags with their positions
p_matches = list(re.finditer(r'<p[^>]*>(.*?)</p>', c, re.DOTALL))
print(f'Total <p> tags: {len(p_matches)}')
for i, pm in enumerate(p_matches[:5]):
    p_text = re.sub(r'<[^>]+>', '', pm.group(1)).strip()
    print(f'\nPara {i} (pos {pm.start()}-{pm.end()}):')
    print(f'  Text: "{p_text[:150]}"')
    # Show raw tag
    print(f'  Raw open: {c[pm.start():pm.start()+30]}')
