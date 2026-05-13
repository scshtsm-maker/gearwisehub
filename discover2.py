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

def get_search_asins(url, max_count=5):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    resp = urllib.request.urlopen(req, timeout=12)
    html = resp.read().decode("utf-8", errors="ignore")
    asins = re.findall(r'data-asin="([A-Z0-9]{10})"', html)
    return list(dict.fromkeys(asins))[:max_count]

checks = [
    ("Sony WH-1000XM6", "https://www.amazon.com/s?k=Sony+WH-1000XM6", "WH-1000XM6"),
    ("Sony WF-1000XM6", "https://www.amazon.com/s?k=Sony+WF-1000XM6", "WF-1000XM6"),
    ("AirPods Pro 3", "https://www.amazon.com/s?k=Apple+AirPods+Pro+3rd+generation", "AirPods Pro"),
    ("AirPods Max 2", "https://www.amazon.com/s?k=Apple+AirPods+Max+2nd+generation", "AirPods Max"),
    ("Bose QC Ultra Earbuds", "https://www.amazon.com/s?k=Bose+QuietComfort+Ultra+Earbuds", "QuietComfort"),
    ("Bose QC Ultra Headphones", "https://www.amazon.com/s?k=Bose+QuietComfort+Ultra+Headphones", "QuietComfort"),
]

confirmed = {}
print("=== ASIN Discovery (lean) ===\n")
for name, url, keyword in checks:
    print(f"[{name}]")
    asins = get_search_asins(url)
    best_asin, best_score = None, 0
    for asin in asins:
        title = get_title(asin)
        # Score
        kw_count = sum(1 for kw in keyword.split() if kw.lower() in title.lower())
        score = kw_count / max(1, len(keyword.split()))
        marker = ""
        if score > best_score:
            best_score = score
            best_asin = asin
        if score > 0.3:
            marker = " <-- MATCH"
        print(f"  {asin} [{score:.1f}]: {title[:70]}{marker}")
        time.sleep(0.3)
    if best_score > 0.3:
        confirmed[name] = best_asin
        print(f"  => CONFIRMED ASIN: {best_asin}")
    else:
        print(f"  => No confident match")
    print()
    time.sleep(1)

print("=== Summary ===")
for name, asin in confirmed.items():
    print(f"  {name}: {asin}")
