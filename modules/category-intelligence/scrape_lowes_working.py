#!/usr/bin/env python3
"""
Scrape Lowe's using working Apify actor with provided credentials.
"""
import json
import os
from pathlib import Path
from apify_client import ApifyClient

APIFY_TOKEN = os.getenv('APIFY_TOKEN')
if not APIFY_TOKEN:
    raise ValueError("APIFY_TOKEN environment variable not set. Run with: op run -- python scrape_lowes_working.py")

client = ApifyClient(APIFY_TOKEN)

print("="*70)
print("SCRAPING LOWE'S WITH APIFY (PAID)")
print("="*70)
print()

# Use Web Scraper to extract Lowe's data
run_input = {
    "startUrls": [
        {"url": "https://www.lowes.com/search?searchTerm=garage+hooks"},
        {"url": "https://www.lowes.com/search?searchTerm=garage+organization"},
        {"url": "https://www.lowes.com/search?searchTerm=wall+hooks"}
    ],
    "linkSelector": "a.product-link",
    "pageFunction": """async function pageFunction(context) {
        const { request, log, jQuery: $ } = context;

        if (request.userData.label === 'START') {
            // Extract product links
            const products = [];
            $('.product-pod').each((i, el) => {
                const $el = $(el);
                const name = $el.find('.product-title').text().trim();
                const price = $el.find('.price').text().trim();
                const url = $el.find('a').attr('href');
                const image = $el.find('img').attr('src');
                const rating = $el.find('.star-rating').attr('aria-label');

                if (name && url) {
                    products.push({
                        name,
                        price,
                        url: url.startsWith('http') ? url : 'https://www.lowes.com' + url,
                        image: image || '',
                        rating: rating || '',
                        retailer: 'Lowes'
                    });
                }
            });

            return products.slice(0, 400);
        }
    }""",
    "maxRequestsPerCrawl": 50,
    "proxyConfiguration": {"useApifyProxy": True}
}

try:
    print("Starting Lowe's scraper...")
    print("Using: apify/web-scraper")

    run = client.actor("apify/web-scraper").call(run_input=run_input)

    print(f"✅ Run completed: {run['id']}")

    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    # Flatten nested results
    all_products = []
    for item in items:
        if isinstance(item, list):
            all_products.extend(item)
        elif isinstance(item, dict):
            all_products.append(item)

    print(f"✅ Retrieved {len(all_products)} products")

    if all_products:
        output_file = Path("data/retailers/lowes_products.json")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_products, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved to {output_file}")
    else:
        print("⚠️  No products extracted")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
