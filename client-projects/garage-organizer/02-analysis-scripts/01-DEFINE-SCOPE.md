# STEP 01: DEFINE SCOPE & PARAMETERS
## Garage Organizer Data Collection Pipeline

**Process:** Baseline definition
**Input:** None (manual definition)
**Output:** `scope_definition.json`
**Time:** 30 minutes
**Validation:** All parameters documented and reasonable

---

## PURPOSE

Define the search parameters, keywords, sample sizes, and data sources BEFORE any collection begins. This prevents scope creep and ensures reproducibility.

---

## INPUTS REQUIRED

None. This step is manual definition. You will create:
- Search keywords for each platform
- Sample size targets
- Date ranges
- Quality thresholds

---

## PROCEDURE

### 1. Define Reddit Search Parameters

**Keywords (use in PRAW search):**
```
garage organization
garage storage
garage shelving
organizing garage
wall storage
garage hooks
garage racks
DIY garage
garage setup
ceiling storage
```

**Subreddits to target:**
- r/DIY (home improvement projects)
- r/HomeImprovement (home renovation)
- r/organization (general organization)
- r/organizing (specific organizing)
- r/InteriorDesign (design-focused)

**Search strategy:**
- Search each keyword in each subreddit
- Limit to posts 2 years old or newer (2023-present)
- Minimum score: 5 upvotes (filters spam)
- Include all comments on qualifying posts

**Sample size target:**
- Total posts: 1,200-1,500
- Minimum quality: 95% have meaningful text (>20 characters)

### 2. Define YouTube Search Parameters

**Keywords:**
```
garage organization
garage storage
garage shelving
garage shelves DIY
garage organization system
garage setup
how to organize garage
garage storage ideas
garage tour
garage makeover
```

**Channel types to include:**
- DIY channels (5M+ subscribers)
- Product review channels
- Home improvement channels
- Individual creator channels

**Search strategy:**
- Video duration: 3 minutes to 30 minutes
- Upload date: 2021 or newer
- View count: >100 views (filters low-engagement)
- Closed caption status: Prefer videos with transcripts available

**Sample size target:**
- Total videos: 60-100
- Minimum quality: 90% have transcripts or auto-generated captions

### 3. Define Product Database Parameters

**Retailers to include:**
1. Walmart.com (target: 3,000-4,000 products)
2. Home Depot (target: 1,000-1,500)
3. Amazon (target: 1,000-1,500)
4. Lowe's (target: 800-1,000)
5. Target (target: 400-600)
6. Etsy (target: 200-400)

**Product categories:**
- Shelving units (all types)
- Wall-mounted storage
- Hooks and hangers
- Ceiling storage
- Cabinets and chests
- Organization systems

**Data to capture per product:**
- Product name
- Retailer
- Product URL
- Price
- Customer rating (if available)
- Review count (if available)
- Category/type
- Availability status

**Sample size target:**
- Total unique products: 7,000-10,000
- Target completeness: 90%+ have price data

### 4. Define Analysis Scope

**Pain point categories to code:**

| Category | Definition | Example Keywords |
|----------|-----------|-------------------|
| Installation Barrier | Difficulty, time, complexity, skill level | "hard to install", "took hours", "needed help" |
| Weight Failure | Collapse, weight limit, structural failure | "fell off wall", "couldn't hold", "too heavy" |
| Adhesive Failure | Tape/adhesive not holding, stickiness | "Command hooks fell", "adhesive failed", "came loose" |
| Rust/Durability | Rust, corrosion, material quality | "rusted quickly", "cheap metal", "durability" |
| Capacity Mismatch | Space, volume, usable area | "not enough space", "too small", "limited capacity" |
| Aesthetic Concern | Appearance, design, visibility | "ugly", "cheap looking", "doesn't match" |
| Cost Concern | Price, value, expensiveness | "expensive", "overpriced", "not worth it" |

**Behavioral categories to code:**

| Category | Definition | Example Keywords |
|----------|-----------|---|
| Frustration Trigger | Events that cause frustration | "angry", "frustrated", "annoyed" |
| Seasonal Driver | Seasonal motivation | "spring cleaning", "move", "season" |
| Life Change Trigger | Major life event | "new house", "baby", "downsizing" |
| Research Method | How consumers research | "YouTube", "Amazon reviews", "Reddit" |
| Purchase Influencer | What influences purchase decision | "reviews", "price", "brand", "recommendation" |
| Follow-on Purchase | Buying related products | "also bought", "came back for", "upgraded" |

**Sample size target for coding:**
- Total records to code: 1,500-2,000
- Inter-rater reliability threshold: ≥85% agreement
- Sample verification: Random spot-check 10% of coded records

---

## OUTPUT FILE: scope_definition.json

Create this file at: `/01-raw-data/scope_definition.json`

```json
{
  "pipeline_metadata": {
    "version": "1.0",
    "created_date": "2025-11-12",
    "created_by": "Your Name",
    "purpose": "Define scope parameters for garage organizer data collection"
  },
  "reddit": {
    "keywords": [
      "garage organization",
      "garage storage",
      "garage shelving",
      "organizing garage",
      "wall storage",
      "garage hooks",
      "garage racks",
      "DIY garage",
      "garage setup",
      "ceiling storage"
    ],
    "subreddits": [
      "r/DIY",
      "r/HomeImprovement",
      "r/organization",
      "r/organizing",
      "r/InteriorDesign"
    ],
    "date_range": {
      "start": "2023-01-01",
      "end": "2025-11-12"
    },
    "minimum_score": 5,
    "sample_size_target": {
      "posts": "1200-1500",
      "quality_threshold": "95% with text >20 chars"
    }
  },
  "youtube": {
    "keywords": [
      "garage organization",
      "garage storage",
      "garage shelving",
      "garage shelves DIY",
      "garage organization system",
      "garage setup",
      "how to organize garage",
      "garage storage ideas",
      "garage tour",
      "garage makeover"
    ],
    "date_range": {
      "start": "2021-01-01",
      "end": "2025-11-12"
    },
    "video_duration_seconds": {
      "min": 180,
      "max": 1800
    },
    "minimum_view_count": 100,
    "caption_preference": "transcripts_or_autogenerated",
    "sample_size_target": {
      "videos": "60-100",
      "quality_threshold": "90% with usable transcripts"
    }
  },
  "products": {
    "retailers": {
      "walmart": {
        "url": "walmart.com",
        "target_count": "3000-4000"
      },
      "home_depot": {
        "url": "homedepot.com",
        "target_count": "1000-1500"
      },
      "amazon": {
        "url": "amazon.com",
        "target_count": "1000-1500"
      },
      "lowes": {
        "url": "lowes.com",
        "target_count": "800-1000"
      },
      "target": {
        "url": "target.com",
        "target_count": "400-600"
      },
      "etsy": {
        "url": "etsy.com",
        "target_count": "200-400"
      }
    },
    "categories": [
      "Shelving units",
      "Wall-mounted storage",
      "Hooks and hangers",
      "Ceiling storage",
      "Cabinets and chests",
      "Organization systems"
    ],
    "data_per_product": [
      "product_name",
      "retailer",
      "product_url",
      "price",
      "customer_rating",
      "review_count",
      "category",
      "availability"
    ],
    "sample_size_target": {
      "total_products": "7000-10000",
      "completeness_threshold": "90% have price"
    }
  },
  "analysis": {
    "pain_point_categories": {
      "installation_barrier": "Difficulty, time, complexity",
      "weight_failure": "Collapse, weight limit, structural failure",
      "adhesive_failure": "Tape/adhesive not holding",
      "rust_durability": "Rust, corrosion, material quality",
      "capacity_mismatch": "Space, volume, usable area",
      "aesthetic_concern": "Appearance, design, visibility",
      "cost_concern": "Price, value, expensiveness"
    },
    "behavioral_categories": {
      "frustration_trigger": "Events that cause frustration",
      "seasonal_driver": "Seasonal motivation",
      "life_change_trigger": "Major life event",
      "research_method": "How consumers research",
      "purchase_influencer": "What influences purchase",
      "followon_purchase": "Buying related products"
    },
    "sample_size_target": {
      "records_to_code": "1500-2000",
      "inter_rater_reliability_threshold": "0.85",
      "verification_sample_percent": "10%"
    }
  },
  "quality_gates": {
    "reddit_completeness": "98%+ have URLs",
    "youtube_completeness": "90%+ have transcripts",
    "product_completeness": "90%+ have prices",
    "analysis_reliability": "85%+ inter-rater agreement"
  },
  "approval": {
    "status": "PENDING_REVIEW",
    "approved_by": null,
    "approved_date": null,
    "notes": "Review and adjust parameters before proceeding to Step 02"
  }
}
```

---

## VALIDATION CHECKLIST

Before proceeding to Step 02, verify:

- [ ] All keywords are relevant to garage organization
- [ ] Sample size targets are realistic (not 100k videos, not 10 products)
- [ ] Date ranges make sense (2+ years of data)
- [ ] Reddit subreddits are appropriate for topic
- [ ] All retailers in product list are operational
- [ ] Category definitions are clear and non-overlapping
- [ ] Inter-rater reliability threshold (85%) is documented
- [ ] Quality gates are measurable (not subjective)
- [ ] scope_definition.json is complete and valid JSON

---

## QUALITY RULES

| Rule | Type | Action |
|------|------|--------|
| All keywords must be garage/storage related | CRITICAL | Reject keywords outside scope |
| Sample sizes must be realistic | CRITICAL | Adjust if targets >50% of total market |
| Date ranges must be >6 months | CRITICAL | Reject if <6 months data available |
| Inter-rater threshold must be ≥80% | MEDIUM | Document justification if lower |
| Quality gates must be measurable | CRITICAL | Reject subjective metrics |

---

## COMMON MISTAKES TO AVOID

❌ **Mistake:** Too broad keywords like "storage" (will capture unrelated results)
✅ **Fix:** Use "garage storage", "garage organization", specific product names

❌ **Mistake:** No date range (will include obsolete data)
✅ **Fix:** Specify start/end dates for all sources

❌ **Mistake:** Sample size too small (no statistical validity)
✅ **Fix:** Aim for 1,500+ Reddit posts, 60+ videos, 8,000+ products

❌ **Mistake:** Forgetting about deduplication strategy
✅ **Fix:** Define how to handle cross-platform reposts and product duplicates

❌ **Mistake:** Missing inter-rater reliability documentation
✅ **Fix:** Document test sample size and methodology for reliability check

---

## NEXT STEP

Once scope_definition.json is complete and validated:
1. Review with stakeholder if needed
2. Update "approval" section with sign-off
3. Proceed to `02-EXTRACT-REDDIT.md`

---

**Status:** READY
**Last Updated:** November 12, 2025
