import re, os, urllib.request, urllib.error, time

BASE = r'C:\Users\Administrator\gearwisehub'
REVIEWS = os.path.join(BASE, 'static', 'reviews')

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36'}

def check_url(url, timeout=5):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        resp = urllib.request.urlopen(req, timeout=timeout)
        return resp.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return f'ERR:{type(e).__name__}'

# Get all article slugs
slugs = sorted(os.listdir(REVIEWS))
print(f'Total articles: {len(slugs)}\n')

issues = []
all_checks = []

for slug in slugs:
    path = os.path.join(REVIEWS, slug, 'index.html')
    if not os.path.isfile(path):
        continue

    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()

    article_issues = []

    # 1. Amazon links
    amazon_links = re.findall(r'(https?://(?:www\.)?amazon\.[^\s"\'<>]+)', c)
    for url in amazon_links:
        asin_m = re.search(r'/(?:dp|exec/obidos/ASIN)/([A-Z0-9]{10})', url)
        tag_m = re.search(r'tag=([a-z0-9_-]+)', url)
        if asin_m and tag_m:
            asin = asin_m.group(1)
            tag = tag_m.group(1)
            if tag != 'cfqclaw-20':
                article_issues.append(f'  [AMAZON] Wrong tag: {tag}')
            # spot check: test first link only per article to save time
            break

    # Test up to 3 Amazon links per article
    for url in amazon_links[:3]:
        status = check_url(url)
        if status != 200:
            article_issues.append(f'  [AMAZON HTTP {status}] {url[:80]}')

    # 2. Unsplash images
    unsplash_urls = re.findall(r'(https?://images\.unsplash\.com/[^\s"\'<>]+)', c)
    for url in unsplash_urls[:3]:
        status = check_url(url)
        if status != 200:
            article_issues.append(f'  [IMAGE HTTP {status}] {url[:80]}')

    # 3. Internal links
    internal_links = re.findall(r'href="(/[^\s"\'<>]+)"', c)
    for link in internal_links[:5]:
        full_url = f'https://cfqclaw.dpdns.org{link}'
        status = check_url(full_url)
        if status == 400:  # SSL issue - ignore
            pass
        elif status != 200:
            article_issues.append(f'  [INTERNAL HTTP {status}] {link}')

    # 4. HTML structure issues
    if '<html' not in c:
        article_issues.append(f'  [HTML] Missing <html> tag')
    if 'lang="en"' not in c and 'lang=\'en\'' not in c:
        article_issues.append(f'  [LANG] lang="en" not found')
    if '<main' not in c:
        article_issues.append(f'  [HTML] Missing <main> tag')

    # 5. Broken HTML patterns
    bad_tags = re.findall(r'(&lt;|&gt;|<>|"">)', c[:500])
    if bad_tags:
        article_issues.append(f'  [ENCODING] Possible encoded HTML entities found')

    # 6. Amazon ASINs used but broken
    asins = re.findall(r'/dp/([A-Z0-9]{10})', ' '.join(amazon_links))
    known_discontinued = {'B08R5WRY6J', 'B0D5TP8LR2', 'B0D6H3XK2M', 'B08B43KB47', 'B0BJ682ZKT'}
    for asin in asins:
        if asin in known_discontinued:
            article_issues.append(f'  [ASIN] Known discontinued ASIN {asin} still in link')

    all_checks.append({'slug': slug, 'issues': article_issues})
    if article_issues:
        issues.extend([(slug, i) for i in article_issues])

print('=' * 60)
print('AUDIT RESULTS')
print('=' * 60)

for result in all_checks:
    if result['issues']:
        print(f"\n❌ {result['slug']}")
        for issue in result['issues']:
            print(issue)
    else:
        print(f'✅ {result["slug"]}')

print(f'\n{"=" * 60}')
print(f'Total: {len(slugs)} articles, {len(issues)} issues found')
