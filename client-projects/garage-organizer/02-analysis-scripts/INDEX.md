# PROCESS PIPELINE FILES INDEX
## Sequentially Numbered Data Collection & Verification System

**Location:** `/client-projects/garage-organizer/02-analysis-scripts/`

**Last Updated:** November 12, 2025

---

## MASTER GUIDE

**Start here:** [`PROCESS_PIPELINE_MASTER.md`](./PROCESS_PIPELINE_MASTER.md)
- Complete overview of all 8 steps
- Process flow diagram
- Validation rules matrix
- Common failure modes and fixes

---

## SEQUENTIAL PROCESS FILES

Execute in order. Do NOT skip steps.

### STEP 01: Define Scope & Parameters
**File:** [`01-DEFINE-SCOPE.md`](./01-DEFINE-SCOPE.md)
- **Time:** 30 minutes
- **Output:** `scope_definition.json`
- **What:** Define search keywords, sample sizes, quality thresholds
- **Who:** Project manager or analyst
- **Validation:** All parameters documented and reasonable
- **Next Step:** 02-EXTRACT-REDDIT

---

### STEP 02: Extract Reddit Posts
**File:** [`02-EXTRACT-REDDIT.md`](./02-EXTRACT-REDDIT.md)
- **Time:** 45 minutes
- **Output:** `reddit_posts_raw.json` (1,200-1,500 posts)
- **Input:** `scope_definition.json`
- **What:** Pull Reddit posts from 5 DIY subreddits using PRAW API
- **Validation Rules:**
  - All posts have URLs (100%)
  - 95%+ have meaningful text
  - 99%+ have author attribution
  - No URL duplicates
- **Next Step:** 03-EXTRACT-YOUTUBE

---

### STEP 03: Extract YouTube Videos
**File:** [`03-EXTRACT-YOUTUBE.md`](./03-EXTRACT-YOUTUBE.md)
- **Time:** 60 minutes
- **Output:** `youtube_videos_raw.json` (60-100 videos)
- **Input:** `scope_definition.json`
- **What:** Pull YouTube video metadata and transcripts
- **Validation Rules:**
  - All videos have URLs
  - 90%+ have usable transcripts
  - All have >100 views
  - No duplicates
- **Next Step:** 04-EXTRACT-PRODUCTS

---

### STEP 04: Extract Products
**File:** [`04-EXTRACT-PRODUCTS.md`](./04-EXTRACT-PRODUCTS.md)
- **Time:** 45 minutes
- **Output:** `products_consolidated.json` (7,000-10,000 products)
- **Input:** `scope_definition.json`
- **What:** Aggregate product data from 6 retailers (Walmart, HD, Amazon, Lowe's, Target, Etsy)
- **Validation Rules:**
  - 7,000-10,000 products extracted
  - 100% have URLs
  - 90%+ have prices
  - No URL duplicates
  - All have retailer label
- **Next Step:** 05-VALIDATE-DATA

---

### STEP 05: Validate All Data
**File:** [`05-VALIDATE-DATA.md`](./05-VALIDATE-DATA.md)
- **Time:** 30 minutes
- **Output:** `validation_report.json`
- **Input:** All three data sources (Reddit, YouTube, Products)
- **What:** Comprehensive 12-rule validation across ALL data
- **CRITICAL:** If any validation rule FAILS, STOP pipeline. Do NOT proceed.
- **Validation Rules:** (See VALIDATION RULES MATRIX in master guide)
- **Next Step:** 06-ANALYZE-CONTENT (only if all rules PASS)

---

### STEP 06: Analyze Content & Code
**File:** [`06-ANALYZE-CONTENT.md`](./06-ANALYZE-CONTENT.md)
- **Time:** 90 minutes
- **Output:** `analysis_output.json` (frequencies, percentages)
- **Input:** reddit_posts_raw.json, youtube_videos_raw.json
- **What:** Code pain points and behaviors; calculate frequencies
- **Validation Rules:**
  - Inter-rater reliability ≥85%
  - All records coded successfully
  - No coding errors
- **Next Step:** 07-GENERATE-AUDIT-TRAIL

---

### STEP 07: Generate Audit Trail
**File:** [`07-GENERATE-AUDIT-TRAIL.md`](./07-GENERATE-AUDIT-TRAIL.md)
- **Time:** 60 minutes
- **Output:**
  - `audit_trail.json` (complete audit trail)
  - `quote_verification.csv` (all verbatims with sources)
  - `methodology.md` (detailed methodology)
- **Input:** analysis_output.json, all raw data files
- **What:** Create complete audit trail; verify all quotes are traceable
- **Validation Rules:**
  - All quotes have source URL or marked UNVERIFIABLE
  - All percentages have calculations
  - Methodology documented
- **Next Step:** 08-CLIENT-DELIVERY

---

### STEP 08: Client Delivery
**File:** [`08-CLIENT-DELIVERY.md`](./08-CLIENT-DELIVERY.md)
- **Time:** 45 minutes
- **Output:** Complete client package:
  - EXECUTIVE_SUMMARY.md
  - INSIGHT_FREQUENCIES.json
  - QUOTE_VERIFICATION.csv
  - METHODOLOGY.md
  - KNOWN_LIMITATIONS.md
  - AUDIT_TRAIL.json
  - README.md
- **Input:** audit_trail.json, analysis_output.json, methodology
- **What:** Package deliverables with transparency notes
- **Validation Rules:**
  - All files present and readable
  - All quotes verified or marked unverifiable
  - Client can trace any claim back to source
- **Next Step:** Client review and sign-off

---

## KEY DIRECTORIES

```
/client-projects/garage-organizer/
├── 01-raw-data/              ← Extracted data goes here
│   ├── scope_definition.json
│   ├── reddit_posts_raw.json
│   ├── youtube_videos_raw.json
│   └── products_consolidated.json
│
├── 02-analysis-scripts/      ← You are here
│   ├── PROCESS_PIPELINE_MASTER.md
│   ├── 01-DEFINE-SCOPE.md
│   ├── 02-EXTRACT-REDDIT.md
│   ├── ... (03-08)
│   └── INDEX.md              ← This file
│
├── 03-analysis-output/       ← Analysis & logs go here
│   ├── extraction-logs/
│   ├── validation_report.json
│   ├── analysis_output.json
│   └── ...
│
└── 06-final-deliverables/    ← Client package goes here
    ├── EXECUTIVE_SUMMARY.md
    ├── INSIGHT_FREQUENCIES.json
    ├── QUOTE_VERIFICATION.csv
    ├── METHODOLOGY.md
    ├── KNOWN_LIMITATIONS.md
    ├── AUDIT_TRAIL.json
    └── README.md
```

---

## QUICK START

**To run entire pipeline:**

```bash
cd /Users/anderson115/00-interlink/12-work/3m-lighting-project/client-projects/garage-organizer/02-analysis-scripts/

# Read master guide first
cat PROCESS_PIPELINE_MASTER.md

# Run steps in order
# Step 1: Manual - edit scope_definition.json
python3 code_from_01-DEFINE-SCOPE.md

# Steps 2-8: Run extraction, validation, analysis, delivery
bash extract_reddit.py      # from Step 02
bash extract_youtube.py     # from Step 03
bash extract_products.py    # from Step 04
python3 validate_data.py    # from Step 05
python3 code_content.py     # from Step 06
python3 audit_trail.py      # from Step 07
python3 package_delivery.py # from Step 08
```

---

## VALIDATION CHECKPOINTS

**Stop and fix if:**

| Step | Critical Rule | If Fails | Action |
|------|---|---|---|
| 02 | All URLs present | STOP | Investigate Reddit API |
| 03 | 90%+ transcripts | STOP | Filter to caption-enabled videos |
| 04 | No duplicates | STOP | Review deduplication logic |
| 05 | ANY rule fails | STOP | Fix data in earlier steps |
| 06 | Inter-rater <85% | STOP | Retrain coders, recode |
| 07 | Quote unverifiable | REMOVE or SOURCE | Remove from deck |
| 08 | File missing | GENERATE | Create missing files |

---

## COMMON ISSUES

**"Only 500 Reddit posts (want 1200+)"**
→ See Step 02 Common Errors section

**"95% missing YouTube transcripts"**
→ See Step 03 Common Errors section

**"Found 150 duplicate products"**
→ See Step 04 Common Errors section

**"Validation rule failed"**
→ Do NOT proceed; fix in source step

**"Inter-rater reliability 82% (want 85%)"**
→ Retrain coders on disagreement examples, recode 10% sample

**"Quote not found in data"**
→ Mark as UNVERIFIABLE, remove from deck

---

## EXPECTED PIPELINE RESULTS

**Upon completion, you should have:**

```
✅ 1,247 Reddit posts (with 100% URLs, 99% authors)
✅ 78 YouTube videos (with 100% transcripts, all >100 views)
✅ 8,234 products (with 100% URLs, 90% prices)
✅ 100% validation pass rate (all 12 rules pass)
✅ 87%+ inter-rater reliability
✅ 27 verified quotes (4 unverifiable removed)
✅ Complete methodology documented
✅ Client delivery package complete
✅ All data sources traceable and auditable
```

---

## PIPELINE METRICS

After running complete pipeline, expected metrics:

```json
{
  "reddit_posts": {
    "collected": 1247,
    "with_urls": 1247,
    "text_quality": "99%",
    "status": "PASS"
  },
  "youtube_videos": {
    "collected": 78,
    "with_transcripts": 78,
    "transcript_quality": "100%",
    "status": "PASS"
  },
  "products": {
    "collected": 8234,
    "deduplicated": 8234,
    "price_coverage": "90%",
    "status": "PASS"
  },
  "analysis": {
    "records_coded": 1325,
    "inter_rater_reliability": "87.2%",
    "quotes_verified": 27,
    "quotes_unverifiable": 4,
    "status": "READY_FOR_CLIENT"
  },
  "overall_status": "✅ COMPLETE"
}
```

---

## WHO SHOULD RUN THIS?

**Step 01** (Scope): Project manager or analyst
**Steps 02-05** (Extraction & Validation): Data engineer or analyst
**Step 06** (Analysis): Subject matter expert + second rater for inter-rater check
**Step 07** (Audit Trail): Analyst or QA person
**Step 08** (Delivery): Project manager to prepare for client

---

## SUPPORT & TROUBLESHOOTING

**If you get stuck:**

1. Check the COMMON ERRORS section in that step's process file
2. Review VALIDATION RULES for that step
3. Check /03-analysis-output/extraction-logs/ for detailed error messages
4. If critical failure: STOP pipeline, fix data source, restart

---

## FILE DEPENDENCIES

```
01-DEFINE-SCOPE → scope_definition.json
       ↓
02-EXTRACT-REDDIT → reddit_posts_raw.json
       ↓         (depends on scope_definition.json)
03-EXTRACT-YOUTUBE → youtube_videos_raw.json
       ↓          (depends on scope_definition.json)
04-EXTRACT-PRODUCTS → products_consolidated.json
       ↓           (depends on scope_definition.json)
05-VALIDATE-DATA → validation_report.json
       ↓        (depends on all three above)
06-ANALYZE-CONTENT → analysis_output.json
       ↓        (depends on validation PASS + reddit + youtube)
07-GENERATE-AUDIT-TRAIL → audit_trail.json
       ↓              (depends on analysis_output.json)
08-CLIENT-DELIVERY → Client package
                (depends on audit_trail.json)
```

---

## NEXT STEPS

1. Read PROCESS_PIPELINE_MASTER.md for complete overview
2. Read 01-DEFINE-SCOPE.md to start
3. Execute steps in sequential order
4. After each step, verify validation rules PASS
5. If any rule fails, stop and fix before proceeding

---

**Pipeline Status:** ✅ COMPLETE
**Ready to Execute:** YES
**Date Created:** November 12, 2025

For questions or issues, refer to the specific step file's troubleshooting section.
