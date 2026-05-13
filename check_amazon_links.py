import re
import os

files = [
    r'C:\Users\Administrator\gearwisehub\static\reviews\best-flagship-noise-canceling-earbuds-2026\index.html',
    r'C:\Users\Administrator\gearwisehub\static\reviews\best-over-ear-noise-canceling-headphones-2026\index.html',
    r'C:\Users\Administrator\gearwisehub\static\reviews\apple-airpods-full-comparison-2026\index.html',
]

for f in files:
    print(f'=== {os.path.basename(os.path.dirname(f))} ===')
    with open(f, encoding='utf-8') as fp:
        content = fp.read()
    urls = re.findall(r'https://www\.amazon\.com[^\s"\'<>]+', content)
    seen = set()
    for u in sorted(set(urls)):
        if u not in seen:
            seen.add(u)
            print(u)
    print()
