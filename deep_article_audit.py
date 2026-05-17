import os, re

BASE = r'C:\Users\Administrator\gearwisehub'
REVIEWS = os.path.join(BASE, 'static', 'reviews')

DISCONTINUED = {'B08R5WRY6J','B0D5TP8LR2','B0D6H3XK2M','B08B43KB47','B0BJ682ZKT'}

slugs = sorted(os.listdir(REVIEWS))
all_issues = {}

for slug in slugs:
    path = os.path.join(REVIEWS, slug, 'index.html')
    if not os.path.isfile(path):
        all_issues[slug] = ['NO INDEX.HTML']
        continue
    
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    
    issues = []
    
    # 1. Chinese chars
    cn = re.findall(r'[\u4e00-\u9fff]+', c)
    if cn:
        issues.append(f'Chinese content: {set(cn)}')
    
    # 2. Discontinued ASINs in /dp/ links
    for a in DISCONTINUED:
        if '/dp/' + a in c:
            issues.append(f'Discontinued ASIN {a} still in /dp/ link')
    
    # 3. Wrong affiliate tag
    tags = set(re.findall(r'tag=([a-z0-9_-]+)', c))
    if tags and 'cfqclaw-20' not in tags:
        issues.append(f'Wrong affiliate tag: {tags}')
    
    # 4. Title check
    title_m = re.search(r'<title>(.*?)</title>', c)
    title = title_m.group(1).strip() if title_m else ''
    if not title:
        issues.append('Empty <title>')
    
    # 5. Escaped HTML tags in content (not inside attributes)
    escaped_tags = re.findall(r'>[^<]*&lt;/?[a-z][^&]*&gt;', c)
    if escaped_tags:
        issues.append(f'Escaped HTML tags in content: {escaped_tags[:3]}')
    
    # 6. Malformed table tags
    malformed_table = re.findall(r'</?t[dh][^>]*>[^<]*(?:</td>|</th>)', c)
    # Check for things like "-- /td>" or broken patterns
    broken_td = re.findall(r'[^\w](--|__|\?\?)[^\w]*</td>', c)
    if broken_td:
        issues.append(f'Malformed table content: {broken_td[:3]}')
    
    # 7. Word count & image count
    word_count = len(re.findall(r'\b[a-zA-Z]+\b', c))
    img_count = len(re.findall(r'<img ', c))
    amz_count = len(re.findall(r'amazon\.com', c, re.I))
    
    # 8. Check for empty key sections
    has_h1 = bool(re.search(r'<h1>', c))
    has_body_content = len(re.findall(r'<p>[^<]{20,}</p>', c)) > 0
    
    if not has_h1:
        issues.append('Missing <h1> heading')
    
    # 9. Date format check (look for "2026, 2026" pattern)
    bad_dates = re.findall(r'2026,\s*2026', c)
    if bad_dates:
        issues.append(f'Bad date format: "2026, 2026" ({len(bad_dates)} occurrences)')
    
    # 10. Broken image URLs (check for unsplash with photo- pattern that might be invalid)
    unsplash_imgs = re.findall(r'(https://images\.unsplash\.com/photo-[a-z0-9]+)', c)
    
    status = 'OK' if not issues else 'ISSUE'
    print(f'[{status}] {slug}')
    print(f'       words={word_count} imgs={img_count} amazon_links={amz_count} title="{title[:65]}"')
    for i in issues:
        print(f'       !! {i}')
    print()
    
    all_issues[slug] = issues

# Summary
ok_count = sum(1 for v in all_issues.values() if not v)
print('='*60)
print(f'Total: {len(slugs)} articles | Clean: {ok_count} | Issues: {len(slugs)-ok_count}')
