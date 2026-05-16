import re, os

BASE = r'C:\Users\Administrator\gearwisehub'
REVIEWS = os.path.join(BASE, 'static', 'reviews')

# ASINs confirmed valid (from verification)
CONFIRMED = {'B09BVXT8TJ', 'B0FNWCYLZN', 'B0BS1PRC4L', 'B0FWJY183S', 'B0F1CL7LTD', 'B0D1S7D9YX', 'B0DQQT2ZS3', 'B07W6H7PY2', 'B08SHZW9MF', 'B083JRW96J', 'B0FHW4CF51', 'B0F2QWR3FB', 'B0GLX2GZ7P', 'B07MSLF5YC', 'B0D6MR7RBD', 'B0F9HTKWRD', 'B0D1J8KX2M', 'B0B7Q5XK8L', 'B0BR4D5YQH', 'B0D3HFRM2Q', 'B08F7PTF53', 'B0FNWJ4FV3', 'B0C33XXS56', 'B0CN9FTKJ4', 'B07JL1K193', 'B08Q8P69JZ', 'B0GXW4KNPB'}

NO_REPLACEMENT = {'B08R5WRY6J', 'B0D5TP8LR2', 'B0D6H3XK2M', 'B08B43KB47'}

issues = []

for slug in os.listdir(REVIEWS):
    path = os.path.join(REVIEWS, slug, 'index.html')
    if not os.path.isfile(path):
        continue
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()

    # Check Amazon links
    asins = set(re.findall(r'([A-Z0-9]{10})', c))
    amazon_asins = {a for a in asins if a.startswith('B0')}

    # Find Amazon links
    links = re.findall(r'(amazon\.com/[^\s"\'<>]+)', c)
    for link in links:
        asin = re.search(r'/(?:dp|exec/obidos/ASIN)/([A-Z0-9]{10})', link)
        tag_m = re.search(r'tag=([a-z0-9_-]+)', link)
        if asin and tag_m:
            asin_val = asin.group(1)
            tag = tag_m.group(1)
            if tag != 'cfqclaw-20':
                issues.append(f'{slug}: Wrong tag={tag} in {link[:80]}')
            elif asin_val in NO_REPLACEMENT:
                issues.append(f'{slug}: BROKEN ASIN={asin_val} in {link[:80]}')
            elif asin_val not in CONFIRMED:
                issues.append(f'{slug}: UNVERIFIED ASIN={asin_val} in {link[:80]}')

    # Check language
    lang_m = re.search(r'<html[^>]*\slang="([^"]+)"', c)
    if lang_m and lang_m.group(1) != 'en':
        issues.append(f'{slug}: Non-English lang={lang_m.group(1)}')

print(f'Total issues found: {len(issues)}')
for issue in issues:
    print(f'  {issue}')
