# Product Requirements Document: Creator Intelligence Module

**Version:** 1.0.0
**Status:** Pre-Development
**Last Updated:** 2025-10-10
**Owner:** 3M Lighting Project Team

---

## 🎯 Executive Summary

The Creator Intelligence Module analyzes creators across YouTube, Etsy, Instagram, and TikTok to discover lighting trends, extract consumer language for marketing, and build a scored database of potential brand partners and research participants.

### Primary Objectives

1. **Creator Trend Analysis**: Understand what creators in the lighting/home improvement space are working on, their pain points, projects, and language patterns
2. **Consumer Language Dictionary**: Extract real consumer terminology used for lighting products, pain points, and jobs-to-be-done to inform marketing messaging
3. **Partnership Database**: Build scored catalog of creators suitable for brand partnerships or consumer research, with geographic and audience filtering

### Key Differentiators

- **Multi-Platform Coverage**: YouTube, Etsy, Instagram, TikTok (first module to cover visual social platforms)
- **Hybrid Scripted/Agentic**: 70% scripted (APIs, DB, metrics) + 30% agentic (LLM classification) - not keyword-dependent
- **Viability Scoring**: Research score (0-100) and Partnership score (0-100) for each creator
- **Grey-Area Scraping**: Aggressive tactics for Instagram/TikTok where official APIs are unavailable
- **Future UI-Ready**: Database designed for eventual frontend exposure to client

---

## 📊 System Architecture

### Three-Tier Data Collection Strategy

| Tier | Method | Platforms | Cost | Stability | Use Case |
|------|--------|-----------|------|-----------|----------|
| **Tier 1** | Official APIs | YouTube, Etsy | Free (quota limits) | ⭐⭐⭐⭐⭐ | Primary data collection |
| **Tier 2** | Managed Scrapers | Instagram, TikTok (Apify) | $0-49/month | ⭐⭐⭐⭐ | Stable grey-area |
| **Tier 3** | Aggressive Scraping | Instagram (Instaloader), TikTok (Playwright) | Free | ⭐⭐⭐ | Fallback when Tier 2 fails |

### Data Flow

```
1. DISCOVERY PHASE
   ├─ YouTube Data API v3: Search creators by lighting keywords
   ├─ Etsy API v3: Find shops selling lighting solutions
   ├─ Instagram Apify: Search hashtags (#LEDlighting, #homeimprovement)
   └─ TikTok Apify: Search hashtags + trending creators

2. ENRICHMENT PHASE
   ├─ Scrape creator profiles (followers, engagement, content frequency)
   ├─ Scrape recent content (titles, descriptions, comments)
   └─ Extract geographic data (country, language, timezone)

3. ANALYSIS PHASE (LLM - Claude Sonnet 4)
   ├─ Content relevance classification (not keyword-based)
   ├─ Pain point detection from descriptions/comments
   ├─ Consumer language extraction (JTBD terms, product mentions)
   ├─ Theme clustering (installation, troubleshooting, design, reviews)
   └─ Brand alignment assessment

4. SCORING PHASE
   ├─ Research Viability Score: engagement (30%) + authenticity (20%) + content quality (25%) + relevance (15%) + geo-match (10%)
   └─ Partnership Viability Score: brand alignment (30%) + audience size (25%) + professionalism (20%) + consistency (15%) + prior partnerships (10%)

5. OUTPUT PHASE
   ├─ SQLite Database: creators, creator_content, consumer_language tables
   ├─ HTML Report: Top creators, trending themes, consumer language dictionary
   ├─ JSON Export: Full dataset for future UI integration
   └─ Excel Workbook: Filterable creator database (geography, followers, scores)
```

---

## 🔧 Platform-Specific Implementation

### YouTube Data API v3

**Method:** Official REST API
**Authentication:** API key
**Quota:** 10,000 units/day (search = 100 units = 100 searches/day)
**Stability:** ⭐⭐⭐⭐⭐

**Data Collected:**
- Channel metadata (subscribers, views, video count)
- Recent video titles/descriptions
- Video comments (top-level only)
- Geographic location (if public)
- Upload frequency

**Rate Limits:**
- 100 search queries per day (default quota)
- Quota increase requires compliance audit
- Aggressive caching required

**Code Example:**
```python
from googleapiclient.discovery import build

youtube = build('youtube', 'v3', developerKey=API_KEY)

search_response = youtube.search().list(
    q='LED lighting installation tutorial',
    type='channel',
    part='snippet',
    maxResults=50,
    relevanceLanguage='en',
    regionCode='US'
).execute()
```

---

### Etsy API v3

**Method:** Official REST API
**Authentication:** OAuth 2.0
**Quota:** 10,000 requests/day, 10 requests/second
**Stability:** ⭐⭐⭐⭐⭐

**Data Collected:**
- Shop metadata (sales, reviews, location)
- Product listings (titles, descriptions, tags)
- Review content (ratings, verbatim feedback)
- Price points and categories
- Shop policies and about text

**Rate Limits:**
- 10,000 requests/day
- 10 requests/second burst limit
- Supports pagination for bulk collection

**Code Example:**
```python
import requests

headers = {'Authorization': f'Bearer {oauth_token}'}

shops = requests.get(
    'https://openapi.etsy.com/v3/application/shops',
    params={
        'shop_name': 'lighting',
        'limit': 100
    },
    headers=headers
).json()
```

---

### Instagram (Apify Primary)

**Method:** Apify Instagram Scraper (commercial but stable)
**Authentication:** Apify API token
**Quota:** 5,000 free credits/month (≈500 profiles)
**Stability:** ⭐⭐⭐⭐

**Data Collected:**
- Profile metadata (followers, following, posts)
- Recent post captions and hashtags
- Engagement metrics (likes, comments per post)
- Bio/contact information
- Verified/business account status

**Rate Limits:**
- 5,000 Apify credits/month free tier
- 1 profile = ~10 credits
- $49/month for 50,000 credits if needed

**Code Example:**
```python
from apify_client import ApifyClient

client = ApifyClient(APIFY_TOKEN)

run = client.actor("apify/instagram-scraper").call(
    run_input={
        "username": ["lightingdesigner123"],
        "resultsType": "posts",
        "resultsLimit": 50
    }
)
```

**Fallback Method:** Instaloader with extreme rate limiting

---

### Instagram (Instaloader Fallback)

**Method:** Instaloader Python library (aggressive scraping)
**Authentication:** Instagram session cookies (optional)
**Quota:** None (but high ban risk)
**Stability:** ⭐⭐⭐

**Risk Mitigation:**
- 2-3 requests per minute maximum
- Random delays (120-180 seconds between profiles)
- User-agent rotation
- Proxy rotation (if available)
- No login required for public profiles
- Cache everything aggressively

**Code Example:**
```python
import instaloader
import time
import random

L = instaloader.Instaloader(
    download_videos=False,
    download_pictures=False,
    save_metadata=False
)

def get_profile_safe(username):
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        time.sleep(random.randint(120, 180))  # 2-3 min delay
        return profile
    except Exception as e:
        logger.error(f"Failed: {e}")
        return None
```

---

### TikTok (Apify Primary)

**Method:** Apify TikTok Scraper (commercial but stable)
**Authentication:** Apify API token
**Quota:** 5,000 free credits/month
**Stability:** ⭐⭐⭐⭐

**Data Collected:**
- Creator profile (followers, likes, videos)
- Recent video metadata (views, likes, comments)
- Video captions and hashtags
- Trending sounds/effects used
- Geographic signals (if available)

**Rate Limits:**
- 5,000 Apify credits/month free tier
- 1 profile = ~15 credits
- Shared quota with Instagram Apify usage

**Code Example:**
```python
from apify_client import ApifyClient

client = ApifyClient(APIFY_TOKEN)

run = client.actor("apify/tiktok-scraper").call(
    run_input={
        "profiles": ["@lightinghacks"],
        "resultsPerPage": 50
    }
)
```

**Fallback Method:** Playwright headless browser automation

---

### TikTok (Playwright Fallback)

**Method:** Playwright headless browser (aggressive scraping)
**Authentication:** None
**Quota:** None (high detection risk)
**Stability:** ⭐⭐⭐

**Risk Mitigation:**
- Headless browser with stealth plugins
- Realistic user behavior simulation (scroll, wait, click)
- JavaScript puzzle solving (TikTok's anti-bot challenge)
- Proxy rotation mandatory
- Maximum 10 profiles per session
- Session recycling every 20 requests

**Code Example:**
```python
from playwright.sync_api import sync_playwright

def scrape_tiktok_profile(username):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 ...',
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()

        page.goto(f'https://www.tiktok.com/@{username}')
        page.wait_for_selector('.profile-header', timeout=10000)

        # Extract data from DOM
        followers = page.locator('.follower-count').text_content()

        browser.close()
        return {'username': username, 'followers': followers}
```

---

## 🧠 LLM Integration (Claude Sonnet 4)

### Content Relevance Classification

**Problem:** Keywords miss implicit mentions and context
**Solution:** LLM classification with confidence scores

**Prompt Template:**
```
Analyze if this creator content is relevant to residential/commercial LED lighting:

Platform: {platform}
Creator: {username}
Title: {title}
Description: {description}
Hashtags: {hashtags}

Consider:
1. Installation, retrofit, or upgrade projects
2. Product reviews, comparisons, or recommendations
3. Troubleshooting, repair, or maintenance content
4. Design inspiration, aesthetics, or ambiance
5. DIY tutorials or professional walkthroughs

Respond in JSON:
{
  "is_relevant": true/false,
  "confidence": 0.0-1.0,
  "primary_theme": "installation|review|troubleshooting|design",
  "reasoning": "brief explanation"
}
```

---

### Pain Point Extraction

**Prompt Template:**
```
Extract lighting-related pain points from this creator content:

Content: {title + description + top_comments}

Identify specific problems, frustrations, or challenges mentioned:
- Technical issues (flickering, compatibility, installation difficulty)
- Aesthetic concerns (color temperature, dimming, brightness)
- Cost/value complaints
- Safety or durability issues

Respond in JSON:
{
  "pain_points": [
    {"text": "verbatim quote", "category": "technical|aesthetic|cost|safety"}
  ]
}
```

---

### Consumer Language Extraction

**Prompt Template:**
```
Extract consumer language terms from this content:

Content: {aggregated_descriptions_and_comments}

Identify:
1. Product names (brand names, product types)
2. Feature descriptions (warm white, color-changing, motion-activated)
3. Job-to-be-done phrases (brighten up my kitchen, create ambiance)
4. Pain point language (too dim, harsh light, difficult to install)

Respond in JSON:
{
  "terms": [
    {"term": "string", "category": "product|feature|job|pain", "frequency": int}
  ]
}
```

---

## 📊 Database Schema

### SQLite (Phase 1)

**Rationale:** Sufficient for 1,000s of creators, zero infrastructure, easy Python integration

**Tables:**

#### `creators`
```sql
CREATE TABLE creators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform TEXT NOT NULL,  -- youtube, etsy, instagram, tiktok
    username TEXT NOT NULL,
    display_name TEXT,
    url TEXT UNIQUE,

    -- Metrics
    followers INTEGER,
    following INTEGER,
    total_posts INTEGER,
    avg_engagement_rate REAL,  -- (likes + comments) / followers
    content_frequency TEXT,  -- daily, weekly, monthly, irregular

    -- Geographic
    country TEXT,
    region TEXT,
    language TEXT,
    timezone TEXT,

    -- Content Analysis (JSON fields for flexibility)
    primary_niche TEXT,  -- lighting_installation, home_improvement, product_review
    content_themes JSON,  -- ["installation", "troubleshooting", "reviews"]
    pain_points_mentioned JSON,  -- [{"text": "...", "category": "technical"}]
    consumer_language JSON,  -- [{"term": "warm white", "frequency": 5}]

    -- Scoring (0-100 scale)
    research_viability_score INTEGER,
    partnership_viability_score INTEGER,
    brand_safety_score INTEGER,

    -- Metadata
    is_verified BOOLEAN DEFAULT 0,
    is_business_account BOOLEAN DEFAULT 0,
    last_scraped TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(platform, username)
);

CREATE INDEX idx_platform ON creators(platform);
CREATE INDEX idx_research_score ON creators(research_viability_score DESC);
CREATE INDEX idx_partnership_score ON creators(partnership_viability_score DESC);
CREATE INDEX idx_country ON creators(country);
```

#### `creator_content`
```sql
CREATE TABLE creator_content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creator_id INTEGER NOT NULL REFERENCES creators(id) ON DELETE CASCADE,

    -- Content metadata
    content_type TEXT,  -- video, post, listing, story
    content_url TEXT UNIQUE,
    title TEXT,
    description TEXT,
    thumbnail_url TEXT,

    -- Engagement
    published_date TIMESTAMP,
    views INTEGER,
    likes INTEGER,
    comments_count INTEGER,
    shares INTEGER,
    engagement_rate REAL,

    -- Analysis (JSON)
    extracted_language JSON,  -- [{"term": "LED strip", "category": "product"}]
    pain_points JSON,  -- [{"text": "too dim", "category": "aesthetic"}]
    themes JSON,  -- ["installation", "review"]

    -- Metadata
    is_relevant BOOLEAN DEFAULT 1,
    relevance_confidence REAL,  -- 0.0-1.0 from LLM
    analyzed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (creator_id) REFERENCES creators(id)
);

CREATE INDEX idx_creator_content ON creator_content(creator_id);
CREATE INDEX idx_published_date ON creator_content(published_date DESC);
CREATE INDEX idx_engagement ON creator_content(engagement_rate DESC);
```

#### `consumer_language`
```sql
CREATE TABLE consumer_language (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    term TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,  -- pain_point, job, feature, product, brand

    -- Frequency tracking
    total_mentions INTEGER DEFAULT 1,
    platforms JSON,  -- {"youtube": 10, "etsy": 5, "instagram": 3}

    -- Examples (for marketing context)
    example_quotes JSON,  -- [{"text": "...", "creator": "...", "platform": "..."}]

    -- Related terms
    synonyms JSON,  -- ["warm white", "soft white", "2700K"]
    co_occurring_terms JSON,  -- ["dimmer", "dimmable", "adjustable brightness"]

    -- Metadata
    first_seen TIMESTAMP,
    last_seen TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_term ON consumer_language(term);
CREATE INDEX idx_category ON consumer_language(category);
CREATE INDEX idx_mentions ON consumer_language(total_mentions DESC);
```

---

### PostgreSQL Migration Plan (Phase 2 - UI Development)

**When to migrate:**
- Client UI development begins
- Need for concurrent access (multiple users)
- Advanced analytics (joins, aggregations, full-text search)

**Migration script:**
```bash
# Export SQLite to SQL
sqlite3 creators.db .dump > creators_backup.sql

# Convert to PostgreSQL syntax (minor tweaks)
sed 's/AUTOINCREMENT/SERIAL/g' creators_backup.sql > creators_postgres.sql

# Import to PostgreSQL
psql -U postgres -d creator_intelligence < creators_postgres.sql
```

**PostgreSQL enhancements:**
- Full-text search on descriptions (tsvector)
- PostGIS for geographic queries
- Partitioning by platform for performance
- JSON indexing (GIN indexes)

---

## 🎯 Scoring Algorithms

### Research Viability Score (0-100)

**Purpose:** How suitable is this creator for consumer research studies?

**Formula:**
```python
research_score = (
    engagement_rate_percentile * 0.30 +  # High engagement = active audience
    authenticity_score * 0.20 +           # Real person, not bot/spam
    content_quality_score * 0.25 +        # Production value, clarity
    relevance_score * 0.15 +              # On-topic for lighting
    geo_match_score * 0.10                # Target market alignment
)
```

**Component Details:**

1. **Engagement Rate Percentile** (0-100)
   - Calculate: `(likes + comments) / followers * 100`
   - Compare to platform benchmarks (YouTube: 3-5%, Instagram: 1-3%, TikTok: 5-10%)
   - Higher = more engaged audience

2. **Authenticity Score** (0-100)
   - Verified account: +30 points
   - Consistent posting history: +20 points
   - Real profile photo/bio: +20 points
   - No spam indicators: +30 points

3. **Content Quality Score** (0-100)
   - Video/image resolution: +25 points (1080p+)
   - Audio quality: +25 points (clear, no background noise)
   - Lighting/composition: +25 points (well-lit, framed)
   - Editing quality: +25 points (cuts, transitions, text overlays)

4. **Relevance Score** (0-100)
   - LLM confidence from content classification
   - 90%+ confidence = 100 points
   - 70-90% confidence = 70 points
   - <70% confidence = exclude

5. **Geo Match Score** (0-100)
   - Target country (US/Canada/UK/Australia): 100 points
   - Europe: 75 points
   - Other English-speaking: 50 points
   - Non-target markets: 25 points

---

### Partnership Viability Score (0-100)

**Purpose:** How suitable is this creator for paid brand partnerships?

**Formula:**
```python
partnership_score = (
    brand_alignment_score * 0.30 +       # Values, aesthetics, messaging fit
    audience_size_percentile * 0.25 +    # Reach potential
    professionalism_score * 0.20 +       # Communication, reliability signals
    consistency_score * 0.15 +           # Regular posting schedule
    prior_partnerships_score * 0.10      # Experience with brand deals
)
```

**Component Details:**

1. **Brand Alignment Score** (0-100)
   - LLM assessment of content tone, values, aesthetics
   - Family-friendly content: +30 points
   - Professional presentation: +30 points
   - Positive sentiment: +20 points
   - No controversial topics: +20 points

2. **Audience Size Percentile** (0-100)
   - Compare to platform benchmarks
   - YouTube: 10K+ subs = 50 points, 100K+ = 100 points
   - Instagram: 5K+ followers = 50 points, 50K+ = 100 points
   - TikTok: 10K+ followers = 50 points, 100K+ = 100 points

3. **Professionalism Score** (0-100)
   - Business account: +30 points
   - Contact info in bio: +20 points
   - Media kit or rate card: +30 points
   - Professional bio language: +20 points

4. **Consistency Score** (0-100)
   - Daily posting: 100 points
   - Weekly posting: 75 points
   - Monthly posting: 50 points
   - Irregular: 25 points

5. **Prior Partnerships Score** (0-100)
   - Detect #ad, #sponsored, brand mentions in captions
   - 5+ prior partnerships: 100 points
   - 1-4 partnerships: 50 points
   - No partnerships: 25 points (not necessarily bad)

---

## 📊 Output Formats

### HTML Report

**Structure:**
```html
<html>
<head><title>Creator Intelligence Report - {project_name}</title></head>
<body>
  <h1>Creator Intelligence Report</h1>
  <section id="executive-summary">
    <h2>Executive Summary</h2>
    <p>Analyzed {total_creators} creators across {platforms}</p>
    <p>Top themes: {top_3_themes}</p>
    <p>Key pain points: {top_5_pain_points}</p>
  </section>

  <section id="top-creators">
    <h2>Top Creators for Research</h2>
    <table>
      <thead>
        <tr><th>Creator</th><th>Platform</th><th>Followers</th><th>Research Score</th><th>Partnership Score</th></tr>
      </thead>
      <tbody>
        <!-- Top 50 creators by research score -->
      </tbody>
    </table>
  </section>

  <section id="consumer-language">
    <h2>Consumer Language Dictionary</h2>
    <h3>Pain Points</h3>
    <ul>
      <!-- Top 20 pain point terms with frequencies -->
    </ul>
    <h3>Product Features</h3>
    <ul>
      <!-- Top 20 feature terms -->
    </ul>
    <h3>Jobs-to-be-Done</h3>
    <ul>
      <!-- Top 20 JTBD phrases -->
    </ul>
  </section>

  <section id="trending-themes">
    <h2>Creator Trends</h2>
    <ul>
      <!-- Top themes with example creators -->
    </ul>
  </section>
</body>
</html>
```

---

### Excel Workbook (Tier 2+)

**Sheets:**

1. **Summary**
   - Total creators analyzed
   - Platform breakdown
   - Top themes
   - Date range
   - Methodology notes

2. **Top Creators (Research)**
   - Columns: Creator, Platform, URL, Followers, Engagement Rate, Research Score, Country, Language, Primary Niche
   - Sortable, filterable
   - Hyperlinks to profiles

3. **Top Creators (Partnership)**
   - Columns: Creator, Platform, URL, Followers, Partnership Score, Brand Alignment, Professionalism, Prior Partnerships
   - Contact info if available

4. **Consumer Language Dictionary**
   - Columns: Term, Category, Total Mentions, YouTube Mentions, Etsy Mentions, Instagram Mentions, TikTok Mentions, Example Quote
   - Sortable by frequency

5. **Trending Themes**
   - Columns: Theme, Creator Count, Platforms, Example Creators
   - Links to example content

6. **Pain Points Analysis**
   - Columns: Pain Point, Category (technical/aesthetic/cost/safety), Frequency, Platforms, Example Quotes
   - Sentiment scoring

7. **Raw Data**
   - Full creator dataset (all fields)
   - For advanced filtering/analysis

---

### JSON Export

**Structure:**
```json
{
  "metadata": {
    "generated_at": "2025-10-10T15:30:00Z",
    "total_creators": 347,
    "platforms": ["youtube", "etsy", "instagram", "tiktok"],
    "date_range": {"start": "2025-09-01", "end": "2025-10-10"}
  },
  "creators": [
    {
      "id": 1,
      "platform": "youtube",
      "username": "lightingguru123",
      "display_name": "Lighting Guru",
      "url": "https://youtube.com/c/lightingguru123",
      "followers": 45000,
      "engagement_rate": 0.045,
      "research_score": 87,
      "partnership_score": 72,
      "country": "US",
      "primary_niche": "lighting_installation",
      "content_themes": ["installation", "troubleshooting"],
      "pain_points": [{"text": "LED strips too dim", "category": "aesthetic"}]
    }
  ],
  "consumer_language": [
    {
      "term": "warm white",
      "category": "feature",
      "mentions": 234,
      "platforms": {"youtube": 120, "etsy": 80, "instagram": 34},
      "examples": ["looking for warm white bulbs for my living room"]
    }
  ],
  "trending_themes": [
    {
      "theme": "LED strip installation",
      "creator_count": 87,
      "platforms": ["youtube", "tiktok"],
      "top_creators": ["lightingguru123", "diyhomehacks"]
    }
  ]
}
```

---

## 🧪 Testing Strategy

### Unit Tests

**Scrapers:**
- Test YouTube API authentication
- Test Etsy OAuth flow
- Test Apify client initialization
- Test Instaloader rate limiting logic
- Test Playwright browser launch

**Analyzers:**
- Test LLM prompt formatting
- Test JSON response parsing
- Test scoring algorithms with known inputs
- Test consumer language extraction

**Database:**
- Test SQLite connection
- Test CRUD operations
- Test JSON field serialization
- Test unique constraint enforcement

---

### Integration Tests

**End-to-End Flows:**
1. Scrape 5 YouTube creators → store in DB → verify data
2. Scrape 5 Etsy shops → extract language → verify consumer_language table
3. Classify 10 pieces of content with LLM → verify accuracy
4. Generate HTML report → verify all sections present
5. Generate Excel workbook → verify all sheets present

**Failover Tests:**
- Simulate Apify quota exhaustion → verify Instaloader fallback
- Simulate TikTok detection → verify Playwright fallback
- Simulate YouTube quota exhaustion → verify graceful degradation

---

### Preflight Checklist

**Before Full Deployment:**

- [ ] YouTube API key created and quota verified
- [ ] Etsy OAuth app created and credentials stored
- [ ] Apify account created with 5,000 free credits
- [ ] Instaloader installed and tested on 1 profile
- [ ] Playwright installed with chromium browser
- [ ] Claude Sonnet 4 API key valid and tested
- [ ] SQLite database created with schema
- [ ] Test scrape of 5 creators per platform successful
- [ ] Test LLM classification on 10 content pieces
- [ ] Test scoring algorithm with manual verification
- [ ] Test HTML report generation
- [ ] Test Excel export with openpyxl
- [ ] Test failover from Apify → Instaloader
- [ ] Test failover from Apify → Playwright
- [ ] Verify all data cached to minimize re-scraping
- [ ] Documentation complete (README, usage examples)

---

## 🚨 Risk Assessment

### High-Risk Areas

**Instagram Scraping (Instaloader):**
- **Risk:** Account bans, 429 errors, IP blocks
- **Mitigation:**
  - Use as fallback only (after Apify fails)
  - 2-3 min delays between requests
  - No login (public profiles only)
  - Proxy rotation if available
  - Aggressive caching (never re-scrape)

**TikTok Scraping (Playwright):**
- **Risk:** JavaScript puzzles, CAPTCHA, bot detection
- **Mitigation:**
  - Use as last resort (after Apify fails)
  - Stealth plugins to mask headless browser
  - Session recycling (new browser every 20 requests)
  - Proxy rotation mandatory
  - Maximum 10 profiles per session

**YouTube Quota Exhaustion:**
- **Risk:** 10,000 units/day = only 100 searches
- **Mitigation:**
  - Cache all search results aggressively
  - Request quota increase (requires compliance audit)
  - Focus on high-quality searches (targeted keywords)
  - Use Etsy/Instagram to discover creators, verify on YouTube

**Apify Cost Overrun:**
- **Risk:** 5,000 free credits = ~500 Instagram profiles OR ~333 TikTok profiles
- **Mitigation:**
  - Monitor credit usage with Apify dashboard
  - Set hard limit alerts at 4,000 credits
  - Transition to paid tier ($49/month for 50,000 credits) if needed
  - Prioritize high-value creators first

---

### Medium-Risk Areas

**LLM Classification Accuracy:**
- **Risk:** False positives (irrelevant creators classified as relevant)
- **Mitigation:**
  - Manual spot-check of 50 creators
  - Require 70%+ confidence threshold
  - A/B test different prompt templates

**Database Scalability:**
- **Risk:** SQLite performance degrades beyond 10,000 creators
- **Mitigation:**
  - Add indexes on frequently queried fields
  - Migrate to PostgreSQL if scaling beyond 5,000 creators
  - Monitor query performance logs

---

### Low-Risk Areas

**YouTube/Etsy API Changes:**
- **Risk:** Official APIs change structure
- **Mitigation:**
  - Monitor API changelogs
  - Wrap API calls in try/except with detailed logging
  - Graceful degradation if endpoints fail

---

## 📅 Development Roadmap

### Phase 1: Foundation (Weeks 1-2)

**Week 1:**
- [ ] Module structure setup (config/, core/, scrapers/, analyzers/, reporters/)
- [ ] YouTube Data API integration with caching
- [ ] Etsy API v3 integration with OAuth
- [ ] SQLite database setup with schema
- [ ] Basic scraper testing (10 creators per platform)

**Week 2:**
- [ ] LLM content classification implementation
- [ ] Pain point extraction with Claude Sonnet 4
- [ ] Consumer language extraction
- [ ] Research viability scoring algorithm
- [ ] Partnership viability scoring algorithm

---

### Phase 2: Grey-Area Scraping (Weeks 3-4)

**Week 3:**
- [ ] Apify Instagram Scraper integration
- [ ] Apify TikTok Scraper integration
- [ ] Credit monitoring and quota alerts
- [ ] Failover logic (Apify → fallback methods)

**Week 4:**
- [ ] Instaloader Instagram fallback with rate limiting
- [ ] Playwright TikTok fallback with stealth
- [ ] Anti-detection techniques (user-agent rotation, delays)
- [ ] Proxy rotation setup (if available)

---

### Phase 3: Reporting & Testing (Week 5)

- [ ] HTML report generation with all sections
- [ ] Excel workbook generation (7 sheets)
- [ ] JSON export for future UI
- [ ] Comprehensive integration tests
- [ ] Manual validation of 50 creators
- [ ] Documentation (README, usage examples, troubleshooting)

---

### Phase 4: Optimization (Week 6)

- [ ] Performance profiling (identify bottlenecks)
- [ ] Caching optimizations
- [ ] Batch processing for large creator sets
- [ ] Error recovery and retry logic
- [ ] Production deployment checklist

---

## 💡 Future Enhancements

### Short-Term (Post-Launch)

1. **Geographic Filtering UI**
   - Select target countries/regions
   - Filter by language preference
   - Timezone-aware scheduling

2. **Advanced Scoring**
   - Historical engagement trends (growing vs declining)
   - Sentiment analysis on comments
   - Brand mention frequency scoring

3. **Automated Monitoring**
   - Weekly creator updates (new content, follower growth)
   - Alert on significant changes (viral content, account deactivation)

---

### Long-Term (UI Development)

1. **Client-Facing Dashboard**
   - Browse creators with filters (score, platform, geo)
   - View creator profiles with embedded content
   - Export custom creator lists for outreach

2. **Partnership Management**
   - Track outreach status (contacted, replied, negotiating, closed)
   - Store contact information and communication logs
   - ROI tracking for paid partnerships

3. **Trend Analysis**
   - Time-series charts of theme popularity
   - Consumer language evolution over time
   - Competitive creator analysis (benchmark against competitors)

---

## 📜 Compliance & Ethics

### Fair Use Considerations

**Grey-Area Disclaimer:**
- This module uses scraping methods that may violate platform Terms of Service
- Data collection is for market research and competitive intelligence
- No user authentication is stored or transmitted
- All scraped data is for internal use only (not redistributed)

**Recommended Best Practices:**
- Obtain legal review before commercial deployment
- Respect robots.txt where implemented
- Honor rate limits and throttling
- Do not scrape personal/private information
- Comply with GDPR/CCPA data privacy laws

---

### Data Retention Policy

**Recommended Retention:**
- Creator profiles: 90 days (refresh monthly)
- Content metadata: 180 days
- Consumer language dictionary: Indefinite (aggregated data)
- Deleted accounts: Remove immediately upon detection

---

## 📚 References

### Platform Documentation

- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- [Etsy API v3](https://developers.etsy.com/documentation/)
- [Apify Instagram Scraper](https://apify.com/apify/instagram-scraper)
- [Apify TikTok Scraper](https://apify.com/apify/tiktok-scraper)
- [Instaloader Docs](https://instaloader.github.io/)
- [Playwright Python](https://playwright.dev/python/)

### Related Modules

- **Expert Authority Module**: Reddit/Stack Exchange analysis (production reference)
- **Consumer Video Module**: YouTube video JTBD analysis (shared analysis patterns)
- **YouTube Datasource Module**: Whisper + LLaVA pipeline (shared scraping logic)

---

**END OF PRD**

**Next Steps:**
1. Review this PRD for completeness and accuracy
2. Create remaining documentation (Technical Architecture, API Preflight, Risk Assessment, Database Schema)
3. Obtain stakeholder approval before implementation
4. Begin Phase 1 development (YouTube + Etsy + SQLite foundation)
