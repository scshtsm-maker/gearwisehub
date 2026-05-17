import os, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = r'C:\Users\Administrator\gearwisehub'
path = os.path.join(BASE, 'static', 'index.html')

with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Extract all cards using a robust pattern
card_pattern = re.compile(
    r'<div class="card">\s*'
    r'<img\s+src="([^"]+)"[^>]*\s*alt="([^"]*)"[^>]*/?>\s*'
    r'<div class="card-body">\s*'
    r'<div class="card-cat">([^<]*)</div>\s*'
    r'<h2 class="card-title"><a href="([^"]+)">([^<]*)</a></h2>\s*'
    r'<p class="card-excerpt"></p>\s*'
    r'<div class="card-meta"><span><time datetime="([^"]+)">[^<]*</time></span><span>([^<]*)</span></div>\s*'
    r'</div>\s*</div>',
    re.DOTALL
)

matches = list(card_pattern.finditer(c))
print(f'Found {len(matches)} cards')

cards_html = []
for m in matches:
    img_src = m.group(1)
    alt = m.group(2)
    cat = m.group(3)
    href = m.group(4)
    title = m.group(5)
    date = m.group(6)
    read_time = m.group(7)
    
    card = (
        '            <div class="card">\n'
        '                <img src="' + img_src + '" alt="' + alt + '" width="600" height="300" loading="lazy">\n'
        '                <div class="card-body">\n'
        '                    <div class="card-cat">' + cat + '</div>\n'
        '                    <h2 class="card-title"><a href="' + href + '">' + title + '</a></h2>\n'
        '                    <p class="card-excerpt"></p>\n'
        '                    <div class="card-meta"><span><time datetime="' + date + '">' + date + '</time></span><span>' + read_time + '</span></div>\n'
        '                </div>\n'
        '            </div>'
    )
    cards_html.append(card)
    print(f'  + {title[:60]}')

# Build page with string concatenation (no f-string issues)
header_part = '''<header>
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

footer_part = '''<footer>
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

js_part = '''<script>
const menuToggle = document.querySelector('.menu-toggle');
const mainNav = document.getElementById('main-nav');
if (menuToggle && mainNav) {
    menuToggle.addEventListener('click', function() {
        const expanded = this.getAttribute('aria-expanded') === 'true';
        this.setAttribute('aria-expanded', !expanded);
        this.classList.toggle('open');
        mainNav.classList.toggle('open');
    });
    mainNav.querySelectorAll('a').forEach(function(link) {
        link.addEventListener('click', function() {
            menuToggle.setAttribute('aria-expanded', 'false');
            menuToggle.classList.remove('open');
            mainNav.classList.remove('open');
        });
    });
}
</script>'''

cards_joined = '\n'.join(cards_html)

new_html = (
    '<!DOCTYPE html>\n'
    '<html lang="en">\n'
    '<head>\n'
    '    <meta charset="UTF-8">\n'
    '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    '    <meta name="description" content="Gearwise Hub &mdash; Expert headphone reviews and buying guides. Tested 50+ audio devices in 2026. Honest reviews, no fluff.">\n'
    '    <meta name="keywords" content="headphone reviews, best headphones 2026, wireless earbuds, noise canceling headphones, audio reviews">\n'
    '    <meta name="theme-color" content="#1a73e8">\n'
    '    <title>Gearwise Hub &mdash; Headphone Reviews &amp; Buying Guides</title>\n'
    '    <link rel="icon" type="image/svg+xml" href="/logo.svg">\n'
    '    <link rel="apple-touch-icon" href="/apple-touch-icon.svg">\n'
    '    <link rel="stylesheet" href="/style.css">\n'
    '    <meta property="og:type" content="website">\n'
    '    <meta property="og:site_name" content="Gearwise Hub">\n'
    '    <meta property="og:title" content="Gearwise Hub &mdash; Headphone Reviews &amp; Buying Guides">\n'
    '    <meta property="og:description" content="Expert headphone reviews and buying guides. Tested 50+ audio devices in 2026.">\n'
    '    <meta property="og:url" content="https://cfqclaw.dpdns.org/">\n'
    '    <meta property="og:image" content="https://images.pexels.com/photos/32940456/pexels-photo-32940456.jpeg?auto=compress&amp;cs=tinysrgb&amp;w=600"/>\n'
    '    <meta name="twitter:card" content="summary_large_image">\n'
    '    <meta name="twitter:title" content="Gearwise Hub &mdash; Headphone Reviews &amp; Buying Guides">\n'
    '    <meta name="twitter:description" content="Expert headphone reviews and buying guides. Tested 50+ audio devices in 2026.">\n'
    '    <meta name="twitter:image" content="https://images.pexels.com/photos/32940456/pexels-photo-32940456.jpeg?auto=compress&amp;cs=tinysrgb&amp;w=600"/>\n'
    '</head>\n'
    '<body>\n'
    '<a class="skip-link" href="#main">Skip to content</a>\n'
    + header_part + '\n'
    '<main id="main">\n'
    '<div class="container">\n'
    '    <h2 class="section-title">Featured Reviews</h2>\n'
    '    <p class="section-sub">Hand-tested, thoroughly researched &mdash; no fluff, just facts.</p>\n'
    '    <div class="grid">\n'
    + cards_joined + '\n'
    '    </div>\n'
    '</div>\n'
    '</main>\n'
    + footer_part + '\n'
    + js_part + '\n'
    '</body>\n'
    '</html>'
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_html)

# Verify
with open(path, 'r', encoding='utf-8') as f:
    v = f.read()

print('\n=== Verification ===')
print('DOCTYPE:', v.startswith('<!DOCTYPE>'))
print('CSS:', '/style.css' in v)
print('Cards total:', v.count('<div class="card">'))
print('File size:', len(v), 'bytes')
gs = v.find('<div class="grid">')
ge = v.rfind('</div>\n    </div>\n</main>')
if gs > 0:
    grid_section = v[gs:ge] if ge > gs else v[gs:]
    ci = grid_section.count('<div class="card">')
    print(f'Cards inside .grid: {ci}')
