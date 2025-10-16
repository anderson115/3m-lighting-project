#!/usr/bin/env python3
"""
Test script to count total sources from all collectors.
"""
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from core.config import config
from collectors.brand_discovery import BrandDiscovery
from collectors.market_researcher import MarketResearcher
from collectors.pricing_analyzer import PricingAnalyzer
from collectors.resource_curator import ResourceCurator

def count_sources():
    """Run collectors and count unique sources."""
    category = "garage storage"
    all_sources = set()

    print(f"\n{'='*60}")
    print(f"SOURCE COUNT TEST - {category}")
    print(f"{'='*60}\n")

    # Test 1: Brand Discovery
    try:
        print("1️⃣ Testing Brand Discovery...")
        brand_disco = BrandDiscovery(config)
        brand_result = brand_disco.discover_brands(category)

        brand_sources = set()
        for brand in brand_result.get('brands', []):
            for url in brand.get('source_urls', []):
                brand_sources.add(url)

        all_sources.update(brand_sources)
        print(f"   ✅ Brand Discovery: {len(brand_sources)} sources")
        print(f"   Brands found: {brand_result.get('total_brands', 0)}")
    except Exception as e:
        print(f"   ❌ Brand Discovery failed: {e}")

    # Test 2: Market Research
    try:
        print("\n2️⃣ Testing Market Researcher...")
        researcher = MarketResearcher(config)
        market_result = researcher.research_market(category)

        market_sources = set()
        for source in market_result.get('sources', []):
            market_sources.add(source.get('url', ''))

        all_sources.update(market_sources)
        print(f"   ✅ Market Researcher: {len(market_sources)} sources")
    except Exception as e:
        print(f"   ❌ Market Researcher failed: {e}")

    # Test 3: Pricing Analysis
    try:
        print("\n3️⃣ Testing Pricing Analyzer...")
        analyzer = PricingAnalyzer(config)
        pricing_result = analyzer.analyze_pricing(category)

        pricing_sources = set()
        for source in pricing_result.get('sources', []):
            pricing_sources.add(source.get('url', ''))

        all_sources.update(pricing_sources)
        print(f"   ✅ Pricing Analyzer: {len(pricing_sources)} sources")
        print(f"   Subcategories: {pricing_result.get('total_subcategories', 0)}")
    except Exception as e:
        print(f"   ❌ Pricing Analyzer failed: {e}")

    # Test 4: Resource Curation
    try:
        print("\n4️⃣ Testing Resource Curator...")
        curator = ResourceCurator(config)
        resource_result = curator.find_resources(category)

        resource_sources = set()
        for source in resource_result.get('sources', []):
            resource_sources.add(source.get('url', ''))

        all_sources.update(resource_sources)
        print(f"   ✅ Resource Curator: {len(resource_sources)} sources")
        print(f"   Resources found: {resource_result.get('total_resources', 0)}")
    except Exception as e:
        print(f"   ❌ Resource Curator failed: {e}")

    # Summary
    print(f"\n{'='*60}")
    print(f"TOTAL UNIQUE SOURCES: {len(all_sources)}")
    print(f"{'='*60}")

    if len(all_sources) >= 100:
        print("✅ PASSED: 100+ sources threshold met!")
    else:
        print(f"⚠️  Need {100 - len(all_sources)} more sources for preflight")

    print(f"\nSource URLs:")
    for i, url in enumerate(sorted(all_sources), 1):
        print(f"  {i}. {url}")

if __name__ == "__main__":
    count_sources()
