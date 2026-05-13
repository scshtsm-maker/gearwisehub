import urllib.request
import re
import time

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

def get_title(asin):
    url = f"https://www.amazon.com/dp/{asin}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        resp = urllib.request.urlopen(req, timeout=8)
        html = resp.read().decode("utf-8", errors="ignore")
        m = re.search(r'<title>([^<]+)</title>', html)
        return m.group(1).strip() if m else "(no title)"
    except Exception as e:
        return f"ERR: {e}"

def get_brand(asin):
    url = f"https://www.amazon.com/dp/{asin}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        resp = urllib.request.urlopen(req, timeout=8)
        html = resp.read().decode("utf-8", errors="ignore")
        m = re.search(r'brand.*?>([^<]+)<', html, re.IGNORECASE)
        if m:
            return m.group(1).strip()
        # Try another pattern
        m2 = re.search(r'"brand":"([^"]+)"', html)
        if m2:
            return m2.group(1).strip()
        return "(unknown brand)"
    except:
        return "(error)"

def get_search_asins(url, max_count=5):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    resp = urllib.request.urlopen(req, timeout=12)
    html = resp.read().decode("utf-8", errors="ignore")
    asins = re.findall(r'data-asin="([A-Z0-9]{10})"', html)
    return list(dict.fromkeys(asins))[:max_count]

print("=== AirPods Pro 3 - Check specific ASINs ===\n")
# Try common ASIN patterns for Apple products
apple_candidates = [
    "B0FRB8FXK5",  # "AirPods Pro (3nd Gen) Renewed"
    "B0FRB8GXYZ",  # Variation
]
# Actually search for AirPods Pro with Apple official seller
url = "https://www.amazon.com/s?k=Apple+AirPods+Pro&rh=p_28%3AAirPods+Pro"
asins = get_search_asins("https://www.amazon.com/s?k=Apple+AirPods+Pro+3rd+generation&s=review-rank", 6)
for asin in asins:
    title = get_title(asin)
    brand = get_brand(asin)
    print(f"  {asin} [{brand}]: {title[:70]}")
    time.sleep(0.5)

print("\n=== AirPods Max 2 - Check specific ASINs ===\n")
asins2 = get_search_asins("https://www.amazon.com/s?k=AirPods+Max+2nd+generation&s=review-rank", 6)
for asin in asins2:
    title = get_title(asin)
    brand = get_brand(asin)
    print(f"  {asin} [{brand}]: {title[:70]}")
    time.sleep(0.5)

print("\n=== Sony WH-1000XM6 - Best matches ===\n")
asins3 = get_search_asins("https://www.amazon.com/s?k=Sony+WH-1000XM6&s=review-rank", 5)
for asin in asins3:
    title = get_title(asin)
    brand = get_brand(asin)
    print(f"  {asin} [{brand}]: {title[:70]}")
    time.sleep(0.5)

print("\n=== Bose QC Ultra Earbuds Gen 2 ===\n")
asins4 = get_search_asins("https://www.amazon.com/s?k=Bose+QuietComfort+Ultra+Earbuds+2&s=review-rank", 5)
for asin in asins4:
    title = get_title(asin)
    brand = get_brand(asin)
    print(f"  {asin} [{brand}]: {title[:70]}")
    time.sleep(0.5)
