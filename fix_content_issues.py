import os, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = r'C:\Users\Administrator\gearwisehub'
REVIEWS = os.path.join(BASE, 'static', 'reviews')

fix_log = []

def fix_file(slug, desc):
    """Apply fixes to a single article file."""
    path = os.path.join(REVIEWS, slug, 'index.html')
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    
    original = c
    fixes = []
    
    # ============================================================
    # FIX 1: Nav menu leaking into first <p> tag
    # The nav HTML (header/nav) is being captured inside a <p> tag
    # because these articles are missing proper <main> wrapper structure
    # or the header is inside a <p> somehow
    # ============================================================
    
    # Pattern: <p> ... (nav content with "GearwiseHub", "Home", etc.) ... </p>
    # This captures the entire header+nav that leaked into a <p>
    nav_leak_pattern = r'<p[^>]*>\s*(?:<[^>]*>\s*){0,5}(?:GearwiseHub|<svg)[^<]*(?:Home|Reviews|Buying Gui|About)[^<]*</p>'
    
    if re.search(nav_leak_pattern, c, re.DOTALL):
        m = re.search(nav_leak_pattern, c, re.DOTALL)
        leak = m.group(0)
        # Remove the leaking <p>...</p> entirely
        c = c.replace(leak, '\n', 1)
        fixes.append(f'Removed nav menu leak from <p> ({len(leak)} chars)')
    
    # ============================================================
    # FIX 2: Duplicate paragraphs - remove later duplicates
    # ============================================================
    
    paras = list(re.finditer(r'<p[^>]*>(.*?)</p>', c, re.DOTALL))
    seen_texts = {}
    paras_to_remove = set()
    
    for pm in paras:
        p_text = re.sub(r'<[^>]+>', '', pm.group(1)).strip()
        if len(p_text) < 60:
            continue
        short_key = p_text[:150]
        if short_key in seen_texts:
            paras_to_remove.add(pm.start())
            fixes.append(f'Removed duplicate para at pos {pm.start()}')
        else:
            seen_texts[short_key] = pm.start()
    
    # Remove duplicates (in reverse order to preserve positions)
    for pos in sorted(paras_to_remove, reverse=True):
        # Find the full <p>...</p> at this position
        m = re.search(r'<p[^>]*>.*?</p>', c[pos:pos+5000], re.DOTALL)
        if m:
            c = c[:pos] + c[pos + m.end():]
    
    # ============================================================
    # FIX 3: Missing spaces around year numbers and punctuation
    # ============================================================
    
    spacing_fixes = 0
    
    # "2026Year" -> "2026 Year"
    new_c, count1 = re.subn(r'(\d{4})Year', r'\1 Year', c)
    if count1:
        spacing_fixes += count1
    
    # "2026Three" / "2026The" / "2026Apple" -> add space
    new_c, count2 = re.subn(r'(\d{4})([A-Z][a-z])', r'\1 \2', new_c)
    if count2:
        spacing_fixes += count2
    
    # "XM5is" / "XM6vs" -> add space before lowercase following word/uppercase
    new_c, count3 = re.subn(r'([A-Za-z0-9]{2,})(is |are |has |vs )', r'\1 \2', new_c)
    if count3:
        spacing_fixes += count3
    
    # "AmazonAffiliate" -> add space
    new_c, count4 = re.subn(r'([a-z])([A-Z][a-z])', r'\1 \2', new_c)
    if count4 > 3:  # only flag if many (could be legitimate camelCase in rare cases)
        spacing_fixes += count4
    
    c = new_c
    if spacing_fixes:
        fixes.append(f'Fixed {spacing_fixes} spacing issues')
    
    # ============================================================
    # FIX 4: Product unavailable text - check and note
    # ============================================================
    
    unavail_count = len(re.findall(r'unavailable|not available|discontinued', c, re.I))
    if unavail_count > 0:
        fixes.append(f'NOTE: {unavail_count} product availability warnings remain')
    
    # Write back if changed
    if c != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        fix_log.append((slug, fixes))
        print(f'[FIXED] {slug}')
        for f_item in fixes:
            print(f'       + {f_item}')
    else:
        print(f'[NOOP]  {slug}')

# Run on all articles with issues
problem_slugs = [
    'apple-airpods-pro-2-review',
    'best-bone-conduction-headphones-2026',
    'best-flagship-noise-canceling-earbuds-2026',
    'best-noise-canceling-headphones-under-200',
    'best-over-ear-noise-canceling-headphones-2026',
    'best-running-headphones-2026',
    'best-wireless-earbuds-under-100',
    'best-wireless-earbuds-under-200',
    'sony-wh-1000xm5',
]

print('Applying content fixes...\n')
for slug in problem_slugs:
    fix_file(slug, slug)

print(f'\n{"="*50}')
print(f'Fixed: {len(fix_log)}/{len(problem_slugs)} articles')
