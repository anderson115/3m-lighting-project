#!/usr/bin/env python3
"""
Validate Manual Scrape Data and Analyze Walmart Products
==========================================================

Purpose:
1. Confirm manual scrape data (Menards, Ace Hardware, Home Depot) is in master spreadsheet
2. Verify all product fields are populated for these retailers
3. Analyze category patterns from HD/Lowe's/Menards/Ace to establish "garage organizer" baseline
4. Review Walmart data for out-of-scope products
5. Report distribution of out-of-scope categories

Date: October 29, 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from collections import Counter, defaultdict

# File paths
MASTER_FILE = Path("modules/category-intelligence/04_CATEGORY_DATA_ALL_PRODUCTS_WEIGHTED.xlsx")
OUTPUT_DIR = Path("modules/category-intelligence/analysis")
OUTPUT_DIR.mkdir(exist_ok=True)

def load_master_data():
    """Load the master product spreadsheet"""
    print("Loading master product spreadsheet...")
    df = pd.read_excel(MASTER_FILE)
    print(f"Total products in master file: {len(df)}")
    return df

def validate_manual_scrape_data(df):
    """
    Validate that manual scrape data from Menards, Ace Hardware, Home Depot is present
    and all fields are populated
    """
    print("\n" + "="*80)
    print("STEP 1: VALIDATE MANUAL SCRAPE DATA")
    print("="*80)

    # Expected counts from manual scrape
    expected_counts = {
        'Menards': 246,
        'Acehardware': 94,
        'Homedepot': 94  # Additional manual scrape (not the original)
    }

    validation_results = {}

    for retailer, expected_count in expected_counts.items():
        print(f"\n--- {retailer} ---")

        # Get retailer data
        retailer_df = df[df['Retailer'].str.lower() == retailer.lower()]
        actual_count = len(retailer_df)

        print(f"Expected: {expected_count} products")
        print(f"Found: {actual_count} products")

        # Check if counts match
        count_match = actual_count >= expected_count
        if count_match:
            print(f"✅ Count validation: PASSED")
        else:
            print(f"⚠️ Count validation: FAILED (short by {expected_count - actual_count} products)")

        # Identify manual scrape products (have "manual_" prefix in Product Link)
        manual_scrape_df = retailer_df[retailer_df['Product Link'].str.startswith('manual_', na=False)]
        manual_count = len(manual_scrape_df)

        print(f"Manual scrape products (Product Link starts with 'manual_'): {manual_count}")

        # Use manual scrape products for field completeness check
        check_df = manual_scrape_df if manual_count > 0 else retailer_df

        # Check field completeness
        required_fields = ['Product Name', 'Brand', 'Price', 'Category', 'Subcategory']
        field_completeness = {}

        print(f"\nField Completeness (checking {len(check_df)} products):")
        for field in required_fields:
            if field in check_df.columns:
                non_null_count = check_df[field].notna().sum()
                completeness_pct = (non_null_count / len(check_df) * 100) if len(check_df) > 0 else 0
                field_completeness[field] = completeness_pct

                status = "✅" if completeness_pct >= 95 else "⚠️" if completeness_pct >= 80 else "❌"
                print(f"  {status} {field}: {completeness_pct:.1f}% complete ({non_null_count}/{len(check_df)})")
            else:
                field_completeness[field] = 0
                print(f"  ❌ {field}: Field not found")

        # Store validation results
        validation_results[retailer] = {
            'expected_count': expected_count,
            'actual_count': actual_count,
            'manual_scrape_count': manual_count,
            'count_match': count_match,
            'field_completeness': field_completeness,
            'avg_completeness': np.mean(list(field_completeness.values()))
        }

    # Overall validation summary
    print("\n" + "="*80)
    print("VALIDATION SUMMARY")
    print("="*80)

    total_expected = sum(expected_counts.values())
    total_actual = sum(r['actual_count'] for r in validation_results.values())

    print(f"\nTotal Expected: {total_expected} products")
    print(f"Total Found: {total_actual} products")
    print(f"Difference: {total_actual - total_expected} products")

    all_passed = all(r['count_match'] for r in validation_results.values())
    avg_completeness = np.mean([r['avg_completeness'] for r in validation_results.values()])

    if all_passed and avg_completeness >= 90:
        print(f"\n✅ Overall Status: PASSED")
        print(f"✅ Average Field Completeness: {avg_completeness:.1f}%")
    else:
        print(f"\n⚠️ Overall Status: NEEDS ATTENTION")
        print(f"⚠️ Average Field Completeness: {avg_completeness:.1f}%")

    return validation_results

def analyze_baseline_category_definition(df):
    """
    Analyze category patterns from HD, Lowe's, Menards, Ace Hardware
    to establish what constitutes a "garage organizer" product
    """
    print("\n" + "="*80)
    print("STEP 2: ESTABLISH CATEGORY BASELINE")
    print("="*80)
    print("\nAnalyzing category patterns from HD, Lowe's, Menards, Ace Hardware...")

    # Get baseline retailers
    baseline_retailers = ['Homedepot', 'Lowes', 'Menards', 'Acehardware']
    baseline_df = df[df['Retailer'].isin(baseline_retailers)]

    print(f"\nBaseline dataset: {len(baseline_df)} products from {len(baseline_retailers)} retailers")

    # Analyze categories
    category_dist = baseline_df['Category'].value_counts()
    category_pct = (category_dist / len(baseline_df) * 100).round(1)

    print("\n--- Category Distribution (Baseline Retailers) ---")
    for cat, count in category_dist.items():
        pct = category_pct[cat]
        print(f"  {cat}: {count} products ({pct}%)")

    # Analyze sub-segments
    subseg_dist = baseline_df['Subcategory'].value_counts()
    subseg_pct = (subseg_dist / len(baseline_df) * 100).round(1)

    print("\n--- Sub-Segment Distribution (Baseline Retailers) ---")
    for subseg, count in subseg_dist.head(15).items():
        pct = subseg_pct[subseg]
        print(f"  {subseg}: {count} products ({pct}%)")

    # Analyze brands to identify patterns
    brand_dist = baseline_df['Brand'].value_counts()

    print("\n--- Top 20 Brands (Baseline Retailers) ---")
    for brand, count in brand_dist.head(20).items():
        pct = (count / len(baseline_df) * 100)
        print(f"  {brand}: {count} products ({pct:.1f}%)")

    # Identify category keywords that define "garage organizer"
    # Extract common terms from product names
    product_names = baseline_df['Product Name'].dropna().str.lower()

    common_keywords = [
        'hook', 'hanger', 'shelf', 'shelving', 'storage', 'organizer',
        'rack', 'cabinet', 'bin', 'basket', 'wall', 'garage', 'mount',
        'overhead', 'utility', 'tool', 'workbench', 'pegboard', 'slatwall',
        'track', 'rail', 'panel', 'holder', 'bike', 'ladder', 'sports'
    ]

    keyword_counts = {}
    for keyword in common_keywords:
        count = product_names.str.contains(keyword, na=False).sum()
        if count > 0:
            keyword_counts[keyword] = count

    # Sort by frequency
    keyword_counts = dict(sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True))

    print("\n--- Common Keywords in Product Names (Baseline) ---")
    for keyword, count in list(keyword_counts.items())[:20]:
        pct = (count / len(baseline_df) * 100)
        print(f"  '{keyword}': {count} products ({pct:.1f}%)")

    # Store baseline definition
    baseline_definition = {
        'total_products': len(baseline_df),
        'categories': category_dist.to_dict(),
        'subsegments': subseg_dist.to_dict(),
        'brands': brand_dist.head(50).to_dict(),
        'keywords': keyword_counts,
        'retailers': baseline_retailers
    }

    return baseline_definition

def analyze_walmart_products(df, baseline_definition):
    """
    Analyze Walmart products against the baseline definition
    Identify out-of-scope products and their distribution
    """
    print("\n" + "="*80)
    print("STEP 3: ANALYZE WALMART PRODUCTS")
    print("="*80)

    walmart_df = df[df['Retailer'] == 'Walmart']
    print(f"\nTotal Walmart products: {len(walmart_df)}")

    # Category analysis
    walmart_categories = walmart_df['Category'].value_counts()
    walmart_cat_pct = (walmart_categories / len(walmart_df) * 100).round(1)

    print("\n--- Walmart Category Distribution ---")
    for cat, count in walmart_categories.items():
        pct = walmart_cat_pct[cat]
        baseline_pct = (baseline_definition['categories'].get(cat, 0) /
                       baseline_definition['total_products'] * 100)

        # Flag if category is not in baseline or significantly over-represented
        if baseline_pct == 0:
            flag = "❌ NOT IN BASELINE"
        elif pct > baseline_pct * 3:
            flag = f"⚠️ OVER-REPRESENTED (baseline: {baseline_pct:.1f}%)"
        else:
            flag = "✅ OK"

        print(f"  {cat}: {count} products ({pct}%) - {flag}")

    # Subcategory analysis
    walmart_subseg = walmart_df['Subcategory'].value_counts()
    walmart_subseg_pct = (walmart_subseg / len(walmart_df) * 100).round(1)

    print("\n--- Walmart Sub-Segment Distribution (Top 20) ---")
    baseline_subseg_total = sum(baseline_definition['subsegments'].values())

    for subseg, count in walmart_subseg.head(20).items():
        pct = walmart_subseg_pct[subseg]
        baseline_count = baseline_definition['subsegments'].get(subseg, 0)
        baseline_pct = (baseline_count / baseline_subseg_total * 100) if baseline_subseg_total > 0 else 0

        if baseline_pct == 0:
            flag = "❌ NOT IN BASELINE"
        elif pct > baseline_pct * 3:
            flag = f"⚠️ OVER-REP (baseline: {baseline_pct:.1f}%)"
        else:
            flag = "✅ OK"

        print(f"  {subseg}: {count} ({pct}%) - {flag}")

    # Keyword-based filtering
    # Check which Walmart products contain baseline keywords
    walmart_names = walmart_df['Product Name'].fillna('').str.lower()
    baseline_keywords = list(baseline_definition['keywords'].keys())[:15]  # Top 15 keywords

    # Products that match at least one baseline keyword
    keyword_matches = walmart_names.apply(
        lambda x: any(keyword in x for keyword in baseline_keywords)
    )

    in_scope_count = keyword_matches.sum()
    out_scope_count = len(walmart_df) - in_scope_count

    print("\n--- Keyword-Based Scope Analysis ---")
    print(f"Products matching baseline keywords: {in_scope_count} ({in_scope_count/len(walmart_df)*100:.1f}%)")
    print(f"Products NOT matching baseline keywords: {out_scope_count} ({out_scope_count/len(walmart_df)*100:.1f}%)")

    # Identify out-of-scope products
    out_of_scope_df = walmart_df[~keyword_matches].copy()

    print("\n" + "="*80)
    print("OUT-OF-SCOPE PRODUCTS ANALYSIS")
    print("="*80)

    if len(out_of_scope_df) > 0:
        print(f"\nTotal out-of-scope products: {len(out_of_scope_df)}")
        print(f"Percentage of Walmart dataset: {len(out_of_scope_df)/len(walmart_df)*100:.1f}%")

        # Category distribution of out-of-scope products
        oos_categories = out_of_scope_df['Category'].value_counts()
        print("\n--- Out-of-Scope Products by Category ---")
        for cat, count in oos_categories.items():
            pct = (count / len(out_of_scope_df) * 100)
            print(f"  {cat}: {count} products ({pct:.1f}%)")

        # Subcategory distribution of out-of-scope products
        oos_subseg = out_of_scope_df['Subcategory'].value_counts()
        print("\n--- Out-of-Scope Products by Sub-Segment (Top 20) ---")
        for subseg, count in oos_subseg.head(20).items():
            pct = (count / len(out_of_scope_df) * 100)
            print(f"  {subseg}: {count} products ({pct:.1f}%)")

        # Sample out-of-scope product names
        print("\n--- Sample Out-of-Scope Product Names (20 examples) ---")
        sample_products = out_of_scope_df[['Product Name', 'Category', 'Subcategory']].head(20)
        for idx, row in sample_products.iterrows():
            print(f"  - {row['Product Name'][:60]}... | {row['Category']} | {row['Subcategory']}")

        # Save out-of-scope products to file
        out_scope_file = OUTPUT_DIR / "walmart_out_of_scope_products.xlsx"
        out_of_scope_df.to_excel(out_scope_file, index=False)
        print(f"\n✅ Out-of-scope products saved to: {out_scope_file}")
    else:
        print("\n✅ All Walmart products appear to be in scope!")

    # Analysis summary
    analysis_summary = {
        'walmart_total': len(walmart_df),
        'in_scope_count': int(in_scope_count),
        'out_scope_count': int(out_scope_count),
        'out_scope_percentage': float(out_scope_count / len(walmart_df) * 100),
        'category_distribution': walmart_categories.to_dict(),
        'out_scope_categories': oos_categories.to_dict() if len(out_of_scope_df) > 0 else {},
        'out_scope_subsegments': oos_subseg.head(20).to_dict() if len(out_of_scope_df) > 0 else {}
    }

    return analysis_summary, out_of_scope_df

def generate_recommendations(validation_results, baseline_definition, walmart_analysis):
    """Generate recommendations based on the analysis"""
    print("\n" + "="*80)
    print("RECOMMENDATIONS")
    print("="*80)

    recommendations = []

    # Check manual scrape validation
    avg_completeness = np.mean([r['avg_completeness'] for r in validation_results.values()])
    if avg_completeness < 90:
        recommendations.append({
            'priority': 'HIGH',
            'area': 'Data Completeness',
            'issue': f'Manual scrape data has {avg_completeness:.1f}% average field completeness',
            'action': 'Review and fill missing fields for Menards, Ace Hardware, Home Depot'
        })

    # Check Walmart out-of-scope
    if walmart_analysis['out_scope_count'] > 0:
        out_scope_pct = walmart_analysis['out_scope_percentage']

        if out_scope_pct > 20:
            priority = 'HIGH'
        elif out_scope_pct > 10:
            priority = 'MEDIUM'
        else:
            priority = 'LOW'

        recommendations.append({
            'priority': priority,
            'area': 'Walmart Data Filtering',
            'issue': f'{walmart_analysis["out_scope_count"]} Walmart products ({out_scope_pct:.1f}%) appear out-of-scope',
            'action': 'Review and filter out products that do not match "garage organizer" definition'
        })

    # Print recommendations
    if recommendations:
        print("\n")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. [{rec['priority']} PRIORITY] {rec['area']}")
            print(f"   Issue: {rec['issue']}")
            print(f"   Action: {rec['action']}")
            print()
    else:
        print("\n✅ No critical issues found. Data quality looks good!")

    return recommendations

def main():
    """Main execution function"""
    print("="*80)
    print("VALIDATE MANUAL SCRAPE DATA & ANALYZE WALMART PRODUCTS")
    print("="*80)

    # Load data
    df = load_master_data()

    # Step 1: Validate manual scrape data
    validation_results = validate_manual_scrape_data(df)

    # Step 2: Establish baseline category definition
    baseline_definition = analyze_baseline_category_definition(df)

    # Step 3: Analyze Walmart products
    walmart_analysis, out_of_scope_df = analyze_walmart_products(df, baseline_definition)

    # Step 4: Generate recommendations
    recommendations = generate_recommendations(validation_results, baseline_definition, walmart_analysis)

    # Save summary report
    summary_report = {
        'validation_results': validation_results,
        'baseline_definition': {
            'total_products': baseline_definition['total_products'],
            'category_count': len(baseline_definition['categories']),
            'top_categories': dict(list(baseline_definition['categories'].items())[:10])
        },
        'walmart_analysis': walmart_analysis,
        'recommendations': recommendations
    }

    # Convert numpy types for JSON serialization
    def convert_to_native(obj):
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: convert_to_native(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_native(item) for item in obj]
        return obj

    summary_report = convert_to_native(summary_report)

    summary_file = OUTPUT_DIR / "validation_and_walmart_analysis_summary.json"
    with open(summary_file, 'w') as f:
        json.dump(summary_report, f, indent=2)

    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print(f"\n✅ Summary report saved to: {summary_file}")
    if len(out_of_scope_df) > 0:
        print(f"✅ Out-of-scope products saved to: {OUTPUT_DIR / 'walmart_out_of_scope_products.xlsx'}")
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
