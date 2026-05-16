import urllib.request, urllib.parse, re, time

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

PRODUCTS = [
    'Bose Ultra Open Earbuds',
    'Samsung Galaxy Buds2 Pro wireless earbuds',
    'Sony LinkBuds S wireless earbuds',
    'Jabra Elite 4 wireless earbuds',
    'Soundcore Space Q45 wireless headphones',
    'Soundcore Spirit C30 NC open ear earbuds',
    'Beats Fit Pro wireless earbuds',
    'Jabra Elite 8 Active wireless earbuds',
    'JBL Tune 760NC wireless headphones',
    'H2O Audio TRI Pro waterproof headphones',
    'Shokz OpenSwim waterproof bone conduction',
    'Philips A6606 bone conduction headphones',
]

for i, p in enumerate(PRODUCTS):
    try:
        q = urllib.parse.quote_plus(p)
        url = 'https://www.amazon.com/s?k=' + q + '&tag=cfqclaw-20'
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        resp = urllib.request.urlopen(req, timeout=10)
        html = resp.read().decode('utf-8', errors='ignore')
        m = re.search(r'data-asin="([A-Z0-9]{10})"', html)
        if m:
            print(m.group(1) + ' | ' + p[:55])
        else:
            print('NO_ASIN | ' + p)
    except Exception as e:
        print('ERROR  | ' + p + ' | ' + str(e)[:40])
    time.sleep(0.5)
