# COMPLETE AUDIT TRAIL SPECIFICATION
## Every Data Point Traceable to Original Source

**Created:** November 12, 2025
**Purpose:** Enable client to independently verify every insight
**Requirement Level:** MANDATORY - No exceptions

---

## AUDIT TRAIL ARCHITECTURE

Every data point follows this chain:

```
ORIGINAL SOURCE
    ↓ (collection method documented)
EXTRACTION LOG
    ↓ (timestamp, parameters, filters)
RAW DATA FILE + MANIFEST
    ↓ (quality metrics, completeness)
RELEVANCY VALIDATION
    ↓ (SME review, score, removal log)
ANALYSIS OUTPUT
    ↓ (coded, frequency calculated)
FINAL INSIGHT / QUOTE
    ↓ (used in deck or removed)
CLIENT DELIVERABLE + AUDIT TRAIL
```

**At ANY point, client must be able to say:**
"Show me the original source for this claim"
**And we provide:** Complete chain with timestamps and verification

---

## LAYER 1: ORIGINAL SOURCE DOCUMENTATION

### For Reddit Posts

**Every Reddit post record MUST include:**

```json
{
  "post_id": "154p7e8",
  "source_url": "https://www.reddit.com/r/DIY/comments/154p7e8/...",
  "subreddit": "r/DIY",
  "author": "WyattTehRobot",
  "author_profile_url": "https://www.reddit.com/user/WyattTehRobot",
  "posted_timestamp": "2023-07-20T14:32:00Z",
  "title": "Command hooks left marks on ceiling - help!",
  "text": "I installed Command hooks to hang a heavy shelf...",

  "source_verification": {
    "url_accessible": true,
    "url_checked_date": "2025-11-12T10:35:42Z",
    "url_http_status": 200,
    "content_matches_extract": true,
    "archived": false
  }
}
```

### For YouTube Videos

**Every YouTube video record MUST include:**

```json
{
  "video_id": "zDzwhtRtMxA",
  "source_url": "https://www.youtube.com/watch?v=zDzwhtRtMxA",
  "channel_id": "UCxxxxxx",
  "channel_name": "DIY Channel Name",
  "channel_url": "https://www.youtube.com/c/...",
  "published_timestamp": "2023-04-27T10:00:00Z",
  "title": "REIBII 72\" Heavy Duty Garage Storage Shelves",
  "description": "...",
  "transcript": "...",
  "transcript_language": "en",
  "transcript_type": "auto-generated",

  "source_verification": {
    "url_accessible": true,
    "url_checked_date": "2025-11-12T11:45:00Z",
    "url_http_status": 200,
    "transcript_available": true,
    "transcript_quality": "good"
  }
}
```

### For Products

**Every product record MUST include:**

```json
{
  "product_id": "B087HQPH7Z",
  "product_name": "3M Claw Garage Hook",
  "source_url": "https://www.amazon.com/dp/B087HQPH7Z",
  "retailer": "amazon",
  "retailer_sku": "B087HQPH7Z",
  "price": 12.99,
  "rating": 4.2,
  "review_count": 1847,
  "category": "Hooks and Hangers",

  "source_verification": {
    "url_accessible": true,
    "url_checked_date": "2025-11-12T13:20:00Z",
    "url_http_status": 200,
    "current_availability": "in_stock",
    "price_checked_date": "2025-11-12T13:20:00Z"
  }
}
```

---

## LAYER 2: EXTRACTION LOG DOCUMENTATION

**For each extraction step, create detailed log:**

`/03-analysis-output/extraction-logs/[SOURCE]_extraction.log`

**Format:**

```
EXTRACTION LOG: reddit_posts_raw.json
═══════════════════════════════════════════════════════════

Extraction Date: 2025-11-12
Extraction Start Time: 10:30:00 UTC
Extraction End Time: 11:15:00 UTC
Total Duration: 45 minutes
Extraction Operator: [analyst_name]
Script Version: extract_reddit.py v1.0
API Used: PRAW v7.7.0

EXTRACTION PARAMETERS (from scope_definition.json):
─────────────────────────────────────────────────
Keywords Used: 10 keywords
  1. "garage organization"
  2. "garage storage"
  3. "garage shelving"
  ... (all 10 listed)

Subreddits Searched: 5 subreddits
  1. r/DIY (searched 2 times)
  2. r/HomeImprovement (searched 2 times)
  3. r/organization (searched 2 times)
  4. r/organizing (searched 2 times)
  5. r/InteriorDesign (searched 2 times)

Date Range: 2023-01-01 to 2025-11-12
Minimum Score: 5 upvotes
Minimum Text Length: 20 characters
Maximum Results Per Keyword: 100

EXECUTION DETAILS:
─────────────────
Total API Calls: 50
Total Records Attempted: 2,847
Total Records Collected: 1,247
Collection Rate: 43.8%

REJECTION BREAKDOWN:
─────────────────────
Below minimum score (5): 800 records
Post text too short (<20 chars): 450 records
Outside date range: 250 records
Duplicate URLs: 100 records
Total Rejected: 1,600 records

QUALITY CHECKS (during collection):
───────────────────────────────────
✅ All 1,247 records have valid URLs
✅ 1,235 records (98.9%) have text >20 characters
✅ 1,240 records (99.4%) have non-deleted authors
✅ 0 duplicate URL hashes detected
✅ All timestamps within specified range
✅ All subreddits match search targets

API ERRORS/ISSUES:
──────────────────
2 API rate limit hits (handled with backoff: 2 second delay)
5 connection timeouts (retried, all successful)
0 authentication errors
0 data corruption detected

CHECKPOINT MANAGEMENT:
──────────────────────
Checkpoint file: /03-analysis-output/extraction-logs/reddit_checkpoint.json
Checkpoint saves: 5 (every 250 records)
Resumable from: Last checkpoint (would resume at keyword "garage racks")

OUTPUT FILE:
─────────────
File: reddit_posts_raw.json
File Size: 4.2 MB
Records in File: 1,247
Manifest Included: YES (complete)
Manifest Verification: Passed

SPOT CHECK (verification of 50 random records):
────────────────────────────────────────────────
Sample Method: Random stratified by subreddit
Sample Size: 50 records
Verification Date: 2025-11-12 11:16:00 UTC
Verification Method: Manual URL access and content verification

Results:
  ✅ All 50 URLs accessible (HTTP 200)
  ✅ All 50 from correct subreddit
  ✅ All 50 timestamps within range
  ✅ All 50 have meaningful content
  ✅ All 50 mention garage/storage/organization context

Spot Check Status: PASS

NEXT STEPS:
────────────
1. Relevancy validation (5% sample review by SME)
2. Integration with youtube and products data
3. Proceed to Step 05: Validate All Data

Extraction Status: ✅ COMPLETE AND VERIFIED
Audit Trail: ✅ COMPLETE
Next Step: 03-EXTRACT-YOUTUBE

═══════════════════════════════════════════════════════════
```

---

## LAYER 3: MANIFEST + METADATA

**Every data file includes complete manifest:**

```json
{
  "manifest": {
    "file_name": "reddit_posts_raw.json",
    "file_version": "1.0",
    "file_created_date": "2025-11-12",

    "data_source": {
      "source_type": "reddit",
      "data_acquisition_method": "PRAW API search",
      "api_version": "PRAW v7.7.0",
      "search_scope": "Reference scope_definition.json (SHA256: abc123...)"
    },

    "extraction_metadata": {
      "extraction_start_time": "2025-11-12T10:30:00Z",
      "extraction_end_time": "2025-11-12T11:15:00Z",
      "extraction_duration_minutes": 45,
      "operator_name": "analyst_name",
      "operator_contact": "email@example.com"
    },

    "data_collection_stats": {
      "total_attempted": 2847,
      "total_collected": 1247,
      "total_rejected": 1600,
      "collection_efficiency_percent": 43.8,

      "rejection_breakdown": {
        "below_minimum_score": 800,
        "text_too_short": 450,
        "outside_date_range": 250,
        "duplicate_urls": 100
      },

      "filters_applied": [
        "score >= 5",
        "text_length >= 20",
        "created_date >= 2023-01-01",
        "created_date <= 2025-11-12",
        "no_duplicate_urls"
      ]
    },

    "data_quality_metrics": {
      "completeness": {
        "records_with_urls": {
          "count": 1247,
          "percent": 100.0
        },
        "records_with_text": {
          "count": 1235,
          "percent": 98.9
        },
        "records_with_author": {
          "count": 1240,
          "percent": 99.4
        },
        "records_with_timestamp": {
          "count": 1247,
          "percent": 100.0
        }
      },

      "data_validity": {
        "url_validity": {
          "valid": 1247,
          "invalid": 0,
          "percent_valid": 100.0
        },
        "timestamp_validity": {
          "in_range": 1247,
          "out_of_range": 0,
          "percent_valid": 100.0
        },
        "duplicate_check": {
          "unique_urls": 1247,
          "duplicates_found": 0,
          "percent_unique": 100.0
        }
      },

      "spot_check": {
        "sample_size": 50,
        "sample_date": "2025-11-12T11:16:00Z",
        "sample_method": "random stratified by subreddit",
        "verification_results": {
          "urls_accessible": 50,
          "urls_inaccessible": 0,
          "content_matches": 50,
          "content_mismatch": 0,
          "percent_verified": 100.0
        }
      }
    },

    "relevancy_validation": {
      "status": "PENDING_MANUAL_REVIEW",
      "review_scheduled_date": "2025-11-12T12:00:00Z",
      "sample_size": 62,
      "sample_method": "5% stratified random",
      "review_criteria_document": "RELEVANCY_STANDARDS.md",

      "review_results": {
        "status": null,  // Filled after review
        "average_score": null,
        "threshold": 1.5,
        "pass": null,
        "reviewer_name": null,
        "review_date": null,
        "review_signature": null
      }
    },

    "audit_trail": {
      "extraction_log_file": "/03-analysis-output/extraction-logs/reddit_extraction.log",
      "checkpoint_file": "/03-analysis-output/extraction-logs/reddit_checkpoint.json",
      "removal_log_file": "/03-analysis-output/extraction-logs/REMOVAL_LOG.json",

      "api_calls": {
        "total_calls": 50,
        "rate_limit_hits": 2,
        "timeouts": 5,
        "errors": 0
      },

      "data_lineage": {
        "original_source": "reddit.com",
        "extraction_method": "PRAW API",
        "extraction_date": "2025-11-12",
        "extraction_parameters": "scope_definition.json v1.0",
        "transformations_applied": [
          "URL validation",
          "Text length validation",
          "Timestamp range filtering",
          "Duplicate removal"
        ]
      }
    },

    "validation_status": {
      "collection_validation": "PASS",
      "quality_metrics_validation": "PASS",
      "audit_trail_complete": "PASS",
      "relevancy_validation": "PENDING",
      "overall_status": "READY_FOR_RELEVANCY_CHECK",
      "approval_gate": "Manual relevancy review required before proceeding"
    },

    "next_steps": [
      "1. SME performs 5% sample relevancy review",
      "2. Remove any Score 0 records",
      "3. Update manifest with relevancy_validation.review_results",
      "4. Proceed to Step 03: EXTRACT-YOUTUBE"
    ]
  },

  "records": [
    {
      "post_id": "abc123",
      "source_url": "https://reddit.com/r/DIY/comments/abc123/...",
      "... all fields ..."
    }
  ]
}
```

---

## LAYER 4: REMOVAL LOG

**Every removed record documented:**

`/03-analysis-output/extraction-logs/REMOVAL_LOG.json`

```json
{
  "removal_log_metadata": {
    "dataset": "reddit_posts_raw.json",
    "log_date": "2025-11-12",
    "total_removals": 15,  // From relevancy review, not collection
    "reasons_count": 4
  },

  "removals": [
    {
      "removal_id": "removal_001",
      "original_post_id": "xyz789",
      "original_source_url": "https://reddit.com/r/DIY/comments/xyz789/",
      "original_subreddit": "r/DIY",
      "original_title": "Commercial warehouse storage solutions",

      "removal_reason": {
        "category": "off_topic",
        "description": "Focuses on commercial warehouse storage, not residential garage",
        "relevancy_score": 0,
        "relevancy_reviewer": "SME_name",
        "review_date": "2025-11-12T12:30:00Z"
      },

      "original_content_preview": "Looking for commercial-grade storage for my warehouse...",

      "removal_documentation": {
        "removal_timestamp": "2025-11-12T12:45:00Z",
        "removal_approved_by": "SME_name",
        "audit_trail_entry": "AUDIT_LOG.md line 245"
      }
    },

    {
      "removal_id": "removal_002",
      "original_post_id": "abc456",
      "original_source_url": "https://reddit.com/r/DIY/comments/abc456/",

      "removal_reason": {
        "category": "spam",
        "description": "Promotional content - brand trying to sell product",
        "relevancy_score": 0,
        "relevancy_reviewer": "SME_name",
        "review_date": "2025-11-12T12:35:00Z"
      },

      "original_content_preview": "Check out [BRANDED PRODUCT] - Buy now with code SAVE20...",
      "removal_timestamp": "2025-11-12T12:45:30Z"
    }
  ],

  "summary": {
    "total_removed": 15,
    "removal_breakdown": {
      "off_topic": 8,
      "spam": 4,
      "bot_account": 2,
      "duplicate_content": 1
    },
    "records_remaining": 1232,
    "retention_rate_percent": 98.8
  }
}
```

---

## LAYER 5: ANALYSIS → QUOTE MAPPING

**Every quote traced back to analysis:**

`/06-final-deliverables/quote_verification.csv`

```csv
quote,deck_usage,source_type,source_id,author,original_url,collection_date,relevancy_check_date,relevancy_score,relevancy_reviewer,analysis_code,analysis_frequency,final_status,sign_off_date,notes

"Command hooks left marks on the ceiling",Slide 9 - Evidence,reddit,post_154p7e8,WyattTehRobot,https://reddit.com/r/DIY/comments/154p7e8/,2025-11-12T10:35:42Z,2025-11-12T12:30:00Z,2,SME_name,pain_point=adhesive_failure,15.2% of Reddit posts,VERIFIED,2025-11-12T15:00:00Z,Direct quote from verified source

"3M Command large 5lb Hooks fell with Ikea curtain",Slide 9 - Evidence,reddit,post_890xyz,simochiology,https://reddit.com/r/DIY/comments/890xyz/,2025-11-12T10:40:15Z,2025-11-12T12:31:00Z,2,SME_name,pain_point=adhesive_failure,15.2% of Reddit posts,VERIFIED,2025-11-12T15:00:00Z,Supports adhesive failure theme

"The Scotch hooks I installed in my garage worked great",N/A,unknown,unknown,unknown,unknown,N/A,N/A,0,SME_name,N/A,N/A,UNVERIFIABLE,2025-11-12T15:00:00Z,"Scotch doesn't make hooks - removed from deck"
```

---

## LAYER 6: FINAL AUDIT TRAIL DOCUMENT

**Delivered to client:**

`/06-final-deliverables/COMPLETE_AUDIT_TRAIL.md`

For each insight in the deck, provide:

```markdown
### Insight: "Installation difficulty is a top concern (25%)"

**Source Chain:**

1. **Original Data Sources**
   - Reddit posts: 312 of 1247 mention installation difficulty/complexity
   - YouTube videos: 18 of 78 discuss installation challenges
   - Source verification: URLs accessible, content verified

2. **Collection Method**
   - Extraction date: 2025-11-12
   - Extraction log: /03-analysis-output/extraction-logs/reddit_extraction.log
   - Keywords used: "garage shelving", "installation", "install difficulty"
   - Filters applied: score>=5, text length>=20

3. **Quality Assurance**
   - Relevancy check: PASS (avg score 1.92/2.0)
   - Sample verified: 50 random records, 100% accessible
   - Removed records: 15 off-topic (logged in REMOVAL_LOG.json)

4. **Analysis**
   - Coding method: Keyword pattern matching
   - Pattern examples: "hard to install", "took hours", "need help"
   - Inter-rater reliability: 87.2% (>=85% required)

5. **Supporting Quotes**
   - Quote 1: "Just spent 6 hours installing..." (post_abc123)
     - URL: https://reddit.com/r/DIY/comments/...
     - Relevancy: 2/2 (verified authentic consumer)
   - Quote 2: "Instructions were unclear..." (video_xyz789)
     - URL: https://youtube.com/watch?v=...
     - Relevancy: 2/2 (verified authentic channel)

6. **Verification Trail**
   - Data collected: 2025-11-12 11:15 UTC
   - Relevancy reviewed: 2025-11-12 12:30 UTC
   - Analysis completed: 2025-11-12 15:00 UTC
   - Client delivered: 2025-11-13 09:00 UTC

**Client Can Verify By:**
- Opening reddit_posts_raw.json, search for post_abc123
- Following source_url to original Reddit post
- Reviewing RELEVANCY_STANDARDS.md for scoring methodology
- Checking REMOVAL_LOG.json for removed posts and why
```

---

## AUDIT TRAIL CHECKLIST

Before client delivery, verify:

- [ ] Every record has original source URL
- [ ] Every URL verified accessible (status 200)
- [ ] Extraction log complete with all parameters
- [ ] Manifest in every data file with all required fields
- [ ] Removal log complete with reasons for all removals
- [ ] Relevancy check completed by SME with sign-off
- [ ] Every quote in deck has source URL documented
- [ ] Every percentage has visible calculation
- [ ] COMPLETE_AUDIT_TRAIL.md links all layers together
- [ ] Client can independently verify any claim
- [ ] No missing links in chain

---

## AUDIT TRAIL TOOL

Create script to verify audit trail completeness:

```python
def verify_audit_trail_complete():
    """
    Automated check that all audit layers are present and complete.
    """

    checks = {
        "raw_data_has_source_urls": verify_all_source_urls_present(),
        "extraction_log_exists": os.path.exists("extraction.log"),
        "manifest_complete": verify_manifest_fields(),
        "removal_log_present": os.path.exists("removal_log.json"),
        "relevancy_signed_off": verify_relevancy_sign_off(),
        "quote_verification_complete": verify_all_quotes_sourced(),
        "final_audit_trail_doc": os.path.exists("COMPLETE_AUDIT_TRAIL.md")
    }

    if all(checks.values()):
        return "PASS - Audit trail complete"
    else:
        failures = [k for k, v in checks.items() if not v]
        return f"FAIL - Missing: {failures}"
```

---

## CLIENT VERIFICATION PROCEDURE

Provide client with:

1. **COMPLETE_AUDIT_TRAIL.md** - Full chain for every insight
2. **quote_verification.csv** - All quotes with source URLs
3. **extraction-logs/ folder** - All extraction logs and removal logs
4. **Raw data files** - Full datasets with manifests
5. **RELEVANCY_STANDARDS.md** - How data was validated
6. **VALIDATION_FRAMEWORK.md** - Quality assurance process

**Client can then:**
```
1. Pick any insight from the deck
2. Find it in COMPLETE_AUDIT_TRAIL.md
3. Follow URL to original source
4. Verify authenticity independently
5. Check relevancy methodology
6. Review manifest and metrics
```

---

**Audit Trail Status:** ✅ SPECIFICATION COMPLETE
**Implementation Level:** MANDATORY - NO EXCEPTIONS
**Client Transparency:** COMPLETE
