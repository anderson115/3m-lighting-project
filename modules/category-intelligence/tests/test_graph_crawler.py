#!/usr/bin/env python3
"""
TEST: Amazon Product Graph Crawler
Tests on 1 seed product with shallow depth to validate crawling and analysis.
"""

import sys
from pathlib import Path

# Test ASIN (from actual Amazon product data)
SEED_ASIN = "B0F5P6B5K3"  # PVZZRKL 18 Pack Garage Hooks

print("="*70)
print("AMAZON PRODUCT GRAPH CRAWLER - TEST MODE")
print(f"Testing with seed ASIN: {SEED_ASIN}")
print("Settings: depth=1, max_products=10")
print("="*70)
print()

# Import the crawler
from amazon_graph_crawler import AmazonGraphCrawler

# Create crawler with test database
test_db = Path(__file__).parent / "data" / "amazon_graph_test.db"
crawler = AmazonGraphCrawler(db_path=test_db, delay=3.0)

try:
    # Crawl with shallow depth for testing
    print("Starting crawl...")
    products_found = crawler.crawl(
        seed_asin=SEED_ASIN,
        max_depth=1,  # Only go 1 level deep
        max_products=10  # Limit to 10 products
    )

    print(f"\n{'='*70}")
    print("ANALYZING RESULTS")
    print("="*70)

    if products_found > 0:
        # Analyze category overlap
        print("\nAnalyzing category overlap...")
        overlap_stats = crawler.analyze_category_overlap()

        if overlap_stats:
            print("\nAdjacent Categories Found:")
            for i, stat in enumerate(overlap_stats[:5], 1):
                print(f"\n  {i}. {stat['source_category']}")
                print(f"     → {stat['target_category']}")
                print(f"     Overlap: {stat['count']} products ({stat['percentage']}%)")

            print(f"\n  ✅ Test passed - Found {len(overlap_stats)} category connections")
        else:
            print("\n  ⚠️  No adjacent categories found (all products in same category)")
            print("     This is OK for test - it means related products are similar")

        print(f"\n{'='*70}")
        print("✅ ALL TESTS PASSED - Ready for full crawl")
        print("="*70)
        print(f"\nTest database: {test_db}")
        print(f"Products crawled: {products_found}")
        print(f"\nTo run full crawl, use:")
        print(f"  python amazon_graph_crawler.py {SEED_ASIN} --depth 2 --max-products 50")
        print()

    else:
        print("\n❌ TEST FAILED - No products found")
        print("This could be due to:")
        print("  1. Network/connectivity issues")
        print("  2. Amazon blocking requests (try increasing --delay)")
        print("  3. Invalid ASIN")

except Exception as e:
    print(f"\n❌ TEST FAILED")
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()
    print("\nThis could be due to:")
    print("  1. Network/connectivity issues")
    print("  2. Amazon anti-scraping measures (try increasing delay)")
    print("  3. HTML structure changes on Amazon")
