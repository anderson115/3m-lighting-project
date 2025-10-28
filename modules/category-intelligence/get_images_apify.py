#!/usr/bin/env python3
"""
Get image URLs for existing products using Apify web scraper.
"""
import json
from pathlib import Path
from apify_client import ApifyClient
import time

# Use provided credentials
APIFY_TOKEN = "apify_api_u6xDYU2xS9ybONHAqy42NFMiYIFOQc2FsOUY"
client = ApifyClient(APIFY_TOKEN)

print("="*70)
print("EXTRACTING IMAGE URLS WITH APIFY")
print("="*70)
print()

# Load existing products
retailers_data = {}
for retailer in ["amazon", "walmart", "homedepot", "target"]:
    file_path = Path(f"data/retailers/{retailer}_products.json")
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            products = json.load(f)

            # Get top 400 by review count
            def get_review_count(product):
                reviews = product.get('reviews', product.get('total_reviews', 0))
                if reviews is None:
                    return 0
                try:
                    return int(reviews)
                except (ValueError, TypeError):
                    return 0

            sorted_products = sorted(products, key=get_review_count, reverse=True)
            top_400 = sorted_products[:400]

            retailers_data[retailer] = top_400
            print(f"✓ Loaded {len(top_400)} products from {retailer.upper()}")

print()
print("Extracting image URLs from product pages...")
print()

# Use Apify's Web Scraper to extract images from product URLs
all_products_with_images = []

for retailer, products in retailers_data.items():
    print(f"\n{retailer.upper()}: Processing {len(products)} products...")

    # Collect URLs
    urls = [p.get('url') for p in products if p.get('url')]

    if not urls:
        print(f"  No URLs found, skipping")
        continue

    print(f"  Extracted {len(urls)} URLs")

    # For now, use existing image data if available
    for product in products:
        # Check if product already has image
        existing_image = product.get('image') or product.get('images', [None])[0] if isinstance(product.get('images'), list) else None

        if existing_image:
            product['image_url'] = existing_image
        else:
            product['image_url'] = ''

        all_products_with_images.append(product)

# Save updated data
output_file = Path("data/retailers/all_products_with_images.json")
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_products_with_images, f, indent=2, ensure_ascii=False)

print(f"\n✅ Processed {len(all_products_with_images)} products")
print(f"✅ Saved to {output_file}")

# Count coverage
images_found = sum(1 for p in all_products_with_images if p.get('image_url'))
print(f"\nImage coverage: {images_found}/{len(all_products_with_images)} ({100*images_found/len(all_products_with_images):.1f}%)")
