import os

base = r'C:\Users\Administrator\gearwisehub\static\reviews'

bose_path = os.path.join(base, "bose-quietcomfort-ultra-review", "index.html")
with open(bose_path, encoding="utf-8") as f:
    content = f.read()

# Revert: B0F7M3HPBD -> B0CBJQFD8H in Bose article (original article is about 1st gen)
if "B0F7M3HPBD" in content:
    content = content.replace("B0F7M3HPBD", "B0CBJQFD8H")
    with open(bose_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Reverted Bose article: B0F7M3HPBD -> B0CBJQFD8H (1st gen, may be delisted)")
else:
    print("Bose article already has original ASIN")

# Verify current state
with open(bose_path, encoding="utf-8") as f:
    content = f.read()
if "B0CBJQFD8H" in content:
    print("Bose article: B0CBJQFD8H present (original 1st gen - may be delisted)")
if "B0F7M3HPBD" in content:
    print("Bose article: B0F7M3HPBD present (2nd gen)")
print("Done")
