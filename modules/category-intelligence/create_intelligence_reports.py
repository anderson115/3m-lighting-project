#!/usr/bin/env python3
"""
Generate 3 critical category intelligence reports for market entry decision.
Target audiences: Category Innovation Team, Pricing Team, Marketing Team
"""

import json
from pathlib import Path
from collections import defaultdict, Counter
import statistics

DATA_FILE = Path(__file__).parent / "data" / "garage_organizers_final_b_plus.json"
OUTPUT_DIR = Path(__file__).parent

def load_data():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return data.get('products', [])

def categorize_product(name):
    """Simple categorization."""
    name_lower = name.lower()
    if 'workbench' in name_lower:
        return 'Workbenches'
    elif any(term in name_lower for term in ['cabinet', 'locker']):
        return 'Cabinets'
    elif any(term in name_lower for term in ['shelf', 'shelving']):
        return 'Shelving'
    elif any(term in name_lower for term in ['bin', 'container', 'tote']):
        return 'Bins & Containers'
    elif any(term in name_lower for term in ['hook', 'hanger']):
        return 'Hooks & Hangers'
    else:
        return 'Other'

def categorize_price_tier(price):
    """Categorize into price tiers."""
    if price is None:
        return None
    if price < 15:
        return 'Budget (<$15)'
    elif price < 50:
        return 'Mid-Market ($15-$50)'
    elif price < 150:
        return 'Premium ($50-$150)'
    else:
        return 'Luxury (>$150)'

# ============================================================================
# REPORT 1: BRAND COMPETITIVE LANDSCAPE
# ============================================================================

def generate_brand_report(products):
    """Generate comprehensive brand intelligence report."""

    print("Generating Brand Competitive Landscape Report...")

    # Collect brand data
    brand_data = defaultdict(lambda: {
        'count': 0,
        'categories': Counter(),
        'retailers': Counter(),
        'prices': [],
        'products': []
    })

    for product in products:
        brand = product.get('brand')
        if not brand or not isinstance(brand, str) or len(brand) < 2:
            brand = 'Unbranded/Generic'

        name = product.get('name') or product.get('title', '')
        category = categorize_product(name)
        retailer = product.get('retailer', 'Unknown')
        price = product.get('price')

        brand_data[brand]['count'] += 1
        brand_data[brand]['categories'][category] += 1
        brand_data[brand]['retailers'][retailer] += 1
        if price:
            brand_data[brand]['prices'].append(price)
        brand_data[brand]['products'].append(product)

    # Generate report
    report = []
    report.append("# BRAND COMPETITIVE LANDSCAPE REPORT")
    report.append("## Garage Organization Category - Brand Intelligence for Market Entry")
    report.append("")
    report.append("**Prepared for:** Category Innovation Team, Marketing Strategy")
    report.append(f"**Dataset:** {len(products):,} products across 6 major retailers")
    report.append(f"**Brands Analyzed:** {len(brand_data)}")
    report.append("")
    report.append("---")
    report.append("")

    # Top brands by market presence
    top_brands = sorted(brand_data.items(), key=lambda x: x[1]['count'], reverse=True)[:30]

    report.append("## 1. TOP 30 BRANDS BY MARKET PRESENCE")
    report.append("")
    report.append("| Rank | Brand | Products | Avg Price | Primary Category | Retailer Presence |")
    report.append("|------|-------|----------|-----------|------------------|-------------------|")

    for i, (brand, data) in enumerate(top_brands, 1):
        avg_price = statistics.mean(data['prices']) if data['prices'] else 0
        primary_cat = data['categories'].most_common(1)[0][0] if data['categories'] else 'N/A'
        retailer_count = len(data['retailers'])

        report.append(f"| {i} | {brand} | {data['count']:,} | ${avg_price:.2f} | {primary_cat} | {retailer_count} retailers |")

    report.append("")
    report.append("---")
    report.append("")

    # Brand positioning analysis
    report.append("## 2. BRAND POSITIONING ANALYSIS")
    report.append("")

    # Categorize brands by price point
    budget_brands = []
    mid_brands = []
    premium_brands = []

    for brand, data in brand_data.items():
        if data['prices'] and data['count'] >= 5:  # Only brands with 5+ products
            avg_price = statistics.mean(data['prices'])
            if avg_price < 20:
                budget_brands.append((brand, avg_price, data['count']))
            elif avg_price < 60:
                mid_brands.append((brand, avg_price, data['count']))
            else:
                premium_brands.append((brand, avg_price, data['count']))

    report.append("### Budget Segment (<$20 avg)")
    report.append("")
    report.append("| Brand | Avg Price | Products |")
    report.append("|-------|-----------|----------|")
    for brand, price, count in sorted(budget_brands, key=lambda x: -x[2])[:10]:
        report.append(f"| {brand} | ${price:.2f} | {count} |")

    report.append("")
    report.append("### Mid-Market Segment ($20-$60 avg)")
    report.append("")
    report.append("| Brand | Avg Price | Products |")
    report.append("|-------|-----------|----------|")
    for brand, price, count in sorted(mid_brands, key=lambda x: -x[2])[:10]:
        report.append(f"| {brand} | ${price:.2f} | {count} |")

    report.append("")
    report.append("### Premium Segment (>$60 avg)")
    report.append("")
    report.append("| Brand | Avg Price | Products |")
    report.append("|-------|-----------|----------|")
    for brand, price, count in sorted(premium_brands, key=lambda x: -x[2])[:10]:
        report.append(f"| {brand} | ${price:.2f} | {count} |")

    report.append("")
    report.append("---")
    report.append("")

    # Retailer-exclusive brands
    report.append("## 3. RETAILER-EXCLUSIVE BRANDS (Strategic Importance)")
    report.append("")

    exclusive_brands = {}
    for brand, data in brand_data.items():
        if len(data['retailers']) == 1 and data['count'] >= 10:
            retailer = list(data['retailers'].keys())[0]
            if retailer not in exclusive_brands:
                exclusive_brands[retailer] = []
            exclusive_brands[retailer].append((brand, data['count'],
                statistics.mean(data['prices']) if data['prices'] else 0))

    for retailer in sorted(exclusive_brands.keys()):
        report.append(f"### {retailer} Exclusive Brands")
        report.append("")
        report.append("| Brand | Products | Avg Price |")
        report.append("|-------|----------|-----------|")
        for brand, count, price in sorted(exclusive_brands[retailer], key=lambda x: -x[1])[:5]:
            report.append(f"| {brand} | {count} | ${price:.2f} |")
        report.append("")

    report.append("---")
    report.append("")

    # Category specialization
    report.append("## 4. BRAND CATEGORY SPECIALIZATION")
    report.append("")
    report.append("**Workbench Specialists:**")
    workbench_brands = [(b, d['categories']['Workbenches']) for b, d in brand_data.items()
                        if d['categories']['Workbenches'] >= 5]
    for brand, count in sorted(workbench_brands, key=lambda x: -x[1])[:5]:
        report.append(f"- {brand}: {count} workbench products")

    report.append("")
    report.append("**Cabinet Specialists:**")
    cabinet_brands = [(b, d['categories']['Cabinets']) for b, d in brand_data.items()
                     if d['categories']['Cabinets'] >= 10]
    for brand, count in sorted(cabinet_brands, key=lambda x: -x[1])[:5]:
        report.append(f"- {brand}: {count} cabinet products")

    report.append("")
    report.append("**Shelving Specialists:**")
    shelving_brands = [(b, d['categories']['Shelving']) for b, d in brand_data.items()
                      if d['categories']['Shelving'] >= 10]
    for brand, count in sorted(shelving_brands, key=lambda x: -x[1])[:5]:
        report.append(f"- {brand}: {count} shelving products")

    report.append("")
    report.append("---")
    report.append("")

    # Strategic insights
    report.append("## 5. STRATEGIC INSIGHTS FOR MARKET ENTRY")
    report.append("")
    report.append("### White Space Opportunities")
    report.append("")
    report.append(f"- **Total brands:** {len(brand_data)}")
    report.append(f"- **Major brands (50+ products):** {len([b for b, d in brand_data.items() if d['count'] >= 50])}")
    report.append(f"- **Market fragmentation:** High - {len([b for b, d in brand_data.items() if d['count'] < 10])} brands with <10 products")
    report.append("")
    report.append("### Competitive Intensity by Segment")
    report.append(f"- Budget segment: {len(budget_brands)} brands competing")
    report.append(f"- Mid-market segment: {len(mid_brands)} brands competing")
    report.append(f"- Premium segment: {len(premium_brands)} brands competing (LESS CROWDED)")
    report.append("")
    report.append("### Recommended Entry Strategy")
    report.append("- **Target segment:** Premium ($60-150) - less competition, higher margins")
    report.append("- **Category focus:** Workbenches or Cabinets - specialist positioning")
    report.append("- **Retailer strategy:** Multi-retailer distribution (avoid exclusive dependency)")
    report.append("- **Brand positioning:** Quality/innovation vs commodity Chinese brands")

    return "\n".join(report)

# ============================================================================
# REPORT 2: PRICING INTELLIGENCE
# ============================================================================

def generate_pricing_report(products):
    """Generate comprehensive pricing intelligence report."""

    print("Generating Pricing Intelligence Report...")

    products_with_price = [p for p in products if p.get('price')]

    report = []
    report.append("# PRICING INTELLIGENCE REPORT")
    report.append("## Garage Organization Category - Competitive Pricing Analysis")
    report.append("")
    report.append("**Prepared for:** Pricing Team, Category Innovation Team")
    report.append(f"**Products Analyzed:** {len(products_with_price):,} with pricing data ({100*len(products_with_price)/len(products):.1f}% coverage)")
    report.append("")
    report.append("---")
    report.append("")

    # Overall price distribution
    all_prices = [p['price'] for p in products_with_price]
    report.append("## 1. OVERALL MARKET PRICE DISTRIBUTION")
    report.append("")
    report.append(f"- **Minimum Price:** ${min(all_prices):.2f}")
    report.append(f"- **Maximum Price:** ${max(all_prices):.2f}")
    report.append(f"- **Mean Price:** ${statistics.mean(all_prices):.2f}")
    report.append(f"- **Median Price:** ${statistics.median(all_prices):.2f}")
    report.append(f"- **25th Percentile:** ${sorted(all_prices)[len(all_prices)//4]:.2f}")
    report.append(f"- **75th Percentile:** ${sorted(all_prices)[3*len(all_prices)//4]:.2f}")
    report.append("")

    # Price tier distribution
    tier_counts = Counter()
    for p in products_with_price:
        tier = categorize_price_tier(p['price'])
        if tier:
            tier_counts[tier] += 1

    report.append("## 2. PRICE TIER DISTRIBUTION")
    report.append("")
    report.append("| Price Tier | Products | % of Market | Strategic Notes |")
    report.append("|------------|----------|-------------|-----------------|")
    report.append(f"| Budget (<$15) | {tier_counts['Budget (<$15)']:,} | {100*tier_counts['Budget (<$15)']/len(products_with_price):.1f}% | High volume, low margin, commodity |")
    report.append(f"| Mid-Market ($15-$50) | {tier_counts['Mid-Market ($15-$50)']:,} | {100*tier_counts['Mid-Market ($15-$50)']/len(products_with_price):.1f}% | Sweet spot, balanced value |")
    report.append(f"| Premium ($50-$150) | {tier_counts['Premium ($50-$150)']:,} | {100*tier_counts['Premium ($50-$150)']/len(products_with_price):.1f}% | Quality differentiation opportunity |")
    report.append(f"| Luxury (>$150) | {tier_counts['Luxury (>$150)']:,} | {100*tier_counts['Luxury (>$150)']/len(products_with_price):.1f}% | Cabinets/workbenches, niche |")
    report.append("")
    report.append("---")
    report.append("")

    # Category pricing
    report.append("## 3. PRICING BY PRODUCT CATEGORY")
    report.append("")

    category_prices = defaultdict(list)
    for p in products_with_price:
        name = p.get('name') or p.get('title', '')
        category = categorize_product(name)
        category_prices[category].append(p['price'])

    report.append("| Category | Avg Price | Median | Min | Max | Products |")
    report.append("|----------|-----------|--------|-----|-----|----------|")

    for category in sorted(category_prices.keys()):
        prices = category_prices[category]
        report.append(f"| {category} | ${statistics.mean(prices):.2f} | ${statistics.median(prices):.2f} | ${min(prices):.2f} | ${max(prices):.2f} | {len(prices)} |")

    report.append("")
    report.append("---")
    report.append("")

    # Retailer pricing
    report.append("## 4. PRICING BY RETAILER")
    report.append("")

    retailer_prices = defaultdict(list)
    for p in products_with_price:
        retailer = p.get('retailer', 'Unknown')
        retailer_prices[retailer].append(p['price'])

    report.append("| Retailer | Avg Price | Median | Price Range | Products | Positioning |")
    report.append("|----------|-----------|--------|-------------|----------|-------------|")

    for retailer in sorted(retailer_prices.keys()):
        prices = retailer_prices[retailer]
        avg = statistics.mean(prices)
        positioning = "Budget" if avg < 25 else "Mid" if avg < 40 else "Premium"
        report.append(f"| {retailer} | ${avg:.2f} | ${statistics.median(prices):.2f} | ${min(prices):.2f}-${max(prices):.2f} | {len(prices)} | {positioning} |")

    report.append("")
    report.append("---")
    report.append("")

    # Competitive pricing benchmarks
    report.append("## 5. COMPETITIVE PRICING BENCHMARKS")
    report.append("")
    report.append("### Recommended Entry Price Points by Category")
    report.append("")

    for category in ['Workbenches', 'Cabinets', 'Shelving', 'Bins & Containers']:
        if category in category_prices and len(category_prices[category]) > 10:
            prices = category_prices[category]
            p25 = sorted(prices)[len(prices)//4]
            p50 = statistics.median(prices)
            p75 = sorted(prices)[3*len(prices)//4]

            report.append(f"**{category}:**")
            report.append(f"- Competitive (match market): ${p50:.2f}")
            report.append(f"- Value positioning: ${p25:.2f}-${p50:.2f}")
            report.append(f"- Premium positioning: ${p75:.2f}+")
            report.append("")

    report.append("---")
    report.append("")

    # Strategic pricing recommendations
    report.append("## 6. STRATEGIC PRICING RECOMMENDATIONS")
    report.append("")
    report.append("### Market Entry Pricing Strategy")
    report.append("")
    report.append("**Budget Segment (<$15):**")
    report.append("- ❌ NOT RECOMMENDED: Overcrowded, low margin, commodity competition")
    report.append("- Chinese generic brands dominate this segment")
    report.append("")
    report.append("**Mid-Market ($15-$50):**")
    report.append("- ✅ VIABLE: Largest segment, balanced value proposition")
    report.append("- Opportunity: Quality at competitive price vs generics")
    report.append("- Recommended: $25-45 sweet spot for differentiated products")
    report.append("")
    report.append("**Premium ($50-$150):**")
    report.append("- ✅ RECOMMENDED: Less competition, higher margins")
    report.append("- Strong opportunity for innovation and quality positioning")
    report.append("- Recommended: $75-125 for cabinets/workbenches")
    report.append("")
    report.append("### Price-to-Value Gap Analysis")
    report.append("")
    report.append(f"- Market average: ${statistics.mean(all_prices):.2f}")
    report.append(f"- Consumer expectation (median): ${statistics.median(all_prices):.2f}")
    report.append(f"- Premium threshold: ${sorted(all_prices)[3*len(all_prices)//4]:.2f}")
    report.append("")
    report.append("**Recommendation:** Enter at 10-15% premium to median with clear value differentiation")

    return "\n".join(report)

# ============================================================================
# REPORT 3: RETAILER MARKET ANALYSIS
# ============================================================================

def generate_retailer_report(products):
    """Generate comprehensive retailer market analysis."""

    print("Generating Retailer Market Analysis Report...")

    report = []
    report.append("# RETAILER MARKET ANALYSIS REPORT")
    report.append("## Garage Organization Category - Distribution & Partnership Intelligence")
    report.append("")
    report.append("**Prepared for:** Category Innovation Team, Sales & Distribution Strategy")
    report.append(f"**Products Analyzed:** {len(products):,}")
    report.append("")
    report.append("---")
    report.append("")

    # Retailer market share
    retailer_data = defaultdict(lambda: {
        'count': 0,
        'categories': Counter(),
        'brands': set(),
        'prices': [],
        'products': []
    })

    for product in products:
        retailer = product.get('retailer', 'Unknown')
        name = product.get('name') or product.get('title', '')
        category = categorize_product(name)
        brand = product.get('brand')
        price = product.get('price')

        retailer_data[retailer]['count'] += 1
        retailer_data[retailer]['categories'][category] += 1
        if brand:
            retailer_data[retailer]['brands'].add(brand)
        if price:
            retailer_data[retailer]['prices'].append(price)
        retailer_data[retailer]['products'].append(product)

    report.append("## 1. RETAILER MARKET SHARE")
    report.append("")
    report.append("| Retailer | Products | Market Share | Avg Price | Brands | Strategic Importance |")
    report.append("|----------|----------|--------------|-----------|--------|---------------------|")

    for retailer in sorted(retailer_data.keys(), key=lambda x: retailer_data[x]['count'], reverse=True):
        data = retailer_data[retailer]
        share = 100 * data['count'] / len(products)
        avg_price = statistics.mean(data['prices']) if data['prices'] else 0
        importance = "Critical" if share > 20 else "High" if share > 5 else "Medium"
        report.append(f"| {retailer} | {data['count']:,} | {share:.1f}% | ${avg_price:.2f} | {len(data['brands'])} | {importance} |")

    report.append("")
    report.append("---")
    report.append("")

    # Category emphasis by retailer
    report.append("## 2. CATEGORY ASSORTMENT BY RETAILER")
    report.append("")

    for retailer in sorted(retailer_data.keys(), key=lambda x: retailer_data[x]['count'], reverse=True):
        if retailer_data[retailer]['count'] < 100:
            continue

        report.append(f"### {retailer}")
        report.append("")
        report.append("| Category | Products | % of Assortment |")
        report.append("|----------|----------|----------------|")

        total = retailer_data[retailer]['count']
        for category, count in retailer_data[retailer]['categories'].most_common(6):
            pct = 100 * count / total
            report.append(f"| {category} | {count:,} | {pct:.1f}% |")
        report.append("")

    report.append("---")
    report.append("")

    # Retailer pricing strategies
    report.append("## 3. RETAILER PRICING STRATEGIES")
    report.append("")

    for retailer in sorted(retailer_data.keys()):
        data = retailer_data[retailer]
        if not data['prices']:
            continue

        prices = data['prices']
        budget = len([p for p in prices if p < 15])
        mid = len([p for p in prices if 15 <= p < 50])
        premium = len([p for p in prices if 50 <= p < 150])
        luxury = len([p for p in prices if p >= 150])
        total_priced = len(prices)

        report.append(f"### {retailer}")
        report.append(f"- Average Price: ${statistics.mean(prices):.2f}")
        report.append(f"- Price Distribution:")
        report.append(f"  - Budget (<$15): {100*budget/total_priced:.1f}%")
        report.append(f"  - Mid ($15-$50): {100*mid/total_priced:.1f}%")
        report.append(f"  - Premium ($50-$150): {100*premium/total_priced:.1f}%")
        report.append(f"  - Luxury (>$150): {100*luxury/total_priced:.1f}%")
        report.append("")

    report.append("---")
    report.append("")

    # Distribution opportunities
    report.append("## 4. DISTRIBUTION STRATEGY RECOMMENDATIONS")
    report.append("")
    report.append("### Primary Distribution Targets (Launch Partners)")
    report.append("")

    walmart = retailer_data.get('Walmart', {})
    homedepot = retailer_data.get('Home Depot', {})
    lowes = retailer_data.get('Lowes', {})

    report.append("**1. Walmart** (78.7% market share)")
    report.append("- ✅ CRITICAL: Largest assortment, mass market reach")
    report.append("- Average price: $" + f"{statistics.mean(walmart['prices']):.2f}" if walmart.get('prices') else "N/A")
    report.append("- Strategy: Launch with 3-5 SKUs in mid-market segment ($25-45)")
    report.append("")

    report.append("**2. Home Depot** (10.6% market share)")
    report.append("- ✅ HIGH PRIORITY: DIY/Pro audience, quality focus")
    report.append("- Average price: $" + f"{statistics.mean(homedepot['prices']):.2f}" if homedepot.get('prices') else "N/A")
    report.append("- Strategy: Premium positioning, workbench/cabinet focus")
    report.append("")

    report.append("**3. Lowes** (4.0% market share)")
    report.append("- ✅ STRATEGIC: Growing category, less crowded than Home Depot")
    report.append("- Average price: $" + f"{statistics.mean(lowes['prices']):.2f}" if lowes.get('prices') else "N/A")
    report.append("- Strategy: Partnership opportunity, exclusive SKUs possible")
    report.append("")

    report.append("### Secondary/Future Targets")
    report.append("- **Amazon** (4.6%): Online expansion after retail validation")
    report.append("- **Target** (1.2%): Design-forward, lifestyle positioning")
    report.append("- **Etsy** (0.9%): Artisanal/custom offerings (different business model)")
    report.append("")
    report.append("---")
    report.append("")

    # Strategic insights
    report.append("## 5. KEY STRATEGIC INSIGHTS")
    report.append("")
    report.append("### Market Entry Recommendations")
    report.append("")
    report.append("**Phase 1: Initial Launch (Months 1-6)**")
    report.append("- Lead retailer: Walmart (3-5 SKUs, $25-45 price range)")
    report.append("- Secondary: Home Depot (2-3 premium SKUs, $75-125)")
    report.append("- Focus: Cabinets OR Workbenches (specialist positioning)")
    report.append("")
    report.append("**Phase 2: Expansion (Months 6-12)**")
    report.append("- Add Lowes partnership (exclusive SKU opportunity)")
    report.append("- Expand SKU count at existing retailers")
    report.append("- Add complementary categories")
    report.append("")
    report.append("**Phase 3: Optimization (Year 2+)**")
    report.append("- Amazon launch for online growth")
    report.append("- Target for design-conscious consumers")
    report.append("- Evaluate regional retailers (Menards, Ace)")
    report.append("")
    report.append("### Competitive Advantages to Leverage")
    report.append("- **Quality vs Chinese generics:** Premium materials, better design")
    report.append("- **Innovation:** Features missing from current market")
    report.append("- **Brand story:** American/quality narrative vs commodity")
    report.append("- **Multi-retailer:** Avoid exclusive lock-in, maximize reach")

    return "\n".join(report)

def main():
    print("="*70)
    print("GENERATING CATEGORY INTELLIGENCE REPORTS")
    print("="*70)
    print()

    products = load_data()
    print(f"Loaded {len(products):,} products")
    print()

    # Generate all 3 reports
    brand_report = generate_brand_report(products)
    pricing_report = generate_pricing_report(products)
    retailer_report = generate_retailer_report(products)

    # Save reports
    with open(OUTPUT_DIR / "BRAND_COMPETITIVE_LANDSCAPE.md", 'w') as f:
        f.write(brand_report)
    print("✓ Saved BRAND_COMPETITIVE_LANDSCAPE.md")

    with open(OUTPUT_DIR / "PRICING_INTELLIGENCE_REPORT.md", 'w') as f:
        f.write(pricing_report)
    print("✓ Saved PRICING_INTELLIGENCE_REPORT.md")

    with open(OUTPUT_DIR / "RETAILER_MARKET_ANALYSIS.md", 'w') as f:
        f.write(retailer_report)
    print("✓ Saved RETAILER_MARKET_ANALYSIS.md")

    print()
    print("="*70)
    print("✅ ALL 3 INTELLIGENCE REPORTS GENERATED")
    print("="*70)

if __name__ == "__main__":
    main()
