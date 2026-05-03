import codecs
path = r"C:\Users\Administrator\gearwisehub\static\categories\reviews\index.html"
with codecs.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace broken image IDs
broken_img = "photo-1590658268037-6bf12f032f55"
good_img = "photo-1618366712010-f4ae9c647dcb"
content = content.replace(broken_img, good_img)

# 2. Fix footer mojibake
content = content.replace("漏 2026 GearwiseHub", "© 2026 GearwiseHub")

# 3. Add missing article cards
new_cards = """
        <div class="card">
            <img src="https://images.unsplash.com/photo-1583394838336-acd977736f90?w=600&q=75" alt="Soundcore Liberty 4 NC" width="600" height="300" loading="lazy">
            <div class="card-body">
                <div class="card-cat">Earbuds</div>
                <h2 class="card-title"><a href="/reviews/soundcore-liberty-4-nc-review/">Soundcore Liberty 4 NC Review (2026)</a></h2>
                <p class="card-excerpt">Budget ANC earbuds with innovative co-axial drivers. How do they stack up?</p>
                <div class="card-meta"><span><time datetime="2026-05-02">May 2, 2026</time></span><span>10 min read</span></div>
            </div>
        </div>
        <div class="card">
            <img src="https://images.unsplash.com/photo-1545127398-14699f92334b?w=600&q=75" alt="Bose QuietComfort Ultra" width="600" height="300" loading="lazy">
            <div class="card-body">
                <div class="card-cat">Premium Audio</div>
                <h2 class="card-title"><a href="/reviews/bose-quietcomfort-ultra-review/">Bose QuietComfort Ultra Review</a></h2>
                <p class="card-excerpt">Premium comfort meets spatial audio. Is it worth the premium price?</p>
                <div class="card-meta"><span><time datetime="2026-05-02">May 2, 2026</time></span><span>12 min read</span></div>
            </div>
        </div>
        <div class="card">
            <img src="https://images.unsplash.com/photo-1606220838315-056192d5e927?w=600&q=75" alt="Best Sports Headphones" width="600" height="300" loading="lazy">
            <div class="card-body">
                <div class="card-cat">Buying Guide</div>
                <h2 class="card-title"><a href="/reviews/best-sports-headphones-2026/">Best Sports Headphones 2026</a></h2>
                <p class="card-excerpt">Secure-fit headphones for running, gym, and swimming. 8 models tested.</p>
                <div class="card-meta"><span><time datetime="2026-05-03">May 3, 2026</time></span><span>11 min read</span></div>
            </div>
        </div>
        <div class="card">
            <img src="https://images.unsplash.com/photo-1593305841991-05c297ba4575?w=600&q=75" alt="Best Gaming Headsets" width="600" height="300" loading="lazy">
            <div class="card-body">
                <div class="card-cat">Buying Guide</div>
                <h2 class="card-title"><a href="/reviews/best-gaming-headsets-2026/">Best Gaming Headsets 2026</a></h2>
                <p class="card-excerpt">PC, PS5, Xbox, Switch  we tested 8 models across all platforms.</p>
                <div class="card-meta"><span><time datetime="2026-05-03">May 3, 2026</time></span><span>13 min read</span></div>
            </div>
        </div>
"""

# Insert before </div></div></main>
content = content.replace("</div>\n    </div>\n</main>", new_cards + "\n    </div>\n</main>")

with codecs.open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Done: reviews category page fixed")