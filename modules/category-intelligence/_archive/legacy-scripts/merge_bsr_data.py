#!/usr/bin/env python3
"""Merge BSR estimates and analyze coverage"""
import json
from pathlib import Path
from collections import defaultdict

# Load both files (they're incomplete due to crash, but have data)
output_dir = Path("outputs")

estimates = []

# Try to load from database instead
import sqlite3
db_path = Path("data/bsr_tracking.db")

if db_path.exists():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all unique products with their latest estimates
    cursor.execute("""
        SELECT DISTINCT
            p.asin,
            p.title,
            p.brand,
            p.category,
            p.current_price,
            b.bsr,
            r.total_reviews,
            r.avg_rating
        FROM products p
        LEFT JOIN bsr_history b ON p.asin = b.asin
        LEFT JOIN review_history r ON p.asin = r.asin
        WHERE b.id = (
            SELECT MAX(id) FROM bsr_history WHERE asin = p.asin
        )
        ORDER BY b.bsr ASC NULLS LAST
    """)

    products = []
    for row in cursor.fetchall():
        asin, title, brand, category, price, bsr, reviews, rating = row
        products.append({
            'asin': asin,
            'title': title,
            'brand': brand,
            'category': category,
            'price': price,
            'bsr': bsr,
            'total_reviews': reviews,
            'avg_rating': rating
        })

    conn.close()

    print(f"Loaded {len(products)} products from database")

    # Analyze BSR distribution
    bsr_tiers = {
        'Top 100': [p for p in products if p['bsr'] and p['bsr'] < 100],
        'Top 1000': [p for p in products if p['bsr'] and 100 <= p['bsr'] < 1000],
        'Top 10K': [p for p in products if p['bsr'] and 1000 <= p['bsr'] < 10000],
        'Top 100K': [p for p in products if p['bsr'] and 10000 <= p['bsr'] < 100000],
        'Below 100K': [p for p in products if p['bsr'] and p['bsr'] >= 100000]
    }

    print("\n" + "="*70)
    print("BSR COVERAGE ANALYSIS")
    print("="*70)

    for tier, prods in bsr_tiers.items():
        if prods:
            avg_bsr = sum(p['bsr'] for p in prods) / len(prods)
            min_bsr = min(p['bsr'] for p in prods)
            max_bsr = max(p['bsr'] for p in prods)
            print(f"\n{tier}: {len(prods)} products")
            print(f"  BSR range: {min_bsr:,} - {max_bsr:,}")
            print(f"  Avg BSR: {avg_bsr:,.0f}")

            # Sample top products
            if len(prods) <= 5:
                for p in prods:
                    print(f"    • {p['title'][:50]}... (BSR: {p['bsr']:,}, ${p['price']:.2f})")

    # Estimate sales using Jungle Scout formula
    def estimate_sales(bsr):
        if bsr < 100:
            return 3500 - (bsr * 25)
        elif bsr < 1000:
            return 2500 - (bsr * 2)
        elif bsr < 10000:
            return 1500 - (bsr * 0.15)
        else:
            return max(50, 100 - (bsr * 0.001))

    # Calculate total estimated market
    total_monthly_sales = 0
    for p in products:
        if p['bsr']:
            sales = estimate_sales(p['bsr'])
            total_monthly_sales += sales
            p['estimated_monthly_sales'] = sales

    print(f"\n{'='*70}")
    print(f"TOTAL ESTIMATED MONTHLY MARKET")
    print(f"{'='*70}")
    print(f"Products tracked: {len([p for p in products if p['bsr']])}")
    print(f"Estimated monthly units: {total_monthly_sales:,.0f}")
    print(f"Avg price: ${sum(p['price'] for p in products if p['price'])/len([p for p in products if p['price']]):.2f}")
    print(f"Estimated monthly revenue: ${total_monthly_sales * 18:.2f}")

    # Top sellers
    print(f"\n{'='*70}")
    print(f"TOP 10 SELLERS BY ESTIMATED VOLUME")
    print(f"{'='*70}")
    top_sellers = sorted([p for p in products if p.get('estimated_monthly_sales')],
                        key=lambda x: x['estimated_monthly_sales'], reverse=True)[:10]

    for i, p in enumerate(top_sellers, 1):
        print(f"\n{i}. {p['title'][:60]}...")
        print(f"   BSR: {p['bsr']:,} | Est. Sales: {p['estimated_monthly_sales']:,.0f}/mo | Price: ${p['price']:.2f}")
        print(f"   Brand: {p['brand']} | Reviews: {p['total_reviews']:,}")

    # Save complete dataset
    output_path = output_dir / "bsr_complete_analysis.json"
    with open(output_path, 'w') as f:
        json.dump(products, f, indent=2)

    print(f"\n\nComplete analysis saved to: {output_path}")

else:
    print("ERROR: Database not found")
