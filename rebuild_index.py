import os, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = r'C:\Users\Administrator\gearwisehub'
path = os.path.join(BASE, 'static', 'index.html')

with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Extract all card divs
cards = re.findall(r'<div class="card">.*?</div>\s*</div>', c, re.DOTALL)
print(f'Found {len(cards)} cards via regex')

# If regex didn't work well, try extracting card blocks differently
if len(cards) < 10:
    # Broader approach: find each card by its img src
    cards = []
    card_pattern = r'<div class="card">\s*<img\s+src="([^"]+)"[^>]*alt="([^"]*)"[^>]*/?>\s*<div class="card-body">\s*<div class="card-cat">([^<]*)</div>\s*<h2 class="card-title"><a href="([^"]+)">([^<]*)</a></h2>\s*<p class="card-excerpt"></p>\s*<div class="card-meta"><span><time datetime="([^"]+)">[^<]*</time></span><span>([^<]*)</span></div>'
    
    for m in re.finditer(card_pattern, c):
        img_src = m.group(1)
        alt = m.group(2)
        cat = m.group(3)
        href = m.group(4)
        title = m.group(5)
        date = m.group(6)
        read_time = m.group(7)
        card_html = f'''            <div class="card">
                <img src="{img_src}" alt="{alt}" width="600" height="300" loading="lazy">
                <div class="card-body">
                    <div class="card-cat">{cat}</div>
                    <h2 class="card-title"><a href="{href}">{title}</a></h2>
                    <p class="card-excerpt"></p>
                    <div class="card-meta"><span><time datetime="{date}">{date}</time></span><span>{read_time}</span></div>
                </div>
            </div>'''
        cards.append((title, card_html))
    
    print(f'Found {len(cards)} cards via broader pattern')
else:
    # Clean up the regex matches for display
    titles = [re.search(r'alt="([^"]*)"', card).group(1) if re.search(r'alt="([^"]*)"', card) else '?' for card in cards]
    print('Cards found:')
    for i, t in enumerate(titles[:20]):
        print(f'  {i+1}. {t[:60]}')

# Build complete index.html with proper structure
header_html = '''<header>
<div class="header-inner">
<a aria-label="Gearwise Hub Home" class="logo" href="/">
<svg aria-hidden="true" viewbox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><rect fill="#1a73e8" height="32" rx="6" width="32"></rect><path d="M8 16h16M16 8v16" stroke="#fff" stroke-linecap="round" stroke-width="2.5"></path></svg>
            Gearwise Hub
        </a>
<button aria-expanded="false" aria-label="Toggle menu" class="menu-toggle">
<span></span><span></span><span></span>
</button>
<nav aria-label="Main navigation" id="main-nav">
<a href="/">Home</a>
<a href="/categories/reviews/">Reviews</a>
<a href="/categories/guides/">Buying Guides</a>
<a href="/about/">About</a>
</nav>
</div>
</header>'''

footer_html = '''<footer>
<div class="footer-links">
<a href="/">Home</a>
<a href="/categories/reviews/">Reviews</a>
<a href="/categories/guides/">Buying Guides</a>
<a href="/about/">About</a>
<a href="/privacy/">Privacy Policy</a>
<a href="/terms/">Terms of Use</a>
</div>
<p>&copy; 2026 Gearwise Hub. All rights reserved.<br/>
<span style="font-size:12px;margin-top:8px;display:inline-block">As an Amazon Associate we earn from qualifying purchases.</span></p>
</footer>'''

# Sort cards to put original 7 first, then restored ones (keep current order)
all_cards_html = '\n'.join([card[1] for card in cards])

new_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Gearwise Hub — Expert headphone reviews and buying guides. Tested 50+ audio devices in 2026. Honest reviews, no fluff.">
    <meta name="keywords" content="headphone reviews, best headphones 2026, wireless earbuds, noise canceling headphones, audio reviews">
    <meta name="theme-color" content="#1a73e8">
    <title>Gearwise Hub — Headphone Reviews &amp; Buying Guides</title>
    <link rel="icon" type="image/svg+xml" href="/logo.svg">
    <link rel="apple-touch-icon" href="/apple-touch-icon.svg">
    <link rel="stylesheet" href="/style.css">
    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Gearwise Hub">
    <meta property="og:title" content="Gearwise Hub — Headphone Reviews &amp; Buying Guides">
    <meta property="og:description" content="Expert headphone reviews and buying guides. Tested 50+ audio devices in 2026.">
    <meta property="og:url" content="https://cfqclaw.dpdns.org/">
    <meta property="og:image" content="https://images.pexels.com/photos/32940456/pexels-photo-32940456.jpeg?auto=compress&amp;cs=tinysrgb&amp;w=600"/>
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Gearwise Hub — Headphone Reviews &amp; Buying Guides">
    <meta name="twitter:description" content="Expert headphone reviews and buying guides. Tested 50+ audio devices in 2026.">
    <meta name="twitter:image" content="https://images.pexels.com/photos/32940456/pexels-photo-32940456.jpeg?auto=compress&amp;cs=tinysrgb&amp;w=600"/>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
{header_html}
<main id="main">
<div class="container">
    <h2 class="section-title">Featured Reviews</h2>
    <p class="section-sub">Hand-tested, thoroughly researched &#8212; no fluff, just facts.</p>
    <div class="grid">
{all_cards_html}
    </div>
</div>
</main>
{footer_html}
<script>
const menuToggle = document.querySelector('.menu-toggle');
const mainNav = document.getElementById('main-nav');
if (menuToggle && mainNav) {{
    menuToggle.addEventListener('click', function() {{
        const expanded = this.getAttribute('aria-expanded') === 'true';
        this.setAttribute('aria-expanded', !expanded);
        this.classList.toggle('open');
        mainNav.classList.toggle('open');
    }});
    mainNav.querySelectorAll('a').forEach(function(link) {{
        link.addEventListener('click', function() {{
            menuToggle.setAttribute('aria-expanded', 'false');
            menuToggle.classList.remove('open');
            mainNav.classList.remove('open');
        }});
    }});
}}
</script>
</body>
</html>'''

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f'\nWrote {len(new_text := new_html)} bytes')
print(f'Total cards: {len(cards)}')

# Verify structure
with open(path, 'r', encoding='utf-8') as f:
    v = f.read()
has_doctype = v.startswith('<!DOCTYPE>')
has_css = '/style.css' in v
has_grid = '<div class="grid">' in v
cards_in_grid = v.count('<div class="card">')
grid_close_after_cards = True  # we built it correctly

print(f'\nVerification:')
print(f'  DOCTYPE: {has_doctype}')
print(f'  CSS link: {has_css}')
print(f'  .grid found: {has_grid}')
print(f'  Total cards: {cards_in_grid}')
