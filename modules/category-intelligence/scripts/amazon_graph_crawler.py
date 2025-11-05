#!/usr/bin/env python3
"""
Amazon Product Graph Crawler
Maps "Customers who bought this also bought" relationships to discover adjacent categories.
Free method using public Amazon data and network analysis.
"""

import os
import sys
import json
import time
import sqlite3
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from dotenv import load_dotenv

# Load environment variables
project_root = Path(__file__).parent.parent.parent
load_dotenv(project_root / '.env')

# Add core to path
sys.path.insert(0, str(project_root / 'core'))

# Try to import required libraries
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: Missing required libraries. Install with:")
    print("  pip install requests beautifulsoup4")
    sys.exit(1)

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    print("WARNING: networkx not available. Install for graph visualization:")
    print("  pip install networkx matplotlib")
    NETWORKX_AVAILABLE = False


class AmazonGraphCrawler:
    """Crawls Amazon product relationships to discover adjacent categories."""

    def __init__(self, db_path=None, delay=2.0):
        """
        Initialize crawler.

        Args:
            db_path: Path to SQLite database (default: data/amazon_graph.db)
            delay: Delay between requests in seconds (default: 2.0)
        """
        self.delay = delay
        self.visited_asins = set()

        # Set up database
        if db_path is None:
            db_path = Path(__file__).parent / "data" / "amazon_graph.db"

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
                price REAL,
                category TEXT,
                avg_rating REAL,
                total_reviews INTEGER,
                discovered_at TEXT
            )
        """)

        # Edges table (product relationships)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_asin TEXT NOT NULL,
                target_asin TEXT NOT NULL,
                relationship_type TEXT,
                discovered_at TEXT,
                UNIQUE(source_asin, target_asin, relationship_type),
                FOREIGN KEY (source_asin) REFERENCES products(asin),
                FOREIGN KEY (target_asin) REFERENCES products(asin)
            )
        """)

        # Category analysis table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS category_overlap (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_category TEXT,
                target_category TEXT,
                overlap_count INTEGER,
                overlap_percentage REAL,
                calculated_at TEXT
            )
        """)

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_rel_source ON relationships(source_asin)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_rel_target ON relationships(target_asin)")

        conn.commit()
        conn.close()

    def scrape_product_details(self, asin):
        """
        Scrape basic product details and related products.

        Args:
            asin: Amazon product ASIN

        Returns:
            Dictionary with product data and related ASINs
        """
        url = f"https://www.amazon.com/dp/{asin}"

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            response = requests.get(url, headers=headers, timeout=30)

            if response.status_code != 200:
                print(f"    WARNING: Got status {response.status_code}")
                return None

            soup = BeautifulSoup(response.text, 'html.parser')

            data = {
                'asin': asin,
                'discovered_at': datetime.now().isoformat(),
                'related_products': {}
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
                try:
                    price_text = price_elem.get_text(strip=True)
                    data['price'] = float(price_text.replace('$', '').replace(',', ''))
                except:
                    data['price'] = None
            else:
                data['price'] = None

            # Category (breadcrumb)
            breadcrumb = soup.find('div', {'id': 'wayfinding-breadcrumbs_feature_div'})
            if breadcrumb:
                categories = [a.get_text(strip=True) for a in breadcrumb.find_all('a')]
                data['category'] = ' > '.join(categories) if categories else None
            else:
                data['category'] = None

            # Reviews
            reviews_elem = soup.find('span', {'id': 'acrCustomerReviewText'})
            if reviews_elem:
                try:
                    review_text = reviews_elem.get_text(strip=True)
                    data['total_reviews'] = int(review_text.split()[0].replace(',', ''))
                except:
                    data['total_reviews'] = 0
            else:
                data['total_reviews'] = 0

            # Rating
            rating_elem = soup.find('span', {'class': 'a-icon-alt'})
            if rating_elem:
                try:
                    rating_text = rating_elem.get_text(strip=True)
                    data['avg_rating'] = float(rating_text.split()[0])
                except:
                    data['avg_rating'] = None
            else:
                data['avg_rating'] = None

            # Scrape related products
            # 1. "Customers who bought this also bought"
            also_bought = self._extract_carousel_asins(soup, 'similarities_feature_div')
            if also_bought:
                data['related_products']['also_bought'] = also_bought

            # 2. "Frequently bought together"
            bought_together = self._extract_carousel_asins(soup, 'sims-fbt')
            if bought_together:
                data['related_products']['bought_together'] = bought_together

            # 3. "Customers also viewed"
            also_viewed = self._extract_carousel_asins(soup, 'sp_detail')
            if also_viewed:
                data['related_products']['also_viewed'] = also_viewed

            # 4. "Compare with similar items"
            similar_items = self._extract_comparison_asins(soup)
            if similar_items:
                data['related_products']['similar_items'] = similar_items

            return data

        except requests.exceptions.RequestException as e:
            print(f"    ERROR: Request failed: {e}")
            return None
        except Exception as e:
            print(f"    ERROR: Parsing failed: {e}")
            return None

    def _extract_carousel_asins(self, soup, container_id):
        """Extract ASINs from a carousel container."""
        asins = []

        container = soup.find('div', {'id': container_id})
        if not container:
            # Try class-based search
            container = soup.find('div', {'class': container_id})

        if container:
            # Look for links with /dp/ pattern
            for link in container.find_all('a', href=True):
                href = link['href']
                if '/dp/' in href:
                    try:
                        asin = href.split('/dp/')[1].split('/')[0].split('?')[0]
                        if len(asin) == 10 and asin not in asins:
                            asins.append(asin)
                    except:
                        continue

        return asins

    def _extract_comparison_asins(self, soup):
        """Extract ASINs from comparison table."""
        asins = []

        # Look for comparison table
        comparison = soup.find('div', {'id': 'HLCXComparisonWidget'})
        if not comparison:
            comparison = soup.find('table', {'id': 'HLCXComparisonTable'})

        if comparison:
            for link in comparison.find_all('a', href=True):
                href = link['href']
                if '/dp/' in href:
                    try:
                        asin = href.split('/dp/')[1].split('/')[0].split('?')[0]
                        if len(asin) == 10 and asin not in asins:
                            asins.append(asin)
                    except:
                        continue

        return asins

    def save_product_data(self, data):
        """Save product and relationships to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Save product
            cursor.execute("""
                INSERT OR REPLACE INTO products
                (asin, title, brand, price, category, avg_rating, total_reviews, discovered_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['asin'],
                data.get('title'),
                data.get('brand'),
                data.get('price'),
                data.get('category'),
                data.get('avg_rating'),
                data.get('total_reviews', 0),
                data['discovered_at']
            ))

            # Save relationships
            for rel_type, related_asins in data.get('related_products', {}).items():
                for target_asin in related_asins:
                    cursor.execute("""
                        INSERT OR IGNORE INTO relationships
                        (source_asin, target_asin, relationship_type, discovered_at)
                        VALUES (?, ?, ?, ?)
                    """, (
                        data['asin'],
                        target_asin,
                        rel_type,
                        data['discovered_at']
                    ))

            conn.commit()

        except Exception as e:
            print(f"    ERROR: Database save failed: {e}")
            conn.rollback()
        finally:
            conn.close()

    def crawl(self, seed_asin, max_depth=2, max_products=50):
        """
        Crawl Amazon product graph starting from seed ASIN.

        Args:
            seed_asin: Starting product ASIN
            max_depth: Maximum crawl depth (default: 2)
            max_products: Maximum total products to crawl (default: 50)

        Returns:
            Number of products discovered
        """
        print(f"\n  Starting crawl from ASIN: {seed_asin}")
        print(f"  Max depth: {max_depth}, Max products: {max_products}")
        print()

        queue = [(seed_asin, 0)]  # (asin, depth)
        products_crawled = 0

        while queue and products_crawled < max_products:
            current_asin, depth = queue.pop(0)

            # Skip if already visited
            if current_asin in self.visited_asins:
                continue

            # Skip if max depth reached
            if depth > max_depth:
                continue

            print(f"  [{products_crawled + 1}/{max_products}] Depth {depth}: {current_asin}")

            # Scrape product
            data = self.scrape_product_details(current_asin)

            if data:
                # Save to database
                self.save_product_data(data)

                # Print summary
                if data.get('title'):
                    print(f"    Title: {data['title'][:60]}...")
                if data.get('category'):
                    print(f"    Category: {data['category'][:60]}...")

                # Print related products found
                total_related = sum(len(asins) for asins in data.get('related_products', {}).values())
                print(f"    Related products found: {total_related}")

                # Add related products to queue
                for rel_type, related_asins in data.get('related_products', {}).items():
                    for related_asin in related_asins:
                        if related_asin not in self.visited_asins:
                            queue.append((related_asin, depth + 1))

                products_crawled += 1
            else:
                print(f"    Failed to scrape")

            # Mark as visited
            self.visited_asins.add(current_asin)

            # Add delay
            if queue:
                time.sleep(self.delay)

        print(f"\n  Crawl complete: {products_crawled} products discovered")
        return products_crawled

    def analyze_category_overlap(self):
        """
        Analyze which categories overlap with the seed category.

        Returns:
            Dictionary of category overlap statistics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get all products with categories
        cursor.execute("""
            SELECT asin, category
            FROM products
            WHERE category IS NOT NULL
        """)

        products = {asin: category for asin, category in cursor.fetchall()}

        # Count category transitions
        category_transitions = Counter()

        cursor.execute("""
            SELECT DISTINCT source_asin, target_asin
            FROM relationships
        """)

        for source_asin, target_asin in cursor.fetchall():
            source_cat = products.get(source_asin)
            target_cat = products.get(target_asin)

            if source_cat and target_cat:
                # Simplify category (take first 2 levels)
                source_simple = ' > '.join(source_cat.split(' > ')[:2])
                target_simple = ' > '.join(target_cat.split(' > ')[:2])

                if source_simple != target_simple:
                    key = (source_simple, target_simple)
                    category_transitions[key] += 1

        # Calculate percentages
        total_transitions = sum(category_transitions.values())
        overlap_stats = []

        for (source_cat, target_cat), count in category_transitions.most_common(20):
            percentage = (count / total_transitions * 100) if total_transitions > 0 else 0

            overlap_stats.append({
                'source_category': source_cat,
                'target_category': target_cat,
                'count': count,
                'percentage': round(percentage, 1)
            })

            # Save to database
            cursor.execute("""
                INSERT OR REPLACE INTO category_overlap
                (source_category, target_category, overlap_count, overlap_percentage, calculated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                source_cat,
                target_cat,
                count,
                percentage,
                datetime.now().isoformat()
            ))

        conn.commit()
        conn.close()

        return overlap_stats

    def generate_graph_visualization(self, output_path):
        """
        Generate network graph visualization (requires networkx and matplotlib).

        Args:
            output_path: Path to save graph image
        """
        if not NETWORKX_AVAILABLE:
            print("ERROR: networkx not available. Install with: pip install networkx matplotlib")
            return False

        try:
            import matplotlib.pyplot as plt

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create directed graph
            G = nx.DiGraph()

            # Add nodes (products)
            cursor.execute("SELECT asin, title, category FROM products")
            for asin, title, category in cursor.fetchall():
                # Simplify category for coloring
                cat_simple = category.split(' > ')[0] if category else 'Unknown'
                G.add_node(asin, title=title, category=cat_simple)

            # Add edges (relationships)
            cursor.execute("""
                SELECT source_asin, target_asin, relationship_type
                FROM relationships
            """)

            for source, target, rel_type in cursor.fetchall():
                if source in G and target in G:
                    G.add_edge(source, target, relationship=rel_type)

            conn.close()

            # Create visualization
            plt.figure(figsize=(20, 20))

            # Layout
            pos = nx.spring_layout(G, k=2, iterations=50)

            # Color nodes by category
            categories = list(set(nx.get_node_attributes(G, 'category').values()))
            color_map = {cat: i for i, cat in enumerate(categories)}
            node_colors = [color_map[G.nodes[node]['category']] for node in G.nodes()]

            # Draw
            nx.draw(
                G, pos,
                node_color=node_colors,
                node_size=500,
                with_labels=False,
                edge_color='gray',
                alpha=0.6,
                arrows=True,
                arrowsize=10
            )

            # Save
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()

            print(f"\n  Graph visualization saved to: {output_path}")
            return True

        except Exception as e:
            print(f"  ERROR: Visualization failed: {e}")
            return False


def main():
    """Main entry point for testing."""
    import argparse

    parser = argparse.ArgumentParser(description='Crawl Amazon product graph for adjacent categories')
    parser.add_argument('seed_asin', help='Starting product ASIN')
    parser.add_argument('--depth', type=int, default=2, help='Maximum crawl depth (default: 2)')
    parser.add_argument('--max-products', type=int, default=50, help='Max products to crawl (default: 50)')
    parser.add_argument('--delay', type=float, default=2.0, help='Delay between requests (seconds)')
    parser.add_argument('--output', help='Output JSON file path')
    parser.add_argument('--graph', help='Generate graph visualization (PNG file path)')

    args = parser.parse_args()

    print("="*70)
    print("AMAZON PRODUCT GRAPH CRAWLER")
    print("="*70)

    crawler = AmazonGraphCrawler(delay=args.delay)

    # Crawl
    products_found = crawler.crawl(
        args.seed_asin,
        max_depth=args.depth,
        max_products=args.max_products
    )

    # Analyze category overlap
    print("\n" + "="*70)
    print("CATEGORY OVERLAP ANALYSIS")
    print("="*70)

    overlap_stats = crawler.analyze_category_overlap()

    if overlap_stats:
        print("\nTop Adjacent Categories:")
        for i, stat in enumerate(overlap_stats[:10], 1):
            print(f"\n  {i}. {stat['source_category']}")
            print(f"     → {stat['target_category']}")
            print(f"     Overlap: {stat['count']} products ({stat['percentage']}%)")
    else:
        print("\nNo category overlap found (all products in same category)")

    # Save results
    if args.output:
        output_data = {
            'seed_asin': args.seed_asin,
            'products_crawled': products_found,
            'category_overlap': overlap_stats,
            'crawled_at': datetime.now().isoformat()
        }

        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)

        print(f"\n\nResults saved to: {output_path}")

    # Generate graph visualization
    if args.graph:
        print("\n" + "="*70)
        print("GENERATING GRAPH VISUALIZATION")
        print("="*70)

        graph_path = Path(args.graph)
        graph_path.parent.mkdir(parents=True, exist_ok=True)

        crawler.generate_graph_visualization(str(graph_path))

    print("\n" + "="*70)
    print("CRAWL COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
