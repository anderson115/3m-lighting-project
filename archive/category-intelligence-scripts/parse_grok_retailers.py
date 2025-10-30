#!/usr/bin/env python3
"""
Parse manually scraped retailer data (Menards, Ace Hardware, Home Depot)
that was parsed using Grok and stored in markdown tables.
"""

import pandas as pd
import re
from pathlib import Path
import hashlib

# File paths
MERGED_FILE = Path("modules/category-intelligence/data/retailers/manual_grok_parsed/menards-ace-homedpot.md")
MASTER_FILE = Path("modules/category-intelligence/04_CATEGORY_DATA_ALL_PRODUCTS_WEIGHTED.xlsx")
OUTPUT_FILE = Path("modules/category-intelligence/04_CATEGORY_DATA_ALL_PRODUCTS_WEIGHTED.xlsx")

print("="*80)
print("PARSING GROK-EXTRACTED RETAILER DATA")
print("="*80)

# Read the merged file
with open(MERGED_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Split by section headers
sections = {}
current_section = None
current_lines = []

for line in content.split('\n'):
    if line.strip().startswith('## '):
        # Save previous section
        if current_section:
            sections[current_section] = '\n'.join(current_lines)
        # Start new section
        current_section = line.strip().replace('## ', '')
        current_lines = []
    else:
        current_lines.append(line)

# Save last section
if current_section:
    sections[current_section] = '\n'.join(current_lines)

print(f"\nFound {len(sections)} retailer sections:")
for retailer in sections.keys():
    print(f"  - {retailer}")

# Parse each section
all_products = []

for retailer, section_content in sections.items():
    print(f"\nParsing {retailer}...")

    # Split into lines and find table
    lines = section_content.strip().split('\n')

    # Find table header
    header_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith('|') and 'Name' in line:
            header_idx = i
            break

    if header_idx is None:
        print(f"  ⚠️  No table found in {retailer} section")
        continue

    # Extract headers
    header_line = lines[header_idx]
    headers = [h.strip() for h in header_line.split('|') if h.strip()]
    print(f"  Columns: {headers}")

    # Skip separator line (---|---|---)
    data_start = header_idx + 2

    # Parse rows
    product_count = 0
    for line in lines[data_start:]:
        if not line.strip() or not line.strip().startswith('|'):
            continue

        # Split by | and keep all cells (including empty ones)
        cells = line.split('|')[1:-1]  # Remove first and last empty strings from split
        cells = [c.strip() for c in cells]

        # Create product dict
        if len(cells) > 0:
            product = {'retailer': retailer}
            for i, header in enumerate(headers):
                if i < len(cells):
                    product[header] = cells[i]
                else:
                    product[header] = ''

            # Skip if no product name
            if not product.get('Name', '').strip():
                continue

            # Clean price values
            price_str = product.get('Price', '') or product.get('Sale Price', '')
            if price_str:
                price_str = re.sub(r'[^\d.]', '', price_str)
                try:
                    product['price_cleaned'] = float(price_str) if price_str else None
                except:
                    product['price_cleaned'] = None
            else:
                product['price_cleaned'] = None

            # Extract rating
            rating_str = product.get('Ratings', '') or product.get('Rating', '')
            if rating_str:
                match = re.search(r'(\d+\.?\d*)', rating_str)
                if match:
                    product['rating_cleaned'] = float(match.group(1))
                else:
                    product['rating_cleaned'] = None
            else:
                product['rating_cleaned'] = None

            # Generate synthetic URL/ID
            name = product.get('Name', '')
            sku = product.get('Sku', '') or product.get('SKU', '')
            product_id = f"{retailer.lower().replace(' ', '_')}_{sku or hashlib.md5(name.encode()).hexdigest()[:8]}"
            product['product_id'] = product_id

            all_products.append(product)
            product_count += 1

    print(f"  ✅ Parsed {product_count} products")

print(f"\n{'='*80}")
print(f"TOTAL PRODUCTS PARSED: {len(all_products)}")
print(f"{'='*80}")

# Count by retailer
retailer_counts = {}
for p in all_products:
    ret = p['retailer']
    retailer_counts[ret] = retailer_counts.get(ret, 0) + 1

print("\nProducts by retailer:")
for retailer, count in sorted(retailer_counts.items()):
    print(f"  {retailer:15s} {count:4d}")

# Create DataFrame with columns matching master spreadsheet EXACTLY
df_new = pd.DataFrame()
df_new['Retailer'] = [p.get('retailer', '').lower().replace(' ', '').capitalize() for p in all_products]
df_new['Product Name'] = [p.get('Name', '') for p in all_products]
df_new['Brand'] = [p.get('Brand', '') for p in all_products]
df_new['Product Link'] = [f"manual_{p.get('product_id', '')}" for p in all_products]
df_new['Price'] = [p.get('price_cleaned') for p in all_products]
df_new['Star Rating'] = [p.get('rating_cleaned') for p in all_products]
df_new['Material'] = [p.get('Material', '') for p in all_products]
df_new['Color'] = [p.get('Color', '') for p in all_products]
# Note: Dimensions from Grok data but not in master schema - will add as new column if needed

print(f"\nCreated DataFrame with {len(df_new)} products")
print(f"\nColumns: {list(df_new.columns)}")

# Load existing master spreadsheet
print(f"\nLoading master spreadsheet...")
df_master = pd.read_excel(MASTER_FILE)
print(f"Existing products: {len(df_master)}")
print(f"Existing columns: {list(df_master.columns)}")

# Map new columns to match master spreadsheet column names
column_mapping = {
    'title': 'title',
    'brand': 'brand',
    'price': 'price',
    'rating': 'rating',
    'retailer': 'retailer',
    'sku': 'sku',
    'url': 'url',
    'source': 'source',
    'dimensions': 'dimensions',
    'material': 'material',
    'color': 'color'
}

# Add any missing columns from master with None values
for col in df_master.columns:
    if col not in df_new.columns:
        df_new[col] = None

# Reorder to match master
df_new = df_new[df_master.columns]

# Append new products
df_combined = pd.concat([df_master, df_new], ignore_index=True)
print(f"\nCombined dataset: {len(df_combined)} products")
print(f"  - Existing: {len(df_master)}")
print(f"  - New: {len(df_new)}")

# Save updated spreadsheet
print(f"\nSaving to {OUTPUT_FILE}...")
df_combined.to_excel(OUTPUT_FILE, index=False)
print(f"✅ Saved successfully!")

# Summary stats
print(f"\n{'='*80}")
print(f"SUMMARY")
print(f"{'='*80}")
print(f"New products added: {len(df_new)}")
print(f"Total products in dataset: {len(df_combined)}")
print(f"\nNew retailer coverage:")
print(f"  Menards: {retailer_counts.get('Menards', 0)} products")
print(f"  Ace Hardware: {retailer_counts.get('Ace Hardware', 0)} products")
print(f"  Home Depot: {retailer_counts.get('Home Depot', 0)} products (supplemental)")
print(f"\n✅ Master spreadsheet updated!")
