import sys
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\Users\Administrator\gearwisehub\static\index.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()
# Find grid section
gs = c.find('<div class="grid">')
if gs >= 0:
    print('Grid section (200 chars):')
    print(repr(c[gs:gs+200]))
else:
    print('No grid found!')
    # Show last 500 chars
    print(repr(c[-500:]))
