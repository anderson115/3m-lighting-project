# Phase 2: Data Collection Plan - Brand Perceptions Module

**Date:** 2025-10-30
**Status:** IN DEVELOPMENT
**Budget:** $0-25 maximum
**Strategy:** Free-first with strategic Bright Data backfill

---

## 🎯 Three-Pass Strategy

### **PASS 1: FREE TOOLS ONLY** (Current Phase)
Collect as much data as possible with 100% free tools, assess coverage gaps

### **PASS 2: ASSESSMENT**
Evaluate what we captured, identify critical gaps that require paid services

### **PASS 3: BACKFILL**
Use Bright Data ($0-25 budget) to fill only the critical gaps identified in Pass 2

---

## Pass 1: Free Data Collection Architecture

### Design Principles
1. **Simple & Stable:** Use battle-tested tools, avoid experimental projects
2. **Checkpoint-Driven:** Verify data quality at every step with small samples
3. **Right-Sized:** No over-engineering, but production-ready
4. **Scalable:** Start with 1 brand sample, then scale to 5 brands

### Tool Selection (Free Only)

```
┌─────────────────────────────────────────────────────────┐
│ PASS 1: FREE DATA COLLECTION                            │
├─────────────────────────────────────────────────────────┤
│ AMAZON REVIEWS                                           │
│ • Tool: PRAW-style approach (Reddit API) NOT AVAILABLE   │
│ • REVISED: Start with WebFetch manual collection        │
│ • Checkpoint: Verify 10 reviews from 1 product          │
│ • Scale: If stable, collect 25% sample (5 brands)       │
├─────────────────────────────────────────────────────────┤
│ YOUTUBE VIDEOS                                           │
│ • Tool: YouTube Data API v3 (official, 10k units/day)   │
│ • Tool: youtube-transcript-api (transcripts)            │
│ • Checkpoint: Verify 5 videos with transcripts          │
│ • Scale: 50-100 videos per brand                        │
├─────────────────────────────────────────────────────────┤
│ REDDIT DISCUSSIONS                                       │
│ • Tool: PRAW (Python Reddit API Wrapper - official)     │
│ • Checkpoint: Verify 10 posts/comments                  │
│ • Scale: 200-400 posts per brand                        │
├─────────────────────────────────────────────────────────┤
│ TWITTER/X POSTS                                          │
│ • Tool: Snscrape (most stable free option 2025)         │
│ • Checkpoint: Verify 10 tweets                          │
│ • Scale: 500-1000 tweets per brand                      │
├─────────────────────────────────────────────────────────┤
│ TIKTOK VIDEOS                                            │
│ • Tool: davidteather/TikTok-Api                         │
│ • Checkpoint: Verify 5 videos with metadata            │
│ • Scale: 100-200 videos per brand                       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ DEFERRED TO PASS 3 (BRIGHT DATA BACKFILL IF NEEDED)     │
├─────────────────────────────────────────────────────────┤
│ • Amazon reviews (if WebFetch insufficient)             │
│ • Home Depot reviews                                     │
│ • Lowes reviews                                          │
│ • Walmart reviews                                        │
│ • Menards reviews                                        │
│ • Ace Hardware reviews                                   │
└─────────────────────────────────────────────────────────┘
```

---

## Implementation Plan

### Stage 1: Setup & Preflight (30 minutes)
- [ ] Install free tool dependencies
- [ ] Configure API credentials (YouTube, Reddit)
- [ ] Create test scripts for each source
- [ ] Run preflight checks on small sample (1 brand, 10 data points each)
- [ ] Git push after preflight passes

### Stage 2: Checkpoint 1 - Single Brand Sample (1 hour)
**Brand:** Command (highest priority)
**Sample Size:** 10 data points per source

**Tasks:**
- [ ] Collect 10 Reddit posts about Command hooks
- [ ] Collect 5 YouTube videos about Command hooks
- [ ] Collect 10 Twitter/X posts about Command hooks
- [ ] Collect 5 TikTok videos about Command hooks
- [ ] Manual WebFetch: 10 Amazon reviews for Command product

**Data Quality Checks:**
- [ ] Verify no blank/null fields in critical columns (text, date, author)
- [ ] Verify US geography (where identifiable)
- [ ] Verify date range (24 months target)
- [ ] Verify data structure consistency

**STOP POINT:** Review sample data with user before proceeding

### Stage 3: Checkpoint 2 - Multi-Brand Small Sample (2 hours)
**Brands:** Command, Scotch-Brite (2 brands)
**Sample Size:** 25 data points per source per brand

**Tasks:**
- [ ] Scale Reddit collection: 25 posts × 2 brands = 50 posts
- [ ] Scale YouTube collection: 10 videos × 2 brands = 20 videos
- [ ] Scale Twitter/X collection: 25 posts × 2 brands = 50 posts
- [ ] Scale TikTok collection: 10 videos × 2 brands = 20 videos

**Data Quality Checks:**
- [ ] Check for duplicate data across brands
- [ ] Verify temporal distribution (not all from same month)
- [ ] Verify brand mentions are accurate (not false positives)
- [ ] Check data volume consistency across brands

**STOP POINT:** Review multi-brand sample, assess stability

### Stage 4: Checkpoint 3 - Full Free Data Collection (4-6 hours)
**Brands:** All 5 (Command, Scotch-Brite, Scotch, Post-it, Scotchgard)
**Sample Size:** 25% sampling target

**Tasks:**
- [ ] Reddit: 100 posts × 5 brands = 500 posts
- [ ] YouTube: 25 videos × 5 brands = 125 videos
- [ ] Twitter/X: 200 posts × 5 brands = 1,000 posts
- [ ] TikTok: 40 videos × 5 brands = 200 videos

**Data Quality Checks:**
- [ ] Verify total record counts match expectations
- [ ] Check for data collection failures/errors
- [ ] Verify US-only filtering (post-process if needed)
- [ ] Verify 24-month temporal filtering

**STOP POINT:** Assess coverage gaps, calculate Pass 2 metrics

---

## Pass 2: Gap Assessment

### Metrics to Calculate
1. **Coverage by Source:**
   - Reddit: X posts collected (target: 500)
   - YouTube: X videos collected (target: 125)
   - Twitter/X: X posts collected (target: 1,000)
   - TikTok: X videos collected (target: 200)
   - Retailer reviews: 0 (target: ~2,000+)

2. **Coverage by Brand:**
   - Command: X% complete
   - Scotch-Brite: X% complete
   - Scotch: X% complete
   - Post-it: X% complete
   - Scotchgard: X% complete

3. **Critical Gaps:**
   - Retailer reviews (Amazon, Home Depot, Lowes, Walmart, Menards, Ace)
   - Any source with <50% target coverage

4. **Cost Estimate for Backfill:**
   - Bright Data requests needed: X
   - Estimated cost: $X (must be ≤$25)

---

## Pass 3: Strategic Backfill (Bright Data)

### Budget Allocation ($25 maximum)
**Bright Data Pricing:** 5,000 free requests/month, then ~$0.0009/record

**Strategy:** Use free 5,000 requests first, then paid if needed

### Prioritization (if budget tight):
1. **Tier 1 (Highest Priority):** Amazon reviews
2. **Tier 2 (High Priority):** Home Depot, Lowes reviews
3. **Tier 3 (Medium Priority):** Walmart reviews
4. **Tier 4 (Lower Priority):** Menards, Ace Hardware reviews

### Backfill Plan (TBD after Pass 2 assessment)
- [ ] Bright Data MCP setup
- [ ] Checkpoint: Test 10 retailer reviews
- [ ] Scale: Collect based on priority tiers within budget
- [ ] Final data quality check

---

## Data Quality Checkpoints (Throughout All Passes)

### Checkpoint Script Requirements
```python
# Each checkpoint must verify:
1. Record count matches expectation
2. No critical null/blank fields:
   - text/content (review text, tweet text, etc.)
   - date/timestamp
   - source identifier
3. US geography filtering (where applicable)
4. 24-month temporal filtering
5. Brand mention accuracy (no false positives)
6. Data structure consistency (same schema)
7. No duplicate records
```

### Red Flags to Watch For
- ❌ Entire columns blank (schema mismatch)
- ❌ All dates from same day (scraper hitting cache)
- ❌ Duplicate records with identical IDs
- ❌ Brand name not found in text (false positive)
- ❌ Non-US geography detected (UK, Australia, etc.)
- ❌ Data older than 24 months
- ❌ API rate limit errors (need to throttle)

---

## Git Workflow

### Commit Checkpoints
1. **After Preflight:** "feat: Pass 1 data collection infrastructure with preflight tests"
2. **After Checkpoint 1:** "feat: Single brand sample collection (Command, 10 per source)"
3. **After Checkpoint 2:** "feat: Multi-brand sample collection (2 brands, 25 per source)"
4. **After Checkpoint 3:** "feat: Full free data collection (5 brands, Pass 1 complete)"
5. **After Pass 2:** "docs: Gap assessment and Bright Data backfill plan"
6. **After Pass 3:** "feat: Strategic backfill complete, final data quality verified"

### Branch Strategy
- Main branch: `main`
- Development: Create `phase2-data-collection` branch
- Merge to main only after each checkpoint passes

---

## File Structure

```
modules/brand-perceptions/
├── scripts/
│   ├── collect_reddit.py          # PRAW Reddit scraper
│   ├── collect_youtube.py         # YouTube API + transcripts
│   ├── collect_twitter.py         # Snscrape Twitter scraper
│   ├── collect_tiktok.py          # TikTok API scraper
│   ├── checkpoint_validator.py    # Data quality checks
│   └── backfill_brightdata.py     # Bright Data MCP integration
├── data/
│   ├── raw/
│   │   ├── pass1_free/            # Free data collection
│   │   │   ├── reddit/
│   │   │   ├── youtube/
│   │   │   ├── twitter/
│   │   │   └── tiktok/
│   │   └── pass3_backfill/        # Bright Data backfill
│   │       ├── amazon/
│   │       ├── homedepot/
│   │       └── lowes/
│   └── processed/
│       └── consolidated/          # Merged, cleaned data
├── config/
│   ├── data_sources.yaml          # Source configuration
│   └── checkpoint_rules.yaml      # Validation rules
└── logs/
    ├── preflight_YYYYMMDD.log
    ├── checkpoint1_YYYYMMDD.log
    └── checkpoint2_YYYYMMDD.log
```

---

## Success Criteria

### Pass 1 Success
- ✅ 500+ Reddit posts collected (5 brands)
- ✅ 125+ YouTube videos collected
- ✅ 1,000+ Twitter/X posts collected
- ✅ 200+ TikTok videos collected
- ✅ All checkpoints pass data quality validation
- ✅ Zero stability issues (no crashes, hangs, or data corruption)
- ✅ US-only and 24-month filters applied

### Pass 2 Success
- ✅ Gap assessment complete with metrics
- ✅ Backfill cost estimate ≤$25
- ✅ Prioritization plan for Bright Data usage

### Pass 3 Success
- ✅ Retailer review data backfilled within budget
- ✅ Total data cost ≤$25
- ✅ Final data quality validation passes
- ✅ 50+ verbatim quotes per brand minimum achieved

---

## Next Steps

1. **User approval of this plan**
2. **Begin Stage 1: Setup & Preflight**
3. **Checkpoint 1: Single brand sample**
4. **Stop and report back for evaluation**

---

## Notes

- **Stability > Speed:** Will use conservative API rate limits to avoid bans
- **Small samples first:** Never scale until checkpoint passes
- **User in the loop:** Stop at every checkpoint for evaluation
- **Cost tracking:** Monitor Bright Data usage in real-time to stay under $25
- **Rollback ready:** Git commits at each checkpoint allow rollback if issues found
