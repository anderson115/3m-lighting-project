#!/usr/bin/env python3
"""Extract strategic insights from weighted product data for slides 2-3"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

# Load fixed data with corrected categories
data_file = "/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/category-intelligence/04_CATEGORY_DATA_RIGHTSIZED_WITH_SUBCATS_FIXED.xlsx"
df = pd.read_excel(data_file)

print("="*80)
print("EXTRACTING STRATEGIC PRODUCT INSIGHTS")
print("="*80)

# Apply weights
retailer_weights = {
    'Walmart': 0.38, 'Homedepot': 0.85, 'Amazon': 1.40,
    'Target': 1.67, 'Lowes': 1.92, 'Menards': 2.90, 'Acehardware': 7.50
}
category_weights = {'Hooks & Hangers': 0.69}

def calculate_weight(row):
    retailer_weight = retailer_weights.get(row['Retailer'], 1.0)
    category_weight = category_weights.get(row['Category'], 1.0)
    return retailer_weight * category_weight

df['weight'] = df.apply(calculate_weight, axis=1)

# ==============================================================================
# INSIGHT 1: QUALITY GAP ANALYSIS (High Price + Low Rating = Opportunity)
# ==============================================================================

print("\n" + "="*80)
print("1. QUALITY GAP ANALYSIS")
print("="*80)

df_quality = df[df['Price'].notna() & df['Star Rating'].notna()].copy()

# Calculate weighted averages by category
quality_gaps = []
for category in df['Category'].dropna().unique():
    cat_df = df_quality[df_quality['Category'] == category].copy()

    if len(cat_df) > 10:  # Only categories with meaningful sample size
        weighted_avg_price = (cat_df['Price'] * cat_df['weight']).sum() / cat_df['weight'].sum()
        weighted_avg_rating = (cat_df['Star Rating'] * cat_df['weight']).sum() / cat_df['weight'].sum()
        weighted_count = cat_df['weight'].sum()

        # Quality gap score: high price but low rating
        gap_score = weighted_avg_price / (weighted_avg_rating ** 2)  # Higher = worse value

        quality_gaps.append({
            'category': category,
            'avg_price': weighted_avg_price,
            'avg_rating': weighted_avg_rating,
            'weighted_count': weighted_count,
            'gap_score': gap_score,
            'quadrant': 'Premium' if weighted_avg_price > 80 and weighted_avg_rating > 4.0 else
                       'Quality Gap' if weighted_avg_price > 80 and weighted_avg_rating < 4.0 else
                       'Value' if weighted_avg_price < 80 and weighted_avg_rating > 4.0 else
                       'Budget'
        })

quality_df = pd.DataFrame(quality_gaps).sort_values('gap_score', ascending=False)

print("\nTop Quality Gap Categories (High Price, Low Satisfaction):")
print(f"{'Category':<30} {'Avg Price':>12} {'Avg Rating':>12} {'Gap Score':>12}")
print("-"*70)
for _, row in quality_df[quality_df['quadrant'] == 'Quality Gap'].head(3).iterrows():
    print(f"{row['category']:<30} ${row['avg_price']:>11.2f} {row['avg_rating']:>12.2f} {row['gap_score']:>12.1f}")

print("\nPremium Success Categories (High Price, High Satisfaction):")
for _, row in quality_df[quality_df['quadrant'] == 'Premium'].head(3).iterrows():
    print(f"{row['category']:<30} ${row['avg_price']:>11.2f} {row['avg_rating']:>12.2f}")

# ==============================================================================
# INSIGHT 2: MARKET SATURATION INDEX
# ==============================================================================

print("\n" + "="*80)
print("2. MARKET SATURATION ANALYSIS")
print("="*80)

saturation = []
for category in df['Category'].dropna().unique():
    cat_df = df[df['Category'] == category].copy()

    weighted_count = cat_df['weight'].sum()
    brand_count = cat_df['Brand'].nunique()

    # Saturation = products per brand (high = crowded)
    saturation_index = weighted_count / brand_count if brand_count > 0 else 0

    # Review volume as demand indicator
    reviews = cat_df[cat_df['Review Count'].notna()]
    avg_reviews = (reviews['Review Count'] * reviews['weight']).sum() / reviews['weight'].sum() if len(reviews) > 0 else 0

    saturation.append({
        'category': category,
        'weighted_count': weighted_count,
        'brand_count': brand_count,
        'saturation_index': saturation_index,
        'avg_reviews': avg_reviews,
        'market_state': 'Crowded' if saturation_index > 3 and brand_count > 50 else
                       'Fragmented' if saturation_index < 2 and brand_count > 30 else
                       'Emerging' if weighted_count < 200 and avg_reviews > 100 else
                       'Established'
    })

saturation_df = pd.DataFrame(saturation).sort_values('saturation_index', ascending=False)

print("\nMost Crowded Categories:")
print(f"{'Category':<30} {'Products':>10} {'Brands':>8} {'Sat Index':>12} {'State':<12}")
print("-"*75)
for _, row in saturation_df.head(5).iterrows():
    print(f"{row['category']:<30} {row['weighted_count']:>10,.0f} {row['brand_count']:>8} {row['saturation_index']:>12.1f} {row['market_state']:<12}")

print("\nEmerging/Underserved Categories:")
for _, row in saturation_df[saturation_df['market_state'] == 'Emerging'].head(3).iterrows():
    print(f"{row['category']:<30} {row['weighted_count']:>10,.0f} {row['brand_count']:>8} {row['avg_reviews']:>12,.0f} reviews")

# ==============================================================================
# INSIGHT 3: RETAILER CATEGORY OWNERSHIP
# ==============================================================================

print("\n" + "="*80)
print("3. RETAILER CATEGORY DOMINANCE")
print("="*80)

retailer_share = []
for category in df['Category'].dropna().unique():
    cat_df = df[df['Category'] == category].copy()
    total_weighted = cat_df['weight'].sum()

    for retailer in df['Retailer'].unique():
        retailer_count = cat_df[cat_df['Retailer'] == retailer]['weight'].sum()
        share_pct = (retailer_count / total_weighted * 100) if total_weighted > 0 else 0

        if share_pct > 0:
            retailer_share.append({
                'category': category,
                'retailer': retailer,
                'share_pct': share_pct,
                'weighted_count': retailer_count
            })

retailer_df = pd.DataFrame(retailer_share)

# Find dominant retailer per category
print("\nRetailer Category Ownership:")
print(f"{'Category':<30} {'Dominant Retailer':<15} {'Share':>8}")
print("-"*56)

for category in df['Category'].dropna().unique():
    cat_share = retailer_df[retailer_df['category'] == category].sort_values('share_pct', ascending=False)
    if len(cat_share) > 0:
        top = cat_share.iloc[0]
        print(f"{category:<30} {top['retailer']:<15} {top['share_pct']:>7.1f}%")

# ==============================================================================
# INSIGHT 4: INSTALLATION BARRIER PREMIUM
# ==============================================================================

print("\n" + "="*80)
print("4. INSTALLATION METHOD ANALYSIS")
print("="*80)

# Identify adhesive vs drill-required products
df_install = df[df['Price'].notna()].copy()
df_install['is_adhesive'] = df_install['Product Name'].str.lower().str.contains('adhesive|command|stick|no drill', na=False)
df_install['is_magnetic'] = df_install['Product Name'].str.lower().str.contains('magnetic|magnet', na=False)

adhesive_price = (df_install[df_install['is_adhesive']]['Price'] * df_install[df_install['is_adhesive']]['weight']).sum() / df_install[df_install['is_adhesive']]['weight'].sum()
drill_price = (df_install[~df_install['is_adhesive'] & ~df_install['is_magnetic']]['Price'] * df_install[~df_install['is_adhesive'] & ~df_install['is_magnetic']]['weight']).sum() / df_install[~df_install['is_adhesive'] & ~df_install['is_magnetic']]['weight'].sum()

print(f"\nAdhesive/Tool-Free Products:  ${adhesive_price:.2f} avg")
print(f"Drill-Required Products:      ${drill_price:.2f} avg")
print(f"Price Differential:           ${drill_price - adhesive_price:.2f} ({((drill_price/adhesive_price - 1) * 100):.1f}% premium)")

# ==============================================================================
# SAVE INSIGHTS FOR SLIDE GENERATION
# ==============================================================================

insights = {
    'quality_gaps': quality_df.to_dict('records'),
    'market_saturation': saturation_df.to_dict('records'),
    'retailer_dominance': retailer_df.to_dict('records'),
    'installation_analysis': {
        'adhesive_avg_price': adhesive_price,
        'drill_avg_price': drill_price,
        'price_differential': drill_price - adhesive_price,
        'premium_pct': ((drill_price/adhesive_price - 1) * 100)
    },
    'summary_stats': {
        'total_products': len(df),
        'total_weighted': df['weight'].sum(),
        'categories': len(df['Category'].dropna().unique()),
        'retailers': len(df['Retailer'].unique()),
        'brands': len(df['Brand'].dropna().unique())
    }
}

output_file = Path(__file__).parent / "product_insights.json"
with open(output_file, 'w') as f:
    json.dump(insights, f, indent=2)

print(f"\n{'='*80}")
print(f"✓ Insights saved to: {output_file.name}")
print(f"{'='*80}")
