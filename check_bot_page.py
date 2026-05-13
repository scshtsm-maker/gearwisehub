import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
url = "https://www.amazon.com/dp/B0F3QJLD3B?tag=cfqclaw-20"
req = urllib.request.Request(url, headers={"User-Agent": UA})
resp = urllib.request.urlopen(req, timeout=10)
html = resp.read().decode("utf-8", errors="ignore")
print(f"Length: {len(html)}")
print(f"Status: {resp.status}")
print()
# Show first and last 500 chars
print("=== First 500 chars ===")
print(html[:500])
print()
print("=== Last 500 chars ===")
print(html[-500:])
