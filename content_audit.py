import os, re

BASE = r'C:\Users\Administrator\gearwisehub'
REVIEWS = os.path.join(BASE, 'static', 'reviews')

slugs = sorted(os.listdir(REVIEWS))

for slug in slugs:
    path = os.path.join(REVIEWS, slug, 'index.html')
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    
    issues = []
    
    # 1. Nav/menu text leaking into body paragraphs (common template bug)
    # Check if first <p> contains nav items like "Home", "Reviews"
    paras = re.findall(r'<p[^>]*>(.*?)</p>', c, re.DOTALL)
    for i, p in enumerate(paras[:5]):
        p_text = re.sub(r'<[^>]+>', '', p).strip()
        if 'Home' in p_text and ('Reviews' in p_text or 'Buying Gui' in p_text):
            issues.append(f'Nav menu leaked into paragraph {i}: "{p_text[:80]}"')
    
    # 2. Missing spaces around em dashes or broken punctuation
    # Look for patterns like "2026 Year" without space before price
    broken_punct = []
    for pattern_name, pattern in [
        ('no-space-before-price', r'\d{4}Year'),
        ('no-space-after-punct', r'[a-zA-Z]\u201c'),  # letter directly followed by "
        ('double-year', r'\d{4}\s*\d{4}Year'),
        ('missing-space-comma', r'[a-z]\d{4}[A-Z]'),  # "2026Three"
    ]:
        matches = re.findall(pattern, c)
        if matches:
            broken_punct.append(f'{pattern_name}: {matches[:3]}')
    if broken_punct:
        for bp in broken_punct:
            issues.append(f'Broken punctuation: {bp}')
    
    # 3. Disclosure text missing proper formatting (should be in disclosure div)
    has_disclosure = bool(re.search(r'class="disclosure"', c) or re.search(r'disclosure', c.lower()))
    has_affiliate_text = 'affiliate' in c.lower() or 'commission' in c.lower()
    if has_affiliate_text and not has_disclosure:
        issues.append('Affiliate text found but no .disclosure styled box')
    
    # 4. Check for duplicate consecutive paragraphs (copy-paste error)
    body_paras = [re.sub(r'<[^>]+>', '', p).strip() for p in paras if len(re.sub(r'<[^>]+>', '', p).strip()) > 50]
    seen = set()
    dupes = []
    for bp in body_paras:
        short = bp[:80]
        if short in seen:
            dupes.append(short)
        seen.add(short)
    if dupes:
        issues.append(f'Duplicate paragraphs detected: {len(dupes)} dupes')
    
    # 5. Product count vs actual products listed
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', c, re.DOTALL)
    h1_text = re.sub(r'<[^>]+>', '', h1.group(1)).strip() if h1 else ''
    
    # 6. Check for "product unavailable" text
    unavail = re.findall(r'unavailable|not available|discontinued|no longer', c, re.I)
    if unavail:
        issues.append(f'Product availability warnings: {len(unavail)} mentions')
    
    # 7. Image alt text quality - check for empty or generic alts
    imgs = re.findall(r'<img[^>]*alt=["\']([^"\']*)["\']', c)
    empty_alts = sum(1 for a in imgs if not a.strip())
    generic_alts = sum(1 for a in imgs if a.strip() and len(a.strip()) < 10)
    if empty_alts:
        issues.append(f'{empty_alts} images with empty alt text')
    
    # 8. Word count warning (too short articles)
    word_count = len(re.findall(r'\b[a-zA-Z]+\b', c))
    if word_count < 1500:
        issues.append(f'Very short article: only ~{word_count} words')
    
    # 9. Amazon links per product ratio
    amz_links = len(re.findall(r'amazon\.com', c, re.I))
    asins = set(re.findall(r'/dp/([A-Z0-9]{10})', c))
    search_links = len(re.findall(r'amazon\.com/s\?', c, re.I))
    
    print(f'=== {slug} === ({word_count}w, {amz_links}amz, {len(asins)}ASINs, {search_links}search)')
    for iss in issues:
        print(f'  !! {iss}')
    if not issues:
        print('  OK')
    print()
