import json, sys, re, os

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open(r'C:\Users\Administrator\gearwisehub\link_audit_results.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('=' * 80)
print('FAILED DIRECT LINKS (404 / Error)')
print('=' * 80)

fails = [r for r in data['direct_results'] if r['status'] != 200]
for r in fails:
    print(f"\n  ASIN: {r['asin']} | Status: {r['status']} | Article: {r['article']}")
    print(f"  URL: {r['url']}")
    if r.get('error'):
        print(f"  Error: {r['error']}")

print('\n' + '=' * 80)
print('SEARCH LINKS STATUS')
print('=' * 80)

for r in data.get('search_sample', []):
    icon = 'OK' if r['status'] == 200 else 'FAIL'
    print(f"  {icon} [{r['status']}] {r['article']} -> {r['url'][:80]}")
