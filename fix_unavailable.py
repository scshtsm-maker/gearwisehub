import os, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = r'C:\Users\Administrator\gearwisehub'
path = os.path.join(BASE, 'static', 'reviews', 'best-wireless-earbuds-under-100', 'index.html')

with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Fix 1: OPPO Enco Air 3 - replace unavailable text with search link
# Also fix the broken "Check the  for just $10 more" sentence
old_oppo = '''        [product unavailable on Amazon US]
    </div>'''
new_oppo = '''<a class="cta-btn-sm" href="https://www.amazon.com/s?k=OPPO+Enco+Air+3+earbuds&tag=cfqclaw-20" rel="nofollow noopener" target="_blank">Check Price on Amazon →</a>
</div>'''
c = c.replace(old_oppo, new_oppo)

# Fix the broken sentence: "Check the  for just $10 more" 
c = c.replace('Need something with actual translation? Check the  for just $10 more.', 
              'Need something with actual translation? Check the Soundcore C30i for just $10 more.')

# Fix 2: JBL Vibe Buds 3 - replace unavailable text with search link
old_jbl = '''        [product unavailable on Amazon US]
    </div>'''
new_jbl = '''<a class="cta-btn-sm" href="https://www.amazon.com/s?k=JBL+Vibe+Buds+3&tag=cfqclaw-20" rel="nofollow noopener" target="_blank">Check Price on Amazon →</a>
</div>'''
c = c.replace(old_jbl, new_jbl)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

# Verify
with open(path, 'r', encoding='utf-8') as f:
    c2 = f.read()

remaining = c2.count('product unavailable')
search_links = len(re.findall(r'amazon\.com/s\?', c2))
print(f'Remaining "unavailable": {remaining}')
print(f'Amazon search links: {search_links}')
print('Done!')
