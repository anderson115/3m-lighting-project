# Phase 2: Data Collection Plan - Brand Perceptions Module

**Date:** 2025-10-30
**Status:** LOCKED IN - Ready for Execution
**Budget:** $0-25 maximum
**Strategy:** Bias-mitigated free data collection with strategic Bright Data backfill

---

## 🎯 Critical Update: Bias Mitigation Strategy

### Key Changes from Original Plan:
1. **Negativity Bias Mitigation:** Balanced query strategy (positive + neutral + negative searches)
2. **Temporal Bias Fix:** 2023-2024 data prioritized 3x, older data tagged separately
3. **Platform Bias Fix:** YouTube success demos, TikTok tutorials, Reddit recommendations added
4. **Geographic Bias Fix:** US sources prioritized, international sources tagged separately
5. **Sample Size Fix:** 200+ verbatims per brand target (up from 50+)
6. **Tool Simplification:** WebSearch/WebFetch primary (proven in preflight), avoid over-engineering APIs

---

## Three-Pass Strategy

### **PASS 1: FREE TOOLS - BIAS-MITIGATED COLLECTION**
Collect balanced data (positive + negative + neutral) with 100% free tools

### **PASS 2: BIAS ASSESSMENT**
Evaluate sentiment distribution, geographic coverage, temporal coverage, platform diversity

### **PASS 3: STRATEGIC BACKFILL**
Use Bright Data ($0-25 budget) to fill critical gaps only

---

## Pass 1: Bias-Mitigated Data Collection

### Design Principles
1. **Simple & Stable:** WebSearch/WebFetch proven in preflight, use what works
2. **Balanced Queries:** For every negative search, run 1 positive + 1 neutral search
3. **Temporal Filtering:** 2023-2024 priority (weighted 3x), 2020-2022 secondary, pre-2020 reference only
4. **Geographic Tagging:** Tag all sources by region, US sources prioritized
5. **Checkpoint-Driven:** Validate bias mitigation at each stage

---

## Data Collection Sources & Query Strategy

### **SOURCE 1: YouTube (Success Case Balance)**
**Purpose:** Overcome negativity bias with successful demonstration videos
**Tool:** WebSearch to find videos, manual extraction of key quotes/timestamps
**Target:** 50 videos per brand (10 in Stage 1, 25 in Stage 2, 50 in Stage 3)

**Query Strategy (per brand):**
```
Positive: "[Brand] garage organization tutorial" OR "[Brand] garage hooks works great"
Neutral:  "[Brand] garage storage review" OR "[Brand] garage organization 2024"
Negative: "[Brand] garage hooks failed" OR "[Brand] garage storage complaints"
```

**Data to Extract:**
- Video URL, title, channel name, date posted
- Transcript quotes showing success/failure
- Use case demonstrated (e.g., "holding garden tools")
- Weight/load shown in video
- Geographic indicators (accent, retailer mentions)

---

### **SOURCE 2: TikTok (Influencer Recommendations)**
**Purpose:** Capture DIY/organization influencer opinions
**Tool:** WebSearch "site:tiktok.com [brand] garage" + manual extraction
**Target:** 50 videos per brand

**Query Strategy:**
```
Positive: "site:tiktok.com [Brand] garage organization hack"
Neutral:  "site:tiktok.com #garageorganization [Brand]"
Negative: "site:tiktok.com [Brand] garage fail OR disaster"
```

**Data to Extract:**
- TikTok URL, creator handle, date posted
- Caption text and hashtags
- Key quote from video (transcribe if necessary)
- Engagement metrics (likes, comments if visible)

---

### **SOURCE 3: Reddit (Community Discussions)**
**Purpose:** Authentic consumer conversations with context
**Tool:** WebSearch "site:reddit.com [brand] garage" + manual extraction
**Target:** 100 posts/comments per brand

**Subreddits Priority:**
- r/HomeImprovement (neutral-positive lean)
- r/organization (positive lean)
- r/garageporn (enthusiast community)
- r/DIY (mixed)
- General search (mixed)

**Query Strategy:**
```
Positive: "site:reddit.com [Brand] garage recommend OR love OR works"
Neutral:  "site:reddit.com r/HomeImprovement [Brand] garage"
Negative: "site:reddit.com [Brand] garage fail OR disappointed OR fell"
```

**Data to Extract:**
- Reddit URL, username (if not deleted), subreddit, date
- Post title + body text OR comment text
- Upvotes/downvotes if visible
- Context (reply chain if relevant)

---

### **SOURCE 4: Retailer Reviews (Amazon, Home Depot, Lowes)**
**Purpose:** High-volume consumer feedback with verification
**Tool:** WebSearch to find product pages, manual extraction OR Bright Data (Pass 3)
**Target:** 100 reviews per brand

**Query Strategy:**
```
Positive: "site:amazon.com [Brand] garage hooks 5 stars OR 4 stars"
Neutral:  "site:amazon.com [Brand] garage utility hooks reviews"
Negative: "site:amazon.com [Brand] garage hooks 1 star OR 2 stars"
```

**Retailers Priority:**
1. Amazon.com (US site only)
2. HomeDepot.com
3. Lowes.com
4. (Walmart, Target, Ace if time permits)

**Data to Extract:**
- Product name, URL, retailer
- Review text, star rating, reviewer name, date
- Verified purchase indicator (if visible)
- Helpful votes (if visible)

---

### **SOURCE 5: Expert Reviews & Blogs**
**Purpose:** Professional assessments and testing
**Tool:** WebSearch for expert review sites
**Target:** 20 articles per brand

**Query Strategy:**
```
"[Brand] garage hooks review expert OR professional 2024 OR 2023"
"[Brand] garage organization blog review"
"best garage hooks [Brand] vs alternatives"
```

**Data to Extract:**
- Article URL, publication name, author, date
- Expert rating/score (if provided)
- Key quotes about performance
- Testing methodology (if described)

---

## Stage 1: Setup & Preflight (1 hour)

### Objectives:
- Validate WebSearch/WebFetch approach with balanced queries
- Confirm bias mitigation strategy works
- Test data extraction workflow

### Tasks:
- [ ] Create `config/query_templates.yaml` with balanced query sets
- [ ] Create `scripts/websearch_collector.py` for systematic collection
- [ ] Update `scripts/checkpoint_validator.py` with bias checks:
  - Sentiment distribution (target: 40-60% negative, not 90%+)
  - Temporal distribution (target: 70%+ from 2023-2024)
  - Geographic distribution (target: 80%+ US sources)
  - Platform diversity (target: 5+ platform types)
- [ ] **Preflight Test:** Collect 10 data points per source for Command brand
  - 10 YouTube videos (5 positive queries, 5 negative queries)
  - 10 Reddit posts (balanced queries)
  - 10 retailer reviews (balanced star ratings)
- [ ] Run checkpoint validator on preflight sample
- [ ] **VALIDATION GATE:** Preflight must show <80% negative sentiment (if >80%, rebalance queries)

---

## Stage 2: Checkpoint 1 - Command Brand Sample (3 hours)

### Objectives:
- Collect 100 balanced data points for Command brand
- Validate bias mitigation is working at scale
- Demonstrate full workflow before scaling to more brands

### Collection Targets (Command brand only):
- [ ] **YouTube:** 25 videos
  - 10 positive query results ("Command garage organization tutorial")
  - 10 neutral query results ("Command garage storage review")
  - 5 negative query results ("Command garage hooks failed")
- [ ] **TikTok:** 25 videos (balanced queries)
- [ ] **Reddit:** 25 posts/comments (balanced subreddits + queries)
- [ ] **Amazon Reviews:** 25 reviews
  - 10 from 4-5 star reviews
  - 10 from 3 star reviews (neutral)
  - 5 from 1-2 star reviews
- [ ] **Expert Reviews:** 5 articles

**Total Stage 2:** 105 data points for Command

### Data Quality Checks:
- [ ] Sentiment distribution: 30-60% negative (not 90%+)
- [ ] Temporal distribution: 70%+ from 2023-2024
- [ ] Geographic tagging: All sources tagged by region
- [ ] US prioritization: 80%+ US sources
- [ ] Brand mention accuracy: 100% verified
- [ ] No duplicate records

### Validation Script:
```python
python3 modules/brand-perceptions/scripts/checkpoint_validator.py \
  --checkpoint=stage2 \
  --brand=Command \
  --min-records=100 \
  --max-negative-sentiment=0.60 \
  --min-recent-data=0.70 \
  --min-us-sources=0.80
```

**STOP POINT:** Review Command sample with user, validate bias mitigation working

---

## Stage 3: Checkpoint 2 - Multi-Brand Expansion (6 hours)

### Objectives:
- Expand to 2 additional brands (Command + Scotch-Brite + Scotch)
- Validate workflow stability across brands
- Build toward 200+ verbatims per brand

### Collection Targets (3 brands × 100 data points = 300 total):
- [ ] **YouTube:** 25 videos per brand × 3 = 75 videos
- [ ] **TikTok:** 25 videos per brand × 3 = 75 videos
- [ ] **Reddit:** 25 posts per brand × 3 = 75 posts
- [ ] **Retailer Reviews:** 25 reviews per brand × 3 = 75 reviews
- [ ] **Expert Reviews:** 5 articles per brand × 3 = 15 articles

**Total Stage 3:** 315 data points across 3 brands

### Data Quality Checks:
- [ ] Cross-brand consistency (similar sentiment distributions)
- [ ] No brand name confusion (e.g., "Scotch" vs "Scotch-Brite")
- [ ] Platform diversity maintained
- [ ] Temporal distribution consistent
- [ ] Geographic tagging complete

### Validation Script:
```python
python3 modules/brand-perceptions/scripts/checkpoint_validator.py \
  --checkpoint=stage3 \
  --brands=Command,Scotch-Brite,Scotch \
  --min-records-per-brand=100 \
  --max-negative-sentiment=0.60 \
  --min-recent-data=0.70
```

**STOP POINT:** Review 3-brand sample, assess if ready to scale to 5 brands OR move to Pass 2 assessment

---

## Pass 2: Bias Assessment & Gap Analysis

### Metrics to Calculate:

#### 1. **Sentiment Distribution Check**
**Target:** 30-60% negative, 20-40% neutral, 20-40% positive
**Current:** Calculate from collected data
**Action:** If >70% negative, add more positive query results in Pass 3

#### 2. **Temporal Coverage Check**
**Target:** 70%+ from 2023-2024
**Current:** Calculate date distribution
**Action:** If <70% recent, prioritize recent content in Pass 3

#### 3. **Geographic Coverage Check**
**Target:** 80%+ US sources
**Current:** Count by geography tag
**Action:** If <80% US, filter out non-US in Pass 3

#### 4. **Platform Diversity Check**
**Target:** 5+ platform types
**Current:** Count unique platforms
**Action:** If missing key platforms (YouTube, TikTok, Reddit, retailer reviews), add in Pass 3

#### 5. **Sample Size Check**
**Target:** 200+ verbatims per brand
**Current:** Count by brand
**Gap:** Calculate remaining needed per brand

#### 6. **Source Quality Check**
**Target:** 20+ unique sources per brand
**Current:** Count distinct URLs/sources
**Action:** If <20, diversify sources in Pass 3

---

## Pass 3: Strategic Backfill (Bright Data)

### Use Cases for Bright Data ($0-25 budget):
1. **Retailer review scale-up** (if manual collection too slow)
2. **Fill geographic gaps** (if too much non-US data)
3. **Recent data boost** (if temporal coverage <70% recent)
4. **Platform gaps** (if missing YouTube/TikTok API access)

### Bright Data Setup:
- [ ] Configure gdrive MCP for Bright Data if available
- [ ] Test 10-record sample from Amazon
- [ ] Validate data quality matches manual collection
- [ ] Scale within $25 budget

### Budget Allocation:
- **Free tier:** 5,000 requests/month (use first)
- **Paid tier:** ~$0.0009/record if needed
- **Max spend:** $25

---

## Data Quality Validation Requirements

### Checkpoint Validator Checks (All Stages):

```yaml
# config/checkpoint_rules.yaml
validation_rules:
  sentiment_distribution:
    max_negative_percentage: 0.60  # Prevent negativity bias
    min_neutral_percentage: 0.15
    min_positive_percentage: 0.15

  temporal_distribution:
    priority_window: "2023-2024"
    min_priority_percentage: 0.70  # 70%+ recent
    acceptable_window: "2020-2024"
    max_old_data_percentage: 0.10  # <10% pre-2020

  geographic_distribution:
    priority_region: "US"
    min_priority_percentage: 0.80  # 80%+ US
    allowed_regions: ["US", "CA"]  # US + Canada acceptable
    excluded_regions: ["UK", "AU"]  # Tag separately, don't mix

  platform_diversity:
    min_unique_platforms: 5
    required_platforms:
      - "YouTube"
      - "Reddit"
      - "Amazon" or "Home Depot" or "Lowes"

  sample_size:
    min_records_per_brand_stage2: 100
    min_records_per_brand_stage3: 200
    min_unique_sources_per_brand: 20

  data_quality:
    required_fields: ["text", "date", "source_url", "brand"]
    no_duplicates: true
    brand_mention_verified: true
```

---

## File Structure (Updated)

```
modules/brand-perceptions/
├── scripts/
│   ├── websearch_collector.py       # Balanced query collection
│   ├── checkpoint_validator.py      # Bias validation checks
│   └── bias_assessment.py           # Pass 2 analysis script
├── data/
│   ├── raw/
│   │   ├── pass1_free/
│   │   │   ├── youtube/             # YouTube videos
│   │   │   ├── tiktok/              # TikTok videos
│   │   │   ├── reddit/              # Reddit posts
│   │   │   ├── amazon/              # Amazon reviews
│   │   │   ├── homedepot/           # Home Depot reviews
│   │   │   └── expert_reviews/      # Blog articles
│   │   └── pass3_backfill/          # Bright Data backfill
│   └── processed/
│       ├── command/                  # Per-brand processed data
│       ├── scotch-brite/
│       └── consolidated/             # Cross-brand analysis
├── config/
│   ├── query_templates.yaml         # Balanced query sets
│   ├── checkpoint_rules.yaml        # Validation rules (LOCKED IN)
│   └── brands.yaml                  # Brand list
└── logs/
    ├── preflight_20251030.log
    ├── stage2_checkpoint.log
    └── stage3_checkpoint.log
```

---

## Success Criteria (Updated with Bias Mitigation)

### Stage 1 (Preflight) Success:
- ✅ 30 balanced data points collected (Command)
- ✅ Sentiment distribution: <80% negative
- ✅ WebSearch/WebFetch workflow validated
- ✅ Checkpoint validator script working

### Stage 2 (Command Sample) Success:
- ✅ 100+ data points collected (Command)
- ✅ Sentiment distribution: 30-60% negative (not 90%+)
- ✅ Temporal coverage: 70%+ from 2023-2024
- ✅ Geographic coverage: 80%+ US sources
- ✅ Platform diversity: 5+ platforms
- ✅ 20+ unique sources

### Stage 3 (Multi-Brand) Success:
- ✅ 300+ data points collected (3 brands)
- ✅ 100+ data points per brand
- ✅ Bias mitigation validated across brands
- ✅ Ready to scale to 5 brands OR move to Pass 2

### Pass 2 (Assessment) Success:
- ✅ Bias assessment complete with metrics
- ✅ Gap analysis showing what's missing
- ✅ Backfill plan ≤$25 budget

### Pass 3 (Backfill) Success:
- ✅ All gaps filled within budget
- ✅ 200+ verbatims per brand achieved
- ✅ Final bias validation passes
- ✅ Total cost ≤$25

---

## Git Workflow

### Commit Strategy:
1. **After Preflight:** `feat: Bias-mitigated data collection infrastructure with preflight validation`
2. **After Stage 2:** `feat: Command brand sample with balanced sentiment (100 data points)`
3. **After Stage 3:** `feat: Multi-brand expansion with bias validation (3 brands, 300 data points)`
4. **After Pass 2:** `docs: Bias assessment and strategic backfill plan`
5. **After Pass 3:** `feat: Final data collection complete with bias mitigation verified`

---

## Next Steps

1. ✅ **Plan locked in** (this document)
2. ⏳ Clean up obsolete files
3. ⏳ Update DEVELOPMENT_PLAN.md
4. ⏳ Create config/checkpoint_rules.yaml
5. ⏳ Run Stage 1 Preflight

---

## Notes

- **Bias mitigation is priority #1** - Quality over speed
- **Stop at every checkpoint** - User validates before proceeding
- **Simple tools work** - WebSearch/WebFetch proven, don't over-engineer
- **Balanced queries required** - For every negative search, run positive + neutral
- **Geographic tagging required** - All sources must be tagged by region
- **Temporal weighting required** - 2023-2024 data weighted 3x higher
