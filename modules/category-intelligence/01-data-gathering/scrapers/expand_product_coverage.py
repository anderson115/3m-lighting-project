#!/usr/bin/env python3
"""
Expand product coverage with ratings and reviews
Budget: $25 Bright Data API
Priority: Amazon (reviews), Target (ratings), Lowe's (missing ratings)
"""

import asyncio
import json
import os
from playwright.async_api import async_playwright
from datetime import datetime
from pathlib import Path

# Bright Data credentials
BRIGHTDATA_ENDPOINT = "wss://brd-customer-hl_694870e0-zone-category_intelligence_module:lk3i01g4z7u2@brd.superproxy.io:9222"

# Output directory
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "expanded_coverage"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class ProductScraper:
    def __init__(self, use_brightdata=True):
        self.use_brightdata = use_brightdata
        self.products_scraped = 0
        self.max_products_per_retailer = 200  # Reduced for reliability

    async def scrape_amazon_with_reviews(self, search_terms):
        """Scrape Amazon products with review data"""
        print("\n🔍 Scraping Amazon products with reviews...")

        async with async_playwright() as p:
            if self.use_brightdata:
                browser = await p.chromium.connect_over_cdp(BRIGHTDATA_ENDPOINT)
            else:
                browser = await p.chromium.launch(headless=True)

            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )

            page = await context.new_page()
            all_products = []

            for term in search_terms:
                if self.products_scraped >= self.max_products_per_retailer:
                    break

                print(f"  Searching: {term}")

                try:
                    # Search Amazon
                    search_url = f"https://www.amazon.com/s?k={term.replace(' ', '+')}"
                    await page.goto(search_url, wait_until="domcontentloaded", timeout=120000)
                    await page.wait_for_timeout(5000)

                    # Extract product cards
                    products = await page.evaluate("""() => {
                        const items = [];
                        const cards = document.querySelectorAll('[data-component-type="s-search-result"]');

                        cards.forEach(card => {
                            try {
                                const titleEl = card.querySelector('h2 a span');
                                const priceEl = card.querySelector('.a-price .a-offscreen');
                                const ratingEl = card.querySelector('.a-icon-star-small .a-icon-alt');
                                const reviewCountEl = card.querySelector('span[aria-label*="stars"]');
                                const linkEl = card.querySelector('h2 a');
                                const imageEl = card.querySelector('img.s-image');

                                if (titleEl && priceEl) {
                                    // Extract rating value
                                    let rating = null;
                                    if (ratingEl) {
                                        const ratingText = ratingEl.textContent;
                                        const match = ratingText.match(/([0-9.]+)/);
                                        if (match) rating = parseFloat(match[1]);
                                    }

                                    // Extract review count
                                    let reviewCount = null;
                                    if (reviewCountEl) {
                                        const reviewText = reviewCountEl.getAttribute('aria-label') || '';
                                        const match = reviewText.match(/([0-9,]+)/);
                                        if (match) reviewCount = parseInt(match[1].replace(/,/g, ''));
                                    }

                                    items.push({
                                        title: titleEl.textContent.trim(),
                                        price: priceEl.textContent.replace('$', '').trim(),
                                        rating: rating,
                                        reviewCount: reviewCount,
                                        url: linkEl ? 'https://amazon.com' + linkEl.getAttribute('href') : null,
                                        image: imageEl ? imageEl.getAttribute('src') : null,
                                        asin: linkEl ? linkEl.getAttribute('href').match(/dp\\/([A-Z0-9]+)/)?.[1] : null
                                    });
                                }
                            } catch (e) {
                                console.error('Error parsing product:', e);
                            }
                        });

                        return items;
                    }""")

                    print(f"    Found {len(products)} products")

                    # For products with high review counts, scrape actual reviews
                    for product in products[:20]:  # Limit to top 20 per search
                        if self.products_scraped >= self.max_products_per_retailer:
                            break

                        if product.get('reviewCount', 0) > 50 and product.get('asin'):
                            reviews = await self.scrape_amazon_reviews(page, product['asin'])
                            product['reviews'] = reviews
                            product['search_term'] = term
                            product['retailer'] = 'Amazon'
                            product['scraped_at'] = datetime.now().isoformat()
                            all_products.append(product)
                            self.products_scraped += 1

                            if self.products_scraped % 10 == 0:
                                print(f"    ✓ Scraped {self.products_scraped} products with reviews")

                    await page.wait_for_timeout(1000)

                except Exception as e:
                    print(f"    ⚠ Error scraping {term}: {e}")
                    continue

            await browser.close()

            # Save results
            output_file = OUTPUT_DIR / f"amazon_with_reviews_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(all_products, f, indent=2)

            print(f"\n✓ Saved {len(all_products)} Amazon products to {output_file}")
            return all_products

    async def scrape_amazon_reviews(self, page, asin, max_reviews=10):
        """Scrape reviews for a specific product"""
        try:
            review_url = f"https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_dp_d_show_all_btm?sortBy=recent"
            await page.goto(review_url, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(1500)

            reviews = await page.evaluate("""() => {
                const reviewEls = document.querySelectorAll('[data-hook="review"]');
                const reviews = [];

                reviewEls.forEach(rev => {
                    try {
                        const titleEl = rev.querySelector('[data-hook="review-title"]');
                        const bodyEl = rev.querySelector('[data-hook="review-body"]');
                        const ratingEl = rev.querySelector('[data-hook="review-star-rating"]');
                        const dateEl = rev.querySelector('[data-hook="review-date"]');
                        const verifiedEl = rev.querySelector('[data-hook="avp-badge"]');

                        if (titleEl && bodyEl) {
                            reviews.push({
                                title: titleEl.textContent.trim(),
                                body: bodyEl.textContent.trim(),
                                rating: ratingEl ? parseFloat(ratingEl.textContent.match(/([0-9.]+)/)?.[1]) : null,
                                date: dateEl ? dateEl.textContent.trim() : null,
                                verified: verifiedEl ? true : false
                            });
                        }
                    } catch (e) {}
                });

                return reviews;
            }""")

            return reviews[:max_reviews]

        except Exception as e:
            print(f"      ⚠ Could not scrape reviews for {asin}: {e}")
            return []

    async def scrape_target(self, search_terms):
        """Scrape Target products with ratings"""
        print("\n🔍 Scraping Target products...")

        async with async_playwright() as p:
            if self.use_brightdata:
                browser = await p.chromium.connect_over_cdp(BRIGHTDATA_ENDPOINT)
            else:
                browser = await p.chromium.launch(headless=True)

            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()
            all_products = []

            for term in search_terms:
                if len(all_products) >= self.max_products_per_retailer:
                    break

                print(f"  Searching: {term}")

                try:
                    search_url = f"https://www.target.com/s?searchTerm={term.replace(' ', '+')}"
                    await page.goto(search_url, wait_until="networkidle", timeout=60000)
                    await page.wait_for_timeout(3000)

                    # Scroll to load more products
                    for _ in range(3):
                        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        await page.wait_for_timeout(1000)

                    products = await page.evaluate("""() => {
                        const items = [];
                        const cards = document.querySelectorAll('[data-test="product-grid"] [data-test*="product"]');

                        cards.forEach(card => {
                            try {
                                const titleEl = card.querySelector('[data-test="product-title"]');
                                const priceEl = card.querySelector('[data-test="current-price"]');
                                const ratingEl = card.querySelector('[data-test="ratings"]');
                                const linkEl = card.querySelector('a[href*="/p/"]');
                                const imageEl = card.querySelector('img');

                                if (titleEl) {
                                    let rating = null;
                                    let reviewCount = null;

                                    if (ratingEl) {
                                        const ratingText = ratingEl.textContent;
                                        const ratingMatch = ratingText.match(/([0-9.]+)/);
                                        if (ratingMatch) rating = parseFloat(ratingMatch[1]);

                                        const reviewMatch = ratingText.match(/\\(([0-9]+)\\)/);
                                        if (reviewMatch) reviewCount = parseInt(reviewMatch[1]);
                                    }

                                    items.push({
                                        title: titleEl.textContent.trim(),
                                        price: priceEl ? priceEl.textContent.replace('$', '').trim() : null,
                                        rating: rating,
                                        reviewCount: reviewCount,
                                        url: linkEl ? 'https://www.target.com' + linkEl.getAttribute('href') : null,
                                        image: imageEl ? imageEl.getAttribute('src') : null
                                    });
                                }
                            } catch (e) {}
                        });

                        return items;
                    }""")

                    for product in products:
                        product['search_term'] = term
                        product['retailer'] = 'Target'
                        product['scraped_at'] = datetime.now().isoformat()

                    all_products.extend(products)
                    print(f"    Found {len(products)} products (total: {len(all_products)})")

                except Exception as e:
                    print(f"    ⚠ Error: {e}")

            await browser.close()

            # Save
            output_file = OUTPUT_DIR / f"target_products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(all_products, f, indent=2)

            print(f"\n✓ Saved {len(all_products)} Target products to {output_file}")
            return all_products

    async def scrape_lowes_missing_ratings(self):
        """Scrape missing Lowe's ratings"""
        print("\n🔍 Filling Lowe's missing ratings...")

        # Load existing Lowe's products without ratings
        existing_file = Path(__file__).parent.parent / "data" / "retailers" / "lowes_products.json"

        if not existing_file.exists():
            print("  ⚠ No existing Lowe's data found")
            return []

        with open(existing_file) as f:
            products = json.load(f)

        products_without_ratings = [p for p in products if not p.get('rating')]
        print(f"  Found {len(products_without_ratings)} products without ratings")

        # Re-scrape with ratings
        # (Implementation similar to Target but for Lowe's)

        return []


async def main():
    scraper = ProductScraper(use_brightdata=True)

    # Search terms for garage organization
    search_terms = [
        "garage hooks heavy duty",
        "garage storage hooks",
        "garage wall organizer",
        "garage shelving",
        "garage bike hooks",
        "garage tool holder",
        "garage pegboard",
        "garage ceiling storage",
        "garage overhead rack",
        "garage cabinets",
        "garage slatwall",
        "garage hose reel",
        "garage lumber rack",
        "garage sports equipment storage"
    ]

    print("=" * 80)
    print("PRODUCT DATA EXPANSION - Garage Organization Category")
    print("=" * 80)
    print(f"Budget: $25 Bright Data")
    print(f"Target: 500+ products per retailer with ratings/reviews")
    print("=" * 80)

    # 1. Scrape Amazon with reviews (priority for evaluation features)
    amazon_products = await scraper.scrape_amazon_with_reviews(search_terms[:10])

    # 2. Scrape Target
    target_products = await scraper.scrape_target(search_terms)

    print("\n" + "=" * 80)
    print("SCRAPING COMPLETE")
    print("=" * 80)
    print(f"Amazon products with reviews: {len(amazon_products)}")
    print(f"Target products with ratings: {len(target_products)}")
    print(f"Total new products: {len(amazon_products) + len(target_products)}")
    print(f"\nData saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
