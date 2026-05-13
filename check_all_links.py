import os, re

base = r'C:\Users\Administrator\gearwisehub\static'
amazon_links = []

for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            rel = os.path.relpath(path, base)
            with open(path, encoding='utf-8', errors='ignore') as fh:
                content = fh.read()
            links = re.findall(r'https?://www\.amazon\.com/[^\s"\'<>]+', content)
            for link in links:
                tag_match = re.search(r'tag=([^&\s]+)', link)
                has_dp = '/dp/' in link
                asin_match = re.search(r'/dp/([A-Z0-9]{10})', link) if has_dp else None
                amazon_links.append((rel, link, tag_match.group(1) if tag_match else 'NO_TAG', asin_match.group(1) if asin_match else '-'))

print(f'Total Amazon links: {len(amazon_links)}')
print()

issues = []
groups = {}

for rel, link, tag, asin in amazon_links:
    if tag != 'cfqclaw-20':
        issues.append((rel, 'BAD TAG', link[:80], tag))
    key = rel
    if key not in groups:
        groups[key] = []
    groups[key].append((link[:80], tag, asin))

for article, links in sorted(groups.items()):
    print(f'=== {article} ===')
    for link, tag, asin in links:
        status = 'OK' if tag == 'cfqclaw-20' else f'BAD_TAG:{tag}'
        print(f'  [{status}] asin={asin} | {link}')
    print()

if issues:
    print(f'\nISSUES FOUND ({len(issues)}):')
    for rel, issue, link, tag in issues:
        print(f'  {rel}: {issue} tag={tag} | {link}')
else:
    print('All links have correct tag cfqclaw-20')
