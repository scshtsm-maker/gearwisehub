import urllib.request, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

def search_product(keyword, page=1):
    start = (page - 1) * 24 + 1
    url = f"https://www.amazon.com/s?k={keyword}&s=review-rank&page={page}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    resp = urllib.request.urlopen(req, timeout=12)
    html = resp.read().decode("utf-8", errors="ignore")
    asins = re.findall(r'data-asin="([A-Z0-9]{10})"', html)
    return list(dict.fromkeys(asins))

def get_title_from_search(asin):
    # Get title from search result page (faster than product page)
    url = f"https://www.amazon.com/s?k=PLACEHOLDER&ref=sr_nr_p_24_{asin}"
    # Try to get from search result context
    search_url = f"https://www.amazon.com/s?k={asin}&i=electronics"
    try:
        req = urllib.request.Request(search_url, headers={"User-Agent": UA})
        resp = urllib.request.urlopen(req, timeout=10)
        html = resp.read().decode("utf-8", errors="ignore")
        # Look for product title
        titles = re.findall(r'<span class="a-size-medium a-color-base a-text-normal">([^<]+)</span>', html)
        for t in titles[:3]:
            if asin in html[html.find(t):html.find(t)+200]:
                return t.strip()
        return None
    except:
        return None

print("=== Additional Sony WF-1000XM6 ASINs (page 2) ===")
asins = search_product("Sony+WF-1000XM6+earbuds", 1)
for asin in asins:
    print(f"  {asin}")
    
print("\n=== AirPods Pro (3rd Gen) - more pages ===")
asins2 = search_product("Apple+AirPods+Pro+3rd+generation", 1)
for asin in asins2:
    print(f"  {asin}")

print("\n=== AirPods Max 2nd generation - page 2 ===")
asins3 = search_product("AirPods+Max+2", 2)
for asin in asins3:
    print(f"  {asin}")
    
print("\n=== Sony Store products ===")
asins4 = search_product("Sony+WH-1000XM6+site:amazon.com", 1)
for asin in asins4:
    print(f"  {asin}")
