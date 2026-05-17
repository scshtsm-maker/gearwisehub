import os, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = r'C:\Users\Administrator\gearwisehub'
REVIEWS = os.path.join(BASE, 'static', 'reviews')

slugs = sorted(os.listdir(REVIEWS))
all_issues = {}

for slug in slugs:
    path = os.path.join(REVIEWS, slug, 'index.html')
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    
    issues = []
    
    # 1. Nav menu leaking into body
    paras = re.findall(r'<p[^>]*>(.*?)</p>', c, re.DOTALL)
    for i, p in enumerate(paras[:5]):
        p_text = re.sub(r'<[^>]+>', '', p).strip()
        if len(p_text) > 10 and ('Home' in p_text and ('Reviews' in p_text or 'Buying Gui' in p_text or 'About' in p_text)):
            issues.append(f'Nav menu leaked into <p> tag (para {i})')
    
    # 2. Broken punctuation / missing spaces
    if re.search(r'\d{4}Year', c):
        cnt = len(re.findall(r'\d{4}Year', c))
        issues.append(f'Missing space: "{cnt}x 2026Year" (should be "2026 Year")')
    
    if re.search(r'[a-z]\d{4}[A-Z]', c) or re.search(r'\d{4}[A-Z][a-z]+', c):
        matches = re.findall(r'.{10}\d{4}[A-Z].{10}', c)
        issues.append(f'Missing space before/after year: {len(matches)} spots')
    
    # 3. Duplicate paragraphs
    body_paras = [re.sub(r'<[^>]+>', '', p).strip() for p in paras if len(re.sub(r'<[^>]+>', '', p).strip()) > 60]
    seen = set()
    dupes = []
    for bp in body_paras:
        short = bp[:100]
        if short in seen:
            dupes.append(short[:60])
        seen.add(short)
    if dupes:
        issues.append(f'{len(dupes)} duplicate paragraph(s)')
    
    # 4. Product unavailable text
    unavail = re.findall(r'(?:product\s+)?(?:is\s+)?(?:unavailable|not\s+available|discontinued|no\s+longer)', c, re.I)
    if unavail:
        issues.append(f'Product unavailable warning ({len(unavail)} mentions)')
    
    # 5. Word count
    word_count = len(re.findall(r'\b[a-zA-Z]+\b', c))
    if word_count < 1500:
        issues.append(f'Very short: ~{word_count} words')
    
    # 6. Amazon links vs products
    amz_links = len(re.findall(r'amazon\.com', c, re.I))
    asins = set(re.findall(r'/dp/([A-Z0-9]{10})', c))
    search_links = len(re.findall(r'amazon\.com/s\?', c, re.I))
    
    # 7. Empty card excerpts on homepage (check if article has intro para)
    has_intro = any(len(re.sub(r'<[^>]+>', '', p).strip()) > 80 for p in paras[:3])
    
    status = 'ISSUE' if issues else 'OK'
    print(f'[{status}] {slug}')
    print(f'      words={word_count} amazon={amz_links} ASINs={len(asins)} search={search_links}')
    for iss in issues:
        print(f'      ! {iss}')
    print()
    
    all_issues[slug] = {'issues': issues, 'words': word_count, 'amz': amz_links, 'asins': asins}

# Summary
ok = sum(1 for v in all_issues.values() if not v['issues'])
print('='*60)
print(f'Total: {len(slugs)} | Clean: {ok} | Issues: {len(slugs)-ok}')
for slug, data in all_issues.items():
    if data['issues']:
        print(f'  - {slug}: {data["issues"]}')
