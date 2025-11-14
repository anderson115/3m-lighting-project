#!/usr/bin/env python3
"""
Collect Amazon reviews for products that make up 80% of category volume.
Target: Minimum 100 quality reviews per product.

Uses same method as brand-perceptions module:
1. Identify top products (80% by volume/review count)
2. Generate Amazon review URLs
3. Manual scrape → save as .md files
4. Parse with review parser
"""

import json
from pathlib import Path
from collections import defaultdict

BASE = Path("/Users/anderson115/00-interlink/12-work/3m-lighting-project")
CI_PROJECT = BASE / "projects/garage-organizer/category-intelligence"
CI_DATA = CI_PROJECT / "data/consolidated"

def identify_pareto_products():
    """Identify products that make up 80% of category by review volume."""
    print("="*100)
    print("STEP 1: IDENTIFYING PARETO 80% PRODUCTS")
    print("="*100)

    # Load all products
    with open(CI_DATA / "garage-organizer-category-products.json") as f:
        products = json.load(f)["products"]

    # Filter products with reviews and ratings
    products_with_reviews = [
        p for p in products
        if p.get("review_count", 0) > 0 and p.get("rating", 0) > 0
    ]

    print(f"\nTotal products: {len(products):,}")
    print(f"Products with reviews: {len(products_with_reviews):,}")

    # Sort by review count (proxy for volume)
    products_sorted = sorted(
        products_with_reviews,
        key=lambda x: x.get("review_count", 0),
        reverse=True
    )

    # Calculate 80% threshold
    total_reviews = sum(p.get("review_count", 0) for p in products_sorted)
    target_reviews = total_reviews * 0.80

    cumulative = 0
    pareto_products = []

    for product in products_sorted:
        cumulative += product.get("review_count", 0)
        pareto_products.append(product)

        if cumulative >= target_reviews:
            break

    print(f"\nTotal review volume: {total_reviews:,}")
    print(f"80% threshold: {target_reviews:,.0f} reviews")
    print(f"Products needed for 80%: {len(pareto_products)}")

    # Group by brand
    brand_counts = defaultdict(int)
    for p in pareto_products:
        brand_counts[p.get("brand", "Unknown")] += 1

    print(f"\nBrand distribution in Pareto 80%:")
    for brand, count in sorted(brand_counts.items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"  {brand:30} {count:>4} products")

    # Check 3M brands
    three_m_products = [p for p in pareto_products if "3m" in p.get("brand", "").lower() or "command" in p.get("brand", "").lower() or "claw" in p.get("brand", "").lower()]
    print(f"\n3M products in Pareto 80%: {len(three_m_products)}")

    return pareto_products

def generate_collection_plan(pareto_products):
    """Generate collection plan: 100 reviews per product."""
    print("\n" + "="*100)
    print("STEP 2: GENERATING COLLECTION PLAN")
    print("="*100)

    collection_plan = []

    for product in pareto_products:
        product_id = product.get("product_id") or product.get("asin", "")

        if not product_id:
            continue

        # Determine if it's a 3M product
        brand = product.get("brand", "")
        is_3m = any(x in brand.lower() for x in ["3m", "command", "claw", "scotch"])

        plan_item = {
            "product_id": product_id,
            "brand": brand,
            "name": product.get("name", ""),
            "existing_review_count": product.get("review_count", 0),
            "rating": product.get("rating", 0),
            "url": product.get("url", ""),
            "target_reviews": 100,
            "priority": "HIGH" if is_3m else "NORMAL",
            "amazon_review_url": f"https://www.amazon.com/product-reviews/{product_id}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
        }

        collection_plan.append(plan_item)

    # Sort by priority (3M first), then by review count
    collection_plan.sort(key=lambda x: (x["priority"] != "HIGH", -x["existing_review_count"]))

    # Statistics
    total_products = len(collection_plan)
    three_m_count = sum(1 for p in collection_plan if p["priority"] == "HIGH")
    total_target_reviews = total_products * 100

    print(f"\nCollection plan:")
    print(f"  Total products: {total_products}")
    print(f"  3M products: {three_m_count}")
    print(f"  Target reviews: {total_target_reviews:,} (100 per product)")
    print(f"  Estimated scraping time: {total_products * 2} minutes (2 min per product)")

    # Show top 10
    print(f"\nTop 10 priority products:")
    for i, item in enumerate(collection_plan[:10], 1):
        print(f"  {i:2}. [{item['priority']:6}] {item['brand']:20} | {item['name'][:50]}")
        print(f"      Reviews: {item['existing_review_count']:>6} | ASIN: {item['product_id']}")

    return collection_plan

def save_collection_instructions(collection_plan):
    """Save collection plan and instructions."""
    print("\n" + "="*100)
    print("STEP 3: SAVING COLLECTION INSTRUCTIONS")
    print("="*100)

    output_dir = CI_PROJECT / "data" / "review_collection"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save plan
    plan_file = output_dir / "collection_plan.json"
    with open(plan_file, 'w') as f:
        json.dump({
            "generated_at": "2025-11-04",
            "total_products": len(collection_plan),
            "target_reviews_per_product": 100,
            "total_target_reviews": len(collection_plan) * 100,
            "products": collection_plan
        }, f, indent=2)

    print(f"✓ Saved collection plan: {plan_file}")

    # Save URL list for manual scraping
    urls_file = output_dir / "review_urls.txt"
    with open(urls_file, 'w') as f:
        f.write("# AMAZON REVIEW COLLECTION URLS\n")
        f.write("# Copy these URLs to browser, save page as .md file\n")
        f.write(f"# Target: 100 reviews per product ({len(collection_plan)} products)\n\n")

        for i, item in enumerate(collection_plan, 1):
            f.write(f"# {i}. [{item['priority']}] {item['brand']} - {item['name'][:60]}\n")
            f.write(f"{item['amazon_review_url']}\n")
            f.write(f"# Save as: {item['product_id']}_reviews.md\n\n")

    print(f"✓ Saved URL list: {urls_file}")

    # Save instructions
    instructions_file = output_dir / "COLLECTION_INSTRUCTIONS.md"
    instructions = f"""# Amazon Review Collection Instructions

**Generated:** 2025-11-04
**Target:** {len(collection_plan)} products, 100 reviews each
**Total reviews:** {len(collection_plan) * 100:,}

## Method (Same as brand-perceptions module)

### Step 1: Manual Scraping
1. Open `review_urls.txt`
2. For each URL:
   - Open in browser
   - Wait for page to load fully
   - Scroll to load all reviews (up to 100)
   - Save page as Markdown: File → Save As → Format: Markdown
   - Name file: `PRODUCT_ID_reviews.md`
3. Save all .md files to: `data/review_collection/raw/`

### Step 2: Parsing
```bash
cd modules/category-intelligence/scraping
python3 parse_collected_reviews.py
```

This will:
- Parse all .md files
- Extract review text, ratings, dates
- Generate consolidated JSON: `garage-organizer-reviews.json`
- Validate: ensure 100+ reviews per product

### Step 3: Quality Check
- Verify all products have ≥100 reviews
- Check 3M products are complete
- Validate review_text field is populated

## Priority Products (HIGH = 3M brands)

"""

    for i, item in enumerate(collection_plan[:20], 1):
        instructions += f"{i}. [{item['priority']}] **{item['brand']}** - {item['name'][:60]}\n"
        instructions += f"   - ASIN: `{item['product_id']}`\n"
        instructions += f"   - Existing reviews: {item['existing_review_count']:,}\n\n"

    instructions += f"""
## Statistics

- Total products: {len(collection_plan)}
- 3M products: {sum(1 for p in collection_plan if p['priority'] == 'HIGH')}
- Other brands: {sum(1 for p in collection_plan if p['priority'] == 'NORMAL')}
- Target reviews: {len(collection_plan) * 100:,}

## Notes

- Use same method as brand-perceptions (manual scraping worked, got 400 Command reviews)
- Focus on 3M products first (HIGH priority)
- Minimum 100 reviews per product (for statistical significance)
- Reviews will be weighted by volume during analysis
"""

    with open(instructions_file, 'w') as f:
        f.write(instructions)

    print(f"✓ Saved instructions: {instructions_file}")

    return output_dir

def main():
    print("="*100)
    print("AMAZON REVIEW COLLECTION PLAN - PARETO 80%")
    print("Method: Same as brand-perceptions (manual scraping)")
    print("="*100)

    # Step 1: Identify products
    pareto_products = identify_pareto_products()

    # Step 2: Generate plan
    collection_plan = generate_collection_plan(pareto_products)

    # Step 3: Save instructions
    output_dir = save_collection_instructions(collection_plan)

    print("\n" + "="*100)
    print("✅ COLLECTION PLAN COMPLETE")
    print("="*100)
    print(f"\nNext steps:")
    print(f"1. Open: {output_dir}/COLLECTION_INSTRUCTIONS.md")
    print(f"2. Follow manual scraping instructions")
    print(f"3. Run parser when complete")
    print(f"\nTarget: {len(collection_plan)} products × 100 reviews = {len(collection_plan) * 100:,} total reviews")

    return 0

if __name__ == "__main__":
    exit(main())
