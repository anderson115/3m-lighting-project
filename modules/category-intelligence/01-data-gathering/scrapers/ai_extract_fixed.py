#!/usr/bin/env python3
"""
AI-powered extraction of missing fields from existing product data.
"""
import json
import anthropic
import os
import re
from pathlib import Path

# Get ANTHROPIC_API_KEY from environment
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise RuntimeError("ANTHROPIC_API_KEY environment variable not set")

client = anthropic.Anthropic(api_key=api_key)

def extract_fields_with_ai(product_name, description=""):
    """Use Claude to extract missing fields from product data."""

    prompt = f"""Extract the following information from this product:

Product Name: {product_name}
Description: {description[:500] if description else "N/A"}

Extract and return ONLY a JSON object with these fields:
{{
  "material": "primary material (metal/plastic/wood/composite/unknown)",
  "color": "primary color or 'unknown'",
  "weight_capacity_lbs": "number only or null",
  "is_rail_or_slatwall": "yes/no",
  "rail_type": "rail|attachment|kit|none",
  "is_hook_or_hanger": "yes/no"
}}

Rules:
- Material: Look for mentions of steel, metal, plastic, aluminum, wood
- Color: Extract explicit color mentions
- Weight capacity: Extract numbers followed by lb/lbs/pound
- Rail/slatwall: Keywords like "slatwall", "rail system", "track"
- Hook/hanger: Products designed to hang items

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
            print(f"⏭️  Skipping {retailer} - file not found")
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
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_enhanced, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Enhanced {len(all_enhanced)} products")
    print(f"✅ Saved to {output_file}")

    return all_enhanced


if __name__ == "__main__":
    process_all_products()
