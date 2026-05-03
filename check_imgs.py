import re, os

base = r'C:\Users\Administrator\gearwisehub\static'

# Check index.html images
idx = os.path.join(base, 'index.html')
with open(idx, 'r', encoding='utf-8') as f:
    content = f.read()
imgs = re.findall(r'src="(https?://[^"]+)"', content)
print('=== index.html images ===')
for i, img in enumerate(imgs):
    print(f'  [{i}] {img}')

print()

# Check which articles use unsplash small vs large
articles = [
    'reviews/best-sports-headphones-2026',
    'reviews/best-gaming-headsets-2026', 
    'reviews/best-bone-conduction-headphones-2026',
]
for art in articles:
    path = os.path.join(base, art, 'index.html')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        og = re.search(r'og:image.*?content="([^"]+)"', c)
        tw = re.search(r'twitter:image.*?content="([^"]+)"', c)
        img = re.search(r'<img[^>]+src="([^"]+)"', c)
        print(f'=== {art} ===')
        if og: print(f'  og:image:   {og.group(1)}')
        if tw: print(f'  tw:image:   {tw.group(1)}')
        if img: print(f'  main img:   {img.group(1)}')

# Also check all article card images in index.html ItemList
schemas = re.findall(r'"image":\s*"([^"]+)"', content)
print()
print('=== index.html ItemList schema images ===')
for i, s in enumerate(schemas):
    print(f'  [{i}] {s}')
