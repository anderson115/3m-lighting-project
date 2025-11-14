# CORE DEFINITIONS - SINGLE SOURCE OF TRUTH
## Unified Definitions for All Pipeline Concepts

**Created:** November 12, 2025
**Purpose:** Single authoritative source for all repeated definitions
**Referenced by:** All other framework documents
**Update Authority:** Pipeline architect only

---

## VALIDATION GATES (THE 4 CRITICAL GATES)

### Gate 1: Relevancy Validation Gate
**When:** After each data collection step (02, 03, 04)
**What:** 5% random sample reviewed by SME
**Criteria:** Average relevancy score ≥1.5 (out of 2.0)
**Failure:** Re-collect with refined parameters

### Gate 2: Quality Metrics Gate
**When:** After Step 05 comprehensive validation
**What:** 12-rule validation matrix applied
**Criteria:** All CRITICAL rules must PASS
**Failure:** Fix data in source step, re-extract

### Gate 3: Inter-Rater Reliability Gate
**When:** During Step 06 content analysis
**What:** 10% of coded records verified by second rater
**Criteria:** ≥85% agreement on pain point/behavior coding
**Failure:** Retrain coders, recode sample, re-validate

### Gate 4: Audit Trail Completeness Gate
**When:** Before Step 08 client delivery
**What:** Every claim verified traceable to original source
**Criteria:** 100% of quotes have source URL or are removed
**Failure:** Remove unverifiable claims from deck

---

## RELEVANCY SCORING RUBRIC

### Score 2: Highly Relevant ✅
**Definition:** Directly addresses garage organization with specific, actionable insight
**Characteristics:**
- Directly about garage/storage/organization products
- Specific problem or solution mentioned
- From authenticated consumer with history
- Actionable for product development

**Example:** "Command hooks fell off my wall after 3 months"

**Action:** KEEP, use in analysis, OK to quote

### Score 1: Marginally Relevant ⚠️
**Definition:** Related to topic but lacks specificity or clarity
**Characteristics:**
- Tangentially related to garage organization
- Generic mention without details
- Potentially authentic but unclear intent
- Provides context but not direct evidence

**Example:** "My garage is a mess and I need storage"

**Action:** KEEP for context, flag in removal log, don't quote directly

### Score 0: Not Relevant ❌
**Definition:** Off-topic, spam, or contradicts scope
**Characteristics:**
- Off-topic or clearly off-subject
- Promotional/spam content
- From bot or deleted user
- Wrong product category entirely

**Example:** "Commercial warehouse storage for business"

**Action:** REMOVE, document in removal log with reason

---

## AUDIT TRAIL CHAIN (6 LAYERS)

### Layer 1: Original Source
**Contents:** URL, author, platform, timestamp
**Example:** `https://reddit.com/r/DIY/comments/abc123/`

### Layer 2: Extraction Log
**Contents:** Date/time, method, parameters, filters applied
**Example:** `extraction_log.txt` line 245: "Extracted 2025-11-12 10:35:42Z using PRAW API"

### Layer 3: Raw Data File + Manifest
**Contents:** Complete record with quality metrics
**Example:** `reddit_posts_raw.json` manifest section

### Layer 4: Relevancy Validation
**Contents:** SME review, score, approval
**Example:** `REMOVAL_LOG.json` entry or relevancy sign-off

### Layer 5: Analysis Output
**Contents:** Coded categories, frequency calculated
**Example:** `analysis_output.json` shows "pain_point=adhesive_failure"

### Layer 6: Client Deliverable
**Contents:** COMPLETE_AUDIT_TRAIL.md showing entire chain
**Example:** Client can trace claim backwards to original source URL

---

## QUALITY GATES ENFORCEMENT MATRIX

### Critical Validation Rules (Must PASS)

| Rule | Metric | Pass Threshold | Fail Action |
|------|--------|---|---|
| URLs Valid | 100% records have valid URL | 100% | STOP - investigate API |
| URLs Accessible | Spot check 50 random | 100% http 200 | STOP - verify source |
| Text Quality | >20 characters | 95%+ | OK if 95%+ pass |
| Completeness | All required fields | 99%+ | OK if 99%+ pass |
| No Duplicates | No URL hash duplicates | 100% | STOP - fix dedup |
| Relevancy Score | SME 5% sample review | ≥1.5 average | Re-collect |
| Removal Log | All removals documented | 100% | STOP - complete log |
| Audit Trail | Complete chain present | 100% | STOP - add missing |

---

## MANIFEST SCHEMA (AUTHORITATIVE)

```json
{
  "manifest": {
    "file_metadata": {
      "file_name": "string",
      "file_version": "1.0",
      "created_date": "ISO8601",
      "schema_version": "1.0"
    },

    "extraction": {
      "source_type": "reddit|youtube|products",
      "extraction_date": "ISO8601",
      "extraction_duration_minutes": number,
      "extraction_method": "string",
      "operator_name": "string",
      "api_version": "string"
    },

    "data_collection": {
      "total_attempted": number,
      "total_collected": number,
      "total_rejected": number,
      "collection_rate_percent": number,
      "rejection_breakdown": {
        "reason_name": number,
        "...": "..."
      }
    },

    "quality_metrics": {
      "completeness": {
        "records_with_field": number,
        "percent": number
      },
      "validity": {
        "valid_records": number,
        "invalid_records": number,
        "percent_valid": number
      },
      "spot_check": {
        "sample_size": number,
        "verified_count": number,
        "verification_rate_percent": number
      }
    },

    "relevancy_validation": {
      "status": "PENDING|PASS|FAIL",
      "sample_size": number,
      "average_score": "0.0-2.0",
      "threshold": 1.5,
      "reviewer_name": "string",
      "review_date": "ISO8601",
      "sign_off": boolean,
      "records_removed": number
    },

    "audit_trail": {
      "extraction_log_file": "path",
      "checkpoint_file": "path",
      "removal_log_file": "path",
      "api_calls_made": number,
      "errors_encountered": number
    },

    "validation_status": {
      "collection_validation": "PASS|FAIL",
      "quality_validation": "PASS|FAIL",
      "relevancy_validation": "PASS|FAIL|PENDING",
      "overall_status": "string",
      "next_step": "string"
    }
  }
}
```

---

## REMOVAL LOG SCHEMA (AUTHORITATIVE)

```json
{
  "removal_entry": {
    "removal_id": "removal_001",
    "source_record_id": "string",
    "source_url": "string",
    "removal_reason": {
      "category": "off_topic|spam|bot_account|duplicate|other",
      "description": "string",
      "relevancy_score": "0-2"
    },
    "reviewer_name": "string",
    "review_date": "ISO8601",
    "content_preview": "string (first 100 chars)",
    "removal_timestamp": "ISO8601"
  }
}
```

---

## CHECKPOINT SCHEMA (AUTHORITATIVE)

```json
{
  "checkpoint": {
    "step": "01|02|03|04|05|06|07|08",
    "last_successful_position": "string",
    "records_collected_so_far": number,
    "timestamp": "ISO8601",
    "next_action": "string",
    "recovery_instructions": "string"
  }
}
```

---

## ENFORCEMENT LEVELS

### 🔴 CRITICAL (No exceptions, stops pipeline)
- **Definition:** Process halts, remediation required before proceeding
- **Examples:**
  - All URLs must be valid (100%)
  - No duplicate URLs allowed
  - Relevancy validation must PASS
  - Inter-rater reliability must be ≥85%
  - Audit trail must be 100% complete

### 🟠 HIGH (Document deviation, proceed with caution)
- **Definition:** Process continues but issue logged and reviewed
- **Examples:**
  - Text quality <95% (OK if 95%+ pass)
  - Completeness <99% (OK if 99%+ pass)
  - Price coverage <90% (note as limitation)

### 🟡 MEDIUM (Log and track, proceed normally)
- **Definition:** Issue noted for future improvement
- **Examples:**
  - API rate limit hit (handled with backoff)
  - Minor formatting inconsistencies
  - Non-critical field missing (<5% of records)

---

## APPROVAL SIGN-OFF STANDARD

Every validation step requires sign-off document:

```
VALIDATION SIGN-OFF
═════════════════════════════════════

Dataset: [name]
Validator: [name]
Validation Date: [ISO8601]

Gate 1 - Relevancy:
  Status: PASS / FAIL
  Average Score: [1.5+]
  Reviewer: [name]
  Sign-off: [approved/rejected]

Gate 2 - Quality:
  Status: PASS / FAIL
  Failed Rules: [none or list]
  Sign-off: [approved/rejected]

Gate 3 - Reliability:
  Status: PASS / FAIL
  Agreement Rate: [85%+]
  Sign-off: [approved/rejected]

Gate 4 - Audit Trail:
  Status: PASS / FAIL
  Missing Items: [none or list]
  Sign-off: [approved/rejected]

Overall Status: ✅ APPROVED / ❌ REJECTED
═════════════════════════════════════
```

---

## DOCUMENT REFERENCE CONVENTION

**All other documents reference these definitions using this format:**

```markdown
See [Relevancy Scoring Rubric](CORE_DEFINITIONS.md#relevancy-scoring-rubric)
See [Validation Gates](CORE_DEFINITIONS.md#validation-gates-the-4-critical-gates)
See [Audit Trail Chain](CORE_DEFINITIONS.md#audit-trail-chain-6-layers)
See [Quality Gates Matrix](CORE_DEFINITIONS.md#quality-gates-enforcement-matrix)
```

**Instead of repeating the definitions in each document.**

---

## VERSION CONTROL

**Current Version:** 1.0
**Release Date:** 2025-11-12
**Compatible With:** All pipeline files v1.0
**Breaking Changes:** None (initial version)

**If you update this document:**
1. Increment version (1.0 → 1.1)
2. Document what changed
3. Notify all dependent documents
4. Verify backward compatibility

---

**Status:** ✅ AUTHORITATIVE
**Authority:** Pipeline architect
**Last Updated:** November 12, 2025
**Next Review:** Upon any breaking change
