# Data Consolidation & Normalization Task
**Project:** 3M Garage Organizer Category Intelligence
**Task:** Consolidate heterogeneous scraper data into normalized master files for PostgreSQL import and brand perception analysis
**Success Criteria:** 99% data integrity, zero data loss, all fields mapped correctly

---

## CONTEXT

You have 69 JSON files from 3 different scraping sessions with inconsistent schemas. Your job is to consolidate this raw data into normalized master files organized by:
1. **Brand** (3M Claw + top 8-10 competitive brands)
2. **Data Type** (products, reviews, videos-youtube, videos-tiktok)
3. **Category** (garage-organizer-category aggregates)

The consolidated data will feed:
- **Brand perception analysis** for 3M Claw
- **Spider/radar charts** showing brand strengths vs category benchmarks
- **Category attribute mapping** (unbiased across retailers/price points)
- **PostgreSQL database** for future analysis

---

## INPUT DATA STRUCTURE

### Data Location
**Base Path:** `modules/category-intelligence/`

**File Manifest:** `FILE_MANIFEST_20251104.json` (69 files, 186.94 MB)

### Key Source Files

#### Products (heterogeneous schemas)
```
data/retailers/all_products_final_with_lowes.json (2,000 products)
├─ Schema: {retailer, name, url, price, rating, brand, sku, reviews, attributes{...}, taxonomy_path[], scraped_at, material, color, weight_capacity_lbs, is_rail_or_slatwall, rail_type, is_hook_or_hanger}

data/expanded_coverage/amazon_products_with_reviews_20251104_155959.json (812 products)
├─ Schema: {asin, title, price, rating, search_term, retailer, scraped_at}

outputs/garage_organizer_sample_20251104.json (1,600 products)
├─ Schema: {retailer, name, url, price, rating, brand, sku, reviews, attributes{...}, taxonomy_path[], ...}
```

#### Reviews
```
data/reviews/amazon_reviews_authenticated_20251104_172901.json (328 reviews, 0.2MB)
├─ Schema: TBD (inspect first)
```

#### Videos - YouTube
```
outputs/3m_claw_all_videos_20251104_153723.json (82 videos)
├─ Schema: {video_id, title, url, channel, views, thumbnail, platform, search_query}

outputs/3m_claw_new_videos.json (54 videos - subset of above)
data/social_videos/youtube_3m_claw_20251104_160154.json (7 videos)
data/social_videos/youtube_3m_claw_20251104_160243.json (168 videos)
outputs/full_garage_organizer_videos.json (12 general category videos)
data/youtube_garage_consumer_insights.json (8 videos)
```

#### Videos - TikTok
```
outputs/3m_claw_tiktok_apify_20251104_161329.json (162 videos)
├─ Schema: {video_id, title, url, channel, views, likes, shares, platform, search_query}
```

#### Additional Data
```
data/walmart_products.json (8,218 products)
data/homedepot_products.json (1,022 products)
data/amazon_products.json (514 products)
data/target_products.json (430 products)
data/lowes_products.json (400 products)
data/etsy_products.json (104 products)
data/reddit_pullpush_sample.json (880 posts)
data/tiktok_garage_consumer_insights.json (8 videos)
```

---

## OUTPUT FILE STRUCTURE

### Naming Convention
- **3M Claw brand:** `3m-claw-{data_type}.json`
- **Category aggregates:** `garage-organizer-category-{data_type}.json`
- **Competitive brands:** `{brand-name-slug}-{data_type}.json`

### Output Directory
`modules/category-intelligence/data/consolidated/`

### Required Master Files

#### 1. Brand-Specific Product Files (Top 10 brands by product count)
```
3m-claw-products.json
gladiator-products.json
rubbermaid-products.json
hyper-tough-products.json
command-products.json
everbilt-products.json
ryobi-products.json
husky-products.json
storewall-products.json
[additional brands based on data availability]
```

**Normalized Schema:**
```json
{
  "brand": "string",
  "total_products": "integer",
  "products": [
    {
      "product_id": "string (sku or asin or generated UUID)",
      "name": "string",
      "brand": "string",
      "retailer": "string (Amazon|Walmart|HomeDepot|Lowes|Target|Etsy)",
      "price": "float",
      "rating": "float (0-5)",
      "review_count": "integer",
      "url": "string",
      "sku": "string",
      "asin": "string (if Amazon)",
      "attributes": {
        "material": "string",
        "color": "string",
        "weight_capacity_lbs": "float",
        "installation_type": "string (derived from is_rail_or_slatwall, is_hook_or_hanger)",
        "categories": ["array of strings"],
        "seller": "string",
        "availability": "string"
      },
      "metadata": {
        "scraped_at": "ISO datetime",
        "source_file": "string"
      }
    }
  ]
}
```

#### 2. Brand-Specific Review Files
```
3m-claw-reviews.json
garage-organizer-category-reviews.json
[brand-name]-reviews.json (for top brands with review data)
```

**Normalized Schema:**
```json
{
  "brand": "string (or 'category' for category file)",
  "total_reviews": "integer",
  "reviews": [
    {
      "review_id": "string (generated UUID)",
      "product_id": "string (link to product file)",
      "product_name": "string",
      "brand": "string",
      "retailer": "string",
      "rating": "float (1-5)",
      "title": "string",
      "body": "string",
      "verified_purchase": "boolean",
      "helpful_count": "integer",
      "metadata": {
        "scraped_at": "ISO datetime",
        "source_file": "string"
      }
    }
  ]
}
```

#### 3. Brand-Specific Video Files (YouTube)
```
3m-claw-videos-youtube.json
garage-organizer-category-videos-youtube.json
```

**Normalized Schema:**
```json
{
  "brand_or_category": "string",
  "total_videos": "integer",
  "platform": "youtube",
  "videos": [
    {
      "video_id": "string (YouTube video ID)",
      "title": "string",
      "url": "string",
      "channel": "string",
      "views": "integer or string (normalize to integer if possible)",
      "thumbnail": "string (URL)",
      "search_query": "string",
      "metadata": {
        "collected_at": "ISO datetime",
        "source_file": "string"
      }
    }
  ]
}
```

#### 4. Brand-Specific Video Files (TikTok)
```
3m-claw-videos-tiktok.json
garage-organizer-category-videos-tiktok.json
```

**Normalized Schema:**
```json
{
  "brand_or_category": "string",
  "total_videos": "integer",
  "platform": "tiktok",
  "videos": [
    {
      "video_id": "string (TikTok video ID)",
      "title": "string",
      "url": "string",
      "channel": "string",
      "views": "integer",
      "likes": "integer",
      "shares": "integer",
      "search_query": "string",
      "metadata": {
        "collected_at": "ISO datetime",
        "source_file": "string"
      }
    }
  ]
}
```

#### 5. Category Aggregate Files
```
garage-organizer-category-products.json (all products across all brands)
garage-organizer-category-reviews.json (all reviews)
garage-organizer-category-videos-youtube.json (general category videos)
garage-organizer-category-videos-tiktok.json (general category videos)
garage-organizer-category-brands-summary.json (brand statistics)
```

**Category Brands Summary Schema:**
```json
{
  "category": "garage-organizer",
  "total_brands": "integer",
  "total_products": "integer",
  "total_reviews": "integer",
  "total_videos": "integer",
  "brands": [
    {
      "brand": "string",
      "product_count": "integer",
      "review_count": "integer",
      "avg_rating": "float",
      "avg_price": "float",
      "price_range": {"min": "float", "max": "float"},
      "retailers": ["array of retailers carrying this brand"]
    }
  ]
}
```

---

## CONSOLIDATION REQUIREMENTS

### 1. Data Deduplication
- **Products:** Deduplicate by `sku` (primary) or `asin` (Amazon) or exact `name + brand + retailer` match
- **Reviews:** Deduplicate by `product_id + review_title + review_body` (fuzzy match if needed)
- **Videos (YouTube):** Deduplicate by `video_id`
- **Videos (TikTok):** Deduplicate by `video_id`

### 2. Brand Extraction & Normalization
- Extract brands from all product files
- Normalize brand names (e.g., "3M" = "3m" = "3M Claw" → "3M")
- Identify top 8-10 brands by product count across all retailers
- Create separate files for each top brand
- Aggregate remaining brands into category files

### 3. Schema Harmonization
**You MUST handle schema differences:**

**Product Name Field:**
- `name` → normalize to `name`
- `title` → normalize to `name`

**Product ID:**
- `sku` → primary `product_id`
- `asin` → secondary `product_id` (keep both)
- If neither exists, generate UUID

**Review Count:**
- `reviews` → normalize to `review_count`
- `reviewCount` → normalize to `review_count`

**Missing Fields:**
- Set to `null` (not `"unknown"` or empty string)
- Document in metadata which fields were missing

### 4. Data Type Validation
**Required validations:**
- `price`: Must be float > 0 (remove if invalid)
- `rating`: Must be float 0-5 (remove if outside range)
- `review_count`: Must be integer ≥ 0
- `views/likes/shares`: Must be integer ≥ 0 (convert string to int if possible)
- `url`: Must start with `http://` or `https://`
- `video_id`: Must be non-empty string

**Validation Log:**
Create `data/consolidated/validation_log.json` with:
```json
{
  "total_records_processed": "integer",
  "total_records_valid": "integer",
  "total_records_dropped": "integer",
  "errors_by_type": {
    "invalid_price": "integer",
    "invalid_rating": "integer",
    "missing_required_field": "integer",
    "duplicate": "integer"
  },
  "dropped_records": [
    {"source_file": "string", "reason": "string", "record_sample": {}}
  ]
}
```

### 5. Attribute Extraction for Category Mapping
**Extract these attributes from ALL reviews and product descriptions (NO BIAS by retailer/price):**

From reviews, identify most frequently mentioned attributes:
- Installation ease (drilling required, damage-free, tools needed, time)
- Weight capacity (lbs, load bearing)
- Durability (rust resistance, longevity, material quality)
- Aesthetics (finish, color, visibility)
- Versatility (adjustable, modular, ecosystem)
- Value (price/performance ratio)

**Output:** `garage-organizer-category-attributes.json`
```json
{
  "category": "garage-organizer",
  "total_mentions_analyzed": "integer",
  "attributes": [
    {
      "attribute_name": "string (e.g., 'installation_ease')",
      "mention_count": "integer",
      "mention_percentage": "float (0-100)",
      "common_keywords": ["array of strings"],
      "sentiment_distribution": {
        "positive": "integer",
        "neutral": "integer",
        "negative": "integer"
      }
    }
  ]
}
```

---

## EXECUTION STEPS

### Step 1: Environment Setup
```bash
mkdir -p modules/category-intelligence/data/consolidated
cd modules/category-intelligence
```

### Step 2: Load & Inspect All Source Files
```python
import json
import glob
from pathlib import Path

# Load file manifest
manifest = json.load(open('FILE_MANIFEST_20251104.json'))

# Inspect schemas of each source file
for file_info in manifest['files']:
    path = file_info['path']
    # Load first record to understand schema
    # Log schema differences
```

### Step 3: Extract Top Brands
```python
# Aggregate all products from all sources
# Count products per brand
# Identify top 10 brands by product count
# Output: top_brands.json
```

### Step 4: Deduplicate & Normalize Products
```python
# For each source file:
#   - Load products
#   - Normalize schema to target schema
#   - Deduplicate by sku/asin
#   - Validate data types
#   - Split by brand
#   - Append to brand-specific files
```

### Step 5: Deduplicate & Normalize Reviews
```python
# Load all review files
# Normalize schema
# Link to product_id
# Deduplicate
# Split by brand
# Validate
```

### Step 6: Deduplicate & Normalize Videos
```python
# YouTube: Load all youtube files, deduplicate by video_id
# TikTok: Load all tiktok files, deduplicate by video_id
# Split by brand (3M Claw) vs category (general)
```

### Step 7: Generate Category Aggregates
```python
# Create garage-organizer-category-products.json (all products)
# Create garage-organizer-category-brands-summary.json
# Calculate statistics
```

### Step 8: Extract Category Attributes
```python
# Load all reviews
# Tokenize and extract attribute mentions
# Count frequency (unbiased across retailer/price)
# Generate garage-organizer-category-attributes.json
```

### Step 9: Validation
```python
# For each output file:
#   - Verify schema matches spec
#   - Check for data loss (compare input vs output counts)
#   - Validate data types
#   - Generate validation_log.json
```

### Step 10: Generate Summary Report
```markdown
# data/consolidated/CONSOLIDATION_REPORT.md

## Summary
- Total source files processed: X
- Total records in: Y
- Total records out: Z
- Data loss: 0%

## Output Files Created
- 3m-claw-products.json (X products)
- gladiator-products.json (X products)
- ...

## Schema Mapping
[Document all schema transformations]

## Validation Results
[Pass/Fail for each file]
```

---

## PYTHON IMPLEMENTATION TEMPLATE

```python
#!/usr/bin/env python3
"""
Data Consolidation Script for 3M Category Intelligence
Handles heterogeneous schemas with zero data loss
"""

import json
import hashlib
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import uuid

BASE_PATH = Path("modules/category-intelligence")
OUTPUT_DIR = BASE_PATH / "data" / "consolidated"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class DataConsolidator:
    def __init__(self):
        self.products = defaultdict(list)  # brand -> [products]
        self.reviews = defaultdict(list)   # brand -> [reviews]
        self.videos_yt = defaultdict(list) # brand -> [videos]
        self.videos_tt = defaultdict(list) # brand -> [videos]
        self.validation_log = {
            "total_records_processed": 0,
            "total_records_valid": 0,
            "total_records_dropped": 0,
            "errors_by_type": defaultdict(int),
            "dropped_records": []
        }

    def normalize_brand_name(self, brand):
        """Normalize brand names to consistent format"""
        if not brand:
            return None
        brand = str(brand).strip().lower()
        # Add normalization rules
        if "3m" in brand or "claw" in brand:
            return "3M"
        if "command" in brand:
            return "Command"
        # Add more rules
        return brand.title()

    def normalize_product(self, raw_product, source_file):
        """Transform heterogeneous product schemas to normalized format"""
        try:
            normalized = {
                "product_id": raw_product.get("sku") or raw_product.get("asin") or str(uuid.uuid4()),
                "name": raw_product.get("name") or raw_product.get("title"),
                "brand": self.normalize_brand_name(raw_product.get("brand")),
                "retailer": raw_product.get("retailer"),
                "price": float(raw_product.get("price", 0)),
                "rating": float(raw_product.get("rating", 0)),
                "review_count": int(raw_product.get("reviews") or raw_product.get("reviewCount") or 0),
                "url": raw_product.get("url"),
                "sku": raw_product.get("sku"),
                "asin": raw_product.get("asin"),
                "attributes": {
                    "material": raw_product.get("material"),
                    "color": raw_product.get("color"),
                    "weight_capacity_lbs": raw_product.get("weight_capacity_lbs"),
                    "installation_type": self._derive_installation_type(raw_product),
                    "categories": raw_product.get("attributes", {}).get("categories", []),
                    "seller": raw_product.get("attributes", {}).get("seller"),
                    "availability": raw_product.get("attributes", {}).get("availability")
                },
                "metadata": {
                    "scraped_at": raw_product.get("scraped_at") or datetime.now().isoformat(),
                    "source_file": source_file
                }
            }

            # Validate
            if not self._validate_product(normalized):
                return None

            self.validation_log["total_records_valid"] += 1
            return normalized

        except Exception as e:
            self.validation_log["total_records_dropped"] += 1
            self.validation_log["errors_by_type"]["normalization_error"] += 1
            self.validation_log["dropped_records"].append({
                "source_file": source_file,
                "reason": str(e),
                "record_sample": raw_product
            })
            return None

    def _validate_product(self, product):
        """Validate normalized product"""
        if not product.get("name"):
            self.validation_log["errors_by_type"]["missing_name"] += 1
            return False
        if product["price"] <= 0:
            self.validation_log["errors_by_type"]["invalid_price"] += 1
            return False
        if not (0 <= product["rating"] <= 5):
            self.validation_log["errors_by_type"]["invalid_rating"] += 1
            return False
        return True

    def _derive_installation_type(self, product):
        """Derive installation type from various fields"""
        if product.get("is_rail_or_slatwall") == "yes":
            return "rail_system"
        if product.get("is_hook_or_hanger") == "yes":
            return "hook_hanger"
        return "unknown"

    def deduplicate_products(self, products):
        """Deduplicate by sku/asin"""
        seen = set()
        unique = []
        for p in products:
            key = p.get("sku") or p.get("asin") or p.get("name")
            if key not in seen:
                seen.add(key)
                unique.append(p)
            else:
                self.validation_log["errors_by_type"]["duplicate"] += 1
        return unique

    def process_product_files(self):
        """Load and normalize all product files"""
        product_files = [
            "data/retailers/all_products_final_with_lowes.json",
            "data/expanded_coverage/amazon_products_with_reviews_20251104_155959.json",
            "outputs/garage_organizer_sample_20251104.json",
            "data/walmart_products.json",
            "data/homedepot_products.json",
            "data/amazon_products.json",
            "data/target_products.json",
            "data/lowes_products.json",
            "data/etsy_products.json"
        ]

        for file_path in product_files:
            full_path = BASE_PATH / file_path
            if not full_path.exists():
                continue

            print(f"Processing {file_path}...")
            with open(full_path) as f:
                data = json.load(f)

            # Handle both array and object with "records" key
            records = data if isinstance(data, list) else data.get("records", [])

            for raw_product in records:
                self.validation_log["total_records_processed"] += 1
                normalized = self.normalize_product(raw_product, file_path)
                if normalized:
                    brand = normalized["brand"] or "Unknown"
                    self.products[brand].append(normalized)

    def get_top_brands(self, n=10):
        """Get top N brands by product count"""
        brand_counts = [(brand, len(products)) for brand, products in self.products.items()]
        brand_counts.sort(key=lambda x: x[1], reverse=True)
        return [brand for brand, count in brand_counts[:n]]

    def write_brand_products(self):
        """Write brand-specific product files"""
        top_brands = self.get_top_brands(10)

        for brand in top_brands:
            products = self.deduplicate_products(self.products[brand])
            slug = brand.lower().replace(" ", "-")

            output = {
                "brand": brand,
                "total_products": len(products),
                "products": products
            }

            output_file = OUTPUT_DIR / f"{slug}-products.json"
            with open(output_file, 'w') as f:
                json.dump(output, f, indent=2)
            print(f"✓ Created {output_file} ({len(products)} products)")

    def write_category_aggregates(self):
        """Write category-level aggregate files"""
        all_products = []
        for products in self.products.values():
            all_products.extend(products)

        all_products = self.deduplicate_products(all_products)

        output = {
            "category": "garage-organizer",
            "total_products": len(all_products),
            "products": all_products
        }

        output_file = OUTPUT_DIR / "garage-organizer-category-products.json"
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
        print(f"✓ Created {output_file} ({len(all_products)} products)")

    def write_validation_log(self):
        """Write validation log"""
        output_file = OUTPUT_DIR / "validation_log.json"
        with open(output_file, 'w') as f:
            json.dump(self.validation_log, f, indent=2)
        print(f"✓ Created {output_file}")

def main():
    consolidator = DataConsolidator()

    print("Starting data consolidation...")
    consolidator.process_product_files()
    consolidator.write_brand_products()
    consolidator.write_category_aggregates()
    consolidator.write_validation_log()

    print("\n" + "="*80)
    print("CONSOLIDATION COMPLETE")
    print("="*80)
    print(f"Records processed: {consolidator.validation_log['total_records_processed']}")
    print(f"Records valid: {consolidator.validation_log['total_records_valid']}")
    print(f"Records dropped: {consolidator.validation_log['total_records_dropped']}")
    print(f"Data integrity: {100 * consolidator.validation_log['total_records_valid'] / max(consolidator.validation_log['total_records_processed'], 1):.2f}%")

if __name__ == "__main__":
    main()
```

---

## SUCCESS CRITERIA CHECKLIST

- [ ] All 69 source files processed
- [ ] Zero data loss (all valid records preserved)
- [ ] Top 10 brands identified and files created
- [ ] All schemas normalized to spec
- [ ] Deduplication applied (sku/asin/video_id)
- [ ] Data type validation passed
- [ ] Category attribute extraction complete (unbiased)
- [ ] PostgreSQL-ready JSON structure
- [ ] validation_log.json created with <1% drop rate
- [ ] CONSOLIDATION_REPORT.md generated

---

## POSTGRESQL IMPORT NOTES

After consolidation, import to PostgreSQL with:

```sql
CREATE TABLE products (
    product_id VARCHAR PRIMARY KEY,
    name TEXT,
    brand VARCHAR,
    retailer VARCHAR,
    price DECIMAL(10,2),
    rating DECIMAL(3,2),
    review_count INTEGER,
    url TEXT,
    sku VARCHAR,
    asin VARCHAR,
    attributes JSONB,
    metadata JSONB
);

CREATE TABLE reviews (
    review_id VARCHAR PRIMARY KEY,
    product_id VARCHAR REFERENCES products(product_id),
    brand VARCHAR,
    rating DECIMAL(3,2),
    title TEXT,
    body TEXT,
    verified_purchase BOOLEAN,
    metadata JSONB
);

CREATE TABLE videos (
    video_id VARCHAR PRIMARY KEY,
    platform VARCHAR CHECK (platform IN ('youtube', 'tiktok')),
    brand_or_category VARCHAR,
    title TEXT,
    url TEXT,
    channel VARCHAR,
    views INTEGER,
    likes INTEGER,
    shares INTEGER,
    metadata JSONB
);
```

Import command:
```bash
# Import products
psql -d category_intelligence -c "\copy products FROM 'consolidated/3m-claw-products.json' CSV QUOTE E'\x01' DELIMITER E'\t'"

# Or use Python script with psycopg2
```

---

## QUESTIONS FOR CLARIFICATION

If you encounter ambiguity during execution:
1. **Missing brand field:** Assign to "Unknown" brand
2. **Conflicting data (same sku, different prices):** Keep most recent by scraped_at
3. **Invalid data types:** Log and drop record (document in validation_log)
4. **Unknown schema field:** Preserve in metadata.raw_fields{}

**END OF PROMPT**
