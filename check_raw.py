import sys
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\Users\Administrator\gearwisehub\static\index.html'
with open(path, 'rb') as f:
    raw = f.read(100)
print('First 100 bytes (hex):', raw[:50].hex())
print('First 100 bytes (repr):', repr(raw[:100]))
print('Starts with <!DOCTYPE:', raw.startswith(b'<!DOCTYPE>'))
