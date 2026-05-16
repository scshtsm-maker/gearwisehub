import os, re

BASE = r'C:\Users\Administrator\gearwisehub'
INDEX = os.path.join(BASE, 'static', 'index.html')

IMAGE_MAP = {
    'best-bone-conduction-headphones-2026': '35599938',
    'best-budget-headphones-2026': '164397',
    'best-gaming-headsets-2026': '18542277',
    'best-noise-canceling-headphones-under-200': '2956951',
    'best-running-headphones-2026': '4009456',
    'best-sports-headphones-2026': '32940456',
    'best-headphones-for-small-ears': '3759959',
    'best-wireless-earbuds-under-100': '4526407',
    'best-wireless-earbuds-under-200': '1618277',
}

ARTICLES = [
    'best-bone-conduction-headphones-2026',
    'best-budget-headphones-2026',
    'best-gaming-headsets-2026',
    'best-noise-canceling-headphones-under-200',
    'best-running-headphones-2026',
    'best-sports-headphones-2026',
    'best-headphones-for-small-ears',
    'best-wireless-earbuds-under-100',
    'best-wireless-earbuds-under-200',
]

REVIEWS_DIR = os.path.join(BASE, 'static', 'reviews')

# Extract article data from HTML files
articles_data = []
for slug in ARTICLES:
    path = os.path.join(REVIEWS_DIR, slug, 'index.html')
    if not os.path.exists(path):
        print(f'SKIP: {slug} (no file)')
        continue
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    title_m = re.search(r'<title>([^<]+)</title>', content)
    lang_m = re.search(r'<html[^>]*\slang="([^"]+)"', content)
    title = title_m.group(1).replace(' | GearwiseHub', '').replace(' - GearwiseHub', '').strip() if title_m else slug
    lang = lang_m.group(1) if lang_m else 'en'

    pexels_id = IMAGE_MAP.get(slug, '164397')
    img_url = f'https://images.pexels.com/photos/{pexels_id}/pexels-photo-{pexels_id}.jpeg?auto=compress&cs=tinysrgb&w=600'

    if lang != 'en':
        print(f'WARNING: {slug} has lang={lang} - needs translation!')

    articles_data.append({
        'slug': slug,
        'title': title,
        'lang': lang,
        'img_url': img_url,
    })

print(f'Articles: {len(articles_data)}')

# Read index.html
with open(INDEX, 'r', encoding='utf-8', errors='ignore') as f:
    index_content = f.read()

# Build new cards HTML
new_cards = ''
for a in articles_data:
    card = f'''
            <div class="card">
                <img src="{a["img_url"]}" alt="{a["title"]}" width="600" height="300" loading="lazy">
                <div class="card-body">
                    <div class="card-cat">Buying Guide</div>
                    <h2 class="card-title"><a href="/reviews/{a["slug"]}/">{a["title"]}</a></h2>
                    <p class="card-excerpt"></p>
                    <div class="card-meta"><span><time datetime="2026-05-16">May 16, 2026</time></span><span>10 min read</span></div>
                </div>
            </div>'''
    new_cards += card

# Find the grid-closing </div> - it's the </div> that closes .grid div
# Looking for the pattern: 8 spaces + </div> followed by </div> (no spaces)
# In the file: "        </div>" then "\n</div>"
grid_close = '        </div>\n</div>'
pos = index_content.find(grid_close)
if pos >= 0:
    insert_at = pos + len(grid_close)
    new_index = index_content[:insert_at] + new_cards + index_content[insert_at:]
    with open(INDEX, 'w', encoding='utf-8') as f:
        f.write(new_index)
    print(f'SUCCESS: Added {len(articles_data)} cards to index.html')
else:
    print('ERROR: Could not find grid close pattern')
    # Try alternate: just find the last </div> in a grid context
    idx = index_content.rfind('        </div>')
    if idx >= 0:
        print(f'Found alternate at {idx}')
