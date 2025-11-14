#!/usr/bin/env python3
"""
AI-powered extraction of missing fields from existing product data:
- Material (plastic, metal, wood, etc.)
- Color
- Weight capacity
- Rail/slatwall system classification
- Hook/hanger classification
"""
import json
import anthropic
import os
import re
from pathlib import Path

# Initialize Claude
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def extract_fields_with_ai(product_name, description="", batch_size=10):
    """Use Claude to extract missing fields from product data."""

    prompt = f"""Extract the following information from this product:

Product Name: {product_name}
Description: {description[:500] if description else "N/A"}

Extract and return ONLY a JSON object with these fields:
{{
  "material": "primary material (metal/plastic/wood/composite/unknown)",
  "color": "primary color or 'unknown'",
  "weight_capacity_lbs": "number only or null (extract from capacity claims like '50 lbs', '100 pounds')",
  "is_rail_or_slatwall": "yes/no (is this a rail, slatwall, track, or french cleat system?)",
  "rail_type": "rail|attachment|kit|none (if yes above, what type?)",
  "is_hook_or_hanger": "yes/no (is this primarily for hanging items?)"
}}

Rules:
- Material: Look for mentions of steel, metal, plastic, aluminum, wood, composite
- Color: Extract explicit color mentions (black, white, silver, etc.)
- Weight capacity: Extract numbers followed by lb/lbs/pound/kg
- Rail/slatwall: Keywords like "slatwall", "rail system", "track", "french cleat"
- Hook/hanger: Products designed to hang items on walls

Return ONLY valid JSON."""

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
    print("AI FIELD EXTRACTION FROM EXISTING PRODUCTS")
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

        print(f"  Total products: {len(products)}")

        # Process in batches
        for i, product in enumerate(products[:400]):  # Top 400
            name = product.get('name', product.get('title', ''))
            description = str(product.get('attributes', ''))

            if i % 50 == 0:
                print(f"  Processing {i}/{min(400, len(products))}...")

            # Extract fields
            extracted = extract_fields_with_ai(name, description)

            # Merge with original
            enhanced = {**product, **extracted}
            all_enhanced.append(enhanced)

            if i >= 399:
                break

    # Save enhanced data
    output_file = Path("data/retailers/all_products_enhanced.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_enhanced, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Enhanced {len(all_enhanced)} products")
    print(f"✅ Saved to {output_file}")

    return all_enhanced


if __name__ == "__main__":
    process_all_products()
