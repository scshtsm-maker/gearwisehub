import re, os

base = r'C:\Users\Administrator\gearwisehub\static'

# === Fix 1: index.html - upgrade Sports and Gaming card images from w=400 to w=1200 ===
idx_path = os.path.join(base, 'index.html')
with open(idx_path, 'r', encoding='utf-8') as f:
    idx = f.read()

# Fix Sports image: w=400 -> w=1200
idx = idx.replace(
    'photo-1571019613454-1cb2f99b2d8b?w=400&q=80',
    'photo-1571019613454-1cb2f99b2d8b?w=1200&q=80'
)
# Fix Gaming image: w=400 -> w=1200  
idx = idx.replace(
    'photo-1593305841991-05c297ba4575?w=400&q=80',
    'photo-1593305841991-05c297ba4575?w=1200&q=80'
)

with open(idx_path, 'w', encoding='utf-8') as f:
    f.write(idx)
print("Fix 1 DONE: index.html images upgraded to w=1200")

# === Fix 2: Bone conduction article - replace image with one proven to work on homepage ===
bone_path = os.path.join(base, 'reviews', 'best-bone-conduction-headphones-2026', 'index.html')
with open(bone_path, 'r', encoding='utf-8') as f:
    bone = f.read()

# Replace ALL occurrences of the problematic bone conduction image
old_img = 'photo-1606220838315-056192d5e927'
new_img = 'photo-1545127398-14699f92334b'  # This one works on homepage (item [8] above)

count = bone.count(old_img)
bone = bone.replace(old_img, new_img)

with open(bone_path, 'w', encoding='utf-8') as f:
    f.write(bone)
print(f"Fix 2 DONE: bone conduction image replaced ({count} occurrences) -> {new_img}")

# === Fix 3: Also fix the bone conduction image in category pages ===
reviews_cat = os.path.join(base, 'categories', 'reviews', 'index.html')
with open(reviews_cat, 'r', encoding='utf-8') as f:
    rc = f.read()
rc_count = rc.count(old_img)
rc = rc.replace(old_img, new_img)
with open(reviews_cat, 'w', encoding='utf-8') as f:
    f.write(rc)
print(f"Fix 3 DONE: reviews category page bone image replaced ({rc_count} occurrences)")

guides_cat = os.path.join(base, 'categories', 'guides', 'index.html')
with open(guides_cat, 'r', encoding='utf-8') as f:
    gc = f.read()
gc_count = gc.count(old_img)
gc = gc.replace(old_img, new_img)
with open(guides_cat, 'w', encoding='utf-8') as f:
    f.write(gc)
print(f"Fix 4 DONE: guides category page bone image replaced ({gc_count} occurrences)")

print("\nALL FIXES APPLIED!")
