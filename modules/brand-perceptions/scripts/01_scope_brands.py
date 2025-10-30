#!/usr/bin/env python3
"""
Phase 1: Brand Portfolio Scoping

Identify 3M brands with potential garage organization relevance.
Outputs a prioritized list of 5-8 brands with rationale.
"""

import yaml
from pathlib import Path

print("=" * 80)
print("PHASE 1: BRAND PORTFOLIO SCOPING")
print("=" * 80)

# 3M Consumer Brand Portfolio - Initial Research
brands_research = [
    {
        "name": "Command",
        "category": "Damage-free hanging & mounting",
        "heritage": "DIY, home organization, wall mounting",
        "technology": "Removable adhesive strips",
        "garage_relevance": "HIGH - Direct applicability to tool/equipment hanging",
        "consumer_association": "Strong DIY/homeowner brand equity"
    },
    {
        "name": "Scotch",
        "category": "Adhesive tapes & fastening",
        "heritage": "General purpose adhesive, mounting, packaging",
        "technology": "Pressure-sensitive adhesives",
        "garage_relevance": "MEDIUM - Heavy-duty variants, mounting applications",
        "consumer_association": "Trusted adhesive technology, multi-purpose"
    },
    {
        "name": "Filtrete",
        "category": "Air & water filtration",
        "heritage": "Home comfort, air quality",
        "technology": "3M filtration technology",
        "garage_relevance": "LOW - Limited direct relevance (air quality?)",
        "consumer_association": "Clean air, home comfort"
    },
    {
        "name": "Post-it",
        "category": "Note-taking & organization",
        "heritage": "Office/home organization, productivity",
        "technology": "Repositionable adhesive",
        "garage_relevance": "LOW-MEDIUM - Organization brand, but non-physical storage",
        "consumer_association": "Organization, productivity, planning"
    },
    {
        "name": "Scotch-Brite",
        "category": "Cleaning & surface prep",
        "heritage": "Scrubbing, cleaning, surface maintenance",
        "technology": "Abrasive materials",
        "garage_relevance": "MEDIUM - Garage cleaning, tool maintenance",
        "consumer_association": "Cleaning, scrubbing, maintenance"
    },
    {
        "name": "Scotchgard",
        "category": "Fabric & surface protection",
        "heritage": "Stain protection, waterproofing",
        "technology": "Protective coatings",
        "garage_relevance": "LOW-MEDIUM - Surface protection for stored items",
        "consumer_association": "Protection, preservation"
    },
    {
        "name": "O-Cel-O",
        "category": "Sponges & cleaning",
        "heritage": "Kitchen & household cleaning",
        "technology": "Cellulose sponges",
        "garage_relevance": "LOW - Limited garage applicability",
        "consumer_association": "Cleaning, kitchen"
    },
    {
        "name": "Nexcare",
        "category": "First aid & bandages",
        "heritage": "Healthcare, wound care",
        "technology": "Medical adhesives",
        "garage_relevance": "VERY LOW - No direct garage relevance",
        "consumer_association": "First aid, healthcare"
    }
]

print("\n" + "=" * 80)
print("BRAND EVALUATION CRITERIA")
print("=" * 80)
print("\n1. Adhesive/mounting/organization heritage")
print("2. Consumer association with DIY/home improvement/storage")
print("3. Core technology applicable to garage problems")

print("\n" + "=" * 80)
print("BRAND SCREENING")
print("=" * 80)

# Apply filters
filtered_brands = []
for brand in brands_research:
    # Relevance filter
    relevance_score = 0
    if "HIGH" in brand["garage_relevance"]:
        relevance_score = 3
    elif "MEDIUM" in brand["garage_relevance"]:
        relevance_score = 2
    elif "LOW-MEDIUM" in brand["garage_relevance"]:
        relevance_score = 1

    # Technology filter
    tech_match = any(keyword in brand["technology"].lower() for keyword in ["adhesive", "mounting", "fastening", "protective"])

    # Only include if relevance >= 2 OR (relevance == 1 AND tech_match)
    if relevance_score >= 2 or (relevance_score == 1 and tech_match):
        filtered_brands.append({
            **brand,
            "relevance_score": relevance_score,
            "tech_match": tech_match
        })

        print(f"\n✓ {brand['name']}")
        print(f"  Relevance: {brand['garage_relevance']}")
        print(f"  Heritage: {brand['heritage']}")
        print(f"  Technology: {brand['technology']}")

# Sort by relevance
filtered_brands.sort(key=lambda x: x["relevance_score"], reverse=True)

print("\n" + "=" * 80)
print("PRIORITIZED BRAND LIST")
print("=" * 80)

prioritized_list = []
for i, brand in enumerate(filtered_brands, 1):
    print(f"\n{i}. {brand['name']} (Score: {brand['relevance_score']})")
    print(f"   Rationale: {brand['garage_relevance']}")

    prioritized_list.append({
        "name": brand["name"],
        "priority": i,
        "rationale": f"{brand['garage_relevance']} - {brand['consumer_association']}",
        "search_terms": [
            f"{brand['name']} garage",
            f"{brand['name']} organization",
            f"{brand['name']} storage",
            f"{brand['name']} DIY"
        ],
        "collection_targets": {
            "reddit_min": 50 if i <= 2 else 30,
            "youtube_min": 50 if i <= 2 else 30,
            "amazon_min": 100 if i <= 2 else 80,
            "social_min": 50 if i <= 2 else 30
        }
    })

# Generate config file
config = {
    "brands": prioritized_list,
    "collection": {
        "timeframe_months": 18,
        "min_total_per_brand": 200,
        "sources": {
            "reddit": {
                "subreddits": [
                    "HomeImprovement",
                    "organization",
                    "DIY",
                    "homeowners",
                    "Garages"
                ]
            },
            "youtube": {
                "search_categories": [
                    "home organization",
                    "garage makeover",
                    "DIY storage"
                ]
            },
            "amazon": {
                "rating_filters": [1, 5],
                "categories": [
                    "Home Improvement",
                    "Storage & Organization"
                ]
            },
            "social": {
                "platforms": ["tiktok", "instagram"],
                "hashtags": [
                    "#garageorganization",
                    "#homeorganization",
                    "#diystorage"
                ]
            }
        }
    }
}

# Save to config/brands.yaml
config_path = Path(__file__).parent.parent / "config" / "brands.yaml"
with open(config_path, "w") as f:
    yaml.dump(config, f, default_flow_style=False, sort_keys=False)

print("\n" + "=" * 80)
print("OUTPUT")
print("=" * 80)
print(f"\n✓ Generated config: {config_path}")
print(f"✓ Total brands selected: {len(prioritized_list)}")
print(f"✓ Total data points target: {len(prioritized_list) * 200}")

print("\n" + "=" * 80)
print("NEXT STEPS")
print("=" * 80)
print("\n1. Review config/brands.yaml and adjust if needed")
print("2. Set up API keys (see docs/API_SETUP.md)")
print("3. Run collectors:")
print("   - python scripts/02_collect_reddit.py")
print("   - python scripts/03_collect_youtube.py")
print("   - python scripts/04_collect_amazon.py (paid)")
print("   - python scripts/05_collect_social.py (paid)")
