import os, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

path = r'C:\Users\Administrator\gearwisehub\static\reviews\best-wireless-earbuds-under-100\index.html'

with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

original = c
fixes = []

# Fix malformed table tags: — /td> → </td>
c2, n1 = re.subn(r'— /td>', r'</td>', c)
if n1:
    fixes.append(f'Fixed {n1}x "— /td>" → "</td>"')

# Fix: ★?/td> → </td>
c2, n2 = re.subn(r'★\?/td>', r'</td>', c2)
if n2:
    fixes.append(f'Fixed {n2}x "★?/td>" → "</td>"')

# Fix: nested <td> — e.g. <td>★★★★☆ <td>10h + 40h</td>
# Pattern: content <td>content</td></td> → content</td>
c2, n3 = re.subn(r'(<td[^>]*>[^<]*?)(<td[^>]*>)', r'\1', c2)
# Actually let's be more careful — find rows with extra <td>
# The pattern is: <td>TEXT\n<td>REAL</td></td></tr>
c2, n3 = re.subn(r'(<td[^>]*>[^<]*?)\n\s+<td', r'\1\n            </td>\n            <td', c2)
if n3:
    fixes.append(f'Fixed {n3}x nested <td> without closing')

# Fix: ★★★★☆ <td> → ★★★★☆</td> (stars rating with unclosed <td> before next <td>)
c2, n4 = re.subn(r'(★★★★[^★<]*)(\s+<td[^>]*>)', r'\1</td>\n            \2', c2)
if n4:
    fixes.append(f'Fixed {n4}x unclosed <td> after star ratings')

# Now rebuild the table properly — it's easier than surgical fixes
# Let me find the table and replace it entirely
table_start = c2.find('<table class="comparison-table">')
table_end = c2.find('</table>') + len('</table>')

if table_start > 0 and table_end > table_start:
    old_table = c2[table_start:table_end]
    
    new_table = '''<table class="comparison-table">
<thead>
<tr>
<th>Model</th>
<th>Price</th>
<th>ANC</th>
<th>Battery (buds+case)</th>
<th>Hi-Res</th>
<th>Rating</th>
</tr>
</thead>
<tbody>
<tr>
<td>Soundcore Liberty 4 NC</td>
<td class="highlight">$79.99</td>
<td class="highlight">★★★★☆</td>
<td>10h + 40h</td>
<td class="highlight">LDAC</td>
<td>4.7</td>
</tr>
<tr>
<td>OPPO Enco Air 3</td>
<td class="highlight">$39.99</td>
<td>Call only</td>
<td>6h + 28h</td>
<td>—</td>
<td>4.3</td>
</tr>
<tr>
<td>JBL Vibe Buds 3</td>
<td>$49.95</td>
<td>None</td>
<td>8h + 24h</td>
<td>—</td>
<td>4.2</td>
</tr>
<tr>
<td>EarFun Free Pro 3</td>
<td>$59.99</td>
<td>★★★★☆</td>
<td>7h + 33h</td>
<td>LDAC</td>
<td>4.4</td>
</tr>
<tr>
<td>1MORE Color Buds 3</td>
<td>$69.99</td>
<td>★★★★☆</td>
<td>8h + 28h</td>
<td>LDAC</td>
<td>4.3</td>
</tr>
</tbody>
</table>'''
    
    c2 = c2[:table_start] + new_table + c2[table_end:]
    fixes.append('Rebuilt comparison table with clean HTML')

# Fix related reviews broken link (second item missing <a>)
c2 = c2.replace(
    '''<li>
<div class="related-excerpt">AI translation for under $50 — real-time 100+ language support</div>
</li>''',
    '''<li>
<a href="https://www.amazon.com/s?k=Soundcore+C30i+translator+earbuds&tag=cfqclaw-20" rel="nofollow noopener" target="_blank">Soundcore C30i — AI Translator Earbuds</a>
<div class="related-excerpt">AI translation for under $50 — real-time 100+ language support</div>
</li>'''
)
fixes.append('Fixed broken related review link (added <a> tag)')

if c2 != original:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c2)
    print('Fixed:')
    for f_item in fixes:
        print(f'  + {f_item}')
else:
    print('No changes needed')

# Verify no more broken tags
with open(path, 'r', encoding='utf-8') as f:
    verify = f.read()

broken = re.findall(r'/td>|/tr>', verify)
print(f'\nVerification: {len(broken)} closing tag fragments found')
for b in broken[:5]:
    print(f'  "{b}"')
