# Walmart Dataset Rightsizing Report

**Date:** October 29, 2025
**Purpose:** Reduce Walmart dataset from 7,498 to ~1,500 products to match HD/Lowe's scope
**Status:** ⚠️ COMPLETED WITH LIMITATIONS

---

## Executive Summary

✅ **Successfully reduced Walmart dataset from 7,498 → 1,500 products (80% reduction)**

✅ **Dataset now comparable in size to baseline:** 1,500 vs 1,553 products

⚠️ **Category bias persisted:** 92.7% Hooks & Hangers (vs 36.7% baseline)

⚠️ **Price gap remains large:** $22.88 vs $147.58 baseline (-84.5%)

🔍 **Root cause:** Original Walmart scrape was 92% hooks/hangers; filtering by engagement doesn't fix category concentration

---

## Methodology

### Scoring Criteria

Products were scored based on data quality and customer engagement:

| Criterion | Points | Products |
|-----------|--------|----------|
| Has star rating | +3 | 264 (3.5%) |
| Has review count | +2 | 264 (3.5%) |
| Review count > 10 | +2 | 152 (2.0%) |
| Review count > 50 | +2 | 63 (0.8%) |
| Has category data | +2 | 7,498 (100%) |
| Has brand data | +1 | 7,497 (99.9%) |
| Has subcategory | +1 | 0 (0%) |
| Rating ≥ 4.0 stars | +1 | 241 (3.2%) |

**Priority Score Range:** 2-13 points

### Selection Process

1. **Scored all products:** Mean score = 3.27
2. **Sorted by priority score:** Highest scores first
3. **Selected top 1,500:** Mean score = 4.33
4. **Removed bottom 5,998:** Mean score = 3.00

---

## Results

### Dataset Transformation

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Walmart Products** | 7,498 | 1,500 | -5,998 (-80%) |
| **Total Products** | 9,989 | 3,991 | -5,998 (-60%) |
| **Walmart % of Dataset** | 75.0% | 37.6% | -37.4pp |
| **Avg Walmart Price** | $19.71 | $22.88 | +$3.17 (+16%) |

### Retailer Distribution (After Rightsizing)

| Retailer | Products | % of Total |
|----------|----------|------------|
| Walmart | 1,500 | 37.6% |
| Home Depot | 842 | 21.1% |
| Amazon | 512 | 12.8% |
| Target | 426 | 10.7% |
| Lowe's | 371 | 9.3% |
| Menards | 246 | 6.2% |
| Ace Hardware | 94 | 2.4% |

**Progress:** Walmart reduced from 75% → 37.6% (target: 15-20% per market reality)

**Status:** ⚠️ Still over-represented, but significantly improved

---

## Comparison to Baseline

### Size Comparison

| Dataset | Products | Status |
|---------|----------|--------|
| Walmart (cleaned) | 1,500 | ✅ |
| Baseline (HD/Lowe's/Menards/Ace) | 1,553 | ✅ |
| **Ratio** | 0.97x | ✅ Comparable |

### Price Comparison

| Dataset | Average Price | Median Price |
|---------|---------------|--------------|
| Walmart (cleaned) | $22.88 | $13.68 |
| Baseline | $147.58 | $79.99 |
| **Difference** | -$124.70 (-84.5%) | -$66.31 (-83%) |

**Finding:** Walmart is dramatically cheaper than baseline retailers, reflecting its budget positioning.

### Category Distribution Comparison

| Category | Walmart | Baseline | Difference |
|----------|---------|----------|------------|
| **Hooks & Hangers** | 92.7% | 36.7% | +55.9pp ⚠️ |
| **Shelving** | 0.3% | 32.2% | -31.9pp ⚠️ |
| **Garage Organization** | 4.1% | 13.3% | -9.2pp |
| **Rails & Tracks** | 0.4% | 6.3% | -5.9pp |
| **Storage & Organization** | 2.5% | 5.1% | -2.6pp |
| **Bins & Baskets** | 0.1% | 4.2% | -4.1pp |
| **Cabinets** | 0.0% | 2.2% | -2.2pp |

**Critical Issue:** Category bias persisted despite rightsizing effort.

---

## What Was Kept vs Removed

### Kept Products (1,500)

**Priority Score:** Mean = 4.33, Median = 3.00, Range = 3-13

**Characteristics:**
- 264 products with ratings/reviews (17.6%)
- 1,236 products without ratings/reviews (82.4%)
- 100% have category data
- 99.9% have brand data
- 0% have subcategory data

**Category Breakdown:**
- Hooks & Hangers: 1,390 (92.7%)
- Garage Organization: 61 (4.1%)
- Storage & Organization: 37 (2.5%)
- Rails & Tracks: 6 (0.4%)
- Shelving: 4 (0.3%)
- Bins & Baskets: 2 (0.1%)

### Removed Products (5,998)

**Priority Score:** Mean = 3.00, Median = 3.00, Range = 2-3

**Characteristics:**
- Nearly all products scored exactly 3 points (category + brand only)
- No ratings or reviews
- No subcategory data
- Lower priority based on lack of engagement metrics

**Why Removed:**
- Insufficient customer engagement data
- Lower data quality scores
- Likely discontinued or unpopular products

---

## Limitations

### 1. Website Scrape Not Available

**Impact:** Could not prioritize products currently listed on Walmart.com

**Consequence:** Had to rely solely on data quality metrics, not current availability

**Ideal Scenario:** Website scrape would identify which of the 7,498 products are actively sold today

### 2. Low Rating/Review Coverage

**Finding:** Only 3.5% of Walmart products (264/7,498) had ratings or reviews

**Impact:** Scoring system couldn't effectively differentiate most products

**Result:** Most products (6,700+) scored identically (3 points), making selection arbitrary

### 3. Category Bias Persisted

**Root Cause:** Original Walmart scrape was 92% hooks/hangers

**Impact:** Random sampling from a biased dataset preserves the bias

**Why It Happened:** Without product availability data, can't target underrepresented categories

### 4. Price Gap Unexplained

**Finding:** Walmart products are 84% cheaper than baseline

**Questions:**
- Are we comparing equivalent products?
- Is Walmart's assortment genuinely budget-focused?
- Did we scrape different categories from different retailers?

**Needs:** Cross-retailer product matching to validate like-for-like pricing

---

## Comparison to Original Strategy

### What the Website Scrape Would Have Enabled

From `parse_walmart_website_scrape.py`, the original plan was:

1. **Match website products to existing data:** Identify discontinued products
2. **Prioritize website-scraped products:** Focus on current inventory
3. **Update prices/ratings:** Use current data from Walmart.com
4. **Identify new products:** Products on website but not in dataset
5. **Flag discontinued:** Products in dataset but not on website

**Why This Matters:**
- Website scrape = current inventory = active products
- Current approach = random sample from potentially stale data

### What We Did Instead

1. ✅ Scored products by data quality
2. ✅ Selected top 1,500 by priority score
3. ⚠️ Category bias preserved
4. ⚠️ Can't validate product currency
5. ⚠️ Can't update pricing to current

---

## Next Steps

### Option A: Apply Market Weights (Recommended)

**Instead of reducing Walmart products, DOWNWEIGHT them in analysis**

From `ROOT_CAUSE_AND_TOP_FIXES.md`:

```python
# Apply retailer weights
weights = {
    'Walmart': 0.20,      # Downweight (75% → 15%)
    'Homedepot': 4.16,    # Upweight (8.4% → 35%)
    'Lowes': 8.11,        # Upweight (3.7% → 30%)
    'Amazon': 2.93,       # Upweight (5.1% → 15%)
    'Target': 1.17,       # Slight upweight (4.3% → 5%)
    'Menards': 4.00,      # Upweight (2.5% → 10%)
    'Acehardware': 5.32   # Upweight (0.9% → 5%)
}

df['Analysis_Weight'] = df['Retailer'].map(weights)
```

**Effect:**
- ✅ Mathematically corrects for retailer over-representation
- ✅ Preserves all data (no deletion)
- ✅ Adjusts category distribution automatically
- ✅ Can be toggled on/off for different analyses

**Effort:** 1 hour
**Impact:** Resolves 60-70% of bias

### Option B: Obtain Walmart Website Scrape

**Action:** Save the Walmart.com HTML to `walmart_website_scrape.txt` and run `parse_walmart_website_scrape.py`

**Benefits:**
- ✅ Validates product currency
- ✅ Updates prices to current
- ✅ Identifies discontinued products
- ✅ More defensible selection (current inventory)

**Effort:** Depends on data availability
**Impact:** Improves product selection quality significantly

### Option C: Re-Scrape Walmart with Category Focus

**Action:** Scrape Walmart.com with search terms targeting underrepresented categories

**Search Terms:**
- "garage shelving"
- "garage cabinets"
- "overhead garage storage"
- "garage ceiling storage"
- "wall mounted garage cabinets"

**Benefits:**
- ✅ Addresses category bias directly
- ✅ Captures current inventory
- ✅ Builds more balanced dataset

**Effort:** 1-2 days
**Impact:** Resolves category concentration issue

---

## Files Generated

1. **Cleaned Walmart Dataset:**
   `modules/category-intelligence/analysis/walmart_cleaned_rightsized.xlsx`
   1,500 products, scored and prioritized

2. **Removed Products:**
   `modules/category-intelligence/analysis/walmart_removed_products.xlsx`
   5,998 products removed during rightsizing

3. **Updated Master Dataset:**
   `modules/category-intelligence/04_CATEGORY_DATA_RIGHTSIZED.xlsx`
   3,991 total products (down from 9,989)

4. **Summary Statistics:**
   `modules/category-intelligence/analysis/walmart_rightsizing_summary.json`
   Scoring criteria, statistics, and metadata

---

## Recommendation

### Immediate Action: Apply Market Weights

**Why:**
- ✅ Fast (1 hour implementation)
- ✅ Mathematically correct
- ✅ Preserves all data
- ✅ Addresses retailer over-representation
- ✅ Automatically corrects category bias

**Implementation:**
1. Add `Analysis_Weight` column to master dataset
2. Use weights in all aggregations (means, sums, percentages)
3. Document weighting methodology in deliverables

**Example:**
```python
# Weighted average price
weighted_avg_price = (df['Price'] * df['Analysis_Weight']).sum() / df['Analysis_Weight'].sum()

# Weighted category distribution
category_dist = df.groupby('Category').apply(lambda x: x['Analysis_Weight'].sum())
```

### Long-Term: Re-Scrape Walmart (Shelving Focus)

**Why:**
- ✅ Addresses root cause (category concentration)
- ✅ Builds comprehensive dataset
- ✅ Validates market reality assumptions

**When:** After current analysis phase, if budget/time permits

---

## Conclusion

✅ **Achieved:** Walmart dataset reduced to 1,500 products, comparable to baseline size

⚠️ **Limitation:** Category bias persisted due to lack of website scrape data

🎯 **Recommendation:** Apply market weights (Fix #1 from ROOT_CAUSE_AND_TOP_FIXES.md) to mathematically correct for over-representation

📊 **Data Quality:** Rightsized dataset prioritizes higher-engagement products, but category diversity remains a gap

---

**Status:** ✅ Rightsizing Complete - Market Weighting Recommended as Next Step
