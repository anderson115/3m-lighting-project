#!/usr/bin/env python3
"""
Scrape Lowe's garage organization products using Apify.
Target: 400 products sorted by best sellers.
"""
import os
import json
from apify_client import ApifyClient

# Initialize client
APIFY_TOKEN = os.getenv('APIFY_API_TOKEN', 'YOUR_TOKEN_HERE')
client = ApifyClient(APIFY_TOKEN)

print("="*70)
print("LOWE'S PRODUCT SCRAPING (APIFY)")
print("="*70)
print()

# Search queries for garage organization
search_queries = [
    "https://www.lowes.com/pl/Garage-organization--Storage-organization/4294642611",
    "https://www.lowes.com/search?searchTerm=garage+hooks",
    "https://www.lowes.com/search?searchTerm=garage+hangers",
    "https://www.lowes.com/search?searchTerm=slatwall+system",
    "https://www.lowes.com/search?searchTerm=garage+storage+hooks"
]

# Configuration
run_input = {
    "startUrls": search_queries,
    "maxItems": 400,
    "proxyConfiguration": {
        "useApifyProxy": True
    }
}

print(f"Starting Apify Lowe's scraper...")
print(f"Target: 400 products")
print(f"Queries: {len(search_queries)} search URLs")
print()

try:
    # Use the easyapi Lowe's scraper
    run = client.actor("easyapi/lowes-product-scraper").call(run_input=run_input)

    print(f"✅ Scraper completed!")
    print(f"Run ID: {run['id']}")
    print()

    # Fetch results
    print("Fetching results...")
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    print(f"✅ Retrieved {len(items)} products")
    print()

    # Save raw data
    output_file = "data/retailers/lowes_products.json"
    os.makedirs("data/retailers", exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved to {output_file}")
    print()

    # Show sample
    if items:
        sample = items[0]
        print("Sample product fields:")
        for key in sample.keys():
            print(f"  - {key}")

except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
