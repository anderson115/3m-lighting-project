# STEP 05: VALIDATE ALL DATA
## Garage Organizer Data Collection Pipeline

**Process:** Data validation
**Input:** reddit_posts_raw.json, youtube_videos_raw.json, products_consolidated.json
**Output:** validation_report.json, data_quality_summary.json
**Time:** 30 minutes
**Validation:** Comprehensive 12-rule validation matrix

---

## PURPOSE

Run comprehensive validation across ALL extracted data. Stop here if ANY critical rule fails. Do not proceed to analysis with bad data.

---

## PROCEDURE

### 1. Validation Rules Matrix

Create file: `/03-analysis-output/VALIDATION_RULES.json`

```json
{
  "reddit_posts": {
    "rule_1_urls_100_percent": {
      "rule": "All posts must have URL",
      "type": "CRITICAL",
      "target_percent": 100,
      "action_if_fail": "STOP - Investigate API response"
    },
    "rule_2_text_quality_95_percent": {
      "rule": "95%+ posts have text >20 characters",
      "type": "CRITICAL",
      "target_percent": 95,
      "action_if_fail": "Flag short posts, review"
    },
    "rule_3_authors_not_deleted": {
      "rule": "99%+ have non-deleted authors",
      "type": "MEDIUM",
      "target_percent": 99,
      "action_if_fail": "Log deleted authors, continue"
    },
    "rule_4_no_duplicates": {
      "rule": "No URL duplicates",
      "type": "CRITICAL",
      "target_percent": 100,
      "action_if_fail": "STOP - Review deduplication"
    }
  },
  "youtube_videos": {
    "rule_5_urls_100_percent": {
      "rule": "All videos have URL",
      "type": "CRITICAL",
      "target_percent": 100,
      "action_if_fail": "STOP"
    },
    "rule_6_transcripts_available": {
      "rule": "90%+ have usable transcripts",
      "type": "CRITICAL",
      "target_percent": 90,
      "action_if_fail": "STOP - Check YouTube captions"
    },
    "rule_7_view_counts_valid": {
      "rule": "All have view_count >100",
      "type": "CRITICAL",
      "target_percent": 100,
      "action_if_fail": "Remove low-view videos"
    }
  },
  "products": {
    "rule_8_urls_complete": {
      "rule": "100% have URL",
      "type": "CRITICAL",
      "target_percent": 100,
      "action_if_fail": "STOP"
    },
    "rule_9_prices_coverage": {
      "rule": "90%+ have prices",
      "type": "CRITICAL",
      "target_percent": 90,
      "action_if_fail": "OK if shortage, note limitation"
    },
    "rule_10_no_duplicates": {
      "rule": "No URL duplicates",
      "type": "CRITICAL",
      "target_percent": 100,
      "action_if_fail": "STOP - Review deduplication"
    },
    "rule_11_retailers_labeled": {
      "rule": "100% have retailer label",
      "type": "CRITICAL",
      "target_percent": 100,
      "action_if_fail": "STOP"
    },
    "rule_12_prices_reasonable": {
      "rule": "Price range $0-$10,000 (no outliers)",
      "type": "MEDIUM",
      "action_if_fail": "Flag and investigate outliers"
    }
  }
}
```

### 2. Validation Script

**Script: `validate_data.py`**

```python
#!/usr/bin/env python3
"""
Comprehensive data validation across all extracted sources.
"""

import json
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler('/03-analysis-output/extraction-logs/validation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load all extracted data
with open('/01-raw-data/reddit_posts_raw.json') as f:
    reddit_data = json.load(f)
    reddit_posts = reddit_data['posts']

with open('/01-raw-data/youtube_videos_raw.json') as f:
    youtube_data = json.load(f)
    youtube_videos = youtube_data['videos']

with open('/01-raw-data/products_consolidated.json') as f:
    products_data = json.load(f)
    products = products_data['products']

logger.info(f"Loaded {len(reddit_posts)} Reddit posts")
logger.info(f"Loaded {len(youtube_videos)} YouTube videos")
logger.info(f"Loaded {len(products)} products")

# Run validations
validation_results = {
    "timestamp": datetime.now().isoformat(),
    "summary": {},
    "reddit_posts": {},
    "youtube_videos": {},
    "products": {},
    "critical_failures": []
}

# REDDIT VALIDATIONS
logger.info("Validating Reddit posts...")

# Rule 1: All have URLs
urls_count = sum(1 for p in reddit_posts if p.get('url'))
rule_1 = {
    "rule": "All posts must have URL",
    "type": "CRITICAL",
    "target": 100,
    "found": (urls_count / len(reddit_posts) * 100) if reddit_posts else 0,
    "pass": urls_count == len(reddit_posts)
}
validation_results['reddit_posts']['rule_1_urls'] = rule_1
if not rule_1['pass']:
    validation_results['critical_failures'].append(f"Reddit Rule 1 FAILED: {urls_count}/{len(reddit_posts)} have URLs")

# Rule 2: 95%+ have meaningful text
text_quality = sum(1 for p in reddit_posts if len(p.get('text', '')) > 20)
rule_2 = {
    "rule": "95%+ posts have text >20 chars",
    "type": "CRITICAL",
    "target": 95,
    "found": (text_quality / len(reddit_posts) * 100) if reddit_posts else 0,
    "pass": (text_quality / len(reddit_posts)) >= 0.95 if reddit_posts else False
}
validation_results['reddit_posts']['rule_2_text_quality'] = rule_2
if not rule_2['pass']:
    validation_results['critical_failures'].append(f"Reddit Rule 2 FAILED: Only {rule_2['found']:.1f}% have quality text")

# Rule 3: 99%+ non-deleted authors
authors_count = sum(1 for p in reddit_posts if p.get('author') != "[deleted]")
rule_3 = {
    "rule": "99%+ have non-deleted authors",
    "type": "MEDIUM",
    "target": 99,
    "found": (authors_count / len(reddit_posts) * 100) if reddit_posts else 0,
    "pass": (authors_count / len(reddit_posts)) >= 0.99 if reddit_posts else False
}
validation_results['reddit_posts']['rule_3_authors'] = rule_3

# Rule 4: No duplicates
unique_urls = len(set(p.get('url') for p in reddit_posts))
rule_4 = {
    "rule": "No URL duplicates",
    "type": "CRITICAL",
    "target": len(reddit_posts),
    "found": unique_urls,
    "pass": unique_urls == len(reddit_posts)
}
validation_results['reddit_posts']['rule_4_no_duplicates'] = rule_4
if not rule_4['pass']:
    validation_results['critical_failures'].append(f"Reddit Rule 4 FAILED: {len(reddit_posts) - unique_urls} duplicates found")

# YOUTUBE VALIDATIONS
logger.info("Validating YouTube videos...")

# Rule 5: All have URLs
yt_urls = sum(1 for v in youtube_videos if v.get('url'))
rule_5 = {
    "rule": "All videos have URL",
    "type": "CRITICAL",
    "target": 100,
    "found": (yt_urls / len(youtube_videos) * 100) if youtube_videos else 0,
    "pass": yt_urls == len(youtube_videos)
}
validation_results['youtube_videos']['rule_5_urls'] = rule_5
if not rule_5['pass']:
    validation_results['critical_failures'].append(f"YouTube Rule 5 FAILED")

# Rule 6: 90%+ have transcripts
transcripts = sum(1 for v in youtube_videos if v.get('transcript'))
rule_6 = {
    "rule": "90%+ have usable transcripts",
    "type": "CRITICAL",
    "target": 90,
    "found": (transcripts / len(youtube_videos) * 100) if youtube_videos else 0,
    "pass": (transcripts / len(youtube_videos)) >= 0.90 if youtube_videos else False
}
validation_results['youtube_videos']['rule_6_transcripts'] = rule_6
if not rule_6['pass']:
    validation_results['critical_failures'].append(f"YouTube Rule 6 FAILED: Only {rule_6['found']:.1f}% have transcripts")

# Rule 7: All have >100 views
min_views = min((v.get('view_count', 0) for v in youtube_videos), default=0)
rule_7 = {
    "rule": "All have view_count >100",
    "type": "CRITICAL",
    "target": 100,
    "found": min_views,
    "pass": all(v.get('view_count', 0) >= 100 for v in youtube_videos)
}
validation_results['youtube_videos']['rule_7_view_counts'] = rule_7
if not rule_7['pass']:
    validation_results['critical_failures'].append(f"YouTube Rule 7 FAILED: Min views = {min_views}")

# PRODUCT VALIDATIONS
logger.info("Validating products...")

# Rule 8: All have URLs
prod_urls = sum(1 for p in products if p.get('url'))
rule_8 = {
    "rule": "100% have URL",
    "type": "CRITICAL",
    "target": 100,
    "found": (prod_urls / len(products) * 100) if products else 0,
    "pass": prod_urls == len(products)
}
validation_results['products']['rule_8_urls'] = rule_8
if not rule_8['pass']:
    validation_results['critical_failures'].append(f"Products Rule 8 FAILED")

# Rule 9: 90%+ have prices
prices = sum(1 for p in products if p.get('price'))
rule_9 = {
    "rule": "90%+ have prices",
    "type": "CRITICAL",
    "target": 90,
    "found": (prices / len(products) * 100) if products else 0,
    "pass": (prices / len(products)) >= 0.90 if products else False
}
validation_results['products']['rule_9_prices'] = rule_9

# Rule 10: No duplicates
unique_prod_urls = len(set(p.get('url') for p in products))
rule_10 = {
    "rule": "No URL duplicates",
    "type": "CRITICAL",
    "target": len(products),
    "found": unique_prod_urls,
    "pass": unique_prod_urls == len(products)
}
validation_results['products']['rule_10_no_duplicates'] = rule_10
if not rule_10['pass']:
    validation_results['critical_failures'].append(f"Products Rule 10 FAILED: {len(products) - unique_prod_urls} duplicates")

# Rule 11: All have retailer
retailers = sum(1 for p in products if p.get('retailer'))
rule_11 = {
    "rule": "100% have retailer label",
    "type": "CRITICAL",
    "target": 100,
    "found": (retailers / len(products) * 100) if products else 0,
    "pass": retailers == len(products)
}
validation_results['products']['rule_11_retailers'] = rule_11
if not rule_11['pass']:
    validation_results['critical_failures'].append(f"Products Rule 11 FAILED")

# Rule 12: Price outliers
try:
    prod_prices = [float(str(p.get('price', 0)).replace('$', '')) for p in products if p.get('price')]
    min_price = min(prod_prices) if prod_prices else 0
    max_price = max(prod_prices) if prod_prices else 0
    rule_12 = {
        "rule": "Price range $0-$10,000",
        "type": "MEDIUM",
        "min": min_price,
        "max": max_price,
        "pass": min_price >= 0 and max_price <= 10000
    }
except:
    rule_12 = {"rule": "Price range check", "pass": False, "error": "Price parsing failed"}

validation_results['products']['rule_12_prices_reasonable'] = rule_12

# Summary
validation_results['summary'] = {
    "total_critical_rules": 11,
    "critical_failures": len(validation_results['critical_failures']),
    "overall_status": "PASS" if len(validation_results['critical_failures']) == 0 else "FAIL"
}

# Write reports
with open('/03-analysis-output/validation_report.json', 'w') as f:
    json.dump(validation_results, f, indent=2)

logger.info(f"Validation complete: {validation_results['summary']['overall_status']}")

if validation_results['critical_failures']:
    logger.error(f"CRITICAL FAILURES: {len(validation_results['critical_failures'])}")
    for failure in validation_results['critical_failures']:
        logger.error(f"  - {failure}")
    raise Exception(f"Data validation failed: {len(validation_results['critical_failures'])} critical rules failed")
else:
    logger.info("All validation rules PASSED")
```

### 3. Execute Validation

```bash
python3 validate_data.py
```

### 4. Review Validation Report

```bash
cat /03-analysis-output/validation_report.json
```

---

## VALIDATION REPORT OUTPUT

```json
{
  "timestamp": "2025-11-12T13:00:00",
  "summary": {
    "total_critical_rules": 11,
    "critical_failures": 0,
    "overall_status": "PASS"
  },
  "reddit_posts": {
    "rule_1_urls": {
      "rule": "All posts must have URL",
      "type": "CRITICAL",
      "target": 100,
      "found": 100,
      "pass": true
    }
  },
  "critical_failures": []
}
```

---

## IF VALIDATION FAILS

**Stop immediately. Do NOT proceed to analysis.**

For EACH critical failure:

1. Identify which rule failed
2. Read that rule's "action_if_fail" instruction
3. Follow the remediation steps
4. Re-run validation_data.py
5. Verify all critical rules PASS before proceeding

**Common failures and fixes:**

| Failure | Cause | Fix |
|---------|-------|-----|
| "Only 95% have URLs" | API missing URL field | Investigate API response format |
| "Only 80% have transcripts" | YouTube videos have no captions | Filter to only caption-enabled videos |
| "Found 150 duplicates" | Deduplication not working | Review duplicate detection logic |

---

## SUCCESS CRITERIA

✅ **This step succeeds when:**
```json
{
  "overall_status": "PASS",
  "critical_failures": 0,
  "all_rules": "PASSED"
}
```

❌ **This step FAILS when:**
- ANY critical rule shows "pass": false
- Any critical_failures list is non-empty

---

## NEXT STEP

**If PASS:** Proceed to `06-ANALYZE-CONTENT.md`

**If FAIL:**
1. Read failure message
2. Identify problematic source (Reddit, YouTube, or Products)
3. Go back to extraction step for that source
4. Fix data
5. Re-run validation

---

**Status:** READY
**Last Updated:** November 12, 2025
