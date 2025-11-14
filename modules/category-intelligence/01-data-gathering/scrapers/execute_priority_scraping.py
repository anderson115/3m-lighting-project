#!/usr/bin/env python3
"""
Execute Priority Scraping - Category Intelligence
Optimized for category mapping and brand positioning analysis
"""

import json
import time
import random
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime
from collections import defaultdict

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "category_mapping"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class CategoryIntelligenceScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

        # Load existing Amazon data
        existing_file = Path(__file__).parent.parent / "data" / "expanded_coverage" / "amazon_products_with_reviews_20251104_155959.json"
        with open(existing_file) as f:
            self.existing_products = json.load(f)

        print(f"✓ Loaded {len(self.existing_products)} existing Amazon products")

    def select_representative_sample(self):
        """
        Priority 1: Select representative products across category
        Stratified sampling by price tier, installation type, capacity
        """
        print("\n" + "="*80)
        print("PRIORITY 1: Representative Category Sample")
        print("="*80)

        selected = {
            "mass_market": [],      # $5-20
            "mid_tier": [],         # $20-50
            "premium": [],          # $50-120
            "professional": []      # $120+
        }

        for product in self.existing_products:
            try:
                price = float(product.get('price', 0))
                rating = product.get('rating', 0)

                # Only select highly rated products for quality signal
                if not rating or rating < 4.0:
                    continue

                if 5 <= price <= 20 and len(selected["mass_market"]) < 30:
                    selected["mass_market"].append(product)
                elif 20 < price <= 50 and len(selected["mid_tier"]) < 40:
                    selected["mid_tier"].append(product)
                elif 50 < price <= 120 and len(selected["premium"]) < 40:
                    selected["premium"].append(product)
                elif price > 120 and len(selected["professional"]) < 20:
                    selected["professional"].append(product)
            except:
                continue

        # Flatten and report
        all_selected = []
        for tier, products in selected.items():
            all_selected.extend(products)
            print(f"  {tier:20s} {len(products):>3} products")

        print(f"\n✓ Total selected: {len(all_selected)} products")
        return all_selected

    def scrape_reviews_batch(self, products, reviews_per_product=20):
        """Extract reviews from selected products"""
        print(f"\n🔍 Extracting {reviews_per_product} reviews from {len(products)} products...")

        reviews_by_tier = defaultdict(list)
        total_reviews = 0

        for i, product in enumerate(products, 1):
            asin = product.get('asin')
            if not asin:
                continue

            price = float(product.get('price', 0))
            tier = "mass" if price <= 20 else "mid" if price <= 50 else "premium" if price <= 120 else "pro"

            print(f"  [{i}/{len(products)}] {tier:8s} ${price:>6.2f} {asin[:10]}... ", end="", flush=True)

            try:
                url = f"https://www.amazon.com/product-reviews/{asin}"
                response = self.session.get(url, timeout=15)
                time.sleep(random.uniform(1.5, 3))

                if response.status_code != 200:
                    print("❌")
                    continue

                soup = BeautifulSoup(response.content, 'html.parser')
                reviews = []

                review_divs = soup.find_all('div', {'data-hook': 'review'})[:reviews_per_product]

                for review_div in review_divs:
                    try:
                        title_elem = review_div.find('a', {'data-hook': 'review-title'})
                        body_elem = review_div.find('span', {'data-hook': 'review-body'})
                        rating_elem = review_div.find('i', {'data-hook': 'review-star-rating'})

                        if title_elem and body_elem:
                            review_text = body_elem.get_text(strip=True)
                            rating_val = None
                            if rating_elem:
                                try:
                                    rating_val = float(rating_elem.get_text().split()[0])
                                except:
                                    pass

                            reviews.append({
                                'title': title_elem.get_text(strip=True),
                                'body': review_text,
                                'rating': rating_val,
                                'product_asin': asin,
                                'product_price': price,
                                'product_tier': tier,
                                'verified': review_div.find('span', {'data-hook': 'avp-badge'}) is not None
                            })
                    except:
                        continue

                reviews_by_tier[tier].extend(reviews)
                total_reviews += len(reviews)
                print(f"✓ {len(reviews)} reviews")

                if i % 10 == 0:
                    print(f"    Progress: {total_reviews} total reviews | Mass:{len(reviews_by_tier['mass'])} Mid:{len(reviews_by_tier['mid'])} Premium:{len(reviews_by_tier['premium'])} Pro:{len(reviews_by_tier['pro'])}")

            except Exception as e:
                print(f"❌ {str(e)[:20]}")
                continue

        return dict(reviews_by_tier), total_reviews

    def search_3m_claw_products(self):
        """Priority 2: Find all 3M Claw products"""
        print("\n" + "="*80)
        print("PRIORITY 2: 3M Claw Brand Intelligence")
        print("="*80)

        search_terms = [
            "3M Claw hooks",
            "3M Claw drywall",
            "3M Claw heavy duty",
            "3M Claw picture hanging"
        ]

        all_claw_products = []

        for term in search_terms:
            print(f"\n  Searching: {term}")

            try:
                url = f"https://www.amazon.com/s?k={term.replace(' ', '+')}"
                response = self.session.get(url, timeout=30)
                time.sleep(random.uniform(2, 4))

                soup = BeautifulSoup(response.content, 'html.parser')
                products = soup.find_all('div', {'data-component-type': 's-search-result'})

                for product in products:
                    try:
                        title_elem = product.find('h2')
                        title = title_elem.text.strip() if title_elem else ""

                        # Only capture actual 3M Claw products
                        if "3M" not in title or "Claw" not in title:
                            continue

                        link_elem = product.find('a', {'class': 'a-link-normal'})
                        asin = None
                        if link_elem and 'href' in link_elem.attrs:
                            href = link_elem['href']
                            if '/dp/' in href:
                                asin = href.split('/dp/')[1].split('/')[0]

                        if asin and asin not in [p.get('asin') for p in all_claw_products]:
                            all_claw_products.append({
                                'asin': asin,
                                'title': title,
                                'search_term': term
                            })
                    except:
                        continue

                print(f"    Found {len([p for p in all_claw_products if p.get('search_term') == term])} Claw products")

            except Exception as e:
                print(f"    ❌ Error: {e}")

        print(f"\n✓ Total unique 3M Claw products: {len(all_claw_products)}")
        return all_claw_products


def main():
    scraper = CategoryIntelligenceScraper()

    # Priority 1: Representative sample across category
    representative_products = scraper.select_representative_sample()
    reviews_by_tier, total_reviews = scraper.scrape_reviews_batch(representative_products, reviews_per_product=20)

    # Save Priority 1 results
    output_p1 = OUTPUT_DIR / f"representative_reviews_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_p1, 'w') as f:
        json.dump({
            'reviews_by_tier': reviews_by_tier,
            'total_reviews': total_reviews,
            'products_sampled': len(representative_products),
            'timestamp': datetime.now().isoformat()
        }, f, indent=2)

    print(f"\n💾 Priority 1 saved to: {output_p1}")

    # Priority 2: 3M Claw deep dive
    claw_products = scraper.search_3m_claw_products()

    if claw_products:
        print(f"\n🔍 Extracting deep reviews for {len(claw_products)} 3M Claw products (50 reviews each)...")
        claw_reviews_by_tier, claw_total = scraper.scrape_reviews_batch(claw_products, reviews_per_product=50)

        output_p2 = OUTPUT_DIR / f"3m_claw_reviews_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_p2, 'w') as f:
            json.dump({
                'products': claw_products,
                'reviews': claw_reviews_by_tier,
                'total_reviews': claw_total,
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)

        print(f"\n💾 Priority 2 saved to: {output_p2}")

    print("\n" + "="*80)
    print("SCRAPING COMPLETE")
    print("="*80)
    print(f"Representative reviews: {total_reviews}")
    print(f"3M Claw reviews: {claw_total if claw_products else 0}")
    print(f"Total reviews collected: {total_reviews + (claw_total if claw_products else 0)}")


if __name__ == "__main__":
    main()
