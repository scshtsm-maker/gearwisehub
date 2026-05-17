import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\Administrator\gearwisehub\static\index.html','r',encoding='utf-8') as f:
    c=f.read()
print('DOCTYPE:', c.startswith('<!DOCTYPE>'))
print('CSS:', '/style.css' in c)
print('.grid:', '<div class="grid">' in c)
ct = '<div class="card">'
print('cards total:', c.count(ct))
print('</main>:', '</main>' in c)
print('</html>:', '</html>' in c)
gs = c.find('<div class="grid">')
ge = c.find('</div>\n    </div>\n</main>')
if gs > 0 and ge > gs:
    section = c[gs:ge]
    ci = section.count(ct)
    print(f'cards inside .grid: {ci}')
else:
    print(f'grid start={gs}, grid end search={ge}')
