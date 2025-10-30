#!/usr/bin/env python3
"""Infer subcategories from product names and descriptions using consistent classification"""

import pandas as pd
import numpy as np
import re
from pathlib import Path

# Load data
data_file = "/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/category-intelligence/04_CATEGORY_DATA_RIGHTSIZED.xlsx"
df = pd.read_excel(data_file)

print("="*80)
print("INFERRING SUBCATEGORIES FROM PRODUCT DATA")
print("="*80)
print(f"\nTotal Products: {len(df):,}")

# ==============================================================================
# SUBCATEGORY TAXONOMY - Consistent Classification Rules
# ==============================================================================

def infer_subcategory(row):
    """
    Infer subcategory from product name, description, and other fields.
    Returns tuple: (subcategory, confidence)
    """
    # Combine text fields for analysis
    product_name = str(row.get('Product Name', '')).lower()
    description = str(row.get('Description', '')).lower()
    category = str(row.get('Category', '')).lower()

    text = f"{product_name} {description}"

    # Rail/Slatwall System (highest priority - specific category)
    if category == 'rails & tracks':
        if any(word in text for word in ['slatwall', 'slat wall', 'wall panel', 'grid', 'pegboard']):
            return ('Slatwall & Pegboard Systems', 0.95)
        elif any(word in text for word in ['rail', 'track', 'hanging rail']):
            return ('Rail Systems', 0.90)
        else:
            return ('Rail & Track Systems', 0.70)

    # Cabinets & Storage Units
    if category == 'cabinets':
        if any(word in text for word in ['tool cabinet', 'tool chest', 'rolling cabinet']):
            return ('Tool Storage Cabinets', 0.95)
        elif any(word in text for word in ['locker', 'tall cabinet', 'storage cabinet']):
            return ('Storage Cabinets & Lockers', 0.90)
        else:
            return ('Cabinets', 0.70)

    # Shelving
    if category == 'shelving':
        if any(word in text for word in ['overhead', 'ceiling', 'mounted shelf']):
            return ('Overhead Storage', 0.95)
        elif any(word in text for word in ['heavy duty', 'industrial', 'steel shelf', 'metal rack']):
            return ('Heavy-Duty Shelving', 0.90)
        elif any(word in text for word in ['wall mount', 'floating', 'bracket']):
            return ('Wall-Mounted Shelving', 0.85)
        else:
            return ('Freestanding Shelving', 0.70)

    # Bins & Baskets
    if category == 'bins & baskets':
        if any(word in text for word in ['stackable', 'stack', 'storage bin', 'tote']):
            return ('Storage Bins & Totes', 0.90)
        elif any(word in text for word in ['basket', 'wire basket']):
            return ('Wire Baskets', 0.85)
        else:
            return ('Bins & Containers', 0.70)

    # Hooks & Hangers - Most granular classification
    if category == 'hooks & hangers':
        # Tool-specific hooks
        if any(word in text for word in ['bike hook', 'bicycle hook', 'bike hanger']):
            return ('Bike Hooks & Racks', 0.95)
        elif any(word in text for word in ['ladder hook', 'ladder rack', 'ladder hanger']):
            return ('Ladder Hooks', 0.95)
        elif any(word in text for word in ['tool hook', 'screwdriver', 'wrench', 'plier']):
            return ('Tool Hooks & Holders', 0.90)
        elif any(word in text for word in ['garden', 'hose', 'rake', 'shovel', 'broom']):
            return ('Garden Tool Hooks', 0.90)
        elif any(word in text for word in ['cord', 'cable', 'extension cord']):
            return ('Cord & Cable Hooks', 0.90)

        # Mounting type
        elif any(word in text for word in ['magnetic', 'magnet']):
            return ('Magnetic Hooks', 0.85)
        elif any(word in text for word in ['adhesive', 'stick', 'command', 'no drill']):
            return ('Adhesive Hooks', 0.85)
        elif any(word in text for word in ['j-hook', 'j hook', 'screw hook', 'utility hook']):
            return ('J-Hooks & Utility Hooks', 0.80)

        # Heavy duty
        elif any(word in text for word in ['heavy duty', 'heavy-duty', 'industrial']):
            return ('Heavy-Duty Hooks', 0.80)

        # Default for hooks
        else:
            return ('General Purpose Hooks', 0.60)

    # Storage & Organization (catch-all)
    if category == 'storage & organization':
        if any(word in text for word in ['workbench', 'work bench', 'work table']):
            return ('Workbenches & Tables', 0.90)
        elif any(word in text for word in ['organizer', 'divider', 'sorter']):
            return ('Organizers & Dividers', 0.85)
        elif any(word in text for word in ['cart', 'trolley', 'rolling']):
            return ('Mobile Storage Carts', 0.85)
        else:
            return ('General Storage Solutions', 0.60)

    # Garage Organization (general category)
    if category == 'garage organization':
        if any(word in text for word in ['sports', 'ball', 'equipment rack']):
            return ('Sports Equipment Storage', 0.85)
        elif any(word in text for word in ['tire', 'wheel']):
            return ('Tire Storage', 0.90)
        elif any(word in text for word in ['ceiling', 'overhead', 'hoist']):
            return ('Overhead Storage Systems', 0.85)
        else:
            return ('Multi-Purpose Organization', 0.60)

    # Default fallback
    return ('Uncategorized', 0.30)

# Apply inference
print("\n⏳ Analyzing products to infer subcategories...")

inference_results = df.apply(infer_subcategory, axis=1)
df['Subcategory_Inferred'] = [r[0] for r in inference_results]
df['Subcategory_Confidence'] = [r[1] for r in inference_results]
df['Subcategory_Is_Inferred'] = True

# If original subcategory exists, use it
original_subcats = df['Subcategory'].notna()
df.loc[original_subcats, 'Subcategory_Is_Inferred'] = False
df.loc[original_subcats, 'Subcategory_Inferred'] = df.loc[original_subcats, 'Subcategory']
df.loc[original_subcats, 'Subcategory_Confidence'] = 1.0

# Update the Subcategory column
df['Subcategory'] = df['Subcategory_Inferred']

print("✓ Subcategory inference complete")

# ==============================================================================
# SUMMARY OF INFERRED SUBCATEGORIES
# ==============================================================================

print(f"\n{'='*80}")
print("SUBCATEGORY CLASSIFICATION SUMMARY")
print(f"{'='*80}\n")

total_inferred = df['Subcategory_Is_Inferred'].sum()
total_original = (~df['Subcategory_Is_Inferred']).sum()

print(f"Total Products:        {len(df):>6,}")
print(f"Inferred Subcategory:  {total_inferred:>6,} ({total_inferred/len(df)*100:.1f}%)")
print(f"Original Subcategory:  {total_original:>6,} ({total_original/len(df)*100:.1f}%)")

print(f"\n{'='*80}")
print("SUBCATEGORY DISTRIBUTION")
print(f"{'='*80}\n")

subcat_summary = df.groupby(['Category', 'Subcategory']).agg({
    'Subcategory_Is_Inferred': ['count', 'sum'],
    'Subcategory_Confidence': 'mean',
    'Price': 'mean'
}).round(2)

subcat_summary.columns = ['Total', 'Inferred', 'Avg_Confidence', 'Avg_Price']
subcat_summary = subcat_summary.sort_values('Total', ascending=False)

print(f"{'Category':<25} {'Subcategory':<35} {'Total':>8} {'Inferred':>10} {'Conf':>6} {'Price':>10}")
print("-"*100)

for (cat, subcat), row in subcat_summary.head(30).iterrows():
    print(f"{cat[:25]:<25} {subcat[:35]:<35} {int(row['Total']):>8,} {int(row['Inferred']):>10,} {row['Avg_Confidence']:>6.2f} ${row['Avg_Price']:>9.2f}")

# ==============================================================================
# CONFIDENCE DISTRIBUTION
# ==============================================================================

print(f"\n{'='*80}")
print("INFERENCE CONFIDENCE DISTRIBUTION")
print(f"{'='*80}\n")

confidence_bins = [0, 0.5, 0.7, 0.8, 0.9, 1.0]
confidence_labels = ['Low (<0.5)', 'Medium (0.5-0.7)', 'Good (0.7-0.8)', 'High (0.8-0.9)', 'Very High (0.9+)']

df_inferred = df[df['Subcategory_Is_Inferred']].copy()
df_inferred['Confidence_Tier'] = pd.cut(df_inferred['Subcategory_Confidence'],
                                         bins=confidence_bins,
                                         labels=confidence_labels,
                                         include_lowest=True)

print(f"{'Confidence Tier':<20} {'Count':>10} {'%':>8}")
print("-"*40)

for tier in confidence_labels:
    count = (df_inferred['Confidence_Tier'] == tier).sum()
    pct = count / len(df_inferred) * 100
    print(f"{tier:<20} {count:>10,} {pct:>7.1f}%")

# ==============================================================================
# SAVE ENHANCED DATASET
# ==============================================================================

output_file = Path(data_file).parent / "04_CATEGORY_DATA_RIGHTSIZED_WITH_SUBCATS.xlsx"
df.to_excel(output_file, index=False)

print(f"\n{'='*80}")
print(f"✓ Enhanced dataset saved to: {output_file.name}")
print(f"{'='*80}")

print(f"\nNew columns added:")
print(f"  • Subcategory: Updated with inferred values")
print(f"  • Subcategory_Inferred: Inferred subcategory name")
print(f"  • Subcategory_Confidence: Confidence score (0-1)")
print(f"  • Subcategory_Is_Inferred: Flag indicating if inferred (True/False)")

print(f"\n{'='*80}")
print("READY FOR WEIGHTED ANALYSIS")
print(f"{'='*80}")
