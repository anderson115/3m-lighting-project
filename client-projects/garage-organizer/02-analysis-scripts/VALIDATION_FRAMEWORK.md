# DATA VALIDATION & AUDIT TRAIL FRAMEWORK
## High Relevancy Standards for Garage Organizer Pipeline

**Created:** November 12, 2025
**Status:** ✅ MANDATORY FOR ALL STEPS
**Enforcement:** NON-NEGOTIABLE

---

## CORE PRINCIPLE

**Every file created must be:**
1. **Relevant** - Data directly addresses scope requirements
2. **Verifiable** - Can trace back to original source
3. **Auditable** - Complete chain of custody documented
4. **Validated** - Self-validating with automated checks

---

## THREE-LAYER VALIDATION ARCHITECTURE

### LAYER 1: COLLECTION VALIDATION
**When:** DURING data extraction
**Who:** Extraction script
**What:** Verify data meets collection criteria BEFORE storing

```
Collect → Validate → Store → Log
                      ↓
                   If FAIL: Reject & Report
```

**Never store data that hasn't been validated.**

---

### LAYER 2: RELEVANCY VALIDATION
**When:** AFTER collection, BEFORE analysis
**Who:** Subject matter expert or analyst
**What:** Confirm ALL data is on-topic and relevant

**Relevancy Questions:**
- Does this data address garage organization?
- Is this consumer voice authentic (not spam)?
- Does this product belong in our category?
- Would this insight be actionable for 3M?

**If NOT relevant: REMOVE and document why**

---

### LAYER 3: AUDIT TRAIL VALIDATION
**When:** BEFORE client delivery
**Who:** QA/Compliance
**What:** Verify complete chain of custody for every data point

**Audit Trail Requirements:**
- Original source URL documented
- Collection timestamp recorded
- Extraction method documented
- Quality flags recorded
- All removals/filters logged with reasons

---

## MANDATORY MANIFEST FOR EVERY FILE

Every extracted data file MUST include this manifest:

```json
{
  "manifest": {
    "file_name": "reddit_posts_raw.json",
    "extraction_date": "2025-11-12T10:30:00Z",
    "extraction_source": "Reddit PRAW API v1.0",
    "extraction_scope": "See scope_definition.json (SHA256: abc123...)",

    "quality_gates": {
      "total_records_attempted": 2847,
      "total_records_collected": 1247,
      "total_records_rejected": 1600,
      "rejection_reasons": {
        "below_minimum_score": 800,
        "post_text_too_short": 450,
        "outside_date_range": 250,
        "duplicate_urls": 100
      }
    },

    "data_quality_metrics": {
      "completeness": {
        "records_with_urls": 1247,
        "records_with_text": 1235,
        "records_with_author": 1240,
        "completeness_percent": 99.0
      },
      "relevancy_check_status": "PENDING_REVIEW",
      "relevancy_checked_by": null,
      "relevancy_check_date": null,
      "relevancy_issues_found": 0,
      "relevancy_issues_resolved": 0
    },

    "audit_trail": {
      "collection_method": "PRAW API search with keywords from scope",
      "keywords_used": ["garage organization", "garage storage", "garage shelving"],
      "subreddits_searched": ["r/DIY", "r/HomeImprovement"],
      "filters_applied": [
        "post_score >= 5",
        "selftext length > 20",
        "created >= 2023-01-01",
        "no_duplicate_urls"
      ],
      "api_calls_made": 50,
      "api_rate_limit_hits": 0,
      "checkpoint_file": "/03-analysis-output/extraction-logs/reddit_checkpoint.json",
      "extraction_log": "/03-analysis-output/extraction-logs/reddit_extraction.log"
    },

    "source_verification": {
      "spot_check_sample_size": 50,
      "spot_check_verified_count": 50,
      "spot_check_verification_rate": 100.0,
      "spot_check_results": {
        "all_urls_accessible": true,
        "all_subreddits_correct": true,
        "all_dates_in_range": true,
        "all_text_relevant": true
      },
      "spot_check_performed_by": "analyst_name",
      "spot_check_date": "2025-11-12T11:00:00Z"
    },

    "validation_status": {
      "collection_validation": "PASS",
      "relevancy_validation": "PENDING",
      "audit_trail_validation": "PASS",
      "overall_status": "READY_FOR_RELEVANCY_CHECK",
      "next_step": "Manual relevancy review of 5% random sample"
    }
  },

  "posts": [
    {
      "post_id": "abc123",
      "source_url": "https://reddit.com/r/DIY/comments/abc123/...",
      "extraction_timestamp": "2025-11-12T10:35:42Z",
      "quality_flags": []
    }
  ]
}
```

---

## RELEVANCY VALIDATION PROCEDURE

**For each extracted dataset:**

### Step 1: Define Relevancy Criteria
```json
{
  "relevancy_criteria": {
    "garage_organization": {
      "must_contain": ["garage", "storage", "shelving", "organization"],
      "context_must_be": "residential garage context",
      "exclude": ["commercial", "warehouse", "industrial"]
    },
    "consumer_authenticity": {
      "must_be": "genuine consumer experience",
      "exclude": ["spam", "promotional", "bot"]
    },
    "actionability": {
      "must_inform": "product development OR customer support OR marketing strategy"
    }
  }
}
```

### Step 2: Random Sample Relevancy Check
- **Sample size:** 5% of collected records (minimum 50 records)
- **Reviewer:** Subject matter expert
- **Method:** Manual review with scoring rubric
- **Scoring:** 0=not relevant, 1=marginally relevant, 2=highly relevant

**Acceptance Criteria:**
- 100% score ≥1 (all relevant or better)
- Average score ≥1.5 (on average highly relevant)
- Zero spam/promotional content

### Step 3: Document Results
```json
{
  "relevancy_validation": {
    "dataset": "reddit_posts_raw.json",
    "sample_size": 62,
    "sample_selection": "random stratified by subreddit",
    "results": {
      "not_relevant": 0,
      "marginally_relevant": 5,
      "highly_relevant": 57,
      "average_score": 1.89,
      "pass_threshold": 1.5,
      "status": "PASS"
    },
    "issues_found": [
      "3 posts about commercial garage (removed)",
      "2 posts off-topic (removed)"
    ],
    "reviewed_by": "subject_matter_expert_name",
    "review_date": "2025-11-12T12:00:00Z",
    "sign_off": true
  }
}
```

### Step 4: Remove Non-Relevant Records
- Delete any records scoring <1
- Document in removal log
- Update manifest with removal count
- Create removal audit trail

---

## AUDIT TRAIL REQUIREMENTS

**Every data point must trace back through:**

```
Original Source URL
    ↓
Extraction Log (timestamp, method, API call)
    ↓
Raw Data File (with manifest)
    ↓
Relevancy Check (verified on-topic)
    ↓
Analysis (coded, frequencies calculated)
    ↓
Client Quote (with source URL and verification date)
```

**Complete Chain Example:**

```
Tweet: "Command hooks fell off my wall"
  ← Original source URL: reddit.com/r/DIY/comments/abc123
  ← Extraction log: 2025-11-12T10:35:42Z, PRAW API search "garage hooks"
  ← Raw data: reddit_posts_raw.json (post_id: abc123)
  ← Relevancy: Reviewed 2025-11-12, scored 2/2 (highly relevant)
  ← Coded: pain_point="adhesive_failure", behavior="frustration_trigger"
  ← Quote: Can be used in deck WITH source attribution
```

---

## SELF-VALIDATING SCRIPTS

Every extraction script MUST include:

### 1. Pre-Extraction Validation
```python
def validate_prerequisites():
    # Verify config files exist
    # Verify API credentials work
    # Verify scope_definition.json is valid
    # Verify output directories exist
    # Return: pass/fail with detailed errors
```

### 2. Real-Time Collection Validation
```python
def validate_record(record):
    # Check all required fields present
    # Check field data types correct
    # Check URLs are valid format
    # Check dates are in range
    # Check text length >= minimum
    # Return: valid/invalid with reason codes
```

### 3. Post-Extraction Validation
```python
def validate_extraction():
    # Compare attempted vs collected vs rejected counts
    # Verify no duplicates (URL hash)
    # Verify completeness percentages
    # Generate spot-check sample
    # Create validation report
    # Return: pass/fail with metrics
```

### 4. Manifest Generation
```python
def generate_manifest():
    # Record all extraction metadata
    # Include quality metrics
    # Include all filters applied
    # Include API call log
    # Include spot-check results
    # Write to manifest section of output file
```

---

## AUDIT LOG REQUIREMENTS

Every step must maintain audit log at:
`/03-analysis-output/extraction-logs/AUDIT_LOG.md`

**Format:**
```markdown
# AUDIT LOG - Data Extraction Pipeline

## Step 02: Extract Reddit (2025-11-12 10:30-11:15)

### Execution
- Start time: 2025-11-12 10:30:00Z
- End time: 2025-11-12 11:15:00Z
- Duration: 45 minutes
- Operator: analyst_name
- Script version: extract_reddit.py v1.0

### Data Collection
- Attempted records: 2,847
- Collected records: 1,247
- Rejected records: 1,600
- Collection rate: 43.8%

### Rejections Breakdown
- Below minimum score (5): 800 records
- Text too short (<20 chars): 450 records
- Outside date range: 250 records
- Duplicate URLs: 100 records

### Quality Checks
- All 1,247 have valid URLs: ✅
- 1,235 (98.9%) have text >20 chars: ✅
- 1,240 (99.4%) have author attribution: ✅
- Zero duplicate URLs detected: ✅

### Spot Check (50 random records)
- All 50 verified accessible: ✅
- All 50 from correct subreddits: ✅
- All 50 within date range: ✅

### Issues Encountered
- 2 API rate limits (handled with backoff)
- 5 timeouts (retried successfully)
- 0 authentication errors

### Output
- File: reddit_posts_raw.json
- Size: 4.2 MB
- Records: 1,247
- Manifest: ✅ Complete
- Checkpoint: ✅ Saved

### Relevancy Validation Status
- Status: PENDING MANUAL REVIEW
- Sample size ready: 62 records (5%)
- Scheduled reviewer: SME name
- Expected review: 2025-11-12 12:00

### Approvals
- Collection validation: ✅ PASS
- Relevancy validation: ⏳ PENDING
- Audit trail: ✅ COMPLETE
- Next step: 03-EXTRACT-YOUTUBE

---
```

---

## CHECKPOINT & RECOVERY

**Every extraction step must support resuming from checkpoint:**

```python
def save_checkpoint(current_position):
    checkpoint = {
        "step": "02-extract-reddit",
        "last_successful_keyword": "garage shelving",
        "last_successful_subreddit": "r/DIY",
        "records_collected_so_far": 847,
        "timestamp": datetime.now().isoformat(),
        "next_action": "Continue with keyword 'organizing garage' in r/HomeImprovement"
    }
    with open('/03-analysis-output/extraction-logs/reddit_checkpoint.json', 'w') as f:
        json.dump(checkpoint, f, indent=2)

def resume_from_checkpoint():
    with open('/03-analysis-output/extraction-logs/reddit_checkpoint.json') as f:
        checkpoint = json.load(f)
    # Resume extraction from saved position
    return checkpoint
```

**If extraction fails mid-way:**
1. Read checkpoint file
2. Verify what was collected
3. Resume from checkpoint (don't re-collect)
4. Append new records to existing file
5. Update manifest and audit log

---

## QUALITY FLAGS SYSTEM

Every record can have quality flags:

```json
{
  "post_id": "abc123",
  "text": "...",
  "quality_flags": [
    "SPAM_SCORE_BORDERLINE: 4.2/10",
    "LATE_EDIT: Last edited 6 months after post",
    "HEAVILY_DOWNVOTED: Score 5 (minimum)"
  ],
  "relevancy_score": null,  // Filled after manual review
  "audit_status": "PENDING_RELEVANCY_CHECK"
}
```

---

## CLIENT AUDIT TRAIL DOCUMENT

Before delivery, create:
`/06-final-deliverables/COMPLETE_AUDIT_TRAIL.md`

This document shows:
1. Every data point → original source URL
2. Collection timestamp → extraction log
3. Quality metrics → validation report
4. Relevancy check → reviewer and date
5. Final usage in deck → slide number and context

**Example:**

```
## Quote #1: "Command hooks left marks on ceiling"

**Original Source:**
- URL: https://reddit.com/r/DIY/comments/154p7e8/...
- Author: WyattTehRobot
- Date: 2023-07-20
- Subreddit: r/DIY

**Extraction Details:**
- Collected: 2025-11-12 10:35:42Z
- Method: PRAW API search "garage hooks"
- File: reddit_posts_raw.json (post_id: xyz789)

**Quality Checks:**
- URL accessible: ✅ Yes (verified 2025-11-12)
- Text length: ✅ 45 characters
- Relevancy: ✅ Score 2/2 (highly relevant)
- Coded as: pain_point="adhesive_failure"

**Usage in Deck:**
- Slide 9: Supporting evidence for adhesive failure claim
- Context: "Multiple consumers report Command hooks failing"
- Verification: Traceable to /06-final-deliverables/quote_verification.csv

**Sign-off:**
- Extraction: analyst_name (2025-11-12 11:15)
- Relevancy: SME_name (2025-11-12 12:30)
- Audit trail: QA_name (2025-11-12 15:00)
```

---

## SUCCESS CRITERIA FOR EACH STEP

### ✅ Step Complete When:

1. **Data Collected**
   - All records have valid structure
   - All required fields present
   - All URLs verified accessible

2. **Manifest Complete**
   - Collection metadata recorded
   - Quality metrics calculated
   - All filters documented
   - Spot check completed

3. **Relevancy Validated**
   - 5% sample reviewed by SME
   - Relevancy score ≥1.5 average
   - Non-relevant records removed
   - Removal reasons logged

4. **Audit Trail Complete**
   - Extraction log written
   - Checkpoint file saved
   - Audit log entry created
   - All approvals obtained

5. **Ready for Next Step**
   - manifest.validation_status = "READY_FOR_ANALYSIS"
   - OR manifest.validation_status = "REQUIRES_REWORK" (with details)

---

## ENFORCEMENT CHECKPOINTS

**These are non-negotiable gates:**

| Gate | Location | Requirement | Failure Action |
|------|----------|-------------|---|
| Pre-Collection | Step 02-04 | Verify scope_definition.json valid | STOP - fix scope |
| During Collection | Step 02-04 | Validate each record in real-time | REJECT invalid record, log reason |
| Post-Collection | Step 02-04 | Manifest complete with metrics | STOP - complete manifest |
| Relevancy Check | After Step 04 | SME reviews 5% sample | REMOVE non-relevant, relog |
| Audit Trail | Step 07 | Trace every data point to source | STOP - add missing URLs |
| Client Delivery | Step 08 | Quote verification complete | REMOVE unverifiable quotes |

---

## SUMMARY

**High relevancy standards require:**

✅ **Self-validating** at collection time (not after)
✅ **Relevancy-checked** before analysis (not assumed)
✅ **Audit trail complete** from original source to deck claim
✅ **Zero unknowns** in chain of custody
✅ **Checkpoints** for recovery if interrupted
✅ **Quality flags** on marginal records
✅ **Complete manifest** on every file
✅ **Removal log** for every excluded record

**Result:** Client can independently verify every insight back to original consumer voice.

---

**Framework Status:** ✅ MANDATORY FOR EXECUTION
**Enforcement Level:** NON-NEGOTIABLE
