# REFERENCE SCHEMAS - AUTHORITATIVE JSON DEFINITIONS
## All data structure schemas in one place

**Created:** November 12, 2025
**Purpose:** Single source of truth for all JSON schemas
**Referenced by:** All framework documents
**Status:** Authoritative

---

## DATA FILE SCHEMAS

### 1. scope_definition.json (Output of Step 01)

```json
{
  "pipeline_metadata": {
    "version": "1.0",
    "created_date": "ISO8601",
    "created_by": "analyst_name",
    "purpose": "Define scope parameters for data collection"
  },
  "reddit": {
    "keywords": ["string", "..."],
    "subreddits": ["string", "..."],
    "date_range": {
      "start": "YYYY-MM-DD",
      "end": "YYYY-MM-DD"
    },
    "minimum_score": number,
    "sample_size_target": {
      "posts": "number-number",
      "quality_threshold": "percent%"
    }
  },
  "youtube": {
    "keywords": ["string", "..."],
    "date_range": { "start": "YYYY-MM-DD", "end": "YYYY-MM-DD" },
    "video_duration_seconds": { "min": number, "max": number },
    "minimum_view_count": number,
    "caption_preference": "string",
    "sample_size_target": { "videos": "number-number", "quality_threshold": "percent%" }
  },
  "products": {
    "retailers": {
      "retailer_name": {
        "url": "string",
        "target_count": "number-number"
      }
    },
    "categories": ["string", "..."],
    "data_per_product": ["string", "..."],
    "sample_size_target": { "total_products": "number-number" }
  },
  "analysis": {
    "pain_point_categories": { "category_name": "description" },
    "behavioral_categories": { "category_name": "description" },
    "sample_size_target": { "records_to_code": "number-number" }
  },
  "approval": {
    "status": "PENDING_REVIEW|APPROVED|REJECTED",
    "approved_by": "string|null",
    "approved_date": "ISO8601|null"
  }
}
```

---

### 2. reddit_posts_raw.json (Output of Step 02)

```json
{
  "manifest": {
    "file_name": "reddit_posts_raw.json",
    "extraction_date": "ISO8601",
    "extraction_source": "Reddit PRAW API",
    "total_records": number,
    "completeness": {
      "records_with_urls": number,
      "records_with_text": number,
      "records_with_author": number
    },
    "relevancy_validation": {
      "status": "PENDING|PASS|FAIL",
      "average_score": "0.0-2.0",
      "threshold": 1.5,
      "reviewer_name": "string|null",
      "review_date": "ISO8601|null"
    }
  },
  "posts": [
    {
      "post_id": "string",
      "subreddit": "string",
      "author": "string",
      "title": "string",
      "text": "string",
      "score": number,
      "num_comments": number,
      "url": "string",
      "created_utc": number,
      "is_self": boolean,
      "source": "reddit",
      "extracted_at": "ISO8601",
      "quality_flags": ["string"],
      "relevancy_score": "0|1|2|null",
      "audit_status": "PENDING_RELEVANCY_CHECK|VERIFIED|REMOVED"
    }
  ]
}
```

---

### 3. youtube_videos_raw.json (Output of Step 03)

```json
{
  "manifest": {
    "file_name": "youtube_videos_raw.json",
    "extraction_date": "ISO8601",
    "collection_method": "YouTube API v3",
    "total_records": number,
    "completeness": {
      "records_with_urls": number,
      "records_with_transcripts": number
    },
    "relevancy_validation": {
      "status": "PENDING|PASS|FAIL",
      "average_score": "0.0-2.0",
      "reviewer_name": "string|null"
    }
  },
  "videos": [
    {
      "video_id": "string",
      "title": "string",
      "description": "string",
      "channel_title": "string",
      "channel_id": "string",
      "published_at": "ISO8601",
      "duration_seconds": number,
      "view_count": number,
      "like_count": number,
      "comment_count": number,
      "url": "string",
      "transcript": "string (first 5000 chars)",
      "transcript_source": "manual|auto_generated|unavailable",
      "source": "youtube",
      "extracted_at": "ISO8601",
      "quality_flags": ["string"],
      "relevancy_score": "0|1|2|null",
      "audit_status": "PENDING_RELEVANCY_CHECK|VERIFIED|REMOVED"
    }
  ]
}
```

---

### 4. products_consolidated.json (Output of Step 04)

```json
{
  "manifest": {
    "file_name": "products_consolidated.json",
    "source": "multi_retailer",
    "collection_date": "ISO8601",
    "total_records": number,
    "retailers": {
      "retailer_name": number
    },
    "completeness": {
      "records_with_urls": number,
      "records_with_prices": number,
      "records_with_ratings": number
    },
    "price_metrics": {
      "avg_price": number,
      "min_price": number,
      "max_price": number,
      "price_coverage_percent": number
    }
  },
  "products": [
    {
      "product_name": "string",
      "retailer": "string",
      "url": "string",
      "price": number|null,
      "rating": number|null,
      "review_count": number|null,
      "category": "string",
      "availability": "in_stock|out_of_stock|unknown",
      "extracted_at": "ISO8601",
      "quality_flags": ["string"],
      "relevancy_score": "0|1|2|null",
      "audit_status": "PENDING_RELEVANCY_CHECK|VERIFIED|REMOVED"
    }
  ]
}
```

---

### 5. validation_report.json (Output of Step 05)

```json
{
  "step": "05-VALIDATE-DATA",
  "timestamp": "ISO8601",
  "summary": {
    "total_critical_rules": number,
    "critical_failures": number,
    "overall_status": "PASS|FAIL"
  },
  "validation_results": {
    "reddit_posts": {
      "rule_name": {
        "rule": "string",
        "type": "CRITICAL|MEDIUM",
        "target": number,
        "found": number,
        "pass": boolean
      }
    },
    "youtube_videos": { "...": "..." },
    "products": { "...": "..." }
  },
  "critical_failures": ["string"]
}
```

---

### 6. analysis_output.json (Output of Step 06)

```json
{
  "manifest": {
    "analysis_date": "ISO8601",
    "total_records_coded": number,
    "reddit_records": number,
    "youtube_records": number,
    "methodology": "string",
    "inter_rater_reliability": number
  },
  "frequencies": {
    "reddit": {
      "total_posts": number,
      "pain_points": {
        "category_name": {
          "count": number,
          "percent": number
        }
      },
      "behaviors": {
        "category_name": {
          "count": number,
          "percent": number
        }
      }
    },
    "youtube": {
      "total_videos": number,
      "pain_points": { "...": "..." },
      "behaviors": { "...": "..." }
    }
  },
  "coded_records": [
    {
      "source": "reddit|youtube",
      "id": "string",
      "text_sample": "string",
      "pain_points": {
        "category_name": "0|1"
      },
      "behaviors": {
        "category_name": "0|1"
      },
      "coded_at": "ISO8601"
    }
  ]
}
```

---

### 7. audit_trail.json (Output of Step 07)

```json
{
  "audit_metadata": {
    "creation_date": "ISO8601",
    "created_by": "string",
    "purpose": "Complete audit trail for all insights"
  },
  "data_sources": {
    "reddit_posts": {
      "total_records": number,
      "file": "path",
      "extraction_date": "ISO8601",
      "quality_metrics": {
        "completeness": "percent%",
        "validation_status": "PASS|FAIL"
      }
    },
    "youtube_videos": { "...": "..." },
    "products": { "...": "..." }
  },
  "insight_sources": {
    "insight_identifier": {
      "claim": "string",
      "percentage": number,
      "source": "string",
      "evidence": "string",
      "calculation": "string",
      "data_file": "path",
      "caveats": "string"
    }
  },
  "quotes_verification": {
    "verified_quotes": [
      {
        "quote": "string",
        "source": "reddit|youtube",
        "author": "string",
        "url": "string",
        "date": "YYYY-MM-DD",
        "status": "VERIFIED"
      }
    ],
    "unverifiable_quotes": [
      {
        "quote": "string",
        "claimed_source": "string",
        "status": "UNVERIFIABLE",
        "reason": "string"
      }
    ]
  },
  "validation_status": "COMPLETE",
  "ready_for_client": boolean
}
```

---

### 8. REMOVAL_LOG.json

```json
{
  "removal_log_metadata": {
    "dataset": "string",
    "log_date": "YYYY-MM-DD",
    "total_removals": number,
    "reasons_count": number
  },
  "removals": [
    {
      "removal_id": "removal_001",
      "original_record_id": "string",
      "original_source_url": "string",
      "removal_reason": {
        "category": "off_topic|spam|bot_account|duplicate|other",
        "description": "string",
        "relevancy_score": "0|1|2"
      },
      "reviewer_name": "string",
      "review_date": "ISO8601",
      "original_content_preview": "string (first 100 chars)",
      "removal_timestamp": "ISO8601"
    }
  ],
  "summary": {
    "total_removed": number,
    "removal_breakdown": {
      "reason_name": number
    },
    "retention_rate_percent": number
  }
}
```

---

### 9. checkpoint.json (For recovery)

```json
{
  "checkpoint": {
    "step": "02|03|04|05|06|07|08",
    "last_successful_keyword": "string",
    "last_successful_subreddit": "string",
    "records_collected_so_far": number,
    "timestamp": "ISO8601",
    "next_action": "string"
  }
}
```

---

### 10. QUALITY_METRICS.json (Summary)

```json
{
  "quality_metrics_summary": {
    "collection_date": "YYYY-MM-DD",
    "reddit": {
      "total_attempted": number,
      "total_collected": number,
      "collection_rate_percent": number,
      "quality_metrics": {
        "urls_valid_percent": number,
        "text_quality_percent": number,
        "author_quality_percent": number
      },
      "relevancy_check": {
        "status": "PASS|FAIL|PENDING",
        "sample_size": number,
        "average_score": number,
        "threshold": 1.5,
        "scorer": "string"
      }
    },
    "youtube": { "...": "..." },
    "products": { "...": "..." },
    "overall_status": "READY_FOR_ANALYSIS|REQUIRES_REWORK",
    "date_generated": "ISO8601"
  }
}
```

---

## CSV SCHEMAS

### quote_verification.csv

```csv
quote,deck_usage,source_type,source_id,author,original_url,collection_date,relevancy_check_date,relevancy_score,relevancy_reviewer,analysis_code,final_status,sign_off_date,notes
```

**Example Row:**
```csv
"Command hooks left marks on the ceiling",Slide 9 - Evidence,reddit,post_154p7e8,WyattTehRobot,https://reddit.com/r/DIY/comments/154p7e8/,2025-11-12T10:35:42Z,2025-11-12T12:30:00Z,2,SME_name,pain_point=adhesive_failure,VERIFIED,2025-11-12T15:00:00Z,Direct quote from verified source
```

---

## TEXT LOG SCHEMAS

### extraction.log

```
EXTRACTION LOG: [dataset_name]
═══════════════════════════════════════════════════════════

Extraction Date: [YYYY-MM-DD]
Extraction Start Time: [HH:MM:SS UTC]
Extraction End Time: [HH:MM:SS UTC]
Total Duration: [X] minutes
Extraction Operator: [name]
Script Version: [script_name] v[version]
API Used: [API name] [version]

EXTRACTION PARAMETERS:
─────────────────────
[parameter_name]: [value]
[parameter_name]: [value]

EXECUTION DETAILS:
──────────────────
Total API Calls: [number]
Total Records Attempted: [number]
Total Records Collected: [number]
Collection Rate: [percent]%

QUALITY CHECKS:
───────────────
✅ [check_name]
✅ [check_name]
❌ [check_name (if any)]

ISSUES ENCOUNTERED:
───────────────────
[issue_type]: [count] (handling: [resolution])

OUTPUT FILE:
─────────────
File: [filename]
Size: [size]
Records: [count]
Manifest: ✅ Complete
Checkpoint: ✅ Saved

NEXT STEPS:
───────────
1. [step_name]
2. [step_name]

Status: ✅ COMPLETE AND VERIFIED

═══════════════════════════════════════════════════════════
```

---

## VALIDATION SIGN-OFF FORMAT

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
  Sign-off: APPROVED / REJECTED

Gate 2 - Quality:
  Status: PASS / FAIL
  Failed Rules: [none or list]
  Sign-off: APPROVED / REJECTED

Gate 3 - Reliability:
  Status: PASS / FAIL
  Agreement Rate: [85%+]
  Sign-off: APPROVED / REJECTED

Gate 4 - Audit Trail:
  Status: PASS / FAIL
  Missing Items: [none or list]
  Sign-off: APPROVED / REJECTED

Overall Status: ✅ APPROVED / ❌ REJECTED

═════════════════════════════════════
```

---

## VERSION INFORMATION

**Schema Version:** 1.0
**Release Date:** 2025-11-12
**Compatibility:** All pipeline v1.0 files

**If you add a new field:**
- Update schema here
- Increment version number
- Document breaking changes
- Notify all dependent documents

---

**Status:** ✅ AUTHORITATIVE REFERENCE
**Last Updated:** November 12, 2025
**Reference These Instead Of:** Embedded examples in other files
