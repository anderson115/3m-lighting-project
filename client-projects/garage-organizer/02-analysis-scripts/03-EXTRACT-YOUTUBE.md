# STEP 03: EXTRACT YOUTUBE VIDEOS
## Garage Organizer Data Collection Pipeline

**Process:** Data extraction
**Input:** `scope_definition.json`
**Output:** `youtube_videos_raw.json`
**Time:** 60 minutes
**Validation:** Transcripts, view counts, deduplication

---

## PURPOSE

Extract YouTube videos and transcripts. YouTube is validation-seeking source (research before purchase).

---

## INPUTS REQUIRED

- `scope_definition.json` (from Step 01)
- YouTube API key configured (Google Cloud project)
- youtube-transcript-api installed (`pip install youtube-transcript-api`)
- pytube installed (`pip install pytube`)

---

## PROCEDURE

### 1. Verify Prerequisites

```bash
# Check libraries
python3 -c "from youtube_transcript_api import YouTubeTranscriptApi; print('Transcript API ready')"
python3 -c "from googleapiclient.discovery import build; print('Google API ready')"

# Verify scope definition exists
test -f /01-raw-data/scope_definition.json && echo "Scope file found"

# Create output directory
mkdir -p /03-analysis-output/extraction-logs/
```

### 2. Configure YouTube API

Create `youtube_config.json`:
```json
{
  "api_key": "YOUR_YOUTUBE_API_KEY",
  "api_version": "v3"
}
```

### 3. Run Extraction Script

**Script: `extract_youtube.py`**

```python
#!/usr/bin/env python3
"""
Extract YouTube videos and transcripts matching scope criteria.
Inputs: scope_definition.json, youtube_config.json
Outputs: youtube_videos_raw.json, youtube_extraction.log
"""

import json
import logging
from datetime import datetime
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/03-analysis-output/extraction-logs/youtube_extraction.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load configurations
with open('/01-raw-data/scope_definition.json') as f:
    scope = json.load(f)

with open('youtube_config.json') as f:
    config = json.load(f)

# Initialize YouTube API
youtube = build('youtube', 'v3', developerKey=config['api_key'])
logger.info("YouTube API initialized")

# Extract videos
all_videos = []
seen_video_ids = set()

youtube_config = scope['youtube']
keywords = youtube_config['keywords']
min_views = youtube_config['minimum_view_count']
min_duration = youtube_config['video_duration_seconds']['min']
max_duration = youtube_config['video_duration_seconds']['max']

logger.info(f"Starting extraction: {len(keywords)} keywords")

for i, keyword in enumerate(keywords):
    logger.info(f"Processing keyword {i+1}/{len(keywords)}: {keyword}")

    try:
        # Search for videos
        request = youtube.search().list(
            q=keyword,
            part='snippet',
            type='video',
            order='relevance',
            maxResults=50,
            publishedAfter='2021-01-01T00:00:00Z',
            relevanceLanguage='en',
            regionCode='US'
        )

        while request and len(all_videos) < 200:  # Limit total requests
            response = request.execute()

            for item in response.get('items', []):
                video_id = item['id']['videoId']

                if video_id in seen_video_ids:
                    continue

                # Get detailed video stats
                try:
                    video_detail = youtube.videos().list(
                        id=video_id,
                        part='contentDetails,statistics,snippet'
                    ).execute()

                    if not video_detail['items']:
                        continue

                    video_data = video_detail['items'][0]
                    stats = video_data['statistics']
                    snippet = video_data['snippet']
                    details = video_data['contentDetails']

                    # Parse duration
                    import re
                    duration_str = details['duration']
                    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
                    if match:
                        hours = int(match.group(1) or 0)
                        minutes = int(match.group(2) or 0)
                        seconds = int(match.group(3) or 0)
                        total_seconds = hours * 3600 + minutes * 60 + seconds
                    else:
                        total_seconds = 0

                    # Skip if outside duration range
                    if total_seconds < min_duration or total_seconds > max_duration:
                        continue

                    # Skip if too few views
                    view_count = int(stats.get('viewCount', 0))
                    if view_count < min_views:
                        continue

                    # Try to get transcript
                    transcript_text = None
                    transcript_source = None
                    try:
                        transcript = YouTubeTranscriptApi.get_transcript(video_id)
                        transcript_text = ' '.join([entry['text'] for entry in transcript])
                        transcript_source = 'manual' if any(t.get('kind') == 'standard' for t in [transcript]) else 'auto_generated'
                    except Exception as e:
                        logger.warning(f"No transcript for {video_id}: {e}")
                        transcript_source = 'unavailable'

                    # Skip if no transcript available
                    if transcript_source == 'unavailable':
                        continue

                    # Build record
                    record = {
                        "video_id": video_id,
                        "title": snippet['title'],
                        "description": snippet['description'],
                        "channel_title": snippet['channelTitle'],
                        "channel_id": snippet['channelId'],
                        "published_at": snippet['publishedAt'],
                        "duration_seconds": total_seconds,
                        "view_count": view_count,
                        "like_count": int(stats.get('likeCount', 0)),
                        "comment_count": int(stats.get('commentCount', 0)),
                        "url": f"https://www.youtube.com/watch?v={video_id}",
                        "transcript": transcript_text[:5000],  # First 5000 chars
                        "transcript_source": transcript_source,
                        "source": "youtube",
                        "extracted_at": datetime.now().isoformat()
                    }

                    all_videos.append(record)
                    seen_video_ids.add(video_id)
                    logger.debug(f"Extracted: {record['title'][:50]}...")

                    time.sleep(0.5)  # Rate limiting

                except Exception as e:
                    logger.warning(f"Error processing video {video_id}: {e}")
                    continue

            # Get next page
            if 'nextPageToken' in response:
                request = youtube.search().list_next(request, response)
            else:
                request = None

    except Exception as e:
        logger.warning(f"Error searching for '{keyword}': {e}")
        time.sleep(2)  # Back off on error
        continue

    time.sleep(1)  # Delay between keywords

logger.info(f"Total videos extracted: {len(all_videos)}")

# Prepare output
output = {
    "manifest": {
        "source": "youtube",
        "collection_date": datetime.now().isoformat(),
        "collection_method": "YouTube API v3",
        "total_records": len(all_videos),
        "expected_range": "60-100",
        "completeness": {
            "records_with_urls": sum(1 for v in all_videos if v['url']),
            "records_with_transcripts": sum(1 for v in all_videos if v.get('transcript')),
            "transcript_manual": sum(1 for v in all_videos if v.get('transcript_source') == 'manual'),
            "transcript_auto": sum(1 for v in all_videos if v.get('transcript_source') == 'auto_generated')
        },
        "quality_metrics": {
            "avg_views": sum(v['view_count'] for v in all_videos) / len(all_videos) if all_videos else 0,
            "avg_duration_seconds": sum(v['duration_seconds'] for v in all_videos) / len(all_videos) if all_videos else 0,
            "avg_engagement": sum(v['like_count'] + v['comment_count'] for v in all_videos) / len(all_videos) if all_videos else 0
        }
    },
    "videos": all_videos
}

# Write output
with open('/01-raw-data/youtube_videos_raw.json', 'w') as f:
    json.dump(output, f, indent=2)

logger.info("Output written to /01-raw-data/youtube_videos_raw.json")

# Validation report
validation_report = {
    "step": "03-EXTRACT-YOUTUBE",
    "timestamp": datetime.now().isoformat(),
    "total_records": len(all_videos),
    "expected_range": "60-100",
    "validation_rules": {
        "rule_urls_complete": {
            "rule": "All videos have URLs",
            "pass": output['manifest']['completeness']['records_with_urls'] == len(all_videos),
            "found": output['manifest']['completeness']['records_with_urls'],
            "expected": len(all_videos)
        },
        "rule_transcripts_complete": {
            "rule": "90%+ have transcripts",
            "threshold": 0.90,
            "found": output['manifest']['completeness']['records_with_transcripts'] / len(all_videos) if all_videos else 0,
            "pass": output['manifest']['completeness']['records_with_transcripts'] / len(all_videos) >= 0.90 if all_videos else False
        },
        "rule_view_minimum": {
            "rule": "All videos have >100 views",
            "min_views": 100,
            "found": min((v['view_count'] for v in all_videos), default=None),
            "pass": all(v['view_count'] >= 100 for v in all_videos)
        },
        "rule_sample_size": {
            "rule": "Sample size 60-100",
            "min": 60,
            "max": 100,
            "found": len(all_videos),
            "pass": 60 <= len(all_videos) <= 100
        }
    },
    "overall_status": "PASS" if all([
        output['manifest']['completeness']['records_with_urls'] == len(all_videos),
        output['manifest']['completeness']['records_with_transcripts'] / len(all_videos) >= 0.90 if all_videos else False,
        all(v['view_count'] >= 100 for v in all_videos),
        60 <= len(all_videos) <= 100
    ]) else "FAIL"
}

with open('/03-analysis-output/validation_report_03.json', 'w') as f:
    json.dump(validation_report, f, indent=2)

logger.info(f"Validation report: {validation_report['overall_status']}")
```

### 4. Execute Extraction

```bash
python3 extract_youtube.py
```

---

## OUTPUT FILE FORMAT: youtube_videos_raw.json

```json
{
  "manifest": {
    "source": "youtube",
    "collection_date": "2025-11-12T11:30:00",
    "collection_method": "YouTube API v3",
    "total_records": 78,
    "expected_range": "60-100",
    "completeness": {
      "records_with_urls": 78,
      "records_with_transcripts": 78,
      "transcript_manual": 12,
      "transcript_auto": 66
    },
    "quality_metrics": {
      "avg_views": 45000,
      "avg_duration_seconds": 600,
      "avg_engagement": 250
    }
  },
  "videos": [
    {
      "video_id": "abc123xyz",
      "title": "How to Build Garage Shelves",
      "description": "Complete guide to building heavy-duty garage shelving...",
      "channel_title": "DIY Channel",
      "channel_id": "UCxxxxx",
      "published_at": "2023-06-15T10:30:00Z",
      "duration_seconds": 900,
      "view_count": 125000,
      "like_count": 3200,
      "comment_count": 450,
      "url": "https://www.youtube.com/watch?v=abc123xyz",
      "transcript": "Today we're building garage shelves. First, gather your materials...",
      "transcript_source": "auto_generated",
      "source": "youtube",
      "extracted_at": "2025-11-12T11:30:00"
    }
  ]
}
```

---

## VALIDATION RULES

| Rule | Type | Threshold | Action if Fail |
|------|------|-----------|---|
| All videos have URLs | CRITICAL | 100% | STOP - investigate API response |
| Transcripts available | CRITICAL | 90%+ | Skip videos without transcripts |
| View count >100 | CRITICAL | 100% | Remove videos with <100 views |
| Sample size 60-100 | CRITICAL | ±5% | Adjust keyword list if too few/many |

---

## COMMON ERRORS & FIXES

### Error: "No transcripts found"
- **Cause:** Video has no captions available
- **Fix:** Skip that video, continue with others
- **Prevention:** Filter by `caption` parameter in API search

### Error: "API quota exceeded"
- **Cause:** Hit YouTube API daily quota
- **Fix:** Wait until next day or upgrade API quota
- **Prevention:** Estimate quota: 50 videos × 5 requests each = 250 units

### Error: "Only 30 videos extracted (want 60+)"
- **Cause:** Keywords too specific, not enough videos match
- **Fix:** Add broader keywords, increase results per search
- **Prevention:** Test keywords with small sample first

---

## DEDUPLICATION STRATEGY

If duplicate videos found:
- **Same video different playlist:** Keep once, note cross-reference
- **Different creators same topic:** Keep both (legitimate variation)
- **Reposted content:** Check upload dates, keep original

---

## SUCCESS CRITERIA

✅ **This step succeeds when:**
- 60-100 videos extracted
- 100% have URLs
- 90%+ have usable transcripts
- All have >100 views

---

## NEXT STEP

Once validation passes:
1. Spot-check 5 random videos for transcript quality
2. Verify transcript text is coherent
3. Proceed to `04-EXTRACT-PRODUCTS.md`

---

**Status:** READY
**Last Updated:** November 12, 2025
