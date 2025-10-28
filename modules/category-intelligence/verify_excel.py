#!/usr/bin/env python3
"""Verify the Excel file has correct data"""
import pandas as pd
from pathlib import Path

excel_file = Path(__file__).parent / "04_CATEGORY_DATA.xlsx"

df = pd.read_excel(excel_file)

print("=" * 70)
print("EXCEL FILE VERIFICATION")
print("=" * 70)
print(f"\nTotal rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"\nColumns: {list(df.columns)}")

print("\n" + "=" * 70)
print("CHECKING FOR BLANK DATA IN KEY COLUMNS")
print("=" * 70)

# Check Product Name
blank_names = df['Product Name'].isna() | (df['Product Name'] == '')
print(f"\nProduct Name: {blank_names.sum()} blank out of {len(df)} ({(blank_names.sum()/len(df)*100):.1f}%)")

# Check Brand
blank_brands = df['Brand'].isna() | (df['Brand'] == '')
print(f"Brand: {blank_brands.sum()} blank out of {len(df)} ({(blank_brands.sum()/len(df)*100):.1f}%)")

# Check Description
blank_descs = df['Description'].isna() | (df['Description'] == '')
print(f"Description: {blank_descs.sum()} blank out of {len(df)} ({(blank_descs.sum()/len(df)*100):.1f}%)")

print("\n" + "=" * 70)
print("SAMPLE ROWS (First 5)")
print("=" * 70)

for i in range(min(5, len(df))):
    row = df.iloc[i]
    print(f"\nRow {i+1}:")
    print(f"  Retailer: {row['Retailer']}")
    print(f"  Product Name: {row['Product Name'][:60] if isinstance(row['Product Name'], str) else row['Product Name']}...")
    print(f"  Brand: {row['Brand']}")
    print(f"  Price: ${row['Price']}")
    print(f"  Description: {row['Description'][:60] if isinstance(row['Description'], str) else row['Description']}...")

print("\n" + "=" * 70)
print("VERIFICATION COMPLETE")
print("=" * 70)
