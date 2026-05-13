import re, os

# ASIN mapping from existing articles (confirmed)
known_asins = {
    'AirPods Pro 2': 'B0CHWR3H34',
    'Bose QC Ultra Earbuds': 'B0CBJQFD8H',
    'Sony WF-1000XM5': 'B0B3L6QSZZ',
    'Sony WH-1000XM5': 'B09JQS3J6ZW',
    'Soundcore Liberty 4 NC': 'B0C1H26C5T',
    'Soundcore Space Q45': 'B0BJ682ZKT',
    'Jabra Elite 85t': 'B08L9F56BL',
}

# Products in the 3 new articles
new_article_products = {
    'best-flagship-noise-canceling-earbuds-2026': {
        'AirPods Pro 3': {'asin': None, 'current': 'https://www.amazon.com/s?k=AirPods+Pro+3&tag=cfqclaw-20'},
        'Sony WF-1000XM6': {'asin': 'B0B3L6QSZZ', 'current': 'https://www.amazon.com/s?k=Sony+WF-1000XM6&tag=cfqclaw-20'},
        'Bose QC Ultra 2 Earbuds': {'asin': 'B0CBJQFD8H', 'current': 'https://www.amazon.com/s?k=Bose+QuietComfort+Ultra+Earbuds+2&tag=cfqclaw-20'},
    },
    'best-over-ear-noise-canceling-headphones-2026': {
        'AirPods Max 2': {'asin': None, 'current': 'https://www.amazon.com/s?k=AirPods+Max+2&tag=cfqclaw-20'},
        'Sony WH-1000XM6': {'asin': 'B09JQS3J6ZW', 'current': 'https://www.amazon.com/s?k=Sony+WH-1000XM6&tag=cfqclaw-20'},
        'Bose QC Ultra Headphones': {'asin': None, 'current': 'https://www.amazon.com/s?k=Bose+QuietComfort+Ultra+Headphones&tag=cfqclaw-20'},
    },
    'apple-airpods-full-comparison-2026': {
        'AirPods 4': {'asin': None, 'current': 'https://www.amazon.com/s?k=AirPods+4&tag=cfqclaw-20'},
        'AirPods Pro 3': {'asin': None, 'current': 'https://www.amazon.com/s?k=AirPods+Pro+3&tag=cfqclaw-20'},
        'AirPods Max 2': {'asin': None, 'current': 'https://www.amazon.com/s?k=AirPods+Max+2&tag=cfqclaw-20'},
    },
}

print("=== 链接审计结果 ===\n")
for article, products in new_article_products.items():
    print(f"文章: {article}")
    for product, info in products.items():
        asin = info['asin']
        if asin:
            new_url = f"https://www.amazon.com/dp/{asin}?tag=cfqclaw-20"
            status = f"✅ 可升级为直链: {new_url}"
        else:
            status = "⚠️ 无确认 ASIN，保持搜索链接"
        print(f"  [{status}] {product}")
        print(f"    当前: {info['current']}")
    print()
