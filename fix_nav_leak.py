import os, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = r'C:\Users\Administrator\gearwisehub'
REVIEWS = os.path.join(BASE, 'static', 'reviews')

# Articles where <header> is incorrectly wrapped in <p></p>
broken_slugs = [
    'apple-airpods-pro-2-review',
    'best-noise-canceling-headphones-under-200',
    'best-wireless-earbuds-under-100',
    'best-wireless-earbuds-under-200',
    'sony-wh-1000xm5',
]

for slug in broken_slugs:
    path = os.path.join(REVIEWS, slug, 'index.html')
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    
    original = c
    
    # Pattern: <p ...> ... <header> ... </header> ... </p>
    # The <p> wraps the entire header section
    # We need to remove the opening <p...> before <header> and closing </p> after </header>
    
    # Find the <p that contains <header>
    pattern = r'(<p[^>]*>\s*)(<header.*?</header>)(\s*</p>)'
    m = re.search(pattern, c, re.DOTALL)
    
    if m:
        p_open = m.group(1)
        header_content = m.group(2)
        p_close = m.group(3)
        
        print(f'{slug}: Found header wrapped in <p>')
        print(f'  <p open>: {repr(p_open[:60])}')
        print(f'  header starts: {header_content[:60]}')
        print(f'  </p close>: {repr(p_close[:60])}')
        
        # Remove the <p> wrapper, keep only the header
        c = c[:m.start()] + '\n' + header_content + '\n' + c[m.end():]
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        
        # Verify
        still_broken = bool(re.search(r'<p[^>]*>.*?<header', c, re.DOTALL))
        has_main = '<main>' in c
        print(f'  Fixed! main={has_main}, header_still_in_p={still_broken}\n')
    else:
        print(f'{slug}: Pattern not matched\n')

print('Done!')
