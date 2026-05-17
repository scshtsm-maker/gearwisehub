import sys, os, re, urllib.request, urllib.error, time, json

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = r'C:\Users\Administrator\gearwisehub\static\reviews'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

def test_asin(asin):
    """Test if ASIN is valid on Amazon"""
    url = f'https://www.amazon.com/dp/{asin}?tag=cfqclaw-20'
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req, timeout=8)
        return (200, resp.geturl())
    except urllib.error.HTTPError as e:
        return (e.code, str(e))
    except Exception as e:
        return (0, str(e)[:60])

def find_asin_by_name(product_name):
    """Search Amazon by product name, return first ASIN"""
    query = urllib.parse.quote(product_name)
    url = f'https://www.amazon.com/s?k={query}&tag=cfqclaw-20'
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        html = resp.read().decode('utf-8', errors='ignore')
        # Find ASINs in search results
        asins = re.findall(r'"asin":"([A-Z0-9]{10})"', html)
        if asins:
            # Return first unique ASIN
            seen = set()
            for a in asins:
                if a not in seen:
                    seen.add(a)
                    return a
    except:
        pass
    return None

import urllib.parse

# Read previous audit results
with open(r'C:\Users\Administrator\gearwisehub\link_audit_results.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

fails = [r for r in data['direct_results'] if r['status'] != 200 and r['asin'] != '?']

print('=' * 80)
print('FAILED ASINs - Looking up replacements')
print('=' * 80)

RESULTS_FILE = r'C:\Users\Administrator\gearwisehub\failed_asin_fixes.txt'

fix_map = {}  # article -> [(old_asin, new_asin_or_searchlink, product_name)]

for r in fails:
    asin = r['asin']
    article = r['article']
    url = r['url']
    
    # Try to find the product name near this link in the article
    art_path = os.path.join(BASE, article, 'index.html')
    if not os.path.exists(art_path):
        continue
    
    with open(art_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find text around the ASIN URL
    idx = content.find(asin)
    if idx == -1:
        # Try finding the URL
        idx = content.find(url[:50])
    
    if idx > -1:
        context = content[max(0,idx-300):idx+300]
        # Try to extract product name from context
        # Look for product name patterns
        name_match = re.search(r'(?:name|product|itemprop|content|title)[^>]*>([^<]{5,80})<', context, re.IGNORECASE)
        # Also look for headings
        h_match = re.search(r'<h[23][^>]*>(.*?)</h[23]>', context, re.DOTALL | re.IGNORECASE)
        product_hint = ''
        if h_match:
            product_hint = re.sub(r'<[^>]+>', '', h_match.group(1)).strip()[:80]
        
        print(f'\n  Article: {article}')
        print(f'  Failed ASIN: {asin}')
        if product_hint:
            print(f'  Possible product: {product_hint}')
            # Try to find replacement ASIN
            new_asin = find_asin_by_name(product_hint[:60])
            if new_asin:
                print(f'  -> Found replacement ASIN: {new_asin}')
                fix_map.setdefault(article, []).append((asin, new_asin, product_hint))
            else:
                print(f'  -> No ASIN found, will use search link')
                fix_map.setdefault(article, []).append((asin, 'SEARCH', product_hint))
        else:
            print(f'  -> Cannot identify product name')
            fix_map.setdefault(article, []).append((asin, 'UNKNOWN', ''))
        
        time.sleep(1)
    else:
        print(f'\n  Article: {article} - ASIN {asin} not found in content (may already be fixed)')

# Write fix map
with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
    json.dump(fix_map, f, indent=2, ensure_ascii=False)

print(f'\n=== Fix map written to {RESULTS_FILE} ===')
print('Summary:')
for article, fixes in fix_map.items():
    print(f'  {article}: {len(fixes)} ASIN(s) to fix')
