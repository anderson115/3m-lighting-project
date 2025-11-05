# Data Collection Log - Category Intelligence Module

## Collection Session: November 4, 2025

### Objective
Expand product coverage with ratings and reviews to enable high-confidence consumer evaluation feature extraction.

### Data Sources

#### 1. Amazon Products (IN PROGRESS)
**Status:** Active scraping
**Target:** 500+ products with reviews
**Method:** BeautifulSoup web scraper
**Current Progress:** 360+ products collected
**Output:** `data/expanded_coverage/amazon_products_with_reviews_YYYYMMDD_HHMMSS.json`

**Search Terms:**
- garage hooks heavy duty
- garage storage hooks wall mount
- garage organization pegboard
- garage bike storage hooks
- garage shelving heavy duty
- garage tool organizer wall
- garage overhead storage rack
- garage wall mount bike rack

**Data Fields Collected:**
- title
- price
- rating
- reviewCount
- asin
- url
- search_term
- retailer
- scraped_at
- reviews (array of review objects with title, body, rating, date, verified)

#### 2. Target Products (PLANNED)
**Status:** Pending
**Target:** 500+ products with ratings
**Method:** Playwright scraper

#### 3. 3M Claw Social Videos (PLANNED)
**Status:** Pending
**Sources:** YouTube, Reddit, TikTok
**Target:** 100+ videos/posts about 3M Claw brand
**Output:** `data/social_videos/`

### Existing Data (Baseline)

**Total Products:** 2,000
- Amazon: 400 (100% with ratings)
- Home Depot: 400 (100% with ratings)
- Lowe's: 400 (61% with ratings)
- Walmart: 400 (84% with ratings)
- Target/Unknown: 400 (0% with ratings)

**Unique Brands:** 493

**Top Brands with Rating Coverage:**
1. Gladiator - 114 products, 4.67★
2. Rubbermaid - 82 products, 4.48★
3. Hyper Tough - 79 products, 4.77★
4. Command - 56 products, 4.55★
5. Everbilt - 52 products, 4.52★

### Data Quality Goals

1. **Breadth:** Cover 3,000+ total products across all major retailers
2. **Depth:** Collect 10-20 reviews per product for top 200 products
3. **Ratings Coverage:** Achieve 90%+ rating coverage across all products
4. **Review Text:** Collect actual review text for evaluation feature extraction

### Consumer Evaluation Features to Extract

From review text analysis, identify what consumers evaluate:
- **Installation Ease:** Tool requirements, time, skill level
- **Weight Capacity:** Actual vs. claimed performance
- **Durability:** Rust resistance, coating quality, longevity
- **Surface Compatibility:** Drywall, concrete, metal, wood
- **Value for Money:** Price vs. quality perception
- **Aesthetics:** Visual appeal, finish quality
- **Damage-Free:** Rental-friendly, removable
- **Versatility:** Use cases, adaptability

### Next Steps

1. ✅ Complete Amazon scraping (500+ products with reviews)
2. ⏳ Scrape Target products with ratings
3. ⏳ Scrape 3M Claw social content (YouTube, Reddit)
4. ⏳ Consolidate all data into master dataset
5. ⏳ Extract evaluation features using NLP
6. ⏳ Create spider/radar maps of product evaluation criteria
7. ⏳ Update category intelligence insights with expanded data

### File Structure

```
data/
├── expanded_coverage/
│   ├── amazon_products_with_reviews_*.json
│   ├── target_products_*.json
│   └── lowes_ratings_fill_*.json
├── social_videos/
│   ├── youtube_3m_claw_*.json
│   ├── reddit_3m_claw_*.json
│   └── tiktok_3m_claw_*.json
├── retailers/
│   └── all_products_final_with_lowes.json (baseline)
└── consolidated/
    └── master_products_YYYYMMDD.json (to be created)
```

### Budget Tracking

- **Bright Data Budget:** $25 allocated
- **Estimated Usage:** $5-10 (simple HTTP scraping, no browser automation)
- **Remaining:** $15-20 for future collections

### Data Labeling Standards

**Retailer field values:**
- "Amazon"
- "Home Depot"
- "Lowes"
- "Walmart"
- "Target"

**Collection metadata:**
- `scraped_at`: ISO 8601 datetime
- `search_term`: Original query used
- `data_source`: "web_scraping" | "api" | "manual"
- `scraper_version`: "v1.0"

---

**Last Updated:** 2025-11-04 23:55 UTC
**Status:** Active scraping in progress
