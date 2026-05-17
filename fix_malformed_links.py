import sys, os, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = r'C:\Users\Administrator\gearwisehub\static\reviews'

# Fix malformed search links (spaces not encoded)
fixes = {
    'best-flagship-noise-canceling-earbuds-2026': [
        ('https://www.amazon.com/s?k=Air Pods+Pro+3&tag=cfqclaw-20',
         'https://www.amazon.com/s?k=AirPods+Pro+3&tag=cfqclaw-20'),
    ],
    'best-over-ear-noise-canceling-headphones-2026': [
        ('https://www.amazon.com/s?k=Air Pods+Max+2&tag=cfqclaw-20',
         'https://www.amazon.com/s?k=AirPods+Max+2&tag=cfqclaw-20'),
        ('https://www.amazon.com/s?k=Bose+Quiet Comfort+Ultra+Headphones&tag=cfqclaw-20',
         'https://www.amazon.com/s?k=Bose+QuietComfort+Ultra+Headphones&tag=cfqclaw-20'),
    ],
}

print('Fixing malformed search links...')
fixed = 0

for article, link_fixes in fixes.items():
    art_path = os.path.join(BASE, article, 'index.html')
    with open(art_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    article_fixed = False
    for old_link, new_link in link_fixes:
        if old_link in content:
            content = content.replace(old_link, new_link)
            print(f'  Fixed: {article} -> {old_link[:60]} -> {new_link[:60]}')
            article_fixed = True
            fixed += 1
        else:
            print(f'  Not found: {article} -> {old_link[:60]}')
    
    if article_fixed:
        with open(art_path, 'w', encoding='utf-8') as f:
            f.write(content)

print(f'\nTotal fixed: {fixed}')
