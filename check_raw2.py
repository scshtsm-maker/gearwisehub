import sys
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\Users\Administrator\gearwisehub\static\index.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()
print('First 50 chars:', repr(c[:50]))
print('Starts with DOCTYPE:', c.startswith('<!DOCTYPE'))
print('File length:', len(c))
# Count cards
ct = '<div class="card">'
print('Card count:', c.count(ct))
