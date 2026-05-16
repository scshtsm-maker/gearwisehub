import re

PATH = r'C:\Users\Administrator\gearwisehub\static\index.html'

with open(PATH, 'r', encoding='utf-8') as f:
    c = f.read()

original = c

# Fix "2026, 2026" dates - these came from broken datetime attributes
# Pattern: <time datetime="2026, 2026">2026, 2026</time>
bad_dates = re.findall(r'<time datetime="([^"]+)">', c)
print('Current datetime values:')
for d in sorted(set(bad_dates)):
    print(f'  {d}')

# Fix: replace bad datetime values with proper ISO format
# The original articles had dates like "2026-05-02" but got corrupted
c = re.sub(
    r'datetime="2026, 2026"',
    'datetime="2026-05-02"',
    c
)
# Also fix the display text
c = re.sub(
    r'>2026, 2026<',
    '>May 2, 2026<',
    c
)

if c != original:
    with open(PATH, 'w', encoding='utf-8') as f:
        f.write(c)
    print('\nFixed: Date formats corrected')
else:
    print('\nNo date fixes needed')

# Also check for empty excerpts
excerpts = re.findall(r'<p class="card-excerpt">(.*?)</p>', c, re.DOTALL)
empty_count = sum(1 for e in excerpts if not e.strip())
print(f'\nEmpty excerpts: {empty_count}/{len(excerpts)}')

# Check image usage
images = re.findall(r'src="(https://[^"]+)"', c)
from collections import Counter
img_counts = Counter(images)
print('\nImage usage:')
for img, count in img_counts.most_common():
    fname = img.split('/')[-1].split('?')[0]
    print(f'  {count}x: {fname}')
