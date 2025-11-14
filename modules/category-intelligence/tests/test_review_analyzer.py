#!/usr/bin/env python3
"""
TEST: Review Failure Analyzer
Tests on 2 garage organization products to validate the scraping and analysis pipeline.
"""

import sys
from pathlib import Path

# Test ASINs (from actual Amazon product data - high review count products)
TEST_ASINS = [
    "B0B96RNZ47",  # EXTRA GRIP Mop & Broom Holder (60K reviews, 4.5 stars)
    "B0B3HR2F7H"   # Adhesive Hooks Heavy Duty (47K reviews, 4.5 stars)
]

print("="*70)
print("REVIEW FAILURE ANALYZER - TEST MODE")
print(f"Testing with {len(TEST_ASINS)} products")
print("="*70)
print()

# Import the analyzer
from review_failure_analyzer import ReviewFailureAnalyzer

# Create analyzer with test database
test_db = Path(__file__).parent / "data" / "review_analysis_test.db"
analyzer = ReviewFailureAnalyzer(db_path=test_db, delay=3.0)

results = []
for i, asin in enumerate(TEST_ASINS, 1):
    print(f"\n[{i}/{len(TEST_ASINS)}] Testing ASIN: {asin}")
    print("-"*70)

    try:
        # Scrape only 20 reviews for testing
        reviews = analyzer.scrape_negative_reviews(asin, max_reviews=20, stars=[1, 2])
        print(f"\n  Reviews scraped: {len(reviews)}")

        if reviews:
            # Save to database
            saved = analyzer.save_reviews(reviews)
            print(f"  Saved: {saved} new reviews")

            # Analyze
            analysis = analyzer.analyze_product(asin)

            print(f"\n  ANALYSIS RESULTS:")
            print(f"    Total reviews: {analysis['total_reviews']}")
            print(f"    Avg rating: {analysis['avg_rating']:.1f} stars")

            if analysis['failure_modes']:
                print(f"\n  TOP FAILURE MODES:")
                sorted_failures = sorted(
                    analysis['failure_modes'].items(),
                    key=lambda x: x[1]['count'],
                    reverse=True
                )
                for category, stats in sorted_failures[:3]:
                    print(f"    • {category}: {stats['percentage']:.1f}%")

            results.append(analysis)
            print(f"\n  ✅ Test passed for {asin}")
        else:
            print(f"  ⚠️  No reviews found for {asin}")

    except Exception as e:
        print(f"  ❌ Test failed for {asin}")
        print(f"  Error: {str(e)}")
        import traceback
        traceback.print_exc()

print("\n" + "="*70)
if len(results) == len(TEST_ASINS):
    print("✅ ALL TESTS PASSED - Ready for full product list")
else:
    print(f"⚠️  PARTIAL SUCCESS - {len(results)}/{len(TEST_ASINS)} products analyzed")
print("="*70)
print(f"\nTest database: {test_db}")
print()
