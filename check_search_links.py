import sys, os, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = r'C:\Users\Administrator\gearwisehub\static\reviews'

print('Checking search link format in all articles...\n')

for article in sorted(os.listdir(BASE)):
    art_path = os.path.join(BASE, article, 'index.html')
    if not os.path.exists(art_path):
        continue
    with open(art_path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Find all Amazon search links
    search_links = re.findall(r'href="(https://www\.amazon\.com/s\?[^"]*)"', c)
    if search_links:
        print(f'{article}:')
        for link in search_links:
            # Check if URL is well-formed
            if ' ' in link:
                print(f'  MALFORMED (space in URL): {link[:100]}')
            elif '%20' not in link and '+' not in link and ' ' not in link:
                print(f'  OK: {link[:100]}')
            else:
                print(f'  Search link: {link[:100]}')
        print()
