#!/usr/bin/env python3
"""Verify Amazon ASINs - writes results to file as it goes."""
import urllib.request
import urllib.parse
import re
import time

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
OUTFILE = 'C:\\Users\\Administrator\\gearwisehub\\asin_results.txt'

ASINS = [
    ('Shokz OpenRun Pro', 'B09WHV7R6J'),
    ('Shokz OpenSwim', 'B08R5WRY6J'),
    ('Philips A6606', 'B09P4QQT6M'),
    ('H2O Audio TRI Pro', 'B0C1S8YQR7'),
    ('Soundcore Life Q20i', 'B0D94WXY8Q'),
    ('Sony WH-CH520', 'B09XS411J7'),
    ('Soundcore Space Q45', 'B0BJ682ZKT'),
    ('SteelSeries Arctis Nova Pro', 'B09V2W7Z8C'),
    ('HyperX Cloud III Wireless', 'B0C1FKG8HM'),
    ('HyperX Cloud III Wired', 'B0C1GJP5YK'),
    ('Razer BlackShark V2 Pro 2026', 'B0D5TP8LR2'),
    ('Xbox Wireless Headset', 'B08XV7V9Z6'),
    ('Logitech G PRO X 2 Lightspeed', 'B0C7JGJQHY'),
    ('EPOS H6PRO', 'B09G9FP2LJ'),
    ('Corsair Virtuoso Pro', 'B0CJQH3Z8V'),
    ('Apple AirPods Pro 2', 'B0BDHWDR9X'),
    ('Sony LinkBuds S', 'B09YXNYS86'),
    ('Soundcore Life Dot 2', 'B08J9D6Z99'),
    ('Jabra Elite 7 Active', 'B09TM9K9W3'),
    ('Soundcore Space One', 'B0CJ9K1J5V'),
    ('Edifier W820NB Plus', 'B0D6H3XK2M'),
    ('1MORE SonoFlow', 'B0BWGFYVJX'),
    ('Soundcore Liberty 4 NC (ANC)', 'B0FNWJ4FV3'),
    ('Shokz OpenRun (running)', 'B09KM6T2JQ'),
    ('Sony WF-1000XM5 (running)', 'B0C6KB8LCJ'),
    ('Adidas RPT-01', 'B08B43KB47'),
    ('Jaybird Vista 2', 'B093BKKBRK'),
    ('Soundcore Spirit C30 NC', 'B0D8ZJYQ3P'),
    ('Bose Sleepbuds II', 'B07XGWQ5X1'),
    ('SleepPhones Runtime', 'B07ZQRZ3XK'),
    ('Shokz OpenRun Pro 2 (sports)', 'B0D1J8KX2M'),
    ('Jabra Elite 8 Active Gen 2', 'B0D8QJN5VX'),
    ('Beats Fit Pro (sports)', 'B09JL54S3K'),
    ('Soundcore Spirit X2', 'B08F7PTF53'),
    ('JBL Endurance Race TWS', 'B0BR4D5YQH'),
    ('Sony LinkBuds S (sports)', 'B0B7Q5XK8L'),
    ('Bose Ultra Open Earbuds', 'B0D3HFRM2Q'),
    ('Soundcore Liberty 4 NC (<100)', 'B0CJL3ZJBM'),
    ('Samsung Galaxy Buds2 Pro', 'B0B86CDZS3'),
    ('Sony WH-1000XM5', 'B0B7Q4HXK2'),
    ('Bose QuietComfort Ultra', 'B0CCZRRQ3K'),
    ('Bose QuietComfort Ultra Earbuds', 'B0BXC7J5HM'),
    ('JBL Tune 760NC', 'B0BSHSWRN1'),
    ('Jabra Elite 4', 'B09V4GMXKJ'),
]

def check_asin(name, asin):
    try:
        params = urllib.parse.urlencode({'k': asin, 'tag': 'cfqclaw-20'})
        url = 'https://www.amazon.com/s?' + params
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        resp = urllib.request.urlopen(req, timeout=10)
        html = resp.read().decode('utf-8', errors='ignore')
        if re.search('data-asin="' + asin + '"', html):
            return 'OK'
        if 'No results for' in html or 'did not match any' in html:
            return 'NOT FOUND'
        found = re.findall(r'data-asin="([A-Z0-9]{10})"', html)
        if found:
            return 'DIFF: found ' + ','.join(found[:3])
        return 'UNKNOWN'
    except Exception as e:
        return 'ERROR: ' + type(e).__name__ + ': ' + str(e)[:40]

ok_list = []
fail_list = []
with open(OUTFILE, 'w', encoding='utf-8') as f:
    start_time = time.strftime('%H:%M:%S')
    f.write('Starting ASIN verification at ' + start_time + '\n')
    f.write('Total ASINs: ' + str(len(ASINS)) + '\n\n')
    f.flush()
    
    for i, (name, asin) in enumerate(ASINS):
        result = check_asin(name, asin)
        status = 'OK' if result.startswith('OK') else ('DIFF' if result.startswith('DIFF') else 'FAIL')
        if status == 'OK':
            ok_list.append((name, asin, result))
        else:
            fail_list.append((name, asin, result))
        line = ('[%02d/%02d] %-5s %-12s %-38s %s' % (i+1, len(ASINS), status, asin, name[:38], result[:80]))
        f.write(line + '\n')
        f.flush()
        time.sleep(0.4)
    
    done_time = time.strftime('%H:%M:%S')
    f.write('\nDone at ' + done_time + '\n')
    f.write('SUMMARY: ' + str(len(ok_list)) + ' OK, ' + str(len(fail_list)) + ' FAIL\n\n')
    for name, asin, result in fail_list:
        f.write('  FAIL: ' + asin + ' - ' + name + '\n')
        f.write('    -> ' + result + '\n')

print('Results written to ' + OUTFILE)
print('Done.')
