#!/usr/bin/env python3
"""
Scrape Lowe's garage organization using Apify with proper credential loading.
"""
import json
from pathlib import Path
from apify_client import ApifyClient

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
print("LOWE'S PRODUCT SCRAPING (APIFY)")
print("="*70)
print()

# Load credentials
token = load_apify_credentials()
client = ApifyClient(token)

run_input = {
    "startUrls": [
        "https://www.lowes.com/search?searchTerm=garage+hooks",
        "https://www.lowes.com/search?searchTerm=garage+organization",
        "https://www.lowes.com/search?searchTerm=slatwall+hooks",
        "https://www.lowes.com/search?searchTerm=garage+storage+hooks",
        "https://www.lowes.com/search?searchTerm=wall+hooks+garage"
    ],
    "maxItems": 400,
    "proxy": {
        "useApifyProxy": True
    }
}

try:
    print("Starting Apify Lowe's scraper...")
    print("Target: 400 products")
    print("Queries: 5 search URLs")
    print()

    run = client.actor("maxcopell/lowes-product-search").call(run_input=run_input)

    print(f"✅ Completed! Run ID: {run['id']}")

    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    print(f"✅ Retrieved {len(items)} products")

    output_file = Path("data/retailers/lowes_products.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved to {output_file}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
