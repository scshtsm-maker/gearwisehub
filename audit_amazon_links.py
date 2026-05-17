import os, re, sys, urllib.request, urllib.error, json

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = r'C:\Users\Administrator\gearwisehub\static\reviews'
RESULTS_FILE = r'C:\Users\Administrator\gearwisehub\link_audit_results.txt'

# Step 1: Extract all Amazon links from all articles
all_links = []  # (article, url, context_text)

for article in sorted(os.listdir(BASE)):
    art_path = os.path.join(BASE, article, 'index.html')
    if not os.path.exists(art_path):
        continue
    with open(art_path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Find all Amazon links
    for m in re.finditer(r'href="(https?://[^"]*amazon\.com[^"]*)"', c):
        url = m.group(1)
        # Get surrounding text for context
        start = max(0, m.start() - 100)
        end = min(len(c), m.end() + 50)
        context = c[start:end].replace('\n', ' ').strip()
        all_links.append((article, url, context))

# Also find ASINs in /dp/ format
dp_links = [l for l in all_links if '/dp/' in l[1]]
search_links = [l for l in all_links if '/s?' in l[1]]
other_links = [l for l in all_links if l not in dp_links and l not in search_links]

print(f'Total Amazon links: {len(all_links)}')
print(f'  /dp/ (direct): {len(dp_links)}')
print(f'  /s? (search): {len(search_links)}')
print(f'  other: {len(other_links)}')

# Step 2: Test each direct link
results = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

def test_url(url):
    """Test URL, return (status, final_url, error)"""
    req = urllib.request.Request(url, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=8)
        return (resp.status, resp.geturl(), None)
    except urllib.error.HTTPError as e:
        return (e.code, getattr(e, 'url', url), str(e.code))
    except Exception as e:
        return (0, url, str(e)[:80])

# Test all dp links
print(f'\n=== Testing {len(dp_links)} direct Amazon links ===')
for i, (article, url, ctx) in enumerate(dp_links):
    status, final_url, err = test_url(url)
    # Extract ASIN from URL
    asin_match = re.search(r'/dp/([A-Z0-9]{10})', url)
    asin = asin_match.group(1) if asin_match else '?'
    
    # Check if redirected
    redirected = final_url != url
    
    results.append({
        'type': 'direct',
        'article': article,
        'asin': asin,
        'url': url,
        'status': status,
        'final_url': final_url,
        'error': err,
        'redirected': redirected,
    })
    
    icon = 'OK' if status == 200 else ('REDIR' if redirected and status == 200 else 'FAIL')
    print(f'  [{i+1}/{len(dp_links)}] {icon} {status} | {asin} | {article[:40]}')
    
    # Small delay to be polite
    import time; time.sleep(0.3)

# Test a sample of search links (just check they don't 404)
print(f'\n=== Testing {len(search_links)} search links (sample) ===')
search_results = []
for i, (article, url, ctx) in enumerate(search_links[:10]):  # Sample first 10
    status, final_url, err = test_url(url)
    icon = 'OK' if status == 200 else 'FAIL'
    print(f'  [{i+1}] {icon} {status} | {article[:40]}')
    search_results.append({'article': article, 'status': status, 'url': url[:80]})
    time.sleep(0.3)

# Write full results
with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
    json.dump({
        'summary': {
            'total_links': len(all_links),
            'direct_links': len(dp_links),
            'search_links': len(search_links),
            'other_links': len(other_links),
        },
        'direct_results': results,
        'search_sample': search_results,
        'all_dp_links': [(a, u, c[:60]) for a, u, c in dp_links],
        'all_search_links': [(a, u[:100], c[:60]) for a, u, c in search_links],
    }, f, indent=2, ensure_ascii=False)

# Summary
ok_count = sum(1 for r in results if r['status'] == 200 and not r['redirected'])
redir_count = sum(1 for r in results if r['status'] == 200 and r['redirected'])
fail_count = sum(1 for r in results if r['status'] != 200)
print(f'\n=== SUMMARY ===')
print(f'Direct links: {ok_count} OK, {redir_count} redirected, {fail_count} FAIL')
