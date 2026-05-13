import urllib.request
import re
import sys

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

products = [
    ("Sony WH-1000XM6", "https://www.amazon.com/s?k=Sony+WH-1000XM6&tag=cfqclaw-20"),
    ("Sony WF-1000XM6", "https://www.amazon.com/s?k=Sony+WF-1000XM6&tag=cfqclaw-20"),
    ("AirPods Pro 3", "https://www.amazon.com/s?k=AirPods+Pro+3&tag=cfqclaw-20"),
    ("AirPods Max 2", "https://www.amazon.com/s?k=AirPods+Max+2&tag=cfqclaw-20"),
    ("AirPods 4", "https://www.amazon.com/s?k=AirPods+4&tag=cfqclaw-20"),
    ("Bose QC Ultra Headphones", "https://www.amazon.com/s?k=Bose+QuietComfort+Ultra+Headphones&tag=cfqclaw-20"),
    ("Bose QC Ultra Earbuds 2", "https://www.amazon.com/s?k=Bose+QuietComfort+Ultra+Earbuds+2&tag=cfqclaw-20"),
]

for name, url in products:
    print(f"\n=== {name} ===")
    print(f"URL: {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        resp = urllib.request.urlopen(req, timeout=15)
        html = resp.read().decode("utf-8", errors="ignore")
        status_code = resp.status
        print(f"HTTP Status: {status_code}")
        # Find ASINs in search results
        asins = re.findall(r'data-asin="([A-Z0-9]{10})"', html)
        dp_asins = re.findall(r'href="https://www\.amazon\.com/[^/]+/dp/([A-Z0-9]{10})', html)
        if asins:
            print(f"ASINs found: {sorted(set(asins))[:5]}")
        elif dp_asins:
            print(f"DP ASINs found: {sorted(set(dp_asins))[:5]}")
        else:
            # Try to find title matches
            titles = re.findall(r'<span class="a-size-medium a-color-base a-text-normal">([^<]+)</span>', html)
            if titles:
                print(f"Titles found: {titles[:3]}")
            else:
                # Check if blocked
                if "bot" in html.lower() or "captcha" in html.lower() or "api-services" in html.lower():
                    print("BLOCKED: Bot/Captcha detected")
                elif "sorry" in html.lower() and "amazon" in html.lower():
                    print("BLOCKED: Access restricted")
                else:
                    print(f"Content length: {len(html)} chars")
                    print(f"Sample: {html[5000:5200]}")
    except Exception as e:
        print(f"ERROR: {e}")
