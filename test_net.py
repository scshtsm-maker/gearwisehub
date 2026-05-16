import urllib.request, time, sys

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

tests = [
    ('httpbin.org', 'https://httpbin.org/get'),
    ('Amazon search (B09WHV7R6J)', 'https://www.amazon.com/s?k=B09WHV7R6J&tag=cfqclaw-20'),
    ('Amazon direct (B0CJL3ZJBM)', 'https://www.amazon.com/dp/B0CJL3ZJBM?tag=cfqclaw-20'),
]

for name, url in tests:
    print(f'Testing: {name}...', flush=True)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        start = time.time()
        resp = urllib.request.urlopen(req, timeout=8)
        elapsed = time.time() - start
        content = resp.read(500).decode('utf-8', errors='ignore')
        print(f'  OK ({elapsed:.1f}s): {content[:200]}')
    except Exception as e:
        print(f'  FAIL: {type(e).__name__}: {e}')
    time.sleep(0.5)
print('Done.')
