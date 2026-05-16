import re

PATH = r'C:\Users\Administrator\gearwisehub\static\index.html'

with open(PATH, 'r', encoding='utf-8') as f:
    c = f.read()

original = c

# The problem: the 9 restored cards are OUTSIDE the .grid and .container divs
# Structure is currently:
#   <div class="container"> ... <div class="grid"> [7 cards] </div> </div> [9 orphan cards] </main>
#
# We need to move the 9 orphan cards INSIDE the .grid div
# Target structure:
#   <div class="container"> ... <div class="grid"> [16 cards] </div> </div> </main>

# Find the orphan cards section - they start right after </div>\n</div>\n (grid close + container close)
# and end before </main>

# Step 1: Extract the orphan cards
pattern = r'(<div class="container">.*?<div class="grid">)(.*?)(</div>\s*</div>)((?:\s*<div class="card">.*?</div>\s*)+)(</main>)'
m = re.search(pattern, c, re.DOTALL)

if m:
    before_grid = m.group(1)       # <div class="container">...<div class="grid">
    inside_grid = m.group(2)        # original 7 cards
    close_tags = m.group(3)         # </div></div> (grid + container close)
    orphan_cards = m.group(4)        # 9 orphan cards with whitespace
    after_main = m.group(5)         # </main>

    print(f'Found {len(re.findall(r"class=\"card\"", inside_grid))} cards inside grid')
    print(f'Found {len(re.findall(r"class=\"card\"", orphan_cards))} orphan cards outside')

    # Rebuild: put ALL cards inside grid, then close grid + container
    new_c = before_grid + inside_grid + orphan_cards.strip() + '\n        ' + close_tags + '\n' + after_main

    if new_c != c:
        with open(PATH, 'w', encoding='utf-8') as f:
            f.write(new_c)
        print('Fixed: All 16 cards are now inside .grid')
    else:
        print('No changes made')
else:
    print('Pattern not matched - checking alternative structure...')
    # Debug: find where grid closes
    grid_close = c.find('</div>\n        </div>')
    if grid_close > 0:
        print(f'Grid closes at position {grid_close}')
        print(f'Context around close: ...{c[grid_close-50:grid_close+80]}...')
