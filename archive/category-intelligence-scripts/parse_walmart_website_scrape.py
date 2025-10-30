#!/usr/bin/env python3
"""
Parse Walmart Website Scrape and Merge with Existing Data
==========================================================

Purpose:
1. Parse manually scraped Walmart.com product listings
2. Match to existing Walmart products in master spreadsheet
3. Prioritize website-scraped products (current inventory)
4. Rightsize Walmart dataset to match HD/Lowe's scope (~1,500 products)
5. Apply filters to remove discontinued or out-of-scope products

Date: October 29, 2025
"""

import pandas as pd
import numpy as np
import re
from pathlib import Path
import json
from collections import Counter

# File paths
MASTER_FILE = Path("modules/category-intelligence/04_CATEGORY_DATA_ALL_PRODUCTS_WEIGHTED.xlsx")
WEBSITE_SCRAPE_FILE = Path("walmart_website_scrape.txt")  # User will need to save the HTML/text
OUTPUT_DIR = Path("modules/category-intelligence/analysis")
OUTPUT_DIR.mkdir(exist_ok=True)

def parse_walmart_website_scrape(scrape_text):
    """
    Parse the Walmart website scrape text to extract product information
    """
    print("="*80)
    print("PARSING WALMART WEBSITE SCRAPE")
    print("="*80)

    products = []

    # Pattern to extract product information
    # Looking for patterns like:
    # Product Name
    # $XX.XX or Now$XX.XX
    # X reviews, X.X stars

    lines = scrape_text.split('\n')

    current_product = {}
    price_pattern = r'\$(\d+)\.?(\d{2})?'
    rating_pattern = r'(\d+\.?\d*) out of 5 Stars'
    review_pattern = r'(\d+) reviews?'

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines and navigation
        if not line or line in ['Options', 'Add', 'Sponsored', 'Best seller', 'Rollback', 'Clearance']:
            i += 1
            continue

        # Look for price patterns
        price_match = re.search(r'Now\$(\d+)\.(\d{2})|current price.*?\$(\d+)\.(\d{2})|^\$(\d+)\.(\d{2})', line)
        if price_match:
            groups = [g for g in price_match.groups() if g is not None]
            if len(groups) >= 2:
                dollars = groups[0]
                cents = groups[1]
                price = float(f"{dollars}.{cents}")

                # Look back for product name (usually 1-3 lines before price)
                for j in range(max(0, i-5), i):
                    potential_name = lines[j].strip()
                    # Product names are usually longer and contain descriptive text
                    if len(potential_name) > 20 and not re.search(r'^\$|current price|variant on', potential_name):
                        # Look ahead for ratings
                        rating = None
                        review_count = None
                        for k in range(i, min(i+10, len(lines))):
                            rating_match = re.search(rating_pattern, lines[k])
                            if rating_match:
                                rating = float(rating_match.group(1))
                            review_match = re.search(review_pattern, lines[k])
                            if review_match:
                                review_count = int(review_match.group(1))
                            if rating and review_count:
                                break

                        products.append({
                            'Product Name': potential_name,
                            'Price': price,
                            'Star Rating': rating,
                            'Review Count': review_count,
                            'Source': 'website_scrape'
                        })
                        break

        i += 1

    print(f"Extracted {len(products)} products from website scrape")

    # Remove duplicates based on product name
    seen_names = set()
    unique_products = []
    for product in products:
        name = product['Product Name']
        if name not in seen_names:
            seen_names.add(name)
            unique_products.append(product)

    print(f"After deduplication: {len(unique_products)} unique products")

    return pd.DataFrame(unique_products)

def match_walmart_products(master_df, website_df):
    """
    Match website-scraped products to existing master dataset
    """
    print("\n" + "="*80)
    print("MATCHING WALMART PRODUCTS")
    print("="*80)

    # Get existing Walmart products
    walmart_existing = master_df[master_df['Retailer'] == 'Walmart'].copy()
    print(f"\nExisting Walmart products in master: {len(walmart_existing)}")
    print(f"Website-scraped products: {len(website_df)}")

    # Try to match based on product name similarity
    matches = []
    unmatched_website = []
    unmatched_existing = walmart_existing.copy()

    for idx, web_product in website_df.iterrows():
        web_name = web_product['Product Name'].lower()
        web_price = web_product['Price']

        # Look for exact or close matches in existing data
        match_found = False
        for ex_idx, ex_product in unmatched_existing.iterrows():
            ex_name = str(ex_product['Product Name']).lower()
            ex_price = ex_product.get('Price', None)

            # Check for name similarity and price match
            if pd.notna(ex_price):
                # Simple matching: if price is within $1 and name has 50%+ word overlap
                price_diff = abs(float(web_price) - float(ex_price))

                # Calculate word overlap
                web_words = set(web_name.split())
                ex_words = set(ex_name.split())
                overlap = len(web_words & ex_words) / len(web_words | ex_words) if len(web_words | ex_words) > 0 else 0

                if price_diff <= 1.0 and overlap >= 0.3:
                    # Match found
                    matches.append({
                        'website_product': web_product.to_dict(),
                        'existing_product': ex_product.to_dict(),
                        'match_score': overlap
                    })
                    unmatched_existing = unmatched_existing.drop(ex_idx)
                    match_found = True
                    break

        if not match_found:
            unmatched_website.append(web_product.to_dict())

    print(f"\nMatching results:")
    print(f"  Matched products: {len(matches)}")
    print(f"  Website products without match: {len(unmatched_website)}")
    print(f"  Existing products without match: {len(unmatched_existing)} (likely discontinued)")

    return matches, unmatched_website, unmatched_existing

def create_cleaned_walmart_dataset(master_df, matches, unmatched_website, unmatched_existing):
    """
    Create a cleaned Walmart dataset prioritizing website-scraped products
    """
    print("\n" + "="*80)
    print("CREATING CLEANED WALMART DATASET")
    print("="*80)

    # Strategy:
    # 1. Keep matched products (prioritize website price/rating, keep other fields from master)
    # 2. Add unmatched website products (new products)
    # 3. Flag unmatched existing products as potentially discontinued
    # 4. Rightsize to ~1,500 products to match HD/Lowe's

    cleaned_products = []

    # Add matched products (priority: website data)
    for match in matches:
        web_prod = match['website_product']
        ex_prod = match['existing_product']

        # Merge: prioritize website fields, keep existing fields for details
        merged = ex_prod.copy()
        merged['Price'] = web_prod['Price']
        if pd.notna(web_prod['Star Rating']):
            merged['Star Rating'] = web_prod['Star Rating']
        if pd.notna(web_prod['Review Count']):
            merged['Review Count'] = web_prod['Review Count']
        merged['Source'] = 'website_matched'
        merged['Match_Score'] = match['match_score']

        cleaned_products.append(merged)

    print(f"\nAdded {len(cleaned_products)} matched products")

    # Add unmatched website products as new
    for web_prod in unmatched_website:
        new_product = {
            'Retailer': 'Walmart',
            'Product Name': web_prod['Product Name'],
            'Price': web_prod['Price'],
            'Star Rating': web_prod.get('Star Rating'),
            'Review Count': web_prod.get('Review Count'),
            'Source': 'website_new'
        }
        cleaned_products.append(new_product)

    print(f"Added {len(unmatched_website)} new website products")

    # Convert to DataFrame
    walmart_cleaned = pd.DataFrame(cleaned_products)

    print(f"\nTotal Walmart products after merge: {len(walmart_cleaned)}")

    # Analyze unmatched existing (potentially discontinued)
    discontinued_df = unmatched_existing.copy()
    discontinued_df['Status'] = 'potentially_discontinued'

    return walmart_cleaned, discontinued_df

def rightsize_walmart_dataset(walmart_df, target_size=1500):
    """
    Rightsize Walmart dataset to target size (~1,500 products like HD/Lowe's)
    """
    print("\n" + "="*80)
    print("RIGHTSIZING WALMART DATASET")
    print("="*80)

    print(f"\nCurrent Walmart products: {len(walmart_df)}")
    print(f"Target size: {target_size}")

    if len(walmart_df) <= target_size:
        print("Dataset is already at or below target size. No filtering needed.")
        return walmart_df, None

    # Prioritization strategy:
    # 1. Keep products with ratings and reviews (active products)
    # 2. Keep products with category data
    # 3. Remove products without key data
    # 4. Sample if still too large

    walmart_scored = walmart_df.copy()
    walmart_scored['priority_score'] = 0

    # Score products
    walmart_scored.loc[walmart_scored['Star Rating'].notna(), 'priority_score'] += 3
    walmart_scored.loc[walmart_scored['Review Count'].notna(), 'priority_score'] += 2
    walmart_scored.loc[walmart_scored['Review Count'] > 10, 'priority_score'] += 2
    walmart_scored.loc[walmart_scored['Review Count'] > 50, 'priority_score'] += 2
    walmart_scored.loc[walmart_scored['Category'].notna(), 'priority_score'] += 2
    walmart_scored.loc[walmart_scored['Brand'].notna(), 'priority_score'] += 1
    walmart_scored.loc[walmart_scored['Source'] == 'website_matched', 'priority_score'] += 2

    # Sort by priority score
    walmart_scored = walmart_scored.sort_values('priority_score', ascending=False)

    # Keep top N
    walmart_final = walmart_scored.head(target_size).copy()
    walmart_removed = walmart_scored.iloc[target_size:].copy()

    print(f"\nAfter rightsizing:")
    print(f"  Kept: {len(walmart_final)} products")
    print(f"  Removed: {len(walmart_removed)} products")

    # Distribution after filtering
    print(f"\nKept products by source:")
    print(walmart_final['Source'].value_counts())

    print(f"\nAverage priority score of kept products: {walmart_final['priority_score'].mean():.1f}")
    print(f"Average priority score of removed products: {walmart_removed['priority_score'].mean():.1f}")

    return walmart_final, walmart_removed

def analyze_walmart_cleaned(walmart_df, baseline_df):
    """
    Analyze the cleaned Walmart dataset compared to baseline
    """
    print("\n" + "="*80)
    print("ANALYSIS: CLEANED WALMART DATASET")
    print("="*80)

    # Compare to baseline
    print(f"\nDataset sizes:")
    print(f"  Walmart (cleaned): {len(walmart_df)}")
    print(f"  Baseline (HD/Lowe's/Menards/Ace): {len(baseline_df)}")
    print(f"  Ratio: {len(walmart_df) / len(baseline_df):.2f}x")

    # Price comparison
    walmart_avg_price = walmart_df['Price'].mean()
    baseline_avg_price = baseline_df['Price'].mean()

    print(f"\nAverage prices:")
    print(f"  Walmart: ${walmart_avg_price:.2f}")
    print(f"  Baseline: ${baseline_avg_price:.2f}")
    print(f"  Difference: ${walmart_avg_price - baseline_avg_price:.2f}")

    # Category distribution
    if 'Category' in walmart_df.columns:
        walmart_cats = walmart_df['Category'].value_counts().head(10)
        print(f"\nTop 10 Walmart categories:")
        for cat, count in walmart_cats.items():
            pct = (count / len(walmart_df) * 100)
            print(f"  {cat}: {count} ({pct:.1f}%)")

def main():
    """Main execution"""
    print("="*80)
    print("WALMART WEBSITE SCRAPE PARSER AND MERGER")
    print("="*80)

    # Check if website scrape file exists
    if not WEBSITE_SCRAPE_FILE.exists():
        print(f"\n❌ ERROR: Website scrape file not found: {WEBSITE_SCRAPE_FILE}")
        print("\nPlease save the Walmart website scrape to 'walmart_website_scrape.txt'")
        print("For now, I'll create a placeholder and show you what the script does.")
        return

    # Load master dataset
    print("\nLoading master dataset...")
    master_df = pd.read_excel(MASTER_FILE)
    print(f"Total products: {len(master_df)}")

    # Parse website scrape
    website_scrape_text = WEBSITE_SCRAPE_FILE.read_text()
    website_df = parse_walmart_website_scrape(website_scrape_text)

    # Match products
    matches, unmatched_website, unmatched_existing = match_walmart_products(master_df, website_df)

    # Create cleaned dataset
    walmart_cleaned, discontinued_df = create_cleaned_walmart_dataset(
        master_df, matches, unmatched_website, unmatched_existing
    )

    # Rightsize to target
    walmart_final, walmart_removed = rightsize_walmart_dataset(walmart_cleaned, target_size=1500)

    # Get baseline for comparison
    baseline_retailers = ['Homedepot', 'Lowes', 'Menards', 'Acehardware']
    baseline_df = master_df[master_df['Retailer'].isin(baseline_retailers)]

    # Analyze cleaned dataset
    analyze_walmart_cleaned(walmart_final, baseline_df)

    # Save outputs
    walmart_final.to_excel(OUTPUT_DIR / "walmart_cleaned_final.xlsx", index=False)
    walmart_removed.to_excel(OUTPUT_DIR / "walmart_removed_products.xlsx", index=False)
    discontinued_df.to_excel(OUTPUT_DIR / "walmart_potentially_discontinued.xlsx", index=False)

    print("\n" + "="*80)
    print("FILES SAVED")
    print("="*80)
    print(f"✅ Cleaned Walmart dataset: {OUTPUT_DIR / 'walmart_cleaned_final.xlsx'}")
    print(f"✅ Removed products: {OUTPUT_DIR / 'walmart_removed_products.xlsx'}")
    print(f"✅ Potentially discontinued: {OUTPUT_DIR / 'walmart_potentially_discontinued.xlsx'}")

    # Create updated master dataset
    print("\n" + "="*80)
    print("CREATING UPDATED MASTER DATASET")
    print("="*80)

    # Remove old Walmart products, add cleaned ones
    master_without_walmart = master_df[master_df['Retailer'] != 'Walmart']
    master_updated = pd.concat([master_without_walmart, walmart_final], ignore_index=True)

    print(f"\nOriginal master dataset: {len(master_df)} products")
    print(f"Updated master dataset: {len(master_updated)} products")
    print(f"  Removed Walmart products: {len(master_df) - len(master_without_walmart)}")
    print(f"  Added cleaned Walmart products: {len(walmart_final)}")
    print(f"  Net change: {len(master_updated) - len(master_df)}")

    # Save updated master
    updated_master_file = Path("modules/category-intelligence/04_CATEGORY_DATA_ALL_PRODUCTS_CLEANED.xlsx")
    master_updated.to_excel(updated_master_file, index=False)
    print(f"\n✅ Updated master dataset saved: {updated_master_file}")

if __name__ == "__main__":
    main()
