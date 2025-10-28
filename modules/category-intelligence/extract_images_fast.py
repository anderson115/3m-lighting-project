#!/usr/bin/env python3
"""
Fast image URL extraction using direct HTTP requests.
"""
import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def extract_image_from_url(url, retailer):
    """Extract image URL from product page."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.content, 'html.parser')

        # Retailer-specific selectors
        selectors = {
            'amazon': ['#landingImage', '#imgBlkFront', 'img[data-a-image-name="landingImage"]'],
            'walmart': ['img[data-testid="product-image"]', '.prod-hero-image img', 'img[itemprop="image"]'],
            'homedepot': ['img.mediagallery__mainimage', 'img[itemprop="image"]', '.media-gallery__image img'],
            'target': ['img[data-test="product-image"]', 'img.styles__Image', 'picture img']
        }

        # Try retailer-specific selectors
        for selector in selectors.get(retailer.lower(), []):
            img = soup.select_one(selector)
            if img:
                image_url = img.get('src') or img.get('data-src')
                if image_url and image_url.startswith('http'):
                    return image_url

        # Fallback: Find any large product image
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src')
            if src and any(keyword in src.lower() for keyword in ['product', 'image', 'main', 'hero']):
                if src.startswith('http') and any(ext in src.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                    return src

        return None

    except Exception as e:
        return None

print("="*70)
print("FAST IMAGE URL EXTRACTION")
print("="*70)
print()

# Load enhanced product data
with open('data/retailers/all_products_enhanced_heuristic.json', 'r') as f:
    products = json.load(f)

print(f"Loaded {len(products)} products")
print(f"Extracting images for sample of products (max 50 per retailer)...")
print()

# Sample products by retailer (take top 50 by reviews from each)
by_retailer = {}
for p in products:
    retailer = p.get('retailer', 'unknown')
    if retailer not in by_retailer:
        by_retailer[retailer] = []
    by_retailer[retailer].append(p)

# Extract images with threading for speed
extracted_count = 0
failed_count = 0

for retailer, retailer_products in by_retailer.items():
    print(f"\n{retailer.upper()}:")

    # Sort by review count and take top 50
    def get_reviews(p):
        try:
            return int(p.get('reviews', p.get('total_reviews', 0)) or 0)
        except:
            return 0

    top_products = sorted(retailer_products, key=get_reviews, reverse=True)[:50]

    # Only extract for products without images
    urls_to_fetch = [(p, p['url']) for p in top_products if p.get('url') and not p.get('image')]

    if not urls_to_fetch:
        print(f"  Skipping (no URLs or already has images)")
        continue

    print(f"  Extracting images for {len(urls_to_fetch)} products...")

    # Use ThreadPoolExecutor for parallel requests
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(extract_image_from_url, url, retailer): product
                   for product, url in urls_to_fetch}

        for future in as_completed(futures):
            product = futures[future]
            try:
                image_url = future.result()
                if image_url:
                    product['image'] = image_url
                    extracted_count += 1
                else:
                    failed_count += 1
            except Exception as e:
                failed_count += 1

    found = sum(1 for p in top_products if p.get('image'))
    print(f"  ✅ Extracted {found} images")

# Save updated data
output_file = Path('data/retailers/all_products_enhanced_with_images.json')
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(products, f, indent=2, ensure_ascii=False)

total_images = sum(1 for p in products if p.get('image'))
print(f"\n{'='*70}")
print(f"EXTRACTION COMPLETE")
print(f"{'='*70}")
print(f"Successfully extracted: {extracted_count}")
print(f"Failed: {failed_count}")
print(f"Total products with images: {total_images}/{len(products)} ({100*total_images/len(products):.1f}%)")
print(f"\n✅ Saved to {output_file}")
