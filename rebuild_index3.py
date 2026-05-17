import os, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

path = r'C:\Users\Administrator\gearwisehub\static\index.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Extract cards via depth tracking
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
        depth += stripped.count('<div') - stripped.count('</div>')
        if depth <= 0 and '</div>' in stripped:
            cards.append('\n'.join(current_card))
            in_card = False
            current_card = []

print(f'Extracted {len(cards)} cards')

# Build new index.html with proper document structure
parts = []

# HTML head
parts.append('<!DOCTYPE html>')
parts.append('<html lang="en">')
parts.append('<head>')
parts.append('    <meta charset="UTF-8">')
parts.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
parts.append('    <meta name="description" content="Gearwise Hub &mdash; Expert headphone reviews and buying guides. Tested 50+ audio devices in 2026. Honest reviews, no fluff.">')
parts.append('    <meta name="keywords" content="headphone reviews, best headphones 2026, wireless earbuds, noise canceling headphones, audio reviews">')
parts.append('    <meta name="theme-color" content="#1a73e8">')
parts.append('    <title>Gearwise Hub &mdash; Headphone Reviews &amp; Buying Guides</title>')
parts.append('    <link rel="icon" type="image/svg+xml" href="/logo.svg">')
parts.append('    <link rel="apple-touch-icon" href="/apple-touch-icon.svg">')
parts.append('    <link rel="stylesheet" href="/style.css">')
parts.append('    <meta property="og:type" content="website">')
parts.append('    <meta property="og:site_name" content="Gearwise Hub">')
parts.append('    <meta property="og:title" content="Gearwise Hub &mdash; Headphone Reviews &amp; Buying Guides">')
parts.append('    <meta property="og:description" content="Expert headphone reviews and buying guides. Tested 50+ audio devices in 2026.">')
parts.append('    <meta property="og:url" content="https://cfqclaw.dpdns.org/">')
parts.append('    <meta property="og:image" content="https://images.pexels.com/photos/32940456/pexels-photo-32940456.jpeg?auto=compress&amp;cs=tinysrgb&amp;w=600"/>')
parts.append('    <meta name="twitter:card" content="summary_large_image">')
parts.append('    <meta name="twitter:title" content="Gearwise Hub &mdash; Headphone Reviews &amp; Buying Guides">')
parts.append('    <meta name="twitter:description" content="Expert headphone reviews and buying guides. Tested 50+ audio devices in 2026.">')
parts.append('    <meta name="twitter:image" content="https://images.pexels.com/photos/32940456/pexels-photo-32940456.jpeg?auto=compress&amp;cs=tinysrgb&amp;w=600"/>')
parts.append('</head>')

# Body
parts.append('<body>')
parts.append('<a class="skip-link" href="#main">Skip to content</a>')

# Header
parts.append('<header>')
parts.append('<div class="header-inner">')
parts.append('<a aria-label="Gearwise Hub Home" class="logo" href="/">')
parts.append('<svg aria-hidden="true" viewbox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><rect fill="#1a73e8" height="32" rx="6" width="32"></rect><path d="M8 16h16M16 8v16" stroke="#fff" stroke-linecap="round" stroke-width="2.5"></path></svg>')
parts.append('            Gearwise Hub')
parts.append('        </a>')
parts.append('<button aria-expanded="false" aria-label="Toggle menu" class="menu-toggle">')
parts.append('<span></span><span></span><span></span>')
parts.append('</button>')
parts.append('<nav aria-label="Main navigation" id="main-nav">')
parts.append('<a href="/">Home</a>')
parts.append('<a href="/categories/reviews/">Reviews</a>')
parts.append('<a href="/categories/guides/">Buying Guides</a>')
parts.append('<a href="/about/">About</a>')
parts.append('</nav>')
parts.append('</div>')
parts.append('</header>')

# Main content
parts.append('<main id="main">')
parts.append('<div class="container">')
parts.append('    <h2 class="section-title">Featured Reviews</h2>')
parts.append('    <p class="section-sub">Hand-tested, thoroughly researched &mdash; no fluff, just facts.</p>')
parts.append('    <div class="grid">')

# Add all cards inside grid
for card in cards:
    parts.append(card)

parts.append('    </div>')
parts.append('</div>')
parts.append('</main>')

# Footer
parts.append('<footer>')
parts.append('<div class="footer-links">')
parts.append('<a href="/">Home</a>')
parts.append('<a href="/categories/reviews/">Reviews</a>')
parts.append('<a href="/categories/guides/">Buying Guides</a>')
parts.append('<a href="/about/">About</a>')
parts.append('<a href="/privacy/">Privacy Policy</a>')
parts.append('<a href="/terms/">Terms of Use</a>')
parts.append('</div>')
parts.append('<p>&copy; 2026 Gearwise Hub. All rights reserved.<br/>')
parts.append('<span style="font-size:12px;margin-top:8px;display:inline-block">As an Amazon Associate we earn from qualifying purchases.</span></p>')
parts.append('</footer>')

# JS
parts.append('<script>')
parts.append('const menuToggle = document.querySelector(".menu-toggle");')
parts.append('const mainNav = document.getElementById("main-nav");')
parts.append('if (menuToggle && mainNav) {')
parts.append('    menuToggle.addEventListener("click", function() {')
parts.append('        const expanded = this.getAttribute("aria-expanded") === "true";')
parts.append('        this.setAttribute("aria-expanded", !expanded);')
parts.append('        this.classList.toggle("open");')
parts.append('        mainNav.classList.toggle("open");')
parts.append('    });')
parts.append('    mainNav.querySelectorAll("a").forEach(function(link) {')
parts.append('        link.addEventListener("click", function() {')
parts.append('            menuToggle.setAttribute("aria-expanded", "false");')
parts.append('            menuToggle.classList.remove("open");')
parts.append('            mainNav.classList.remove("open");')
parts.append('        });')
parts.append('    });')
parts.append('}')
parts.append('</script>')

parts.append('</body>')
parts.append('</html>')

new_html = '\n'.join(parts) + '\n'

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_html)

# Verify
with open(path, 'r', encoding='utf-8') as f:
    v = f.read()

print('\n=== Verification ===')
print('Starts with DOCTYPE:', v.startswith('<!DOCTYPE>'))
print('Has CSS:', '/style.css' in v)
print('Has header:', '<header>' in v)
print('Has footer:', '<footer>' in v)
print('Has </html>:', v.rstrip().endswith('</html>'))
ct = '<div class="card">'
total_cards = v.count(ct)
print(f'Total cards: {total_cards}')
gs = v.find('<div class="grid">')
ge = v.find('</div>\n    </div>\n</main>')
if gs > 0 and ge > gs:
    grid_section = v[gs:ge]
    ci = grid_section.count(ct)
    print(f'Cards inside .grid: {ci}')
print(f'File size: {len(v)} bytes')
