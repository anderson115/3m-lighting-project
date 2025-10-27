#!/usr/bin/env python3
"""
Best Seller Rank (BSR) Sales Tracker
Tracks Amazon BSR and review velocity to estimate monthly sales.
Free method using public Amazon data.
"""

import os
import sys
import json
import time
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from dotenv import load_dotenv

# Load environment variables
project_root = Path(__file__).parent.parent.parent
load_dotenv(project_root / '.env')

# Add core to path
sys.path.insert(0, str(project_root / 'core'))

# Try to import scraping libraries
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: Missing required libraries. Install with:")
    print("  pip install requests beautifulsoup4")
    sys.exit(1)


class BSRSalesTracker:
    """Tracks Amazon Best Seller Rank and estimates sales velocity."""

    def __init__(self, db_path=None, delay=2.0):
        """
        Initialize tracker.

        Args:
            db_path: Path to SQLite database (default: data/bsr_tracking.db)
            delay: Delay between requests in seconds (default: 2.0)
        """
        self.delay = delay

        # Set up database
        if db_path is None:
            db_path = Path(__file__).parent / "data" / "bsr_tracking.db"

        self.db_path = db_path
        self.db_path.parent.mkdir(exist_ok=True)

        self._init_database()

    def _init_database(self):
        """Initialize SQLite database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                asin TEXT PRIMARY KEY,
                title TEXT,
                brand TEXT,
                category TEXT,
                current_price REAL,
                first_tracked TEXT,
                last_tracked TEXT
            )
        """)

        # BSR history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bsr_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asin TEXT NOT NULL,
                bsr INTEGER,
                category_rank TEXT,
                price REAL,
                in_stock BOOLEAN,
                tracked_at TEXT,
                FOREIGN KEY (asin) REFERENCES products(asin)
            )
        """)

        # Review history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS review_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asin TEXT NOT NULL,
                total_reviews INTEGER,
                avg_rating REAL,
                tracked_at TEXT,
                FOREIGN KEY (asin) REFERENCES products(asin)
            )
        """)

        # Sales estimates table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales_estimates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asin TEXT NOT NULL,
                estimated_monthly_sales INTEGER,
                estimation_method TEXT,
                confidence_level TEXT,
                calculated_at TEXT,
                FOREIGN KEY (asin) REFERENCES products(asin)
            )
        """)

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_bsr_asin ON bsr_history(asin)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_bsr_date ON bsr_history(tracked_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_review_asin ON review_history(asin)")

        conn.commit()
        conn.close()

    def scrape_product_data(self, asin):
        """
        Scrape current product data from Amazon.

        Args:
            asin: Amazon product ASIN

        Returns:
            Dictionary with product data or None if failed
        """
        url = f"https://www.amazon.com/dp/{asin}"

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            response = requests.get(url, headers=headers, timeout=30)

            if response.status_code != 200:
                print(f"  WARNING: Got status {response.status_code}")
                return None

            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract product data
            data = {
                'asin': asin,
                'tracked_at': datetime.now().isoformat()
            }

            # Title
            title_elem = soup.find('span', {'id': 'productTitle'})
            data['title'] = title_elem.get_text(strip=True) if title_elem else None

            # Brand
            brand_elem = soup.find('a', {'id': 'bylineInfo'})
            if brand_elem:
                data['brand'] = brand_elem.get_text(strip=True).replace('Visit the', '').replace('Store', '').strip()
            else:
                data['brand'] = None

            # Price
            price_elem = soup.find('span', {'class': 'a-offscreen'})
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                try:
                    data['price'] = float(price_text.replace('$', '').replace(',', ''))
                except:
                    data['price'] = None
            else:
                data['price'] = None

            # In stock
            availability = soup.find('div', {'id': 'availability'})
            data['in_stock'] = True
            if availability:
                avail_text = availability.get_text(strip=True).lower()
                if 'unavailable' in avail_text or 'out of stock' in avail_text:
                    data['in_stock'] = False

            # BSR (Best Seller Rank)
            data['bsr'] = None
            data['category_rank'] = None

            # Try multiple BSR locations
            product_details = soup.find('div', {'id': 'detailBulletsWrapper_feature_div'})
            if product_details:
                for li in product_details.find_all('li'):
                    text = li.get_text()
                    if 'Best Sellers Rank' in text or 'Amazon Best Sellers Rank' in text:
                        # Extract first rank number (main BSR)
                        try:
                            bsr_text = text.split('#')[1].split('in')[0].strip()
                            data['bsr'] = int(bsr_text.replace(',', ''))

                            # Extract category
                            category_parts = text.split('in')[1].split('(')[0].strip()
                            data['category_rank'] = category_parts
                        except:
                            pass
                        break

            # Alternative BSR location (table format)
            if data['bsr'] is None:
                details_table = soup.find('table', {'id': 'productDetails_detailBullets_sections1'})
                if details_table:
                    for row in details_table.find_all('tr'):
                        th = row.find('th')
                        if th and 'Best Sellers Rank' in th.get_text():
                            td = row.find('td')
                            if td:
                                try:
                                    bsr_text = td.get_text().split('#')[1].split('in')[0].strip()
                                    data['bsr'] = int(bsr_text.replace(',', ''))

                                    category_parts = td.get_text().split('in')[1].split('(')[0].strip()
                                    data['category_rank'] = category_parts
                                except:
                                    pass
                                break

            # Review count
            data['total_reviews'] = 0
            reviews_elem = soup.find('span', {'id': 'acrCustomerReviewText'})
            if reviews_elem:
                try:
                    review_text = reviews_elem.get_text(strip=True)
                    data['total_reviews'] = int(review_text.split()[0].replace(',', ''))
                except:
                    pass

            # Average rating
            data['avg_rating'] = None
            rating_elem = soup.find('span', {'class': 'a-icon-alt'})
            if rating_elem:
                try:
                    rating_text = rating_elem.get_text(strip=True)
                    data['avg_rating'] = float(rating_text.split()[0])
                except:
                    pass

            return data

        except requests.exceptions.RequestException as e:
            print(f"  ERROR: Request failed: {e}")
            return None
        except Exception as e:
            print(f"  ERROR: Parsing failed: {e}")
            return None

    def save_tracking_data(self, data):
        """Save scraped data to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        asin = data['asin']
        tracked_at = data['tracked_at']

        try:
            # Update or insert product
            cursor.execute("""
                INSERT INTO products (asin, title, brand, category, current_price, first_tracked, last_tracked)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(asin) DO UPDATE SET
                    title = COALESCE(excluded.title, title),
                    brand = COALESCE(excluded.brand, brand),
                    category = COALESCE(excluded.category, category),
                    current_price = COALESCE(excluded.current_price, current_price),
                    last_tracked = excluded.last_tracked
            """, (
                asin,
                data.get('title'),
                data.get('brand'),
                data.get('category_rank'),
                data.get('price'),
                tracked_at,
                tracked_at
            ))

            # Insert BSR history
            if data.get('bsr') is not None:
                cursor.execute("""
                    INSERT INTO bsr_history (asin, bsr, category_rank, price, in_stock, tracked_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    asin,
                    data['bsr'],
                    data.get('category_rank'),
                    data.get('price'),
                    data.get('in_stock', True),
                    tracked_at
                ))

            # Insert review history
            if data.get('total_reviews') is not None:
                cursor.execute("""
                    INSERT INTO review_history (asin, total_reviews, avg_rating, tracked_at)
                    VALUES (?, ?, ?, ?)
                """, (
                    asin,
                    data['total_reviews'],
                    data.get('avg_rating'),
                    tracked_at
                ))

            conn.commit()

        except Exception as e:
            print(f"  ERROR: Database save failed: {e}")
            conn.rollback()
        finally:
            conn.close()

    def estimate_monthly_sales(self, bsr, category='Home & Kitchen'):
        """
        Estimate monthly sales from BSR.

        Formula based on Jungle Scout published data for Home & Kitchen category.

        Args:
            bsr: Best Seller Rank
            category: Product category (currently only Home & Kitchen supported)

        Returns:
            Estimated monthly sales, confidence level
        """
        if bsr is None:
            return None, 'none'

        # Home & Kitchen > Storage & Organization formula
        if bsr < 100:
            sales = 3500 - (bsr * 25)
            confidence = 'high'
        elif bsr < 1000:
            sales = 2500 - (bsr * 2)
            confidence = 'high'
        elif bsr < 10000:
            sales = 1500 - (bsr * 0.15)
            confidence = 'medium'
        elif bsr < 50000:
            sales = 100 - (bsr * 0.001)
            confidence = 'low'
        else:
            sales = 50
            confidence = 'very_low'

        # Ensure non-negative
        sales = max(0, int(sales))

        return sales, confidence

    def calculate_review_velocity(self, asin, days=30):
        """
        Calculate review velocity (reviews per day) for recent period.

        Args:
            asin: Amazon ASIN
            days: Number of days to analyze

        Returns:
            Reviews per day, estimated monthly sales based on 1-2% conversion
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get recent review counts
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()

        cursor.execute("""
            SELECT total_reviews, tracked_at
            FROM review_history
            WHERE asin = ? AND tracked_at >= ?
            ORDER BY tracked_at ASC
        """, (asin, cutoff_date))

        rows = cursor.fetchall()
        conn.close()

        if len(rows) < 2:
            return None, None

        # Calculate change
        first_count = rows[0][0]
        last_count = rows[-1][0]
        review_increase = last_count - first_count

        if review_increase <= 0:
            return 0, 0

        # Reviews per day
        reviews_per_day = review_increase / days

        # Estimate sales (assuming 1-2% of buyers leave reviews)
        # Using conservative 2% rate
        estimated_sales_per_day = reviews_per_day / 0.02
        estimated_monthly_sales = int(estimated_sales_per_day * 30)

        return reviews_per_day, estimated_monthly_sales

    def generate_sales_estimate(self, asin):
        """
        Generate comprehensive sales estimate for a product.

        Combines BSR method and review velocity method.

        Args:
            asin: Amazon ASIN

        Returns:
            Dictionary with sales estimates
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get latest BSR
        cursor.execute("""
            SELECT bsr, tracked_at
            FROM bsr_history
            WHERE asin = ?
            ORDER BY tracked_at DESC
            LIMIT 1
        """, (asin,))

        bsr_row = cursor.fetchone()
        conn.close()

        result = {
            'asin': asin,
            'calculated_at': datetime.now().isoformat()
        }

        # BSR-based estimate
        if bsr_row:
            bsr, tracked_at = bsr_row
            sales_bsr, confidence = self.estimate_monthly_sales(bsr)

            result['bsr'] = bsr
            result['bsr_tracked_at'] = tracked_at
            result['estimated_sales_bsr'] = sales_bsr
            result['bsr_confidence'] = confidence

        # Review velocity estimate
        reviews_per_day, sales_velocity = self.calculate_review_velocity(asin, days=30)

        if reviews_per_day is not None:
            result['reviews_per_day'] = round(reviews_per_day, 2)
            result['estimated_sales_velocity'] = sales_velocity

        # Combined estimate (average if both available)
        if 'estimated_sales_bsr' in result and 'estimated_sales_velocity' in result:
            result['estimated_sales_combined'] = int(
                (result['estimated_sales_bsr'] + result['estimated_sales_velocity']) / 2
            )
            result['estimation_method'] = 'combined'
        elif 'estimated_sales_bsr' in result:
            result['estimated_sales_combined'] = result['estimated_sales_bsr']
            result['estimation_method'] = 'bsr_only'
        elif 'estimated_sales_velocity' in result:
            result['estimated_sales_combined'] = result['estimated_sales_velocity']
            result['estimation_method'] = 'velocity_only'
        else:
            result['estimated_sales_combined'] = None
            result['estimation_method'] = 'none'

        # Save estimate to database
        if result.get('estimated_sales_combined'):
            self._save_estimate(result)

        return result

    def _save_estimate(self, estimate):
        """Save sales estimate to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO sales_estimates
            (asin, estimated_monthly_sales, estimation_method, confidence_level, calculated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            estimate['asin'],
            estimate['estimated_sales_combined'],
            estimate['estimation_method'],
            estimate.get('bsr_confidence', 'unknown'),
            estimate['calculated_at']
        ))

        conn.commit()
        conn.close()


def main():
    """Main entry point for testing."""
    import argparse

    parser = argparse.ArgumentParser(description='Track Amazon BSR and estimate sales')
    parser.add_argument('asins', nargs='+', help='Amazon ASINs to track')
    parser.add_argument('--delay', type=float, default=2.0, help='Delay between requests (seconds)')
    parser.add_argument('--output', help='Output JSON file path')

    args = parser.parse_args()

    print("="*70)
    print("BSR SALES TRACKER")
    print(f"Products to track: {len(args.asins)}")
    print("="*70)
    print()

    tracker = BSRSalesTracker(delay=args.delay)

    results = []
    for i, asin in enumerate(args.asins, 1):
        print(f"\n[{i}/{len(args.asins)}] Tracking ASIN: {asin}")
        print("-"*70)

        # Scrape current data
        print("  Scraping Amazon data...")
        data = tracker.scrape_product_data(asin)

        if not data:
            print("  ERROR: Could not scrape product data")
            continue

        # Save to database
        tracker.save_tracking_data(data)

        # Print current data
        print(f"\n  CURRENT DATA:")
        title = data.get('title') or 'N/A'
        print(f"    Title: {title[:60]}...")
        print(f"    Brand: {data.get('brand') or 'N/A'}")
        print(f"    Price: ${data.get('price', 0):.2f}")
        print(f"    BSR: {data.get('bsr', 'N/A'):,}" if data.get('bsr') else "    BSR: N/A")
        print(f"    Reviews: {data.get('total_reviews', 0):,}")
        print(f"    Rating: {data.get('avg_rating', 0):.1f}/5.0" if data.get('avg_rating') else "    Rating: N/A")
        print(f"    In Stock: {'Yes' if data.get('in_stock') else 'No'}")

        # Generate sales estimate
        print("\n  Calculating sales estimate...")
        estimate = tracker.generate_sales_estimate(asin)

        print(f"\n  SALES ESTIMATE:")
        if estimate.get('estimated_sales_combined'):
            print(f"    Estimated Monthly Sales: {estimate['estimated_sales_combined']:,} units")
            print(f"    Estimation Method: {estimate['estimation_method']}")

            if 'estimated_sales_bsr' in estimate:
                print(f"    BSR Method: {estimate['estimated_sales_bsr']:,} units ({estimate['bsr_confidence']} confidence)")

            if 'estimated_sales_velocity' in estimate:
                print(f"    Velocity Method: {estimate['estimated_sales_velocity']:,} units")
                print(f"    Review Velocity: {estimate['reviews_per_day']:.1f} reviews/day")
        else:
            print("    Could not estimate sales (insufficient data)")

        results.append(estimate)

        # Add delay between products
        if i < len(args.asins):
            time.sleep(args.delay)

    # Save results to JSON
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"\n\nResults saved to: {output_path}")

    print("\n" + "="*70)
    print("TRACKING COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
