#!/usr/bin/env python3
"""Quick inspection of actual data structure"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data" / "retailers"

for retailer_file in ['amazon_products.json', 'walmart_products.json', 'homedepot_products.json']:
    print(f"\n{'='*70}")
    print(f"{retailer_file}")
    print('='*70)
    try:
        with open(DATA_DIR / retailer_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                print(f"Type: List with {len(data)} items")
                print(f"\nFirst item keys:")
                for key in data[0].keys():
                    value = data[0][key]
                    if isinstance(value, str):
                        value_preview = value[:60] + "..." if len(value) > 60 else value
                    else:
                        value_preview = str(value)[:60]
                    print(f"  {key}: {value_preview}")
            elif isinstance(data, dict):
                print(f"Type: Dict")
                print(f"Keys: {list(data.keys())}")
    except Exception as e:
        print(f"ERROR: {e}")
