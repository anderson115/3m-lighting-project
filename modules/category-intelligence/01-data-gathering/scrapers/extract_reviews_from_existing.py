#!/usr/bin/env python3
"""
Extract reviews for existing Amazon products (targeted extraction)
"""

import requests
import json
import time
import random
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = DATA_DIR / "expanded_coverage"

class ReviewExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        })

    def scrape_product_reviews(self, asin, max_reviews=15):
        """Scrape reviews for a specific product"""
        try:
            url = f"https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_dp_d_show_all_btm?sortBy=recent"
            response = self.session.get(url, timeout=30)
            time.sleep(random.uniform(1.5, 3))

            if response.status_code != 200:
                return []

            soup = BeautifulSoup(response.content, 'html.parser')
            reviews = []

            review_divs = soup.find_all('div', {'data-hook': 'review'})

            for review_div in review_divs[:max_reviews]:
                try:
                    title_elem = review_div.find('a', {'data-hook': 'review-title'})
                    title = title_elem.text.strip() if title_elem else None

                    body_elem = review_div.find('span', {'data-hook': 'review-body'})
                    body = body_elem.text.strip() if body_elem else None

                    rating_elem = review_div.find('i', {'data-hook': 'review-star-rating'})
                    rating = None
                    if rating_elem:
                        try:
                            rating = float(rating_elem.text.split()[0])
                        except:
                            pass

                    date_elem = review_div.find('span', {'data-hook': 'review-date'})
                    date = date_elem.text.strip() if date_elem else None

                    verified = review_div.find('span', {'data-hook': 'avp-badge'}) is not None

                    if title and body:
                        reviews.append({
                            'title': title,
                            'body': body,
                            'rating': rating,
                            'date': date,
                            'verified': verified
                        })

                except:
                    continue

            return reviews

        except Exception as e:
            print(f"Error: {e}")
            return []


def main():
    # Load existing Amazon products
    input_file = OUTPUT_DIR / "amazon_products_with_reviews_20251104_155959.json"

    print("=" * 80)
    print("REVIEW EXTRACTION - For Existing Amazon Products")
    print("=" * 80)

    with open(input_file, 'r') as f:
        products = json.load(f)

    print(f"\n📦 Loaded {len(products)} products")

    # Filter products with high review counts
    products_for_reviews = [
        p for p in products
        if p.get('asin') and (p.get('reviewCount') or 0) > 50
    ]
    products_for_reviews.sort(key=lambda x: (x.get('reviewCount') or 0), reverse=True)

    print(f"✓ Found {len(products_for_reviews)} products with >50 reviews")
    print(f"\n🔍 Extracting reviews for top {min(50, len(products_for_reviews))} products...")

    extractor = ReviewExtractor()
    extracted_count = 0

    for i, product in enumerate(products_for_reviews[:50], 1):
        asin = product.get('asin')
        title = product.get('title', '')[:60]
        review_count = product.get('reviewCount') or 0

        print(f"\n  [{i}/50] {asin}")
        print(f"         {title}...")
        print(f"         ({review_count:,} reviews)", end=" ", flush=True)

        reviews = extractor.scrape_product_reviews(asin, max_reviews=15)

        if reviews:
            product['reviews'] = reviews
            extracted_count += 1
            print(f" ✓ Extracted {len(reviews)} reviews")
        else:
            print(f" ⚠ No reviews extracted")
            product['reviews'] = []

        time.sleep(random.uniform(2, 4))

    # Save updated products
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = OUTPUT_DIR / f"amazon_products_with_reviews_UPDATED_{timestamp}.json"

    with open(output_file, 'w') as f:
        json.dump(products, f, indent=2)

    # Calculate review stats
    total_reviews = sum(len(p.get('reviews', [])) for p in products)
    products_with_reviews = sum(1 for p in products if p.get('reviews'))

    print("\n" + "=" * 80)
    print("REVIEW EXTRACTION COMPLETE")
    print("=" * 80)
    print(f"\n📊 Results:")
    print(f"  Total products: {len(products):,}")
    print(f"  Products with reviews: {products_with_reviews:,}")
    print(f"  Total reviews extracted: {total_reviews:,}")
    print(f"  Avg reviews per product: {total_reviews / products_with_reviews if products_with_reviews > 0 else 0:.1f}")
    print(f"\n💾 Saved to: {output_file}")
    print(f"   File size: {output_file.stat().st_size / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()
