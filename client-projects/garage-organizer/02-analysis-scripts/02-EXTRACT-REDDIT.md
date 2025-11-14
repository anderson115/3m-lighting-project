# STEP 02: EXTRACT REDDIT POSTS
## Garage Organizer Data Collection Pipeline

**Process:** Data extraction
**Input:** `scope_definition.json`
**Output:** `reddit_posts_raw.json`
**Time:** 45 minutes
**Validation:** Format, URLs, deduplication

---

## PURPOSE

Extract Reddit posts matching scope parameters. Reddit is primary source for consumer pain points (problem-seeking community).

---

## INPUTS REQUIRED

- `scope_definition.json` (from Step 01)
- Reddit API credentials configured
- PRAW library installed (`pip install praw`)

---

## PROCEDURE

### 1. Verify Prerequisites

```bash
# Check PRAW installed
python3 -c "import praw; print('PRAW ready')"

# Verify scope definition exists
test -f /01-raw-data/scope_definition.json && echo "Scope file found"

# Create output directory
mkdir -p /03-analysis-output/extraction-logs/
```

### 2. Configure Reddit API

You need:
- Reddit app credentials (client_id, client_secret, user_agent)
- These should be in environment variables or config file

**Create `reddit_config.json` (one-time setup):**
```json
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "user_agent": "GarageOrganizerBot/1.0",
  "username": "YOUR_USERNAME",
  "password": "YOUR_PASSWORD"
}
```

### 3. Run Extraction Script

**Script: `extract_reddit.py`**

```python
#!/usr/bin/env python3
"""
Extract Reddit posts matching garage organizer criteria.
Inputs: scope_definition.json, reddit_config.json
Outputs: reddit_posts_raw.json, reddit_extraction.log
"""

import json
import praw
import logging
from datetime import datetime
from collections import defaultdict
import hashlib

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/03-analysis-output/extraction-logs/reddit_extraction.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load configurations
with open('/01-raw-data/scope_definition.json') as f:
    scope = json.load(f)

with open('reddit_config.json') as f:
    config = json.load(f)

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=config['client_id'],
    client_secret=config['client_secret'],
    user_agent=config['user_agent'],
    username=config['username'],
    password=config['password']
)

logger.info("Reddit API initialized")

# Extract posts
all_posts = []
seen_urls = set()  # For deduplication
posts_by_subreddit = defaultdict(int)

reddit_config = scope['reddit']
keywords = reddit_config['keywords']
subreddits = [sr.replace('r/', '') for sr in reddit_config['subreddits']]
min_score = reddit_config['minimum_score']
start_date = datetime.fromisoformat(reddit_config['date_range']['start'])

logger.info(f"Starting extraction: {len(keywords)} keywords × {len(subreddits)} subreddits")

for subreddit_name in subreddits:
    logger.info(f"Processing r/{subreddit_name}")
    subreddit = reddit.subreddit(subreddit_name)

    for keyword in keywords:
        try:
            # Search with keyword
            posts = subreddit.search(keyword, time_filter='year', limit=100)

            for post in posts:
                # Validation checks
                if post.score < min_score:
                    continue

                if post.url in seen_urls:
                    continue

                post_date = datetime.fromtimestamp(post.created_utc)
                if post_date < start_date:
                    continue

                if len(post.selftext) < 20:
                    continue

                # Build record
                record = {
                    "post_id": post.id,
                    "subreddit": post.subreddit.display_name,
                    "author": post.author.name if post.author else "[deleted]",
                    "title": post.title,
                    "text": post.selftext,
                    "score": post.score,
                    "num_comments": post.num_comments,
                    "url": post.url,
                    "created_utc": post.created_utc,
                    "is_self": post.is_self,
                    "source": "reddit",
                    "extracted_at": datetime.now().isoformat()
                }

                all_posts.append(record)
                seen_urls.add(post.url)
                posts_by_subreddit[subreddit_name] += 1

                logger.debug(f"Extracted: {post.title[:50]}... from r/{subreddit_name}")

        except Exception as e:
            logger.warning(f"Error searching r/{subreddit_name} for '{keyword}': {e}")
            continue

logger.info(f"Total posts extracted: {len(all_posts)}")
logger.info(f"Posts by subreddit: {dict(posts_by_subreddit)}")

# Prepare output
output = {
    "manifest": {
        "source": "reddit",
        "collection_date": datetime.now().isoformat(),
        "collection_method": "PRAW API",
        "total_records": len(all_posts),
        "expected_range": "1200-1500",
        "completeness": {
            "records_with_urls": sum(1 for p in all_posts if p['url']),
            "records_with_text": sum(1 for p in all_posts if len(p['text']) > 20),
            "records_with_author": sum(1 for p in all_posts if p['author'] != "[deleted]")
        },
        "quality_metrics": {
            "avg_score": sum(p['score'] for p in all_posts) / len(all_posts) if all_posts else 0,
            "avg_comments": sum(p['num_comments'] for p in all_posts) / len(all_posts) if all_posts else 0,
            "date_range": {
                "earliest": min((p['created_utc'] for p in all_posts), default=None),
                "latest": max((p['created_utc'] for p in all_posts), default=None)
            }
        },
        "deduplication": {
            "unique_urls": len(seen_urls),
            "duplicates_removed": 0
        }
    },
    "posts": all_posts
}

# Write output
with open('/01-raw-data/reddit_posts_raw.json', 'w') as f:
    json.dump(output, f, indent=2)

logger.info("Output written to /01-raw-data/reddit_posts_raw.json")

# Validation report
validation_report = {
    "step": "02-EXTRACT-REDDIT",
    "timestamp": datetime.now().isoformat(),
    "total_records": len(all_posts),
    "expected_range": "1200-1500",
    "validation_rules": {
        "rule_urls_complete": {
            "rule": "All posts have URLs",
            "pass": output['manifest']['completeness']['records_with_urls'] == len(all_posts),
            "found": output['manifest']['completeness']['records_with_urls'],
            "expected": len(all_posts)
        },
        "rule_text_quality": {
            "rule": "95%+ posts have text >20 chars",
            "threshold": 0.95,
            "found": output['manifest']['completeness']['records_with_text'] / len(all_posts),
            "pass": output['manifest']['completeness']['records_with_text'] / len(all_posts) >= 0.95
        },
        "rule_author_quality": {
            "rule": "99%+ have non-deleted authors",
            "threshold": 0.99,
            "found": output['manifest']['completeness']['records_with_author'] / len(all_posts),
            "pass": output['manifest']['completeness']['records_with_author'] / len(all_posts) >= 0.99
        },
        "rule_sample_size": {
            "rule": "Sample size 1200-1500",
            "min": 1200,
            "max": 1500,
            "found": len(all_posts),
            "pass": 1200 <= len(all_posts) <= 1500
        }
    },
    "overall_status": "PASS" if all(
        v['pass'] for v in [
            output['manifest']['completeness']['records_with_urls'] == len(all_posts),
            output['manifest']['completeness']['records_with_text'] / len(all_posts) >= 0.95,
            output['manifest']['completeness']['records_with_author'] / len(all_posts) >= 0.99,
            1200 <= len(all_posts) <= 1500
        ]
    ) else "FAIL"
}

with open('/03-analysis-output/validation_report_02.json', 'w') as f:
    json.dump(validation_report, f, indent=2)

logger.info(f"Validation report: {validation_report['overall_status']}")
```

### 4. Execute Extraction

```bash
python3 extract_reddit.py
```

Expected output:
```
Started extraction: 10 keywords × 5 subreddits
Processing r/DIY
Processing r/HomeImprovement
...
Total posts extracted: 1,247
Extracted 1,247 posts from Reddit
Output written to /01-raw-data/reddit_posts_raw.json
Validation report: PASS
```

---

## OUTPUT FILE FORMAT: reddit_posts_raw.json

```json
{
  "manifest": {
    "source": "reddit",
    "collection_date": "2025-11-12T10:30:00",
    "collection_method": "PRAW API",
    "total_records": 1247,
    "expected_range": "1200-1500",
    "completeness": {
      "records_with_urls": 1247,
      "records_with_text": 1235,
      "records_with_author": 1240
    },
    "quality_metrics": {
      "avg_score": 87.3,
      "avg_comments": 23.5,
      "date_range": {
        "earliest": 1672531200,
        "latest": 1731331200
      }
    },
    "deduplication": {
      "unique_urls": 1247,
      "duplicates_removed": 0
    }
  },
  "posts": [
    {
      "post_id": "abc123",
      "subreddit": "DIY",
      "author": "user1234",
      "title": "Built garage shelving - installation nightmare",
      "text": "Just spent 6 hours installing these shelves. The instructions were unclear and I needed help from my neighbor.",
      "score": 156,
      "num_comments": 23,
      "url": "https://reddit.com/r/DIY/comments/abc123",
      "created_utc": 1731331200,
      "is_self": true,
      "source": "reddit",
      "extracted_at": "2025-11-12T10:30:00"
    }
  ]
}
```

---

## VALIDATION RULES

| Rule | Type | Threshold | Action if Fail |
|------|------|-----------|---|
| All posts have URL | CRITICAL | 100% | STOP - investigate API response |
| Text quality (>20 chars) | CRITICAL | 95%+ | Flag short posts, review |
| Author not deleted | MEDIUM | 99%+ | Log deleted authors, continue |
| Sample size 1200-1500 | CRITICAL | ±5% | Adjust keywords if too few/many |
| No duplicate URLs | CRITICAL | 100% | Log duplicates, review dedup |

---

## COMMON ERRORS & FIXES

### Error: "Authentication failed"
- **Cause:** Bad Reddit API credentials
- **Fix:** Verify client_id, client_secret in reddit_config.json
- **Prevention:** Test credentials with simple query: `reddit.user.me()`

### Error: "Rate limit exceeded"
- **Cause:** Too many API requests too fast
- **Fix:** Add 2-second delay between keyword searches
- **Prevention:** Use checkpoint file to resume from last successful keyword

### Error: "Only 500 posts extracted (want 1200+)"
- **Cause:** Keywords too narrow or subreddits not relevant
- **Fix:** Review keyword list, add broader terms, check subreddit activity
- **Prevention:** Do pilot search with 3 keywords before full run

### Error: "95% of posts have text <20 chars"
- **Cause:** Extracting too many link posts (not self-posts)
- **Fix:** Add `is_self=True` filter to extraction
- **Prevention:** Document filter in script comments

---

## DEDUPLICATION STRATEGY

If duplicate posts detected:

1. **Cross-subreddit duplicates** (same post posted multiple places)
   - Action: Keep first occurrence, log rest
   - Store: Remove duplicates before analysis

2. **Reposted content** (same content, different URL)
   - Action: Check for exact text match, keep first
   - Store: Document cross-post relationships

3. **Author duplicates** (same author multiple posts)
   - Action: Keep all (not a duplicate, legitimate author contribution)
   - Store: Note for potential author bias in analysis

---

## SUCCESS CRITERIA

✅ **This step succeeds when:**

```json
{
  "total_records": 1247,  // Within 1200-1500 range
  "completeness": {
    "urls": 100,          // All have URLs
    "text_quality": 99.0, // 99% with meaningful text
    "authors": 99.4       // 99.4% not deleted
  },
  "status": "PASS",
  "next_step": "03-EXTRACT-YOUTUBE.md"
}
```

❌ **This step fails when:**
- Sample size <1200 or >1500
- <95% have text >20 characters
- <90% have non-deleted authors
- Critical API errors

---

## NEXT STEP

Once validation passes:
1. Review reddit_posts_raw.json spot-check (5 random posts)
2. Verify extraction log for warnings
3. Proceed to `03-EXTRACT-YOUTUBE.md`

If validation fails:
1. Identify which rule failed (see VALIDATION RULES)
2. Review COMMON ERRORS section
3. Fix and re-run extraction
4. Do not proceed until all rules PASS

---

**Status:** READY
**Last Updated:** November 12, 2025
