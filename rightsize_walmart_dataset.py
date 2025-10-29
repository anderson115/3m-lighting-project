#!/usr/bin/env python3
"""
Rightsize Walmart Dataset Without Website Scrape
================================================

Purpose:
1. Load existing Walmart products from master spreadsheet
2. Apply intelligent filtering based on data quality and engagement
3. Rightsize to ~1,500 products to match HD/Lowe's scope
4. Prioritize products with ratings, reviews, and complete data
5. Create cleaned Walmart dataset that mirrors market realities

Date: October 29, 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

# File paths
MASTER_FILE = Path("modules/category-intelligence/04_CATEGORY_DATA_ALL_PRODUCTS_WEIGHTED.xlsx")
OUTPUT_DIR = Path("modules/category-intelligence/analysis")
OUTPUT_DIR.mkdir(exist_ok=True)

def analyze_walmart_current_state(walmart_df):
    """
    Analyze current Walmart dataset
    """
    print("="*80)
    print("CURRENT WALMART DATASET ANALYSIS")
    print("="*80)

    print(f"\nTotal Walmart products: {len(walmart_df)}")

    # Category distribution
    print(f"\nCategory distribution:")
    cat_dist = walmart_df['Category'].value_counts()
    for cat, count in cat_dist.head(10).items():
        pct = (count / len(walmart_df) * 100)
        print(f"  {cat}: {count} ({pct:.1f}%)")

    # Data completeness
    print(f"\nData completeness:")
    fields = ['Product Name', 'Brand', 'Price', 'Star Rating', 'Review Count', 'Category', 'Subcategory']
    for field in fields:
        if field in walmart_df.columns:
            complete = walmart_df[field].notna().sum()
            pct = (complete / len(walmart_df) * 100)
            print(f"  {field}: {complete}/{len(walmart_df)} ({pct:.1f}%)")

    # Price distribution
    if 'Price' in walmart_df.columns:
        print(f"\nPrice statistics:")
        print(f"  Average: ${walmart_df['Price'].mean():.2f}")
        print(f"  Median: ${walmart_df['Price'].median():.2f}")
        print(f"  Min: ${walmart_df['Price'].min():.2f}")
        print(f"  Max: ${walmart_df['Price'].max():.2f}")

    # Rating distribution
    if 'Star Rating' in walmart_df.columns:
        rated_count = walmart_df['Star Rating'].notna().sum()
        print(f"\nProducts with ratings: {rated_count} ({rated_count/len(walmart_df)*100:.1f}%)")
        if rated_count > 0:
            print(f"  Average rating: {walmart_df['Star Rating'].mean():.2f}")

    # Review distribution
    if 'Review Count' in walmart_df.columns:
        reviewed_count = walmart_df['Review Count'].notna().sum()
        print(f"\nProducts with reviews: {reviewed_count} ({reviewed_count/len(walmart_df)*100:.1f}%)")
        if reviewed_count > 0:
            print(f"  Average review count: {walmart_df['Review Count'].mean():.1f}")
            print(f"  Median review count: {walmart_df['Review Count'].median():.1f}")

def score_walmart_products(walmart_df):
    """
    Score Walmart products based on data quality and engagement
    """
    print("\n" + "="*80)
    print("SCORING WALMART PRODUCTS")
    print("="*80)

    walmart_scored = walmart_df.copy()
    walmart_scored['priority_score'] = 0

    # Score products based on multiple factors

    # 1. Has rating (indicates active product with customer feedback)
    if 'Star Rating' in walmart_scored.columns:
        has_rating = walmart_scored['Star Rating'].notna()
        walmart_scored.loc[has_rating, 'priority_score'] += 3
        print(f"\n+3 points for having rating: {has_rating.sum()} products")

    # 2. Has reviews (indicates customer engagement)
    if 'Review Count' in walmart_scored.columns:
        has_reviews = walmart_scored['Review Count'].notna()
        walmart_scored.loc[has_reviews, 'priority_score'] += 2
        print(f"+2 points for having reviews: {has_reviews.sum()} products")

        # 3. High engagement (>10 reviews)
        high_engagement = walmart_scored['Review Count'] > 10
        walmart_scored.loc[high_engagement, 'priority_score'] += 2
        print(f"+2 points for >10 reviews: {high_engagement.sum()} products")

        # 4. Very high engagement (>50 reviews)
        very_high = walmart_scored['Review Count'] > 50
        walmart_scored.loc[very_high, 'priority_score'] += 2
        print(f"+2 points for >50 reviews: {very_high.sum()} products")

    # 5. Has category data (better organized)
    if 'Category' in walmart_scored.columns:
        has_category = walmart_scored['Category'].notna()
        walmart_scored.loc[has_category, 'priority_score'] += 2
        print(f"+2 points for having category: {has_category.sum()} products")

    # 6. Has brand data
    if 'Brand' in walmart_scored.columns:
        has_brand = walmart_scored['Brand'].notna()
        walmart_scored.loc[has_brand, 'priority_score'] += 1
        print(f"+1 point for having brand: {has_brand.sum()} products")

    # 7. Has subcategory (most detailed)
    if 'Subcategory' in walmart_scored.columns:
        has_subcat = walmart_scored['Subcategory'].notna()
        walmart_scored.loc[has_subcat, 'priority_score'] += 1
        print(f"+1 point for having subcategory: {has_subcat.sum()} products")

    # 8. High rating (4+ stars indicates quality)
    if 'Star Rating' in walmart_scored.columns:
        high_rating = walmart_scored['Star Rating'] >= 4.0
        walmart_scored.loc[high_rating, 'priority_score'] += 1
        print(f"+1 point for 4+ star rating: {high_rating.sum()} products")

    print(f"\nPriority score distribution:")
    print(walmart_scored['priority_score'].describe())

    return walmart_scored

def rightsize_walmart(walmart_scored, target_size=1500):
    """
    Rightsize Walmart dataset to target size
    """
    print("\n" + "="*80)
    print("RIGHTSIZING WALMART DATASET")
    print("="*80)

    print(f"\nCurrent size: {len(walmart_scored)}")
    print(f"Target size: {target_size}")
    print(f"Products to remove: {len(walmart_scored) - target_size}")

    # Sort by priority score
    walmart_sorted = walmart_scored.sort_values('priority_score', ascending=False)

    # Keep top N
    walmart_final = walmart_sorted.head(target_size).copy()
    walmart_removed = walmart_sorted.iloc[target_size:].copy()

    print(f"\nKept: {len(walmart_final)} products")
    print(f"Removed: {len(walmart_removed)} products")

    # Analyze what was kept vs removed
    print(f"\nKept products - priority score stats:")
    print(walmart_final['priority_score'].describe())

    print(f"\nRemoved products - priority score stats:")
    print(walmart_removed['priority_score'].describe())

    # Category distribution after filtering
    if 'Category' in walmart_final.columns:
        print(f"\nKept products - category distribution:")
        cat_dist = walmart_final['Category'].value_counts().head(10)
        for cat, count in cat_dist.items():
            pct = (count / len(walmart_final) * 100)
            print(f"  {cat}: {count} ({pct:.1f}%)")

    # Price comparison
    if 'Price' in walmart_final.columns:
        print(f"\nPrice comparison:")
        print(f"  Kept avg: ${walmart_final['Price'].mean():.2f}")
        print(f"  Removed avg: ${walmart_removed['Price'].mean():.2f}")
        print(f"  Difference: ${walmart_final['Price'].mean() - walmart_removed['Price'].mean():.2f}")

    return walmart_final, walmart_removed

def compare_to_baseline(walmart_final, master_df):
    """
    Compare final Walmart dataset to baseline retailers
    """
    print("\n" + "="*80)
    print("COMPARISON TO BASELINE RETAILERS")
    print("="*80)

    # Get baseline (HD, Lowe's, Menards, Ace)
    baseline_retailers = ['Homedepot', 'Lowes', 'Menards', 'Acehardware']
    baseline_df = master_df[master_df['Retailer'].isin(baseline_retailers)]

    print(f"\nDataset sizes:")
    print(f"  Walmart (cleaned): {len(walmart_final)}")
    print(f"  Baseline: {len(baseline_df)}")
    print(f"  Ratio: {len(walmart_final) / len(baseline_df):.2f}x")

    # Price comparison
    if 'Price' in walmart_final.columns and 'Price' in baseline_df.columns:
        walmart_avg = walmart_final['Price'].mean()
        baseline_avg = baseline_df['Price'].mean()
        print(f"\nAverage price:")
        print(f"  Walmart: ${walmart_avg:.2f}")
        print(f"  Baseline: ${baseline_avg:.2f}")
        print(f"  Difference: ${walmart_avg - baseline_avg:.2f} ({((walmart_avg/baseline_avg - 1)*100):.1f}%)")

    # Category comparison
    if 'Category' in walmart_final.columns and 'Category' in baseline_df.columns:
        print(f"\nCategory distribution comparison:")
        walmart_cats = walmart_final['Category'].value_counts(normalize=True) * 100
        baseline_cats = baseline_df['Category'].value_counts(normalize=True) * 100

        all_cats = set(walmart_cats.index) | set(baseline_cats.index)
        for cat in sorted(all_cats, key=lambda x: baseline_cats.get(x, 0), reverse=True)[:10]:
            wm_pct = walmart_cats.get(cat, 0)
            bl_pct = baseline_cats.get(cat, 0)
            diff = wm_pct - bl_pct
            print(f"  {cat}:")
            print(f"    Walmart: {wm_pct:.1f}% | Baseline: {bl_pct:.1f}% | Diff: {diff:+.1f}pp")

def create_updated_master(master_df, walmart_final):
    """
    Create updated master dataset with cleaned Walmart products
    """
    print("\n" + "="*80)
    print("CREATING UPDATED MASTER DATASET")
    print("="*80)

    # Remove old Walmart products
    master_without_walmart = master_df[master_df['Retailer'] != 'Walmart'].copy()

    # Add cleaned Walmart products
    master_updated = pd.concat([master_without_walmart, walmart_final], ignore_index=True)

    print(f"\nOriginal master: {len(master_df)} products")
    print(f"  Walmart products: {len(master_df[master_df['Retailer'] == 'Walmart'])}")
    print(f"  Other retailers: {len(master_without_walmart)}")

    print(f"\nUpdated master: {len(master_updated)} products")
    print(f"  Walmart products: {len(walmart_final)}")
    print(f"  Other retailers: {len(master_without_walmart)}")
    print(f"  Net change: {len(master_updated) - len(master_df):+d} products")

    # Retailer distribution
    print(f"\nRetailer distribution (updated):")
    retailer_dist = master_updated['Retailer'].value_counts()
    for retailer, count in retailer_dist.items():
        pct = (count / len(master_updated) * 100)
        print(f"  {retailer}: {count} ({pct:.1f}%)")

    return master_updated

def main():
    """Main execution"""
    print("="*80)
    print("WALMART DATASET RIGHTSIZING")
    print("="*80)
    print("\nStrategy: Prioritize high-engagement, well-documented products")
    print("Target: ~1,500 products (comparable to HD/Lowe's baseline)")

    # Load master dataset
    print(f"\nLoading master dataset: {MASTER_FILE}")
    master_df = pd.read_excel(MASTER_FILE)
    print(f"Total products: {len(master_df)}")

    # Get Walmart products
    walmart_df = master_df[master_df['Retailer'] == 'Walmart'].copy()

    # Analyze current state
    analyze_walmart_current_state(walmart_df)

    # Score products
    walmart_scored = score_walmart_products(walmart_df)

    # Rightsize
    walmart_final, walmart_removed = rightsize_walmart(walmart_scored, target_size=1500)

    # Compare to baseline
    compare_to_baseline(walmart_final, master_df)

    # Create updated master
    master_updated = create_updated_master(master_df, walmart_final)

    # Save outputs
    print("\n" + "="*80)
    print("SAVING OUTPUT FILES")
    print("="*80)

    # Save cleaned Walmart dataset
    output_walmart = OUTPUT_DIR / "walmart_cleaned_rightsized.xlsx"
    walmart_final.to_excel(output_walmart, index=False)
    print(f"\n✅ Cleaned Walmart dataset: {output_walmart}")

    # Save removed products
    output_removed = OUTPUT_DIR / "walmart_removed_products.xlsx"
    walmart_removed.to_excel(output_removed, index=False)
    print(f"✅ Removed products: {output_removed}")

    # Save updated master
    output_master = Path("modules/category-intelligence/04_CATEGORY_DATA_RIGHTSIZED.xlsx")
    master_updated.to_excel(output_master, index=False)
    print(f"✅ Updated master dataset: {output_master}")

    # Save summary statistics
    summary = {
        "timestamp": pd.Timestamp.now().isoformat(),
        "original_walmart_count": len(walmart_df),
        "final_walmart_count": len(walmart_final),
        "removed_count": len(walmart_removed),
        "original_total": len(master_df),
        "final_total": len(master_updated),
        "scoring_criteria": {
            "has_rating": "+3 points",
            "has_reviews": "+2 points",
            "high_engagement_10": "+2 points",
            "high_engagement_50": "+2 points",
            "has_category": "+2 points",
            "has_brand": "+1 point",
            "has_subcategory": "+1 point",
            "high_rating_4plus": "+1 point"
        },
        "kept_score_stats": {
            "mean": float(walmart_final['priority_score'].mean()),
            "median": float(walmart_final['priority_score'].median()),
            "min": int(walmart_final['priority_score'].min()),
            "max": int(walmart_final['priority_score'].max())
        },
        "removed_score_stats": {
            "mean": float(walmart_removed['priority_score'].mean()),
            "median": float(walmart_removed['priority_score'].median()),
            "min": int(walmart_removed['priority_score'].min()),
            "max": int(walmart_removed['priority_score'].max())
        }
    }

    summary_file = OUTPUT_DIR / "walmart_rightsizing_summary.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"✅ Summary statistics: {summary_file}")

    print("\n" + "="*80)
    print("✅ WALMART RIGHTSIZING COMPLETE")
    print("="*80)
    print(f"\nWalmart products: {len(walmart_df)} → {len(walmart_final)} ({len(walmart_removed)} removed)")
    print(f"Total products: {len(master_df)} → {len(master_updated)}")
    print(f"\nNext steps:")
    print("1. Review removed products in walmart_removed_products.xlsx")
    print("2. Validate category distribution matches market reality")
    print("3. Use updated master dataset for analysis: 04_CATEGORY_DATA_RIGHTSIZED.xlsx")

if __name__ == "__main__":
    main()
