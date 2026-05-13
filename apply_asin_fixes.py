import re, os, shutil

base = r'C:\Users\Administrator\gearwisehub\static\reviews'

def replace_in_file(filepath, old, new):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    if old not in content:
        return False
    new_content = content.replace(old, new)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True

# =========================================
# Fix 1: Bose QC Ultra Earbuds article - B0CBJQFD8H -> B0F7M3HPBD
# =========================================
bose_path = os.path.join(base, "bose-quietcomfort-ultra-review", "index.html")
old_asin = "B0CBJQFD8H"
new_asin = "B0F7M3HPBD"
if os.path.exists(bose_path):
    ok = replace_in_file(bose_path, f"/dp/{old_asin}", f"/dp/{new_asin}")
    print(f"Bose article B0CBJQFD8H -> B0F7M3HPBD: {'OK' if ok else 'NOT FOUND'}")

# =========================================
# Fix 2: Update comparison articles with confirmed ASINs
# =========================================
fixes = [
    # (article_dir, search_url, dp_url)
    # best-over-ear: Sony WH-1000XM6
    ("best-over-ear-noise-canceling-headphones-2026",
     "https://www.amazon.com/s?k=Sony+WH-1000XM6&tag=cfqclaw-20",
     "https://www.amazon.com/dp/B0F3QJLD3B?tag=cfqclaw-20"),
    # best-flagship: Bose QC Ultra 2 Earbuds
    ("best-flagship-noise-canceling-earbuds-2026",
     "https://www.amazon.com/s?k=Bose+QuietComfort+Ultra+Earbuds+2&tag=cfqclaw-20",
     "https://www.amazon.com/dp/B0F7M3HPBD?tag=cfqclaw-20"),
]

for article_dir, search_url, dp_url in fixes:
    path = os.path.join(base, article_dir, "index.html")
    if os.path.exists(path):
        ok = replace_in_file(path, search_url, dp_url)
        print(f"{article_dir}: {search_url[-30:]} -> {dp_url[-30:]} : {'OK' if ok else 'NOT FOUND'}")

print("\nDone!")
