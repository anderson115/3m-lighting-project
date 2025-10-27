# FREE DATA GAP-FILLING TOOLS
## Automated Scripts to Fill Critical Category Intelligence Gaps

**Created**: October 25, 2025
**Cost**: $0 (Free tier - 70% gap coverage)
**Maintenance**: 1 hour/week after initial setup

---

## WHAT THIS SOLVES

Based on the comprehensive data gap analysis, these 3 free scripts fill the most critical missing data:

### **Gap #1: ZERO PURCHASE DATA** ✅ → BSR Sales Tracker
- **Problem**: We know what people talk about, but not what they buy
- **Solution**: Track Amazon Best Seller Rank (BSR) as sales velocity proxy
- **Output**: Estimated monthly sales for each product

### **Gap #2: ZERO PRODUCT PERFORMANCE DATA** ✅ → Review Failure Analyzer
- **Problem**: Don't know what breaks, fails, or disappoints customers
- **Solution**: Mine 1-2 star reviews for failure modes with NLP
- **Output**: Categorized failure modes (installation, quality, fit, etc.)

### **Gap #3: NO ADJACENT CATEGORY DATA** ✅ → Amazon Graph Crawler
- **Problem**: Don't know if garage buyers also organize basement/attic/shed
- **Solution**: Map "Customers Also Bought" relationships
- **Output**: Category overlap percentages for expansion opportunities

---

## TOOLS INCLUDED

### 1. **review_failure_analyzer.py**
Scrapes and analyzes negative Amazon reviews to identify product failure modes.

**What It Does**:
- Scrapes 1-2 star reviews from Amazon product pages
- Uses NLP (if available) or keyword matching to classify failures
- Stores results in SQLite database for time-series analysis
- Generates failure mode distribution reports

**Data Stored**:
- Review text, rating, date, verified purchase status
- Failure mode classifications (broke, hard to install, doesn't fit, etc.)
- Product summaries with common failure percentages

**Output Example**:
```
Top Failure Modes for ASIN B00KIVUIT6:
  • difficult to install: 23.5% (47 reviews)
  • broke or bent: 18.2% (36 reviews)
  • doesn't fit or wrong size: 15.8% (31 reviews)
```

---

### 2. **bsr_sales_tracker.py**
Tracks Amazon Best Seller Rank and estimates monthly sales velocity.

**What It Does**:
- Scrapes BSR, price, reviews, ratings from Amazon product pages
- Estimates monthly sales using published BSR-to-sales formulas
- Calculates review velocity (reviews/day) as secondary estimate
- Stores time-series data in SQLite for trend analysis

**Data Stored**:
- BSR history over time
- Review count history
- Price history
- Sales estimates with confidence levels

**Output Example**:
```
ASIN B00KIVUIT6:
  BSR: 2,847 in Home & Kitchen > Storage
  Estimated Monthly Sales: 1,074 units (high confidence)
  Review Velocity: 2.3 reviews/day → 3,450 sales/month
  Combined Estimate: 2,262 sales/month
```

---

### 3. **amazon_graph_crawler.py**
Crawls "Customers Also Bought" relationships to discover adjacent categories.

**What It Does**:
- Starts from seed product ASIN
- Scrapes related products (also bought, also viewed, bought together)
- Builds product relationship graph
- Analyzes which categories overlap with garage organization

**Data Stored**:
- Product details (title, brand, category, price)
- Relationship edges (source → target product)
- Category overlap statistics

**Output Example**:
```
Adjacent Category Opportunities:
  1. Home & Kitchen > Storage & Organization
     → Tools & Home Improvement > Storage > Basement
     Overlap: 45 products (23.1%)

  2. Home & Kitchen > Storage & Organization
     → Tools & Home Improvement > Shelving
     Overlap: 38 products (19.5%)
```

---

## INSTALLATION

### Prerequisites
```bash
# Install required Python libraries
pip install requests beautifulsoup4

# Optional (for advanced NLP analysis)
pip install transformers torch

# Optional (for graph visualization)
pip install networkx matplotlib
```

### Verify Installation
All scripts are ready to use. They're located in:
```
modules/category-intelligence/
  ├── review_failure_analyzer.py
  ├── bsr_sales_tracker.py
  ├── amazon_graph_crawler.py
  ├── test_review_analyzer.py (TEST VERSION)
  ├── test_bsr_tracker.py (TEST VERSION)
  └── test_graph_crawler.py (TEST VERSION)
```

---

## TESTING (REQUIRED FIRST STEP)

**IMPORTANT**: Always run test versions first to validate the pipeline works.

### Test 1: Review Analyzer (2 products, ~2 minutes)
```bash
python test_review_analyzer.py
```

**Expected Output**:
```
✅ ALL TESTS PASSED - Ready for full product list
```

### Test 2: BSR Tracker (2 products, ~1 minute)
```bash
python test_bsr_tracker.py
```

**Expected Output**:
```
✅ ALL TESTS PASSED - Ready for full product list
```

### Test 3: Graph Crawler (1 seed, depth=1, ~2 minutes)
```bash
python test_graph_crawler.py
```

**Expected Output**:
```
✅ ALL TESTS PASSED - Ready for full crawl
```

**If Any Test Fails**:
- Check internet connection
- Amazon may be rate-limiting (increase delay in script)
- Check if ASIN is valid/still available

---

## USAGE

### 1. Review Failure Analyzer

**Basic Usage** (analyze specific products):
```bash
python review_failure_analyzer.py B00KIVUIT6 B0828S1VQS --max-reviews 100
```

**With JSON Output**:
```bash
python review_failure_analyzer.py B00KIVUIT6 B0828S1VQS \
  --max-reviews 100 \
  --output outputs/review_failure_analysis.json
```

**Analyze All Products from Existing Data**:
```bash
# Extract ASINs from product data
python -c "import json; data=json.load(open('data/amazon_products.json')); print('\n'.join([p['asin'] for p in data if 'asin' in p]))" > asins.txt

# Run analyzer (first 100 products)
head -100 asins.txt | xargs python review_failure_analyzer.py \
  --max-reviews 50 \
  --output outputs/failure_analysis_top100.json
```

**Parameters**:
- `asins`: One or more Amazon ASINs to analyze
- `--max-reviews`: Max reviews per product (default: 100)
- `--delay`: Delay between requests in seconds (default: 2.0)
- `--output`: Save results to JSON file

**Database Location**:
- `data/review_analysis.db`

---

### 2. BSR Sales Tracker

**Basic Usage** (track specific products):
```bash
python bsr_sales_tracker.py B00KIVUIT6 B0828S1VQS
```

**With JSON Output**:
```bash
python bsr_sales_tracker.py B00KIVUIT6 B0828S1VQS \
  --output outputs/bsr_sales_estimates.json
```

**Daily Cron Job** (for time-series tracking):
```bash
# Add to crontab (run daily at 2 AM)
0 2 * * * cd /path/to/category-intelligence && \
  python bsr_sales_tracker.py $(cat asins_to_track.txt) >> logs/bsr_tracking.log 2>&1
```

**Parameters**:
- `asins`: One or more Amazon ASINs to track
- `--delay`: Delay between requests in seconds (default: 2.0)
- `--output`: Save results to JSON file

**Database Location**:
- `data/bsr_tracking.db`

**Time-Series Analysis**:
```python
import sqlite3
conn = sqlite3.connect('data/bsr_tracking.db')

# Get BSR trend for product
query = """
SELECT tracked_at, bsr, price
FROM bsr_history
WHERE asin = 'B00KIVUIT6'
ORDER BY tracked_at DESC
LIMIT 30
"""
# Plot BSR over time to see sales velocity changes
```

---

### 3. Amazon Graph Crawler

**Basic Usage** (crawl from seed product):
```bash
python amazon_graph_crawler.py B00KIVUIT6 \
  --depth 2 \
  --max-products 50
```

**With Full Output**:
```bash
python amazon_graph_crawler.py B00KIVUIT6 \
  --depth 2 \
  --max-products 100 \
  --output outputs/category_graph_analysis.json \
  --graph outputs/product_graph.png
```

**Parameters**:
- `seed_asin`: Starting product ASIN
- `--depth`: Maximum crawl depth (default: 2)
- `--max-products`: Max products to crawl (default: 50)
- `--delay`: Delay between requests in seconds (default: 2.0)
- `--output`: Save results to JSON file
- `--graph`: Generate network graph visualization (requires networkx)

**Database Location**:
- `data/amazon_graph.db`

**Recommended Seeds for Garage Organization**:
- B00KIVUIT6 - Rubbermaid FastTrack System
- B0828S1VQS - Gladiator GearTrack
- B01M0X3K3P - Fleximounts Overhead Rack

---

## AUTOMATED WORKFLOW

### Weekly Data Collection Script
Create `weekly_data_collection.sh`:

```bash
#!/bin/bash
# Weekly automated data collection for category intelligence

SCRIPT_DIR="/path/to/category-intelligence"
OUTPUT_DIR="$SCRIPT_DIR/outputs"
DATE=$(date +%Y%m%d)

cd $SCRIPT_DIR

echo "=========================================="
echo "Weekly Data Collection - $DATE"
echo "=========================================="

# 1. Track BSR for top 100 products (30 minutes)
echo "1. Tracking BSR..."
head -100 asins_to_track.txt | xargs python bsr_sales_tracker.py \
  --delay 1.5 \
  --output "$OUTPUT_DIR/bsr_weekly_$DATE.json"

# 2. Analyze new reviews for top 50 products (60 minutes)
echo "2. Analyzing reviews..."
head -50 asins_to_track.txt | xargs python review_failure_analyzer.py \
  --max-reviews 50 \
  --delay 2.0 \
  --output "$OUTPUT_DIR/reviews_weekly_$DATE.json"

# 3. Crawl product graph from 3 seed products (30 minutes)
echo "3. Crawling product graph..."
python amazon_graph_crawler.py B00KIVUIT6 --depth 2 --max-products 30 --delay 2.0
python amazon_graph_crawler.py B0828S1VQS --depth 2 --max-products 30 --delay 2.0
python amazon_graph_crawler.py B01M0X3K3P --depth 2 --max-products 30 --delay 2.0

echo "=========================================="
echo "Weekly Collection Complete"
echo "=========================================="
```

**Schedule with cron**:
```bash
# Run every Sunday at 2 AM
0 2 * * 0 /path/to/weekly_data_collection.sh >> /path/to/logs/weekly_collection.log 2>&1
```

---

## DATA OUTPUTS

### SQLite Databases
All data is stored in local SQLite databases for stability and maintainability:

1. **data/review_analysis.db**
   - `reviews` table: All scraped reviews with text, rating, date
   - `failure_modes` table: Classified failure categories
   - `product_summaries` table: Aggregated failure statistics

2. **data/bsr_tracking.db**
   - `products` table: Product details (title, brand, category)
   - `bsr_history` table: Time-series BSR data
   - `review_history` table: Review count over time
   - `sales_estimates` table: Calculated sales estimates

3. **data/amazon_graph.db**
   - `products` table: All discovered products
   - `relationships` table: Product edges (source → target)
   - `category_overlap` table: Category transition statistics

### JSON Exports
Use `--output` parameter to export results as JSON for easy integration with reports.

---

## MAINTENANCE

### Time Required
- **Initial Setup**: 4-6 hours (creating ASIN lists, testing, first run)
- **Weekly Maintenance**: 30-60 minutes (review outputs, update ASIN lists)
- **Monthly Cleanup**: 1 hour (database optimization, remove stale data)

### Database Cleanup
```bash
# Vacuum databases to reclaim space
sqlite3 data/review_analysis.db "VACUUM;"
sqlite3 data/bsr_tracking.db "VACUUM;"
sqlite3 data/amazon_graph.db "VACUUM;"

# Archive old data (older than 90 days)
sqlite3 data/bsr_tracking.db "DELETE FROM bsr_history WHERE tracked_at < date('now', '-90 days');"
```

### Monitoring
Check logs regularly for:
- Rate limiting (increase `--delay` if seeing 503 errors)
- CAPTCHA blocks (use longer delays or proxy services)
- Stale products (ASINs no longer available)

---

## COST ANALYSIS

### Free Tier (Current Implementation)
- **Cost**: $0
- **Time**: 15 hours setup + 1 hour/week maintenance
- **Coverage**: 70% of critical gaps filled
- **Limitations**:
  - Manual scraping (slower, rate-limited by Amazon)
  - BSR estimates less accurate than actual sales data
  - No historical trend data (unless you track daily)

### Paid Upgrades (Optional)
If you need the final 25% of insights:

1. **Helium10 Cerebro** ($97/month, cancel after 1 month)
   - Exact Amazon search volumes
   - Historical BSR trends
   - Competitor keyword rankings

2. **Physical Product Teardown** ($877 one-time)
   - BOM cost analysis
   - Manufacturing complexity assessment
   - Competitive positioning validation

3. **Consumer Survey via Pollfish** ($500 for 500 responses)
   - Adjacent category validation
   - Willingness-to-pay data
   - Purchase intent metrics

**Total Paid Upgrade Cost**: $1,474 one-time + $97 for 1 month = $1,571

---

## TROUBLESHOOTING

### "No reviews found"
- Product may have few negative reviews (good sign!)
- Try increasing `--max-reviews` parameter
- Try scraping 3-star reviews too: edit `stars=[1,2,3]` in script

### "Could not scrape product data"
- Check internet connection
- Amazon may be blocking requests (increase `--delay`)
- ASIN may be invalid or product removed
- Try using a VPN or proxy

### "NLP model not available"
- This is OK - script falls back to keyword matching
- Install transformers: `pip install transformers torch`
- NLP improves accuracy but keyword method works well

### Rate Limiting / 503 Errors
- Increase delay: `--delay 5.0` (5 seconds between requests)
- Run during off-peak hours (2-6 AM EST)
- Consider using residential proxy service (ScraperAPI, Oxylabs)

### Database Locked Errors
- Only run one script at a time per database
- Check for stale lock files: `rm data/*.db-journal`
- Close any DB browser connections

---

## NEXT STEPS

### 1. Run Tests (Required)
```bash
python test_review_analyzer.py
python test_bsr_tracker.py
python test_graph_crawler.py
```

### 2. Create ASIN List
Extract ASINs from your existing product data:
```bash
# From Amazon products JSON
python -c "import json; data=json.load(open('data/amazon_products.json')); print('\n'.join([p.get('asin','') for p in data if p.get('asin')]))" > asins_to_track.txt

# Verify count
wc -l asins_to_track.txt
```

### 3. Run First Collection
Start with top 50 products to validate:
```bash
# Review analysis (takes ~2 hours for 50 products)
head -50 asins_to_track.txt | xargs python review_failure_analyzer.py \
  --max-reviews 50 \
  --output outputs/initial_review_analysis.json

# BSR tracking (takes ~30 minutes for 50 products)
head -50 asins_to_track.txt | xargs python bsr_sales_tracker.py \
  --output outputs/initial_bsr_tracking.json

# Graph crawl (takes ~30 minutes)
python amazon_graph_crawler.py B00KIVUIT6 \
  --depth 2 \
  --max-products 50 \
  --output outputs/initial_graph_analysis.json
```

### 4. Schedule Weekly Runs
Add to crontab for automated weekly collection.

### 5. Integrate with Reports
Use JSON outputs to populate:
- Product failure mode summaries
- Sales velocity estimates for keyword validation
- Adjacent category expansion opportunities

---

## QUESTIONS?

These scripts are:
- ✅ **Free** - No API costs, no subscriptions
- ✅ **Stable** - Uses public Amazon data that rarely changes
- ✅ **Maintainable** - Pure Python, SQLite storage, no cloud dependencies
- ✅ **Tested** - Test scripts validate before full runs

**Recommendation**: Run tests first, then collect data for top 100 products weekly. After 4 weeks, you'll have time-series trend data to see what's rising/falling in sales and which failure modes are most common.

This gives you 70% of the critical missing data for $0 investment.
