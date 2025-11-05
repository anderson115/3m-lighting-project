#!/usr/bin/env python3
"""
Analyze Walmart Over-Sampling in Product Dataset
Investigate why Walmart represents 78.5% of products vs ~15% market revenue
"""

import json
import pandas as pd
from collections import Counter, defaultdict
import re

print("=" * 80)
print("WALMART OVER-SAMPLING ROOT CAUSE ANALYSIS")
print("=" * 80)
print()

# Load data files
print("📁 Loading data files...")
with open('data/retailers/walmart_products.json', 'r') as f:
    walmart = json.load(f)

with open('data/retailers/homedepot_products.json', 'r') as f:
    homedepot = json.load(f)

with open('data/retailers/all_products_final_with_lowes.json', 'r') as f:
    all_products = json.load(f)

print(f"   Walmart: {len(walmart)} products")
print(f"   Home Depot: {len(homedepot)} products")
print(f"   All products: {len(all_products)} products")
print()

# ============================================================================
# HYPOTHESIS 1: Category Definition Too Broad
# ============================================================================
print("=" * 80)
print("HYPOTHESIS 1: Category Definition Too Broad for Walmart")
print("=" * 80)
print()

def extract_categories(products, source_name):
    """Extract and analyze category distribution"""
    categories = []
    subcategories = []

    for p in products:
        if isinstance(p.get('category'), str):
            categories.append(p['category'])
        if 'subcategory' in p and p['subcategory']:
            subcategories.append(p['subcategory'])

    cat_counts = Counter(categories)
    subcat_counts = Counter(subcategories)

    print(f"\n{source_name} - Top Categories:")
    for cat, count in cat_counts.most_common(10):
        pct = (count / len(products)) * 100
        print(f"   {cat}: {count} ({pct:.1f}%)")

    if subcat_counts:
        print(f"\n{source_name} - Top Subcategories:")
        for subcat, count in subcat_counts.most_common(10):
            pct = (count / len(products)) * 100
            print(f"   {subcat}: {count} ({pct:.1f}%)")

    return cat_counts, subcat_counts

walmart_cats, walmart_subcats = extract_categories(walmart, "WALMART")
homedepot_cats, homedepot_subcats = extract_categories(homedepot, "HOME DEPOT")

# Identify categories in Walmart but not Home Depot
walmart_only_cats = set(walmart_cats.keys()) - set(homedepot_cats.keys())
if walmart_only_cats:
    print(f"\n⚠️  WALMART-ONLY CATEGORIES (not in Home Depot):")
    for cat in walmart_only_cats:
        count = walmart_cats[cat]
        pct = (count / len(walmart)) * 100
        print(f"   {cat}: {count} products ({pct:.1f}% of Walmart)")

print()

# ============================================================================
# HYPOTHESIS 2: Too Many 3rd Party Resellers
# ============================================================================
print("=" * 80)
print("HYPOTHESIS 2: Too Many 3rd Party Resellers")
print("=" * 80)
print()

def analyze_sellers(products, source_name):
    """Analyze seller/brand distribution"""
    sellers = []
    brands = []

    for p in products:
        if 'seller' in p and p['seller']:
            sellers.append(p['seller'])
        if 'brand' in p and p['brand']:
            brands.append(p['brand'])

    seller_counts = Counter(sellers)
    brand_counts = Counter(brands)

    print(f"\n{source_name} - Seller Analysis:")
    print(f"   Total unique sellers: {len(seller_counts)}")
    print(f"   Total unique brands: {len(brand_counts)}")
    print(f"   Products with seller info: {len(sellers)} / {len(products)}")

    # Identify marketplace/3rd party patterns
    third_party_keywords = ['marketplace', '3rd party', 'third party', 'reseller',
                            'fulfilled by', 'sold by', 'vendor']
    third_party_count = 0

    for p in products:
        seller = str(p.get('seller', '')).lower()
        if any(kw in seller for kw in third_party_keywords):
            third_party_count += 1

    print(f"   Potential 3rd party products: {third_party_count} ({(third_party_count/len(products)*100):.1f}%)")

    # Top sellers
    print(f"\n{source_name} - Top 10 Sellers:")
    for seller, count in seller_counts.most_common(10):
        pct = (count / len(products)) * 100
        print(f"   {seller}: {count} ({pct:.1f}%)")

    return seller_counts, brand_counts

walmart_sellers, walmart_brands = analyze_sellers(walmart, "WALMART")
homedepot_sellers, homedepot_brands = analyze_sellers(homedepot, "HOME DEPOT")

# Compare seller diversity
print(f"\n📊 SELLER DIVERSITY COMPARISON:")
print(f"   Walmart sellers per product: {len(walmart_sellers) / len(walmart):.3f}")
print(f"   Home Depot sellers per product: {len(homedepot_sellers) / len(homedepot):.3f}")

if len(walmart_sellers) / len(walmart) > len(homedepot_sellers) / len(homedepot):
    print(f"   ⚠️  Walmart has {((len(walmart_sellers)/len(walmart)) / (len(homedepot_sellers)/len(homedepot))):.1f}x more seller diversity")
    print(f"   This suggests marketplace/3rd party inflation")

print()

# ============================================================================
# HYPOTHESIS 3: Duplication
# ============================================================================
print("=" * 80)
print("HYPOTHESIS 3: Duplicate Products")
print("=" * 80)
print()

def find_duplicates(products, source_name):
    """Find potential duplicate products"""

    # Check for duplicate SKUs
    skus = [p.get('sku', '') for p in products if p.get('sku')]
    sku_counts = Counter(skus)
    duplicates_by_sku = {sku: count for sku, count in sku_counts.items() if count > 1}

    # Check for duplicate titles (normalized)
    def normalize_title(title):
        if not title:
            return ""
        # Remove special chars, lowercase, strip extra spaces
        return re.sub(r'[^a-z0-9\s]', '', title.lower()).strip()

    titles = [normalize_title(p.get('title', '')) for p in products]
    title_counts = Counter(titles)
    duplicates_by_title = {title: count for title, count in title_counts.items()
                           if count > 1 and title}

    # Check for duplicate URLs
    urls = [p.get('url', '') for p in products if p.get('url')]
    url_counts = Counter(urls)
    duplicates_by_url = {url: count for url, count in url_counts.items() if count > 1}

    print(f"\n{source_name} - Duplication Analysis:")
    print(f"   Duplicate SKUs: {len(duplicates_by_sku)} SKUs affecting {sum(duplicates_by_sku.values())} products")
    print(f"   Duplicate titles: {len(duplicates_by_title)} titles affecting {sum(duplicates_by_title.values())} products")
    print(f"   Duplicate URLs: {len(duplicates_by_url)} URLs affecting {sum(duplicates_by_url.values())} products")

    if duplicates_by_sku:
        print(f"\n   Top duplicate SKUs:")
        for sku, count in sorted(duplicates_by_sku.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"      {sku}: {count} copies")

    if duplicates_by_title:
        print(f"\n   Sample duplicate titles:")
        for title, count in sorted(duplicates_by_title.items(), key=lambda x: x[1], reverse=True)[:3]:
            print(f"      '{title[:60]}...': {count} copies")

    total_duplicate_estimate = sum(duplicates_by_title.values()) - len(duplicates_by_title)
    pct_duplicates = (total_duplicate_estimate / len(products)) * 100

    print(f"\n   📊 Estimated duplicate products: ~{total_duplicate_estimate} ({pct_duplicates:.1f}%)")

    return duplicates_by_sku, duplicates_by_title, duplicates_by_url

walmart_dup_sku, walmart_dup_title, walmart_dup_url = find_duplicates(walmart, "WALMART")
homedepot_dup_sku, homedepot_dup_title, homedepot_dup_url = find_duplicates(homedepot, "HOME DEPOT")

print()

# ============================================================================
# HYPOTHESIS 4: Non-US Products
# ============================================================================
print("=" * 80)
print("HYPOTHESIS 4: Non-US Products Included")
print("=" * 80)
print()

def check_non_us_products(products, source_name):
    """Check for international/non-US products"""

    non_us_indicators = [
        'international shipping', 'ships from china', 'ships from uk',
        'import', 'imported', 'european', 'asian', 'metric',
        'uk only', 'canada only', 'eu only'
    ]

    potential_non_us = 0
    examples = []

    for p in products:
        title = str(p.get('title', '')).lower()
        description = str(p.get('description', '')).lower()
        combined = title + ' ' + description

        if any(indicator in combined for indicator in non_us_indicators):
            potential_non_us += 1
            if len(examples) < 5:
                examples.append(p.get('title', 'No title'))

    print(f"\n{source_name} - Non-US Product Analysis:")
    print(f"   Potential non-US products: {potential_non_us} ({(potential_non_us/len(products)*100):.1f}%)")

    if examples:
        print(f"\n   Sample non-US products:")
        for ex in examples:
            print(f"      {ex[:80]}")

    return potential_non_us

walmart_non_us = check_non_us_products(walmart, "WALMART")
homedepot_non_us = check_non_us_products(homedepot, "MENARDS")

print()

# ============================================================================
# HYPOTHESIS 5: Price Range Analysis
# ============================================================================
print("=" * 80)
print("HYPOTHESIS 5: Price Range Differences")
print("=" * 80)
print()

def analyze_prices(products, source_name):
    """Analyze price distribution"""

    prices = []
    for p in products:
        price_str = p.get('price', '')
        if price_str:
            # Extract numeric price
            price_match = re.search(r'[\d,]+\.?\d*', str(price_str))
            if price_match:
                try:
                    price = float(price_match.group().replace(',', ''))
                    if 0 < price < 1000:  # Filter outliers
                        prices.append(price)
                except:
                    pass

    if prices:
        df_prices = pd.Series(prices)
        print(f"\n{source_name} - Price Distribution:")
        print(f"   Products with prices: {len(prices)} / {len(products)}")
        print(f"   Mean: ${df_prices.mean():.2f}")
        print(f"   Median: ${df_prices.median():.2f}")
        print(f"   Min: ${df_prices.min():.2f}")
        print(f"   Max: ${df_prices.max():.2f}")
        print(f"\n   Price Ranges:")
        print(f"      $0-10: {sum(1 for p in prices if p < 10)} ({sum(1 for p in prices if p < 10)/len(prices)*100:.1f}%)")
        print(f"      $10-25: {sum(1 for p in prices if 10 <= p < 25)} ({sum(1 for p in prices if 10 <= p < 25)/len(prices)*100:.1f}%)")
        print(f"      $25-50: {sum(1 for p in prices if 25 <= p < 50)} ({sum(1 for p in prices if 25 <= p < 50)/len(prices)*100:.1f}%)")
        print(f"      $50-100: {sum(1 for p in prices if 50 <= p < 100)} ({sum(1 for p in prices if 50 <= p < 100)/len(prices)*100:.1f}%)")
        print(f"      $100+: {sum(1 for p in prices if p >= 100)} ({sum(1 for p in prices if p >= 100)/len(prices)*100:.1f}%)")

    return prices

walmart_prices = analyze_prices(walmart, "WALMART")
homedepot_prices = analyze_prices(homedepot, "MENARDS")

# Check if Walmart has abnormal low-price product concentration
if walmart_prices and homedepot_prices:
    walmart_under_10 = sum(1 for p in walmart_prices if p < 10) / len(walmart_prices) * 100
    homedepot_under_10 = sum(1 for p in homedepot_prices if p < 10) / len(homedepot_prices) * 100

    print(f"\n📊 LOW-PRICE CONCENTRATION:")
    print(f"   Walmart under $10: {walmart_under_10:.1f}%")
    print(f"   Home Depot under $10: {homedepot_under_10:.1f}%")

    if walmart_under_10 > homedepot_under_10 * 1.5:
        print(f"   ⚠️  Walmart has {walmart_under_10/homedepot_under_10:.1f}x more low-price items")
        print(f"   Suggests accessories/add-ons inflating count")

print()

# ============================================================================
# SUMMARY & RECOMMENDATIONS
# ============================================================================
print("=" * 80)
print("ROOT CAUSE SUMMARY & RECOMMENDATIONS")
print("=" * 80)
print()

print("🔍 FINDINGS:\n")

# Collect issues
issues = []

# Check category breadth
walmart_only_count = sum(walmart_cats[cat] for cat in walmart_only_cats)
if walmart_only_count > len(walmart) * 0.1:
    issues.append({
        'severity': 'HIGH',
        'issue': 'Category Definition Too Broad',
        'impact': f'{walmart_only_count} products ({walmart_only_count/len(walmart)*100:.1f}%) in Walmart-only categories',
        'recommendation': 'Exclude categories not present in other retailers (HD, Lowe\'s, Home Depot)'
    })

# Check 3rd party
walmart_seller_diversity = len(walmart_sellers) / len(walmart)
homedepot_seller_diversity = len(homedepot_sellers) / len(homedepot)
if walmart_seller_diversity > homedepot_seller_diversity * 1.3:
    issues.append({
        'severity': 'MEDIUM',
        'issue': '3rd Party Marketplace Inflation',
        'impact': f'Walmart has {walmart_seller_diversity/homedepot_seller_diversity:.1f}x more seller diversity',
        'recommendation': 'Filter to major brands only; exclude marketplace/3rd party sellers'
    })

# Check duplicates
walmart_dup_pct = (sum(walmart_dup_title.values()) - len(walmart_dup_title)) / len(walmart) * 100
if walmart_dup_pct > 5:
    issues.append({
        'severity': 'MEDIUM',
        'issue': 'Duplicate Products',
        'impact': f'~{walmart_dup_pct:.1f}% estimated duplicates',
        'recommendation': 'De-duplicate by normalized title + price; keep lowest price variant'
    })

# Check low-price concentration
if walmart_prices and homedepot_prices:
    walmart_under_10 = sum(1 for p in walmart_prices if p < 10) / len(walmart_prices) * 100
    homedepot_under_10 = sum(1 for p in homedepot_prices if p < 10) / len(homedepot_prices) * 100
    if walmart_under_10 > homedepot_under_10 * 1.5:
        issues.append({
            'severity': 'HIGH',
            'issue': 'Accessories/Add-ons Inflating Count',
            'impact': f'Walmart: {walmart_under_10:.1f}% under $10 vs Home Depot: {homedepot_under_10:.1f}%',
            'recommendation': 'Set minimum price threshold ($15-20) to exclude small accessories'
        })

# Print issues
for i, issue in enumerate(issues, 1):
    print(f"{i}. [{issue['severity']}] {issue['issue']}")
    print(f"   Impact: {issue['impact']}")
    print(f"   Fix: {issue['recommendation']}\n")

# Estimate impact of fixes
print("=" * 80)
print("ESTIMATED IMPACT OF RECOMMENDED FIXES")
print("=" * 80)
print()

current_walmart = len(walmart)
estimated_after_fixes = current_walmart

# Estimate reductions
if issues:
    print("Starting: 7,499 Walmart products (78.5% of dataset)\n")

    for issue in issues:
        if 'Category' in issue['issue']:
            reduction = walmart_only_count
            estimated_after_fixes -= reduction
            print(f"After removing out-of-scope categories: -{reduction} products → {estimated_after_fixes}")

        elif 'Accessories' in issue['issue']:
            reduction = int(len(walmart) * (walmart_under_10 / 100) * 0.7)  # Remove 70% of under $10
            estimated_after_fixes -= reduction
            print(f"After $15 minimum price filter: -{reduction} products → {estimated_after_fixes}")

        elif 'Duplicate' in issue['issue']:
            reduction = int(len(walmart) * walmart_dup_pct / 100)
            estimated_after_fixes -= reduction
            print(f"After de-duplication: -{reduction} products → {estimated_after_fixes}")

        elif '3rd Party' in issue['issue']:
            reduction = int(len(walmart) * 0.15)  # Estimate 15% are 3rd party
            estimated_after_fixes -= reduction
            print(f"After removing 3rd party: -{reduction} products → {estimated_after_fixes}")

    print(f"\nFinal estimated Walmart count: {estimated_after_fixes}")

    # Recalculate percentage
    total_after = len(all_products) - (current_walmart - estimated_after_fixes)
    new_pct = (estimated_after_fixes / total_after) * 100

    print(f"New dataset total: {total_after}")
    print(f"Walmart would be: {new_pct:.1f}% of dataset")
    print(f"\nImprovement: 78.5% → {new_pct:.1f}% ({78.5 - new_pct:.1f} percentage points)")

    if new_pct < 30:
        print("✅ This would significantly reduce over-sampling bias")
    elif new_pct < 50:
        print("⚠️  Still some bias, but much improved")
    else:
        print("❌ Additional filtering needed")

print()
print("=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
