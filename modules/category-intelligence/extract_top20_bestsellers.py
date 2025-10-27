#!/usr/bin/env python3
"""Extract top 20 bestselling products for teardown analysis"""
import json
import sqlite3
from pathlib import Path

# Get products from BSR database
db_path = Path("data/bsr_tracking.db")

if db_path.exists():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get top 20 by BSR
    cursor.execute("""
        SELECT DISTINCT
            p.asin,
            p.title,
            p.brand,
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
        AND b.bsr IS NOT NULL
        ORDER BY b.bsr ASC
        LIMIT 20
    """)

    products = []
    for row in cursor.fetchall():
        asin, title, brand, price, bsr, reviews, rating = row

        # Estimate monthly sales using Jungle Scout formula
        if bsr < 100:
            estimated_sales = 3500 - (bsr * 25)
        elif bsr < 1000:
            estimated_sales = 2500 - (bsr * 2)
        elif bsr < 10000:
            estimated_sales = 1500 - (bsr * 0.15)
        else:
            estimated_sales = max(50, 100 - (bsr * 0.001))

        products.append({
            'rank': len(products) + 1,
            'asin': asin,
            'title': title,
            'brand': brand,
            'price': price,
            'bsr': bsr,
            'estimated_monthly_sales': int(estimated_sales),
            'total_reviews': reviews or 0,
            'avg_rating': rating or 0,
            'amazon_url': f'https://www.amazon.com/dp/{asin}'
        })

    conn.close()

    # Save to JSON
    output_path = Path("outputs/top20_bestsellers_for_teardown.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(products, f, indent=2)

    print("="*70)
    print("TOP 20 BESTSELLERS - TEARDOWN TARGET LIST")
    print("="*70)
    print()

    for p in products:
        print(f"{p['rank']:2}. {p['title'][:60]}...")
        print(f"    Brand: {p['brand']} | ASIN: {p['asin']}")
        print(f"    BSR: {p['bsr']:,} | Est. Sales: {p['estimated_monthly_sales']:,}/mo | Price: ${p['price']:.2f}")
        print(f"    Reviews: {p['total_reviews']:,} | Rating: {p['avg_rating']:.1f}★")
        print()

    print("="*70)
    print(f"Saved to: {output_path}")
    print("="*70)

else:
    print("ERROR: BSR database not found")
