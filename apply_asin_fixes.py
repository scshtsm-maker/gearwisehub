import sys, os, re, json

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = r'C:\Users\Administrator\gearwisehub\static\reviews'

# Load fix plan
with open(r'C:\Users\Administrator\gearwisehub\asin_fix_plan.json', 'r', encoding='utf-8') as f:
    fix_plan = json.load(f)

print('=' * 80)
print('FIXING ASINs - Replacing with Amazon Search Links')
print('=' * 80)

def build_search_link(product_name):
    """Build Amazon search link with affiliate tag"""
    from urllib.parse import quote
    q = quote(product_name)
    return f'https://www.amazon.com/s?k={q}&tag=cfqclaw-20'

fixed_count = 0
fix_log = []

for article, fixes in fix_plan.items():
    art_path = os.path.join(BASE, article, 'index.html')
    if not os.path.exists(art_path):
        print(f'  SKIP: {art_path} not found')
        continue
    
    with open(art_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    article_changed = False
    for old_asin, new_asin, search_url, product_name in fixes:
        old_url_pattern = f'/dp/{old_asin}'
        if old_url_pattern not in content and f'dp/{old_asin}' not in content:
            print(f'  {article}: ASIN {old_asin} not found in content (already fixed?)')
            continue
        
        if new_asin:
            # Replace with new direct link
            old_url = f'https://www.amazon.com/dp/{old_asin}?tag=cfqclaw-20'
            new_url = f'https://www.amazon.com/dp/{new_asin}?tag=cfqclaw-20'
            if old_url in content:
                content = content.replace(old_url, new_url)
                article_changed = True
                fixed_count += 1
                fix_log.append(f'{article}: {old_asin} -> {new_asin} ({product_name})')
                print(f'  {article}: {old_asin} -> {new_asin} ({product_name})')
        else:
            # Replace with search link
            search_link = build_search_link(product_name)
            # Find and replace all URLs with this ASIN
            pattern = rf'https?://www\.amazon\.com/dp/{old_asin}[^"]*'
            replacements = re.findall(pattern, content)
            if replacements:
                content = re.sub(pattern, search_link, content)
                article_changed = True
                fixed_count += 1
                fix_log.append(f'{article}: {old_asin} -> SEARCH LINK ({product_name})')
                print(f'  {article}: {old_asin} -> SEARCH LINK ({product_name})')
    
    if article_changed:
        with open(art_path, 'w', encoding='utf-8') as f:
            f.write(content)

print(f'\n=== Done: {fixed_count} ASIN replacements ===')
for log in fix_log:
    print(f'  {log}')
