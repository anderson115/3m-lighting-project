#!/usr/bin/env python3
"""
Re-scrape Amazon with enhanced data: images, specifications, attributes.
"""
import os
import json
from apify_client import ApifyClient

APIFY_TOKEN = os.getenv('APIFY_API_TOKEN', 'YOUR_TOKEN_HERE')
client = ApifyClient(APIFY_TOKEN)

print("="*70)
print("AMAZON RE-SCRAPE (ENHANCED DATA)")
print("="*70)

# Amazon garage organization category URL
run_input = {
    "startUrls": [
        {"url": "https://www.amazon.com/s?k=garage+hooks&rh=n%3A495224"},
        {"url": "https://www.amazon.com/s?k=garage+organization&rh=n%3A495224"},
        {"url": "https://www.amazon.com/s?k=slatwall+hooks"}
    ],
    "maxItems": 400,
    "proxy": {
        "useApifyProxy": True
    },
    "includeDescription": True,
    "includeImages": True
}

try:
    print("Starting Amazon Product Scraper...")
    run = client.actor("junglee/amazon-crawler").call(run_input=run_input)

    print(f"✅ Completed! Run ID: {run['id']}")

    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    print(f"✅ Retrieved {len(items)} products")

    output_file = "data/retailers/amazon_products_enhanced.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved to {output_file}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
