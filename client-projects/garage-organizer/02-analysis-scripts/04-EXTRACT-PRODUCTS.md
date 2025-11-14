# STEP 04: EXTRACT PRODUCTS
## Garage Organizer Data Collection Pipeline

**Process:** Data extraction
**Input:** `scope_definition.json`
**Output:** `products_consolidated.json`
**Time:** 45 minutes
**Validation:** Deduplication, price coverage, retailer distribution

---

## PURPOSE

Aggregate product data from 6 retailers (Walmart, Home Depot, Amazon, Lowe's, Target, Etsy). This provides market context for design decisions.

---

## INPUTS REQUIRED

- `scope_definition.json` (from Step 01)
- Retailer APIs configured or web scraping tools ready
- Previous product data if available for merging

---

## PROCEDURE

### 1. Data Sources by Retailer

Each retailer requires different extraction method:

**Walmart & Home Depot:** Use internal APIs (if available) or web scraping
**Amazon:** Product Advertising API or BeautifulSoup
**Lowe's:** Web scraping or affiliate API
**Target:** Web scraping
**Etsy:** Official API

### 2. Extraction Strategy

For each retailer:
1. Search with keywords from scope_definition.json
2. Capture: name, URL, price, rating, review count, availability
3. Deduplicate by URL hash
4. Store with retailer label

**Script: `extract_products.py`**

```python
#!/usr/bin/env python3
"""
Consolidate product data from multiple retailers.
"""

import json
import logging
from datetime import datetime
from collections import defaultdict
import hashlib

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler('/03-analysis-output/extraction-logs/products_extraction.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

with open('/01-raw-data/scope_definition.json') as f:
    scope = json.load(f)

all_products = []
retailer_counts = defaultdict(int)
url_hashes = set()
price_stats = {'total': 0, 'with_price': 0, 'prices': []}

# This is a template - actual implementation depends on retailer APIs
# For now, load from any previous product JSON files

retailers_config = scope['products']['retailers']

for retailer_name, retailer_config in retailers_config.items():
    logger.info(f"Processing {retailer_name}")
    target_count = retailer_config['target_count'].split('-')
    min_target = int(target_count[0].replace(',', ''))
    max_target = int(target_count[1].replace(',', ''))

    # Import products from retailer (placeholder)
    products = []  # Would be populated from retailer API/scraper

    for product in products:
        # Deduplicate by URL hash
        url_hash = hashlib.md5(product['url'].encode()).hexdigest()
        if url_hash in url_hashes:
            continue

        # Normalize record
        record = {
            "product_name": product.get('name'),
            "retailer": retailer_name,
            "url": product.get('url'),
            "price": product.get('price'),
            "rating": product.get('rating'),
            "review_count": product.get('review_count'),
            "category": product.get('category'),
            "availability": product.get('availability', 'unknown'),
            "extracted_at": datetime.now().isoformat()
        }

        all_products.append(record)
        url_hashes.add(url_hash)
        retailer_counts[retailer_name] += 1

        if record['price']:
            price_stats['with_price'] += 1
            try:
                price_stats['prices'].append(float(str(record['price']).replace('$', '')))
            except:
                pass

        price_stats['total'] += 1

# Validation
output = {
    "manifest": {
        "source": "multi_retailer",
        "collection_date": datetime.now().isoformat(),
        "total_records": len(all_products),
        "expected_range": "7000-10000",
        "retailers": dict(retailer_counts),
        "completeness": {
            "records_with_urls": sum(1 for p in all_products if p['url']),
            "records_with_prices": price_stats['with_price'],
            "records_with_ratings": sum(1 for p in all_products if p.get('rating')),
            "deduplication": {
                "unique_urls": len(url_hashes),
                "total_records": len(all_products)
            }
        },
        "price_metrics": {
            "avg_price": sum(price_stats['prices']) / len(price_stats['prices']) if price_stats['prices'] else 0,
            "min_price": min(price_stats['prices']) if price_stats['prices'] else 0,
            "max_price": max(price_stats['prices']) if price_stats['prices'] else 0,
            "price_coverage_percent": (price_stats['with_price'] / price_stats['total'] * 100) if price_stats['total'] else 0
        }
    },
    "products": all_products
}

with open('/01-raw-data/products_consolidated.json', 'w') as f:
    json.dump(output, f, indent=2)

logger.info(f"Extracted {len(all_products)} total products")
logger.info(f"Retailer breakdown: {dict(retailer_counts)}")

# Validation report
validation_report = {
    "step": "04-EXTRACT-PRODUCTS",
    "timestamp": datetime.now().isoformat(),
    "total_records": len(all_products),
    "expected_range": "7000-10000",
    "validation_rules": {
        "rule_sample_size": {
            "rule": "Sample size 7000-10000",
            "min": 7000,
            "max": 10000,
            "found": len(all_products),
            "pass": 7000 <= len(all_products) <= 10000
        },
        "rule_price_coverage": {
            "rule": "90%+ have prices",
            "threshold": 0.90,
            "found": price_stats['with_price'] / price_stats['total'] if price_stats['total'] else 0,
            "pass": price_stats['with_price'] / price_stats['total'] >= 0.90 if price_stats['total'] else False
        },
        "rule_deduplication": {
            "rule": "No URL duplicates",
            "found_duplicates": len(all_products) - len(url_hashes),
            "pass": len(all_products) == len(url_hashes)
        },
        "rule_urls_complete": {
            "rule": "100% have URLs",
            "pass": sum(1 for p in all_products if p['url']) == len(all_products)
        }
    },
    "overall_status": "PASS" if all([
        7000 <= len(all_products) <= 10000,
        price_stats['with_price'] / price_stats['total'] >= 0.90 if price_stats['total'] else False,
        len(all_products) == len(url_hashes),
        sum(1 for p in all_products if p['url']) == len(all_products)
    ]) else "FAIL"
}

with open('/03-analysis-output/validation_report_04.json', 'w') as f:
    json.dump(validation_report, f, indent=2)

logger.info(f"Validation report: {validation_report['overall_status']}")
```

### 3. Deduplication Logic

```
FOR each product:
  1. Create URL hash: MD5(url)
  2. IF hash exists in seen_hashes:
     - SKIP this product (duplicate)
     - LOG duplicate with original retailer
  3. ELSE:
     - ADD to products list
     - ADD hash to seen_hashes
```

### 4. Execute Extraction

```bash
python3 extract_products.py
```

---

## OUTPUT FILE FORMAT: products_consolidated.json

```json
{
  "manifest": {
    "source": "multi_retailer",
    "collection_date": "2025-11-12T12:30:00",
    "total_records": 8234,
    "expected_range": "7000-10000",
    "retailers": {
      "walmart": 3100,
      "home_depot": 1200,
      "amazon": 1050,
      "lowes": 950,
      "target": 520,
      "etsy": 414
    },
    "completeness": {
      "records_with_urls": 8234,
      "records_with_prices": 7411,
      "records_with_ratings": 2043,
      "deduplication": {
        "unique_urls": 8234,
        "total_records": 8234
      }
    },
    "price_metrics": {
      "avg_price": 47.82,
      "min_price": 2.99,
      "max_price": 1299.99,
      "price_coverage_percent": 90.0
    }
  },
  "products": [
    {
      "product_name": "5-Tier Heavy Duty Garage Shelving",
      "retailer": "walmart",
      "url": "https://walmart.com/ip/...",
      "price": 89.99,
      "rating": 4.5,
      "review_count": 234,
      "category": "Shelving units",
      "availability": "in_stock",
      "extracted_at": "2025-11-12T12:30:00"
    }
  ]
}
```

---

## VALIDATION RULES

| Rule | Type | Threshold | Action if Fail |
|------|------|-----------|---|
| Sample size 7000-10000 | CRITICAL | ±5% | Adjust scraping if needed |
| Price coverage 90%+ | CRITICAL | ≥90% | OK if some products have no price |
| No URL duplicates | CRITICAL | 100% | Log and remove duplicates |
| All have retailer label | CRITICAL | 100% | Reject if missing |

---

## COMMON ERRORS & FIXES

### Error: "Only 2000 products extracted (want 7000+)"
- **Cause:** Retailer API limits or incomplete scraping
- **Fix:** Expand keyword list, increase pages per keyword
- **Prevention:** Estimate per keyword: 1000+ products / 10 keywords = 100 each

### Error: "95% missing prices"
- **Cause:** Retailer doesn't include price in API response
- **Fix:** Switch to different data source or note as limitation
- **Prevention:** Verify API includes price field before extraction

### Error: "8500 products but 9200 unique URLs"
- **Cause:** Same product on multiple retailer pages
- **Fix:** Correct deduplication logic (this shouldn't happen)
- **Prevention:** Log dedup process to verify it's working

---

## SUCCESS CRITERIA

✅ **This step succeeds when:**
- 7000-10000 products extracted
- 100% have URLs
- 90%+ have prices
- No URL duplicates
- All have retailer label

---

## NEXT STEP

Once validation passes:
1. Spot-check 10 random products for quality
2. Verify price ranges are reasonable ($2.99-$1299.99)
3. Proceed to `05-VALIDATE-DATA.md`

---

**Status:** READY
**Last Updated:** November 12, 2025
