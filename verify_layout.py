with open('static/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

cards = c.count('class="card"')
grid_open = c.find('<div class="grid">')
main_close = c.find('</main>')

print(f'Total cards: {cards}')

between = c[grid_open:main_close]
cards_in_grid = between.count('class="card"')
print(f'Cards inside grid (before </main>): {cards_in_grid}')

# Check if orphan cards still exist after grid close but before main
# Find the grid's closing tag
grid_end = between.rfind('</div>')
after_grid = between[grid_end:]
cards_after_grid = after_grid.count('class="card"')
print(f'Cards after grid closes but before </main>: {cards_after_grid}')

# Show structure around key points
lines = c.split('\n')
for i, line in enumerate(lines):
    stripped = line.strip()
    if ('class="grid"' in stripped or
        ('</div>' in stripped and len(stripped) < 20) or
        'class="container"' in stripped or '</main>' in stripped):
        print(f'L{i}: {stripped[:120]}')
