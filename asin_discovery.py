import urllib.request, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

def get_asins_from_search(keyword):
    url = f"https://www.amazon.com/s?k={keyword}&tag=cfqclaw-20"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        resp = urllib.request.urlopen(req, timeout=12)
        html = resp.read().decode("utf-8", errors="ignore")
        if len(html) < 3000:
            return [], f"short page ({len(html)} bytes)"
        title = re.search(r"<title>([^<]+)</title>", html)
        title_str = title.group(1).strip() if title else "no title"
        asins = re.findall(r'data-asin="([A-Z0-9]{10})"', html)
        asins = list(dict.fromkeys(asins))
        return asins, title_str
    except Exception as e:
        return [], str(e)

searches = [
    ("AirPods Pro 3", "Apple+AirPods+Pro+3"),
    ("Sony WF-1000XM6", "Sony+WF-1000XM6"),
    ("AirPods Max 2", "Apple+AirPods+Max+2"),
    ("AirPods 4", "Apple+AirPods+4"),
    ("Sony WH-1000XM6", "Sony+WH-1000XM6"),
    ("Bose QC Ultra Earbuds 2", "Bose+QuietComfort+Ultra+Earbuds+2"),
    ("JBL Tune 760NC", "JBL+Tune+760NC"),
]

print("=== ASIN Discovery from Search Results ===\n")
for label, keyword in searches:
    asins, title = get_asins_from_search(keyword)
    if asins:
        print(f"[{label}] title={title}")
        print(f"  ASINs ({len(asins)}): {asins[:8]}")
        print()
    else:
        print(f"[{label}] FAILED: {title}")
        print()
