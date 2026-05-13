import urllib.request, re, urllib.error

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

def check(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        resp = urllib.request.urlopen(req, timeout=10)
        final_url = resp.url
        html = resp.read().decode("utf-8", errors="ignore")
        title = re.search(r"<title>([^<]+)</title>", html)
        t = title.group(1).strip() if title else "(no title)"
        length = len(html)
        # Detect bot page
        is_bot = length < 3000 or "sorry" in html[:300].lower() or "captcha" in html[:300].lower()
        return (resp.status, final_url, t[:70], length, is_bot)
    except urllib.error.HTTPError as e:
        return (e.code, url, f"HTTP {e.code}", 0, False)
    except Exception as e:
        return (0, url, f"ERR: {e}", 0, False)

checks = [
    # Search links - just check status
    ("AirPods Pro 3 search", "https://www.amazon.com/s?k=AirPods+Pro+3&tag=cfqclaw-20"),
    ("Sony WF-1000XM6 search", "https://www.amazon.com/s?k=Sony+WF-1000XM6&tag=cfqclaw-20"),
    ("AirPods Max 2 search", "https://www.amazon.com/s?k=AirPods+Max+2&tag=cfqclaw-20"),
    ("AirPods 4 search", "https://www.amazon.com/s?k=AirPods+4&tag=cfqclaw-20"),
    ("Sony WH-1000XM6 search", "https://www.amazon.com/s?k=Sony+WH-1000XM6&tag=cfqclaw-20"),
    ("Bose QC Ultra Headphones search", "https://www.amazon.com/s?k=Bose+QuietComfort+Ultra+Headphones&tag=cfqclaw-20"),
    ("Bose QC Ultra Earbuds 2 search", "https://www.amazon.com/s?k=Bose+QuietComfort+Ultra+Earbuds+2&tag=cfqclaw-20"),
    ("JBL Tune 760NC search", "https://www.amazon.com/s?k=JBL+Tune+760NC&tag=cfqclaw-20"),
    ("AI translation earbuds search", "https://www.amazon.com/s?k=AI+translation+earbuds&tag=cfqclaw-20"),
    # Direct ASIN links
    ("Bose QC Ultra Earbuds B0CBJQFD8H", "https://www.amazon.com/dp/B0CBJQFD8H?tag=cfqclaw-20"),
    ("Bose QC Ultra Earbuds2 B0F7M3HPBD", "https://www.amazon.com/dp/B0F7M3HPBD?tag=cfqclaw-20"),
    ("Sony WH-1000XM6 B0F3QJLD3B", "https://www.amazon.com/dp/B0F3QJLD3B?tag=cfqclaw-20"),
    ("Sony WF-1000XM5 B0B3L6QSZZ", "https://www.amazon.com/dp/B0B3L6QSZZ?tag=cfqclaw-20"),
    ("Sony WH-1000XM5 B09JQS3J6ZW", "https://www.amazon.com/dp/B09JQS3J6ZW?tag=cfqclaw-20"),
    ("AirPods Pro 2 B0CHWR3H34", "https://www.amazon.com/dp/B0CHWR3H34?tag=cfqclaw-20"),
]

print("=== Link Validation ===\n")
for label, url in checks:
    status, final_url, title, length, is_bot = check(url)
    if status == 200 and not is_bot and length > 3000:
        print(f"OK   {label}: {title}")
    elif status == 404:
        print(f"404  {label}: PRODUCT DELISTED")
    elif status >= 400:
        print(f"ERR  {label}: HTTP {status}")
    else:
        print(f"WARN {label}: status={status} len={length} | {title}")
    import time; time.sleep(0.4)
