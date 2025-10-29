#!/usr/bin/env python3
"""
Use SearchAPI.io Google Shopping - works with aggregated results.
Note: Google Shopping returns aggregated product listings without direct retailer URLs.
"""
import requests
import json
from pathlib import Path
import pandas as pd
import time
from dotenv import load_dotenv
import os
import hashlib

print("="*80)
print("GOOGLE SHOPPING via SearchAPI (Aggregated Mode)")
print("="*80)

# Load API key
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)
SEARCHAPI_KEY = os.getenv('SEARCHAPI_KEY')

if not SEARCHAPI_KEY:
    print("\n❌ ERROR: SEARCHAPI_KEY not found in .env file")
    exit(1)

print(f"✅ API key loaded")

# Load existing
existing_file = Path("/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/category-intelligence/04_CATEGORY_DATA_ALL_PRODUCTS.xlsx")
df_existing = pd.read_excel(existing_file)

print(f"Existing dataset: {len(df_existing):,} products\n")

# Focused queries for missing segments
SEARCH_QUERIES = [
    ("kobalt garage storage", "Kobalt/Lowes"),
    ("menards garage storage", "Menards"),
    ("gladiator garage cabinets", "Premium"),
    ("overhead garage storage", "Missing category"),
]

print("Target: Fill Kobalt, Menards, Premium gaps")
print(f"Queries: {len(SEARCH_QUERIES)}\n")

all_products = []

for i, (query, target) in enumerate(SEARCH_QUERIES):
    print(f"{i+1}/{len(SEARCH_QUERIES)} '{query}' → {target}")

    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": SEARCHAPI_KEY,
        "num": 40,
    }

    try:
        response = requests.get("https://www.searchapi.io/api/v1/search", params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            results = data.get("shopping_results", [])

            for product in results:
                # Map seller to our retailer format
                seller = product.get('seller', '')
                retailer = 'Unknown'
                if 'lowes' in seller.lower() or "lowe's" in seller.lower():
                    retailer = 'Lowes'
                elif 'home depot' in seller.lower() or 'homedepot' in seller.lower():
                    retailer = 'Homedepot'
                elif 'menards' in seller.lower():
                    retailer = 'Menards'
                elif 'walmart' in seller.lower():
                    retailer = 'Walmart'
                elif 'amazon' in seller.lower():
                    retailer = 'Amazon'
                elif 'target' in seller.lower():
                    retailer = 'Target'

                # Create synthetic ID (since we don't have URLs)
                product_id = product.get('product_id', '')
                synthetic_url = f"google-shopping://{product_id}"

                all_products.append({
                    'title': product.get('title', ''),
                    'price': product.get('extracted_price'),
                    'url': synthetic_url,
                    'retailer': retailer,
                    'seller': seller,
                    'rating': product.get('rating'),
                    'reviews': product.get('reviews'),
                    'product_id': product_id
                })

            print(f"  → {len(results)} products")

        time.sleep(1)

    except Exception as e:
        print(f"  Error: {e}")

print(f"\n{'='*80}")
print(f"RESULTS: {len(all_products)} products")
print(f"{'='*80}\n")

if all_products:
    # Distribution
    retailers = {}
    for p in all_products:
        ret = p['retailer']
        retailers[ret] = retailers.get(ret, 0) + 1

    print("By retailer:")
    for retailer, count in sorted(retailers.items(), key=lambda x: x[1], reverse=True):
        print(f"  {retailer:15s} {count:4d}")

    # Key fills
    kobalt = len([p for p in all_products if 'kobalt' in p['title'].lower()])
    menards = len([p for p in all_products if p['retailer'] == 'Menards'])

    print(f"\nKey fills:")
    print(f"  Kobalt: {kobalt}")
    print(f"  Menards: {menards}")

    # Save just the supplemental data
    output = Path("/tmp/google_shopping_supplement.json")
    with open(output, 'w') as f:
        json.dump(all_products, f, indent=2)

    print(f"\n✅ Saved to {output}")

    # Show sample
    print(f"\nSample products:")
    for i, p in enumerate(all_products[:5]):
        print(f"{i+1}. {p['title'][:60]}")
        print(f"   ${p['price']} at {p['seller']}")

else:
    print("No products found")
