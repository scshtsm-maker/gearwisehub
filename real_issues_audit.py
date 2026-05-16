import re, os

BASE = r'C:\Users\Administrator\gearwisehub'
REVIEWS = os.path.join(BASE, 'static', 'reviews')

DISCONTINUED = {'B08R5WRY6J','B0D5TP8LR2','B0D6H3XK2M','B08B43KB47','B0BJ682ZKT'}

slugs = sorted(os.listdir(REVIEWS))
real_issues = []
ok = []

for slug in slugs:
    path = os.path.join(REVIEWS, slug, 'index.html')
    if not os.path.isfile(path):
        ok.append(f'{slug}: NO INDEX.HTML')
        continue

    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()

    issues = []

    # 1. Discontinued ASINs still in links
    for asin in DISCONTINUED:
        if asin in c and '/dp/' + asin in c:
            issues.append(f'Discontinued ASIN {asin} still in Amazon link')

    # 2. Wrong affiliate tag
    tags = set(re.findall(r'tag=([a-z0-9_-]+)', c))
    if 'cfqclaw-20' not in tags and tags:
        issues.append(f'Wrong/missing tag: {sorted(tags)}')

    # 3. No Amazon links at all
    if not re.search(r'https?://[^\s<>"\']*amazon[^\s<>"\']+', c):
        issues.append('No Amazon affiliate links')

    # 4. Chinese characters in body content
    chinese = re.findall(r'[\u4e00-\u9fff]+', c)
    if chinese:
        issues.append(f'Chinese content: {set(chinese)}')

    # 5. Missing SEO elements
    if '<title' not in c.lower():
        issues.append('Missing <title>')
    if 'schema.org' not in c and 'schema\.org' not in c:
        issues.append('Missing JSON-LD')

    # 6. Language
    lang_m = re.search(r'lang="([^"]+)"', c)
    lang = lang_m.group(1) if lang_m else 'NONE'
    if lang != 'en':
        issues.append(f'Wrong lang: {lang}')

    if issues:
        real_issues.append((slug, issues))
    else:
        ok.append(slug)

print('=' * 60)
print('GENUINE ISSUES AUDIT')
print('=' * 60)

if real_issues:
    print()
    for slug, issues in real_issues:
        print(f'[ISSUE] {slug}')
        for i in issues:
            print(f'  - {i}')
        print()
else:
    print('All articles pass!')

print()
print('=' * 60)
print(f'Clean: {len(ok)} articles')
for s in ok:
    print(f'  [OK] {s}')
if real_issues:
    print(f'With issues: {len(real_issues)} articles')
    for s, _ in real_issues:
        print(f'  [!!] {s}')
