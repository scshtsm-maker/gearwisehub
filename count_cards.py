import re
with open('static/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find any href with review or article links
links = re.findall(r'href="([^"]*)"', c)
review_links = [l for l in links if 'review' in l or 'best-' in l or 'sony' in l or 'bose' in l or 'airpods' in l or 'soundcore' in l]
print('Article links on homepage: ' + str(len(review_links)))
for l in sorted(set(review_links)):
    print('  ' + l)
