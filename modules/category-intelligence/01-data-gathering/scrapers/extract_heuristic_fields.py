#!/usr/bin/env python3
"""
Extract fields using heuristics and regex from product names.
"""
import json
import re
from pathlib import Path

def extract_material(text):
    """Extract material from product name/description."""
    text_lower = text.lower()
    if any(word in text_lower for word in ['steel', 'stainless steel', 'metal']):
        return 'metal'
    elif 'aluminum' in text_lower or 'aluminium' in text_lower:
        return 'aluminum'
    elif 'plastic' in text_lower or 'resin' in text_lower:
        return 'plastic'
    elif 'wood' in text_lower or 'wooden' in text_lower:
        return 'wood'
    else:
        return 'unknown'

def extract_color(text):
    """Extract color from product name."""
    text_lower = text.lower()
    colors = ['black', 'white', 'silver', 'gray', 'grey', 'red', 'blue', 'green', 'brown', 'yellow']
    for color in colors:
        if color in text_lower:
            return color
    return 'unknown'

def extract_weight_capacity(text):
    """Extract weight capacity in lbs."""
    # Look for patterns like "50 lbs", "100 pounds", "50-lb"
    patterns = [
        r'(\d+)\s*(?:lbs?|pounds?)',
        r'(\d+)\s*(?:kg)',  # Convert kg to lbs
        r'capacity[:\s]+(\d+)',
        r'holds?\s+(\d+)',
        r'supports?\s+(\d+)'
    ]

    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            weight = int(match.group(1))
            # Convert kg to lbs if needed
            if 'kg' in pattern:
                weight = int(weight * 2.20462)
            return weight
    return None

def is_rail_or_slatwall(text):
    """Check if product is rail/slatwall system."""
    text_lower = text.lower()
    keywords = ['slatwall', 'slat wall', 'rail system', 'track system', 'french cleat', 'wall track']
    return 'yes' if any(kw in text_lower for kw in keywords) else 'no'

def get_rail_type(text):
    """Get rail type if applicable."""
    text_lower = text.lower()
    if is_rail_or_slatwall(text) == 'no':
        return 'none'
    elif 'rail' in text_lower:
        return 'rail'
    elif 'attachment' in text_lower or 'accessory' in text_lower:
        return 'attachment'
    elif 'kit' in text_lower or 'system' in text_lower:
        return 'kit'
    return 'rail'

def is_hook_or_hanger(text):
    """Check if product is hook/hanger."""
    text_lower = text.lower()
    keywords = ['hook', 'hanger', 'hang', 'holder', 'mount']
    return 'yes' if any(kw in text_lower for kw in keywords) else 'no'

print("="*70)
print("HEURISTIC FIELD EXTRACTION")
print("="*70)
print()

retailers = ["amazon", "walmart", "homedepot", "target"]
all_enhanced = []

for retailer in retailers:
    file_path = Path(f"data/retailers/{retailer}_products.json")
    if not file_path.exists():
        continue

    print(f"Processing {retailer.upper()}...")

    with open(file_path, 'r', encoding='utf-8') as f:
        products = json.load(f)

    # Get top 400 by review count
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

    for product in top_400:
        name = product.get('name', product.get('title', ''))
        description = str(product.get('attributes', ''))
        full_text = f"{name} {description}"

        # Extract fields
        product['material'] = extract_material(full_text)
        product['color'] = extract_color(full_text)
        product['weight_capacity_lbs'] = extract_weight_capacity(full_text)
        product['is_rail_or_slatwall'] = is_rail_or_slatwall(full_text)
        product['rail_type'] = get_rail_type(full_text)
        product['is_hook_or_hanger'] = is_hook_or_hanger(full_text)

        all_enhanced.append(product)

    print(f"  Processed {len(top_400)} products")

# Save
output_file = Path("data/retailers/all_products_enhanced_heuristic.json")
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_enhanced, f, indent=2, ensure_ascii=False)

print(f"\n✅ Enhanced {len(all_enhanced)} products")
print(f"✅ Saved to {output_file}")

# Coverage stats
material_count = sum(1 for p in all_enhanced if p.get('material') != 'unknown')
color_count = sum(1 for p in all_enhanced if p.get('color') != 'unknown')
weight_count = sum(1 for p in all_enhanced if p.get('weight_capacity_lbs'))
rail_count = sum(1 for p in all_enhanced if p.get('is_rail_or_slatwall') == 'yes')
hook_count = sum(1 for p in all_enhanced if p.get('is_hook_or_hanger') == 'yes')

print()
print("="*70)
print("EXTRACTION COVERAGE")
print("="*70)
print(f"Material: {material_count}/{len(all_enhanced)} ({100*material_count/len(all_enhanced):.1f}%)")
print(f"Color: {color_count}/{len(all_enhanced)} ({100*color_count/len(all_enhanced):.1f}%)")
print(f"Weight Capacity: {weight_count}/{len(all_enhanced)} ({100*weight_count/len(all_enhanced):.1f}%)")
print(f"Rail/Slatwall: {rail_count} products identified ({100*rail_count/len(all_enhanced):.1f}%)")
print(f"Hook/Hanger: {hook_count} products identified ({100*hook_count/len(all_enhanced):.1f}%)")
