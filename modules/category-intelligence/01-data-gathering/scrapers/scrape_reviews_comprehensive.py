#!/usr/bin/env python3
"""
Comprehensive review scraper - works with consolidated master dataset
Extracts reviews for top products based on ratings
"""

import requests
import json
import time
import random
import re
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CONSOLIDATED_DIR = DATA_DIR / "consolidated"
OUTPUT_DIR = DATA_DIR / "reviews"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class ReviewScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        })

    def extract_asin_from_url(self, url):
        """Extract ASIN from Amazon URL"""
        if not url or 'amazon.com' not in url:
            return None

        # Pattern: /dp/ASIN or /product/ASIN
        match = re.search(r'/(?:dp|product)/([A-Z0-9]{10})', url)
        if match:
            return match.group(1)
        return None

    def scrape_product_reviews(self, asin, max_reviews=20):
        """Scrape reviews for a specific product"""
        try:
            url = f"https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_dp_d_show_all_btm?sortBy=recent"
            response = self.session.get(url, timeout=30)
            time.sleep(random.uniform(2, 4))

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
                            'verified': verified,
                            'scraped_at': datetime.now().isoformat()
                        })

                except Exception as e:
                    continue

            return reviews

        except Exception as e:
            return []


def main():
    # Load consolidated master dataset
    master_files = list(CONSOLIDATED_DIR.glob("master_dataset_*.json"))
    if not master_files:
        print("❌ No master dataset found!")
        return

    latest_master = sorted(master_files)[-1]

    print("=" * 80)
    print("COMPREHENSIVE REVIEW SCRAPING")
    print("=" * 80)
    print(f"\n📂 Loading: {latest_master.name}")

    with open(latest_master, 'r') as f:
        master_data = json.load(f)

    products = master_data.get('products', [])
    print(f"✓ Loaded {len(products):,} products")

    # Identify Amazon products with valid URLs/ASINs
    scraper = ReviewScraper()
    amazon_products = []

    for p in products:
        asin = p.get('asin')
        if not asin:
            # Try to extract from URL
            url = p.get('url', '')
            asin = scraper.extract_asin_from_url(url)
            if asin:
                p['asin'] = asin  # Update product with extracted ASIN

        if asin:
            # Prioritize products with ratings
            rating = p.get('rating')
            if rating:
                try:
                    rating_float = float(rating)
                    p['rating_float'] = rating_float
                    amazon_products.append(p)
                except:
                    pass

    print(f"✓ Found {len(amazon_products):,} Amazon products with ASINs and ratings")

    # Sort by rating (highest first) to get best products
    amazon_products.sort(key=lambda x: x.get('rating_float', 0), reverse=True)

    # Take top 100 products (will extract ~2000 reviews)
    target_products = amazon_products[:100]

    print(f"\n🎯 Target: Top {len(target_products)} products by rating")
    print(f"   Expected reviews: ~{len(target_products) * 15:,}")
    print(f"   Estimated time: ~{len(target_products) * 3 / 60:.0f} minutes")

    # Extract reviews
    products_with_reviews = []
    total_reviews = 0

    print(f"\n🔍 Extracting reviews...")

    for i, product in enumerate(target_products, 1):
        asin = product.get('asin')
        title = (product.get('title') or '')[:50]
        rating = product.get('rating_float', 0)
        brand = product.get('brand') or 'Unknown'

        print(f"\n  [{i}/{len(target_products)}] {brand} - {rating:.1f}★")
        print(f"         {asin}")
        if title:
            print(f"         {title}...")

        reviews = scraper.scrape_product_reviews(asin, max_reviews=20)

        if reviews:
            product['reviews'] = reviews
            products_with_reviews.append({
                'asin': asin,
                'title': product.get('title'),
                'brand': brand,
                'rating': rating,
                'url': product.get('url'),
                'reviews': reviews,
                'review_count': len(reviews),
                'scraped_at': datetime.now().isoformat()
            })
            total_reviews += len(reviews)
            print(f"         ✓ {len(reviews)} reviews extracted (total: {total_reviews})")
        else:
            print(f"         ⚠ No reviews extracted")

        # Save progress every 10 products
        if i % 10 == 0:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            checkpoint_file = OUTPUT_DIR / f"reviews_checkpoint_{timestamp}.json"
            with open(checkpoint_file, 'w') as f:
                json.dump({
                    'scraped_at': datetime.now().isoformat(),
                    'products_count': len(products_with_reviews),
                    'total_reviews': total_reviews,
                    'products': products_with_reviews
                }, f, indent=2)
            print(f"         💾 Checkpoint saved: {total_reviews} reviews")

    # Save final results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = OUTPUT_DIR / f"amazon_reviews_top100_{timestamp}.json"

    with open(output_file, 'w') as f:
        json.dump({
            'scraped_at': datetime.now().isoformat(),
            'source': latest_master.name,
            'products_scraped': len(products_with_reviews),
            'total_reviews': total_reviews,
            'products': products_with_reviews
        }, f, indent=2)

    print("\n" + "=" * 80)
    print("REVIEW SCRAPING COMPLETE")
    print("=" * 80)
    print(f"\n📊 Results:")
    print(f"  Products with reviews: {len(products_with_reviews):,}")
    print(f"  Total reviews extracted: {total_reviews:,}")
    print(f"  Avg reviews per product: {total_reviews / len(products_with_reviews) if products_with_reviews else 0:.1f}")
    print(f"\n💾 Saved to: {output_file}")
    print(f"   File size: {output_file.stat().st_size / 1024 / 1024:.1f} MB")

    return products_with_reviews


if __name__ == "__main__":
    main()
