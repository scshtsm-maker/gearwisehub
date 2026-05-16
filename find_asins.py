#!/usr/bin/env python3
"""Search Amazon by product name and extract first result ASIN."""
import urllib.request
import urllib.parse
import re
import time
import sys

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

PRODUCTS = [
    'Shokz OpenRun Pro bone conduction headphones',
    'Soundcore Life Q20i wireless headphones',
    'Sony WH-CH520 wireless headphones',
    'SteelSeries Arctis Nova Pro Wireless gaming headset',
    'HyperX Cloud III wireless gaming headset',
    'Logitech G Pro X 2 Lightspeed gaming headset',
    'Bose Sleepbuds II sleep earbuds',
    'Jaybird Vista 2 wireless earbuds',
    'Bose QuietComfort Ultra headphones',
    'Sony WF-1000XM5 wireless earbuds',
    'Bose Ultra Open Earbuds open design',
    'Samsung Galaxy Buds2 Pro wireless earbuds',
    'Sony LinkBuds S wireless earbuds',
    'Jabra Elite 4 wireless earbuds',
    'Soundcore Space One wireless headphones',
    'Adidas RPT-01 sport headphones',
    'Edifier W820NB Plus wireless headphones',
    '1MORE SonoFlow wireless headphones',
    'Shokz OpenSwim waterproof bone conduction',
    'H2O Audio TRI Pro waterproof headphones',
    'Soundcore Spirit C30 NC open ear earbuds',
    'Philips A6606 bone conduction headphones',
    'Soundcore Liberty 4 NC wireless earbuds',
    'Beats Fit Pro wireless earbuds',
    'Jabra Elite 8 Active wireless earbuds',
    'JBL Tune 760NC wireless headphones',
    'Bose SoundSport Free wireless earbuds',
    'Soundcore Spirit X2 wireless earbuds sports',
    'Shokz OpenFit open ear earbuds',
    'Sony WH-1000XM6 wireless headphones',
]

def search_product(query):
    try:
        q = urllib.parse.quote_plus(query)
        url = f'https://www.amazon.com/s?k={q}&tag=cfqclaw-20'
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        resp = urllib.request.urlopen(req, timeout=10)
        html = resp.read().decode('utf-8', errors='ignore')
        
        # Extract first result ASIN
        pattern = r'data-asin="([A-Z0-9]{10})"'
        matches = re.findall(pattern, html)
        
        if matches:
            first_asin = matches[0]
            # Try to extract product name
            # Look for the product title near the first ASIN
            idx = html.find('data-asin="' + first_asin + '"')
            if idx >= 0:
                snippet = html[idx:idx+500]
                title_m = re.search(r'<span[^>]*class="[^"]*(?:a-size-medium|a-size-base)[^"]*"[^>]*>([^<]+)<', snippet)
                if title_m:
                    title = re.sub('<[^>]+>', '', title_m.group(0)).strip()[:80]
                else:
                    title = '(title not extracted)'
            else:
                title = '(ASIN not found in HTML)'
            return first_asin, title
        
        if 'No results for' in html or 'did not match' in html:
            return 'NO RESULTS', ''
        return 'ERROR', 'could not extract ASIN'
    except Exception as e:
        return 'ERROR', str(e)[:60]

outfile = 'C:\\Users\\Administrator\\gearwisehub\\asin_search_results.txt'
with open(outfile, 'w', encoding='utf-8') as f:
    for i, product in enumerate(PRODUCTS):
        asin, title = search_product(product)
        f.write(f'{i+1:02d}. {product[:50]}\n')
        f.write(f'    ASIN: {asin} | {title}\n')
        f.flush()
        time.sleep(0.5)
        print(f'[{i+1}/{len(PRODUCTS)}] {asin} - {product[:50]}')

print(f'\nDone. Results in {outfile}')
