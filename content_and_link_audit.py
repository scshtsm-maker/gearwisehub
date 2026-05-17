import sys, os, re

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = r'C:\Users\Administrator\gearwisehub\static\reviews'

# 1. Fix all "htt ps://" typos in all article files
print("=== Fixing 'htt ps://' typos ===")
fixed_files = 0
for article in sorted(os.listdir(BASE)):
    art_path = os.path.join(BASE, article, 'index.html')
    if not os.path.exists(art_path):
        continue
    with open(art_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'htt ps://' in content:
        content = content.replace('htt ps://', 'https://')
        with open(art_path, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_files += 1
        print(f'  Fixed: {article}')

print(f'  Total files fixed: {fixed_files}')

# 2. Now do content quality check
print('\n=== Content Quality Check ===')

issues = []

for article in sorted(os.listdir(BASE)):
    art_path = os.path.join(BASE, article, 'index.html')
    if not os.path.exists(art_path):
        continue
    
    with open(art_path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    article_issues = []
    
    # Check for mixed Chinese/English (encoding artifacts)
    # Look for Chinese characters in body text (not JSON-LD)
    body = re.search(r'<body[^>]*>(.*?)</body>', c, re.DOTALL | re.IGNORECASE)
    if body:
        body_text = body.group(1)
        # Count Chinese characters in body
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', body_text))
        if chinese_chars > 10:
            article_issues.append(f'Chinese chars in body: {chinese_chars}')
    
    # Check for encoding artifacts
    artifacts = ['??', 'â€', 'Â', 'â€™', 'â€"', 'â€“', 'ã€', 'ã¢']
    for art in artifacts:
        if art in c:
            article_issues.append(f'Encoding artifact: {repr(art)}')
            break
    
    # Check for broken spacing (e.g. "2026 Three" instead of "In 2026, three")
    spacing_issues = re.findall(r'([a-z])([A-Z])', c)  # lowercase immediately followed by uppercase (missing space)
    if spacing_issues and len(spacing_issues) > 2:
        article_issues.append(f'Spacing issues: {len(spacing_issues)} found')
    
    # Check for "product unavailable on Amazon" warnings
    if 'unavailable on Amazon' in c or 'product unavailable' in c:
        article_issues.append('Has "product unavailable" warning')
    
    # Check for nav HTML leaking into body (e.g. <ul> inside <p>)
    if re.search(r'<p[^>]*>\s*<nav', c, re.IGNORECASE) or re.search(r'<p[^>]*>\s*<ul', c, re.IGNORECASE):
        article_issues.append('Nav/UL inside <p> tag (HTML structure issue)')
    
    # Check JSON-LD for Chinese (should be OK - it's technical)
    # Check if article title matches product mentioned
    title_match = re.search(r'<title>(.*?)</title>', c, re.IGNORECASE)
    if title_match:
        title = title_match.group(1)
        # Check if title has encoding issues
        if '??' in title or 'â' in title:
            article_issues.append(f'Title has encoding issue: {title[:60]}')
    
    if article_issues:
        issues.append((article, article_issues))
        print(f'\n  {article}:')
        for issue in article_issues:
            print(f'    - {issue}')
    else:
        print(f'  {article}: OK')

print(f'\n=== SUMMARY ===')
print(f'Articles with issues: {len(issues)} / 16')
