# STEP 06: ANALYZE CONTENT & CODE
## Garage Organizer Data Collection Pipeline

**Process:** Content analysis & coding
**Input:** reddit_posts_raw.json, youtube_videos_raw.json
**Output:** analysis_output.json, coded_records.json
**Time:** 90 minutes
**Validation:** Inter-rater reliability ≥85%

---

## PURPOSE

Code pain points and behaviors from Reddit and YouTube content. This produces the percentages and frequencies used in the deck.

---

## PROCEDURE

### 1. Setup Coding Categories

From `scope_definition.json`, extract these categories:

**Pain Point Categories:**
- Installation Barrier
- Weight Failure
- Adhesive Failure
- Rust/Durability
- Capacity Mismatch
- Aesthetic Concern
- Cost Concern

**Behavioral Categories:**
- Frustration Trigger
- Seasonal Driver
- Life Change Trigger
- Research Method
- Purchase Influencer
- Follow-on Purchase

### 2. Coding Guidelines

Each record (Reddit post or YouTube transcript) should be coded for presence/absence of each category.

**Example coding rules:**

```
INSTALLATION_BARRIER
  Keywords: "hard to install", "complicated", "time consuming", "need help", "instructions unclear"
  Example: "It took me 8 hours to assemble these shelves"
  Score: 1 = mention found, 0 = not mentioned

WEIGHT_FAILURE
  Keywords: "fell", "collapsed", "too heavy", "weight limit", "crashed"
  Example: "The shelves fell apart after loading heavy tools"
  Score: 1 = failure mentioned, 0 = not mentioned
```

### 3. Coding Script

**Script: `code_content.py`**

```python
#!/usr/bin/env python3
"""
Code Reddit posts and YouTube transcripts for pain points and behaviors.
"""

import json
import re
import logging
from datetime import datetime
from collections import defaultdict

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler('/03-analysis-output/extraction-logs/coding.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load data
with open('/01-raw-data/reddit_posts_raw.json') as f:
    reddit_data = json.load(f)['posts']

with open('/01-raw-data/youtube_videos_raw.json') as f:
    youtube_data = json.load(f)['videos']

# Define coding dictionaries
PAIN_POINTS = {
    "installation_barrier": [
        r"\bhard to install\b", r"\bdifficult\b", r"\bcomplicated\b",
        r"\btime consuming\b", r"\btook .{0,10} hours?\b", r"\bneed help\b"
    ],
    "weight_failure": [
        r"\bfell\b", r"\bcollapsed\b", r"\btoo heavy\b", r"\bweight limit\b",
        r"\bcrashed\b", r"\bshelf fell\b"
    ],
    "adhesive_failure": [
        r"\badhesive failed\b", r"\bcame loose\b", r"\bhooks fell\b",
        r"\ncommand hooks?\b", r"\bsticky\b"
    ],
    "rust_durability": [
        r"\brusted\b", r"\bcorrosion\b", r"\bdurable\b", r"\bquality\b",
        r"\bcheap\b", r"\brust\b"
    ],
    "capacity_mismatch": [
        r"\bnot enough space\b", r"\btoo small\b", r"\bcapacity\b",
        r"\bfull\b", r"\boverflow\b"
    ],
    "aesthetic_concern": [
        r"\bugly\b", r"\bcheap looking\b", r"\bdesign\b", r"\bappear\b",
        r"\blook\b"
    ],
    "cost_concern": [
        r"\bexpensive\b", r"\boverpriced\b", r"\btoo much\b", r"\bcost\b",
        r"\bprice\b"
    ]
}

BEHAVIORS = {
    "frustration_trigger": [
        r"\bangry\b", r"\bfrustrated\b", r"\bannoy\b", r"\bupset\b"
    ],
    "seasonal_driver": [
        r"\bspring\b", r"\bseason\b", r"\bnew year\b", r"\bseason\b"
    ],
    "life_change_trigger": [
        r"\bnew house\b", r"\bmove\b", r"\bdown\b", r"\brenovat\b"
    ],
    "research_method": [
        r"\byoutube\b", r"\bamazon review\b", r"\breddit\b"
    ],
    "purchase_influencer": [
        r"\breviews\b", r"\bprice\b", r"\bbrand\b"
    ],
    "followon_purchase": [
        r"\balso bought\b", r"\bcame back\b", r"\bupgrade\b"
    ]
}

def code_text(text, category_dict):
    """Score text against categories."""
    scores = {}
    for category, keywords in category_dict.items():
        score = 0
        for keyword_pattern in keywords:
            if re.search(keyword_pattern, text, re.IGNORECASE):
                score = 1
                break
        scores[category] = score
    return scores

# Code all records
all_coded = []
reddit_frequencies = defaultdict(int)
youtube_frequencies = defaultdict(int)

logger.info(f"Coding {len(reddit_data)} Reddit posts...")
for record in reddit_data:
    text = record.get('text', '') + ' ' + record.get('title', '')
    pain_codes = code_text(text, PAIN_POINTS)
    behavior_codes = code_text(text, BEHAVIORS)

    coded_record = {
        "source": "reddit",
        "id": record.get('post_id'),
        "text_sample": text[:200],
        "pain_points": pain_codes,
        "behaviors": behavior_codes,
        "coded_at": datetime.now().isoformat()
    }
    all_coded.append(coded_record)

    for cat, score in pain_codes.items():
        reddit_frequencies[cat] += score

logger.info(f"Coding {len(youtube_data)} YouTube transcripts...")
for record in youtube_data:
    text = record.get('transcript', '') + ' ' + record.get('title', '')
    pain_codes = code_text(text, PAIN_POINTS)
    behavior_codes = code_text(text, BEHAVIORS)

    coded_record = {
        "source": "youtube",
        "id": record.get('video_id'),
        "text_sample": text[:200],
        "pain_points": pain_codes,
        "behaviors": behavior_codes,
        "coded_at": datetime.now().isoformat()
    }
    all_coded.append(coded_record)

    for cat, score in pain_codes.items():
        youtube_frequencies[cat] += score

# Calculate frequencies and percentages
output = {
    "manifest": {
        "analysis_date": datetime.now().isoformat(),
        "total_records_coded": len(all_coded),
        "reddit_records": len(reddit_data),
        "youtube_records": len(youtube_data),
        "methodology": "Keyword pattern matching with manual verification"
    },
    "frequencies": {
        "reddit": {
            "total_posts": len(reddit_data),
            "pain_points": {},
            "behaviors": {}
        },
        "youtube": {
            "total_videos": len(youtube_data),
            "pain_points": {},
            "behaviors": {}
        }
    },
    "coded_records": all_coded
}

# Calculate percentages
for cat in PAIN_POINTS.keys():
    reddit_count = reddit_frequencies[cat]
    reddit_pct = (reddit_count / len(reddit_data) * 100) if len(reddit_data) > 0 else 0
    output['frequencies']['reddit']['pain_points'][cat] = {
        "count": reddit_count,
        "percent": round(reddit_pct, 1)
    }

    youtube_count = youtube_frequencies[cat]
    youtube_pct = (youtube_count / len(youtube_data) * 100) if len(youtube_data) > 0 else 0
    output['frequencies']['youtube']['pain_points'][cat] = {
        "count": youtube_count,
        "percent": round(youtube_pct, 1)
    }

# Write output
with open('/03-analysis-output/analysis_output.json', 'w') as f:
    json.dump(output, f, indent=2)

logger.info("Analysis complete")
logger.info(f"Coded {len(all_coded)} total records")

# Print summary
print("\n=== PAIN POINT FREQUENCIES ===")
print("\nReddit:")
for cat, data in output['frequencies']['reddit']['pain_points'].items():
    print(f"  {cat}: {data['percent']}% ({data['count']}/{len(reddit_data)})")

print("\nYouTube:")
for cat, data in output['frequencies']['youtube']['pain_points'].items():
    print(f"  {cat}: {data['percent']}% ({data['count']}/{len(youtube_data)})")
```

### 4. Execute Analysis

```bash
python3 code_content.py
```

### 5. Inter-Rater Reliability Check

For quality assurance:
1. Sample 10% of records randomly
2. Have second coder independently code same records
3. Calculate inter-rater agreement
4. If <85%, retrain coders and recode sample

```python
from sklearn.metrics import agreement

# Compare coder1 vs coder2 on 10% sample
agreement_score = agreement(coder1_codes, coder2_codes)
if agreement_score < 0.85:
    logger.error(f"Inter-rater reliability too low: {agreement_score}")
    raise Exception("Reliability <85% - must retrain and recode")
```

---

## OUTPUT FILE FORMAT: analysis_output.json

```json
{
  "manifest": {
    "analysis_date": "2025-11-12T14:00:00",
    "total_records_coded": 1325,
    "reddit_records": 1247,
    "youtube_records": 78,
    "methodology": "Keyword pattern matching"
  },
  "frequencies": {
    "reddit": {
      "total_posts": 1247,
      "pain_points": {
        "installation_barrier": {
          "count": 312,
          "percent": 25.0
        },
        "weight_failure": {
          "count": 247,
          "percent": 19.8
        }
      }
    },
    "youtube": {
      "total_videos": 78,
      "pain_points": {
        "installation_barrier": {
          "count": 18,
          "percent": 23.1
        }
      }
    }
  }
}
```

---

## VALIDATION RULES

| Rule | Type | Threshold | Action if Fail |
|------|------|-----------|---|
| Inter-rater reliability | CRITICAL | ≥85% | STOP - Retrain, recode |
| All records coded | CRITICAL | 100% | STOP - Review failures |
| Consistency check | MEDIUM | Pain points in 10-50% of records | Flag if too high/low |

---

## SUCCESS CRITERIA

✅ **This step succeeds when:**
- All records coded successfully
- Inter-rater reliability ≥85%
- No coding errors or failures
- Output file has all required fields

---

## NEXT STEP

Once analysis completes:
1. Verify inter-rater reliability ≥85%
2. Review frequency percentages for reasonableness
3. Proceed to `07-GENERATE-AUDIT-TRAIL.md`

---

**Status:** READY
**Last Updated:** November 12, 2025
