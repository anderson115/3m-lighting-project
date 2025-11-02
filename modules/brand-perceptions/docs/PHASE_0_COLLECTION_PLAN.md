# Phase 0: Data Collection Plan
**Project:** 3M Garage Organization Market Intelligence
**Date:** 2025-11-01
**Status:** IN PROGRESS

---

## Objective

Collect additional product reviews to achieve comprehensive brand coverage for strategic analysis:
- **Scotch mounting tape:** 400-500 reviews
- **3M Claw drywall hooks:** 300-400 reviews
- **Total target:** 700-900 new reviews
- **Final dataset:** ~3,600-3,800 total records

---

## Target Products

### Scotch Mounting Tape (5 products, ~100 reviews each)

1. **Scotch Extreme Mounting Tape - Mega Roll**
   - ASIN: B00FUEN2GK
   - Model: 414H-Long-DC
   - Target: 100 reviews

2. **Scotch Extreme Mounting Strips**
   - ASIN: B018GKCI82
   - Model: 414H-ST
   - Target: 100 reviews

3. **Scotch Extreme 2-Pack**
   - ASIN: B07N9HZQXN
   - Model: ET-414-2NA
   - Target: 100 reviews

4. **Scotch Extreme Mounting Tape (60in)**
   - ASIN: B005SRECEU
   - Model: 414P
   - Target: 100 reviews

5. **Scotch Indoor Mounting Tape**
   - ASIN: B0007P5G8Y
   - Model: 314H-MED
   - Target: 100 reviews

**Scotch Total Target:** 500 reviews

### 3M Claw Drywall Hooks (4 products, ~100 reviews each)

1. **3M Claw 15 lb (6-pack)**
   - ASIN: B087HQPH7Z
   - Target: 100 reviews

2. **3M Claw 25 lb**
   - ASIN: B08KCYFKCH
   - Target: 100 reviews

3. **3M Claw 65 lb (3-pack)**
   - ASIN: B08J49NCXM
   - Target: 100 reviews

4. **3M Claw Variety Pack (8-pack)**
   - ASIN: B0BLNGNM73
   - Target: 100 reviews

**3M Claw Total Target:** 400 reviews

---

## Collection Method

### Amazon Reviews
- **Tool:** Playwright + Chrome CDP (proven protocol)
- **Rate:** 2-5 minutes per product
- **Estimated time:** 45-90 minutes total
- **Output format:** JSON (structured)
- **Location:** `data/collected/amazon_reviews_raw/phase0/`

### YouTube/Reddit (Optional Enhancement)
- **Searches:**
  - "Scotch mounting tape garage"
  - "3M Claw garage hooks"
  - "Scotch vs Command garage"
- **Target:** +100-200 posts
- **Estimated time:** 30 minutes
- **Output:** `data/collected/phase0/`

---

## File Organization

```
data/collected/
├── amazon_reviews_raw/
│   └── phase0/
│       ├── scotch_B00FUEN2GK.json
│       ├── scotch_B018GKCI82.json
│       ├── scotch_B07N9HZQXN.json
│       ├── scotch_B005SRECEU.json
│       ├── scotch_B0007P5G8Y.json
│       ├── claw_B087HQPH7Z.json
│       ├── claw_B08KCYFKCH.json
│       ├── claw_B08J49NCXM.json
│       └── claw_B0BLNGNM73.json
├── youtube_raw/
│   └── phase0_youtube.json (if collected)
└── reddit_raw/
    └── phase0_reddit.json (if collected)
```

---

## Quality Targets

- **Verified purchases:** >90%
- **Field completeness:** >95%
- **No duplicates:** Validation required
- **Review text length:** Avg >50 chars

---

## Process Checklist

### Pre-Collection
- [x] Identify target products (9 products total)
- [x] Validate ASINs accessible
- [ ] Chrome remote debugging ready
- [ ] Output directories created
- [ ] Collection script prepared

### During Collection
- [ ] Monitor for CAPTCHA (solve manually if needed)
- [ ] Verify review counts match expectations
- [ ] Check file sizes increasing
- [ ] Log any errors/issues

### Post-Collection
- [ ] Validate JSON structure
- [ ] Check record counts (target: 700-900)
- [ ] Verify no duplicates with existing data
- [ ] Create product catalog entry
- [ ] Consolidate with existing dataset
- [ ] Update database
- [ ] Git commit with documentation

---

## Success Criteria

**Minimum:**
- 700 new reviews collected
- >90% verified purchases
- No critical data quality issues

**Target:**
- 900 new reviews collected
- >95% verified purchases
- Complete field coverage

**Stretch:**
- 1,000+ reviews
- +200 social media posts
- Product catalog complete

---

## Timeline

**Day 1 (Today):**
- [x] Product identification
- [ ] Collection script setup
- [ ] Amazon collection (Scotch products)
- [ ] Git checkpoint 1

**Day 2:**
- [ ] Amazon collection (3M Claw products)
- [ ] Social media collection (optional)
- [ ] Data validation
- [ ] Git checkpoint 2

**Day 3:**
- [ ] Consolidation
- [ ] Quality validation
- [ ] Database update
- [ ] **CHECKPOINT 1:** Dataset review

---

## Documentation for Scalability

### Reusable Components

1. **Product Research Process:**
   - Use WebSearch to find products: `[brand] [category] Amazon ASIN [use case] 2025`
   - Verify ASINs accessible on Amazon
   - Target products with 100+ reviews
   - Document ASINs in collection plan

2. **Collection Script Template:**
   - Proven: `/tmp/collect_command_products_bulk.py`
   - Input: List of ASINs + product names + targets
   - Output: Structured JSON per product
   - Location: `data/collected/amazon_reviews_raw/[phase]/`

3. **Quality Validation:**
   - Run preflight validation after collection
   - Check: verified %, field completeness, duplicates
   - Document issues in collection report

4. **Consolidation Process:**
   - Merge new data with existing
   - Update product catalog
   - Refresh database
   - Git commit with summary

### Template for Other Clients

```markdown
# Phase 0: Data Collection Plan
**Client:** [Client Name]
**Category:** [Product Category]
**Target Brands:** [Brand 1], [Brand 2], [Brand 3]

## Target Products
[Use WebSearch to identify products]
[Document ASINs, models, targets]

## Collection Method
[Use proven Amazon scraping protocol]
[Optional: YouTube/Reddit enhancement]

## File Organization
[Follow standard structure]

## Process Checklist
[Standard checklist applicable to all projects]
```

---

**Created:** 2025-11-01T20:55:00
**Next Step:** Set up collection script and begin Amazon collection
