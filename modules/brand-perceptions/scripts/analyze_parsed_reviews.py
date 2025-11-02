#!/usr/bin/env python3
"""Analyze parsed review JSON file."""

import json
from pathlib import Path
from collections import Counter

def main():
    file_path = Path(__file__).parent.parent / 'data' / 'collected' / '3m-garage-reviews-parsed.json'

    with open(file_path, 'r') as f:
        reviews = json.load(f)

    print(f"Total reviews: {len(reviews)}")

    brands = Counter(r['brand'] for r in reviews)
    products = Counter(r['product_id'] for r in reviews)

    print(f"\nBy Brand:")
    for brand, count in sorted(brands.items()):
        print(f"  {brand}: {count}")

    print(f"\nBy Product ID:")
    for product_id, count in sorted(products.items()):
        print(f"  {product_id}: {count}")

    print(f"\nBy Product Title:")
    product_titles = {}
    for r in reviews:
        key = r['product_id']
        if key not in product_titles:
            product_titles[key] = {
                'title': r['product_title'][:80],
                'count': 0
            }
        product_titles[key]['count'] += 1

    for pid, info in sorted(product_titles.items()):
        print(f"  {pid}: {info['count']} reviews")
        print(f"    {info['title']}...")

    # Check for any anomalies
    print(f"\n\nAnomalies:")
    long_reviews = [r for r in reviews if len(r['review_text']) > 1000]
    if long_reviews:
        print(f"  Found {len(long_reviews)} reviews with text > 1000 chars (possible merge issues)")
        for r in long_reviews[:3]:
            print(f"    - {r['author']}: {len(r['review_text'])} chars")
            print(f"      Preview: {r['review_text'][:200]}...")
    else:
        print(f"  No long reviews detected")

if __name__ == '__main__':
    main()
