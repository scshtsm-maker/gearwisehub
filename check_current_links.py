import re, os

base = r'C:\Users\Administrator\gearwisehub\static\reviews'

# ASIN mapping - confirmed from Amazon
CONFIRMED_ASINS = {
    "Sony WH-1000XM6": "B0F3QJLD3B",
    "Bose QC Ultra Earbuds 2": "B0F7M3HPBD",
    # "AirPods Pro 3": "B0FRB8FXK5",  # NOT confident yet - renewed only
    # "AirPods Max 2": "TBD",
    # "Sony WF-1000XM6": "TBD",
}

# Search to replace: old search links that should be upgraded to direct links
# Pattern: https://www.amazon.com/s?k=PRODUCT+NAME&tag=cfqclaw-20

articles = {
    "best-over-ear-noise-canceling-headphones-2026": [
        ("Sony WH-1000XM6", "Sony+WH-1000XM6"),
        ("AirPods Max 2", "AirPods+Max+2"),
        ("Bose QC Ultra Headphones", "Bose+QuietComfort+Ultra+Headphones"),
    ],
    "best-flagship-noise-canceling-earbuds-2026": [
        ("AirPods Pro 3", "AirPods+Pro+3"),
        ("Sony WF-1000XM6", "Sony+WF-1000XM6"),
        ("Bose QC Ultra 2 Earbuds", "Bose+QuietComfort+Ultra+Earbuds+2"),
    ],
    "apple-airpods-full-comparison-2026": [
        ("AirPods 4", "AirPods+4"),
        ("AirPods Pro 3", "AirPods+Pro+3"),
        ("AirPods Max 2", "AirPods+Max+2"),
    ],
}

def make_dp_url(product_name, tag="cfqclaw-20"):
    if product_name in CONFIRMED_ASINS:
        asin = CONFIRMED_ASINS[product_name]
        return f"https://www.amazon.com/dp/{asin}?tag={tag}"
    return None

# Check current state
print("=== Current links in articles ===\n")
for article_dir, products in articles.items():
    path = os.path.join(base, article_dir, "index.html")
    if not os.path.exists(path):
        print(f"[{article_dir}] FILE NOT FOUND")
        continue
    
    with open(path, encoding="utf-8") as f:
        content = f.read()
    
    print(f"[{article_dir}]")
    for product_name, search_term in products:
        search_url = f"https://www.amazon.com/s?k={search_term}&tag=cfqclaw-20"
        dp_url = make_dp_url(product_name)
        
        has_search = search_url in content
        has_dp = dp_url and dp_url in content
        
        if has_dp:
            status = f"ALREADY DP: {dp_url}"
        elif has_search:
            status = f"SEARCH LINK (can upgrade)" + (f" -> {dp_url}" if dp_url else "")
        else:
            status = "NO LINK FOUND"
        
        print(f"  {product_name}: {status}")
    print()
