import re, os, sys

BASE = r'C:\Users\Administrator\gearwisehub'
REVIEWS = os.path.join(BASE, 'static', 'reviews')
OUTFILE = os.path.join(BASE, 'audit_static.txt')

DISCONTINUED = {'B08R5WRY6J','B0D5TP8LR2','B0D6H3XK2M','B08B43KB47','B0BJ682ZKT'}

slugs = sorted(os.listdir(REVIEWS))
lines = []

def log(msg):
    lines.append(msg)

log('=' * 65)
log('STATIC AUDIT RESULTS')
log('=' * 65)
log('')

ok_list = []
fail_list = []

for slug in slugs:
    path = os.path.join(REVIEWS, slug, 'index.html')
    if not os.path.isfile(path):
        log(f'[SKIP] {slug} - no index.html')
        continue

    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()

    issues = []

    # 1. Amazon ASIN links
    asins = re.findall(r'/dp/([A-Z0-9]{10})', c)
    tags = set(re.findall(r'tag=([a-z0-9_-]+)', c))
    for asin in set(asins):
        if asin in DISCONTINUED:
            issues.append(f'  [ASIN] Discontinued ASIN {asin} still present!')
    if 'cfqclaw-20' not in tags:
        issues.append(f'  [TAG] Missing cfqclaw-20 tag (found: {sorted(tags)})')

    # 2. Structure
    if '<html' not in c.lower():
        issues.append('  [HTML] Missing <html>')
    lang_m = re.search(r'lang="([^"]+)"', c)
    lang = lang_m.group(1) if lang_m else 'NONE'
    if lang != 'en':
        issues.append(f'  [LANG] Not en (lang={lang})')
    if '<main' not in c:
        issues.append('  [HTML] Missing <main>')
    if '<title' not in c.lower():
        issues.append('  [SEO] Missing <title>')
    if 'schema.org' not in c:
        issues.append('  [SEO] Missing JSON-LD schema')
    amazon_links_count = len(re.findall(r'https?://[^\s<>"\']*amazon[^\s<>"\']+', c))
    if amazon_links_count == 0:
        issues.append('  [ASIN] No Amazon links found!')

    # 3. Encoding issues
    if '&lt;' in c or '&gt;' in c:
        issues.append('  [ENCODING] HTML entity &lt;/&gt; in content')
    if '&#' in c:
        issues.append('  [ENCODING] Numeric HTML entities &#...; in content')
    if '漏' in c or '中' in c or '文' in c:
        issues.append('  [LANG] Chinese characters found in content')

    # 4. HTML structure
    divs = len(re.findall(r'<div', c))
    if divs == 0:
        issues.append('  [HTML] No <div> tags - possible template issue')

    asin_count = len(set(asins))
    if issues:
        log(f'[FAIL] {slug} ({asin_count} ASINs)')
        for i in issues:
            log(i)
        fail_list.append(slug)
    else:
        log(f'[OK]   {slug} ({asin_count} ASINs)')
        ok_list.append(slug)

log('')
log('=' * 65)
log(f'Results: {len(ok_list)} OK  {len(fail_list)} FAIL  / {len(slugs)} total')
if fail_list:
    log('')
    log('Articles with issues:')
    for s in fail_list:
        log(f'  - {s}')

result = '\n'.join(lines)
print(result)

with open(OUTFILE, 'w', encoding='utf-8') as f:
    f.write(result)
