import urllib.request, urllib.error

urls = [
    ("Sports w=400 (current)", "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&q=80"),
    ("Sports w=1200 (proposed)", "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=1200&q=80"),
    ("Gaming w=400 (current)", "https://images.unsplash.com/photo-1593305841991-05c297ba4575?w=400&q=80"),
    ("Gaming w=1200 (proposed)", "https://images.unsplash.com/photo-1593305841991-05c297ba4575?w=1200&q=80"),
    ("Bone conduction current", "https://images.unsplash.com/photo-1606220838315-056192d5e927?w=1200&q=80"),
    ("Bone conduction alt1", "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=1200&q=80"),
    ("Bone conduction alt2", "https://images.unsplash.com/photo-1545127398-14699f92334b?w=1200&q=80"),
]

for name, url in urls:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=10)
        ct = resp.headers.get("Content-Type", "?")
        size = len(resp.read())
        print(f"  OK  {name}")
        print(f"       {ct} | {size} bytes")
    except Exception as e:
        print(f" FAIL {name}: {e}")
