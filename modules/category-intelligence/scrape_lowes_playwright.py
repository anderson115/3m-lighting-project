#!/usr/bin/env python3
"""
Scrape Lowe's garage organization using Playwright (FREE - no API needed).
"""
import json
import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

async def scrape_lowes():
    products = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        search_url = "https://www.lowes.com/search?searchTerm=garage+organization+hooks"

        print(f"Navigating to Lowe's...")
        await page.goto(search_url, wait_until="networkidle")
        await asyncio.sleep(3)

        # Scroll to load more products
        for i in range(10):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(1)

        print("Extracting product data...")

        # Extract product grid
        product_cards = await page.query_selector_all('[data-selector="product-card"], .product-pod, .search-product')

        for card in product_cards[:400]:
            try:
                # Extract data
                title_elem = await card.query_selector('h2, .product-title, [data-selector="product-title"]')
                title = await title_elem.inner_text() if title_elem else ""

                price_elem = await card.query_selector('[data-selector="product-price"], .product-price, .price')
                price_text = await price_elem.inner_text() if price_elem else ""

                link_elem = await card.query_selector('a[href*="/pd/"]')
                link = await link_elem.get_attribute("href") if link_elem else ""
                if link and not link.startswith("http"):
                    link = f"https://www.lowes.com{link}"

                img_elem = await card.query_selector('img')
                img_url = await img_elem.get_attribute("src") if img_elem else ""

                # Rating
                rating_elem = await card.query_selector('[data-selector="star-rating"], .star-rating')
                rating_text = await rating_elem.get_attribute("aria-label") if rating_elem else ""

                if title:
                    products.append({
                        "name": title.strip(),
                        "price": price_text.strip(),
                        "url": link,
                        "image": img_url,
                        "rating_text": rating_text.strip(),
                        "retailer": "Lowes"
                    })

                    if len(products) % 50 == 0:
                        print(f"  Extracted {len(products)} products...")

                if len(products) >= 400:
                    break

            except Exception as e:
                continue

        await browser.close()

    return products

async def main():
    print("="*70)
    print("LOWE'S SCRAPING (PLAYWRIGHT - FREE)")
    print("="*70)
    print()

    products = await scrape_lowes()

    print(f"\n✅ Extracted {len(products)} products")

    # Save
    output_file = Path("data/retailers/lowes_products.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved to {output_file}")

if __name__ == "__main__":
    asyncio.run(main())
