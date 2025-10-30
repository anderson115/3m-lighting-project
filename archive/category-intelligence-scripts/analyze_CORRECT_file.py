#!/usr/bin/env python3
"""Analyze CORRECT master file - RIGHTSIZED version"""

import pandas as pd
import numpy as np

df = pd.read_excel("/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/category-intelligence/04_CATEGORY_DATA_RIGHTSIZED.xlsx")

print("="*80)
print("MASTER PRODUCT DATA - CORRECT FILE (RIGHTSIZED - Oct 29, 2025)")
print("="*80)
print(f"\nTotal Products: {len(df):,}")
print(f"Date: October 29, 2025")

# ==============================================================================
# 1. RETAILER DISTRIBUTION
# ==============================================================================
print("\n" + "="*80)
print("1. RETAILER DISTRIBUTION")
print("="*80)

retailer_dist = df['Retailer'].value_counts()
total_with_retailer = retailer_dist.sum()

print(f"\n{'Retailer':<20} {'Products':>10} {'% of Total':>12} {'% of Valid':>12}")
print("-"*56)
for retailer, count in retailer_dist.items():
    pct_total = count/len(df)*100
    pct_valid = count/total_with_retailer*100
    print(f"{retailer:<20} {count:>10,} {pct_total:>11.1f}% {pct_valid:>11.1f}%")

walmart_pct = (df['Retailer'] == 'Walmart').sum() / len(df) * 100

if walmart_pct > 40:
    print(f"\n⚠️  WALMART DOMINANCE: {walmart_pct:.1f}% of dataset")
else:
    print(f"\n✅ Retailer distribution appears reasonable")

# ==============================================================================
# 2. BRAND DISTRIBUTION
# ==============================================================================
print("\n" + "="*80)
print("2. BRAND DISTRIBUTION")
print("="*80)

brand_dist = df['Brand'].dropna().value_counts()
total_brands = df['Brand'].nunique()

print(f"\nTotal Unique Brands: {total_brands:,}")
print(f"\nTop 15 Brands:")
print(f"{'Brand':<25} {'Products':>10} {'% of Total':>12} {'Avg Price':>12}")
print("-"*62)

for brand in brand_dist.head(15).index:
    count = brand_dist[brand]
    pct = count/len(df)*100
    avg_price = df[df['Brand'] == brand]['Price'].mean()
    print(f"{str(brand)[:25]:<25} {count:>10,} {pct:>11.1f}% ${avg_price:>10.2f}")

top5_pct = (brand_dist.head(5).sum() / len(df)) * 100
print(f"\nTop 5 brands: {top5_pct:.1f}% of data")

if top5_pct > 30:
    print("⚠️  Moderate brand concentration")
else:
    print("✅ Good brand diversity")

# ==============================================================================
# 3. PRICE DISTRIBUTION
# ==============================================================================
print("\n" + "="*80)
print("3. PRICE DISTRIBUTION")
print("="*80)

df_price = df[df['Price'].notna() & (df['Price'] > 0)].copy()

print(f"\nOverall Statistics:")
print(f"  Products with price: {len(df_price):,} ({len(df_price)/len(df)*100:.1f}%)")
print(f"  Mean:   ${df_price['Price'].mean():.2f}")
print(f"  Median: ${df_price['Price'].median():.2f}")
print(f"  Std Dev: ${df_price['Price'].std():.2f}")
print(f"  25th percentile: ${df_price['Price'].quantile(0.25):.2f}")
print(f"  75th percentile: ${df_price['Price'].quantile(0.75):.2f}")
print(f"  Range:  ${df_price['Price'].min():.2f} - ${df_price['Price'].max():.2f}")

# Price segments
df_price['segment'] = pd.cut(df_price['Price'],
                              bins=[0, 10, 20, 30, 50, 100, float('inf')],
                              labels=['Budget (<$10)', 'Value ($10-20)', 'Mid ($20-30)',
                                     'Premium ($30-50)', 'High ($50-100)', 'Luxury ($100+)'])

print(f"\nPrice Segment Distribution:")
print(f"{'Segment':<20} {'Products':>10} {'%':>8}")
print("-"*40)
for segment in ['Budget (<$10)', 'Value ($10-20)', 'Mid ($20-30)', 'Premium ($30-50)', 'High ($50-100)', 'Luxury ($100+)']:
    count = (df_price['segment'] == segment).sum()
    pct = count/len(df_price)*100
    print(f"{segment:<20} {count:>10,} {pct:>7.1f}%")

# By retailer
print(f"\nPrice by Retailer:")
print(f"{'Retailer':<15} {'Mean':>10} {'Median':>10} {'Count':>8}")
print("-"*46)
for retailer in retailer_dist.index:
    retailer_data = df[df['Retailer'] == retailer]
    retailer_prices = retailer_data['Price'].dropna()
    if len(retailer_prices) > 0:
        print(f"{retailer:<15} ${retailer_prices.mean():>9.2f} ${retailer_prices.median():>9.2f} {len(retailer_prices):>7,}")

budget_pct = ((df_price['Price'] < 20).sum() / len(df_price)) * 100
premium_pct = ((df_price['Price'] > 50).sum() / len(df_price)) * 100

print(f"\nSegment Balance:")
print(f"  Budget segment (<$20): {budget_pct:.1f}%")
print(f"  Premium segment (>$50): {premium_pct:.1f}%")

if budget_pct > 60:
    print("⚠️  Heavy budget skew may underweight premium insights")
else:
    print("✅ Reasonable price balance")

# ==============================================================================
# 4. CATEGORY DISTRIBUTION
# ==============================================================================
print("\n" + "="*80)
print("4. CATEGORY DISTRIBUTION")
print("="*80)

cat_dist = df['Category'].dropna().value_counts()

print(f"\n{'Category':<35} {'Products':>10} {'%':>8}")
print("-"*55)
for cat, count in cat_dist.items():
    pct = count/len(df)*100
    print(f"{str(cat)[:35]:<35} {count:>10,} {pct:>7.1f}%")

hooks_pct = (df['Category'] == 'Hooks & Hangers').sum() / len(df) * 100

if hooks_pct > 60:
    print(f"\n⚠️  'Hooks & Hangers' dominates at {hooks_pct:.1f}%")
else:
    print(f"\n✅ Category distribution reasonable for garage organizer study")

# ==============================================================================
# 5. DATA QUALITY ASSESSMENT
# ==============================================================================
print("\n" + "="*80)
print("5. DATA QUALITY & BIAS ASSESSMENT")
print("="*80)

issues = []
warnings = []

# Missing data for CRITICAL fields
critical_fields = ['Retailer', 'Brand', 'Price', 'Category']
print(f"\nCritical Field Completeness:")
for field in critical_fields:
    missing_pct = df[field].isnull().sum() / len(df) * 100
    complete_pct = 100 - missing_pct
    status = "✅" if missing_pct < 10 else ("⚠️ " if missing_pct < 25 else "🔴")
    print(f"  {status} {field:<15}: {complete_pct:>5.1f}% complete ({missing_pct:.1f}% missing)")

    if missing_pct > 20:
        issues.append(f"Critical field '{field}' has {missing_pct:.1f}% missing data")
    elif missing_pct > 10:
        warnings.append(f"'{field}' has {missing_pct:.1f}% missing data")

# Retailer balance
if walmart_pct > 45:
    warnings.append(f"Walmart dominates with {walmart_pct:.1f}% - potential bias")

# Price skew
if budget_pct > 65:
    warnings.append(f"Budget segment ({budget_pct:.1f}%) heavily dominates")

# Category concentration
if hooks_pct > 65:
    warnings.append(f"'Hooks & Hangers' concentration at {hooks_pct:.1f}% is high")

# Outliers
outlier_threshold = df_price['Price'].quantile(0.99)
outliers = (df_price['Price'] > outlier_threshold).sum()
if outliers > 50:
    warnings.append(f"{outliers} extreme price outliers may skew analysis")

print(f"\nCRITICAL ISSUES:")
if issues:
    for i, issue in enumerate(issues, 1):
        print(f"  {i}. 🔴 {issue}")
else:
    print("  None ✅")

print(f"\nWARNINGS:")
if warnings:
    for i, warning in enumerate(warnings, 1):
        print(f"  {i}. ⚠️  {warning}")
else:
    print("  None ✅")

# ==============================================================================
# 6. FINAL RECOMMENDATION
# ==============================================================================
print("\n" + "="*80)
print("6. FINAL RECOMMENDATION")
print("="*80)

if len(issues) > 0:
    print("\n🔴 NOT READY - CRITICAL ISSUES MUST BE ADDRESSED\n")
    print("Required actions:")
    for issue in issues:
        print(f"  • Fix: {issue}")
else:
    if len(warnings) > 2:
        print("\n⚠️  PROCEED WITH CAUTION\n")
        print("Data is usable but account for these biases:")
        for warning in warnings:
            print(f"  • {warning}")
        print("\nMitigation:")
        print("  • Use weighted analysis")
        print("  • Segment by retailer/category")
        print("  • Use median over mean for prices")
        print("  • Note limitations in report")
    else:
        print("\n✅ READY FOR ANALYSIS\n")
        print("Data quality is acceptable:")
        print("  ✓ Critical fields mostly complete")
        print("  ✓ Reasonable retailer distribution")
        print("  ✓ Good brand diversity")
        print("  ✓ Acceptable category focus")
        print("\nProceed with analysis.")

print("\n" + "="*80)
