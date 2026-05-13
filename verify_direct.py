import urllib.request
import re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

def check_product(url, keywords):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        resp = urllib.request.urlopen(req, timeout=12)
        html = resp.read().decode("utf-8", errors="ignore")
        if "sorry" in html[:500].lower() or len(html) < 5000:
            return "BLOCKED/EMPTY"
        # Look for product title
        title = re.search(r'<title>([^<]+)</title>', html)
        if title:
            t = title.group(1).strip()
            # Check for keywords
            for kw in keywords:
                if kw.lower() in t.lower():
                    return f"MATCH: {t}"
            return f"OTHER: {t}"
        return "No title"
    except Exception as e:
        return f"ERROR: {e}"

# Direct product page checks
checks = [
    # Sony WH-1000XM6 - check common ASIN patterns (based on Sony naming)
    ("Sony WH-1000XM6", "https://www.amazon.com/s?k=Sony+WH-1000XM6&s=review-rank", ["WH-1000XM6", "XM6"]),
    # Sony WF-1000XM6
    ("Sony WF-1000XM6", "https://www.amazon.com/s?k=Sony+WF-1000XM6", ["WF-1000XM6", "XM6"]),
    # AirPods Pro 3 - Apple naming convention
    ("AirPods Pro 3", "https://www.amazon.com/s?k=Apple+AirPods+Pro+3rd+generation", ["AirPods Pro", "3rd generation"]),
    # AirPods Max 2
    ("AirPods Max 2", "https://www.amazon.com/s?k=Apple+AirPods+Max+2nd+generation", ["AirPods Max", "2nd generation"]),
    # Bose QC Ultra Headphones (original model - 2023)
    ("Bose QC Ultra Headphones (original)", "https://www.amazon.com/s?k=Bose+QuietComfort+Ultra+Headphones", ["QuietComfort", "Ultra"]),
    # Bose QC Ultra Earbuds (original model - 2023) - verify existing ASIN
    ("Bose QC Ultra Earbuds (B0CBJQFD8H)", "https://www.amazon.com/dp/B0CBJQFD8H?tag=cfqclaw-20", ["QuietComfort", "Ultra", "Earbuds"]),
]

print("=== Direct Amazon Verification ===\n")
for name, url, keywords in checks:
    print(f"[{name}]")
    result = check_product(url, keywords)
    print(f"  {result}")
    print()
