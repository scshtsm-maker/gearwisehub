import re
import os

base = r'C:\Users\Administrator\gearwisehub\static\reviews'
for subdir in os.listdir(base):
    path = os.path.join(base, subdir, 'index.html')
    if not os.path.exists(path):
        continue
    with open(path, encoding='utf-8') as f:
        content = f.read()
    urls = re.findall(r'https://www\.amazon\.com/dp/[A-Z0-9]+[^\s"\'<>]*', content)
    if urls:
        print(f'--- {subdir} ---')
        for u in sorted(set(urls)):
            print(u)
