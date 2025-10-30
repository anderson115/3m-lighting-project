#!/usr/bin/env python3
"""
Comprehensive statistical analysis of master product dataset
Identifies biases and strategic implications
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

# File paths
MASTER_FILE = Path("modules/category-intelligence/04_CATEGORY_DATA_ALL_PRODUCTS_WEIGHTED.xlsx")
OUTPUT_DIR = Path("modules/category-intelligence/analysis")
OUTPUT_DIR.mkdir(exist_ok=True)

print("="*80)
print("COMPREHENSIVE PRODUCT DATASET ANALYSIS")
print("="*80)

# Load data
print(f"\nLoading {MASTER_FILE}...")
df = pd.read_excel(MASTER_FILE)
print(f"✅ Loaded {len(df):,} products")
print(f"\nColumns: {list(df.columns)}")

# Basic statistics
print(f"\n{'='*80}")
print("DATASET OVERVIEW")
print("="*80)
print(f"Total Products: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# ============================================================================
# 1. RETAILER DISTRIBUTION
# ============================================================================
print(f"\n{'='*80}")
print("1. RETAILER DISTRIBUTION")
print("="*80)

retailer_counts = df['Retailer'].value_counts()
retailer_pct = df['Retailer'].value_counts(normalize=True) * 100

retailer_stats = pd.DataFrame({
    'Count': retailer_counts,
    'Percentage': retailer_pct
})
print(retailer_stats.to_string())

# Calculate bias factors (vs estimated market share)
market_share_estimates = {
    'Walmart': 15,
    'Homedepot': 35,
    'Lowes': 30,
    'Amazon': 15,
    'Target': 5,
    'Menards': 10,
    'Acehardware': 5
}

print("\nRETAILER BIAS ANALYSIS:")
print(f"{'Retailer':<15} {'Dataset %':>10} {'Est Market %':>12} {'Bias Factor':>12}")
print("-" * 52)
for retailer in retailer_stats.index:
    dataset_pct = retailer_stats.loc[retailer, 'Percentage']
    market_pct = market_share_estimates.get(retailer, 0)
    bias_factor = dataset_pct / market_pct if market_pct > 0 else 0
    print(f"{retailer:<15} {dataset_pct:>9.1f}% {market_pct:>11.0f}% {bias_factor:>11.1f}x")

# ============================================================================
# 2. PRICE DISTRIBUTION
# ============================================================================
print(f"\n{'='*80}")
print("2. PRICE DISTRIBUTION")
print("="*80)

# Clean price data
df['Price_Clean'] = pd.to_numeric(df['Price'], errors='coerce')
df_with_price = df[df['Price_Clean'].notna()]

print(f"\nProducts with price data: {len(df_with_price):,} ({len(df_with_price)/len(df)*100:.1f}%)")
print(f"Products missing price: {len(df) - len(df_with_price):,}")

# Price statistics
print(f"\nPRICE STATISTICS:")
print(f"  Mean:    ${df_with_price['Price_Clean'].mean():.2f}")
print(f"  Median:  ${df_with_price['Price_Clean'].median():.2f}")
print(f"  Std Dev: ${df_with_price['Price_Clean'].std():.2f}")
print(f"  Min:     ${df_with_price['Price_Clean'].min():.2f}")
print(f"  Max:     ${df_with_price['Price_Clean'].max():.2f}")

# Price percentiles
percentiles = [10, 25, 50, 75, 90, 95, 99]
print(f"\nPRICE PERCENTILES:")
for p in percentiles:
    value = df_with_price['Price_Clean'].quantile(p/100)
    print(f"  {p:2d}th: ${value:>8.2f}")

# Price buckets
price_buckets = [0, 20, 50, 100, 200, 500, float('inf')]
bucket_labels = ['$0-20', '$20-50', '$50-100', '$100-200', '$200-500', '$500+']
df_with_price['Price_Bucket'] = pd.cut(df_with_price['Price_Clean'],
                                         bins=price_buckets,
                                         labels=bucket_labels)

print(f"\nPRICE DISTRIBUTION BY BUCKET:")
price_dist = df_with_price['Price_Bucket'].value_counts().sort_index()
for bucket, count in price_dist.items():
    pct = count / len(df_with_price) * 100
    print(f"  {bucket:<12} {count:>5,} ({pct:>5.1f}%)")

# Premium segment definition
df_with_price['Is_Premium'] = df_with_price['Price_Clean'] >= 50
premium_count = df_with_price['Is_Premium'].sum()
premium_pct = premium_count / len(df_with_price) * 100
print(f"\nPREMIUM SEGMENT ($50+): {premium_count:,} products ({premium_pct:.1f}%)")

# ============================================================================
# 3. PRICE BY RETAILER
# ============================================================================
print(f"\n{'='*80}")
print("3. PRICE BY RETAILER")
print("="*80)

print(f"{'Retailer':<15} {'Count':>7} {'Avg Price':>10} {'Median':>10} {'% Premium':>10}")
print("-" * 55)
for retailer in retailer_counts.index:
    retailer_df = df_with_price[df_with_price['Retailer'] == retailer]
    if len(retailer_df) > 0:
        avg_price = retailer_df['Price_Clean'].mean()
        median_price = retailer_df['Price_Clean'].median()
        premium_pct = (retailer_df['Price_Clean'] >= 50).sum() / len(retailer_df) * 100
        print(f"{retailer:<15} {len(retailer_df):>7,} ${avg_price:>9.2f} ${median_price:>9.2f} {premium_pct:>9.1f}%")

# ============================================================================
# 4. CATEGORY DISTRIBUTION
# ============================================================================
print(f"\n{'='*80}")
print("4. CATEGORY DISTRIBUTION")
print("="*80)

if 'Category' in df.columns:
    category_counts = df['Category'].value_counts()
    print(f"\nProducts with category data: {df['Category'].notna().sum():,}")
    print(f"Products missing category: {df['Category'].isna().sum():,}")

    print(f"\nTOP 20 CATEGORIES:")
    for i, (cat, count) in enumerate(category_counts.head(20).items(), 1):
        pct = count / len(df) * 100
        print(f"  {i:2d}. {str(cat)[:50]:<50} {count:>5,} ({pct:>5.1f}%)")
else:
    print("⚠️  No 'Category' column found")

# ============================================================================
# 5. SUBCATEGORY DISTRIBUTION
# ============================================================================
print(f"\n{'='*80}")
print("5. SUBCATEGORY DISTRIBUTION")
print("="*80)

if 'Subcategory' in df.columns:
    subcat_counts = df['Subcategory'].value_counts()
    print(f"\nProducts with subcategory data: {df['Subcategory'].notna().sum():,}")
    print(f"Products missing subcategory: {df['Subcategory'].isna().sum():,}")

    print(f"\nTOP 20 SUBCATEGORIES:")
    for i, (subcat, count) in enumerate(subcat_counts.head(20).items(), 1):
        pct = count / len(df) * 100
        print(f"  {i:2d}. {str(subcat)[:50]:<50} {count:>5,} ({pct:>5.1f}%)")
else:
    print("⚠️  No 'Subcategory' column found")

# ============================================================================
# 6. BRAND DISTRIBUTION
# ============================================================================
print(f"\n{'='*80}")
print("6. BRAND DISTRIBUTION")
print("="*80)

if 'Brand' in df.columns:
    brand_counts = df['Brand'].value_counts()
    print(f"\nProducts with brand data: {df['Brand'].notna().sum():,}")
    print(f"Products missing brand: {df['Brand'].isna().sum():,}")
    print(f"Unique brands: {df['Brand'].nunique():,}")

    print(f"\nTOP 30 BRANDS:")
    for i, (brand, count) in enumerate(brand_counts.head(30).items(), 1):
        pct = count / len(df) * 100
        # Calculate average price for brand
        brand_df = df_with_price[df_with_price['Brand'] == brand]
        avg_price = brand_df['Price_Clean'].mean() if len(brand_df) > 0 else 0
        print(f"  {i:2d}. {str(brand)[:30]:<30} {count:>5,} ({pct:>4.1f}%) ${avg_price:>7.2f} avg")
else:
    print("⚠️  No 'Brand' column found")

# ============================================================================
# 7. RATING & REVIEW DISTRIBUTION
# ============================================================================
print(f"\n{'='*80}")
print("7. RATING & REVIEW DISTRIBUTION")
print("="*80)

if 'Star Rating' in df.columns:
    df['Rating_Clean'] = pd.to_numeric(df['Star Rating'], errors='coerce')
    df_with_rating = df[df['Rating_Clean'].notna()]

    print(f"\nProducts with rating data: {len(df_with_rating):,} ({len(df_with_rating)/len(df)*100:.1f}%)")
    print(f"Products missing rating: {len(df) - len(df_with_rating):,}")

    if len(df_with_rating) > 0:
        print(f"\nRATING STATISTICS:")
        print(f"  Mean:   {df_with_rating['Rating_Clean'].mean():.2f}")
        print(f"  Median: {df_with_rating['Rating_Clean'].median():.2f}")
        print(f"  Std Dev: {df_with_rating['Rating_Clean'].std():.2f}")

        # Quality failure analysis (< 4.0 stars)
        poor_quality = df_with_rating[df_with_rating['Rating_Clean'] < 4.0]
        print(f"\nQUALITY ANALYSIS:")
        print(f"  Products < 4.0 stars: {len(poor_quality):,} ({len(poor_quality)/len(df_with_rating)*100:.1f}%)")
        print(f"  Products >= 4.0 stars: {len(df_with_rating) - len(poor_quality):,}")

if 'Review Count' in df.columns:
    df['Reviews_Clean'] = pd.to_numeric(df['Review Count'], errors='coerce')
    df_with_reviews = df[df['Reviews_Clean'].notna()]

    if len(df_with_reviews) > 0:
        print(f"\nREVIEW COUNT STATISTICS:")
        print(f"  Total reviews across all products: {df_with_reviews['Reviews_Clean'].sum():,.0f}")
        print(f"  Mean reviews per product: {df_with_reviews['Reviews_Clean'].mean():.1f}")
        print(f"  Median reviews per product: {df_with_reviews['Reviews_Clean'].median():.0f}")

# ============================================================================
# 8. SPECIAL FEATURES DISTRIBUTION
# ============================================================================
print(f"\n{'='*80}")
print("8. SPECIAL FEATURES DISTRIBUTION")
print("="*80)

# Rail/Slatwall systems
if 'Rail/Slatwall System' in df.columns:
    rail_counts = df['Rail/Slatwall System'].value_counts()
    print(f"\nRAIL/SLATWALL SYSTEMS:")
    for feature, count in rail_counts.items():
        pct = count / len(df) * 100
        print(f"  {feature}: {count:,} ({pct:.1f}%)")

# Hook/Hanger products
if 'Hook/Hanger Product' in df.columns:
    hook_counts = df['Hook/Hanger Product'].value_counts()
    print(f"\nHOOK/HANGER PRODUCTS:")
    for feature, count in hook_counts.items():
        pct = count / len(df) * 100
        print(f"  {feature}: {count:,} ({pct:.1f}%)")

# ============================================================================
# 9. DATA COMPLETENESS ANALYSIS
# ============================================================================
print(f"\n{'='*80}")
print("9. DATA COMPLETENESS ANALYSIS")
print("="*80)

completeness = {}
for col in df.columns:
    non_null = df[col].notna().sum()
    pct = non_null / len(df) * 100
    completeness[col] = {'count': non_null, 'pct': pct}

print(f"\n{'Column':<30} {'Non-Null':>10} {'Complete %':>12}")
print("-" * 55)
for col, stats in sorted(completeness.items(), key=lambda x: x[1]['pct'], reverse=True):
    print(f"{col[:30]:<30} {stats['count']:>10,} {stats['pct']:>11.1f}%")

# ============================================================================
# 10. BIAS IDENTIFICATION & STRATEGIC IMPLICATIONS
# ============================================================================
print(f"\n{'='*80}")
print("10. BIAS IDENTIFICATION & STRATEGIC IMPLICATIONS")
print("="*80)

biases = []

# Retailer bias
walmart_pct = retailer_stats.loc['Walmart', 'Percentage']
if walmart_pct > 60:
    biases.append({
        'type': 'Retailer Over-Sampling',
        'issue': f'Walmart represents {walmart_pct:.1f}% of dataset (should be ~15%)',
        'impact': 'Dataset skewed toward budget products and hooks/hangers',
        'recommendation': 'Apply market weights or collect more HD/Lowe\'s data'
    })

# Premium coverage bias
if 'Price_Clean' in df.columns:
    raw_premium_pct = (df_with_price['Price_Clean'] >= 50).sum() / len(df_with_price) * 100
    if raw_premium_pct < 30:
        biases.append({
            'type': 'Premium Segment Under-Representation',
            'issue': f'Only {raw_premium_pct:.1f}% of products are $50+ (market likely 40-50%)',
            'impact': 'May underestimate premium opportunity and pricing power',
            'recommendation': 'Supplement with HD/Lowe\'s premium products'
        })

# Category bias
if 'Category' in df.columns and df['Category'].notna().sum() > 0:
    top_cat_pct = (df['Category'].value_counts().iloc[0] / len(df) * 100) if len(df['Category'].value_counts()) > 0 else 0
    if top_cat_pct > 50:
        biases.append({
            'type': 'Category Concentration',
            'issue': f'One category represents {top_cat_pct:.1f}% of products',
            'impact': 'May miss emerging categories and growth opportunities',
            'recommendation': 'Expand category coverage with targeted searches'
        })

# Rating coverage bias
if 'Star Rating' in df.columns:
    rating_coverage = (df['Rating_Clean'].notna().sum() / len(df) * 100)
    if rating_coverage < 30:
        biases.append({
            'type': 'Quality Data Sparsity',
            'issue': f'Only {rating_coverage:.1f}% of products have ratings',
            'impact': 'Quality failure claims lack statistical support',
            'recommendation': 'Scrape reviews/ratings for key product segments'
        })

# Menards still under-represented
menards_count = retailer_counts.get('Menards', 0)
if menards_count < 500:
    biases.append({
        'type': 'Regional Retailer Gap',
        'issue': f'Menards has only {menards_count} products (should be 1,000+)',
        'impact': 'Missing Midwest market dynamics and pricing',
        'recommendation': 'Comprehensive Menards category scrape'
    })

print(f"\nIDENTIFIED BIASES: {len(biases)}")
for i, bias in enumerate(biases, 1):
    print(f"\n{i}. {bias['type'].upper()}")
    print(f"   Issue: {bias['issue']}")
    print(f"   Impact: {bias['impact']}")
    print(f"   Recommendation: {bias['recommendation']}")

# ============================================================================
# SAVE RESULTS
# ============================================================================
print(f"\n{'='*80}")
print("SAVING RESULTS")
print("="*80)

# Save summary statistics to JSON (convert numpy types to native Python)
def convert_to_native(obj):
    """Convert numpy types to native Python types"""
    if isinstance(obj, (np.integer, np.int8, np.int16, np.int32, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float16, np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, (np.ndarray,)):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_to_native(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_native(item) for item in obj]
    elif hasattr(obj, 'item'):  # Catch any numpy scalar
        return obj.item()
    return obj

summary = {
    'dataset_overview': {
        'total_products': int(len(df)),
        'columns': int(len(df.columns)),
        'date_analyzed': pd.Timestamp.now().isoformat()
    },
    'retailer_distribution': convert_to_native(retailer_stats.to_dict()),
    'price_statistics': {
        'mean': float(df_with_price['Price_Clean'].mean()),
        'median': float(df_with_price['Price_Clean'].median()),
        'std': float(df_with_price['Price_Clean'].std()),
        'premium_pct': float(premium_pct)
    },
    'data_completeness': convert_to_native(completeness),
    'identified_biases': biases
}

output_json = OUTPUT_DIR / 'product_statistics_summary.json'
with open(output_json, 'w') as f:
    json.dump(summary, f, indent=2)
print(f"✅ Saved summary to {output_json}")

# Save detailed stats to Excel
with pd.ExcelWriter(OUTPUT_DIR / 'product_statistics_detailed.xlsx') as writer:
    retailer_stats.to_excel(writer, sheet_name='Retailer Distribution')
    if len(df_with_price) > 0:
        price_dist.to_frame('Count').to_excel(writer, sheet_name='Price Distribution')
    if 'Brand' in df.columns:
        brand_counts.head(50).to_frame('Count').to_excel(writer, sheet_name='Top Brands')
    if 'Category' in df.columns and df['Category'].notna().sum() > 0:
        category_counts.head(50).to_frame('Count').to_excel(writer, sheet_name='Top Categories')

print(f"✅ Saved detailed stats to {OUTPUT_DIR / 'product_statistics_detailed.xlsx'}")

print(f"\n{'='*80}")
print("ANALYSIS COMPLETE")
print("="*80)
