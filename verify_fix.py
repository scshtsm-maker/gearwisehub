import re, os
base = r'C:\Users\Administrator\gearwisehub\static'
idx = os.path.join(base, 'index.html')
with open(idx, 'r', encoding='utf-8') as f:
    c = f.read()
imgs = re.findall(r'src="(https://[^"]+)"', c)
print('=== index.html card images ===')
for i, img in enumerate(imgs):
    if 'w=400' in img: w = 'w=400 <<<< LOW'
    elif 'w=600' in img: w = 'w=600'
    else: w = 'w=1200'
    name = img.split('?')[0].split('/')[-1]
    print(f'  [{i}] {w} | {name}')
bone = os.path.join(base, 'reviews', 'best-bone-conduction-headphones-2026', 'index.html')
with open(bone, 'r', encoding='utf-8') as f:
    b = f.read()
has_new = 'photo-1545127398-14699f92334b' in b
has_old = 'photo-1606220838315' in b
print()
print('Bone conduction image check:')
print(f'  New image present: {has_new}')
print(f'  Old image removed: {not has_old}')
