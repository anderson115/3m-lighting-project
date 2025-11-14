#!/usr/bin/env python3
"""Full inspection including attributes"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data" / "retailers"

for retailer_file in ['amazon_products.json', 'walmart_products.json', 'homedepot_products.json', 'target_products.json', 'etsy_products.json']:
    print(f"\n{'='*70}")
    print(f"{retailer_file}")
    print('='*70)
    try:
        with open(DATA_DIR / retailer_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                item = data[0]
                print(f"Total items: {len(data)}")
                print(f"\nAll top-level keys: {list(item.keys())}")

                # Check if attributes has description
                if 'attributes' in item and isinstance(item['attributes'], dict):
                    print(f"\nAttributes keys: {list(item['attributes'].keys())[:10]}")
                    if 'description' in item['attributes']:
                        desc = item['attributes']['description']
                        print(f"\nDescription (in attributes): {desc[:100] if isinstance(desc, str) else desc}...")

                # Check for description at top level
                if 'description' in item:
                    desc = item['description']
                    print(f"\nDescription (top-level): {desc[:100] if isinstance(desc, str) else desc}...")

                # Show taxonomy_path structure
                if 'taxonomy_path' in item:
                    print(f"\nTaxonomy path: {item['taxonomy_path']}")

    except Exception as e:
        print(f"ERROR: {e}")
