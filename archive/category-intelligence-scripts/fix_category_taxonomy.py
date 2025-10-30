#!/usr/bin/env python3
"""Fix category taxonomy - remove 'Garage Organization' category and reclassify"""

import pandas as pd
import numpy as np
from pathlib import Path

# Load data
data_file = "/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/category-intelligence/04_CATEGORY_DATA_RIGHTSIZED_WITH_SUBCATS.xlsx"
df = pd.read_excel(data_file)

print("="*80)
print("FIXING CATEGORY TAXONOMY")
print("="*80)
print(f"\nTotal Products: {len(df):,}")

# Current categories
print("\nCurrent Category Distribution:")
print(df['Category'].value_counts())

print("\n" + "="*80)
print("RECLASSIFYING 'GARAGE ORGANIZATION' PRODUCTS")
print("="*80)

# Find ALL products that need reclassification
garage_org = df[df['Category'] == 'Garage Organization'].copy()
storage_org = df[df['Category'] == 'Storage & Organization'].copy()
total_to_reclassify = len(garage_org) + len(storage_org)

print(f"\nProducts in 'Garage Organization': {len(garage_org):,}")
print(f"Products in 'Storage & Organization': {len(storage_org):,}")
print(f"Total to reclassify: {total_to_reclassify:,}")

# Analyze their subcategories to understand what they are
print("\nCurrent subcategories in 'Garage Organization':")
print(garage_org['Subcategory'].value_counts().head(20))

if len(storage_org) > 0:
    print("\nCurrent subcategories in 'Storage & Organization':")
    print(storage_org['Subcategory'].value_counts().head(20))

# Reclassification logic based on product characteristics
def reclassify_garage_org(row):
    """
    Reclassify products into MECE categories.

    Valid Categories (mutually exclusive):
    - Hooks & Hangers: mounting accessories for hanging
    - Shelving: horizontal storage platforms & racks
    - Cabinets: enclosed storage units
    - Bins & Baskets: portable containers
    - Rails & Tracks: wall-mounted systems (slatwall, pegboard, rails)
    - Workbenches: work surfaces and tables
    - Specialty Holders: specific-use storage (bike stands, tire racks, sports equipment)
    """
    product_name = str(row.get('Product Name', '')).lower()
    description = str(row.get('Description', '')).lower()
    subcategory = str(row.get('Subcategory', '')).lower()

    text = f"{product_name} {description} {subcategory}"

    # WORKBENCHES - dedicated work surfaces
    if any(word in text for word in ['workbench', 'work bench', 'work table', 'work station', 'worktable']):
        return 'Workbenches', 'Work Surfaces'

    # SPECIALTY HOLDERS - specific purpose storage
    # Bike storage
    elif any(word in text for word in ['bike', 'bicycle', 'cycle']):
        return 'Specialty Holders', 'Bike Storage'

    # Tire storage
    elif any(word in text for word in ['tire', 'wheel']):
        return 'Specialty Holders', 'Tire Racks'

    # Sports equipment
    elif any(word in text for word in ['sports', 'ball', 'bat', 'racket', 'ski', 'snowboard', 'equipment rack']):
        return 'Specialty Holders', 'Sports Equipment'

    # Ladder storage
    elif any(word in text for word in ['ladder rack', 'ladder storage', 'ladder holder']) and 'hook' not in text:
        return 'Specialty Holders', 'Ladder Racks'

    # CABINETS - enclosed units
    elif any(word in text for word in ['cabinet', 'locker', 'enclosed']):
        return 'Cabinets', 'Storage Cabinets'

    # BINS & BASKETS - portable containers
    elif any(word in text for word in ['bin', 'container', 'basket', 'tote', 'box', 'organizer box']):
        return 'Bins & Baskets', 'Storage Containers'

    # SHELVING - horizontal platforms, racks, overhead
    elif any(word in text for word in ['shelf', 'shelving', 'rack', 'overhead', 'ceiling', 'platform', 'hoist', 'pulley']):
        if any(word in text for word in ['overhead', 'ceiling']):
            return 'Shelving', 'Overhead Storage'
        elif any(word in text for word in ['cart', 'trolley', 'rolling', 'mobile', 'wheels']):
            return 'Shelving', 'Mobile Carts'
        else:
            return 'Shelving', 'Storage Racks'

    # HOOKS & HANGERS - hanging accessories
    elif any(word in text for word in ['hook', 'hanger', 'hang']):
        return 'Hooks & Hangers', 'Utility Hooks'

    # RAILS & TRACKS - wall systems
    elif any(word in text for word in ['rail', 'track', 'slatwall', 'slat wall', 'pegboard', 'peg board', 'grid']):
        return 'Rails & Tracks', 'Wall Systems'

    # DEFAULT - if unclear, classify by product features
    else:
        # Check material/construction type
        if any(word in text for word in ['cabinet', 'drawer']):
            return 'Cabinets', 'Storage Units'
        elif any(word in text for word in ['stand', 'holder', 'mount']):
            return 'Specialty Holders', 'Specialty Storage'
        else:
            # Last resort: Shelving (most generic category)
            return 'Shelving', 'Storage Solutions'

# Apply reclassification
print("\n⏳ Reclassifying products...")

reclassified = []

# Reclassify both "Garage Organization" AND "Storage & Organization"
products_to_reclassify = pd.concat([garage_org, storage_org])

for idx, row in products_to_reclassify.iterrows():
    new_cat, new_subcat = reclassify_garage_org(row)
    reclassified.append({
        'index': idx,
        'old_category': row['Category'],
        'old_subcategory': row['Subcategory'],
        'new_category': new_cat,
        'new_subcategory': new_subcat,
        'product_name': row['Product Name']
    })

    # Update in dataframe
    df.at[idx, 'Category'] = new_cat
    df.at[idx, 'Subcategory'] = new_subcat
    df.at[idx, 'Subcategory_Inferred'] = new_subcat
    df.at[idx, 'Subcategory_Confidence'] = 0.85  # High confidence for rule-based reclassification

reclassified_df = pd.DataFrame(reclassified)

print("\nReclassification Summary:")
print(reclassified_df.groupby(['new_category', 'new_subcategory']).size().sort_values(ascending=False))

# Verify no more "Garage Organization" or "Storage & Organization" categories
print("\n" + "="*80)
print("UPDATED CATEGORY DISTRIBUTION")
print("="*80)

print(f"\n{'Category':<30} {'Count':>10} {'%':>8}")
print("-"*50)
for cat, count in df['Category'].value_counts().items():
    pct = count/len(df)*100
    print(f"{cat:<30} {count:>10,} {pct:>7.1f}%")

# Validation checks
garage_org_remaining = (df['Category'] == 'Garage Organization').sum()
storage_org_remaining = (df['Category'] == 'Storage & Organization').sum()
invalid_categories = garage_org_remaining + storage_org_remaining

if invalid_categories == 0:
    print(f"\n✅ SUCCESS: All invalid categories reclassified")
else:
    print(f"\n⚠️  WARNING: {invalid_categories} products still in invalid categories")

# Check for catch-all categories (>40% of products)
print("\n" + "="*80)
print("CATEGORY SIZE VALIDATION")
print("="*80)

issues = []
for cat, count in df['Category'].value_counts().items():
    pct = count/len(df)*100
    if pct > 40:
        issues.append(f"⚠️  '{cat}' contains {pct:.1f}% of products - may be too broad")
    elif count < 20:
        issues.append(f"⚠️  '{cat}' only has {count} products - may be too narrow")

if issues:
    print("\nCategory sizing issues:")
    for issue in issues:
        print(f"  {issue}")
else:
    print("\n✅ All categories properly sized")

# Save updated dataset
output_file = Path(data_file).parent / "04_CATEGORY_DATA_RIGHTSIZED_WITH_SUBCATS_FIXED.xlsx"
df.to_excel(output_file, index=False)

print(f"\n{'='*80}")
print(f"✓ Updated dataset saved to: {output_file.name}")
print(f"{'='*80}")

# Save reclassification log
log_file = Path(__file__).parent / "reclassification_log.csv"
reclassified_df.to_csv(log_file, index=False)
print(f"✓ Reclassification log saved to: {log_file.name}")
