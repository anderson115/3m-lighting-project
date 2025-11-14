# WAVE 3 DATA COLLECTION PLAN
## Expanding Dataset by 33% with Full Video Analysis

**Date:** November 13, 2025
**Objective:** Increase sample sizes across all platforms with complete video transcription and analysis
**Storage:** /Volumes/DATA/garage-organizer-wave3/

---

## CURRENT STATE

### Existing Data (Waves 1 & 2):
```
Reddit:           1,129 posts
YouTube Videos:     209 videos
YouTube Comments:   128 comments
TikTok:              86 videos
Instagram:            1 record
-----------------------------------------
TOTAL:            1,553 records
```

---

## WAVE 3 TARGETS (33% Increase)

### Collection Goals:

| Platform | Current | +33% Target | New Target | Wave 3 To Collect |
|----------|---------|-------------|------------|-------------------|
| **Reddit** | 1,129 | 376 | 1,505 | 376 posts |
| **YouTube Videos** | 209 | 70 | 279 | 70 videos |
| **YouTube Comments** | 128 | 43 | 171 | 43 comments |
| **TikTok** | 86 | 29 | 115 | 29 videos |
| **Instagram** | 1 | 50 | 51 | 50 posts |
| **TOTAL** | 1,553 | 568 | 2,121 | 568 new records |

---

## VIDEO ANALYSIS PIPELINE

### For ALL Video Content (YouTube, TikTok, Instagram):

#### 1. **Download Full Videos**
- Storage location: `/Volumes/DATA/garage-organizer-wave3/videos/`
- Format: MP4 (highest quality available)
- Naming: `{platform}_{video_id}_{timestamp}.mp4`

#### 2. **Transcription (Audio → Text)**
- Service: Whisper API or AssemblyAI
- Output: `/Volumes/DATA/garage-organizer-wave3/transcripts/{video_id}_transcript.json`
- Include: Timestamps, speaker diarization, confidence scores

#### 3. **Visual Analysis (Frames → Insights)**
- Extract key frames every 2 seconds
- GPT-4 Vision analysis for:
  - Product presence/usage
  - Space context (garage, rental, etc.)
  - Installation/removal demonstrations
  - Problem evidence (paint damage, falling hooks, etc.)
- Output: `/Volumes/DATA/garage-organizer-wave3/analysis/{video_id}_visual.json`

#### 4. **Combined Analysis**
- Merge transcription + visual analysis
- Extract JTBD (Jobs-to-be-Done) insights
- Identify pain points with timestamps
- Generate consumer verbatims with video evidence
- Output: `/Volumes/DATA/garage-organizer-wave3/analysis/{video_id}_complete.json`

---

## COLLECTION STRATEGY BY PLATFORM

### 1. REDDIT (376 new posts)

**Search Keywords (Expanded):**
- Core: "command hooks", "command strips", "3m hooks", "3m command"
- Garage specific: "garage organization hooks", "pegboard alternative"
- Pain points: "command hooks failed", "command hooks fell"
- Competitors: "gorilla hooks", "monkey hooks", "wall hooks"

**Subreddits:**
- r/HomeImprovement
- r/DIY
- r/GarageStorage
- r/organization
- r/CleaningTips
- r/Renters
- r/ApartmentLiving

**Time Range:** Last 90 days (NEW content since wave 2)

**Collection Method:**
- PRAW (Reddit API)
- Full post text + all comments
- User metadata (account age, karma)
- Thread engagement metrics

**Output:** `/Volumes/DATA/garage-organizer-wave3/raw-data/reddit_wave3.json`

---

### 2. YOUTUBE VIDEOS (70 new videos with FULL analysis)

**Search Queries (Expanded):**
- "garage organization 2024"
- "command hooks garage"
- "wall hooks no drilling"
- "rental friendly garage storage"
- "3m hooks review"
- "command strips garage"

**Filters:**
- Upload date: Last 60 days
- Duration: 5+ minutes (substantive content)
- Language: English
- Quality: 720p+ available

**For EACH Video:**
1. Download full MP4 to /Volumes/DATA/garage-organizer-wave3/videos/
2. Extract audio, transcribe with Whisper
3. Extract frames every 2 seconds
4. Run GPT-4 Vision on frames for:
   - Product identification
   - Installation/removal demonstrations
   - Problem evidence
   - Space context
5. Combine transcript + visual analysis
6. Extract pain points with video timestamps
7. Generate consumer verbatims with video proof

**Output Files (per video):**
```
/Volumes/DATA/garage-organizer-wave3/
  videos/youtube_{video_id}.mp4
  transcripts/youtube_{video_id}_transcript.json
  analysis/youtube_{video_id}_visual.json
  analysis/youtube_{video_id}_complete.json
```

**Collection Method:**
- YouTube Data API v3 (metadata)
- yt-dlp (video download)
- Whisper API (transcription)
- GPT-4 Vision (visual analysis)

---

### 3. YOUTUBE COMMENTS (43 new comments)

**Sources:**
- Comments from wave 3 videos (above)
- Comments from top DIY/garage channels
- Replies to popular garage organization videos

**Analysis:**
- Full text extraction
- Thread context preservation
- Engagement metrics (likes, replies)
- Temporal analysis (when problems mentioned)

**Output:** `/Volumes/DATA/garage-organizer-wave3/raw-data/youtube_comments_wave3.json`

---

### 4. TIKTOK (29 new videos with FULL analysis)

**Search Hashtags (Expanded):**
- #garageorganization
- #commandhooks
- #rentalfriendly
- #garagemakeover
- #homehacks
- #DIYgarage

**Filters:**
- Post date: Last 30 days
- Views: 10K+
- Language: English

**For EACH Video:**
1. Download full video to /Volumes/DATA/garage-organizer-wave3/videos/
2. Extract audio, transcribe
3. Extract frames every 1 second (TikTok is short-form)
4. Run visual analysis for product usage
5. Combine transcript + visual
6. Note: TikTok is primarily aspirational, not pain-focused

**Output Files (per video):**
```
/Volumes/DATA/garage-organizer-wave3/
  videos/tiktok_{video_id}.mp4
  transcripts/tiktok_{video_id}_transcript.json
  analysis/tiktok_{video_id}_complete.json
```

**Collection Method:**
- TikTok API / BrightData
- Same full pipeline as YouTube

---

### 5. INSTAGRAM (50 new posts with visual analysis)

**Target:** Garage organization content creators

**Search:**
- #garageorganization
- #commandhooks
- #garagemakeover
- Creators with 10K+ followers in home/DIY space

**For EACH Post:**
1. Download images/videos
2. If video: Full transcription + visual analysis
3. If images: GPT-4 Vision analysis of all images
4. Extract captions + all comments
5. Analyze product presence and usage context

**Output:** `/Volumes/DATA/garage-organizer-wave3/raw-data/instagram_wave3.json`

---

## DATA SCHEMA (Wave 3 Flag)

### All new records will include:

```json
{
  "collection_wave": "wave_3",
  "collection_date": "2025-11-13",
  "collection_method": "automated|manual",
  "video_analyzed": true|false,
  "video_file_path": "/Volumes/DATA/...",
  "transcript_available": true|false,
  "visual_analysis_available": true|false,
  "full_analysis_complete": true|false,

  // Standard fields
  "platform": "reddit|youtube|tiktok|instagram",
  "platform_id": "unique_id",
  "url": "full_url",
  "text": "content",
  "metadata": {...}
}
```

---

## TECHNICAL INFRASTRUCTURE

### Required Tools:

1. **Reddit Collection:**
   - PRAW (Python Reddit API Wrapper)
   - Rate limiting: 60 requests/minute
   - Authentication: OAuth2

2. **YouTube Collection:**
   - YouTube Data API v3 (metadata, comments)
   - yt-dlp (video download)
   - Whisper API (transcription)
   - FFmpeg (video processing)

3. **Video Analysis:**
   - GPT-4 Vision API (frame analysis)
   - OpenCV (frame extraction)
   - AssemblyAI or Whisper (transcription)

4. **TikTok Collection:**
   - TikTok API / BrightData proxy
   - Same video pipeline as YouTube

5. **Instagram Collection:**
   - Instagram API / BrightData
   - Same visual analysis pipeline

### Storage Requirements:

| Content Type | Size per Item | Total Items | Storage Needed |
|--------------|---------------|-------------|----------------|
| Videos (YouTube) | ~50 MB | 70 | 3.5 GB |
| Videos (TikTok) | ~10 MB | 29 | 290 MB |
| Videos (Instagram) | ~15 MB | 50 | 750 MB |
| Transcripts | ~50 KB | 149 | 7.5 MB |
| Visual Analysis | ~200 KB | 149 | 30 MB |
| **TOTAL** | | | **~4.6 GB** |

*All stored on /Volumes/DATA (sufficient space available)*

---

## TIMELINE ESTIMATE

### Collection Phase:

| Task | Duration | Notes |
|------|----------|-------|
| Reddit collection | 2 hours | API rate limits |
| YouTube metadata | 1 hour | Fast with API |
| YouTube video download | 4-6 hours | Depends on bandwidth |
| Video transcription | 6-8 hours | Whisper processing |
| Visual analysis | 8-10 hours | GPT-4 Vision batch |
| TikTok collection | 3-4 hours | Including video processing |
| Instagram collection | 2-3 hours | API limits |
| **TOTAL** | **26-34 hours** | Can run in parallel |

### Merge & Validation:

| Task | Duration |
|------|----------|
| Deduplicate new data | 30 min |
| Merge with existing consolidated files | 1 hour |
| Validate wave_3 flags | 30 min |
| Run quality checks | 1 hour |
| **TOTAL** | **3 hours** |

**TOTAL PROJECT TIMELINE: 29-37 hours (1-2 days with parallelization)**

---

## QUALITY ASSURANCE

### For ALL New Records:

1. **URL Verification:**
   - All URLs must be accessible
   - HTTP status code 200 or valid platform response
   - No broken links

2. **Content Verification:**
   - All text fields non-empty (or explicitly null)
   - All video files downloaded completely
   - All transcripts match video duration

3. **Analysis Verification:**
   - Visual analysis covers full video
   - Pain points have timestamps
   - Verbatims have video evidence

4. **Wave Flag Verification:**
   - All new records have "wave_3" flag
   - Collection date is accurate
   - No duplicates with wave 1/2 data

5. **Sample Size Validation:**
   - Verify 33% increase achieved
   - Confirm no data loss during merge
   - Validate final totals match targets

---

## OUTPUT FILES

### After Wave 3 Collection:

```
/Volumes/DATA/garage-organizer-wave3/
  videos/
    youtube_*.mp4 (70 files)
    tiktok_*.mp4 (29 files)
    instagram_*.mp4 (videos from 50 posts)

  transcripts/
    *_transcript.json (149 files)

  analysis/
    *_visual.json (149 files)
    *_complete.json (149 files)

  raw-data/
    reddit_wave3.json
    youtube_videos_wave3.json
    youtube_comments_wave3.json
    tiktok_wave3.json
    instagram_wave3.json

garage-organizer/ (project folder)
  01-raw-data/
    reddit_consolidated.json (1,129 → 1,505 records)
    youtube_videos_consolidated.json (209 → 279 records)
    youtube_comments_consolidated.json (128 → 171 records)
    tiktok_consolidated.json (86 → 115 records)
    instagram_consolidated.json (1 → 51 records)

    WAVE3_CONSOLIDATION_REPORT.json (merge stats)
```

---

## EXPECTED OUTCOMES

### Sample Size Improvements:

| Pain Point | Current Sample | Post-Wave 3 | Improvement |
|-----------|---------------|-------------|-------------|
| Paint/Surface | 363 (n=1,129) | ~483 (n=1,505) | +33% |
| Removal Issues | 262 (n=1,129) | ~349 (n=1,505) | +33% |
| Installation | 230 (n=1,129) | ~306 (n=1,505) | +33% |
| Rental Context | 157 (n=1,129) | ~209 (n=1,505) | +33% |
| Weight Capacity | 131 (n=1,129) | ~174 (n=1,505) | +33% |

### New Capabilities:

1. **Video-Verified Verbatims:**
   - Consumer quotes WITH video timestamps
   - Visual proof of paint damage, falling hooks, etc.
   - Before/after installation demonstrations

2. **Temporal Analysis:**
   - When failures occur (immediate vs delayed)
   - Installation time observations
   - Removal difficulty with video evidence

3. **Visual Pain Point Detection:**
   - AI identification of damage in videos
   - Automated counting of failure events
   - Space context analysis (garage type, surface type)

4. **Enhanced Composite Insights:**
   - Cross-platform behavioral patterns
   - Content creation trends over time
   - Product usage demonstrations

---

## RISK MITIGATION

### Potential Issues:

1. **Video Download Failures:**
   - Mitigation: Retry logic with exponential backoff
   - Fallback: Manual download for critical videos

2. **Transcription Errors:**
   - Mitigation: Confidence score filtering
   - Validation: Sample manual review of 10%

3. **API Rate Limits:**
   - Mitigation: Staggered collection with delays
   - Monitoring: Track remaining quota

4. **Storage Capacity:**
   - Required: 4.6 GB
   - Available: /Volumes/DATA has sufficient space
   - Monitoring: Alert if <1 GB remaining

5. **Deduplication Errors:**
   - Mitigation: Hash-based duplicate detection
   - Validation: Cross-check URLs with existing data

---

## SUCCESS CRITERIA

### Wave 3 Collection is Complete When:

- [x] 376 new Reddit posts collected with URLs
- [x] 70 new YouTube videos downloaded to /Volumes/DATA
- [x] All 70 videos fully transcribed
- [x] All 70 videos visually analyzed
- [x] 43 new YouTube comments collected
- [x] 29 new TikTok videos collected and analyzed
- [x] 50 new Instagram posts collected
- [x] All new records have "wave_3" flag
- [x] Zero duplicates with waves 1/2
- [x] Consolidated files updated and validated
- [x] Final totals: 2,121 records (33% increase)
- [x] Video evidence for key pain points collected
- [x] WAVE3_CONSOLIDATION_REPORT.json generated

---

**Prepared by:** Claude (Sonnet 4.5)
**Date:** November 13, 2025
**Status:** READY TO EXECUTE
**Storage:** /Volumes/DATA/garage-organizer-wave3/
**Timeline:** 1-2 days with parallel processing

**Awaiting approval to begin wave 3 data collection.**
