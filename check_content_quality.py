import sys, os, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = r'C:\Users\Administrator\gearwisehub\static\reviews'

# Check a few articles for content vs product consistency
check_articles = [
    'bose-quietcomfort-ultra-review',
    'best-sports-headphones-2026',
    'best-flagship-noise-canceling-earbuds-2026',
    'best-bone-conduction-headphones-2026',
]

for article in check_articles:
    art_path = os.path.join(BASE, article, 'index.html')
    with open(art_path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    print(f'\n{"="*60}')
    print(f'ARTICLE: {article}')
    print(f'{"="*60}')
    
    # Get title
    title_match = re.search(r'<title>(.*?)</title>', c, re.IGNORECASE)
    title = title_match.group(1) if title_match else '?'
    # Clean HTML entities
    title = re.sub(r'&#\d+;', '', title)
    print(f'Title: {title[:80]}')
    
    # Get all h2/h3 headings (product names or section names)
    headings = re.findall(r'<h([23])[^>]*>(.*?)</h[23]>', c, re.DOTALL | re.IGNORECASE)
    print(f'H2/H3 headings ({len(headings)}):')
    for level, h in headings[:8]:
        clean = re.sub(r'<[^>]+>', '', h).strip()
        clean = re.sub(r'&#\d+;', '-', clean)  # Replace numeric entities
        print(f'  H{level}: {clean[:70]}')
    
    # Get first paragraph of body text (intro)
    main = re.search(r'<main[^>]*>(.*?)</main>', c, re.DOTALL | re.IGNORECASE)
    if main:
        text = re.sub(r'<[^>]+>', ' ', main.group(1))
        text = re.sub(r'&#\d+;', '', text)  # Remove numeric entities
        text = re.sub(r'\s+', ' ', text).strip()
        print(f'Intro (first 200 chars): {text[200:400]}')
    
    # Check Amazon links - extract product context
    amazon_links = re.findall(r'href="(https?://[^"]*amazon\.com[^"]*)"', c)
    print(f'Amazon links: {len(amazon_links)}')
    for link in amazon_links[:3]:
        # Get ASIN
        asin_match = re.search(r'/dp/([A-Z0-9]{10})', link)
        if asin_match:
            print(f'  ASIN: {asin_match.group(1)}')
        else:
            print(f'  Search: {link[50:100]}')
