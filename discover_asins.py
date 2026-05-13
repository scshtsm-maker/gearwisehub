import urllib.request
import re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

def get_asins_from_search(url, expected_product_name, min_confidence=0.6):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    resp = urllib.request.urlopen(req, timeout=15)
    html = resp.read().decode("utf-8", errors="ignore")
    
    # Find all ASINs with their titles
    # Pattern: data-asin="ASIN" followed by product title
    products = re.findall(r'data-asin="([A-Z0-9]{10})"', html)
    products = list(dict.fromkeys(products))  # dedupe preserving order
    
    results = []
    for asin in products[:8]:
        product_url = f"https://www.amazon.com/dp/{asin}?tag=cfqclaw-20"
        try:
            req2 = urllib.request.Request(product_url, headers={"User-Agent": UA})
            resp2 = urllib.request.urlopen(req2, timeout=10)
            product_html = resp2.read().decode("utf-8", errors="ignore")
            title_match = re.search(r'<title>([^<]+)</title>', product_html)
            title = title_match.group(1).strip() if title_match else "(no title)"
            
            # Score the match
            title_lower = title.lower()
            expected_lower = expected_product_name.lower()
            score = 0
            for word in expected_lower.split():
                if len(word) > 2 and word in title_lower:
                    score += 1 / len(expected_lower.split())
            
            results.append((asin, title, score))
        except Exception as e:
            results.append((asin, f"ERROR: {e}", 0))
    
    return sorted(results, key=lambda x: -x[2])

searches = [
    ("Sony WH-1000XM6", "https://www.amazon.com/s?k=Sony+WH-1000XM6&s=review-rank", "Sony WH-1000XM6"),
    ("Sony WF-1000XM6", "https://www.amazon.com/s?k=Sony+WF-1000XM6", "Sony WF-1000XM6"),
    ("AirPods Pro 3", "https://www.amazon.com/s?k=Apple+AirPods+Pro+3rd+generation", "AirPods Pro 3"),
    ("AirPods Max 2", "https://www.amazon.com/s?k=Apple+AirPods+Max+2nd+generation", "AirPods Max 2"),
    ("Bose QC Ultra Headphones", "https://www.amazon.com/s?k=Bose+QuietComfort+Ultra+Headphones", "Bose QuietComfort Ultra Headphones"),
    ("Bose QC Ultra Earbuds", "https://www.amazon.com/s?k=Bose+QuietComfort+Ultra+Earbuds", "Bose QuietComfort Ultra Earbuds"),
]

print("=== ASIN Discovery ===\n")
confirmed = {}

for name, url, expected in searches:
    print(f"[{name}]")
    results = get_asins_from_search(url, expected)
    best = None
    for asin, title, score in results[:5]:
        marker = " <-- BEST" if score == results[0][2] and score > 0.5 else ""
        print(f"  {score:.2f} {asin}: {title[:80]}{marker}")
        if best is None or score > best[1]:
            best = (asin, score)
    if best and best[1] > 0.5:
        confirmed[name] = best[0]
        print(f"  CONFIRMED: {best[0]}")
    else:
        print(f"  NO CONFIRMED ASIN")
    print()

print("=== Final ASIN Map ===")
for name, asin in confirmed.items():
    print(f"  {name}: {asin}")
