# API Integration Preflight Checklist

**Module:** Creator Intelligence
**Version:** 1.0.0
**Last Updated:** 2025-10-10
**Purpose:** Pre-implementation verification of all platform integrations

---

## ✅ **Preflight Overview**

This checklist ensures all platform APIs and scraping methods are properly configured before full module implementation.

### Checklist Summary

- [ ] **YouTube Data API v3** - Official API setup
- [ ] **Etsy API v3** - OAuth authentication configured
- [ ] **Apify Account** - Credits allocated for Instagram/TikTok
- [ ] **Instaloader** - Fallback scraper installed and tested
- [ ] **Playwright** - Headless browser configured
- [ ] **Claude Sonnet 4 API** - LLM analysis ready
- [ ] **SQLite Database** - Schema created
- [ ] **Cache Directory** - File structure prepared
- [ ] **Error Logging** - Monitoring configured

---

## 1️⃣ YouTube Data API v3

### Prerequisites

- [ ] Google Cloud Console account created
- [ ] New project created (e.g., "3M-Creator-Intelligence")
- [ ] YouTube Data API v3 enabled for project

### Setup Steps

```bash
# 1. Create API Key
# Navigate to: https://console.cloud.google.com/apis/credentials
# Click "Create Credentials" → "API Key"
# Copy API key

# 2. Add to .env file
echo "YOUTUBE_API_KEY=YOUR_API_KEY_HERE" >> modules/creator-intelligence/config/.env

# 3. Test API access
python3 << EOF
from googleapiclient.discovery import build

api_key = "YOUR_API_KEY"
youtube = build('youtube', 'v3', developerKey=api_key)

# Test search
response = youtube.search().list(
    q='LED lighting',
    type='channel',
    part='snippet',
    maxResults=5
).execute()

print(f"✅ YouTube API working! Found {len(response['items'])} channels")
EOF
```

### Verification Checklist

- [ ] API key generated and added to `.env`
- [ ] YouTube Data API v3 enabled in Google Cloud Console
- [ ] Test search returns results (run script above)
- [ ] Quota confirmed: 10,000 units/day (default)
- [ ] Quota monitoring dashboard bookmarked

### Quota Management

**Default Quota:** 10,000 units/day
**Search Cost:** 100 units per search (= 100 searches/day)
**Channel Details:** 1 unit per channel
**Video Details:** 1 unit per video

**Estimated Usage (500 creators):**
- Discovery searches: 10 searches × 100 units = 1,000 units
- Channel profiles: 500 × 1 unit = 500 units
- Video content: 500 × 20 videos × 1 unit = 10,000 units
- **Total:** ~11,500 units (requires 2 days or quota increase)

**Quota Increase:**
- Navigate to: [YouTube API Quota Request](https://support.google.com/youtube/contact/yt_api_form)
- Request 100,000 or 1,000,000 units/day
- Requires compliance audit (Terms of Service agreement, data usage description)

### Expected Test Output

```
✅ YouTube API working! Found 5 channels
```

---

## 2️⃣ Etsy API v3

### Prerequisites

- [ ] Etsy developer account created: https://www.etsy.com/developers/register
- [ ] App created in Etsy Developer Portal
- [ ] OAuth 2.0 credentials generated

### Setup Steps

```bash
# 1. Create Etsy App
# Navigate to: https://www.etsy.com/developers/your-apps
# Click "Create a New App"
# Fill in:
#   - App Name: "3M Creator Intelligence"
#   - App Purpose: "Market research and creator discovery"
#   - Callback URL: http://localhost:8000/etsy/callback (for local testing)

# 2. Get API Credentials
# Copy: Client ID (Keystring) and Client Secret

# 3. Add to .env
cat >> modules/creator-intelligence/config/.env << EOF
ETSY_API_KEY=your_keystring_here
ETSY_SHARED_SECRET=your_shared_secret_here
ETSY_OAUTH_TOKEN=  # Will be generated after OAuth flow
ETSY_OAUTH_TOKEN_SECRET=
EOF

# 4. Run OAuth Flow (interactive)
python3 << EOF
import requests
from urllib.parse import urlencode

# Step 1: Get request token
params = {
    'api_key': 'YOUR_ETSY_API_KEY',
    'scope': 'listings_r shops_r',
    'callback': 'http://localhost:8000/etsy/callback'
}

response = requests.get(
    'https://openapi.etsy.com/v2/oauth/request_token',
    params=params
)

# Follow OAuth flow instructions
print("Visit this URL to authorize:")
print(f"https://www.etsy.com/oauth/signin?{urlencode({'oauth_token': response.text.split('&')[0].split('=')[1]})}")
EOF
```

### Verification Checklist

- [ ] Etsy developer account created
- [ ] App registered with OAuth credentials
- [ ] API key and shared secret added to `.env`
- [ ] OAuth flow completed and tokens stored
- [ ] Test search returns shop results

### Test Script

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv('modules/creator-intelligence/config/.env')

# Test shop search
headers = {
    'x-api-key': os.getenv('ETSY_API_KEY'),
    'Authorization': f'Bearer {os.getenv("ETSY_OAUTH_TOKEN")}'
}

response = requests.get(
    'https://openapi.etsy.com/v3/application/shops',
    params={'shop_name': 'lighting'},
    headers=headers
)

if response.status_code == 200:
    shops = response.json()
    print(f"✅ Etsy API working! Found {len(shops.get('results', []))} shops")
else:
    print(f"❌ Error: {response.status_code} - {response.text}")
```

### Expected Output

```
✅ Etsy API working! Found 10 shops
```

---

## 3️⃣ Apify Account Setup

### Prerequisites

- [ ] Apify account created: https://console.apify.com/sign-up
- [ ] Free tier activated (5,000 credits/month)

### Setup Steps

```bash
# 1. Create Account
# Visit: https://console.apify.com/sign-up
# Sign up with email (no credit card required for free tier)

# 2. Get API Token
# Navigate to: https://console.apify.com/account#/integrations
# Copy "Personal API Token"

# 3. Add to .env
echo "APIFY_TOKEN=apify_api_YOUR_TOKEN_HERE" >> modules/creator-intelligence/config/.env

# 4. Install Apify Python Client
pip install apify-client

# 5. Test Instagram Scraper
python3 << EOF
from apify_client import ApifyClient
import os
from dotenv import load_dotenv

load_dotenv('modules/creator-intelligence/config/.env')

client = ApifyClient(os.getenv('APIFY_TOKEN'))

# Test Instagram scraper (small test)
run_input = {
    "username": ["instagram"],  # Official Instagram account
    "resultsType": "posts",
    "resultsLimit": 1
}

print("🔄 Testing Apify Instagram Scraper...")
run = client.actor("apify/instagram-scraper").call(run_input=run_input)

# Get results
items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
print(f"✅ Apify Instagram Scraper working! Scraped {len(items)} post(s)")
print(f"Credits used: ~10-15 (estimated)")
EOF
```

### Verification Checklist

- [ ] Apify account created (free tier)
- [ ] API token generated and added to `.env`
- [ ] `apify-client` Python package installed
- [ ] Instagram Scraper test successful
- [ ] TikTok Scraper test successful
- [ ] Credit usage monitoring dashboard bookmarked

### Credit Management

**Free Tier:** 5,000 credits/month

**Cost Breakdown:**
- Instagram profile scrape: ~10 credits
- TikTok profile scrape: ~15 credits
- Instagram post scrape: ~1-2 credits per 10 posts
- TikTok video scrape: ~1-2 credits per 10 videos

**Estimated Usage (500 creators, 50% Instagram, 50% TikTok):**
- 250 Instagram profiles × 10 credits = 2,500 credits
- 250 TikTok profiles × 15 credits = 3,750 credits
- **Total:** ~6,250 credits (requires paid tier or 2-month split)

**Paid Tier:**
- $49/month = 50,000 credits
- $199/month = 250,000 credits

### Test Output Expected

```
🔄 Testing Apify Instagram Scraper...
✅ Apify Instagram Scraper working! Scraped 1 post(s)
Credits used: ~10-15 (estimated)
```

---

## 4️⃣ Instaloader (Instagram Fallback)

### Prerequisites

- [ ] Python 3.9+ installed
- [ ] pip package manager available

### Setup Steps

```bash
# 1. Install Instaloader
pip install instaloader

# 2. Test Basic Scraping (No Login)
python3 << EOF
import instaloader
import time

L = instaloader.Instaloader(
    download_videos=False,
    download_pictures=False,
    save_metadata=False
)

try:
    # Test scraping public Instagram profile
    profile = instaloader.Profile.from_username(L.context, 'instagram')

    print(f"✅ Instaloader working!")
    print(f"Username: {profile.username}")
    print(f"Followers: {profile.followers:,}")
    print(f"Posts: {profile.mediacount}")

    # Wait 2-3 minutes to simulate rate limiting
    print("⏳ Waiting 120 seconds (rate limit simulation)...")
    time.sleep(120)
    print("✅ Rate limiting test complete")

except Exception as e:
    print(f"❌ Error: {e}")
EOF
```

### Verification Checklist

- [ ] Instaloader installed via pip
- [ ] Test scrape of public profile successful
- [ ] Rate limiting (120s delay) implemented
- [ ] No account ban warnings received

### ⚠️ **CRITICAL WARNINGS**

**Instagram actively blocks Instaloader users. Risk mitigation required:**

1. **Rate Limiting:** 2-3 minutes between requests (mandatory)
2. **No Login:** Use public profile scraping only (avoid account bans)
3. **Proxy Rotation:** Consider using rotating proxies if available
4. **Fallback Only:** Use ONLY when Apify fails (not primary method)
5. **Monitor Bans:** If 429 errors occur, stop immediately for 24 hours

### Expected Output

```
✅ Instaloader working!
Username: instagram
Followers: 627,000,000
Posts: 7,528
⏳ Waiting 120 seconds (rate limit simulation)...
✅ Rate limiting test complete
```

---

## 5️⃣ Playwright (TikTok Fallback)

### Prerequisites

- [ ] Python 3.9+ installed
- [ ] Node.js 14+ installed (for Playwright browsers)

### Setup Steps

```bash
# 1. Install Playwright
pip install playwright

# 2. Install Chromium Browser
playwright install chromium

# 3. Test Headless Scraping
python3 << EOF
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    print("🔄 Launching headless browser...")

    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        viewport={'width': 1920, 'height': 1080}
    )
    page = context.new_page()

    try:
        print("🔄 Navigating to TikTok...")
        page.goto('https://www.tiktok.com', timeout=30000)

        # Wait for page load
        time.sleep(5)

        # Check if page loaded
        title = page.title()
        print(f"✅ Playwright working! Page title: {title}")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        browser.close()
        print("✅ Browser closed successfully")
EOF
```

### Verification Checklist

- [ ] Playwright installed via pip
- [ ] Chromium browser downloaded (~300MB)
- [ ] Headless browser launches successfully
- [ ] TikTok homepage loads without CAPTCHA
- [ ] Stealth mode configured (user-agent, viewport)

### Anti-Detection Configuration

**Required Stealth Techniques:**
1. Custom user-agent (real browser string)
2. Viewport size (1920×1080 desktop)
3. Request throttling (3-7 second delays)
4. Session recycling (new browser every 20 requests)
5. Proxy rotation (recommended but optional)

### Expected Output

```
🔄 Launching headless browser...
🔄 Navigating to TikTok...
✅ Playwright working! Page title: TikTok - Make Your Day
✅ Browser closed successfully
```

---

## 6️⃣ Claude Sonnet 4 API (LLM Analysis)

### Prerequisites

- [ ] Anthropic account created: https://console.anthropic.com
- [ ] API key generated

### Setup Steps

```bash
# 1. Create Anthropic Account
# Visit: https://console.anthropic.com/sign-up
# Complete email verification

# 2. Generate API Key
# Navigate to: https://console.anthropic.com/settings/keys
# Click "Create Key"
# Copy API key (starts with sk-ant-api03-)

# 3. Add to .env
echo "ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE" >> modules/creator-intelligence/config/.env

# 4. Install Anthropic Python SDK
pip install anthropic

# 5. Test Classification
python3 << EOF
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv('modules/creator-intelligence/config/.env')

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

prompt = """Analyze if this content is relevant to LED lighting:
Title: How to Install LED Strip Lights in Your Kitchen
Description: Step-by-step tutorial for installing under-cabinet LED strips

Respond in JSON:
{"is_relevant": true/false, "confidence": 0.0-1.0, "primary_theme": "installation"}
"""

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=200,
    messages=[{"role": "user", "content": prompt}]
)

print("✅ Claude API working!")
print(f"Response: {response.content[0].text}")
EOF
```

### Verification Checklist

- [ ] Anthropic account created
- [ ] API key generated and added to `.env`
- [ ] `anthropic` Python package installed
- [ ] Test classification returns valid JSON
- [ ] Model `claude-sonnet-4-20250514` accessible

### Cost Estimation

**Claude Sonnet 4 Pricing (as of 2025-10-10):**
- Input: $3 per million tokens
- Output: $15 per million tokens

**Estimated Usage (500 creators):**
- Content classification: 500 items × 500 tokens = 250K tokens input + 50K tokens output = $0.75 + $0.75 = $1.50
- Pain point extraction: 500 items × 1,000 tokens = 500K tokens input + 200K tokens output = $1.50 + $3.00 = $4.50
- Consumer language: 500 items × 1,000 tokens = 500K tokens input + 200K tokens output = $1.50 + $3.00 = $4.50
- **Total:** ~$12.50 per 500-creator analysis

### Expected Output

```
✅ Claude API working!
Response: {"is_relevant": true, "confidence": 0.95, "primary_theme": "installation"}
```

---

## 7️⃣ SQLite Database Setup

### Prerequisites

- [ ] Python 3.9+ (sqlite3 built-in)

### Setup Steps

```bash
# 1. Create database directory
mkdir -p modules/creator-intelligence/data/database

# 2. Initialize database with schema
python3 << 'EOF'
import sqlite3
import os

db_path = 'modules/creator-intelligence/data/database/creators.db'
os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create creators table
cursor.execute('''
CREATE TABLE IF NOT EXISTS creators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform TEXT NOT NULL,
    username TEXT NOT NULL,
    display_name TEXT,
    url TEXT UNIQUE,
    followers INTEGER,
    following INTEGER,
    total_posts INTEGER,
    avg_engagement_rate REAL,
    content_frequency TEXT,
    country TEXT,
    region TEXT,
    language TEXT,
    timezone TEXT,
    primary_niche TEXT,
    content_themes JSON,
    pain_points_mentioned JSON,
    consumer_language JSON,
    research_viability_score INTEGER,
    partnership_viability_score INTEGER,
    brand_safety_score INTEGER,
    is_verified BOOLEAN DEFAULT 0,
    is_business_account BOOLEAN DEFAULT 0,
    last_scraped TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(platform, username)
)
''')

# Create indexes
cursor.execute('CREATE INDEX IF NOT EXISTS idx_platform ON creators(platform)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_research_score ON creators(research_viability_score DESC)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_country ON creators(country)')

print("✅ SQLite database created with schema")
print(f"Location: {db_path}")

conn.commit()
conn.close()
EOF

# 3. Verify database
sqlite3 modules/creator-intelligence/data/database/creators.db "SELECT name FROM sqlite_master WHERE type='table';"
```

### Verification Checklist

- [ ] Database file created at `data/database/creators.db`
- [ ] `creators` table exists with correct schema
- [ ] Indexes created on `platform`, `research_viability_score`, `country`
- [ ] Test insert/select successful

### Expected Output

```
✅ SQLite database created with schema
Location: modules/creator-intelligence/data/database/creators.db
creators
```

---

## 8️⃣ Cache Directory Structure

### Setup Steps

```bash
# Create cache directories
mkdir -p modules/creator-intelligence/data/cache/{youtube,etsy,instagram,tiktok}
mkdir -p modules/creator-intelligence/data/reports
mkdir -p modules/creator-intelligence/data/language
mkdir -p modules/creator-intelligence/data/logs

# Verify structure
tree modules/creator-intelligence/data/ -L 2
```

### Expected Structure

```
modules/creator-intelligence/data/
├── cache/
│   ├── youtube/
│   ├── etsy/
│   ├── instagram/
│   └── tiktok/
├── database/
│   └── creators.db
├── reports/
├── language/
└── logs/
```

### Verification Checklist

- [ ] All cache directories created
- [ ] Reports directory exists
- [ ] Language dictionary directory exists
- [ ] Logs directory exists

---

## 9️⃣ Error Logging Setup

### Setup Steps

```python
# Test logging configuration
python3 << 'EOF'
import logging
import os

log_dir = 'modules/creator-intelligence/data/logs'
os.makedirs(log_dir, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'{log_dir}/creator_intelligence.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('CreatorIntelligence')

# Test log levels
logger.debug('Debug message (not visible at INFO level)')
logger.info('✅ Info message - pipeline progress')
logger.warning('⚠️ Warning message - failover triggered')
logger.error('❌ Error message - scraping failure')

print(f"\n✅ Logging configured. Check: {log_dir}/creator_intelligence.log")
EOF

# View log file
cat modules/creator-intelligence/data/logs/creator_intelligence.log
```

### Expected Output

```
2025-10-10 15:30:00,123 - CreatorIntelligence - INFO - ✅ Info message - pipeline progress
2025-10-10 15:30:00,124 - CreatorIntelligence - WARNING - ⚠️ Warning message - failover triggered
2025-10-10 15:30:00,125 - CreatorIntelligence - ERROR - ❌ Error message - scraping failure

✅ Logging configured. Check: modules/creator-intelligence/data/logs/creator_intelligence.log
```

---

## 🚀 **Final Preflight Checklist**

Before starting implementation, confirm ALL items:

### Platform APIs
- [ ] ✅ YouTube Data API v3 tested and working
- [ ] ✅ Etsy API v3 OAuth flow completed
- [ ] ✅ Apify account with 5,000+ credits available
- [ ] ✅ Instaloader installed with rate limiting tested
- [ ] ✅ Playwright with Chromium browser working
- [ ] ✅ Claude Sonnet 4 API key valid and tested

### Infrastructure
- [ ] ✅ SQLite database created with schema
- [ ] ✅ Cache directories created (youtube, etsy, instagram, tiktok)
- [ ] ✅ Reports/language/logs directories created
- [ ] ✅ Error logging configured and writing to file

### Configuration
- [ ] ✅ `.env` file created with all API keys
- [ ] ✅ `.env.example` template documented
- [ ] ✅ `.gitignore` configured to protect credentials
- [ ] ✅ All Python dependencies installed (`requirements.txt`)

### Testing
- [ ] ✅ Each platform tested individually with success
- [ ] ✅ Failover logic conceptually validated
- [ ] ✅ Rate limiting delays tested (Instagram, TikTok)
- [ ] ✅ LLM classification returns valid JSON

---

## 📋 **Troubleshooting Common Issues**

### YouTube API 403 Forbidden
**Problem:** API key has insufficient permissions
**Solution:**
1. Verify YouTube Data API v3 is enabled in Google Cloud Console
2. Check API key restrictions (none should be set for testing)
3. Wait 5-10 minutes for API activation to propagate

### Etsy OAuth Flow Fails
**Problem:** Callback URL mismatch
**Solution:**
1. Ensure callback URL in Etsy app matches exactly: `http://localhost:8000/etsy/callback`
2. Use OAuth 2.0 (not OAuth 1.0)
3. Check scopes include `listings_r shops_r`

### Apify 429 Rate Limit
**Problem:** Too many concurrent requests
**Solution:**
1. Reduce concurrency (max 1-2 scraping jobs at a time)
2. Add delays between Apify actor calls (10-15 seconds)
3. Monitor credit usage in Apify dashboard

### Instaloader Account Ban
**Problem:** Instagram detected automated access
**Solution:**
1. **STOP IMMEDIATELY** - do not retry for 24 hours
2. Increase delays to 3-5 minutes between requests
3. Switch to Apify as primary method
4. Consider using Instaloader only for high-value creators

### Playwright CAPTCHA Challenge
**Problem:** TikTok detected headless browser
**Solution:**
1. Add stealth plugins: `playwright-stealth`
2. Use residential proxies instead of datacenter proxies
3. Reduce scraping frequency (max 10 profiles per session)
4. Recycle browser every 20 requests

### Claude API 529 Overloaded
**Problem:** Anthropic servers temporarily overloaded
**Solution:**
1. Implement exponential backoff retry (wait 5s, 10s, 20s)
2. Batch requests where possible
3. Retry failed requests after 60 seconds

---

## 📞 **Support Resources**

### Platform Documentation
- **YouTube Data API:** https://developers.google.com/youtube/v3
- **Etsy API:** https://developers.etsy.com/documentation
- **Apify:** https://docs.apify.com
- **Instaloader:** https://instaloader.github.io
- **Playwright:** https://playwright.dev/python
- **Anthropic:** https://docs.anthropic.com

### Community Forums
- YouTube API: https://stackoverflow.com/questions/tagged/youtube-api
- Etsy API: https://community.etsy.com/t5/Developers/ct-p/developers
- Apify: https://discord.gg/jyEM2PRvMU

---

**END OF API INTEGRATION PREFLIGHT CHECKLIST**

**Status:** ✅ Ready for implementation once all checkboxes are completed

**Next Steps:**
1. Complete all checklist items above
2. Document any deviations or issues in Risk Assessment
3. Begin Phase 1 implementation (YouTube + Etsy foundation)
