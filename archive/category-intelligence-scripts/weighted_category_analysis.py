#!/usr/bin/env python3
"""Weighted category analysis with bias correction"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

# Load data (with fixed categories)
data_file = "/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/category-intelligence/04_CATEGORY_DATA_RIGHTSIZED_WITH_SUBCATS_FIXED.xlsx"
df = pd.read_excel(data_file)

print("="*80)
print("WEIGHTED CATEGORY ANALYSIS - BIAS CORRECTED")
print("="*80)
print(f"\nTotal Products: {len(df):,}")

# ==============================================================================
# CALCULATE WEIGHTS
# ==============================================================================

# Retailer weights (to achieve equal 14.3% representation)
retailer_weights = {
    'Walmart': 0.38,
    'Homedepot': 0.85,
    'Amazon': 1.40,
    'Target': 1.67,
    'Lowes': 1.92,
    'Menards': 2.90,
    'Acehardware': 7.50
}

# Category weights (reduce Hooks & Hangers from 58% to 40%)
category_weights = {
    'Hooks & Hangers': 0.69
}

def calculate_weight(row):
    """Calculate combined weight for retailer and category bias correction"""
    retailer_weight = retailer_weights.get(row['Retailer'], 1.0)
    category_weight = category_weights.get(row['Category'], 1.0)
    return retailer_weight * category_weight

df['weight'] = df.apply(calculate_weight, axis=1)

print(f"\n✓ Applied bias correction weights")
print(f"  - Retailer weights: {len(retailer_weights)} retailers")
print(f"  - Category weights: Hooks & Hangers = 0.69x")

# ==============================================================================
# WEIGHTED CATEGORY ANALYSIS
# ==============================================================================

# Use 'Category' column for main categories
categories = df['Category'].dropna().unique()

results = []

for category in sorted(categories):
    cat_df = df[df['Category'] == category].copy()

    # Raw counts
    raw_count = len(cat_df)

    # Weighted count
    weighted_count = cat_df['weight'].sum()

    # Price statistics (weighted)
    prices = cat_df[cat_df['Price'].notna()].copy()
    if len(prices) > 0:
        weighted_avg_price = (prices['Price'] * prices['weight']).sum() / prices['weight'].sum()
        price_min = prices['Price'].min()
        price_max = prices['Price'].max()
        price_median = prices['Price'].median()
    else:
        weighted_avg_price = 0
        price_min = 0
        price_max = 0
        price_median = 0

    # Retailer diversity
    retailer_count = cat_df['Retailer'].nunique()

    # Brand diversity
    brand_count = cat_df['Brand'].nunique()

    # Top brands
    top_brands = cat_df['Brand'].value_counts().head(3).index.tolist()

    # Customer satisfaction (Star Rating)
    ratings = cat_df[cat_df['Star Rating'].notna()].copy()
    if len(ratings) > 0:
        weighted_avg_rating = (ratings['Star Rating'] * ratings['weight']).sum() / ratings['weight'].sum()
        rating_count = len(ratings)
    else:
        weighted_avg_rating = 0
        rating_count = 0

    # Review count
    reviews = cat_df[cat_df['Review Count'].notna()].copy()
    if len(reviews) > 0:
        weighted_avg_reviews = (reviews['Review Count'] * reviews['weight']).sum() / reviews['weight'].sum()
    else:
        weighted_avg_reviews = 0

    results.append({
        'category': category,
        'raw_count': raw_count,
        'weighted_count': weighted_count,
        'pct_of_total': (weighted_count / df['weight'].sum()) * 100,
        'avg_price': weighted_avg_price,
        'price_min': price_min,
        'price_max': price_max,
        'price_median': price_median,
        'avg_rating': weighted_avg_rating,
        'rating_count': rating_count,
        'avg_reviews': weighted_avg_reviews,
        'retailer_diversity': retailer_count,
        'brand_count': brand_count,
        'top_brands': top_brands[:3]
    })

results_df = pd.DataFrame(results).sort_values('weighted_count', ascending=False)

print(f"\n{'='*80}")
print("WEIGHTED CATEGORY SUMMARY")
print(f"{'='*80}\n")

print(f"{'Category':<25} {'Raw':>8} {'Weighted':>10} {'%':>7} {'Avg Price':>12} {'Range':>20}")
print("-"*90)

for _, row in results_df.iterrows():
    print(f"{row['category']:<25} {row['raw_count']:>8,} {row['weighted_count']:>10,.0f} {row['pct_of_total']:>6.1f}% ${row['avg_price']:>10.2f} ${row['price_min']:.0f}-${row['price_max']:.0f}")

# ==============================================================================
# SUBCATEGORY ANALYSIS (if available)
# ==============================================================================

if 'Subcategory' in df.columns:
    print(f"\n{'='*80}")
    print("WEIGHTED SUBCATEGORY ANALYSIS")
    print(f"{'='*80}\n")

    subcategories = df['Subcategory'].dropna().unique()
    subcat_results = []

    for subcat in sorted(subcategories):
        subcat_df = df[df['Subcategory'] == subcat].copy()

        raw_count = len(subcat_df)
        weighted_count = subcat_df['weight'].sum()

        # Parent category
        if len(subcat_df) > 0 and len(subcat_df['Category'].mode()) > 0:
            parent_cat = subcat_df['Category'].mode().iloc[0]
        else:
            parent_cat = 'Unknown'

        # Price statistics
        prices = subcat_df[subcat_df['Price'].notna()].copy()
        if len(prices) > 0:
            weighted_avg_price = (prices['Price'] * prices['weight']).sum() / prices['weight'].sum()
            price_median = prices['Price'].median()
        else:
            weighted_avg_price = 0
            price_median = 0

        # Customer satisfaction
        ratings = subcat_df[subcat_df['Star Rating'].notna()].copy()
        if len(ratings) > 0:
            weighted_avg_rating = (ratings['Star Rating'] * ratings['weight']).sum() / ratings['weight'].sum()
        else:
            weighted_avg_rating = 0

        # Confidence score for inferred subcategories
        avg_confidence = subcat_df['Subcategory_Confidence'].mean() if 'Subcategory_Confidence' in subcat_df.columns else 1.0

        subcat_results.append({
            'subcategory': subcat,
            'parent_category': parent_cat,
            'raw_count': raw_count,
            'weighted_count': weighted_count,
            'pct_of_total': (weighted_count / df['weight'].sum()) * 100,
            'avg_price': weighted_avg_price,
            'median_price': price_median,
            'avg_rating': weighted_avg_rating,
            'avg_confidence': avg_confidence
        })

    subcat_df = pd.DataFrame(subcat_results)
    if len(subcat_df) > 0:
        subcat_df = subcat_df.sort_values('weighted_count', ascending=False)
    else:
        subcat_df = pd.DataFrame()

    print(f"{'Subcategory':<30} {'Parent Category':<25} {'Weighted':>10} {'%':>7} {'Avg Price':>12}")
    print("-"*90)

    for _, row in subcat_df.head(15).iterrows():
        print(f"{str(row['subcategory'])[:30]:<30} {str(row['parent_category'])[:25]:<25} {row['weighted_count']:>10,.0f} {row['pct_of_total']:>6.1f}% ${row['avg_price']:>10.2f}")

# ==============================================================================
# PRICE TIER ANALYSIS
# ==============================================================================

print(f"\n{'='*80}")
print("WEIGHTED PRICE TIER DISTRIBUTION")
print(f"{'='*80}\n")

df_price = df[df['Price'].notna()].copy()
df_price['price_tier'] = pd.cut(df_price['Price'],
                                  bins=[0, 10, 20, 30, 50, 100, float('inf')],
                                  labels=['Budget (<$10)', 'Value ($10-20)', 'Mid ($20-30)',
                                         'Premium ($30-50)', 'High ($50-100)', 'Luxury ($100+)'])

tier_summary = []
for tier in ['Budget (<$10)', 'Value ($10-20)', 'Mid ($20-30)', 'Premium ($30-50)', 'High ($50-100)', 'Luxury ($100+)']:
    tier_df = df_price[df_price['price_tier'] == tier]
    weighted_count = tier_df['weight'].sum()
    pct = (weighted_count / df_price['weight'].sum()) * 100

    tier_summary.append({
        'tier': tier,
        'weighted_count': weighted_count,
        'pct': pct,
        'raw_count': len(tier_df)
    })

print(f"{'Price Tier':<20} {'Weighted Count':>15} {'%':>8} {'Raw Count':>12}")
print("-"*60)

for item in tier_summary:
    print(f"{item['tier']:<20} {item['weighted_count']:>15,.0f} {item['pct']:>7.1f}% {item['raw_count']:>12,}")

# ==============================================================================
# SAVE RESULTS FOR SLIDE GENERATION
# ==============================================================================

output = {
    'summary': {
        'total_products': len(df),
        'total_weighted': df['weight'].sum(),
        'categories': len(categories),
        'avg_price': (df_price['Price'] * df_price['weight']).sum() / df_price['weight'].sum()
    },
    'categories': results_df.to_dict('records'),
    'subcategories': subcat_df.to_dict('records') if 'Subcategory' in df.columns else [],
    'price_tiers': tier_summary
}

output_file = Path(__file__).parent / "weighted_category_summary.json"
with open(output_file, 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n{'='*80}")
print(f"✓ Analysis complete - results saved to: {output_file.name}")
print(f"{'='*80}")
