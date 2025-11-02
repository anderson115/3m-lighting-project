#!/usr/bin/env python3
"""
Parse Amazon reviews from raw HTML/text scrape.
Extracts product info and review data into structured JSON.
"""

import re
import json
from datetime import datetime
from pathlib import Path

def extract_product_info(lines, start_idx):
    """Extract product title and ASIN from the beginning of a product section."""
    product_info = {
        'title': '',
        'asin': '',
        'brand': '3M',  # Default based on filename
        'total_rating': '',
        'total_reviews': 0
    }

    # Look for product title in first 150 lines
    for i in range(start_idx, min(start_idx + 150, len(lines))):
        line = lines[i].strip()

        # Product title is usually at the very beginning
        if i == start_idx and len(line) > 20 and 'Skip to' not in line:
            product_info['title'] = line

        # Look for rating info
        if 'out of 5 stars' in line and 'customer reviews' not in line:
            if not product_info['total_rating']:
                product_info['total_rating'] = line

        # Look for total review count
        if 'customer reviews' in line:
            match = re.search(r'(\d+)\s+customer reviews', line)
            if match:
                product_info['total_reviews'] = int(match.group(1))

        # Try to extract ASIN from product title variations
        if 'by' in line and i < start_idx + 105:
            # Brand might be here
            if 'Bulina' in line or 'Command' in line or '3M' in line:
                if 'Command' in line:
                    product_info['brand'] = 'Command (3M)'
                elif 'Bulina' in line:
                    product_info['brand'] = 'Bulina'

    return product_info

def parse_review(lines, start_idx):
    """Parse a single review starting from the author line."""
    review = {
        'author': '',
        'rating': '',
        'title': '',
        'date': '',
        'verified_purchase': False,
        'review_text': '',
        'style': '',
        'size': '',
        'color': ''
    }

    idx = start_idx

    # Author name (current line)
    review['author'] = lines[idx].strip()
    idx += 1

    if idx >= len(lines):
        return None, idx

    # Rating and title (next line)
    line = lines[idx].strip()
    if ' out of 5 stars ' in line:
        parts = line.split(' out of 5 stars ', 1)
        review['rating'] = parts[0] + ' out of 5 stars'
        if len(parts) > 1:
            review['title'] = parts[1]
    idx += 1

    if idx >= len(lines):
        return review, idx

    # Date and purchase info (next line)
    line = lines[idx].strip()
    if 'Reviewed in' in line:
        # Extract date
        date_match = re.search(r'Reviewed in .+ on (.+)', line)
        if date_match:
            review['date'] = date_match.group(1)
    idx += 1

    if idx >= len(lines):
        return review, idx

    # Style/Size/Color and Verified Purchase (next line)
    line = lines[idx].strip()
    if 'Verified Purchase' in line or 'Style:' in line or 'Color:' in line or 'Size:' in line:
        # Extract style/color/size
        style_match = re.search(r'Style:\s*([^S]+?)(?:Size:|Color:|Verified|$)', line)
        if style_match:
            review['style'] = style_match.group(1).strip()

        size_match = re.search(r'Size:\s*([^V]+?)(?:Verified|Color:|Style:|$)', line)
        if size_match:
            review['size'] = size_match.group(1).strip()

        color_match = re.search(r'Color:\s*([^S]+?)(?:Size:|Style:|Verified|$)', line)
        if color_match:
            review['color'] = color_match.group(1).strip()

        if 'Verified Purchase' in line:
            review['verified_purchase'] = True
        idx += 1

    # Review text - collect until we hit a marker for next section
    review_text_lines = []
    while idx < len(lines):
        line = lines[idx].strip()

        # Stop conditions - check for next review
        # Next review pattern: Author name (any text) followed by X.0 out of 5 stars
        if idx + 1 < len(lines):
            next_line = lines[idx + 1].strip()
            # Check if this could be the start of next review
            if ' out of 5 stars ' in next_line and line and line not in ['Helpful', 'Report', 'Customer image']:
                # This line is likely an author name for next review
                break

        # Skip these marker lines but continue
        if line in ['Helpful', 'Report', 'Customer image', '']:
            idx += 1
            continue
        elif 'people found this helpful' in line or 'person found this helpful' in line:
            idx += 1
            continue
        elif line.startswith('From the United States'):
            idx += 1
            break
        elif 'Previous page' in line or 'Next page' in line or 'Sponsored' in line:
            break
        elif line.startswith('##'):
            # New product section
            break
        else:
            review_text_lines.append(line)
            idx += 1

    review['review_text'] = ' '.join(review_text_lines)

    return review, idx

def parse_amazon_reviews(file_path):
    """Main parser function."""
    print(f"Reading file: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"Total lines: {len(lines)}")

    # First, identify all product boundaries (lines starting with ##)
    product_boundaries = [0]  # First product starts at line 0
    for i, line in enumerate(lines):
        if line.strip().startswith('##'):
            product_boundaries.append(i)
    product_boundaries.append(len(lines))  # End boundary

    print(f"Found {len(product_boundaries) - 1} product sections")

    products = []

    # Process each product section
    for section_idx in range(len(product_boundaries) - 1):
        start_line = product_boundaries[section_idx]
        end_line = product_boundaries[section_idx + 1]

        section_lines = lines[start_line:end_line]

        # Extract product title
        product_title = ''
        if section_lines[0].strip().startswith('##'):
            product_title = section_lines[0].strip()[2:].strip()  # Remove ##
        else:
            # First product doesn't have ##, title is on first line
            product_title = section_lines[0].strip()

        # Determine brand
        brand = '3M'
        if 'Command' in product_title:
            brand = 'Command (3M)'
        elif 'Bulina' in ' '.join(section_lines[:20]):
            brand = 'Bulina'

        # Find total review count
        total_reviews = 0
        for line in section_lines[:200]:
            match = re.search(r'(\d+)\s+customer reviews', line.strip())
            if match:
                total_reviews = int(match.group(1))
                break

        product = {
            'title': product_title,
            'brand': brand,
            'total_reviews': total_reviews,
            'reviews': []
        }

        # Parse reviews in this section
        i = 0
        while i < len(section_lines):
            line = section_lines[i].strip()

            # Look for review author names
            # Author names are followed by rating lines
            if i + 1 < len(section_lines) and ' out of 5 stars ' in section_lines[i + 1]:
                # This is likely an author line
                author_name = line

                # Skip empty author names or navigation text
                if author_name and author_name not in ['From the United States', 'Previous page', 'Next page', ''] and not author_name.startswith('http') and not author_name.startswith('##'):
                    review, next_idx = parse_review(section_lines, i)
                    if review and review['review_text']:  # Only add reviews with actual content
                        product['reviews'].append(review)
                    i = next_idx
                    continue

            i += 1

        products.append(product)
        print(f"Product {section_idx + 1}: {product['title'][:60]}... - {len(product['reviews'])} reviews (expected {total_reviews})")

    return products

def extract_product_id(title):
    """
    Extract product ID from product title.
    Try multiple strategies: ASIN (B0...), product code (SJ3550A), or create from title.
    """
    # Look for standard Amazon ASIN (10 chars, starts with B0)
    matches = re.findall(r'\b(B0[A-Z0-9]{8})\b', title)
    if matches:
        return matches[0]

    # Look for product codes like SJ3550A
    code_match = re.search(r'\b([A-Z]{2}\d{4}[A-Z]?)\b', title)
    if code_match:
        return code_match.group(1)

    # Create a unique ID from the product title
    # Extract key product name/model info
    # For Command products, extract the product type
    if 'Command' in title:
        # Try to extract product type
        if 'Toggle Hooks' in title or 'Wire Toggle' in title:
            if 'Small' in title:
                return 'CMD-TOGGLE-SMALL'
            else:
                return 'CMD-TOGGLE'
        elif 'Garland Holder' in title:
            return 'CMD-GARLAND'
        elif 'Hand Towel Bar' in title or 'Towel Bar' in title:
            return 'CMD-TOWEL-BAR'
        elif 'Wall Hooks' in title:
            if 'Dusty Rose' in title:
                return 'CMD-HOOKS-ROSE'
            elif 'Medium' in title:
                return 'CMD-HOOKS-MED'
            else:
                return 'CMD-HOOKS'

    return "UNKNOWN"

def convert_to_output_format(products):
    """Convert parsed products to the output format matching product_reviews.json."""
    output_reviews = []
    collected_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    for product in products:
        # Try to extract product ID from title
        product_id = extract_product_id(product['title'])

        for review in product['reviews']:
            output_review = {
                'title': review['title'],
                'rating': review['rating'],
                'author': review['author'],
                'date': review['date'],
                'verified_purchase': review['verified_purchase'],
                'review_text': review['review_text'],
                'product_id': product_id,
                'product_title': product['title'],
                'brand': product['brand'],
                'source': 'amazon',
                'collected_date': collected_date
            }

            # Add style/color/size if present
            if review.get('style'):
                output_review['style'] = review['style']
            if review.get('color'):
                output_review['color'] = review['color']
            if review.get('size'):
                output_review['size'] = review['size']

            output_reviews.append(output_review)

    return output_reviews

def main():
    # File paths
    input_file = Path(__file__).parent.parent / 'data' / 'collected' / '3m-garage-reviews-raw.md'
    output_file = Path(__file__).parent.parent / 'data' / 'collected' / '3m-garage-reviews-parsed.json'

    print("="*80)
    print("Amazon Reviews Parser")
    print("="*80)

    # Parse the file
    products = parse_amazon_reviews(input_file)

    print("\n" + "="*80)
    print("PARSING SUMMARY")
    print("="*80)
    print(f"Total products found: {len(products)}")

    total_reviews = 0
    for i, product in enumerate(products, 1):
        print(f"\nProduct {i}:")
        print(f"  Title: {product['title'][:80]}...")
        print(f"  Brand: {product['brand']}")
        print(f"  Expected reviews: {product['total_reviews']}")
        print(f"  Extracted reviews: {len(product['reviews'])}")
        total_reviews += len(product['reviews'])

    print(f"\nTotal reviews extracted: {total_reviews}")

    # Convert to output format
    output_reviews = convert_to_output_format(products)

    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_reviews, f, indent=2, ensure_ascii=False)

    print(f"\nOutput saved to: {output_file}")
    print(f"Total reviews in output: {len(output_reviews)}")

    # Report any issues
    print("\n" + "="*80)
    print("PARSING ISSUES")
    print("="*80)

    issues = []
    for product in products:
        expected = product['total_reviews']
        extracted = len(product['reviews'])
        if expected != extracted:
            if expected > 0:
                coverage = extracted/expected*100
                issues.append(f"Product '{product['title'][:60]}...': Expected {expected}, got {extracted} ({coverage:.1f}% coverage)")
            else:
                issues.append(f"Product '{product['title'][:60]}...': No expected count found, extracted {extracted} reviews")

    if issues:
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("  No issues detected - all expected reviews extracted!")

    print("="*80)

if __name__ == '__main__':
    main()
