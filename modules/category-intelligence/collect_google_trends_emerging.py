#!/usr/bin/env python3
"""
GOOGLE TRENDS - EMERGING PRODUCT DISCOVERY
Identifies spiking search terms and early trend indicators

Strategic Focus:
- Keywords with rising momentum (not yet mainstream)
- Related queries that reveal unknown product categories
- Geographic origins of trends
- Comparison to identify gaps vs mainstream retail
"""

import json
import time
from pathlib import Path
from pytrends.request import TrendReq
from datetime import datetime

print("="*80)
print("GOOGLE TRENDS - EMERGING PRODUCT DISCOVERY")
print("Identifying spiking keywords and early trend indicators")
print("="*80)
print()

# Initialize pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# Keywords from our analysis + exploratory terms
PRIMARY_KEYWORDS = [
    'french cleat',
    'slatwall',
    'overhead garage storage',
    'garage makeover',
    'pegboard garage'
]

# Broader category terms for discovery
DISCOVERY_KEYWORDS = [
    'garage organization',
    'garage storage',
    'garage hooks',
    'garage shelving',
    'garage ceiling storage'
]

# Budget marketplace indicators
BUDGET_INDICATORS = [
    'cheap garage storage',
    'diy garage organization',
    'affordable garage shelving',
    'garage organization ideas'
]

def get_interest_over_time(keywords, timeframe='today 12-m'):
    """Get search interest over time."""
    try:
        pytrends.build_payload(keywords, timeframe=timeframe)
        data = pytrends.interest_over_time()
        return data
    except Exception as e:
        print(f"   ⚠️  Error getting interest over time: {str(e)[:100]}")
        return None

def get_related_queries(keyword):
    """Get related and rising queries for a keyword."""
    try:
        pytrends.build_payload([keyword], timeframe='today 12-m')
        related = pytrends.related_queries()
        return related
    except Exception as e:
        print(f"   ⚠️  Error getting related queries for '{keyword}': {str(e)[:100]}")
        return None

def get_regional_interest(keywords):
    """Get geographic distribution of interest."""
    try:
        pytrends.build_payload(keywords, timeframe='today 12-m')
        regional = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True)
        return regional
    except Exception as e:
        print(f"   ⚠️  Error getting regional interest: {str(e)[:100]}")
        return None

results = {
    "collected_at": datetime.now().isoformat(),
    "purpose": "emerging_trend_discovery",
    "data": {
        "primary_keywords": {},
        "discovery_keywords": {},
        "budget_indicators": {},
        "rising_opportunities": []
    }
}

# Analyze primary keywords (our identified opportunities)
print("PHASE 1: PRIMARY KEYWORD TREND ANALYSIS")
print("-" * 80)
print()

for keyword in PRIMARY_KEYWORDS:
    print(f"Analyzing: '{keyword}'")

    # Get interest over time
    interest = get_interest_over_time([keyword])

    # Get related/rising queries
    related = get_related_queries(keyword)

    if interest is not None and not interest.empty:
        # Calculate trend direction
        recent_avg = interest[keyword].iloc[-4:].mean()  # Last month
        earlier_avg = interest[keyword].iloc[:4].mean()  # First month

        if earlier_avg > 0:
            trend_change = ((recent_avg - earlier_avg) / earlier_avg) * 100
        else:
            trend_change = 100 if recent_avg > 0 else 0

        print(f"   📈 Trend: {trend_change:+.1f}% (12-month change)")
        print(f"   📊 Recent interest: {int(recent_avg)}/100")

        # Convert timestamps to strings for JSON serialization
        interest_dict = {str(k): v for k, v in interest[keyword].to_dict().items()}

        results["data"]["primary_keywords"][keyword] = {
            "trend_change_pct": round(trend_change, 1),
            "recent_interest": int(recent_avg),
            "earlier_interest": int(earlier_avg),
            "peak_interest": int(interest[keyword].max()),
            "interest_over_time": interest_dict
        }

    if related is not None and keyword in related:
        # Rising queries (these are spiking)
        if 'rising' in related[keyword] and related[keyword]['rising'] is not None:
            rising = related[keyword]['rising']
            if not rising.empty:
                print(f"   🚀 Rising queries ({len(rising)}):")
                for i, row in rising.head(5).iterrows():
                    value = row['value']
                    query = row['query']
                    if value == 'Breakout':
                        print(f"      • {query} → BREAKOUT")
                    else:
                        print(f"      • {query} → +{value}%")

                results["data"]["primary_keywords"][keyword]["rising_queries"] = rising.to_dict('records')

        # Top related queries
        if 'top' in related[keyword] and related[keyword]['top'] is not None:
            top = related[keyword]['top']
            if not top.empty:
                results["data"]["primary_keywords"][keyword]["top_related"] = top.to_dict('records')

    print()
    time.sleep(2)  # Rate limiting

# Discovery phase - broader terms to find new categories
print("PHASE 2: DISCOVERY KEYWORD ANALYSIS")
print("-" * 80)
print()

all_rising_queries = []

for keyword in DISCOVERY_KEYWORDS:
    print(f"Discovering from: '{keyword}'")

    related = get_related_queries(keyword)

    if related is not None and keyword in related:
        if 'rising' in related[keyword] and related[keyword]['rising'] is not None:
            rising = related[keyword]['rising']
            if not rising.empty:
                print(f"   🔍 Found {len(rising)} rising queries")

                # Collect all rising queries for deduplication
                for i, row in rising.iterrows():
                    all_rising_queries.append({
                        'query': row['query'],
                        'value': row['value'],
                        'source_keyword': keyword
                    })

                # Show top 3 breakouts
                breakouts = rising[rising['value'] == 'Breakout']
                if not breakouts.empty:
                    print(f"   ⚡ Breakout terms:")
                    for i, row in breakouts.head(3).iterrows():
                        print(f"      • {row['query']}")

        results["data"]["discovery_keywords"][keyword] = {
            "rising_queries": rising.to_dict('records') if related and 'rising' in related[keyword] and related[keyword]['rising'] is not None else [],
            "top_queries": top.to_dict('records') if related and 'top' in related[keyword] and related[keyword]['top'] is not None else []
        }

    print()
    time.sleep(2)

# Budget marketplace indicators
print("PHASE 3: BUDGET MARKETPLACE SIGNALS")
print("-" * 80)
print()

for keyword in BUDGET_INDICATORS:
    print(f"Analyzing budget trend: '{keyword}'")

    interest = get_interest_over_time([keyword])

    if interest is not None and not interest.empty:
        recent_avg = interest[keyword].iloc[-4:].mean()
        print(f"   💰 Interest level: {int(recent_avg)}/100")

        # Convert timestamps to strings for JSON serialization
        interest_dict = {str(k): v for k, v in interest[keyword].to_dict().items()}

        results["data"]["budget_indicators"][keyword] = {
            "recent_interest": int(recent_avg),
            "interest_over_time": interest_dict
        }

    time.sleep(2)

# Identify top rising opportunities (deduplicated)
print()
print("PHASE 4: TOP RISING OPPORTUNITIES")
print("-" * 80)
print()

# Deduplicate and rank rising queries
from collections import Counter
rising_query_counts = Counter([q['query'] for q in all_rising_queries])

# Focus on queries that appear multiple times (cross-validated trends)
top_rising = []
for query, count in rising_query_counts.most_common(30):
    # Get value (Breakout or percentage)
    matching = [q for q in all_rising_queries if q['query'] == query]
    values = [q['value'] for q in matching]

    # Prioritize Breakout
    if 'Breakout' in values:
        top_rising.append({
            'query': query,
            'status': 'Breakout',
            'sources': count,
            'source_keywords': list(set([q['source_keyword'] for q in matching]))
        })
    else:
        # Get max percentage increase
        numeric_values = [v for v in values if v != 'Breakout' and isinstance(v, (int, float))]
        if numeric_values:
            top_rising.append({
                'query': query,
                'status': f"+{max(numeric_values)}%",
                'sources': count,
                'source_keywords': list(set([q['source_keyword'] for q in matching]))
            })

results["data"]["rising_opportunities"] = top_rising

print("🚀 TOP CROSS-VALIDATED RISING QUERIES:")
print()
for i, item in enumerate(top_rising[:20], 1):
    print(f"{i:2d}. '{item['query']}' → {item['status']}")
    print(f"    Validated across {item['sources']} keyword(s): {', '.join(item['source_keywords'])}")
    print()

# Save results
output_file = Path(__file__).parent / "data" / "google_trends_emerging_products.json"
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print()
print("="*80)
print("GOOGLE TRENDS ANALYSIS COMPLETE")
print("="*80)
print(f"Saved to: {output_file.name}")
print()
print("KEY INSIGHTS:")
print(f"  • {len(PRIMARY_KEYWORDS)} primary keywords analyzed")
print(f"  • {len(DISCOVERY_KEYWORDS)} discovery keywords explored")
print(f"  • {len(top_rising)} rising opportunities identified")
print(f"  • {len([q for q in top_rising if q['status'] == 'Breakout'])} BREAKOUT terms found")
print()
print("NEXT STEP: Compare with Amazon/retailer data to find gaps")
print("="*80)
