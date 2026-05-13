import urllib.request
import re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

def get_product_title(asin):
    url = f"https://www.amazon.com/dp/{asin}?tag=cfqclaw-20"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        resp = urllib.request.urlopen(req, timeout=10)
        html = resp.read().decode("utf-8", errors="ignore")
        # Try to find product title
        title = re.search(r'<span id="productTitle"[^>]*>([^<]+)</span>', html)
        if title:
            return title.group(1).strip()
        # Alternative
        title2 = re.search(r'<title>([^<]+)</title>', html)
        if title2:
            return title2.group(1).strip()
        return "(no title found)"
    except Exception as e:
        return f"ERROR: {e}"

# All candidate ASINs grouped by product
candidates = {
    "Sony WH-1000XM6": ["B0863TXGM3", "B09XS7JWHH", "B09XSDMT4F", "B0B2FCT81R", "B0BS1QCFHX"],
    "Sony WF-1000XM6": ["B08MSRBKGH", "B09DT48V16", "B09LD2D1TV", "B09LD44NW6", "B09TN4MP6V"],
    "AirPods Pro 3": ["B09JQL3NWT", "B0BJQWYLYN", "B0CHWRXH8B", "B0CJJHSFFP", "B0D6T9CRLT"],
    "AirPods Max 2": ["B08RBVHYNR", "B08RNK4CDR", "B09XS7JWHH", "B0BMLXSNG8", "B0BVBBJYTV"],
    "AirPods 4": ["B09JQL3NWT", "B09TN4MP6V", "B0BJQWYLYN", "B0C1BTXM9W", "B0C1QDR7HP"],
    "Bose QC Ultra Earbuds 2": ["B08CJCLV4F", "B09DT48V16", "B09LD2D1TV", "B09LD44NW6", "B0B7838HH6"],
}

print("=== ASIN 验证 ===\n")
for product, asins in candidates.items():
    print(f"[{product}]")
    for asin in asins:
        title = get_product_title(asin)
        print(f"  {asin}: {title}")
    print()
