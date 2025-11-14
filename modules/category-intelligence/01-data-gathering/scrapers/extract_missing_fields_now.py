#!/usr/bin/env python3
"""
Extract missing fields using Claude API (available in Claude Code environment).
"""
import json
import anthropic
import os
import re
from pathlib import Path

# Initialize Claude client - API key from environment
client = anthropic.Anthropic()

def extract_fields_with_ai(product_name, description=""):
    """Use Claude to extract missing fields."""

    prompt = f"""Extract the following information from this product:

Product Name: {product_name}
Description: {description[:500] if description else "N/A"}

Extract and return ONLY a JSON object with these fields:
{{
  "material": "primary material (metal/plastic/wood/composite/unknown)",
  "color": "primary color or 'unknown'",
  "weight_capacity_lbs": number or null,
  "is_rail_or_slatwall": "yes/no",
  "rail_type": "rail|attachment|kit|none",
  "is_hook_or_hanger": "yes/no"
}}

Rules:
- Material: steel, metal, plastic, aluminum, wood, composite
- Color: Extract color names (black, white, silver, etc.)
- Weight capacity: Extract numbers followed by lb/lbs/pound
- Rail/slatwall: Look for "slatwall", "rail system", "track", "french cleat"
- Hook/hanger: Products for hanging items

Return ONLY valid JSON, no other text."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text

        # Extract JSON from response
        json_match = re.search(r'\{[^}]+\}', response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            return {}

    except Exception as e:
        print(f"  Error: {e}")
        return {}


def process_all_products():
    """Process all existing retailer products."""

    print("="*70)
    print("AI FIELD EXTRACTION - RUNNING NOW")
    print("="*70)
    print()

    retailers = ["amazon", "walmart", "homedepot", "target"]
    all_enhanced = []

    for retailer in retailers:
        file_path = Path(f"data/retailers/{retailer}_products.json")
        if not file_path.exists():
            continue

        print(f"\nProcessing {retailer.upper()}...")

        with open(file_path, 'r', encoding='utf-8') as f:
            products = json.load(f)

        # Process top 400 only
        def get_review_count(product):
            reviews = product.get('reviews', product.get('total_reviews', 0))
            if reviews is None:
                return 0
            try:
                return int(reviews)
            except (ValueError, TypeError):
                return 0

        sorted_products = sorted(products, key=get_review_count, reverse=True)
        top_400 = sorted_products[:400]

        print(f"  Processing {len(top_400)} products...")

        for i, product in enumerate(top_400):
            name = product.get('name', product.get('title', ''))
            description = str(product.get('attributes', product.get('description', '')))

            if i % 50 == 0:
                print(f"  {i}/{len(top_400)}...")

            # Extract fields
            extracted = extract_fields_with_ai(name, description)

            # Merge with original
            enhanced = {**product, **extracted}
            all_enhanced.append(enhanced)

    # Save enhanced data
    output_file = Path("data/retailers/all_products_enhanced_final.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_enhanced, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Enhanced {len(all_enhanced)} products")
    print(f"✅ Saved to {output_file}")

    return all_enhanced


if __name__ == "__main__":
    enhanced = process_all_products()

    # Count coverage
    material_count = sum(1 for p in enhanced if p.get('material') and p['material'] != 'unknown')
    color_count = sum(1 for p in enhanced if p.get('color') and p['color'] != 'unknown')
    weight_count = sum(1 for p in enhanced if p.get('weight_capacity_lbs'))
    rail_count = sum(1 for p in enhanced if p.get('is_rail_or_slatwall') == 'yes')
    hook_count = sum(1 for p in enhanced if p.get('is_hook_or_hanger') == 'yes')

    print()
    print("="*70)
    print("EXTRACTION COVERAGE")
    print("="*70)
    print(f"Material: {material_count}/{len(enhanced)} ({100*material_count/len(enhanced):.1f}%)")
    print(f"Color: {color_count}/{len(enhanced)} ({100*color_count/len(enhanced):.1f}%)")
    print(f"Weight Capacity: {weight_count}/{len(enhanced)} ({100*weight_count/len(enhanced):.1f}%)")
    print(f"Rail/Slatwall: {rail_count} products identified")
    print(f"Hook/Hanger: {hook_count} products identified")
