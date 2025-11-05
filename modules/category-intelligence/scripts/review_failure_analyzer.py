#!/usr/bin/env python3
"""
Review Failure Analyzer
Scrapes 1-2 star Amazon reviews for product failure analysis.
Uses free methods with NLP to extract failure modes and pain points.
"""

import os
import sys
import json
import time
import sqlite3
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict
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

# Try to import NLP libraries
try:
    from transformers import pipeline
    NLP_AVAILABLE = True
except ImportError:
    print("WARNING: transformers not available. Install for advanced analysis:")
    print("  pip install transformers torch")
    NLP_AVAILABLE = False


class ReviewFailureAnalyzer:
    """Scrapes and analyzes negative Amazon reviews for failure modes."""

    def __init__(self, db_path=None, delay=2.0):
        """
        Initialize analyzer.

        Args:
            db_path: Path to SQLite database (default: data/review_analysis.db)
            delay: Delay between requests in seconds (default: 2.0)
        """
        self.delay = delay

        # Set up database
        if db_path is None:
            db_path = Path(__file__).parent / "data" / "review_analysis.db"

        self.db_path = db_path
        self.db_path.parent.mkdir(exist_ok=True)

        self._init_database()

        # Set up NLP classifier if available
        self.classifier = None
        if NLP_AVAILABLE:
            try:
                print("Loading NLP model for failure classification...")
                self.classifier = pipeline(
                    "zero-shot-classification",
                    model="facebook/bart-large-mnli"
                )
                print("✓ NLP model loaded successfully")
            except Exception as e:
                print(f"WARNING: Could not load NLP model: {e}")
                print("Will use keyword-based classification instead")

        # Failure categories for classification
        self.failure_categories = [
            "broke or bent",
            "difficult to install",
            "doesn't fit or wrong size",
            "poor quality materials",
            "not as described",
            "weight capacity failure",
            "screws or fasteners failed",
            "too expensive for quality"
        ]

    def _init_database(self):
        """Initialize SQLite database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Reviews table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asin TEXT NOT NULL,
                review_id TEXT UNIQUE,
                rating INTEGER,
                title TEXT,
                body TEXT,
                date TEXT,
                verified_purchase BOOLEAN,
                helpful_votes INTEGER,
                scraped_at TEXT,
                UNIQUE(asin, review_id)
            )
        """)

        # Failure modes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS failure_modes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                review_id INTEGER,
                category TEXT,
                confidence REAL,
                keywords TEXT,
                FOREIGN KEY (review_id) REFERENCES reviews(id)
            )
        """)

        # Product summary table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_summaries (
                asin TEXT PRIMARY KEY,
                total_reviews INTEGER,
                avg_rating REAL,
                common_failures TEXT,
                last_analyzed TEXT
            )
        """)

        conn.commit()
        conn.close()

    def scrape_negative_reviews(self, asin, max_reviews=100, stars=[1, 2]):
        """
        Scrape negative reviews for a product.

        Args:
            asin: Amazon product ASIN
            max_reviews: Maximum reviews to scrape
            stars: List of star ratings to scrape (default: [1, 2])

        Returns:
            List of review dictionaries
        """
        reviews = []

        for star_rating in stars:
            print(f"\n  Scraping {star_rating}-star reviews for {asin}...")

            page = 1
            reviews_this_rating = 0

            while reviews_this_rating < max_reviews // len(stars):
                # Construct URL
                url = f"https://www.amazon.com/product-reviews/{asin}"
                params = {
                    'reviewerType': 'all_reviews',
                    'filterByStar': f'{star_rating}_star',
                    'pageNumber': page
                }

                try:
                    # Add delay to be respectful
                    if page > 1 or star_rating > min(stars):
                        time.sleep(self.delay)

                    # Make request
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                    }
                    response = requests.get(url, params=params, headers=headers, timeout=30)

                    if response.status_code != 200:
                        print(f"    WARNING: Got status {response.status_code}, stopping")
                        break

                    # Parse HTML
                    soup = BeautifulSoup(response.text, 'html.parser')
                    review_divs = soup.find_all('div', {'data-hook': 'review'})

                    if not review_divs:
                        print(f"    No more reviews found on page {page}")
                        break

                    # Extract review data
                    for review_div in review_divs:
                        try:
                            review_id = review_div.get('id', '')

                            # Title
                            title_elem = review_div.find('a', {'data-hook': 'review-title'})
                            title = title_elem.get_text(strip=True) if title_elem else ''

                            # Body
                            body_elem = review_div.find('span', {'data-hook': 'review-body'})
                            body = body_elem.get_text(strip=True) if body_elem else ''

                            # Date
                            date_elem = review_div.find('span', {'data-hook': 'review-date'})
                            date = date_elem.get_text(strip=True) if date_elem else ''

                            # Verified purchase
                            verified = bool(review_div.find('span', {'data-hook': 'avp-badge'}))

                            # Helpful votes
                            helpful_elem = review_div.find('span', {'data-hook': 'helpful-vote-statement'})
                            helpful_votes = 0
                            if helpful_elem:
                                helpful_text = helpful_elem.get_text(strip=True)
                                if 'people' in helpful_text or 'person' in helpful_text:
                                    try:
                                        helpful_votes = int(''.join(filter(str.isdigit, helpful_text)))
                                    except:
                                        pass

                            review = {
                                'asin': asin,
                                'review_id': review_id,
                                'rating': star_rating,
                                'title': title,
                                'body': body,
                                'date': date,
                                'verified_purchase': verified,
                                'helpful_votes': helpful_votes
                            }

                            reviews.append(review)
                            reviews_this_rating += 1

                            if reviews_this_rating >= max_reviews // len(stars):
                                break

                        except Exception as e:
                            print(f"    WARNING: Error parsing review: {e}")
                            continue

                    print(f"    Page {page}: {len(review_divs)} reviews scraped")
                    page += 1

                except requests.exceptions.RequestException as e:
                    print(f"    ERROR: Request failed: {e}")
                    break

            print(f"  Total {star_rating}-star reviews: {reviews_this_rating}")

        return reviews

    def classify_failure_mode(self, review_text):
        """
        Classify review into failure categories.

        Args:
            review_text: Combined title + body text

        Returns:
            List of (category, confidence) tuples
        """
        if not review_text:
            return []

        # Use NLP classifier if available
        if self.classifier:
            try:
                result = self.classifier(
                    review_text[:500],  # Limit length for speed
                    self.failure_categories,
                    multi_label=True
                )

                # Return categories with confidence > 0.3
                return [
                    (label, score)
                    for label, score in zip(result['labels'], result['scores'])
                    if score > 0.3
                ]
            except Exception as e:
                print(f"    WARNING: NLP classification failed: {e}")
                # Fall through to keyword-based

        # Keyword-based classification (fallback)
        review_lower = review_text.lower()
        results = []

        keywords_map = {
            "broke or bent": ["broke", "broken", "bent", "snapped", "cracked", "shattered"],
            "difficult to install": ["hard to install", "difficult", "complicated", "confusing", "instructions", "impossible to"],
            "doesn't fit or wrong size": ["doesn't fit", "too small", "too large", "wrong size", "doesn't match"],
            "poor quality materials": ["cheap", "flimsy", "thin", "poor quality", "plastic", "feels cheap"],
            "not as described": ["not as described", "misleading", "false advertising", "different from picture"],
            "weight capacity failure": ["weight", "hold", "capacity", "heavy", "fell off", "couldn't support"],
            "screws or fasteners failed": ["screw", "bolt", "fastener", "stripped", "anchor", "mounting"],
            "too expensive for quality": ["overpriced", "not worth", "too expensive", "waste of money", "rip off"]
        }

        for category, keywords in keywords_map.items():
            matches = sum(1 for kw in keywords if kw in review_lower)
            if matches > 0:
                confidence = min(0.9, 0.3 + (matches * 0.2))
                results.append((category, confidence))

        return results

    def save_reviews(self, reviews):
        """Save reviews to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        saved = 0
        for review in reviews:
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO reviews
                    (asin, review_id, rating, title, body, date, verified_purchase, helpful_votes, scraped_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    review['asin'],
                    review['review_id'],
                    review['rating'],
                    review['title'],
                    review['body'],
                    review['date'],
                    review['verified_purchase'],
                    review['helpful_votes'],
                    datetime.now().isoformat()
                ))

                if cursor.rowcount > 0:
                    saved += 1

                    # Analyze failure modes
                    review_text = f"{review['title']} {review['body']}"
                    failure_modes = self.classify_failure_mode(review_text)

                    review_db_id = cursor.lastrowid
                    for category, confidence in failure_modes:
                        cursor.execute("""
                            INSERT INTO failure_modes (review_id, category, confidence)
                            VALUES (?, ?, ?)
                        """, (review_db_id, category, confidence))

            except Exception as e:
                print(f"  WARNING: Error saving review: {e}")
                continue

        conn.commit()
        conn.close()

        return saved

    def analyze_product(self, asin):
        """Generate summary analysis for a product."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get review stats
        cursor.execute("""
            SELECT COUNT(*), AVG(rating)
            FROM reviews
            WHERE asin = ?
        """, (asin,))

        total_reviews, avg_rating = cursor.fetchone()

        # Get failure mode distribution
        cursor.execute("""
            SELECT fm.category, COUNT(*) as count, AVG(fm.confidence) as avg_confidence
            FROM failure_modes fm
            JOIN reviews r ON fm.review_id = r.id
            WHERE r.asin = ?
            GROUP BY fm.category
            ORDER BY count DESC
        """, (asin,))

        failure_distribution = {}
        for category, count, avg_conf in cursor.fetchall():
            failure_distribution[category] = {
                'count': count,
                'percentage': (count / total_reviews * 100) if total_reviews > 0 else 0,
                'avg_confidence': avg_conf
            }

        # Save summary
        cursor.execute("""
            INSERT OR REPLACE INTO product_summaries
            (asin, total_reviews, avg_rating, common_failures, last_analyzed)
            VALUES (?, ?, ?, ?, ?)
        """, (
            asin,
            total_reviews,
            avg_rating,
            json.dumps(failure_distribution),
            datetime.now().isoformat()
        ))

        conn.commit()
        conn.close()

        return {
            'asin': asin,
            'total_reviews': total_reviews,
            'avg_rating': avg_rating,
            'failure_modes': failure_distribution
        }


def main():
    """Main entry point for testing."""
    import argparse

    parser = argparse.ArgumentParser(description='Analyze Amazon product reviews for failure modes')
    parser.add_argument('asins', nargs='+', help='Amazon ASINs to analyze')
    parser.add_argument('--max-reviews', type=int, default=100, help='Max reviews per product')
    parser.add_argument('--delay', type=float, default=2.0, help='Delay between requests (seconds)')
    parser.add_argument('--output', help='Output JSON file path')

    args = parser.parse_args()

    print("="*70)
    print("REVIEW FAILURE ANALYZER")
    print(f"Products to analyze: {len(args.asins)}")
    print(f"Max reviews per product: {args.max_reviews}")
    print("="*70)
    print()

    analyzer = ReviewFailureAnalyzer(delay=args.delay)

    results = []
    for i, asin in enumerate(args.asins, 1):
        print(f"\n[{i}/{len(args.asins)}] Analyzing ASIN: {asin}")
        print("-"*70)

        # Scrape reviews
        reviews = analyzer.scrape_negative_reviews(asin, max_reviews=args.max_reviews)
        print(f"\n  Total reviews scraped: {len(reviews)}")

        if not reviews:
            print("  WARNING: No reviews found, skipping")
            continue

        # Save to database
        saved = analyzer.save_reviews(reviews)
        print(f"  Saved {saved} new reviews to database")

        # Generate analysis
        print("\n  Analyzing failure modes...")
        analysis = analyzer.analyze_product(asin)
        results.append(analysis)

        # Print summary
        print(f"\n  SUMMARY:")
        print(f"    Total reviews analyzed: {analysis['total_reviews']}")
        print(f"    Average rating: {analysis['avg_rating']:.1f} stars")
        print(f"\n  TOP FAILURE MODES:")

        sorted_failures = sorted(
            analysis['failure_modes'].items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )

        for category, stats in sorted_failures[:5]:
            print(f"    • {category}: {stats['percentage']:.1f}% ({stats['count']} reviews)")

    # Save results to JSON
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"\n\nResults saved to: {output_path}")

    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
