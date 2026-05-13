import urllib.request
import re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

def try_asin(asin, expected_keywords):
    url = f"https://www.amazon.com/dp/{asin}?tag=cfqclaw-20"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        resp = urllib.request.urlopen(req, timeout=10)
        html = resp.read().decode("utf-8", errors="ignore")
        title = re.search(r'<span id="productTitle"[^>]*>([^<]+)</span>', html)
        if title:
            t = title.group(1).strip()
            # Check if matches expected keywords
            matches = any(kw.lower() in t.lower() for kw in expected_keywords)
            return (t, matches)
        return ("(no title)", False)
    except Exception as e:
        return (f"ERROR: {e}", False)

# More targeted ASINs for 2026 models based on common patterns
# Sony XM6 patterns: usually B0 prefix for 2025+ products
candidates = {
    "Sony WH-1000XM6": [
        ("B0DXY7N5LZ", ["WH-1000XM6", "WH1000XM6"]),
        ("B0DXY9KQ3M", ["WH-1000XM6", "WH1000XM6"]),
        ("B0DXZ1M4PQ", ["WH-1000XM6", "WH1000XM6"]),
        ("B0DXZ3N7RS", ["WH-1000XM6", "WH1000XM6"]),
    ],
    "Sony WF-1000XM6": [
        ("B0DXY2P1AB", ["WF-1000XM6", "WF1000XM6"]),
        ("B0DXY4Q2CD", ["WF-1000XM6", "WF1000XM6"]),
        ("B0DXY6R3EF", ["WF-1000XM6", "WF1000XM6"]),
        ("B0DXY8S4GH", ["WF-1000XM6", "WF1000XM6"]),
    ],
    "AirPods Pro 3": [
        ("B0DGYDMXWZ", ["AirPods Pro", "AirPods Pro 3", "3rd Generation"]),
        ("B0DGYFNYWX", ["AirPods Pro", "AirPods Pro 3"]),
        ("B0DGZHPQRS", ["AirPods Pro", "AirPods Pro 3"]),
    ],
    "AirPods Max 2": [
        ("B0DGYCMNTV", ["AirPods Max", "AirPods Max 2", "AirPods Max 2nd"]),
        ("B0DGZDLOPW", ["AirPods Max", "AirPods Max 2"]),
    ],
    "Bose QC Ultra Headphones": [
        ("B0DGYEKNPX", ["QuietComfort", "QC Ultra", "Ultra Headphones"]),
        ("B0DGZFMPQY", ["QuietComfort", "QC Ultra", "Ultra Headphones"]),
    ],
}

print("=== 精确 ASIN 验证 ===\n")
for product, asins in candidates.items():
    print(f"[{product}]")
    found = False
    for asin, keywords in asins:
        title, match = try_asin(asin, keywords)
        status = "MATCH!" if match else "---"
        print(f"  {status} {asin}: {title}")
        if match:
            found = True
    if not found:
        print("  (none matched)")
    print()
