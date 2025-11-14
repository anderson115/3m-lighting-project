#!/usr/bin/env python3
"""
Amazon review scraper using local browser with user login
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = DATA_DIR / "reviews"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

async def scrape_reviews_with_login():
    """Use local browser for Amazon review scraping (user will log in)"""
    print("=" * 80)
    print("AMAZON REVIEW SCRAPING - With User Login")
    print("=" * 80)
    print("\n🌐 Opening browser to Amazon...")
    print("   Please sign in to your Amazon account when the browser opens.")
    print("   After signing in, press ENTER in this terminal to continue...")

    async with async_playwright() as p:
        # Launch visible Chrome browser
        browser = await p.chromium.launch(
            headless=False,
            channel="chrome"
        )

        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()

        # Navigate to Amazon
        await page.goto("https://www.amazon.com", wait_until="domcontentloaded")

        print("\n✓ Browser opened!")
        print("   1. Sign in to Amazon")
        print("   2. You have 2 minutes to complete the login")
        print("   3. Scraping will begin automatically in 2 minutes")

        # Wait for user to sign in (2 minutes)
        print("\n⏳ Waiting 120 seconds for you to sign in...")
        for remaining in range(120, 0, -10):
            print(f"   {remaining} seconds remaining...")
            await asyncio.sleep(10)
        print("\n✓ Starting scraping now!")

        # Load products to scrape from consolidated data
        consolidated_files = list((DATA_DIR / "consolidated").glob("master_dataset_*.json"))
        if not consolidated_files:
            print("❌ No consolidated data found!")
            await browser.close()
            return

        latest_file = sorted(consolidated_files)[-1]
        print(f"\n📂 Loading products from: {latest_file.name}")

        with open(latest_file, 'r') as f:
            master_data = json.load(f)

        products = master_data.get('products', [])

        # Filter Amazon products with ASINs
        amazon_products = []
        for p in products:
            asin = p.get('asin')
            if asin and p.get('rating'):
                try:
                    p['rating_float'] = float(p.get('rating'))
                    amazon_products.append(p)
                except:
                    pass

        # Sort by rating and take top 50
        amazon_products.sort(key=lambda x: x.get('rating_float', 0), reverse=True)
        target_products = amazon_products[:50]

        print(f"✓ Found {len(target_products)} products to scrape")
        print(f"\n🔍 Starting review extraction...\n")

        all_reviews = []
        products_with_reviews = []

        for i, product in enumerate(target_products, 1):
            asin = product.get('asin')
            title = (product.get('title') or '')[:60]
            rating = product.get('rating_float', 0)
            brand = product.get('brand') or 'Unknown'

            print(f"[{i}/{len(target_products)}] {brand} - {rating:.1f}★")
            print(f"         {asin}")
            if title:
                print(f"         {title}...")

            try:
                # Navigate to reviews page
                review_url = f"https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_dp_d_show_all_btm?sortBy=recent"
                await page.goto(review_url, wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_timeout(2000)

                # Extract reviews using JavaScript
                reviews = await page.evaluate("""() => {
                    const reviewData = [];
                    const reviewDivs = document.querySelectorAll('[data-hook="review"]');

                    reviewDivs.forEach((review, idx) => {
                        if (idx >= 20) return; // Max 20 reviews per product

                        try {
                            const titleEl = review.querySelector('[data-hook="review-title"]');
                            const bodyEl = review.querySelector('[data-hook="review-body"]');
                            const ratingEl = review.querySelector('[data-hook="review-star-rating"]');
                            const dateEl = review.querySelector('[data-hook="review-date"]');
                            const verifiedEl = review.querySelector('[data-hook="avp-badge"]');

                            const title = titleEl ? titleEl.textContent.trim() : null;
                            const body = bodyEl ? bodyEl.textContent.trim() : null;
                            const ratingText = ratingEl ? ratingEl.textContent.trim() : null;
                            const date = dateEl ? dateEl.textContent.trim() : null;
                            const verified = verifiedEl !== null;

                            let rating = null;
                            if (ratingText) {
                                const match = ratingText.match(/([0-9.]+)/);
                                if (match) rating = parseFloat(match[1]);
                            }

                            if (title && body) {
                                reviewData.push({
                                    title: title,
                                    body: body,
                                    rating: rating,
                                    date: date,
                                    verified: verified
                                });
                            }
                        } catch (e) {
                            console.error('Error parsing review:', e);
                        }
                    });

                    return reviewData;
                }""")

                if reviews:
                    product_review_data = {
                        'asin': asin,
                        'title': product.get('title'),
                        'brand': brand,
                        'rating': rating,
                        'url': product.get('url'),
                        'reviews': reviews,
                        'review_count': len(reviews),
                        'scraped_at': datetime.now().isoformat()
                    }
                    products_with_reviews.append(product_review_data)
                    all_reviews.extend(reviews)
                    print(f"         ✓ {len(reviews)} reviews extracted (total: {len(all_reviews)})")
                else:
                    print(f"         ⚠ No reviews found")

                # Save checkpoint every 10 products
                if i % 10 == 0:
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    checkpoint_file = OUTPUT_DIR / f"reviews_checkpoint_{timestamp}.json"
                    with open(checkpoint_file, 'w') as f:
                        json.dump({
                            'scraped_at': datetime.now().isoformat(),
                            'products_count': len(products_with_reviews),
                            'total_reviews': len(all_reviews),
                            'products': products_with_reviews
                        }, f, indent=2)
                    print(f"         💾 Checkpoint: {len(all_reviews)} reviews saved")

                await page.wait_for_timeout(3000)  # Polite delay

            except Exception as e:
                print(f"         ❌ Error: {e}")
                continue

        await browser.close()

        # Save final results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = OUTPUT_DIR / f"amazon_reviews_authenticated_{timestamp}.json"

        with open(output_file, 'w') as f:
            json.dump({
                'scraped_at': datetime.now().isoformat(),
                'products_scraped': len(products_with_reviews),
                'total_reviews': len(all_reviews),
                'products': products_with_reviews
            }, f, indent=2)

        print("\n" + "=" * 80)
        print("REVIEW SCRAPING COMPLETE")
        print("=" * 80)
        print(f"\n📊 Results:")
        print(f"  Products with reviews: {len(products_with_reviews):,}")
        print(f"  Total reviews extracted: {len(all_reviews):,}")
        print(f"  Avg reviews per product: {len(all_reviews) / len(products_with_reviews) if products_with_reviews else 0:.1f}")
        print(f"\n💾 Saved to: {output_file}")
        print(f"   File size: {output_file.stat().st_size / 1024 / 1024:.1f} MB")

        return products_with_reviews


async def main():
    await scrape_reviews_with_login()


if __name__ == "__main__":
    asyncio.run(main())
