#!/usr/bin/env python3
"""
Parse Lowes product data from MD file and integrate into master product list.
"""
import json
import csv
import re
from pathlib import Path
from io import StringIO

print("="*70)
print("PARSING LOWES DATA FROM MD FILE")
print("="*70)
print()

# Read the MD file
md_file = Path("/Users/anderson115/Desktop/3m-organizer-hook.md")
with open(md_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the CSV data block (starts after "Code snippet" and contains proper CSV)
# Look for the section with the CSV header and data
csv_pattern = r'"Product ID","Search Term".*?(?=\n\n|\Z)'
matches = re.findall(csv_pattern, content, re.DOTALL)

if not matches:
    print("❌ Could not find CSV data in MD file")
    exit(1)

# Take the longest match (most complete dataset)
csv_data = max(matches, key=len)

print(f"Found CSV block with {len(csv_data)} characters")
print(f"Parsing CSV data...")
print()

# Parse CSV
csv_reader = csv.DictReader(StringIO(csv_data))
lowes_products = []

for row in csv_reader:
    # Clean up price
    price_str = (row.get('Price ($)') or '').replace('$', '').replace(',', '').strip()
    try:
        price = float(price_str) if price_str and price_str != 'View Lower Price in Cart' else 0
    except:
        price = 0

    # Clean up rating
    rating_str = (row.get('Rating') or '').strip()
    try:
        rating = float(rating_str) if rating_str and rating_str != 'NA' else 0
    except:
        rating = 0

    # Clean up review count
    reviews_str = (row.get('Review Count') or '').replace(',', '').strip()
    try:
        reviews = int(reviews_str) if reviews_str and reviews_str != 'NA' else 0
    except:
        reviews = 0

    # Create product entry matching our schema
    product = {
        'retailer': 'Lowes',
        'name': (row.get('Product Name') or '').strip(),
        'brand': (row.get('Brand') or '').strip(),
        'url': f"https://www.lowes.com/search?searchTerm={(row.get('Search Term') or 'garage+organizer').replace(' ', '+')}",
        'price': price,
        'rating': rating,
        'reviews': reviews,
        'sku': (row.get('Product ID') or ''),
        'attributes': {
            'dimensions': (row.get('Dimensions (Inches)') or '').strip(),
            'material': (row.get('Material') or '').strip(),
            'color': (row.get('Color/Finish') or '').strip(),
            'special_notes': (row.get('Special Notes') or '').strip(),
            'pickup': (row.get('Pickup Availability') or '').strip(),
            'delivery': (row.get('Delivery Availability') or '').strip()
        },
        'taxonomy_path': ['Lowes', 'Garage Organization'],
        'scraped_at': '2024-10-27'
    }

    if product['name']:  # Only add if has a name
        lowes_products.append(product)

print(f"✅ Parsed {len(lowes_products)} Lowes products")
print()

# Get top 400 by review count
sorted_products = sorted(lowes_products, key=lambda p: p.get('reviews', 0), reverse=True)
top_400 = sorted_products[:400]

print(f"Selected top 400 products by review count")
print()

# Extract enhanced fields using heuristics
print("Extracting enhanced fields...")

def extract_material(text):
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
    text_lower = text.lower()
    colors = ['black', 'white', 'silver', 'gray', 'grey', 'red', 'blue', 'green', 'brown', 'yellow']
    for color in colors:
        if color in text_lower:
            return color
    return 'unknown'

def extract_weight_capacity(text):
    patterns = [
        r'(\d+)\s*(?:lbs?|pounds?)',
        r'(\d+)\s*(?:kg)',
        r'capacity[:\s]+(\d+)',
        r'holds?\s+(\d+)',
        r'supports?\s+(\d+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            weight = int(match.group(1))
            if 'kg' in pattern:
                weight = int(weight * 2.20462)
            return weight
    return None

def is_rail_or_slatwall(text):
    text_lower = text.lower()
    keywords = ['slatwall', 'slat wall', 'rail system', 'track system', 'french cleat', 'wall track', 'geartrack', 'versatrack']
    return 'yes' if any(kw in text_lower for kw in keywords) else 'no'

def get_rail_type(text):
    text_lower = text.lower()
    if is_rail_or_slatwall(text) == 'no':
        return 'none'
    elif 'rail' in text_lower or 'track' in text_lower:
        return 'rail'
    elif 'attachment' in text_lower or 'accessory' in text_lower:
        return 'attachment'
    elif 'kit' in text_lower or 'system' in text_lower:
        return 'kit'
    return 'rail'

def is_hook_or_hanger(text):
    text_lower = text.lower()
    keywords = ['hook', 'hanger', 'hang', 'holder', 'mount']
    return 'yes' if any(kw in text_lower for kw in keywords) else 'no'

for product in top_400:
    name = product.get('name', '')
    attrs = product.get('attributes', {})
    material_field = attrs.get('material', '')
    color_field = attrs.get('color', '')

    full_text = f"{name} {material_field} {color_field}"

    # Extract fields
    product['material'] = extract_material(full_text)
    product['color'] = extract_color(full_text)
    product['weight_capacity_lbs'] = extract_weight_capacity(full_text)
    product['is_rail_or_slatwall'] = is_rail_or_slatwall(full_text)
    product['rail_type'] = get_rail_type(full_text)
    product['is_hook_or_hanger'] = is_hook_or_hanger(full_text)

print(f"✅ Enhanced fields extracted")
print()

# Save Lowes products
lowes_output = Path("data/retailers/lowes_products.json")
lowes_output.parent.mkdir(parents=True, exist_ok=True)

with open(lowes_output, 'w', encoding='utf-8') as f:
    json.dump(top_400, f, indent=2, ensure_ascii=False)

print(f"✅ Saved {len(top_400)} Lowes products to {lowes_output}")
print()

# Load existing product data
existing_products = []
for retailer in ["amazon", "walmart", "homedepot", "target"]:
    file_path = Path(f"data/retailers/{retailer}_products.json")
    if file_path.exists():
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

        sorted_prods = sorted(products, key=get_review_count, reverse=True)
        top_400_existing = sorted_prods[:400]

        # Apply enhanced fields if not already present
        for product in top_400_existing:
            if 'material' not in product:
                name = product.get('name', product.get('title', ''))
                description = str(product.get('attributes', ''))
                full_text = f"{name} {description}"

                product['material'] = extract_material(full_text)
                product['color'] = extract_color(full_text)
                product['weight_capacity_lbs'] = extract_weight_capacity(full_text)
                product['is_rail_or_slatwall'] = is_rail_or_slatwall(full_text)
                product['rail_type'] = get_rail_type(full_text)
                product['is_hook_or_hanger'] = is_hook_or_hanger(full_text)

        existing_products.extend(top_400_existing)
        print(f"Loaded {len(top_400_existing)} products from {retailer.upper()}")

# Combine all products
all_products = existing_products + top_400

print()
print(f"✅ Total products: {len(all_products)} (includes {len(top_400)} from Lowes)")
print()

# Save combined data
combined_output = Path("data/retailers/all_products_final_with_lowes.json")
with open(combined_output, 'w', encoding='utf-8') as f:
    json.dump(all_products, f, indent=2, ensure_ascii=False)

print(f"✅ Saved combined product data to {combined_output}")
print()

# Summary stats
by_retailer = {}
for p in all_products:
    retailer = p.get('retailer', 'unknown')
    by_retailer[retailer] = by_retailer.get(retailer, 0) + 1

print("="*70)
print("PRODUCT BREAKDOWN BY RETAILER")
print("="*70)
for retailer, count in sorted(by_retailer.items()):
    print(f"  {retailer}: {count} products")

print()
print("="*70)
print("PARSING COMPLETE")
print("="*70)
