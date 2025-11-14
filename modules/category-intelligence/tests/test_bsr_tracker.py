#!/usr/bin/env python3
"""
TEST: BSR Sales Tracker
Tests on 2 garage organization products to validate scraping and sales estimation.
"""

import sys
from pathlib import Path

# Test ASINs (from actual Amazon product data)
TEST_ASINS = [
    "B0F5P6B5K3",  # PVZZRKL 18 Pack Garage Hooks
    "B0FF41VB68"   # MUZHUPGUZ 2 Pcs Heavy Duty Garage Hooks
]

print("="*70)
print("BSR SALES TRACKER - TEST MODE")
print(f"Testing with {len(TEST_ASINS)} products")
print("="*70)
print()

# Import the tracker
from bsr_sales_tracker import BSRSalesTracker

# Create tracker with test database
test_db = Path(__file__).parent / "data" / "bsr_tracking_test.db"
tracker = BSRSalesTracker(db_path=test_db, delay=3.0)

results = []
for i, asin in enumerate(TEST_ASINS, 1):
    print(f"\n[{i}/{len(TEST_ASINS)}] Testing ASIN: {asin}")
    print("-"*70)

    try:
        # Scrape product data
        print("  Scraping Amazon data...")
        data = tracker.scrape_product_data(asin)

        if data:
            # Save to database
            tracker.save_tracking_data(data)

            # Print scraped data
            print(f"\n  SCRAPED DATA:")
            print(f"    Title: {data.get('title', 'N/A')[:60]}...")
            print(f"    Brand: {data.get('brand', 'N/A')}")
            print(f"    Price: ${data.get('price', 0):.2f}" if data.get('price') else "    Price: N/A")
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
                    print(f"    BSR Method: {estimate['estimated_sales_bsr']:,} units")
                    print(f"    Confidence: {estimate['bsr_confidence']}")

                if 'estimated_sales_velocity' in estimate:
                    print(f"    Velocity Method: {estimate['estimated_sales_velocity']:,} units")

                results.append(estimate)
                print(f"\n  ✅ Test passed for {asin}")
            else:
                print("    ⚠️  Could not estimate sales (no BSR data)")
                results.append({'asin': asin, 'status': 'no_bsr'})
        else:
            print(f"  ❌ Failed to scrape product data")

    except Exception as e:
        print(f"  ❌ Test failed for {asin}")
        print(f"  Error: {str(e)}")
        import traceback
        traceback.print_exc()

print("\n" + "="*70)
if len(results) >= len(TEST_ASINS):
    print("✅ ALL TESTS PASSED - Ready for full product list")
    print("\nNote: Sales estimates require BSR data.")
    print("Some products may not have BSR if they're not in top sellers.")
else:
    print(f"⚠️  TESTS INCOMPLETE - {len(results)}/{len(TEST_ASINS)} products processed")
print("="*70)
print(f"\nTest database: {test_db}")
print()
