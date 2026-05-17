import os, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

path = r'C:\Users\Administrator\gearwisehub\static\index.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()
print(f'File size: {len(c)} bytes')
print(f'First 80 chars: {repr(c[:80])}')

# Simpler: just find all <div class="card"> ... </div> </div> blocks
# The card ends with </div> (card-body close) + </div> (card close)
# Let's use a line-by-line approach to extract card blocks
lines = c.split('\n')
cards = []
current_card = []
in_card = False
depth = 0

for line in lines:
    stripped = line.strip()
    if '<div class="card">' in stripped:
        in_card = True
        depth = 1
        current_card = [line]
    elif in_card:
        current_card.append(line)
        # Count open/close divs
        depth += stripped.count('<div') - stripped.count('</div>')
        # Card closes when we're back to depth 0 and we see the pattern
        if depth <= 0 and '</div>' in stripped:
            cards.append('\n'.join(current_card))
            in_card = False
            current_card = []

print(f'\nExtracted {len(cards)} cards via depth tracking')
for i, card in enumerate(cards):
    title_match = re.search(r'alt="([^"]*)"', card)
    t = title_match.group(1) if title_match else '?'
    print(f'  {i+1}. {t[:60]}')
