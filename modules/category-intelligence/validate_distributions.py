#!/usr/bin/env python3
"""
Statistical validation of product distributions vs expected market distributions.
Checks for sampling bias across categories, price points, and subcategories.
"""

import json
from pathlib import Path
from collections import defaultdict, Counter
import statistics

DATA_FILE = Path(__file__).parent / "data" / "garage_organizers_final_b_plus.json"

# Expected market distributions based on industry research & category expertise
EXPECTED_DISTRIBUTIONS = {
    # Main category splits (% of total garage organizer market)
    "category_distribution": {
        "Hooks & Hangers": (25, 35),  # Should be 25-35% combined
        "Cabinets & Storage": (10, 20),
        "Shelving": (20, 35),
        "Bins & Containers": (10, 20),
        "Workbenches": (3, 8),
        "Wall Systems": (5, 15),
        "Overhead Storage": (3, 8),
        "Tool Storage": (5, 12)
    },

    # Price tier distribution (% of products in each tier)
    "price_tiers": {
        "Budget (<$15)": (30, 45),      # Commodity/accessories
        "Mid ($15-$50)": (35, 50),      # Most common purchase range
        "Premium ($50-$150)": (15, 25), # Quality/investment pieces
        "High-End (>$150)": (5, 15)     # Cabinet systems/workbenches
    },

    # Shelving subcategories (% within shelving category)
    "shelving_types": {
        "Wire/Metal": (40, 60),
        "Wood/Composite": (15, 25),
        "Plastic/Resin": (20, 35)
    },

    # Cabinet subcategories (% within cabinet category)
    "cabinet_types": {
        "Base/Floor": (30, 45),
        "Wall-Mount": (25, 40),
        "Tall/Locker": (20, 35)
    }
}

def load_data():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return data.get('products', [])

def categorize_product(name):
    """Categorize products into main categories."""
    name_lower = name.lower()
    categories = []

    if any(term in name_lower for term in ['hook', 'hanger', 'peg']):
        categories.append('Hooks & Hangers')
    if any(term in name_lower for term in ['cabinet', 'locker']):
        categories.append('Cabinets & Storage')
    if any(term in name_lower for term in ['shelf', 'shelving', 'rack']):
        categories.append('Shelving')
    if any(term in name_lower for term in ['bin', 'container', 'tote']):
        categories.append('Bins & Containers')
    if 'workbench' in name_lower or 'work bench' in name_lower:
        categories.append('Workbenches')
    if any(term in name_lower for term in ['pegboard', 'slatwall', 'wall panel']):
        categories.append('Wall Systems')
    if any(term in name_lower for term in ['ceiling', 'overhead']):
        categories.append('Overhead Storage')
    if 'tool' in name_lower and 'organizer' in name_lower:
        categories.append('Tool Storage')

    return categories if categories else ['Other']

def categorize_shelving_type(name):
    """Subcategorize shelving products."""
    name_lower = name.lower()
    if any(term in name_lower for term in ['wire', 'metal', 'chrome', 'steel']):
        return 'Wire/Metal'
    elif any(term in name_lower for term in ['wood', 'composite']):
        return 'Wood/Composite'
    elif any(term in name_lower for term in ['plastic', 'resin']):
        return 'Plastic/Resin'
    return 'Other'

def categorize_cabinet_type(name):
    """Subcategorize cabinet products."""
    name_lower = name.lower()
    if any(term in name_lower for term in ['base', 'floor', 'freestanding']):
        return 'Base/Floor'
    elif 'wall' in name_lower:
        return 'Wall-Mount'
    elif any(term in name_lower for term in ['tall', 'locker']):
        return 'Tall/Locker'
    return 'Other'

def categorize_price_tier(price):
    """Categorize product into price tier."""
    if price is None:
        return None
    if price < 15:
        return 'Budget (<$15)'
    elif price < 50:
        return 'Mid ($15-$50)'
    elif price < 150:
        return 'Premium ($50-$150)'
    else:
        return 'High-End (>$150)'

def calculate_variance(actual_pct, expected_range):
    """Calculate variance from expected range."""
    expected_min, expected_max = expected_range
    expected_mid = (expected_min + expected_max) / 2
    variance = actual_pct - expected_mid
    variance_pct = abs(variance)

    # Check if within range
    within_range = expected_min <= actual_pct <= expected_max

    return {
        'variance': variance,
        'variance_pct': variance_pct,
        'within_range': within_range,
        'expected_range': expected_range,
        'expected_mid': expected_mid
    }

def validate_category_distribution(products):
    """Validate main category distribution."""
    print("\n" + "="*70)
    print("1. CATEGORY DISTRIBUTION VALIDATION")
    print("="*70)

    # Count products by category
    category_counts = defaultdict(int)
    for product in products:
        name = product.get('name') or product.get('title', '')
        categories = categorize_product(name)
        for cat in categories:
            category_counts[cat] += 1

    total = len(products)
    results = {}

    print(f"\nTotal products analyzed: {total:,}\n")
    print(f"{'Category':<25} {'Count':>8} {'Actual %':>10} {'Expected %':>15} {'Variance':>10} {'Status':>10}")
    print("-" * 90)

    for category, expected_range in EXPECTED_DISTRIBUTIONS['category_distribution'].items():
        count = category_counts.get(category, 0)
        actual_pct = 100 * count / total

        analysis = calculate_variance(actual_pct, expected_range)
        results[category] = analysis

        status = "✅ PASS" if analysis['within_range'] else "⚠️ VARIANCE"

        print(f"{category:<25} {count:>8,} {actual_pct:>9.1f}% "
              f"{expected_range[0]:>6.0f}-{expected_range[1]:<6.0f}% "
              f"{analysis['variance']:>+9.1f}% {status:>10}")

    return results

def validate_price_distribution(products):
    """Validate price tier distribution."""
    print("\n" + "="*70)
    print("2. PRICE TIER DISTRIBUTION VALIDATION")
    print("="*70)

    # Count products by price tier
    products_with_price = [p for p in products if p.get('price')]
    tier_counts = defaultdict(int)

    for product in products_with_price:
        price = product.get('price')
        tier = categorize_price_tier(price)
        if tier:
            tier_counts[tier] += 1

    total = len(products_with_price)
    results = {}

    print(f"\nProducts with pricing: {total:,} ({100*total/len(products):.1f}% coverage)\n")
    print(f"{'Price Tier':<25} {'Count':>8} {'Actual %':>10} {'Expected %':>15} {'Variance':>10} {'Status':>10}")
    print("-" * 90)

    for tier, expected_range in EXPECTED_DISTRIBUTIONS['price_tiers'].items():
        count = tier_counts.get(tier, 0)
        actual_pct = 100 * count / total if total > 0 else 0

        analysis = calculate_variance(actual_pct, expected_range)
        results[tier] = analysis

        status = "✅ PASS" if analysis['within_range'] else "⚠️ VARIANCE"

        print(f"{tier:<25} {count:>8,} {actual_pct:>9.1f}% "
              f"{expected_range[0]:>6.0f}-{expected_range[1]:<6.0f}% "
              f"{analysis['variance']:>+9.1f}% {status:>10}")

    return results

def validate_shelving_subcategories(products):
    """Validate shelving subcategory distribution."""
    print("\n" + "="*70)
    print("3. SHELVING SUBCATEGORY VALIDATION")
    print("="*70)

    # Get shelving products
    shelving_products = []
    for product in products:
        name = product.get('name') or product.get('title', '')
        categories = categorize_product(name)
        if 'Shelving' in categories:
            shelving_products.append(product)

    # Count by type
    type_counts = defaultdict(int)
    for product in shelving_products:
        name = product.get('name') or product.get('title', '')
        shelf_type = categorize_shelving_type(name)
        type_counts[shelf_type] += 1

    total = len(shelving_products)
    results = {}

    print(f"\nTotal shelving products: {total:,}\n")
    print(f"{'Shelving Type':<25} {'Count':>8} {'Actual %':>10} {'Expected %':>15} {'Variance':>10} {'Status':>10}")
    print("-" * 90)

    for shelf_type, expected_range in EXPECTED_DISTRIBUTIONS['shelving_types'].items():
        count = type_counts.get(shelf_type, 0)
        actual_pct = 100 * count / total if total > 0 else 0

        analysis = calculate_variance(actual_pct, expected_range)
        results[shelf_type] = analysis

        status = "✅ PASS" if analysis['within_range'] else "⚠️ VARIANCE"

        print(f"{shelf_type:<25} {count:>8,} {actual_pct:>9.1f}% "
              f"{expected_range[0]:>6.0f}-{expected_range[1]:<6.0f}% "
              f"{analysis['variance']:>+9.1f}% {status:>10}")

    return results

def validate_cabinet_subcategories(products):
    """Validate cabinet subcategory distribution."""
    print("\n" + "="*70)
    print("4. CABINET SUBCATEGORY VALIDATION")
    print("="*70)

    # Get cabinet products
    cabinet_products = []
    for product in products:
        name = product.get('name') or product.get('title', '')
        categories = categorize_product(name)
        if 'Cabinets & Storage' in categories:
            cabinet_products.append(product)

    # Count by type
    type_counts = defaultdict(int)
    for product in cabinet_products:
        name = product.get('name') or product.get('title', '')
        cab_type = categorize_cabinet_type(name)
        type_counts[cab_type] += 1

    total = len(cabinet_products)
    results = {}

    print(f"\nTotal cabinet products: {total:,}\n")
    print(f"{'Cabinet Type':<25} {'Count':>8} {'Actual %':>10} {'Expected %':>15} {'Variance':>10} {'Status':>10}")
    print("-" * 90)

    for cab_type, expected_range in EXPECTED_DISTRIBUTIONS['cabinet_types'].items():
        count = type_counts.get(cab_type, 0)
        actual_pct = 100 * count / total if total > 0 else 0

        analysis = calculate_variance(actual_pct, expected_range)
        results[cab_type] = analysis

        status = "✅ PASS" if analysis['within_range'] else "⚠️ VARIANCE"

        print(f"{cab_type:<25} {count:>8,} {actual_pct:>9.1f}% "
              f"{expected_range[0]:>6.0f}-{expected_range[1]:<6.0f}% "
              f"{analysis['variance']:>+9.1f}% {status:>10}")

    return results

def generate_summary(all_results):
    """Generate overall validation summary."""
    print("\n" + "="*70)
    print("OVERALL VALIDATION SUMMARY")
    print("="*70)

    total_checks = 0
    passed_checks = 0
    high_variance = []

    for validation_name, results in all_results.items():
        for item, analysis in results.items():
            total_checks += 1
            if analysis['within_range']:
                passed_checks += 1
            elif analysis['variance_pct'] > 5:
                high_variance.append((validation_name, item, analysis))

    pass_rate = 100 * passed_checks / total_checks if total_checks > 0 else 0

    print(f"\nTotal validation checks: {total_checks}")
    print(f"Passed (within expected range): {passed_checks} ({pass_rate:.1f}%)")
    print(f"Variance warnings: {total_checks - passed_checks}")

    if high_variance:
        print(f"\n⚠️  HIGH VARIANCE ITEMS (>5% from expected mid-point):")
        for val_name, item, analysis in high_variance:
            print(f"   • {val_name} - {item}: {analysis['variance']:+.1f}% variance")
    else:
        print("\n✅ No high variance items detected!")

    print(f"\n{'='*70}")
    if pass_rate >= 75:
        print("✅ VALIDATION PASSED: Dataset distributions are representative")
        print("   No significant sampling bias detected.")
    elif pass_rate >= 50:
        print("⚠️  VALIDATION WARNING: Some variance detected but acceptable")
        print("   Minor sampling bias present but dataset is usable.")
    else:
        print("❌ VALIDATION FAILED: Significant distribution variance")
        print("   Dataset may have sampling bias issues.")
    print("="*70)

def main():
    print("="*70)
    print("STATISTICAL DISTRIBUTION VALIDATION")
    print("Checking for sampling bias across categories & price points")
    print("="*70)

    products = load_data()
    print(f"\nDataset: {len(products):,} unique products")

    all_results = {}

    # Run all validations
    all_results['Category Distribution'] = validate_category_distribution(products)
    all_results['Price Tiers'] = validate_price_distribution(products)
    all_results['Shelving Types'] = validate_shelving_subcategories(products)
    all_results['Cabinet Types'] = validate_cabinet_subcategories(products)

    # Generate summary
    generate_summary(all_results)

if __name__ == "__main__":
    main()
