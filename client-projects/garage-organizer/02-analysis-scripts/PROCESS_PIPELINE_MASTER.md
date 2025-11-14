# GARAGE ORGANIZER DATA COLLECTION PIPELINE
## Master Process Guide

**Version:** 1.0
**Created:** November 12, 2025
**Status:** Ready for execution

---

## OVERVIEW

This pipeline collects, validates, and documents audit trails for all data and insights in the Garage Organizer Category Intelligence analysis. The process is **sequential, repeatable, and auditable**.

Each step produces:
1. **Raw output file** (with manifest)
2. **Validation report** (pass/fail on all rules)
3. **Audit log** (what was done, when, by whom)

---

## PROCESS FLOW

```
01-DEFINE-SCOPE.md
       ↓
02-EXTRACT-REDDIT.md
       ↓
03-EXTRACT-YOUTUBE.md
       ↓
04-EXTRACT-PRODUCTS.md
       ↓
05-VALIDATE-DATA.md
       ↓
06-ANALYZE-CONTENT.md
       ↓
07-GENERATE-AUDIT-TRAIL.md
       ↓
08-CLIENT-DELIVERY.md
```

---

## QUICK START

**To run the full pipeline:**

```bash
cd /Users/anderson115/00-interlink/12-work/3m-lighting-project/client-projects/garage-organizer/02-analysis-scripts/

# Run each step in order:
bash 01-DEFINE-SCOPE.sh
bash 02-EXTRACT-REDDIT.sh
bash 03-EXTRACT-YOUTUBE.sh
bash 04-EXTRACT-PRODUCTS.sh
bash 05-VALIDATE-DATA.sh
bash 06-ANALYZE-CONTENT.sh
bash 07-GENERATE-AUDIT-TRAIL.sh
bash 08-CLIENT-DELIVERY.sh
```

**Expected runtime:** 4-6 hours total
**Output location:** `/01-raw-data/`, `/03-analysis-output/`, `/06-final-deliverables/`

---

## KEY CONSTRAINTS (NON-NEGOTIABLE)

### Rule 1: No Fabricated Data
- Every quote must have source URL
- Every statistic must have calculation shown
- Every dataset must include metadata

### Rule 2: Audit Trail First
- Each file must include manifest with:
  - Collection date/time
  - Collection method
  - Record count
  - Data quality metrics
  - Completeness percentage

### Rule 3: Validation Loops at Each Step
- Do NOT wait until end to validate
- Stop and escalate if any validation rule fails
- Document all failures with remediation steps

### Rule 4: No Assumptions
- Verify every file path before execution
- Verify every API key before requesting data
- Log all errors with full stack traces

---

## PROCESS FILE DESCRIPTIONS

### 01-DEFINE-SCOPE.md
**What:** Define search parameters, sample sizes, and platform keywords
**Output:** `scope_definition.json` (single file, no data yet)
**Validation:** Confirm all parameters are documented and reasonable
**Time:** 30 minutes

### 02-EXTRACT-REDDIT.md
**What:** Pull Reddit posts from r/DIY, r/HomeImprovement, r/organization using PRAW
**Output:** `reddit_posts_raw.json` (1,200-1,500 posts)
**Validation:** Format check, URL verification, author deduplication
**Time:** 45 minutes

### 03-EXTRACT-YOUTUBE.md
**What:** Pull YouTube video metadata and transcripts
**Output:** `youtube_videos_raw.json` (60-100 videos)
**Validation:** Transcript quality, view count verification
**Time:** 60 minutes

### 04-EXTRACT-PRODUCTS.md
**What:** Aggregate product database from 6 retailers
**Output:** `products_consolidated.json` (7,000-10,000 products)
**Validation:** Price/rating/SKU deduplication, category matching
**Time:** 45 minutes

### 05-VALIDATE-DATA.md
**What:** Run comprehensive validation across all files
**Output:** `validation_report.json` (pass/fail on 12 rule sets)
**Validation:** Stop if any critical rule fails
**Time:** 30 minutes

### 06-ANALYZE-CONTENT.md
**What:** Code pain points, behaviors, and sentiment
**Output:** `analysis_output.json` (frequencies, percentages, inter-rater reliability)
**Validation:** Manual spot-check on 10% sample, verify inter-rater reliability ≥85%
**Time:** 90 minutes

### 07-GENERATE-AUDIT-TRAIL.md
**What:** Create quote verification worksheet and methodology documentation
**Output:** `audit_trail.json`, `quote_verification.csv`, `methodology.md`
**Validation:** All quotes must have URL, all percentages must have calculation
**Time:** 60 minutes

### 08-CLIENT-DELIVERY.md
**What:** Package final deliverables with limitations and transparency notes
**Output:** Client-ready summary, methodology appendix, quote verification worksheet
**Validation:** Client sign-off ready
**Time:** 45 minutes

---

## VALIDATION RULES MATRIX

| Step | Rule | Type | Failure Action |
|------|------|------|-----------------|
| 02 | All Reddit posts have URL | CRITICAL | Stop pipeline, review API response |
| 02 | No duplicate authors in single post | CRITICAL | Log duplicates, remove before analysis |
| 02 | Post text >20 characters | MEDIUM | Flag short posts, verify intent |
| 03 | All videos have transcripts | CRITICAL | Skip video if transcript unavailable |
| 03 | Video view count >0 | CRITICAL | Flag zero-view videos |
| 04 | All products have retailer | CRITICAL | Reject product record |
| 04 | Price >$0 for items with price | MEDIUM | Flag anomalies, investigate |
| 04 | Deduplication by URL or SKU | CRITICAL | Remove exact duplicates |
| 05 | All required fields present | CRITICAL | Generate missing field report |
| 05 | Record count within ±5% of target | MEDIUM | Log discrepancy, justify |
| 06 | Inter-rater reliability ≥85% | CRITICAL | Retrain coders, reprocess sample |
| 07 | All quotes have source URL | CRITICAL | Remove unverifiable quote |

---

## COMMON FAILURE MODES & FIXES

### Failure: "API Rate Limit Exceeded"
- **Cause:** Too many requests in short time
- **Fix:** Add 2-second delay between requests, resume from last checkpoint
- **Prevention:** Use checkpoint file to resume interrupted runs

### Failure: "Duplicate Records Detected"
- **Cause:** Same post scraped multiple times or cross-platform repost
- **Fix:** Deduplicate by URL hash, keep first occurrence, log removed records
- **Prevention:** Build deduplication into extraction step

### Failure: "Missing Transcript for YouTube Video"
- **Cause:** Video has no auto-generated or manual captions
- **Fix:** Skip video, log with video_id and title
- **Prevention:** Check caption availability before adding to extraction list

### Failure: "Inter-rater Reliability <85%"
- **Cause:** Coders disagreed on classification
- **Fix:** Review disagreement examples, clarify coding rules, recode sample
- **Prevention:** Do inter-rater test on small sample BEFORE full analysis

### Failure: "Product Price = $0"
- **Cause:** Missing price data from retailer
- **Fix:** Mark as "price_unavailable", do not filter out
- **Prevention:** Check price field for all retailer APIs

### Failure: "Quote Not Found in Raw Data"
- **Cause:** Verbatim doesn't exist in any data source
- **Fix:** Flag as UNVERIFIABLE, remove from deck UNLESS source URL provided
- **Prevention:** Audit trail creation requires quote verification worksheet

---

## FILE LOCATIONS

**Input Location:**
```
/client-projects/garage-organizer/
├── 01-raw-data/          (input data sources)
```

**Output Locations:**
```
/client-projects/garage-organizer/
├── 02-analysis-scripts/  (this directory - process files)
├── 03-analysis-output/   (intermediate analysis files)
└── 06-final-deliverables/ (client-ready files)
```

---

## EXECUTION CHECKLIST

Before running each step:

- [ ] Read the process file completely
- [ ] Verify all input files exist
- [ ] Check all API keys are configured
- [ ] Ensure output directory exists
- [ ] Review expected output file format
- [ ] Understand validation rules for this step

After running each step:

- [ ] Validation report shows all rules PASS
- [ ] Output file has required manifest section
- [ ] Record count matches expected range
- [ ] Spot-check 5 random records for quality
- [ ] Document any unusual findings

---

## SUPPORT & ESCALATION

**If validation rule fails:**
1. Read the failure description in that step's process file
2. Follow the "Fix" procedure
3. Re-run the step with corrected input
4. Document the issue in `/03-analysis-output/ISSUES_LOG.md`

**If issue persists:**
1. Log full error in ISSUES_LOG.md with timestamp
2. Identify root cause (API error, bad data, code bug)
3. Propose remediation (resume from checkpoint, retry, data fix)
4. Do not proceed to next step until resolved

---

## METRICS TO TRACK

At completion, the pipeline should produce:

```json
{
  "reddit_posts": {
    "collected": 1200,
    "with_urls": 1200,
    "deduped": 1185,
    "final": 1185,
    "completion_rate": "98.75%"
  },
  "youtube_videos": {
    "collected": 80,
    "with_transcripts": 78,
    "final": 78,
    "completion_rate": "97.5%"
  },
  "products": {
    "collected": 8500,
    "deduplicated": 8200,
    "final": 8200,
    "completion_rate": "96.5%"
  },
  "analysis": {
    "records_coded": 8463,
    "inter_rater_reliability": "87.2%",
    "quotes_verified": 31,
    "quotes_unverifiable": 0,
    "status": "READY_FOR_CLIENT"
  }
}
```

---

## NEXT STEPS

1. Read `01-DEFINE-SCOPE.md` to start
2. Execute in order (do not skip steps)
3. After each step, review validation report
4. Stop immediately if any CRITICAL rule fails
5. Document all decisions in `/03-analysis-output/EXECUTION_LOG.md`

---

**Pipeline Ready:** ✅
**Last Updated:** November 12, 2025
