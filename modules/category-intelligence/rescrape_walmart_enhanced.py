#!/usr/bin/env python3
"""
Re-scrape Walmart with enhanced data: images, specifications, variants.
"""
import os
import json
from apify_client import ApifyClient

APIFY_TOKEN = os.getenv('APIFY_API_TOKEN', 'YOUR_TOKEN_HERE')
client = ApifyClient(APIFY_TOKEN)

print("="*70)
print("WALMART RE-SCRAPE (ENHANCED DATA)")
print("="*70)

run_input = {
    "startUrls": [
        "https://www.walmart.com/browse/home/garage-organization/4044_1032619_6735625",
        "https://www.walmart.com/search?q=garage+hooks",
        "https://www.walmart.com/search?q=slatwall+system"
    ],
    "maxItems": 400,
    "proxy": {
        "useApifyProxy": True
    }
}

try:
    print("Starting Walmart Product Data Extractor...")
    run = client.actor("epctex/walmart-scraper").call(run_input=run_input)

    print(f"✅ Completed! Run ID: {run['id']}")

    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    print(f"✅ Retrieved {len(items)} products")

    output_file = "data/retailers/walmart_products_enhanced.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved to {output_file}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
