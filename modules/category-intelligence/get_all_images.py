#!/usr/bin/env python3
"""
Extract image URLs for all products using Apify web scraper.
"""
import json
import os
from pathlib import Path
from apify_client import ApifyClient
import time

APIFY_TOKEN = os.getenv('APIFY_TOKEN')
if not APIFY_TOKEN:
    raise ValueError("APIFY_TOKEN environment variable not set. Run with: op run -- python get_all_images.py")

client = ApifyClient(APIFY_TOKEN)

print("="*70)
print("EXTRACTING IMAGE URLS WITH APIFY")
print("="*70)
print()

# Load products with enhanced data
with open('data/retailers/all_products_enhanced_heuristic.json', 'r') as f:
    all_products = json.load(f)

print(f"Loaded {len(all_products)} products")
print()

# Group by retailer
by_retailer = {}
for p in all_products:
    retailer = p.get('retailer', 'unknown')
    if retailer not in by_retailer:
        by_retailer[retailer] = []
    by_retailer[retailer].append(p)

# For each retailer, batch scrape product pages for images
for retailer, products in by_retailer.items():
    print(f"\n{retailer.upper()}: Extracting images for {len(products)} products...")

    # Take sample of URLs (limit to avoid huge scrape)
    urls = [p.get('url') for p in products if p.get('url')][:100]

    if not urls:
        print(f"  No URLs found")
        continue

    print(f"  Scraping {len(urls)} product pages...")

    run_input = {
        "startUrls": [{"url": url} for url in urls],
        "pageFunction": """async function pageFunction(context) {
            const { request, log, jQuery: $ } = context;

            // Try multiple selectors for images
            let image = '';
            const selectors = [
                'img[data-main-image]',
                'img.main-image',
                'img[class*="product-image"]',
                'img[id*="product"]',
                '.product-media img',
                '#product-image img',
                'img[alt*="product"]'
            ];

            for (const selector of selectors) {
                const img = $(selector).first();
                if (img.length) {
                    image = img.attr('src') || img.attr('data-src') || '';
                    if (image) break;
                }
            }

            return {
                url: request.url,
                image: image
            };
        }""",
        "maxRequestsPerCrawl": 100,
        "proxyConfiguration": {"useApifyProxy": True}
    }

    try:
        run = client.actor("apify/web-scraper").call(run_input=run_input)
        results = list(client.dataset(run["defaultDatasetId"]).iterate_items())

        # Map images back to products
        image_map = {r['url']: r.get('image', '') for r in results if r.get('url')}

        for product in products:
            url = product.get('url')
            if url in image_map:
                product['image_url'] = image_map[url]

        found = sum(1 for p in products if p.get('image_url'))
        print(f"  ✅ Found images for {found}/{len(products)} products")

    except Exception as e:
        print(f"  ❌ Error: {e}")
        continue

# Save updated data
output_file = Path("data/retailers/all_products_with_images_final.json")
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_products, f, indent=2, ensure_ascii=False)

total_images = sum(1 for p in all_products if p.get('image_url'))
print(f"\n✅ Total products with images: {total_images}/{len(all_products)} ({100*total_images/len(all_products):.1f}%)")
print(f"✅ Saved to {output_file}")
