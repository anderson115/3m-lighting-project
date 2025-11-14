#!/usr/bin/env python3
"""
Simple Amazon scraper using requests + BeautifulSoup
More reliable than browser automation for bulk data collection
"""

import requests
import json
import time
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import random

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "expanded_coverage"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class SimpleAmazonScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })

    def scrape_search_page(self, search_term, max_pages=5):
        """Scrape Amazon search results"""
        print(f"\n🔍 Scraping Amazon: {search_term}")
        all_products = []

        for page_num in range(1, max_pages + 1):
            try:
                url = f"https://www.amazon.com/s?k={search_term.replace(' ', '+')}&page={page_num}"
                print(f"  Page {page_num}...", end=" ", flush=True)

                response = self.session.get(url, timeout=30)
                time.sleep(random.uniform(2, 4))  # Polite delay

                if response.status_code != 200:
                    print(f"❌ Status {response.status_code}")
                    break

                soup = BeautifulSoup(response.content, 'html.parser')

                # Find product cards
                products = soup.find_all('div', {'data-component-type': 's-search-result'})

                for product in products:
                    try:
                        # Extract data
                        title_elem = product.find('h2')
                        title = title_elem.text.strip() if title_elem else None

                        price_elem = product.find('span', {'class': 'a-offscreen'})
                        price = price_elem.text.replace('$', '').strip() if price_elem else None

                        rating_elem = product.find('span', {'class': 'a-icon-alt'})
                        rating = None
                        if rating_elem:
                            rating_text = rating_elem.text
                            try:
                                rating = float(rating_text.split()[0])
                            except:
                                pass

                        # Try multiple methods to get review count
                        review_count = None

                        # Method 1: Look for aria-label with ratings
                        review_elems = product.find_all('span', {'aria-label': True})
                        for elem in review_elems:
                            aria_label = elem.get('aria-label', '')
                            if 'ratings' in aria_label.lower() or 'rating' in aria_label.lower():
                                try:
                                    # Extract numbers like "1,234 ratings"
                                    num_str = ''.join(filter(lambda x: x.isdigit() or x == ',', aria_label))
                                    review_count = int(num_str.replace(',', ''))
                                    break
                                except:
                                    pass

                        # Method 2: Look for text containing ratings
                        if not review_count:
                            rating_text_elem = product.find('span', string=lambda text: text and 'rating' in text.lower())
                            if rating_text_elem:
                                try:
                                    text = rating_text_elem.get_text()
                                    nums = ''.join(filter(lambda x: x.isdigit() or x == ',', text.split()[0]))
                                    review_count = int(nums.replace(',', ''))
                                except:
                                    pass

                        link_elem = product.find('a', {'class': 'a-link-normal'})
                        asin = None
                        url = None
                        if link_elem and 'href' in link_elem.attrs:
                            href = link_elem['href']
                            url = f"https://www.amazon.com{href}"
                            if '/dp/' in href:
                                asin = href.split('/dp/')[1].split('/')[0]

                        if title and price:
                            all_products.append({
                                'title': title,
                                'price': price,
                                'rating': rating,
                                'reviewCount': review_count,
                                'asin': asin,
                                'url': url,
                                'search_term': search_term,
                                'retailer': 'Amazon',
                                'scraped_at': datetime.now().isoformat()
                            })

                    except Exception as e:
                        continue

                print(f"✓ Found {len(products)} products")

                if len(products) == 0:
                    break  # No more results

            except Exception as e:
                print(f"❌ Error: {e}")
                break

        return all_products

    def scrape_product_reviews(self, asin, max_reviews=20):
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
            return []


def main():
    scraper = SimpleAmazonScraper()

    search_terms = [
        "garage hooks heavy duty",
        "garage storage hooks wall mount",
        "garage organization pegboard",
        "garage bike storage hooks",
        "garage shelving heavy duty",
        "garage tool organizer wall",
        "garage overhead storage rack",
        "garage wall mount bike rack"
    ]

    print("=" * 80)
    print("AMAZON PRODUCT SCRAPING - Garage Organization")
    print("=" * 80)

    all_products = []

    # Scrape search results
    for term in search_terms:
        products = scraper.scrape_search_page(term, max_pages=3)
        all_products.extend(products)
        print(f"  Total products so far: {len(all_products)}")
        time.sleep(2)

    # Remove duplicates based on ASIN
    unique_products = {}
    for p in all_products:
        asin = p.get('asin')
        if asin and asin not in unique_products:
            unique_products[asin] = p

    all_products = list(unique_products.values())

    print(f"\n✓ Total unique products: {len(all_products)}")

    # Scrape reviews for top products (those with most reviews)
    products_with_reviews = [p for p in all_products if (p.get('reviewCount') or 0) > 50]
    products_with_reviews.sort(key=lambda x: (x.get('reviewCount') or 0), reverse=True)

    print(f"\n🔍 Scraping reviews for top {min(50, len(products_with_reviews))} products...")

    for i, product in enumerate(products_with_reviews[:50], 1):
        asin = product.get('asin')
        if asin:
            print(f"  [{i}/50] {asin[:10]}... ", end="", flush=True)
            reviews = scraper.scrape_product_reviews(asin, max_reviews=15)
            product['reviews'] = reviews
            print(f"✓ {len(reviews)} reviews")
            time.sleep(random.uniform(2, 4))

    # Save results
    output_file = OUTPUT_DIR / f"amazon_products_with_reviews_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(all_products, f, indent=2)

    print("\n" + "=" * 80)
    print("SCRAPING COMPLETE")
    print("=" * 80)
    print(f"Total products: {len(all_products)}")
    print(f"Products with reviews: {sum(1 for p in all_products if p.get('reviews'))}")
    print(f"Total reviews collected: {sum(len(p.get('reviews', [])) for p in all_products)}")
    print(f"\nSaved to: {output_file}")


if __name__ == "__main__":
    main()
