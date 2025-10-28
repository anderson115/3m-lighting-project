#!/usr/bin/env python3
"""
Re-scrape all retailers (Amazon, Walmart, Home Depot, Target) with enhanced data.
"""
import json
from pathlib import Path
from apify_client import ApifyClient
import time

def load_apify_credentials():
    """Load Apify credentials from env file."""
    env_path = Path("/Volumes/DATA/config/offbrain/category-intelligence/apify.env")
    if not env_path.exists():
        raise FileNotFoundError(f"Credentials file not found: {env_path}")

    credentials = {}
    for line in env_path.read_text().splitlines():
        if not line or line.strip().startswith("#"):
            continue
        key, _, value = line.partition("=")
        credentials[key.strip()] = value.strip()

    return credentials["APIFY_API_TOKEN"]

print("="*70)
print("RE-SCRAPING ALL RETAILERS WITH ENHANCED DATA")
print("="*70)
print()

# Load credentials
token = load_apify_credentials()
client = ApifyClient(token)

retailers = [
    {
        "name": "Amazon",
        "actor": "junglee/amazon-crawler",
        "input": {
            "startUrls": [
                {"url": "https://www.amazon.com/s?k=garage+hooks&rh=n%3A495224"},
                {"url": "https://www.amazon.com/s?k=garage+organization&rh=n%3A495224"},
                {"url": "https://www.amazon.com/s?k=slatwall+hooks"}
            ],
            "maxItems": 400,
            "proxy": {"useApifyProxy": True},
            "includeDescription": True,
            "includeImages": True
        },
        "output": "data/retailers/amazon_products_enhanced.json"
    },
    {
        "name": "Walmart",
        "actor": "epctex/walmart-scraper",
        "input": {
            "startUrls": [
                "https://www.walmart.com/browse/home/garage-organization/4044_1032619_6735625",
                "https://www.walmart.com/search?q=garage+hooks",
                "https://www.walmart.com/search?q=slatwall+system"
            ],
            "maxItems": 400,
            "proxy": {"useApifyProxy": True}
        },
        "output": "data/retailers/walmart_products_enhanced.json"
    },
    {
        "name": "Home Depot",
        "actor": "epctex/home-depot-scraper",
        "input": {
            "startUrls": [
                "https://www.homedepot.com/b/Storage-Organization-Garage-Storage/N-5yc1vZc89t",
                "https://www.homedepot.com/s/garage%2520hooks"
            ],
            "maxItems": 400,
            "proxy": {"useApifyProxy": True}
        },
        "output": "data/retailers/homedepot_products_enhanced.json"
    },
    {
        "name": "Target",
        "actor": "epctex/target-scraper",
        "input": {
            "startUrls": [
                "https://www.target.com/s?searchTerm=garage+hooks",
                "https://www.target.com/s?searchTerm=garage+organization"
            ],
            "maxItems": 400,
            "proxy": {"useApifyProxy": True}
        },
        "output": "data/retailers/target_products_enhanced.json"
    }
]

for retailer in retailers:
    print(f"\n{'='*70}")
    print(f"SCRAPING {retailer['name'].upper()}")
    print('='*70)

    try:
        print(f"Actor: {retailer['actor']}")
        print(f"Target: {retailer['input']['maxItems']} products")
        print()

        run = client.actor(retailer["actor"]).call(run_input=retailer["input"])

        print(f"✅ Completed! Run ID: {run['id']}")

        items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        print(f"✅ Retrieved {len(items)} products")

        output_file = Path(retailer["output"])
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(items, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved to {output_file}")

        # Brief pause between retailers
        time.sleep(2)

    except Exception as e:
        print(f"❌ Error scraping {retailer['name']}: {e}")
        import traceback
        traceback.print_exc()
        continue

print("\n" + "="*70)
print("SCRAPING COMPLETE")
print("="*70)
