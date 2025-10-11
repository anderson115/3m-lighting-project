# Technical Architecture: Creator Intelligence Module

**Version:** 1.0.0
**Last Updated:** 2025-10-10
**Status:** Pre-Development

---

## 🏗️ System Overview

The Creator Intelligence Module is a hybrid scripted/agentic system (70% scripted / 30% LLM-powered) that collects, analyzes, and scores creators across 4 platforms using a three-tier data collection strategy with intelligent failover mechanisms.

### Core Design Principles

1. **Resilience Through Failover**: Every platform has primary → fallback → last-resort scraping methods
2. **API Quota Conservation**: Aggressive caching to minimize re-scraping and API calls
3. **Hybrid Analysis**: Scripted metrics (followers, engagement) + LLM semantic analysis (relevance, pain points)
4. **Database-Centric**: SQLite as single source of truth, reports generated from DB
5. **Modular & Extensible**: Easy to add new platforms or analysis modules

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                     ORCHESTRATOR (core/orchestrator.py)             │
│  - Coordinates all modules                                          │
│  - Manages execution flow                                           │
│  - Handles errors and retries                                       │
└─────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│   SCRAPERS       │       │   ANALYZERS      │       │   REPORTERS      │
│                  │       │                  │       │                  │
│ - YouTube        │──────▶│ - Content        │──────▶│ - HTML Report    │
│ - Etsy           │       │   Classifier     │       │ - Excel Workbook │
│ - Instagram      │       │ - Pain Point     │       │ - JSON Export    │
│ - TikTok         │       │   Detector       │       │                  │
│                  │       │ - Language       │       └──────────────────┘
│ (with failover)  │       │   Extractor      │
│                  │       │ - Creator Scorer │
└──────────────────┘       └──────────────────┘
        │                           │
        │                           │
        ▼                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                         DATABASE (SQLite)                            │
│  - creators table (profile data + scores)                            │
│  - creator_content table (posts/videos/listings)                     │
│  - consumer_language table (extracted marketing terms)               │
└──────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────────────────────┐
│                         CACHE (data/cache/)                          │
│  - Raw JSON responses from APIs                                      │
│  - Prevents re-scraping                                              │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Module Structure

```
modules/creator-intelligence/
├── README.md                       # User-facing documentation
├── config/
│   ├── .env.example                # API key template
│   ├── .env                        # Actual API keys (gitignored)
│   ├── .gitignore                  # Protect credentials
│   └── platforms.yaml              # Platform-specific configs
│
├── core/
│   ├── __init__.py
│   ├── config.py                   # Configuration loader
│   ├── orchestrator.py             # Main pipeline coordinator
│   └── database.py                 # SQLite connection & queries
│
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py             # Abstract base class
│   ├── youtube_scraper.py          # YouTube Data API v3
│   ├── etsy_scraper.py             # Etsy API v3 (OAuth)
│   ├── instagram_scraper.py        # Apify primary, Instaloader fallback
│   ├── tiktok_scraper.py           # Apify primary, Playwright fallback
│   ├── apify_client.py             # Apify SDK wrapper
│   └── failover_pool.py            # Scraper failover logic
│
├── analyzers/
│   ├── __init__.py
│   ├── content_classifier.py       # LLM relevance classification
│   ├── pain_point_detector.py      # Extract pain points with LLM
│   ├── language_extractor.py       # Consumer language extraction
│   ├── trend_analyzer.py           # Theme clustering
│   └── creator_scorer.py           # Research/partnership scoring
│
├── reporters/
│   ├── __init__.py
│   ├── html_reporter.py            # HTML report generation
│   ├── excel_reporter.py           # Excel workbook generation
│   └── json_exporter.py            # JSON export for UI
│
├── agents/
│   ├── __init__.py
│   ├── semantic_grouper.py         # LLM-based theme grouping
│   └── viability_assessor.py       # LLM brand alignment scoring
│
├── data/
│   ├── cache/                      # Raw scraped data (JSON)
│   │   ├── youtube/
│   │   ├── etsy/
│   │   ├── instagram/
│   │   └── tiktok/
│   ├── database/                   # SQLite database file
│   │   └── creators.db
│   ├── reports/                    # Generated reports
│   │   ├── *.html
│   │   ├── *.xlsx
│   │   └── *.json
│   └── language/                   # Consumer language dictionaries
│       └── *.json
│
├── docs/
│   ├── PRD-creator-intelligence.md
│   ├── TECHNICAL-ARCHITECTURE.md   # This file
│   ├── API-INTEGRATION-PREFLIGHT.md
│   ├── RISK-ASSESSMENT.md
│   └── DATABASE-SCHEMA.md
│
└── tests/
    ├── __init__.py
    ├── test_scrapers.py
    ├── test_analyzers.py
    ├── test_scoring.py
    └── test_end_to_end.py
```

---

## 🔧 Core Components

### Orchestrator (`core/orchestrator.py`)

**Responsibilities:**
- Coordinate scraping → analysis → scoring → reporting pipeline
- Manage platform-specific workflows
- Handle errors and retries
- Logging and progress tracking

**Key Methods:**
```python
class CreatorIntelligenceOrchestrator:
    def __init__(self, tier: int = 1):
        """Initialize with tier level (1=official APIs, 2=managed scrapers, 3=aggressive)"""
        self.tier = tier
        self.config = Config()
        self.db = Database()

    def run_analysis(
        self,
        platforms: List[str],
        keywords: List[str],
        target_creator_count: int = 100,
        geographic_filters: Dict = None
    ) -> Dict:
        """
        Main entry point for creator analysis.

        Returns:
            {
                'creators_discovered': int,
                'creators_analyzed': int,
                'database_path': str,
                'reports': {
                    'html': str,
                    'excel': str,
                    'json': str
                },
                'consumer_language_terms': int,
                'trending_themes': List[str]
            }
        """
        pass

    def _scrape_platform(self, platform: str, keywords: List[str]) -> List[Dict]:
        """Scrape creators from a single platform using failover logic"""
        pass

    def _analyze_content(self, creator_id: int) -> Dict:
        """Run LLM analysis on creator content"""
        pass

    def _score_creators(self) -> None:
        """Calculate research/partnership scores for all creators"""
        pass

    def _generate_reports(self) -> Dict:
        """Generate HTML, Excel, and JSON reports"""
        pass
```

**Execution Flow:**
```python
# Pseudocode
def run_analysis():
    for platform in platforms:
        # 1. DISCOVERY
        creators = scrape_platform(platform, keywords)  # Uses failover pool

        for creator in creators:
            # 2. ENRICHMENT
            profile = scrape_creator_profile(creator['username'])
            recent_content = scrape_creator_content(creator['username'], limit=20)

            # 3. STORAGE
            creator_id = db.insert_creator(profile)
            db.insert_content(creator_id, recent_content)

    # 4. ANALYSIS (LLM)
    for creator in db.get_all_creators():
        relevance = llm_classify_relevance(creator['content'])
        pain_points = llm_extract_pain_points(creator['content'])
        language = llm_extract_consumer_language(creator['content'])

        db.update_creator_analysis(creator['id'], relevance, pain_points, language)

    # 5. SCORING
    for creator in db.get_all_creators():
        research_score = calculate_research_score(creator)
        partnership_score = calculate_partnership_score(creator)

        db.update_creator_scores(creator['id'], research_score, partnership_score)

    # 6. REPORTING
    html_report = generate_html_report(db)
    excel_report = generate_excel_report(db)
    json_export = generate_json_export(db)

    return {
        'reports': {
            'html': html_report,
            'excel': excel_report,
            'json': json_export
        }
    }
```

---

### Database Layer (`core/database.py`)

**Responsibilities:**
- SQLite connection management
- CRUD operations for creators, content, language
- Query optimization with indexes
- JSON field serialization

**Key Methods:**
```python
class Database:
    def __init__(self, db_path: str = 'data/database/creators.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._initialize_schema()

    def insert_creator(self, profile: Dict) -> int:
        """Insert creator profile, return creator_id"""
        pass

    def insert_content(self, creator_id: int, content: List[Dict]) -> None:
        """Insert creator content (posts, videos, listings)"""
        pass

    def update_creator_analysis(self, creator_id: int, analysis: Dict) -> None:
        """Update creator with LLM analysis results"""
        pass

    def update_creator_scores(self, creator_id: int, research_score: int, partnership_score: int) -> None:
        """Update viability scores"""
        pass

    def get_all_creators(self, filters: Dict = None) -> List[Dict]:
        """Get all creators with optional filters (platform, country, min_score)"""
        pass

    def get_top_creators(self, score_type: str = 'research', limit: int = 50) -> List[Dict]:
        """Get top N creators by score"""
        pass

    def get_consumer_language(self, category: str = None, min_mentions: int = 5) -> List[Dict]:
        """Get consumer language terms"""
        pass

    def get_trending_themes(self, min_creator_count: int = 10) -> List[Dict]:
        """Get themes mentioned by multiple creators"""
        pass
```

**Example Query:**
```python
# Get top 50 US-based creators for research with scores > 70
creators = db.get_all_creators(filters={
    'country': 'US',
    'min_research_score': 70,
    'platforms': ['youtube', 'instagram'],
    'limit': 50,
    'order_by': 'research_viability_score DESC'
})
```

---

### Scraper Architecture (`scrapers/`)

#### Base Scraper (`base_scraper.py`)

**Abstract base class for all platform scrapers:**

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import logging

class BaseScraper(ABC):
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.cache_enabled = True
        self.cache_dir = f"data/cache/{self.platform_name}/"

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Return platform name (youtube, etsy, instagram, tiktok)"""
        pass

    @abstractmethod
    def search_creators(self, keywords: List[str], limit: int = 100) -> List[Dict]:
        """
        Search for creators by keywords.

        Returns:
            List of dicts with minimum fields:
            [
                {
                    'username': str,
                    'display_name': str,
                    'url': str,
                    'followers': int (if available)
                }
            ]
        """
        pass

    @abstractmethod
    def get_creator_profile(self, username: str) -> Optional[Dict]:
        """
        Get detailed creator profile.

        Returns:
            {
                'platform': str,
                'username': str,
                'display_name': str,
                'url': str,
                'followers': int,
                'following': int,
                'total_posts': int,
                'bio': str,
                'country': str,
                'language': str,
                'is_verified': bool,
                'is_business_account': bool,
                'last_scraped': str (ISO timestamp)
            }
        """
        pass

    @abstractmethod
    def get_creator_content(self, username: str, limit: int = 20) -> List[Dict]:
        """
        Get recent content from creator.

        Returns:
            [
                {
                    'content_type': 'video|post|listing',
                    'content_url': str,
                    'title': str,
                    'description': str,
                    'published_date': str (ISO timestamp),
                    'views': int,
                    'likes': int,
                    'comments_count': int,
                    'engagement_rate': float
                }
            ]
        """
        pass

    def _load_from_cache(self, cache_key: str) -> Optional[Dict]:
        """Load cached data if exists and not expired"""
        if not self.cache_enabled:
            return None

        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        if os.path.exists(cache_file):
            # Check if cache is < 30 days old
            if time.time() - os.path.getmtime(cache_file) < 30 * 24 * 3600:
                with open(cache_file, 'r') as f:
                    return json.load(f)
        return None

    def _save_to_cache(self, cache_key: str, data: Dict) -> None:
        """Save data to cache"""
        if not self.cache_enabled:
            return

        os.makedirs(self.cache_dir, exist_ok=True)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        with open(cache_file, 'w') as f:
            json.dump(data, f, indent=2)
```

---

#### YouTube Scraper (`youtube_scraper.py`)

**Implementation:**
```python
from googleapiclient.discovery import build
from scrapers.base_scraper import BaseScraper

class YouTubeScraper(BaseScraper):
    @property
    def platform_name(self) -> str:
        return 'youtube'

    def __init__(self, config: Dict):
        super().__init__(config)
        self.api_key = config['youtube_api_key']
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def search_creators(self, keywords: List[str], limit: int = 100) -> List[Dict]:
        """
        Search YouTube channels by keywords.
        Cost: 100 units per search (10,000 quota = 100 searches/day)
        """
        # Check cache first
        cache_key = f"search_{'_'.join(keywords)}"
        cached = self._load_from_cache(cache_key)
        if cached:
            self.logger.info(f"Loaded {len(cached)} creators from cache")
            return cached

        creators = []
        for keyword in keywords:
            response = self.youtube.search().list(
                q=keyword,
                type='channel',
                part='snippet',
                maxResults=min(50, limit),
                relevanceLanguage='en',
                order='relevance'
            ).execute()

            for item in response.get('items', []):
                creators.append({
                    'username': item['snippet']['channelId'],
                    'display_name': item['snippet']['title'],
                    'url': f"https://youtube.com/channel/{item['snippet']['channelId']}",
                    'followers': None  # Will get from get_creator_profile
                })

        # Save to cache
        self._save_to_cache(cache_key, creators)
        return creators[:limit]

    def get_creator_profile(self, username: str) -> Optional[Dict]:
        """
        Get YouTube channel details.
        Cost: 1 unit per channel
        """
        # Check cache
        cache_key = f"profile_{username}"
        cached = self._load_from_cache(cache_key)
        if cached:
            return cached

        try:
            response = self.youtube.channels().list(
                part='snippet,statistics,brandingSettings',
                id=username
            ).execute()

            if not response.get('items'):
                return None

            channel = response['items'][0]
            profile = {
                'platform': 'youtube',
                'username': username,
                'display_name': channel['snippet']['title'],
                'url': f"https://youtube.com/channel/{username}",
                'followers': int(channel['statistics']['subscriberCount']),
                'following': 0,  # YouTube doesn't expose this
                'total_posts': int(channel['statistics']['videoCount']),
                'bio': channel['snippet']['description'],
                'country': channel['snippet'].get('country', 'Unknown'),
                'language': channel['snippet'].get('defaultLanguage', 'en'),
                'is_verified': 'verified' in channel['snippet'].get('customUrl', ''),
                'is_business_account': False,  # Not exposed by API
                'last_scraped': datetime.utcnow().isoformat()
            }

            self._save_to_cache(cache_key, profile)
            return profile

        except Exception as e:
            self.logger.error(f"Error fetching profile for {username}: {e}")
            return None

    def get_creator_content(self, username: str, limit: int = 20) -> List[Dict]:
        """
        Get recent videos from channel.
        Cost: 1 unit to get upload playlist + 1 unit per 50 videos
        """
        # Check cache
        cache_key = f"content_{username}"
        cached = self._load_from_cache(cache_key)
        if cached:
            return cached[:limit]

        try:
            # Get uploads playlist ID
            channel_response = self.youtube.channels().list(
                part='contentDetails',
                id=username
            ).execute()

            if not channel_response.get('items'):
                return []

            uploads_playlist = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

            # Get videos from playlist
            videos = []
            playlist_response = self.youtube.playlistItems().list(
                part='snippet',
                playlistId=uploads_playlist,
                maxResults=limit
            ).execute()

            video_ids = [item['snippet']['resourceId']['videoId'] for item in playlist_response.get('items', [])]

            # Get video statistics
            stats_response = self.youtube.videos().list(
                part='statistics,snippet',
                id=','.join(video_ids)
            ).execute()

            for video in stats_response.get('items', []):
                stats = video['statistics']
                snippet = video['snippet']

                views = int(stats.get('viewCount', 0))
                likes = int(stats.get('likeCount', 0))
                comments = int(stats.get('commentCount', 0))

                # Engagement rate = (likes + comments) / views
                engagement_rate = (likes + comments) / views if views > 0 else 0

                videos.append({
                    'content_type': 'video',
                    'content_url': f"https://youtube.com/watch?v={video['id']}",
                    'title': snippet['title'],
                    'description': snippet['description'],
                    'published_date': snippet['publishedAt'],
                    'views': views,
                    'likes': likes,
                    'comments_count': comments,
                    'engagement_rate': engagement_rate
                })

            self._save_to_cache(cache_key, videos)
            return videos

        except Exception as e:
            self.logger.error(f"Error fetching content for {username}: {e}")
            return []
```

---

#### Instagram Scraper (`instagram_scraper.py`)

**Failover Implementation:**

```python
from scrapers.base_scraper import BaseScraper
from apify_client import ApifyClient
import instaloader
import time
import random

class InstagramScraper(BaseScraper):
    @property
    def platform_name(self) -> str:
        return 'instagram'

    def __init__(self, config: Dict):
        super().__init__(config)
        self.apify_token = config.get('apify_token')
        self.use_apify_primary = config.get('use_apify_primary', True)

        # Initialize Apify client
        if self.apify_token:
            self.apify_client = ApifyClient(self.apify_token)

        # Initialize Instaloader (fallback)
        self.instaloader = instaloader.Instaloader(
            download_videos=False,
            download_pictures=False,
            save_metadata=False,
            compress_json=False
        )

    def search_creators(self, keywords: List[str], limit: int = 100) -> List[Dict]:
        """
        Search Instagram creators by hashtags.

        Method priority:
        1. Apify Instagram Scraper (primary)
        2. Instaloader hashtag search (fallback)
        """
        # Try Apify first
        if self.use_apify_primary and self.apify_token:
            try:
                return self._search_creators_apify(keywords, limit)
            except Exception as e:
                self.logger.warning(f"Apify search failed: {e}. Falling back to Instaloader.")

        # Fallback to Instaloader
        return self._search_creators_instaloader(keywords, limit)

    def _search_creators_apify(self, keywords: List[str], limit: int) -> List[Dict]:
        """Use Apify Instagram Scraper"""
        # Convert keywords to hashtags
        hashtags = [f"#{kw.replace(' ', '')}" for kw in keywords]

        run_input = {
            "hashtags": hashtags,
            "resultsLimit": limit,
            "resultsType": "accounts"
        }

        run = self.apify_client.actor("apify/instagram-scraper").call(run_input=run_input)

        creators = []
        for item in self.apify_client.dataset(run["defaultDatasetId"]).iterate_items():
            creators.append({
                'username': item['username'],
                'display_name': item.get('fullName', item['username']),
                'url': f"https://instagram.com/{item['username']}",
                'followers': item.get('followersCount', 0)
            })

        return creators[:limit]

    def _search_creators_instaloader(self, keywords: List[str], limit: int) -> List[Dict]:
        """Fallback: Instaloader with extreme rate limiting"""
        creators = []

        for keyword in keywords:
            hashtag = keyword.replace(' ', '').lower()

            try:
                # Get posts from hashtag
                posts = instaloader.Hashtag.from_name(self.instaloader.context, hashtag).get_posts()

                # Extract unique creators
                seen_usernames = set()
                for post in posts:
                    if len(creators) >= limit:
                        break

                    username = post.owner_username
                    if username not in seen_usernames:
                        seen_usernames.add(username)
                        creators.append({
                            'username': username,
                            'display_name': username,
                            'url': f"https://instagram.com/{username}",
                            'followers': None  # Will get from profile
                        })

                    # CRITICAL: Rate limiting
                    time.sleep(random.randint(120, 180))  # 2-3 minutes between requests

            except Exception as e:
                self.logger.error(f"Error searching hashtag {hashtag}: {e}")
                continue

        return creators[:limit]

    def get_creator_profile(self, username: str) -> Optional[Dict]:
        """Get Instagram profile with failover"""
        # Try Apify first
        if self.use_apify_primary and self.apify_token:
            try:
                return self._get_profile_apify(username)
            except Exception as e:
                self.logger.warning(f"Apify profile fetch failed for {username}: {e}. Falling back to Instaloader.")

        # Fallback to Instaloader
        return self._get_profile_instaloader(username)

    def _get_profile_apify(self, username: str) -> Optional[Dict]:
        """Use Apify to get profile"""
        run_input = {
            "username": [username],
            "resultsType": "posts",
            "resultsLimit": 1  # Just need profile metadata
        }

        run = self.apify_client.actor("apify/instagram-scraper").call(run_input=run_input)

        for item in self.apify_client.dataset(run["defaultDatasetId"]).iterate_items():
            return {
                'platform': 'instagram',
                'username': item['username'],
                'display_name': item.get('fullName', item['username']),
                'url': f"https://instagram.com/{item['username']}",
                'followers': item.get('followersCount', 0),
                'following': item.get('followingCount', 0),
                'total_posts': item.get('postsCount', 0),
                'bio': item.get('biography', ''),
                'country': 'Unknown',  # Instagram doesn't expose this
                'language': 'en',
                'is_verified': item.get('verified', False),
                'is_business_account': item.get('isBusinessAccount', False),
                'last_scraped': datetime.utcnow().isoformat()
            }

        return None

    def _get_profile_instaloader(self, username: str) -> Optional[Dict]:
        """Fallback: Instaloader with rate limiting"""
        try:
            profile = instaloader.Profile.from_username(self.instaloader.context, username)

            # Calculate engagement rate from recent posts
            engagement_rate = 0
            post_count = 0
            for post in profile.get_posts():
                if post_count >= 12:  # Last 12 posts
                    break
                engagement = (post.likes + post.comments) / profile.followers if profile.followers > 0 else 0
                engagement_rate += engagement
                post_count += 1

            avg_engagement = engagement_rate / post_count if post_count > 0 else 0

            result = {
                'platform': 'instagram',
                'username': profile.username,
                'display_name': profile.full_name,
                'url': f"https://instagram.com/{profile.username}",
                'followers': profile.followers,
                'following': profile.followees,
                'total_posts': profile.mediacount,
                'bio': profile.biography,
                'country': 'Unknown',
                'language': 'en',
                'is_verified': profile.is_verified,
                'is_business_account': profile.is_business_account,
                'avg_engagement_rate': avg_engagement,
                'last_scraped': datetime.utcnow().isoformat()
            }

            # CRITICAL: Rate limiting
            time.sleep(random.randint(120, 180))  # 2-3 minutes

            return result

        except Exception as e:
            self.logger.error(f"Error fetching profile for {username}: {e}")
            return None
```

---

#### TikTok Scraper (`tiktok_scraper.py`)

**Playwright Fallback Implementation:**

```python
from scrapers.base_scraper import BaseScraper
from apify_client import ApifyClient
from playwright.sync_api import sync_playwright
import time
import random

class TikTokScraper(BaseScraper):
    @property
    def platform_name(self) -> str:
        return 'tiktok'

    def __init__(self, config: Dict):
        super().__init__(config)
        self.apify_token = config.get('apify_token')
        self.use_apify_primary = config.get('use_apify_primary', True)

        if self.apify_token:
            self.apify_client = ApifyClient(self.apify_token)

    def search_creators(self, keywords: List[str], limit: int = 100) -> List[Dict]:
        """Search TikTok creators with failover"""
        # Try Apify first
        if self.use_apify_primary and self.apify_token:
            try:
                return self._search_creators_apify(keywords, limit)
            except Exception as e:
                self.logger.warning(f"Apify search failed: {e}. Falling back to Playwright.")

        # Fallback to Playwright
        return self._search_creators_playwright(keywords, limit)

    def _search_creators_apify(self, keywords: List[str], limit: int) -> List[Dict]:
        """Use Apify TikTok Scraper"""
        hashtags = [f"#{kw.replace(' ', '')}" for kw in keywords]

        run_input = {
            "hashtags": hashtags,
            "resultsPerPage": limit
        }

        run = self.apify_client.actor("apify/tiktok-scraper").call(run_input=run_input)

        creators = []
        seen_usernames = set()

        for item in self.apify_client.dataset(run["defaultDatasetId"]).iterate_items():
            username = item['authorMeta']['name']
            if username not in seen_usernames:
                seen_usernames.add(username)
                creators.append({
                    'username': username,
                    'display_name': item['authorMeta'].get('nickName', username),
                    'url': f"https://tiktok.com/@{username}",
                    'followers': item['authorMeta'].get('fans', 0)
                })

        return creators[:limit]

    def _search_creators_playwright(self, keywords: List[str], limit: int) -> List[Dict]:
        """Fallback: Playwright headless browser"""
        creators = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                viewport={'width': 1920, 'height': 1080}
            )
            page = context.new_page()

            for keyword in keywords:
                hashtag = keyword.replace(' ', '').lower()

                try:
                    # Navigate to hashtag page
                    page.goto(f'https://www.tiktok.com/tag/{hashtag}', timeout=30000)

                    # Wait for content to load
                    page.wait_for_selector('[data-e2e="user-post-item"]', timeout=10000)

                    # Extract creator usernames from posts
                    usernames = page.eval_on_selector_all(
                        '[data-e2e="user-post-item-username"]',
                        'elements => elements.map(e => e.textContent)'
                    )

                    for username in usernames[:limit]:
                        if len(creators) >= limit:
                            break

                        creators.append({
                            'username': username.replace('@', ''),
                            'display_name': username.replace('@', ''),
                            'url': f"https://tiktok.com/@{username.replace('@', '')}",
                            'followers': None  # Will get from profile
                        })

                    # Random delay to avoid detection
                    time.sleep(random.randint(3, 7))

                except Exception as e:
                    self.logger.error(f"Error scraping hashtag {hashtag}: {e}")
                    continue

            browser.close()

        return creators[:limit]

    def get_creator_profile(self, username: str) -> Optional[Dict]:
        """Get TikTok profile with failover"""
        # Try Apify first
        if self.use_apify_primary and self.apify_token:
            try:
                return self._get_profile_apify(username)
            except Exception as e:
                self.logger.warning(f"Apify profile fetch failed for {username}: {e}. Falling back to Playwright.")

        # Fallback to Playwright
        return self._get_profile_playwright(username)

    def _get_profile_playwright(self, username: str) -> Optional[Dict]:
        """Scrape TikTok profile with Playwright"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                viewport={'width': 1920, 'height': 1080}
            )
            page = context.new_page()

            try:
                page.goto(f'https://www.tiktok.com/@{username}', timeout=30000)
                page.wait_for_selector('[data-e2e="user-page"]', timeout=10000)

                # Extract profile data
                followers = page.locator('[data-e2e="followers-count"]').text_content()
                following = page.locator('[data-e2e="following-count"]').text_content()
                likes = page.locator('[data-e2e="likes-count"]').text_content()

                # Parse counts (handle K, M suffixes)
                def parse_count(text):
                    text = text.strip().lower()
                    if 'k' in text:
                        return int(float(text.replace('k', '')) * 1000)
                    elif 'm' in text:
                        return int(float(text.replace('m', '')) * 1000000)
                    else:
                        return int(text)

                profile = {
                    'platform': 'tiktok',
                    'username': username,
                    'display_name': page.locator('[data-e2e="user-title"]').text_content(),
                    'url': f"https://tiktok.com/@{username}",
                    'followers': parse_count(followers),
                    'following': parse_count(following),
                    'total_posts': 0,  # Not easily accessible
                    'bio': page.locator('[data-e2e="user-bio"]').text_content() if page.locator('[data-e2e="user-bio"]').count() > 0 else '',
                    'country': 'Unknown',
                    'language': 'en',
                    'is_verified': page.locator('[data-e2e="user-verified"]').count() > 0,
                    'is_business_account': False,
                    'last_scraped': datetime.utcnow().isoformat()
                }

                browser.close()

                # Rate limiting
                time.sleep(random.randint(3, 7))

                return profile

            except Exception as e:
                self.logger.error(f"Error scraping profile for {username}: {e}")
                browser.close()
                return None
```

---

### Analyzer Architecture (`analyzers/`)

#### Content Classifier (`content_classifier.py`)

**LLM-Powered Relevance Detection:**

```python
from anthropic import Anthropic

class ContentClassifier:
    def __init__(self, anthropic_api_key: str):
        self.client = Anthropic(api_key=anthropic_api_key)
        self.model = "claude-sonnet-4-20250514"

    def classify_relevance(self, content: Dict) -> Dict:
        """
        Classify if creator content is relevant to lighting industry.

        Args:
            content: {
                'platform': str,
                'username': str,
                'title': str,
                'description': str,
                'hashtags': List[str]
            }

        Returns:
            {
                'is_relevant': bool,
                'confidence': float (0.0-1.0),
                'primary_theme': str,
                'reasoning': str
            }
        """
        prompt = f"""Analyze if this creator content is relevant to residential/commercial LED lighting:

Platform: {content['platform']}
Creator: {content['username']}
Title: {content.get('title', 'N/A')}
Description: {content.get('description', 'N/A')}
Hashtags: {', '.join(content.get('hashtags', []))}

Consider these categories as RELEVANT:
1. Installation, retrofit, or upgrade projects (LED strips, bulbs, fixtures)
2. Product reviews, comparisons, or recommendations (specific brands/models)
3. Troubleshooting, repair, or maintenance content (flickering, dimming issues)
4. Design inspiration, aesthetics, or ambiance (mood lighting, color temperature)
5. DIY tutorials or professional walkthroughs (wiring, smart home integration)

Consider these categories as IRRELEVANT:
- General home improvement (no lighting focus)
- Outdoor/automotive lighting (unless residential)
- Stage/photography lighting (professional production)
- Completely unrelated content

Respond in JSON format:
{{
  "is_relevant": true or false,
  "confidence": 0.0 to 1.0,
  "primary_theme": "installation" or "review" or "troubleshooting" or "design" or "other" or "irrelevant",
  "reasoning": "brief explanation (1-2 sentences)"
}}"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse JSON response
        import json
        try:
            result = json.loads(response.content[0].text)
            return result
        except json.JSONDecodeError:
            self.logger.error(f"Failed to parse LLM response: {response.content[0].text}")
            return {
                'is_relevant': False,
                'confidence': 0.0,
                'primary_theme': 'error',
                'reasoning': 'Failed to parse LLM response'
            }
```

---

#### Pain Point Detector (`pain_point_detector.py`)

**Extract Pain Points from Content:**

```python
class PainPointDetector:
    def __init__(self, anthropic_api_key: str):
        self.client = Anthropic(api_key=anthropic_api_key)
        self.model = "claude-sonnet-4-20250514"

    def extract_pain_points(self, content_texts: List[str]) -> List[Dict]:
        """
        Extract lighting-related pain points from aggregated content.

        Args:
            content_texts: List of descriptions, titles, comments

        Returns:
            [
                {
                    "text": "verbatim quote",
                    "category": "technical|aesthetic|cost|safety|usability",
                    "severity": "low|medium|high"
                }
            ]
        """
        aggregated_text = "\n\n".join(content_texts[:10])  # Limit to 10 pieces to fit context

        prompt = f"""Extract specific lighting-related pain points from this creator content:

Content:
{aggregated_text}

Identify concrete problems, frustrations, or challenges:
- **Technical**: Flickering, compatibility issues, installation difficulty, wiring problems
- **Aesthetic**: Wrong color temperature, too dim/bright, glare, harsh shadows
- **Cost**: Expensive to replace, high energy bills, short lifespan
- **Safety**: Overheating, fire risk, electrical hazards
- **Usability**: Difficult controls, unreliable smart features, complex setup

For each pain point:
1. Extract verbatim quote (or paraphrase if implicit)
2. Categorize (technical, aesthetic, cost, safety, usability)
3. Rate severity (low, medium, high)

Respond in JSON format:
{{
  "pain_points": [
    {{
      "text": "LED strips are too dim for task lighting",
      "category": "aesthetic",
      "severity": "medium"
    }}
  ]
}}

Only include pain points explicitly or strongly implied in the content."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        import json
        try:
            result = json.loads(response.content[0].text)
            return result.get('pain_points', [])
        except json.JSONDecodeError:
            self.logger.error(f"Failed to parse pain points: {response.content[0].text}")
            return []
```

---

#### Consumer Language Extractor (`language_extractor.py`)

**Extract Marketing-Relevant Terminology:**

```python
class LanguageExtractor:
    def __init__(self, anthropic_api_key: str):
        self.client = Anthropic(api_key=anthropic_api_key)
        self.model = "claude-sonnet-4-20250514"

    def extract_consumer_language(self, content_texts: List[str]) -> List[Dict]:
        """
        Extract consumer language terms for marketing.

        Returns:
            [
                {
                    "term": "warm white",
                    "category": "feature|product|job|pain",
                    "frequency": int,
                    "example": "verbatim quote"
                }
            ]
        """
        aggregated_text = "\n\n".join(content_texts[:15])

        prompt = f"""Extract consumer language terms from this content for marketing insights:

Content:
{aggregated_text}

Identify:
1. **Product Terms**: Brand names, product types (LED strip, smart bulb, dimmer switch)
2. **Feature Descriptions**: Warm white, color-changing, dimmable, motion-activated
3. **Jobs-to-be-Done**: "brighten up my kitchen", "create cozy ambiance", "save on energy bills"
4. **Pain Point Language**: "too dim", "harsh light", "difficult to install", "unreliable"

For each term:
- Extract the exact phrase consumers use (not technical jargon)
- Categorize (product, feature, job, pain)
- Provide example quote for context

Respond in JSON:
{{
  "terms": [
    {{
      "term": "warm white",
      "category": "feature",
      "example": "looking for warm white bulbs for my living room"
    }}
  ]
}}"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )

        import json
        try:
            result = json.loads(response.content[0].text)
            return result.get('terms', [])
        except json.JSONDecodeError:
            return []
```

---

#### Creator Scorer (`creator_scorer.py`)

**Calculate Viability Scores:**

```python
class CreatorScorer:
    def calculate_research_score(self, creator: Dict) -> int:
        """
        Research Viability Score (0-100)

        Components:
        - Engagement rate percentile: 30%
        - Authenticity: 20%
        - Content quality: 25%
        - Relevance: 15%
        - Geographic match: 10%
        """
        # 1. Engagement Rate Percentile (0-100)
        engagement_rate = creator.get('avg_engagement_rate', 0)
        platform = creator['platform']

        # Platform benchmarks
        benchmarks = {
            'youtube': 0.04,  # 4% is excellent
            'instagram': 0.02,  # 2% is excellent
            'tiktok': 0.08,  # 8% is excellent
            'etsy': 0.05  # 5% is excellent (reviews/sales ratio)
        }

        benchmark = benchmarks.get(platform, 0.03)
        engagement_percentile = min(100, (engagement_rate / benchmark) * 100)

        # 2. Authenticity Score (0-100)
        authenticity = 0
        if creator.get('is_verified'):
            authenticity += 30
        if creator.get('total_posts', 0) >= 50:  # Consistent history
            authenticity += 20
        if creator.get('bio') and len(creator.get('bio', '')) > 20:
            authenticity += 20
        if creator.get('followers', 0) / max(creator.get('following', 1), 1) > 2:  # More followers than following
            authenticity += 30

        # 3. Content Quality Score (0-100)
        # Estimated from engagement + follower count
        quality = min(100, (engagement_percentile + (creator.get('followers', 0) / 1000)))

        # 4. Relevance Score (0-100)
        relevance = creator.get('relevance_confidence', 0.5) * 100

        # 5. Geographic Match (0-100)
        target_countries = ['US', 'CA', 'UK', 'AU', 'NZ']
        country = creator.get('country', 'Unknown')

        if country in target_countries:
            geo_score = 100
        elif country in ['DE', 'FR', 'IT', 'ES', 'NL']:  # Europe
            geo_score = 75
        elif creator.get('language') == 'en':
            geo_score = 50
        else:
            geo_score = 25

        # Weighted sum
        research_score = (
            engagement_percentile * 0.30 +
            authenticity * 0.20 +
            quality * 0.25 +
            relevance * 0.15 +
            geo_score * 0.10
        )

        return int(research_score)

    def calculate_partnership_score(self, creator: Dict, brand_alignment: float = None) -> int:
        """
        Partnership Viability Score (0-100)

        Components:
        - Brand alignment: 30% (requires LLM assessment)
        - Audience size percentile: 25%
        - Professionalism: 20%
        - Consistency: 15%
        - Prior partnerships: 10%
        """
        # 1. Brand Alignment (0-100) - passed from LLM assessment
        if brand_alignment is None:
            brand_alignment = 50  # Default neutral

        # 2. Audience Size Percentile (0-100)
        followers = creator.get('followers', 0)
        platform = creator['platform']

        # Thresholds for "good" audience size
        thresholds = {
            'youtube': 100000,  # 100K subs
            'instagram': 50000,  # 50K followers
            'tiktok': 100000,  # 100K followers
            'etsy': 5000  # 5K sales
        }

        threshold = thresholds.get(platform, 50000)
        audience_percentile = min(100, (followers / threshold) * 100)

        # 3. Professionalism Score (0-100)
        professionalism = 0
        if creator.get('is_business_account'):
            professionalism += 30
        if creator.get('bio') and any(word in creator.get('bio', '').lower() for word in ['contact', 'email', 'dm', 'collab']):
            professionalism += 20
        if creator.get('is_verified'):
            professionalism += 30
        if followers >= threshold * 0.5:  # At least 50% of threshold
            professionalism += 20

        # 4. Consistency Score (0-100)
        # Estimated from total posts
        posts = creator.get('total_posts', 0)
        if posts >= 365:  # Daily posting for a year
            consistency = 100
        elif posts >= 52:  # Weekly for a year
            consistency = 75
        elif posts >= 12:  # Monthly for a year
            consistency = 50
        else:
            consistency = 25

        # 5. Prior Partnerships (0-100)
        # Detected from bio or content (keywords like #ad, #sponsored, "partner")
        partnership_indicators = ['#ad', '#sponsored', 'partner', 'collaboration', 'ambassador']
        has_partnerships = any(indicator in creator.get('bio', '').lower() for indicator in partnership_indicators)

        prior_partnerships = 100 if has_partnerships else 50  # 50 = neutral (not bad if no prior partnerships)

        # Weighted sum
        partnership_score = (
            brand_alignment * 0.30 +
            audience_percentile * 0.25 +
            professionalism * 0.20 +
            consistency * 0.15 +
            prior_partnerships * 0.10
        )

        return int(partnership_score)
```

---

## 🔄 Failover Logic (`scrapers/failover_pool.py`)

**Automatic Method Switching:**

```python
class ScraperFailoverPool:
    """
    Manages multiple scraping methods for a platform with automatic failover.

    Example usage:
        pool = ScraperFailoverPool(platform='instagram')
        pool.add_method('apify', apify_scraper.search_creators, priority=1)
        pool.add_method('instaloader', instaloader_scraper.search_creators, priority=2)

        results = pool.execute('search_creators', keywords=['LED lighting'], limit=100)
    """

    def __init__(self, platform: str):
        self.platform = platform
        self.methods = []  # List of (name, callable, priority) tuples
        self.logger = logging.getLogger(f"FailoverPool-{platform}")

    def add_method(self, name: str, method_callable: Callable, priority: int = 1):
        """Add scraping method with priority (1=highest, 3=lowest)"""
        self.methods.append((name, method_callable, priority))
        self.methods.sort(key=lambda x: x[2])  # Sort by priority

    def execute(self, operation: str, *args, **kwargs) -> Optional[Any]:
        """
        Execute operation with automatic failover.

        Args:
            operation: Method name (e.g., 'search_creators', 'get_creator_profile')
            *args, **kwargs: Arguments to pass to method

        Returns:
            Result from first successful method, or None if all fail
        """
        for method_name, method_callable, priority in self.methods:
            try:
                self.logger.info(f"[{self.platform}] Trying {method_name} (priority {priority})...")

                result = method_callable(*args, **kwargs)

                if result:
                    self.logger.info(f"✅ [{self.platform}] {method_name} succeeded")
                    return result
                else:
                    self.logger.warning(f"⚠️ [{self.platform}] {method_name} returned empty result")

            except Exception as e:
                self.logger.error(f"❌ [{self.platform}] {method_name} failed: {e}")
                continue

        # All methods failed
        self.logger.error(f"🚨 [{self.platform}] All scraping methods failed for {operation}")
        return None
```

**Usage in Orchestrator:**

```python
# In orchestrator.py
def _setup_failover_pools(self):
    """Initialize failover pools for each platform"""

    # Instagram
    instagram_pool = ScraperFailoverPool('instagram')
    instagram_pool.add_method('apify', self.instagram_scraper._search_creators_apify, priority=1)
    instagram_pool.add_method('instaloader', self.instagram_scraper._search_creators_instaloader, priority=2)

    # TikTok
    tiktok_pool = ScraperFailoverPool('tiktok')
    tiktok_pool.add_method('apify', self.tiktok_scraper._search_creators_apify, priority=1)
    tiktok_pool.add_method('playwright', self.tiktok_scraper._search_creators_playwright, priority=2)

    self.failover_pools = {
        'instagram': instagram_pool,
        'tiktok': tiktok_pool
    }

def _scrape_platform(self, platform: str, keywords: List[str]) -> List[Dict]:
    """Scrape creators with automatic failover"""
    if platform in self.failover_pools:
        return self.failover_pools[platform].execute('search_creators', keywords=keywords, limit=100)
    else:
        # Official APIs don't need failover
        scraper = self.scrapers[platform]
        return scraper.search_creators(keywords, limit=100)
```

---

## 📊 Reporting Architecture (`reporters/`)

### HTML Reporter (`html_reporter.py`)

**Template-Based Report Generation:**

```python
from jinja2 import Template

class HTMLReporter:
    def generate_report(self, db: Database, project_name: str) -> str:
        """
        Generate HTML report from database.

        Returns:
            Path to generated HTML file
        """
        # Load data
        top_research_creators = db.get_top_creators(score_type='research', limit=50)
        top_partnership_creators = db.get_top_creators(score_type='partnership', limit=50)
        consumer_language = db.get_consumer_language(min_mentions=3)
        trending_themes = db.get_trending_themes(min_creator_count=5)

        # Group consumer language by category
        language_by_category = {}
        for term in consumer_language:
            category = term['category']
            if category not in language_by_category:
                language_by_category[category] = []
            language_by_category[category].append(term)

        # Render template
        template = self._load_template()
        html = template.render(
            project_name=project_name,
            generated_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'),
            total_creators=len(db.get_all_creators()),
            top_research_creators=top_research_creators,
            top_partnership_creators=top_partnership_creators,
            consumer_language=language_by_category,
            trending_themes=trending_themes
        )

        # Save to file
        output_path = f"data/reports/{project_name}_creator_intelligence_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.html"
        with open(output_path, 'w') as f:
            f.write(html)

        return output_path

    def _load_template(self) -> Template:
        """Load Jinja2 HTML template"""
        template_str = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>{{ project_name }} - Creator Intelligence Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                h1 { color: #2c3e50; }
                table { border-collapse: collapse; width: 100%; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
                th { background-color: #3498db; color: white; }
                .score { font-weight: bold; }
                .score-high { color: #27ae60; }
                .score-medium { color: #f39c12; }
                .score-low { color: #e74c3c; }
            </style>
        </head>
        <body>
            <h1>{{ project_name }} - Creator Intelligence Report</h1>
            <p><strong>Generated:</strong> {{ generated_at }}</p>
            <p><strong>Total Creators Analyzed:</strong> {{ total_creators }}</p>

            <h2>Top Creators for Research</h2>
            <table>
                <thead>
                    <tr>
                        <th>Creator</th>
                        <th>Platform</th>
                        <th>Followers</th>
                        <th>Research Score</th>
                        <th>Country</th>
                        <th>Link</th>
                    </tr>
                </thead>
                <tbody>
                    {% for creator in top_research_creators %}
                    <tr>
                        <td>{{ creator.display_name }}</td>
                        <td>{{ creator.platform }}</td>
                        <td>{{ "{:,}".format(creator.followers) }}</td>
                        <td class="score score-high">{{ creator.research_viability_score }}/100</td>
                        <td>{{ creator.country }}</td>
                        <td><a href="{{ creator.url }}" target="_blank">View</a></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>

            <h2>Consumer Language Dictionary</h2>
            {% for category, terms in consumer_language.items() %}
            <h3>{{ category.replace('_', ' ').title() }}</h3>
            <ul>
                {% for term in terms[:20] %}
                <li><strong>{{ term.term }}</strong> ({{ term.total_mentions }} mentions) - {{ term.example_quotes[0].text if term.example_quotes else '' }}</li>
                {% endfor %}
            </ul>
            {% endfor %}

            <h2>Trending Themes</h2>
            <ul>
                {% for theme in trending_themes %}
                <li><strong>{{ theme.theme }}</strong> - {{ theme.creator_count }} creators</li>
                {% endfor %}
            </ul>
        </body>
        </html>
        """
        return Template(template_str)
```

---

## 🚀 Deployment & Performance

### Performance Targets

| Operation | Target Time | Notes |
|-----------|------------|-------|
| YouTube search (50 creators) | 5-10s | API call + parsing |
| Etsy search (50 shops) | 5-10s | API call + pagination |
| Instagram Apify (100 profiles) | 2-3 min | Managed scraper |
| TikTok Apify (100 profiles) | 2-3 min | Managed scraper |
| LLM content classification (100 pieces) | 3-5 min | Batch processing |
| Pain point extraction (100 pieces) | 5-7 min | Longer prompts |
| Scoring (500 creators) | 10-20s | Pure computation |
| HTML report generation | 5-10s | Template rendering |
| Excel export (500 creators) | 15-30s | openpyxl writing |

**Total Pipeline Time (500 creators):** ~30-45 minutes

---

### Scaling Considerations

**Database:**
- SQLite handles 1,000-10,000 creators efficiently
- Add indexes on `platform`, `research_viability_score`, `partnership_viability_score`, `country`
- Migrate to PostgreSQL if >10,000 creators or UI development begins

**API Quotas:**
- YouTube: Request quota increase (up to 1M units/day with compliance audit)
- Etsy: 10,000 req/day sufficient for 500-1,000 shops
- Apify: Free tier supports ~500 profiles/month combined (Instagram + TikTok)

**Rate Limiting:**
- Instagram Instaloader: Max 20 profiles/hour (2-3 min delays)
- TikTok Playwright: Max 50 profiles/session (recycle browser every 20 requests)
- LLM API: Batch requests where possible (combine multiple content pieces)

---

## 🔒 Security & Compliance

### API Key Management

**Storage:**
- All API keys in `.env` file (gitignored)
- Use `python-dotenv` with `override=True` for .env priority
- Never hardcode credentials in source code

**Access Control:**
- API keys should have minimum required permissions
- YouTube: Read-only access
- Etsy: Read-only OAuth scope
- Apify: Actor execution only (no account management)

---

### Data Privacy

**GDPR/CCPA Compliance:**
- Only scrape publicly available data
- Do not store personally identifiable information beyond what's public
- Implement data retention policy (90-180 days)
- Honor deletion requests (remove creator from database)

**Grey-Area Scraping Disclaimer:**
- Scraping Instagram/TikTok may violate Terms of Service
- For research and competitive intelligence only
- Do not redistribute scraped data
- Obtain legal review before commercial deployment

---

## 📚 Dependencies

### Python Packages

```txt
# Core
python-dotenv>=1.0.0
pyyaml>=6.0

# Scrapers
google-api-python-client>=2.0.0  # YouTube Data API
apify-client>=1.0.0  # Apify managed scrapers
instaloader>=4.10.0  # Instagram fallback
playwright>=1.40.0  # TikTok fallback

# LLM
anthropic>=0.20.0  # Claude API

# Database
sqlite3  # Built-in

# Reporting
jinja2>=3.1.2  # HTML templates
openpyxl>=3.1.0  # Excel generation

# Testing
pytest>=7.4.0
pytest-mock>=3.12.0
```

---

## 🧪 Testing Strategy

### Unit Tests

**Test Coverage:**
- Scrapers: Mock API responses, verify parsing
- Analyzers: Test LLM prompt formatting, JSON parsing
- Scoring: Test algorithms with known inputs
- Database: Test CRUD operations, query correctness

**Example Test:**
```python
def test_youtube_scraper_search():
    """Test YouTube creator search"""
    mock_config = {'youtube_api_key': 'test_key'}
    scraper = YouTubeScraper(mock_config)

    # Mock API response
    with patch.object(scraper.youtube, 'search') as mock_search:
        mock_search.return_value.list.return_value.execute.return_value = {
            'items': [
                {
                    'snippet': {
                        'channelId': 'UC123',
                        'title': 'Test Channel'
                    }
                }
            ]
        }

        results = scraper.search_creators(['LED lighting'], limit=10)

        assert len(results) == 1
        assert results[0]['username'] == 'UC123'
        assert results[0]['display_name'] == 'Test Channel'
```

---

### Integration Tests

**End-to-End Flows:**
```python
def test_full_pipeline():
    """Test complete analysis pipeline"""
    orchestrator = CreatorIntelligenceOrchestrator(tier=1)

    results = orchestrator.run_analysis(
        platforms=['youtube'],
        keywords=['LED lighting tutorial'],
        target_creator_count=5
    )

    assert results['creators_discovered'] >= 5
    assert os.path.exists(results['reports']['html'])
    assert os.path.exists(results['database_path'])
```

---

## 📝 Logging Strategy

**Log Levels:**
- **DEBUG**: Raw API responses, cache hits/misses
- **INFO**: Pipeline progress, method success/failure
- **WARNING**: Failover triggers, API quota warnings
- **ERROR**: Scraping failures, LLM errors
- **CRITICAL**: Pipeline failures, database corruption

**Log Format:**
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/logs/creator_intelligence.log'),
        logging.StreamHandler()
    ]
)
```

---

**END OF TECHNICAL ARCHITECTURE**

**Next Steps:**
1. Review architecture for completeness
2. Create API Integration Preflight Checklist
3. Create Risk Assessment & Mitigation Plan
4. Create Database Schema Documentation
5. Obtain stakeholder approval
6. Begin implementation
