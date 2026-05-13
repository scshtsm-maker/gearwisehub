import re, os

# Read all review articles and extract product names + ASINs
base = r'C:\Users\Administrator\gearwisehub\static\reviews'
products = {}  # asin -> list of articles mentioning it

for subdir in os.listdir(base):
    path = os.path.join(base, subdir, 'index.html')
    if not os.path.exists(path):
        continue
    with open(path, encoding='utf-8') as f:
        content = f.read()
    
    # Extract ASINs
    asins = re.findall(r'https://www\.amazon\.com/[^/]+/dp/([A-Z0-9]+)', content)
    for asin in set(asins):
        if asin not in products:
            products[asin] = []
        products[asin].append(subdir)

print("=== 现有文章中的 ASIN 映射 ===\n")
for asin, articles in sorted(products.items()):
    print(f"ASIN {asin}:")
    for a in articles:
        print(f"  - {a}")

print("\n=== 新文章产品对照 ===")
# Products mentioned in new articles vs known ASINs
new_article_product_asins = {
    # From best-flagship-noise-canceling-earbuds-2026
    'AirPods Pro 3': None,  # No confirmed ASIN
    'Sony WF-1000XM6': None,  # No confirmed ASIN
    'Bose QC Ultra 2 Earbuds': 'B0CBJQFD8H',  # Bose QC Ultra Earbuds ASIN - this is correct
    
    # From best-over-ear-noise-canceling-headphones-2026
    'AirPods Max 2': None,
    'Sony WH-1000XM6': None,
    'Bose QC Ultra Headphones': None,
    
    # From apple-airpods-full-comparison-2026
    'AirPods 4': None,
}

print("\n产品 ASIN 状态:")
for product, asin in new_article_product_asins.items():
    if asin:
        print(f"  {product} -> ASIN {asin} ✅")
    else:
        print(f"  {product} -> 无确认 ASIN ⚠️")
