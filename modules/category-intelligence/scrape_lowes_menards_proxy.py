#!/usr/bin/env python3
"""
Scrape Lowe's and Menards using Bright Data proxy or direct Apify actors.
"""
from apify_client import ApifyClient
import json
from pathlib import Path

APIFY_TOKEN = "apify_api_u6xDYU2xS9ybONHAqy42NFMiYIFOQc2FsOUY"
client = ApifyClient(APIFY_TOKEN)

print("="*70)
print("SCRAPING LOWE'S AND MENARDS WITH APIFY")
print("="*70)
print()

# Try multiple Apify actors for Lowe's and Menards
retailers = {
    "lowes": {
        "urls": [
            "https://www.lowes.com/search?searchTerm=garage+hooks",
            "https://www.lowes.com/search?searchTerm=garage+organization",
            "https://www.lowes.com/search?searchTerm=wall+hooks",
            "https://www.lowes.com/search?searchTerm=garage+storage"
        ]
    },
    "menards": {
        "urls": [
            "https://www.menards.com/main/search.html?search=garage+hooks",
            "https://www.menards.com/main/search.html?search=garage+organization",
            "https://www.menards.com/main/search.html?search=wall+hooks",
            "https://www.menards.com/main/search.html?search=garage+storage"
        ]
    }
}

for retailer, config in retailers.items():
    print(f"\n{'='*70}")
    print(f"SCRAPING {retailer.upper()}")
    print(f"{'='*70}")

    all_products = []

    # Try using generic web scraper
    for url in config["urls"]:
        print(f"\nScraping: {url}")

        run_input = {
            "startUrls": [{"url": url}],
            "pageFunction": """async function pageFunction(context) {
                const { request, log, jQuery: $ } = context;
                const products = [];

                // Generic product selectors
                const productSelectors = [
                    '.product',
                    '.product-pod',
                    '.product-card',
                    '[data-product]',
                    '[class*="product"]'
                ];

                for (const selector of productSelectors) {
                    $(selector).each((i, el) => {
                        const $el = $(el);
                        const name = $el.find('[class*="title"], [class*="name"], h2, h3').first().text().trim();
                        const price = $el.find('[class*="price"]').first().text().trim();
                        const url = $el.find('a').first().attr('href');
                        const image = $el.find('img').first().attr('src');
                        const rating = $el.find('[class*="rating"], [class*="star"]').first().text().trim();

                        if (name && name.length > 0) {
                            products.push({
                                name,
                                price,
                                url: url ? (url.startsWith('http') ? url : request.loadedUrl + url) : '',
                                image: image || '',
                                rating: rating || '',
                                retailer: request.loadedUrl.includes('lowes') ? 'Lowes' : 'Menards'
                            });
                        }
                    });

                    if (products.length > 0) break;
                }

                return products;
            }""",
            "maxRequestsPerCrawl": 10,
            "proxyConfiguration": {"useApifyProxy": True}
        }

        try:
            print(f"  Starting Apify web-scraper...")
            run = client.actor("apify/web-scraper").call(run_input=run_input)
            print(f"  Run ID: {run['id']}")

            items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

            # Flatten results
            for item in items:
                if isinstance(item, list):
                    all_products.extend(item)
                elif isinstance(item, dict):
                    all_products.append(item)

            print(f"  ✅ Extracted {len(items)} items (total so far: {len(all_products)})")

        except Exception as e:
            print(f"  ❌ Error: {e}")
            continue

    if all_products:
        output_file = Path(f"data/retailers/{retailer}_products.json")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_products, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Saved {len(all_products)} {retailer} products to {output_file}")
    else:
        print(f"\n❌ No {retailer} products scraped")

print(f"\n{'='*70}")
print("SCRAPING COMPLETE")
print(f"{'='*70}")
