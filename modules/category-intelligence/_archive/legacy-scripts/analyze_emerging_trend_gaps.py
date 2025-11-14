#!/usr/bin/env python3
"""
EMERGING TREND GAP ANALYSIS
Identifies products spiking on Google Trends but underserved by mainstream retailers

KEY INSIGHT: Products trending in search but with low Amazon/retailer availability
represent early-stage opportunities (like Temu/Alibaba products before they hit mainstream)

Analysis:
1. Load Google Trends rising queries
2. Search retailer data for product availability
3. Calculate "Gap Score" = (Search Trend Momentum) / (Retailer Product Count)
4. Identify high-gap opportunities (trending demand, low supply)
"""

import json
from pathlib import Path
from collections import defaultdict

print("="*80)
print("EMERGING TREND GAP ANALYSIS")
print("Finding Google Trends spikes with low retailer availability")
print("="*80)
print()

# Load Google Trends data
trends_file = Path(__file__).parent / "data" / "google_trends_emerging_products.json"
with open(trends_file) as f:
    trends_data = json.load(f)

# Load retailer product data
products_file = Path(__file__).parent / "data" / "garage_organizers_final_with_workbenches.json"
with open(products_file) as f:
    products_data = json.load(f)

if isinstance(products_data, dict) and 'products' in products_data:
    products = products_data['products']
else:
    products = products_data

print(f"Loaded {len(products):,} retailer products")
print()

# Extract all rising queries
all_rising = []

# From primary keywords
for keyword, data in trends_data['data']['primary_keywords'].items():
    if 'rising_queries' in data:
        for query in data['rising_queries']:
            all_rising.append({
                'query': query['query'],
                'value': query['value'],
                'source': f"Primary: {keyword}",
                'category': 'primary'
            })

# From discovery keywords
for keyword, data in trends_data['data']['discovery_keywords'].items():
    if 'rising_queries' in data:
        for query in data['rising_queries']:
            all_rising.append({
                'query': query['query'],
                'value': query['value'],
                'source': f"Discovery: {keyword}",
                'category': 'discovery'
            })

print(f"Analyzing {len(all_rising)} rising search queries")
print()

# For each rising query, count matching products in retailer data
gap_analysis = []

for item in all_rising:
    query = item['query'].lower()
    query_words = query.split()

    # Count products that match this query
    matching_products = 0
    for product in products:
        name = (product.get('name') or product.get('title', '')).lower()
        desc = str(product.get('description', '')).lower()

        # Check if all query words appear in product name or description
        if all(word in name or word in desc for word in query_words):
            matching_products += 1

    # Calculate gap score
    # Higher value = more trending
    # Lower matching products = bigger gap
    if item['value'] == 'Breakout':
        trend_score = 1000  # Breakout gets maximum score
    else:
        try:
            trend_score = int(item['value'].replace('+', '').replace('%', ''))
        except:
            trend_score = 0

    # Gap score: high trend with low product count = opportunity
    if matching_products == 0:
        gap_score = trend_score  # Maximum gap
    else:
        gap_score = trend_score / (matching_products + 1)  # Normalize by product count

    gap_analysis.append({
        'query': item['query'],
        'trend_value': item['value'],
        'trend_score': trend_score,
        'product_count': matching_products,
        'gap_score': round(gap_score, 2),
        'source': item['source'],
        'category': item['category'],
        'opportunity_type': 'HIGH' if gap_score > 50 and matching_products < 10 else
                           'MEDIUM' if gap_score > 20 and matching_products < 50 else 'LOW'
    })

# Sort by gap score (highest = best opportunity)
gap_analysis.sort(key=lambda x: x['gap_score'], reverse=True)

print("="*80)
print("TOP EMERGING TREND OPPORTUNITIES (High Search Demand, Low Retailer Supply)")
print("="*80)
print()

print("🚀 TIER 1: BREAKOUT OPPORTUNITIES (Spiking searches, minimal products)")
print("-" * 80)
tier1 = [g for g in gap_analysis if g['opportunity_type'] == 'HIGH']
for i, gap in enumerate(tier1[:10], 1):
    print(f"{i:2d}. \"{gap['query']}\"")
    print(f"    Google Trend: {gap['trend_value']}")
    print(f"    Retailer products: {gap['product_count']}")
    print(f"    Gap Score: {gap['gap_score']:.1f}")
    print(f"    → {gap['source']}")
    print()

print()
print("⭐ TIER 2: STRONG OPPORTUNITIES (Growing searches, underserved)")
print("-" * 80)
tier2 = [g for g in gap_analysis if g['opportunity_type'] == 'MEDIUM']
for i, gap in enumerate(tier2[:10], 1):
    print(f"{i:2d}. \"{gap['query']}\"")
    print(f"    Google Trend: {gap['trend_value']}")
    print(f"    Retailer products: {gap['product_count']}")
    print(f"    Gap Score: {gap['gap_score']:.1f}")
    print()

# Identify product categories with gaps
print()
print("="*80)
print("PRODUCT CATEGORY GAP ANALYSIS")
print("="*80)
print()

category_patterns = {
    'Installation Services': ['installation', 'install service', 'professional install'],
    'Double/Two-Car Garage': ['double garage', 'two car garage', '2 car garage'],
    'Brand-Specific': ['richelieu', 'lifetime', 'gladiator', 'rubbermaid'],
    'Custom/Premium': ['custom garage', 'custom storage', 'premium garage'],
    'Local Services': ['near me', 'garage organization company', 'installation service'],
    'Budget Solutions': ['cheap', 'affordable', 'budget garage']
}

for category, patterns in category_patterns.items():
    category_gaps = []
    for gap in gap_analysis:
        if any(pattern in gap['query'].lower() for pattern in patterns):
            category_gaps.append(gap)

    if category_gaps:
        top_gap = category_gaps[0]
        print(f"📦 {category}")
        print(f"   Top opportunity: \"{top_gap['query']}\"")
        print(f"   Trend: {top_gap['trend_value']} | Products: {top_gap['product_count']} | Gap: {top_gap['gap_score']:.1f}")
        print(f"   Total related queries: {len(category_gaps)}")
        print()

# Specific product opportunities
print("="*80)
print("SPECIFIC PRODUCT OPPORTUNITIES")
print("="*80)
print()

print("These are SPECIFIC products/brands trending in search with minimal retailer presence:")
print()

specific_products = [
    g for g in gap_analysis
    if g['product_count'] == 0 and g['trend_score'] > 50
]

for i, gap in enumerate(specific_products[:15], 1):
    print(f"{i:2d}. \"{gap['query']}\" → {gap['trend_value']}")
    print(f"    Gap Score: {gap['gap_score']:.1f} (NO matching products found)")
    print()

# Save results
output_data = {
    "analysis_type": "emerging_trend_gaps",
    "methodology": "Google Trends rising queries vs retailer product availability",
    "total_queries_analyzed": len(all_rising),
    "total_retailer_products": len(products),
    "tier1_opportunities": [g for g in gap_analysis if g['opportunity_type'] == 'HIGH'],
    "tier2_opportunities": [g for g in gap_analysis if g['opportunity_type'] == 'MEDIUM'],
    "all_gaps": gap_analysis,
    "category_insights": {
        category: {
            "total_queries": len([g for g in gap_analysis if any(p in g['query'].lower() for p in patterns)]),
            "avg_gap_score": round(
                sum(g['gap_score'] for g in gap_analysis if any(p in g['query'].lower() for p in patterns)) /
                max(len([g for g in gap_analysis if any(p in g['query'].lower() for p in patterns)]), 1),
                2
            )
        }
        for category, patterns in category_patterns.items()
    }
}

output_file = Path(__file__).parent / "outputs" / "emerging_trend_gap_analysis.json"
output_file.parent.mkdir(exist_ok=True)
with open(output_file, 'w') as f:
    json.dump(output_data, f, indent=2)

print()
print("="*80)
print("GAP ANALYSIS COMPLETE")
print("="*80)
print(f"Saved to: {output_file.name}")
print()
print("STRATEGIC INSIGHTS:")
print(f"  • Tier 1 (HIGH) opportunities: {len(tier1)}")
print(f"  • Tier 2 (MEDIUM) opportunities: {len(tier2)}")
print(f"  • Specific products with zero retailer presence: {len(specific_products)}")
print()
print("KEY TAKEAWAY:")
print("  These are the 'Temu/Alibaba opportunities' - products trending in search")
print("  but not yet widely available on Amazon/mainstream retailers.")
print("  Early movers who source/list these products will capture emerging demand.")
print("="*80)
