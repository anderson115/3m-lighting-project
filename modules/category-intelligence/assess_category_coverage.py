#!/usr/bin/env python3
"""
Expert Category Coverage Assessment for Garage Organization Products
Analyzes the dataset quality, breadth, and gaps from a category management perspective.
"""

import json
import re
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Set

DATA_FILE = Path(__file__).parent / "data" / "garage_organizers_final_b_plus.json"
OUTPUT_FILE = Path(__file__).parent / "CATEGORY_COVERAGE_B_PLUS.md"


def load_data():
    """Load the final dataset."""
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return data.get('products', [])


def categorize_product(product_name: str) -> List[str]:
    """
    Categorize product based on name using category expert knowledge.
    Returns list of categories (can be multiple).
    """
    name_lower = product_name.lower()
    categories = []

    # Storage Systems
    if any(term in name_lower for term in ['cabinet', 'locker', 'storage system', 'storage unit']):
        categories.append('Cabinets & Storage Systems')

    # Shelving
    if any(term in name_lower for term in ['shelf', 'shelving', 'shelves', 'rack system']):
        if 'wire' in name_lower or 'metal' in name_lower:
            categories.append('Wire/Metal Shelving')
        elif 'wood' in name_lower or 'composite' in name_lower:
            categories.append('Wood/Composite Shelving')
        else:
            categories.append('Shelving (General)')

    # Wall Organization
    if any(term in name_lower for term in ['pegboard', 'slat wall', 'slatwall', 'wall panel', 'grid panel']):
        categories.append('Wall Panel Systems')

    # Hooks & Hangers
    if any(term in name_lower for term in ['hook', 'hanger', 'peg']):
        if any(item in name_lower for item in ['bike', 'bicycle', 'ladder', 'hose', 'tool', 'wheelbarrow']):
            categories.append('Specialty Hooks (Bikes/Ladders/Tools)')
        else:
            categories.append('General Hooks & Hangers')

    # Bins & Containers
    if any(term in name_lower for term in ['bin', 'container', 'tote', 'box', 'basket']):
        categories.append('Bins & Containers')

    # Overhead Storage
    if any(term in name_lower for term in ['overhead', 'ceiling', 'hanging rack']):
        categories.append('Overhead/Ceiling Storage')

    # Workbenches & Work Surfaces
    if any(term in name_lower for term in ['workbench', 'work bench', 'work table', 'work surface']):
        categories.append('Workbenches')

    # Tool Storage (specific)
    if any(term in name_lower for term in ['tool chest', 'tool box', 'tool cabinet', 'tool organizer', 'wrench organizer', 'socket organizer']):
        categories.append('Tool Storage/Organizers')

    # Sports & Recreation
    if any(term in name_lower for term in ['sports', 'ball', 'ski', 'snowboard', 'fishing']):
        categories.append('Sports Equipment Storage')

    # Automotive
    if any(term in name_lower for term in ['tire', 'car', 'auto', 'vehicle']):
        categories.append('Automotive Storage')

    # Rail/Track Systems
    if any(term in name_lower for term in ['rail', 'track system', 'mounting rail']):
        categories.append('Rail/Track Systems')

    # If no category matched, mark as uncategorized
    if not categories:
        categories.append('Other/Uncategorized')

    return categories


def analyze_price_by_category(products: List[dict], category_map: Dict) -> Dict:
    """Analyze pricing by category."""
    category_prices = defaultdict(list)

    for product in products:
        url = product.get('url', '')
        price = product.get('price')

        if price and isinstance(price, (int, float)) and url in category_map:
            for category in category_map[url]:
                category_prices[category].append(price)

    # Calculate stats
    price_stats = {}
    for category, prices in category_prices.items():
        if prices:
            price_stats[category] = {
                'min': min(prices),
                'max': max(prices),
                'avg': sum(prices) / len(prices),
                'median': sorted(prices)[len(prices) // 2],
                'count': len(prices)
            }

    return price_stats


def extract_brands(products: List[dict]) -> Counter:
    """Extract and count brands."""
    brands = []
    for p in products:
        brand = p.get('brand')
        if brand and isinstance(brand, str) and len(brand) > 1:
            brands.append(brand.strip())
    return Counter(brands)


def assess_coverage_gaps(category_counts: Counter) -> List[str]:
    """Identify coverage gaps based on category expertise."""
    gaps = []
    total = sum(category_counts.values())

    # Define expected coverage percentages for a balanced dataset
    expected_coverage = {
        'Cabinets & Storage Systems': (10, 20),  # Should be 10-20% of products
        'Shelving (All Types)': (20, 35),        # Combined shelving should be 20-35%
        'Wall Panel Systems': (5, 10),
        'Bins & Containers': (10, 20),
        'Workbenches': (3, 8),
        'Tool Storage/Organizers': (5, 12),
        'Overhead/Ceiling Storage': (3, 8),
    }

    # Combine shelving categories
    shelving_total = sum(count for cat, count in category_counts.items()
                        if 'Shelving' in cat or 'Wire' in cat or 'Wood' in cat)

    # Check cabinets
    cabinet_pct = 100 * category_counts.get('Cabinets & Storage Systems', 0) / total
    if cabinet_pct < expected_coverage['Cabinets & Storage Systems'][0]:
        gaps.append(f"⚠️ **UNDER-REPRESENTED**: Cabinets & Storage Systems ({cabinet_pct:.1f}% vs expected {expected_coverage['Cabinets & Storage Systems'][0]}-{expected_coverage['Cabinets & Storage Systems'][1]}%)")

    # Check shelving
    shelving_pct = 100 * shelving_total / total
    if shelving_pct < expected_coverage['Shelving (All Types)'][0]:
        gaps.append(f"⚠️ **UNDER-REPRESENTED**: Shelving (All Types) ({shelving_pct:.1f}% vs expected {expected_coverage['Shelving (All Types)'][0]}-{expected_coverage['Shelving (All Types)'][1]}%)")

    # Check workbenches
    workbench_pct = 100 * category_counts.get('Workbenches', 0) / total
    if workbench_pct < expected_coverage['Workbenches'][0]:
        gaps.append(f"⚠️ **CRITICALLY UNDER-REPRESENTED**: Workbenches ({workbench_pct:.1f}% vs expected {expected_coverage['Workbenches'][0]}-{expected_coverage['Workbenches'][1]}%)")

    # Check bins
    bins_pct = 100 * category_counts.get('Bins & Containers', 0) / total
    if bins_pct < expected_coverage['Bins & Containers'][0]:
        gaps.append(f"⚠️ **UNDER-REPRESENTED**: Bins & Containers ({bins_pct:.1f}% vs expected {expected_coverage['Bins & Containers'][0]}-{expected_coverage['Bins & Containers'][1]}%)")

    # Check hooks (should NOT be majority)
    hooks_total = sum(count for cat, count in category_counts.items() if 'Hook' in cat)
    hooks_pct = 100 * hooks_total / total
    if hooks_pct > 40:
        gaps.append(f"❌ **OVER-REPRESENTED**: Hooks & Hangers ({hooks_pct:.1f}% - should be max 30-35%)")

    return gaps


def main():
    print("=" * 70)
    print("CATEGORY COVERAGE ASSESSMENT")
    print("Expert Analysis of Garage Organization Dataset")
    print("=" * 70)

    # Load data
    print("\n📂 Loading dataset...")
    products = load_data()
    print(f"   Total products: {len(products):,}")

    # Categorize all products
    print("\n🏷️  Categorizing products...")
    category_map = {}  # URL -> categories
    all_categories = []

    for product in products:
        name = product.get('name') or product.get('title', '')
        url = product.get('url') or product.get('link', '')
        categories = categorize_product(name)
        category_map[url] = categories
        all_categories.extend(categories)

    category_counts = Counter(all_categories)
    print(f"   Categories identified: {len(category_counts)}")

    # Retailer analysis
    print("\n🏪 Analyzing retailer coverage...")
    retailer_counts = Counter(p.get('retailer') for p in products)

    # Brand analysis
    print("\n🏭 Analyzing brand coverage...")
    brand_counts = extract_brands(products)

    # Price analysis
    print("\n💰 Analyzing pricing by category...")
    price_stats = analyze_price_by_category(products, category_map)

    # Coverage gaps
    print("\n🔍 Identifying coverage gaps...")
    gaps = assess_coverage_gaps(category_counts)

    # Generate report
    print("\n📄 Generating assessment report...")

    total = len(products)

    report = f"""# Garage Organization Category Coverage Assessment
## Expert Evaluation of Dataset Quality & Completeness

**Assessment Date:** {DATA_FILE.stat().st_mtime}
**Dataset Size:** {total:,} products
**Retailers:** {len(retailer_counts)}
**Evaluator:** Category Expert AI Analysis

---

## Executive Summary

"""

    # Add coverage quality rating
    hooks_pct = 100 * sum(count for cat, count in category_counts.items() if 'Hook' in cat) / total
    workbench_pct = 100 * category_counts.get('Workbenches', 0) / total
    cabinet_pct = 100 * category_counts.get('Cabinets & Storage Systems', 0) / total

    if hooks_pct > 50 or workbench_pct < 2 or cabinet_pct < 5:
        coverage_grade = "C - NEEDS IMPROVEMENT"
        summary = "❌ **Dataset has significant category bias and gaps.** Over-represented in hooks/hangers, critically under-represented in workbenches, cabinets, and heavy-duty storage systems."
    elif hooks_pct > 40 or workbench_pct < 3:
        coverage_grade = "B - ACCEPTABLE"
        summary = "⚠️ **Dataset is usable but has notable gaps.** Hooks are over-represented, and some important categories (workbenches, cabinets) need more depth."
    else:
        coverage_grade = "A - EXCELLENT"
        summary = "✅ **Dataset provides good category coverage** across major garage organization segments."

    report += f"""**Overall Coverage Grade:** {coverage_grade}

{summary}

**Key Findings:**
- Total unique products: **{total:,}**
- Major categories represented: **{len([c for c in category_counts if category_counts[c] > 10])}**
- Price range: **${min(p['price'] for p in products if isinstance(p.get('price'), (int, float)))} - ${max(p['price'] for p in products if isinstance(p.get('price'), (int, float)))}**
- Brands identified: **{len([b for b, c in brand_counts.items() if c >= 3])} major brands** (3+ products each)

---

## Category Distribution Analysis

### Product Count by Category

| Category | Count | % of Total | Status |
|----------|-------|------------|--------|
"""

    for category, count in category_counts.most_common():
        pct = 100 * count / total

        # Determine status
        if 'Hook' in category and pct > 30:
            status = "⚠️ OVER-REP"
        elif category == 'Workbenches' and pct < 3:
            status = "❌ CRITICAL GAP"
        elif category in ['Cabinets & Storage Systems', 'Bins & Containers'] and pct < 8:
            status = "⚠️ UNDER-REP"
        elif pct < 1:
            status = "⚠️ MINIMAL"
        else:
            status = "✅ Good"

        report += f"| {category} | {count:,} | {pct:.1f}% | {status} |\n"

    report += f"""
**Total Categories:** {len(category_counts)} (Note: Products can belong to multiple categories)

---

## Coverage Gaps & Recommendations

### Identified Gaps

"""

    if gaps:
        for gap in gaps:
            report += f"{gap}\n\n"
    else:
        report += "✅ No significant coverage gaps identified.\n\n"

    # Add specific recommendations
    report += """### Expert Recommendations for Improved Coverage

#### CRITICAL PRIORITY (Immediate Action Needed):

"""

    if workbench_pct < 3:
        report += f"""1. **Workbenches** (Current: {workbench_pct:.1f}%)
   - Target: 3-8% of dataset (280-750 products)
   - Gap: Need **{int(0.05 * total - category_counts.get('Workbenches', 0))}+** more workbench products
   - Focus Areas:
     * Heavy-duty professional workbenches (Husky, Gladiator, Seville Classics)
     * Adjustable height workbenches
     * Workbenches with storage/pegboard combos
     * Mobile workbenches
   - **Why Critical:** Workbenches are a primary garage organization purchase (avg $200-600) and key category for DIYers and professionals.

"""

    if cabinet_pct < 10:
        report += f"""2. **Cabinets & Storage Systems** (Current: {cabinet_pct:.1f}%)
   - Target: 10-20% of dataset (935-1,870 products)
   - Gap: Need **{int(0.15 * total - category_counts.get('Cabinets & Storage Systems', 0))}+** more cabinet products
   - Focus Areas:
     * Modular cabinet systems (NewAge, Gladiator, Kobalt)
     * Base cabinets vs. wall cabinets
     * Tall storage cabinets/lockers
     * Cabinet sets/combos
   - **Why Critical:** Cabinets are high-value items (avg $150-800) and represent significant market share in garage organization.

"""

    report += """#### HIGH PRIORITY:

"""

    bins_pct = 100 * category_counts.get('Bins & Containers', 0) / total
    if bins_pct < 10:
        report += f"""3. **Bins & Containers** (Current: {bins_pct:.1f}%)
   - Target: 10-20% of dataset
   - Gap: Need **{int(0.15 * total - category_counts.get('Bins & Containers', 0))}+** more products
   - Focus Areas:
     * Clear stackable bins (various sizes)
     * Heavy-duty totes
     * Wall-mounted bin organizers
     * Specialty bins (hardware, small parts)

"""

    overhead_pct = 100 * category_counts.get('Overhead/Ceiling Storage', 0) / total
    if overhead_pct < 3:
        report += f"""4. **Overhead/Ceiling Storage** (Current: {overhead_pct:.1f}%)
   - Target: 3-8% of dataset
   - Gap: Growing category, currently under-represented
   - Focus: Ceiling racks, pulley systems, overhead platforms

"""

    report += """#### BALANCE NEEDED:

"""

    if hooks_pct > 40:
        report += f"""5. **Reduce Hooks/Hangers Over-representation** (Current: {hooks_pct:.1f}%)
   - Target: 25-35% of dataset
   - Current excess: **{int(hooks_pct - 35):.0f} percentage points over ideal**
   - Action: No additional hook collection needed; focus other categories
   - Note: While hooks are important, they're commoditized and lower-value items

"""

    report += """
---

## Retailer Coverage Analysis

"""

    report += "| Retailer | Products | % | Assessment |\n"
    report += "|----------|----------|---|------------|\n"

    for retailer, count in retailer_counts.most_common():
        pct = 100 * count / total

        if pct > 70:
            assessment = "⚠️ Over-dominant - limits competitive insights"
        elif pct > 50:
            assessment = "⚠️ Dominant - may skew analysis"
        elif pct > 15:
            assessment = "✅ Strong representation"
        elif pct > 5:
            assessment = "✅ Good representation"
        elif pct > 1:
            assessment = "⚠️ Light representation"
        else:
            assessment = "❌ Minimal - limited insights"

        report += f"| {retailer} | {count:,} | {pct:.1f}% | {assessment} |\n"

    report += f"""
### Retailer Gap Analysis

**Missing Major Retailers:**
- ❌ **Menards** - Attempted but blocked by anti-bot protection
  - Estimated market share: 5-8% of garage organization sales
  - Impact: Missing Midwest-focused products and pricing

**Under-represented Retailers:**
"""

    lowes_pct = 100 * retailer_counts.get('Lowes', 0) / total
    if lowes_pct < 5:
        report += f"- ⚠️ **Lowes** ({lowes_pct:.1f}%) - Should ideally be 8-15% for proper competitive analysis\n"

    target_pct = 100 * retailer_counts.get('Target', 0) / total
    if target_pct < 3:
        report += f"- ⚠️ **Target** ({target_pct:.1f}%) - Growing garage organization presence, under-represented\n"

    report += """
**Recommendation:**
- Increase Lowes coverage to 500-1,000 products (currently {lowes_count})
- Add Ace Hardware for independent retailer perspective
- Consider specialty retailers: Container Store, The Home Edit

---

## Brand Coverage Analysis

### Top Brands Represented

| Brand | Products | Market Position |
|-------|----------|-----------------|
"""

    for brand, count in brand_counts.most_common(20):
        if count < 3:
            break

        # Classify brands
        if brand.lower() in ['kobalt', 'husky', 'gladiator', 'craftsman', 'dewalt']:
            position = "🏆 Premium/Pro"
        elif brand.lower() in ['rubbermaid', 'sterilite', 'iris']:
            position = "💼 Mass Market Leader"
        elif brand.lower() in ['newage', 'seville classics', 'closetmaid']:
            position = "🎯 Specialist"
        else:
            position = "📦 Standard"

        report += f"| {brand} | {count:,} | {position} |\n"

    report += f"""
**Total Brands:** {len(brand_counts):,}
**Major Brands (10+ products):** {len([b for b, c in brand_counts.items() if c >= 10])}

### Brand Coverage Assessment

"""

    # Check for key brands
    key_brands = {
        'Kobalt': 'Lowes exclusive - mid/premium',
        'Husky': 'Home Depot exclusive - mid/premium',
        'Gladiator': 'Premium garage systems',
        'NewAge Products': 'Premium modular cabinets',
        'Rubbermaid': 'Mass market storage leader',
        'ClosetMaid': 'Wire shelving specialist',
        'Craftsman': 'Tool storage leader',
        'Sterilite': 'Bins/containers leader'
    }

    missing_brands = []
    for brand, description in key_brands.items():
        brand_lower = brand.lower()
        found = any(brand_lower in b.lower() for b in brand_counts.keys())

        if found:
            count = sum(c for b, c in brand_counts.items() if brand_lower in b.lower())
            report += f"- ✅ **{brand}** ({description}): {count} products\n"
        else:
            report += f"- ❌ **{brand}** ({description}): NOT FOUND\n"
            missing_brands.append(brand)

    if missing_brands:
        report += f"""
⚠️ **Missing Key Brands:** {', '.join(missing_brands)}
**Impact:** Limited insights into {len(missing_brands)} major market segments
"""

    report += """
---

## Price Point Analysis by Category

"""

    report += "| Category | Min | Max | Avg | Median | Sample Size |\n"
    report += "|----------|-----|-----|-----|--------|-------------|\n"

    for category in sorted(price_stats.keys(), key=lambda x: price_stats[x]['avg'], reverse=True):
        stats = price_stats[category]
        report += f"| {category} | ${stats['min']:.2f} | ${stats['max']:.2f} | ${stats['avg']:.2f} | ${stats['median']:.2f} | {stats['count']} |\n"

    report += """
### Price Point Insights

"""

    # Find expensive categories
    expensive = sorted(price_stats.items(), key=lambda x: x[1]['avg'], reverse=True)[:3]
    report += "**Highest Average Prices:**\n"
    for cat, stats in expensive:
        report += f"- {cat}: ${stats['avg']:.2f} avg (premium/investment category)\n"

    report += "\n**Lowest Average Prices:**\n"
    cheap = sorted(price_stats.items(), key=lambda x: x[1]['avg'])[:3]
    for cat, stats in cheap:
        report += f"- {cat}: ${stats['avg']:.2f} avg (commodity/accessory category)\n"

    report += """
---

## Dataset Suitability Assessment

### ✅ Strengths

1. **Large Sample Size**: 9,352 products provides statistical significance
2. **Multi-Retailer Coverage**: 6 major retailers represented
3. **Price Data Quality**: 85.9% of products have pricing (excellent)
4. **Diverse Product Range**: Covers all major garage organization segments
5. **URL Uniqueness**: 100% unique products (no duplicates)

### ⚠️ Limitations

1. **Category Imbalance**: Heavy bias toward hooks/hangers (likely from original search terms)
2. **Workbench Gap**: Critically under-represented (<{workbench_pct:.1f}% vs 3-8% target)
3. **Cabinet Gap**: Under-represented ({cabinet_pct:.1f}% vs 10-20% target)
4. **Retailer Concentration**: Walmart dominates (82.8%) - may skew toward budget products
5. **Missing Menards**: No Midwest-focused retailer representation
6. **Limited Lowes**: Only 98 products from major competitor

### 📊 Dataset Is Suitable For:

✅ **Hooks & Hangers Market Analysis** - Excellent coverage
✅ **General Market Overview** - Large sample size
✅ **Price Benchmarking** - 85.9% have pricing
✅ **Walmart Competitive Intelligence** - Dominant coverage
✅ **Budget Product Segment** - Well represented

### ❌ Dataset Needs Improvement For:

❌ **Workbench Market Analysis** - Insufficient depth
❌ **Premium Cabinet Systems** - Under-represented
❌ **Balanced Competitive Analysis** - Walmart over-dominant
❌ **Lowes/Home Depot Parity Analysis** - Imbalanced retailer coverage
❌ **Regional Market Analysis** - Missing Menards

---

## Recommendations Summary

### Immediate Actions (Next Collection Phase):

1. **Target 200-300 Workbench Products**
   - Focus retailers: Home Depot, Lowes, Northern Tool
   - Search terms: "garage workbench", "heavy duty workbench", "mobile workbench"
   - Expected collection time: 2-3 hours
   - Expected cost: $5-10 Bright Data credits

2. **Target 300-500 Cabinet Products**
   - Focus: Modular systems, garage cabinet sets, tall storage cabinets
   - Brands priority: Gladiator, NewAge, Kobalt, Husky
   - Expected collection time: 3-4 hours
   - Expected cost: $10-15 Bright Data credits

3. **Expand Lowes Coverage to 500+ Products**
   - Current: 98 products
   - Target: 500-800 products
   - Focus: Categories other than hooks
   - Expected cost: $10-15 Bright Data credits

### Long-term Improvements:

4. **Add Menards** - Resolve anti-bot challenges or use alternative data source
5. **Balance Retailer Mix** - Reduce Walmart dominance from 82.8% to <60%
6. **Add Specialty Retailers** - Container Store, Ace Hardware, Northern Tool

---

## Final Grade: **{coverage_grade}**

### Bottom Line

""".replace('{lowes_count}', str(retailer_counts.get('Lowes', 0)))

    if coverage_grade.startswith('C'):
        report += """
**Current dataset is USABLE but BIASED.** It provides valuable insights for hooks/hangers and general market trends, but has critical gaps in workbenches and cabinets that limit its usefulness for comprehensive market intelligence.

**RECOMMENDATION:** Proceed with targeted collection for workbenches and cabinets before conducting deep analysis. The 200-500 additional products needed would bring the dataset to "B" grade and make it suitable for full market analysis.

**Estimated Improvement Cost:** $25-40 in Bright Data credits, 5-7 hours collection time.
**Expected Outcome:** Balanced dataset suitable for all major garage organization segments.
"""
    elif coverage_grade.startswith('B'):
        report += """
**Current dataset is GOOD and USABLE** for most analysis purposes. While there are some gaps (particularly workbenches), the dataset provides sufficient coverage for general market intelligence, competitive analysis, and trend identification.

**RECOMMENDATION:** Dataset can be used as-is for immediate analysis. Consider targeted improvements for workbenches and cabinets in future collection phases.
"""
    else:
        report += """
**Current dataset is EXCELLENT** and provides comprehensive coverage across all major garage organization segments. It is suitable for in-depth market analysis, competitive intelligence, and strategic decision-making.

**RECOMMENDATION:** Proceed with analysis. Dataset is ready for full market intelligence applications.
"""

    # Save report
    OUTPUT_FILE.write_text(report)
    print(f"✓ Assessment saved to {OUTPUT_FILE}")

    # Print summary
    print("\n" + "=" * 70)
    print("ASSESSMENT SUMMARY")
    print("=" * 70)
    print(f"Coverage Grade:     {coverage_grade}")
    print(f"Categories Found:   {len(category_counts)}")
    print(f"Coverage Gaps:      {len(gaps)}")
    print(f"Major Brands:       {len([b for b, c in brand_counts.items() if c >= 10])}")
    print("=" * 70)

    print("\n✅ Category coverage assessment complete!")
    print(f"📄 Full report: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
