# RELEVANCY STANDARDS & QUALITY GATES
## Garage Organizer Category Intelligence Pipeline

**Created:** November 12, 2025
**Authority:** Non-negotiable data quality requirement
**Enforcement:** Every dataset must pass before proceeding

---

## RELEVANCY DEFINITION

**Data is RELEVANT if it:**

1. **Directly addresses garage organization category**
   - NOT: Commercial storage, automotive repair, industrial warehouse
   - YES: Home garage shelving, residential storage, garage organization products

2. **Represents authentic consumer experience**
   - NOT: Brand promotional content, paid reviews, bot-generated posts
   - YES: Genuine problem-solving, personal experience, honest feedback

3. **Provides actionable insights**
   - NOT: Generic comments ("storage is hard")
   - YES: Specific problems ("shelves collapsed under weight")

4. **Comes from valid source**
   - NOT: Spam, deleted users, bots
   - YES: Real person, real account, real experience

---

## RELEVANCY SCORING RUBRIC

### Score 2: Highly Relevant ✅
- Directly about garage organization products/services
- Clear, specific consumer pain point or behavior
- Actionable insight for product development
- From authenticated consumer with history
- Example: "Command hooks fell off after 3 months in cold garage"

**Action:** KEEP, use in analysis

### Score 1: Marginally Relevant ⚠️
- Related to garage/storage but not directly about organization
- Generic mention without specifics
- Tangentially useful for context
- Potentially authentic but unclear
- Example: "My garage is a mess"

**Action:** KEEP for context, note quality concern, don't quote directly

### Score 0: Not Relevant ❌
- Off-topic or spam
- Promotional content
- From bot/deleted user
- Contradicts scope definition
- Example: "Check out my commercial warehouse storage solution"

**Action:** REMOVE, log removal reason

---

## DATASET-SPECIFIC RELEVANCY CRITERIA

### REDDIT POSTS

**Relevancy Checkpoints:**

1. **Subreddit Appropriateness**
   - r/DIY: Should mention home/garage projects
   - r/HomeImprovement: Should include home context
   - r/organization: Should be about residential organizing
   - ❌ REMOVE: Posts about commercial/industrial only

2. **Content Specificity**
   - ✅ KEEP: "I tried [Product X], here's what happened"
   - ✅ KEEP: "Installing [type] shelves, struggling with [problem]"
   - ❌ REMOVE: "Storage is important" (too generic)
   - ❌ REMOVE: Product spam links with no commentary

3. **Author Verification**
   - ✅ KEEP: Account with post history, credible context
   - ⚠️ FLAG: New account (but keep if content relevant)
   - ❌ REMOVE: Deleted user, obvious bot accounts

4. **Temporal Appropriateness**
   - ✅ KEEP: Posted in 2023-2025 (recent consumer sentiment)
   - ⚠️ FLAG: Posted 2021-2023 (slightly dated, keep with note)
   - ❌ REMOVE: Posted before 2021 (consumer needs changed)

### YOUTUBE VIDEOS

**Relevancy Checkpoints:**

1. **Video Type**
   - ✅ KEEP: DIY garage organization, product reviews, installation guides
   - ✅ KEEP: Before/after garage transformations with commentary
   - ⚠️ FLAG: General garage content (keep if relevant segment exists)
   - ❌ REMOVE: Commercial storage, automotive repair, unrelated content

2. **Channel Authenticity**
   - ✅ KEEP: Individual creators, legitimate review channels
   - ✅ KEEP: DIY/home improvement channels with subscriber base
   - ⚠️ FLAG: Brand-owned channels (potential bias, keep with note)
   - ❌ REMOVE: Obvious spam channels, dead channels (no views)

3. **Transcript Quality**
   - ✅ KEEP: Manual captions or high-quality auto-generated
   - ⚠️ FLAG: Poor auto-generated (keep if content clear)
   - ❌ REMOVE: No transcript available

4. **Content Focus**
   - ✅ KEEP: Discusses pain points, features, durability, installation
   - ✅ KEEP: Consumer problems with products
   - ⚠️ FLAG: Primarily sales-focused (keep with bias note)
   - ❌ REMOVE: No garage/storage discussion

### PRODUCTS

**Relevancy Checkpoints:**

1. **Category Accuracy**
   - ✅ KEEP: Shelving, wall storage, hooks, ceiling racks, organization
   - ⚠️ FLAG: Multipurpose furniture (keep if garage-appropriate)
   - ❌ REMOVE: Automotive parts, commercial-only, unrelated categories

2. **Retailer Appropriateness**
   - ✅ KEEP: Consumer-focused retailers (Walmart, HD, Amazon, Target)
   - ⚠️ FLAG: Etsy (artisan/niche, keep with sourcing note)
   - ❌ REMOVE: B2B/industrial-only retailers

3. **Product Description**
   - ✅ KEEP: Clear garage organization purpose
   - ⚠️ FLAG: Generic description but category appropriate
   - ❌ REMOVE: Misleading category, irrelevant product

4. **Current Availability**
   - ✅ KEEP: In stock or recently discontinued
   - ⚠️ FLAG: Discontinued 1+ years ago (keep for market history)
   - ❌ REMOVE: Product URL is dead/inaccessible

---

## RELEVANCY VALIDATION PROCEDURE

### Phase 1: Automated Filtering (During Collection)

```python
def automated_relevancy_filter(record, source_type):
    """
    Apply automated rules DURING collection.
    These are hard filters, not subject to reviewer opinion.
    """

    if source_type == "reddit":
        # AUTOMATIC REJECTION (hard filters)
        if record['author'] == '[deleted]':
            return REJECT("Deleted user")
        if record['score'] < 5:
            return REJECT("Below minimum score")
        if len(record['text']) < 20:
            return REJECT("Text too short")
        if not is_valid_url(record['url']):
            return REJECT("Invalid URL")
        if is_timestamp_outside_range(record['created_utc']):
            return REJECT("Outside date range")
        if is_exact_duplicate_url(record['url']):
            return REJECT("Duplicate URL")

        # PASSED hard filters, but may need review
        return ACCEPT_FOR_REVIEW

    # Similar logic for YouTube, Products
```

### Phase 2: SME Relevancy Review

**Sample:** 5% of passed records (minimum 50)
**Reviewer:** Subject matter expert (not involved in collection)
**Time per sample:** 5-10 minutes
**Scoring:** Use scoring rubric above (0, 1, or 2)

**Procedure:**

```
1. Extract 5% random sample
2. SME scores each record: 0=Remove, 1=Keep with flag, 2=Keep
3. Calculate average score
4. If average ≥1.5 and no score of 0 items: PASS
5. If average <1.5 or any score of 0: Identify root cause
```

### Phase 3: Root Cause Analysis

**If relevancy check FAILS:**

```
Example: YouTube video dataset average score = 1.2 (FAIL)

Questions:
1. Are keywords too broad? (Getting off-topic videos)
   → Fix: Refine keywords in Step 01

2. Are channels including non-relevant content?
   → Fix: Add channel filter in extraction

3. Is time period capturing outdated products?
   → Fix: Narrow date range in Step 01

4. Is sample size too small?
   → Fix: Collect more records to achieve target sample

Action: Fix root cause, re-extract, re-test relevancy
```

### Phase 4: Removal Documentation

**For each removed record:**

```json
{
  "removed_record_id": "post_123",
  "original_source": "https://reddit.com/r/DIY/comments/...",
  "removal_reason": "Score 0 - Off-topic (about automotive repair, not garage storage)",
  "removal_scorer": "SME_name",
  "removal_date": "2025-11-12T12:30:00Z",
  "original_content_sample": "Tips for changing your truck's oil...",
  "audit_trail": "Removal_log_entry_#847"
}
```

All removals logged to: `/03-analysis-output/extraction-logs/REMOVAL_LOG.json`

---

## QUALITY GATES BY DATASET

### REDDIT POSTS: Must Pass ALL

| Gate | Requirement | Validation | Failure Action |
|------|-------------|-----------|---|
| Sample Relevancy | ≥1.5 avg score | 5% sample review | Refine keywords, re-extract |
| Content Quality | ≥95% >20 chars | Automated check | OK if 95%+ pass |
| Author Quality | ≥99% non-deleted | Automated check | OK if 99%+ pass |
| URL Quality | 100% valid URLs | Automated check | STOP if <100% |
| No Spam | <5% spam in sample | Manual review | Remove identified spam |

### YOUTUBE VIDEOS: Must Pass ALL

| Gate | Requirement | Validation | Failure Action |
|------|-------------|-----------|---|
| Sample Relevancy | ≥1.5 avg score | 5% sample review | Refine keywords, re-extract |
| Transcript Quality | ≥90% usable | Automated check | OK if 90%+ have transcripts |
| Channel Quality | ≥95% legitimate | Manual review | Block spam channels |
| View Count | 100% >100 views | Automated check | STOP if <100% |
| Content Focus | ≥85% garage-relevant | Manual review | Remove non-garage videos |

### PRODUCTS: Must Pass ALL

| Gate | Requirement | Validation | Failure Action |
|------|-------------|-----------|---|
| Sample Relevancy | ≥1.5 avg score | 5% sample review | Refine categories, re-extract |
| Category Match | ≥95% correct category | Manual spot-check | Fix category labels |
| URL Validity | 100% accessible | Automated verification | STOP if links dead |
| Data Completeness | ≥90% have prices | Automated check | OK if 90%+ have prices |
| Retailer Quality | 100% valid retailers | Automated check | STOP if invalid retailer |

---

## RELEVANCY ISSUES & RESOLUTIONS

### Issue 1: "Reddit Keywords Return Too Many Off-Topic Posts"

**Symptom:** Relevancy score 1.0 (below 1.5 threshold)

**Root Cause:** Keywords like "storage" are too broad (also matches storage lockers, file storage, data storage)

**Resolution:**
- Add exclusion keywords: "NOT garage", "NOT commercial", "NOT warehouse"
- Refine to compound keywords: "garage storage", "garage shelving", "home organization"
- Add subreddit filtering (r/DIY posts more specific than r/organization)
- Re-extract with refined parameters

### Issue 2: "YouTube Videos Include Unrelated Channels"

**Symptom:** Relevancy score 1.1 (below threshold)

**Root Cause:** Keyword "storage" matches general organizing channels, not garage-specific

**Resolution:**
- Add channel-level filtering (known DIY channels only)
- Add phrase matching requirement: must say "garage" OR "garage" in description
- Manually blocklist irrelevant channels found in review
- Re-extract with filters

### Issue 3: "Products Include Wrong Categories"

**Symptom:** Sample includes automotive parts, filing cabinets, tool chests (borderline)

**Root Cause:** Category tags on retailer sites are inconsistent/inaccurate

**Resolution:**
- Manual product review to correct category labels
- Re-extract with refined category filters
- OR accept with notation that product scope is broader than "shelving" only
- Document in methodology what "garage organization" means

---

## RELEVANCY SIGN-OFF PROCESS

**Every dataset requires SME sign-off:**

```
RELEVANCY CHECK SIGN-OFF
═══════════════════════════════════════

Dataset: reddit_posts_raw.json
Records: 1,247

Reviewer Name: [SME Name]
Review Date: 2025-11-12
Review Duration: 90 minutes

Sample Size: 62 records (5%)
Scoring Results:
  - Score 2 (Highly Relevant): 57 records (91.9%)
  - Score 1 (Marginally Relevant): 5 records (8.1%)
  - Score 0 (Not Relevant): 0 records (0%)

Average Score: 1.92 / 2.0
Pass Threshold: 1.5
STATUS: ✅ PASS

Records to Remove (Score 0): 0
Records Removed Reason: N/A

Issues Found:
- 2 posts about RV storage (tangential, kept with note)
- 1 post discussing commercial warehouse (kept for comparison context)

Reviewer Assessment:
"Data is highly relevant. Posts directly address garage organization
pain points and product choices. Authentic consumer voices. Ready for
analysis. Note: Small percentage of posts are tangentially related
(RVs, commercial) but provided useful context for consumer mindset."

Reviewer Signature: [Approved]
═══════════════════════════════════════
```

---

## QUALITY METRICS DASHBOARD

After each dataset collection, create:
`/03-analysis-output/QUALITY_METRICS.json`

```json
{
  "quality_metrics_summary": {
    "collection_date": "2025-11-12",

    "reddit": {
      "total_attempted": 2847,
      "total_collected": 1247,
      "collection_rate_percent": 43.8,
      "rejected_reasons": {
        "below_min_score": 800,
        "text_too_short": 450,
        "outside_date": 250,
        "duplicates": 100,
        "other": 0
      },
      "quality_metrics": {
        "urls_valid_percent": 100,
        "text_quality_percent": 98.9,
        "author_quality_percent": 99.4
      },
      "relevancy_check": {
        "status": "PASS",
        "sample_size": 62,
        "average_score": 1.92,
        "threshold": 1.5,
        "scorer": "SME_name",
        "date": "2025-11-12T12:30:00Z"
      }
    },

    "youtube": {
      "total_attempted": 450,
      "total_collected": 78,
      "collection_rate_percent": 17.3,
      "relevancy_check": {
        "status": "PASS",
        "average_score": 1.85,
        "threshold": 1.5
      }
    },

    "products": {
      "total_attempted": 8900,
      "total_collected": 8234,
      "collection_rate_percent": 92.5,
      "relevancy_check": {
        "status": "PASS",
        "average_score": 1.88,
        "threshold": 1.5
      }
    },

    "overall_status": "READY_FOR_ANALYSIS",
    "date_generated": "2025-11-12T15:00:00Z"
  }
}
```

---

## ENFORCEMENT

**Relevancy validation is NON-NEGOTIABLE:**

- ✅ Cannot skip relevancy review
- ✅ Cannot proceed to analysis with relevancy_status = "PENDING"
- ✅ Cannot combine low-relevancy datasets with other projects
- ✅ Cannot deliver client insights without relevancy sign-off

**If relevancy fails:**
1. Identify root cause
2. Re-collect with refined parameters
3. Re-validate relevancy
4. Proceed only after PASS

---

## SUCCESS CRITERIA

**Step passes when:**

1. All automated filters applied correctly
2. 5% sample reviewed by SME
3. Sample average score ≥1.5 (≥1.5 out of 2.0)
4. Zero Score 0 items, OR all removed and logged
5. SME sign-off obtained and documented
6. Removal log complete with reasons
7. Quality metrics dashboard updated
8. Manifest shows "relevancy_status": "PASS"

---

**Framework Status:** ✅ ACTIVE
**Last Updated:** November 12, 2025
**Enforcement Level:** MANDATORY - NO EXCEPTIONS
