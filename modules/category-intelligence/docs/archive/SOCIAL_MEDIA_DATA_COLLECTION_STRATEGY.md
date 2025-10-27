# Social Media Consumer Insights Collection Strategy
**Platform Target:** TikTok & YouTube
**Purpose:** Garage organization consumer language, trends, pain points
**Date:** 2025-10-24

---

## YOUTUBE DATA COLLECTION - ✅ READY TO USE

### Current Status: FULLY CONFIGURED

**API Key Found:** `AIzaSyBlVDc0Hstxb_ZpJxOH-Z-3hV0rdjiudp8`
**Module Location:** `/core/data_sources/youtube.py`
**Environment:** Configured in `.env` file

### Capabilities Available:
- ✅ Search videos by keyword with filters (relevance, date, viewCount)
- ✅ Extract full metadata (title, description, views, likes, comments, tags)
- ✅ Download videos using yt-dlp
- ✅ Extract audio for transcription (16kHz WAV, Whisper-optimized)
- ✅ Deduplication logic
- ✅ Pagination support (50 results per page, unlimited pages)

### Usage Example:
```python
from core.data_sources.youtube import YouTubeDataSource

yt = YouTubeDataSource()  # Uses YOUTUBE_API_KEY from .env

# Search for garage organization content
videos = yt.search_videos(
    query="garage organization",
    max_results=100,
    order="relevance",
    published_after="2024-01-01T00:00:00Z"  # Last year only
)

# Get detailed metadata
for video in videos:
    metadata = yt.get_video_metadata(video['video_id'])
    # Analyze title, description, tags for consumer language
```

### Recommended YouTube Collection Plan:
**Queries:** "garage organization", "garage makeover", "DIY garage storage", "organize garage", "garage transformation", "small garage organization"
**Target:** 150-200 videos (free tier allows 10,000 API units/day)
**Cost:** FREE (within quota)
**Time:** ~5 minutes
**Output:** Titles, descriptions, tags, engagement metrics

---

## TIKTOK DATA COLLECTION - MULTIPLE OPTIONS

### OPTION 1: Apify TikTok Scraper (RECOMMENDED - EASIEST)

**Status:** ✅ API credentials already configured
**Actor:** `clockworks/tiktok-scraper`
**Cost:** Uses existing Apify account credits

**Capabilities:**
- Hashtag search (#garageorganization, #garagemakeover)
- Profile scraping
- Video metadata (caption, likes, comments, shares, views)
- Music/sound tracking
- Trend analysis

**Pros:**
- Already have Apify credentials configured
- Maintained by professional team
- Handles anti-bot defenses automatically
- JSON output ready for analysis
- Free tier: First run often free, then ~$0.25-1.00 per 1000 videos

**Cons:**
- Requires credits (may run out quickly)
- Less control over scraping logic

**Implementation:**
```python
from apify_client import ApifyClient

client = ApifyClient(os.environ.get('APIFY_API_TOKEN'))

run_input = {
    "hashtags": ["garageorganization", "garagemakeover", "garagehacks"],
    "resultsPerPage": 100,
    "maxProfilesCount": 500
}

run = client.actor("clockworks/tiktok-scraper").call(run_input=run_input)

# Extract captions, hashtags, trending sounds
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    caption = item.get("text", "")
    hashtags = item.get("hashtags", [])
    # Analyze for consumer language patterns
```

---

### OPTION 2: TikTok-Api Python Library (RECOMMENDED - BEST CONTROL)

**Status:** Open source, actively maintained (5.7k GitHub stars)
**Repository:** https://github.com/davidteather/TikTok-Api
**Cost:** FREE
**Last Updated:** August 2025

**Capabilities:**
- Trending content by hashtag
- User profile data
- Video metadata
- Comment scraping
- Sound/music tracking
- Async/await patterns

**Pros:**
- Completely free
- Full control over scraping
- Active community support
- Works around TikTok's defenses
- Can run unlimited queries

**Cons:**
- Requires ms_token from cookies (one-time manual setup)
- Needs Playwright installation
- May require occasional updates if TikTok changes API
- More complex setup than Apify

**Setup:**
```bash
pip install TikTokApi
python -m playwright install
```

**Implementation:**
```python
from TikTokApi import TikTokApi
import asyncio

async def get_hashtag_videos():
    async with TikTokApi() as api:
        await api.create_sessions(
            ms_tokens=[YOUR_MS_TOKEN],  # From cookies
            num_sessions=1,
            sleep_after=3
        )

        tag = api.hashtag(name="garageorganization")

        async for video in tag.videos(count=100):
            # Extract caption, hashtags, engagement
            print(video.desc)  # Caption/description
            print(video.stats)  # Views, likes, comments

asyncio.run(get_hashtag_videos())
```

---

### OPTION 3: Manual Download + Transcription (HYBRID APPROACH)

**Tools:**
- **KOLsprite Chrome Extension** - Bulk download TikTok videos
- **Whisper (OpenAI)** - Transcribe audio to text
- **Claude Code** - Analyze transcripts for consumer language

**Workflow:**
1. Use browser extension to bulk download 50-100 garage organization TikToks
2. Extract audio with ffmpeg
3. Transcribe with Whisper (free, local)
4. Feed transcripts to Claude for analysis

**Pros:**
- No API limitations
- Get actual speech/voiceover content
- Can analyze visual context
- Free after initial setup

**Cons:**
- Manual/semi-automated
- Time-consuming (30-60 min for 100 videos)
- Requires disk space
- Miss out on metadata (likes, shares, etc.)

**Implementation:**
```bash
# After downloading videos
for video in *.mp4; do
    ffmpeg -i "$video" -ar 16000 -ac 1 "${video%.mp4}.wav"
    whisper "${video%.mp4}.wav" --model medium --language en
done

# Then analyze transcripts with Claude Code
```

---

### OPTION 4: Scrapy + Playwright (ADVANCED DIY)

**Status:** Custom solution
**Cost:** FREE
**Complexity:** HIGH

**Use when:** Need full customization and willing to maintain scraper

**Pros:**
- Complete control
- Can scrape anything visible
- No API costs

**Cons:**
- Requires 8-15 hours/month maintenance
- TikTok changes defenses 1-2x per month
- X-Gorgon header challenges
- IP rotation needed
- Not recommended unless expert

---

## RECOMMENDED IMPLEMENTATION STRATEGY

### Phase 1: Quick Win (YouTube Only) - 1 hour
✅ Use existing YouTube API
✅ Collect 150-200 videos
✅ Analyze titles, descriptions, tags
✅ Extract consumer language patterns
**Cost:** FREE
**Output:** Comprehensive YouTube insights

### Phase 2: TikTok via Apify (Easiest) - 30 min
✅ Use existing Apify credentials
✅ Collect 300-500 hashtag videos
✅ Extract captions, hashtags, trends
**Cost:** ~$5-10
**Output:** TikTok consumer language + trends

### Phase 3: TikTok-Api Library (Best Long-term) - 2 hours setup
✅ Install TikTok-Api Python library
✅ Get ms_token from cookies (one-time)
✅ Build custom scraper for specific needs
**Cost:** FREE
**Output:** Unlimited TikTok data

---

## DATA ANALYSIS APPROACH

Once data collected, analyze with Claude Code for:

### Consumer Language Extraction:
- Unique terms/slang not in retailer copy
- Pain points mentioned repeatedly
- Aspirational language ("dream garage", "finally organized")
- DIY techniques discussed
- Product features consumers care about

### Trend Identification:
- Viral hashtags gaining momentum
- Popular sounds/music (indicates viral potential)
- Emerging subcategories
- Seasonal patterns
- Geographic variations

### Sentiment Analysis:
- Frustration vs. satisfaction
- Common complaints
- Success stories
- Unmet needs

---

## FINAL RECOMMENDATION

**For Maximum Impact with Minimum Effort:**

1. **YouTube (Immediate):** Run collection today using existing API
   - 6 searches × 30 videos = 180 videos
   - FREE, 10 minutes, comprehensive metadata

2. **TikTok Option A (Fast):** Apify scraper if budget allows
   - 3 hashtags × 200 videos = 600 TikToks
   - $5-10, 20 minutes, captions + engagement

3. **TikTok Option B (Free but slower):** TikTok-Api library
   - Same data as Option A
   - FREE, 2 hours setup + 30 min collection
   - Reusable for future projects

**Combined Output:**
- 180 YouTube videos (titles, descriptions, tags, engagement)
- 600 TikTok videos (captions, hashtags, sounds, engagement)
- Rich consumer language dataset
- Trend identification
- Pain point analysis

**Total Cost:** $0-10 depending on TikTok approach
**Total Time:** 3-5 hours
**Strategic Value:** HIGH - fills critical consumer insights gap

---

## NEXT STEPS

1. ✅ Confirm approach preference (Apify vs. TikTok-Api)
2. Run YouTube collection (ready now)
3. Execute TikTok collection
4. Analyze combined dataset with Claude Code
5. Update CONSUMER_LANGUAGE_REPORT.md with findings
6. Identify new consumer terms for marketing/SEO
