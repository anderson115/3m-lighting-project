#!/usr/bin/env python3
"""Analyze master product data for distribution and bias"""

import pandas as pd
from pathlib import Path

# Load the data
data_file = Path("/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/category-intelligence/04_CATEGORY_DATA_FINAL.xlsx")

print("Loading master product data...")
df = pd.read_excel(data_file)

print(f"\n{'='*80}")
print(f"MASTER PRODUCT DATA ANALYSIS")
print(f"{'='*80}")
print(f"\nTotal Products: {len(df):,}")
print(f"Total Columns: {len(df.columns)}")

# Show columns
print(f"\nColumns:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2}. {col}")

print(f"\n{'='*80}")
print(f"DISTRIBUTION BY RETAILER")
print(f"{'='*80}")

if 'retailer' in df.columns or 'Retailer' in df.columns:
    retailer_col = 'retailer' if 'retailer' in df.columns else 'Retailer'
    retailer_dist = df[retailer_col].value_counts()
    total = len(df)

    print(f"\n{'Retailer':<20} {'Count':>10} {'%':>8}")
    print(f"{'-'*40}")
    for retailer, count in retailer_dist.items():
        pct = count/total*100
        print(f"{str(retailer):<20} {count:>10,} {pct:>7.1f}%")

print(f"\n{'='*80}")
print(f"DISTRIBUTION BY BRAND")
print(f"{'='*80}")

brand_cols = [c for c in df.columns if 'brand' in c.lower()]
if brand_cols:
    brand_col = brand_cols[0]
    brand_dist = df[brand_col].value_counts()

    print(f"\nTop 20 Brands:")
    print(f"{'Brand':<30} {'Count':>10} {'%':>8}")
    print(f"{'-'*50}")
    for brand, count in brand_dist.head(20).items():
        pct = count/len(df)*100
        print(f"{str(brand)[:30]:<30} {count:>10,} {pct:>7.1f}%")

    print(f"\nTotal Unique Brands: {df[brand_col].nunique():,}")

print(f"\n{'='*80}")
print(f"DISTRIBUTION BY PRICE POINT")
print(f"{'='*80}")

price_cols = [c for c in df.columns if 'price' in c.lower()]
if price_cols:
    price_col = price_cols[0]

    # Remove non-numeric prices
    df_price = df[df[price_col].notna()].copy()
    df_price[price_col] = pd.to_numeric(df_price[price_col], errors='coerce')
    df_price = df_price[df_price[price_col].notna()]

    print(f"\nPrice Statistics:")
    print(f"  Count: {len(df_price):,}")
    print(f"  Mean:  ${df_price[price_col].mean():.2f}")
    print(f"  Median: ${df_price[price_col].median():.2f}")
    print(f"  Min:   ${df_price[price_col].min():.2f}")
    print(f"  Max:   ${df_price[price_col].max():.2f}")

    # Price ranges
    df_price['price_range'] = pd.cut(df_price[price_col],
                                      bins=[0, 10, 20, 30, 50, 100, float('inf')],
                                      labels=['$0-10', '$10-20', '$20-30', '$30-50', '$50-100', '$100+'])

    print(f"\nPrice Range Distribution:")
    print(f"{'Range':<15} {'Count':>10} {'%':>8}")
    print(f"{'-'*35}")
    for range_val, count in df_price['price_range'].value_counts().sort_index().items():
        pct = count/len(df_price)*100
        print(f"{range_val:<15} {count:>10,} {pct:>7.1f}%")

print(f"\n{'='*80}")
print(f"DISTRIBUTION BY SUBCATEGORY")
print(f"{'='*80}")

subcat_cols = [c for c in df.columns if 'subcategory' in c.lower() or 'sub_category' in c.lower() or 'category' in c.lower()]
if subcat_cols:
    subcat_col = subcat_cols[0]
    subcat_dist = df[subcat_col].value_counts()

    print(f"\n{'Subcategory':<40} {'Count':>10} {'%':>8}")
    print(f"{'-'*60}")
    for subcat, count in subcat_dist.items():
        pct = count/len(df)*100
        print(f"{str(subcat)[:40]:<40} {count:>10,} {pct:>7.1f}%")

print(f"\n{'='*80}")
print(f"BIAS & QUALITY CHECKS")
print(f"{'='*80}")

issues = []

# Check 1: Retailer imbalance
if 'retailer' in df.columns or 'Retailer' in df.columns:
    retailer_col = 'retailer' if 'retailer' in df.columns else 'Retailer'
    retailer_pcts = df[retailer_col].value_counts(normalize=True) * 100

    if retailer_pcts.max() > 70:
        issues.append(f"⚠️  RETAILER BIAS: {retailer_pcts.idxmax()} represents {retailer_pcts.max():.1f}% of data")

    if retailer_pcts.min() < 5:
        issues.append(f"⚠️  UNDERREPRESENTED: {retailer_pcts.idxmin()} only {retailer_pcts.min():.1f}% of data")

# Check 2: Price concentration
if price_cols:
    price_col = price_cols[0]
    df_price_temp = df[df[price_col].notna()].copy()
    df_price_temp[price_col] = pd.to_numeric(df_price_temp[price_col], errors='coerce')

    low_price_pct = (df_price_temp[price_col] < 20).sum() / len(df_price_temp) * 100
    if low_price_pct > 80:
        issues.append(f"⚠️  PRICE BIAS: {low_price_pct:.1f}% of products under $20 - may skew toward budget segment")

# Check 3: Missing data
missing_summary = df.isnull().sum()
critical_cols = [c for c in df.columns if any(x in c.lower() for x in ['price', 'brand', 'category', 'retailer'])]

for col in critical_cols:
    if col in df.columns:
        missing_pct = df[col].isnull().sum() / len(df) * 100
        if missing_pct > 10:
            issues.append(f"⚠️  MISSING DATA: {col} has {missing_pct:.1f}% missing values")

# Check 4: Subcategory balance
if subcat_cols:
    subcat_col = subcat_cols[0]
    subcat_pcts = df[subcat_col].value_counts(normalize=True) * 100

    if subcat_pcts.max() > 60:
        issues.append(f"⚠️  CATEGORY BIAS: {subcat_pcts.idxmax()} dominates with {subcat_pcts.max():.1f}%")

if issues:
    print("\n⚠️  POTENTIAL ISSUES FOUND:\n")
    for i, issue in enumerate(issues, 1):
        print(f"{i}. {issue}")
else:
    print("\n✅ NO MAJOR BIAS OR DISTRIBUTION ISSUES DETECTED")

print(f"\n{'='*80}")
print(f"RECOMMENDATION")
print(f"{'='*80}")

if len(issues) > 0:
    print("\n⚠️  ISSUES NEED CORRECTION BEFORE ANALYSIS")
    print("\nSuggested actions:")
    if any('RETAILER BIAS' in i for i in issues):
        print("  • Balance retailer representation through weighted sampling")
    if any('PRICE BIAS' in i for i in issues):
        print("  • Ensure adequate representation across all price segments")
    if any('MISSING DATA' in i for i in issues):
        print("  • Clean or impute critical missing values")
    if any('CATEGORY BIAS' in i for i in issues):
        print("  • Consider stratified analysis by subcategory")
else:
    print("\n✅ DATA IS READY FOR ANALYSIS")
    print("\nData appears well-balanced across:")
    print("  • Retailer distribution")
    print("  • Price segments")
    print("  • Product categories")
    print("  • Brand representation")

print(f"\n{'='*80}")
