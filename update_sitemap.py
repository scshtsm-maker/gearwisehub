import os
from datetime import datetime

BASE = r'C:\Users\Administrator\gearwisehub'
REVIEWS = os.path.join(BASE, 'static', 'reviews')
SITEMAP = os.path.join(BASE, 'static', 'sitemap.xml')

# Get all article directories
articles = []
for slug in os.listdir(REVIEWS):
    path = os.path.join(REVIEWS, slug, 'index.html')
    if os.path.isfile(path):
        mtime = datetime.fromtimestamp(os.path.getmtime(path))
        articles.append({
            'slug': slug,
            'url': f'https://cfqclaw.dpdns.org/reviews/{slug}/',
            'lastmod': mtime.strftime('%Y-%m-%d'),
        })

# Sort by lastmod descending
articles.sort(key=lambda x: x['lastmod'], reverse=True)

# Generate sitemap
url_count = len(articles)
sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://cfqclaw.dpdns.org/</loc>
    <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://cfqclaw.dpdns.org/reviews/</loc>
    <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
'''
for a in articles:
    sitemap += f'''  <url>
    <loc>{a['url']}</loc>
    <lastmod>{a['lastmod']}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
'''

sitemap += '</urlset>'

with open(SITEMAP, 'w', encoding='utf-8') as f:
    f.write(sitemap)

print(f'Sitemap updated with {url_count} articles')
for a in articles:
    print(f'  {a["lastmod"]} | {a["slug"]}')
