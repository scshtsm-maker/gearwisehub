import urllib.request, re, urllib.error

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

checks = [
    ("Bose QC Ultra Earbuds (orig)", "https://www.amazon.com/dp/B0CBJQFD8H?tag=cfqclaw-20"),
    ("Bose QC Ultra Earbuds 2nd", "https://www.amazon.com/dp/B0F7M3HPBD?tag=cfqclaw-20"),
    ("Sony WH-1000XM6", "https://www.amazon.com/dp/B0F3QJLD3B?tag=cfqclaw-20"),
]

for label, url in checks:
    print(f"[{label}] {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        resp = urllib.request.urlopen(req, timeout=10)
        html = resp.read().decode("utf-8", errors="ignore")
        title = re.search(r"<title>([^<]+)</title>", html)
        t = title.group(1).strip() if title else "(no title)"
        final_url = resp.url
        print(f"  Status: {resp.status} | Final URL: {final_url}")
        print(f"  Title: {t}")
        print(f"  Length: {len(html)}")
        if "sorry" in html[:500].lower() or "captcha" in html[:500].lower():
            print("  WARNING: Blocked/Sorry page")
        if resp.status == 200 and len(html) < 2000:
            print("  WARNING: Very short page")
    except urllib.error.HTTPError as e:
        print(f"  HTTP Error: {e.code} {e.reason}")
    except Exception as e:
        print(f"  Error: {e}")
    print()
