import re, os

BASE = r'C:\Users\Administrator\gearwisehub'

# Articles missing <main> tag
TO_FIX = [
    'best-running-headphones-2026',
    'bose-quietcomfort-ultra-review',
]

for slug in TO_FIX:
    path = os.path.join(BASE, 'static', 'reviews', slug, 'index.html')
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()

    original = c

    # Strategy: wrap the main content in <main> tags
    # Look for the nav/header section and wrap everything after it
    # Find <body...> then look for the first <header or <nav
    body_m = re.search(r'(<body[^>]*>)', c)
    if not body_m:
        print(f'{slug}: No <body> found - skipping')
        continue

    body_start = body_m.end()

    # Find the first main content block (look for first <section or <div after body)
    # We'll insert <main> after body start and </main> before </body>
    # But we need to find where to close it - before </body>
    body_end_m = re.search(r'(</body>)', c)
    if not body_end_m:
        print(f'{slug}: No </body> found - skipping')
        continue

    body_end_pos = body_end_m.start()

    # Check if <main> already exists (just not detected)
    if '<main' in c[body_start:body_end_pos]:
        print(f'{slug}: <main> actually exists in content - just needs wrapping properly')
        # Just add <main> before the first child element after body
        # and </main> before </body>
        content_after_body = c[body_start:]
        if content_after_body.startswith('</main>'):
            print(f'  Already has </main> at start - might be closed elsewhere')
        print(f'  Content after body: {content_after_body[:200]}')
        continue

    # Insert <main> right after <body...>
    c = c[:body_start] + '<main>\n' + c[body_start:]

    # Find new body end position
    body_end_m2 = re.search(r'(</body>)', c)
    body_end_pos2 = body_end_m2.start()

    # Insert </main> before </body>
    c = c[:body_end_pos2] + '</main>\n' + c[body_end_pos2:]

    if c != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f'{slug}: Fixed - <main> tags added')
    else:
        print(f'{slug}: No changes made')
