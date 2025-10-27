#!/usr/bin/env python3
"""Extract next batch of ASINs for BSR tracking"""
import json
import sqlite3
from pathlib import Path

# Load full product dataset
data_file = Path("data/amazon_garage_organizers_mined.json")
products = json.loads(data_file.read_text())

print(f"Total products in dataset: {len(products)}")

# Get already tracked ASINs from database
db_path = Path("data/bsr_tracking.db")
tracked_asins = set()

if db_path.exists():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT asin FROM products")
    tracked_asins = {row[0] for row in cursor.fetchall()}
    conn.close()

print(f"Already tracked: {len(tracked_asins)}")

# Filter to products with meaningful review counts (proxy for sales)
# High review count = likely high sales volume
untracked = [p for p in products if p.get('sku') not in tracked_asins]

# Sort by review count (proxy for volume) and rating (quality)
# Focus on products with >50 reviews (more reliable data)
high_potential = sorted(
    [p for p in untracked if p.get('reviews', 0) >= 50],
    key=lambda x: (x.get('reviews', 0) * x.get('rating', 0)),
    reverse=True
)

print(f"\nHigh-potential untracked products (50+ reviews): {len(high_potential)}")

# Take next 300 products
next_batch = high_potential[:300]

print(f"Selected for next batch: {len(next_batch)}")

# Calculate estimated coverage
if next_batch:
    total_reviews_tracked = sum(p.get('reviews', 0) for p in products if p.get('sku') in tracked_asins)
    total_reviews_next = sum(p.get('reviews', 0) for p in next_batch)
    total_reviews_all = sum(p.get('reviews', 0) for p in products)

    current_coverage = (total_reviews_tracked / total_reviews_all) * 100 if total_reviews_all else 0
    new_coverage = ((total_reviews_tracked + total_reviews_next) / total_reviews_all) * 100 if total_reviews_all else 0

    print(f"\nCOVERAGE ESTIMATE (by review volume as proxy):")
    print(f"  Current: {current_coverage:.1f}%")
    print(f"  After next batch: {new_coverage:.1f}%")

# Save ASINs to file
output_path = Path("asins_next300.txt")
output_path.write_text('\n'.join(p.get('sku', '') for p in next_batch if p.get('sku')))

print(f"\nSaved to: {output_path}")
print(f"\nTop 10 from next batch:")
for i, p in enumerate(next_batch[:10], 1):
    print(f"  {i}. {p.get('title', 'N/A')[:60]}... ({p.get('reviews', 0):,} reviews, {p.get('rating', 0):.1f}★)")
