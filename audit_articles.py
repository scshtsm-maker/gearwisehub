import os, re, glob

dirs = sorted(os.listdir('static/reviews'))
results = []

for d in dirs:
    path = os.path.join('static/reviews', d, 'index.html')
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Word count (rough - strip HTML)
    text = re.sub(r'<[^>]+>', ' ', c)
    text = re.sub(r'\s+', ' ', text).strip()
    words = len(text.split())
    
    # Check for Chinese content
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', c))
    
    # Check for Amazon links
    amazon_links = len(re.findall(r'amazon\.com', c))
    
    # Check for ASIN
    asins = re.findall(r'/dp/([A-Z0-9]{10})', c)
    unique_asins = list(set(asins))
    
    # Check for search links (invalid ASIN fallback)
    search_links = len(re.findall(r'amazon\.com/s\?k=', c))
    
    # JSON-LD present?
    has_jsonld = 'application/ld+json' in c
    
    # Has FAQ?
    has_faq = 'faq' in c.lower() or 'frequently' in c.lower()
    
    # Title
    title_match = re.search(r'<title>(.*?)</title>', c)
    title = title_match.group(1)[:60] if title_match else 'NO TITLE'
    
    results.append({
        'dir': d,
        'words': words,
        'chinese': chinese_chars,
        'amazon_links': amazon_links,
        'asins': unique_asins,
        'search_links': search_links,
        'has_jsonld': has_jsonld,
        'has_faq': has_faq,
        'title': title,
    })

# Sort by word count ascending to spot weak articles
results.sort(key=lambda x: x['words'])

print(f"{'Article':<50} {'Words':>5} {'CN':>4} {'ASINs':>5} {'Search':>6} {'LD':>2} {'FAQ':>3}")
print('-' * 85)
for r in results:
    asin_str = ','.join(r['asins'][:3]) + ('...' if len(r['asins']) > 3 else '')
    print(f"{r['dir']:<50} {r['words']:>5} {r['chinese']:>4} {len(r['asins']):>5} {r['search_links']:>6} {'Y' if r['has_jsonld'] else 'N':>2} {'Y' if r['has_faq'] else 'N':>3}")
