#!/usr/bin/env python3
"""Check for image fields and description in attributes"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data" / "retailers"

for retailer_file in ['amazon_products.json', 'walmart_products.json', 'homedepot_products.json']:
    print(f"\n{'='*70}")
    print(f"{retailer_file}")
    print('='*70)
    with open(DATA_DIR / retailer_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        item = data[0]

        # Check for image field
        if 'image' in item:
            print(f"IMAGE field exists: {item['image'][:80]}")
        else:
            print("NO image field at top level")

        # Check attributes in detail
        if 'attributes' in item:
            attrs = item['attributes']
            print(f"\nAttributes structure:")
            for key, value in attrs.items():
                if isinstance(value, (str, int, float, bool)):
                    print(f"  {key}: {str(value)[:60]}")
                elif isinstance(value, dict):
                    print(f"  {key}: [dict with {len(value)} keys: {list(value.keys())[:5]}]")
                elif isinstance(value, list):
                    print(f"  {key}: [list with {len(value)} items]")
                    if len(value) > 0:
                        print(f"    First item: {str(value[0])[:60]}")
