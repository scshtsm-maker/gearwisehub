#!/usr/bin/env python3
"""Restore deleted articles from git and fix broken ASINs."""
import subprocess
import os

BASE = r'C:\Users\Administrator\gearwisehub'
REV = 'a298284^'  # commit before deletion

# Articles to restore (slug -> ASIN fixes as old->new)
ARTICLES = {
    'best-bone-conduction-headphones-2026': {
        'B09WHV7R6J': 'B09BVXT8TJ',  # Shokz OpenRun Pro
        'B08R5WRY6J': None,           # Shokz OpenSwim - no replacement
        'B09P4QQT6M': 'B07JL1K193',  # Philips A6606
    },
    'best-budget-headphones-2026': {
        'B0D94WXY8Q': 'B0FNWCYLZN',  # Soundcore Life Q20i
        'B09XS411J7': 'B0BS1PRC4L',  # Sony WH-CH520
        'B0BJ682ZKT': 'B0FWJY183S',  # Soundcore Space Q45
    },
    'best-noise-canceling-headphones-under-200': {
        'B0D6H3XK2M': None,            # Edifier W820NB Plus - no replacement
        'B0BWGFYVJX': 'B0F1CL7LTD',  # 1MORE SonoFlow
        'B0CJ9K1J5V': 'B0GXW4KNPB',  # Soundcore Space One
        # B0FNWJ4FV3 is OK
    },
    'best-gaming-headsets-2026': {
        'B09V2W7Z8C': 'B0D1S7D9YX',  # SteelSeries Arctis Nova Pro
        'B0C1FKG8HM': 'B0DQQT2ZS3',  # HyperX Cloud III Wireless
        'B0C1GJP5YK': 'B0DQQT2ZS3',  # HyperX Cloud III Wired
        'B0D5TP8LR2': None,            # Razer BlackShark V2 Pro 2026 - discontinued
        'B08XV7V9Z6': 'B0FHW4CF51',  # Xbox Wireless Headset
        'B0C7JGJQHY': 'B07W6H7PY2',  # Logitech G PRO X 2 Lightspeed
        'B09G9FP2LJ': 'B08SHZW9MF',  # EPOS H6PRO
        'B0CJQH3Z8V': 'B083JRW96J',  # Corsair Virtuoso Pro
    },
    'best-running-headphones-2026': {
        'B09KM6T2JQ': 'B09BVXT8TJ',  # Shokz OpenRun
        'B0D8ZJYQ3P': 'B0GLX2GZ7P',  # Soundcore Spirit C30 NC
        'B093BKKBRK': 'B07MSLF5YC',  # Jaybird Vista 2
        'B08B43KB47': None,            # Adidas RPT-01 - discontinued
        'B0C6KB8LCJ': 'B0B7Q4HXK2',  # Sony WF-1000XM5
    },
    'best-sports-headphones-2026': {
        'B0D1J8KX2M': 'B0D1J8KX2M',  # Shokz OpenRun Pro 2 (OK)
        'B0C1S8YQR7': 'B0D6MR7RBD',  # H2O Audio TRI Pro
        'B0D8QJN5VX': 'B0F9HTKWRD',  # Jabra Elite 8 Active Gen 2
        'B09JL54S3K': 'B08Q8P69JZ',  # Beats Fit Pro
        'B0B7Q5XK8L': 'B0B7Q5XK8L',  # Sony LinkBuds S (OK)
        'B0BR4D5YQH': 'B0BR4D5YQH',  # JBL Endurance Race TWS (check)
        'B0D3HFRM2Q': 'B0D3HFRM2Q',  # Bose Ultra Open Earbuds (OK)
        'B08F7PTF53': 'B08F7PTF53',  # Soundcore Spirit X2 (check)
    },
    'best-headphones-for-small-ears': {
        'B08J9D6Z99': 'B0F2QWR3FB',  # Soundcore Life Dot 2
        'B09TM9K9W3': 'B0F9HTKWRD',  # Jabra Elite 7 Active -> Elite 8 Active
        'B0BDHWDR9X': 'B0BDHWDR9X',  # Apple AirPods Pro 2 (OK - in existing article)
        'B09YXNYS86': 'B0B7Q5XK8L',  # Sony LinkBuds S
    },
    'best-wireless-earbuds-under-100': {
        'B0CJL3ZJBM': 'B0FNWJ4FV3',  # Soundcore Liberty 4 NC
    },
    'best-wireless-earbuds-under-200': {
        # From deleted article - need to check ASINs
    },
}

def restore_file(slug, asin_fixes):
    path = os.path.join(BASE, 'static', 'reviews', slug, 'index.html')
    
    # Get file content from git
    git_path = f'static/reviews/{slug}/index.html'
    cmd = ['git', 'show', f'{REV}:{git_path}']
    result = subprocess.run(cmd, capture_output=True, cwd=BASE)
    
    if result.returncode != 0:
        print(f'FAIL: {slug} - git show failed')
        return False
    
    # Decode with UTF-8, replace errors for robustness
    try:
        content = result.stdout.decode('utf-8', errors='replace')
    except Exception as e:
        print(f'FAIL: {slug} - decode error: {e}')
        return False
    
    # Fix ASINs
    fixes_made = []
    for old_asin, new_asin in asin_fixes.items():
        if old_asin in content:
            if new_asin:
                content = content.replace(old_asin, new_asin)
                fixes_made.append(f'{old_asin} -> {new_asin}')
            else:
                # Mark for replacement with search link (keep URL but remove ASIN)
                fixes_made.append(f'{old_asin} -> (removed - no replacement)')
    
    # Also fix the Sony WH-CH520 old ASIN which was missing
    # B09XS411J7 -> B0BS1PRC4L done above
    
    # Fix Bose QC Ultra (old article had wrong ASIN B0CCZRRQ3K, should be B0CN9FTKJ4)
    if 'B0CCZRRQ3K' in content:
        content = content.replace('B0CCZRRQ3K', 'B0CN9FTKJ4')
        fixes_made.append('B0CCZRRQ3K -> B0CN9FTKJ4 (Bose QC Ultra)')
    
    # Write file
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'OK: {slug}')
    if fixes_made:
        for fix in fixes_made:
            print(f'  ASIN fix: {fix}')
    return True

for slug, asin_fixes in ARTICLES.items():
    restore_file(slug, asin_fixes)

print('\nDone restoring articles.')
