#!/usr/bin/env python3
"""
Scrape Lowe's using Bright Data API.
"""
import requests
import json
import os
from pathlib import Path

BRIGHTDATA_API_TOKEN = os.getenv('BRIGHTDATA_API_TOKEN')
if not BRIGHTDATA_API_TOKEN:
    raise ValueError("BRIGHTDATA_API_TOKEN environment variable not set. Run with: op run -- python scrape_lowes_brightdata.py")

print("="*70)
print("SCRAPING LOWE'S WITH BRIGHT DATA")
print("="*70)
print()

# Bright Data Web Unlocker API endpoint
url = "https://api.brightdata.com/datasets/v3/trigger"

queries = [
    "garage hooks",
    "garage organization",
    "wall hooks",
    "garage storage",
    "tool hooks"
]

all_products = []

for query in queries:
    print(f"Scraping query: {query}")

    # Bright Data request
    payload = {
        "dataset_id": "gd_l6q5p3vz3k4wf4rm",  # Generic ecommerce scraper
        "endpoint": "search",
        "discover_by": "keyword",
        "keyword": [query],
        "domain": ["lowes.com"],
        "limit": 100
    }

    headers = {
        "Authorization": f"Bearer {BRIGHTDATA_API_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"  Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"  Response: {data}")

            # Get snapshot ID to poll for results
            if "snapshot_id" in data:
                snapshot_id = data["snapshot_id"]
                print(f"  Snapshot ID: {snapshot_id}")

                # Poll for results
                import time
                time.sleep(5)

                results_url = f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}"
                results_response = requests.get(results_url, headers=headers)

                if results_response.status_code == 200:
                    results = results_response.json()
                    print(f"  Got {len(results)} results")
                    all_products.extend(results)
                else:
                    print(f"  Failed to get results: {results_response.text}")
        else:
            print(f"  Error: {response.text}")

    except Exception as e:
        print(f"  Exception: {e}")
        import traceback
        traceback.print_exc()

if all_products:
    output_file = Path("data/retailers/lowes_products_brightdata.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_products, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Saved {len(all_products)} products to {output_file}")
else:
    print("\n❌ No products scraped")
