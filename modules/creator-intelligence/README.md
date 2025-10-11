# Creator Intelligence Module

**Multi-Platform Creator Analysis for Lighting Industry**

---

## 🎯 Overview

The Creator Intelligence Module discovers, analyzes, and scores creators across YouTube, Etsy, Instagram, and TikTok to identify lighting trends, extract consumer marketing language, and build a database of potential brand partners and research participants.

**Status**: 📋 PRE-DEVELOPMENT (Documentation Complete)
**Version**: 1.0.0
**Last Updated**: 2025-10-10

---

## ✨ Key Features

### 1. Multi-Platform Creator Discovery
- **YouTube**: Official Data API v3 (10K quota/day)
- **Etsy**: Official API v3 (OAuth)
- **Instagram**: Apify Scraper (primary) + Instaloader (fallback)
- **TikTok**: Apify Scraper (primary) + Playwright (fallback)

### 2. Hybrid Analysis (70% Scripted / 30% LLM)
- ✅ Scripted: Platform APIs, metrics calculation, database operations
- ✅ LLM-Powered: Content relevance classification, pain point extraction, consumer language analysis
- ✅ Not keyword-dependent: Semantic understanding via Claude Sonnet 4

### 3. Triple Intelligence Objectives
- **Creator Trends**: Jobs, projects, pain points, language patterns
- **Consumer Language Dictionary**: Marketing-ready terminology extracted from real content
- **Partnership Database**: Scored creators (Research + Partnership viability 0-100)

### 4. Grey-Area Scraping (Instagram/TikTok)
- Aggressive failover tactics when official APIs unavailable
- Risk-mitigated with rate limiting, proxy rotation, circuit breakers
- Explicitly approved by stakeholder for comprehensive coverage

---

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.11+
python --version

# Install dependencies
pip install google-api-python-client apify-client instaloader playwright anthropic python-dotenv openpyxl

# Install Playwright browsers
playwright install chromium
```

### API Keys Setup

```bash
# 1. Copy environment template
cp modules/creator-intelligence/config/.env.example modules/creator-intelligence/config/.env

# 2. Add your API keys to .env
# Required:
YOUTUBE_API_KEY=your_youtube_api_key
ANTHROPIC_API_KEY=sk-ant-api03-your_key

# Optional (but recommended):
APIFY_TOKEN=apify_api_your_token
ETSY_API_KEY=your_etsy_keystring
```

### Basic Usage

```python
from modules.creator_intelligence.core.orchestrator import CreatorIntelligenceOrchestrator

# Initialize orchestrator
orchestrator = CreatorIntelligenceOrchestrator(tier=1)

# Run analysis
results = orchestrator.run_analysis(
    platforms=['youtube', 'etsy'],
    keywords=['LED lighting tutorial', 'residential lighting installation'],
    target_creator_count=100
)

# Access results
print(f"Creators discovered: {results['creators_discovered']}")
print(f"HTML Report: {results['reports']['html']}")
print(f"Excel Report: {results['reports']['excel']}")
print(f"Database: {results['database_path']}")
```

---

## 📊 Data Sources & Methods

### Tier 1: Official APIs (Stable ⭐⭐⭐⭐⭐)

| Platform | Method | Cost | Quota | Risk |
|----------|--------|------|-------|------|
| YouTube | Data API v3 | Free | 10K units/day | Low |
| Etsy | API v3 OAuth | Free | 10K req/day | Low |

### Tier 2: Managed Scrapers (Stable ⭐⭐⭐⭐)

| Platform | Method | Cost | Quota | Risk |
|----------|--------|------|-------|------|
| Instagram | Apify Scraper | $0-49/mo | 5K credits/mo | Medium |
| TikTok | Apify Scraper | $0-49/mo | 5K credits/mo | Medium |

### Tier 3: Aggressive Scraping (Stable ⭐⭐⭐)

| Platform | Method | Cost | Risk | Mitigation |
|----------|--------|------|------|------------|
| Instagram | Instaloader | Free | 🔴 HIGH (bans) | 2-3 min delays, circuit breaker |
| TikTok | Playwright | Free | 🔴 HIGH (detection) | Stealth, proxy rotation |

---

## 🎯 Use Cases

### Use Case 1: Market Research
**Goal**: Understand what professional installers struggle with

```python
orchestrator = CreatorIntelligenceOrchestrator(tier=2)
results = orchestrator.run_analysis(
    platforms=['youtube', 'instagram'],
    keywords=['commercial LED installation', 'residential retrofit'],
    target_creator_count=250,
    geographic_filters={'countries': ['US', 'CA']}
)

# Access pain points
pain_points = results['pain_points_summary']
# Example output: "LED strip dimming compatibility issues" mentioned 47 times
```

### Use Case 2: Marketing Language Research
**Goal**: Extract consumer terminology for ad copy

```python
# Run analysis
results = orchestrator.run_analysis(platforms=['etsy', 'instagram'], ...)

# Access consumer language dictionary
language_dict = results['consumer_language_dictionary']
# Example: "warm white" (234 mentions), "under-cabinet lighting" (189 mentions)
```

### Use Case 3: Creator Partnerships
**Goal**: Find 50 US-based creators for brand partnerships

```python
results = orchestrator.run_analysis(
    platforms=['youtube', 'tiktok'],
    target_creator_count=500,
    geographic_filters={'countries': ['US'], 'min_followers': 10000}
)

# Get top creators
top_partnerships = results['top_partnership_creators']
# Sorted by partnership_viability_score (0-100)
```

---

## 📁 Module Structure

```
modules/creator-intelligence/
├── README.md                       # This file
├── config/
│   ├── .env.example                # API key template
│   └── .env                        # Your API keys (gitignored)
├── core/
│   ├── orchestrator.py             # Main pipeline coordinator
│   ├── config.py                   # Configuration management
│   └── database.py                 # SQLite operations
├── scrapers/
│   ├── youtube_scraper.py          # YouTube Data API
│   ├── etsy_scraper.py             # Etsy API v3
│   ├── instagram_scraper.py        # Apify + Instaloader
│   ├── tiktok_scraper.py           # Apify + Playwright
│   └── failover_pool.py            # Automatic method switching
├── analyzers/
│   ├── content_classifier.py       # LLM relevance detection
│   ├── pain_point_detector.py      # LLM pain point extraction
│   ├── language_extractor.py       # Consumer language extraction
│   └── creator_scorer.py           # Research/partnership scoring
├── reporters/
│   ├── html_reporter.py            # HTML report generation
│   ├── excel_reporter.py           # Excel workbook generation
│   └── json_exporter.py            # JSON export
├── data/
│   ├── cache/                      # Scraped data (JSON)
│   ├── database/                   # SQLite database
│   ├── reports/                    # Generated reports
│   └── logs/                       # Error logs
└── docs/
    ├── PRD-creator-intelligence.md # Product requirements
    ├── TECHNICAL-ARCHITECTURE.md   # System design
    ├── API-INTEGRATION-PREFLIGHT.md # Setup checklist
    ├── RISK-ASSESSMENT.md          # Risk mitigation strategies
    └── DATABASE-SCHEMA.md          # Database documentation
```

---

## 🔧 Configuration

### Tier Selection

- **Tier 1**: Official APIs only (YouTube + Etsy) - safest, limited coverage
- **Tier 2**: Add managed scrapers (Instagram/TikTok via Apify) - recommended
- **Tier 3**: Add aggressive scraping (Instaloader + Playwright) - highest risk, full coverage

```python
# Recommended: Start with Tier 2
orchestrator = CreatorIntelligenceOrchestrator(tier=2)
```

### Geographic Filters

```python
results = orchestrator.run_analysis(
    platforms=['youtube'],
    keywords=['LED lighting'],
    geographic_filters={
        'countries': ['US', 'CA', 'UK', 'AU'],  # Target markets
        'languages': ['en'],                     # English only
        'exclude_countries': ['CN', 'RU']        # Exclude specific countries
    }
)
```

### Custom Keywords

```python
# Niche-specific keywords
keywords = [
    'LED strip installation',
    'smart home lighting',
    'residential lighting upgrade',
    'commercial LED retrofit',
    'under-cabinet lighting',
    'ambient mood lighting'
]
```

---

## 📊 Output Formats

### HTML Report
- Executive summary (creator count, top themes)
- Top 50 research-viable creators (with scores)
- Top 50 partnership-viable creators (with scores)
- Consumer language dictionary (by category)
- Trending themes
- Pain points analysis

### Excel Workbook (7 Sheets)
1. **Summary**: Overview statistics
2. **Top Research Creators**: Sortable table with filters
3. **Top Partnership Creators**: Contact info + scores
4. **Consumer Language**: Frequency analysis
5. **Trending Themes**: Theme breakdown
6. **Pain Points**: Categorized pain points
7. **Raw Data**: Full dataset for custom analysis

### JSON Export
- Full dataset for programmatic access
- UI-ready format for future frontend
- Includes all metadata, scores, timestamps

---

## ⚙️ Advanced Features

### Viability Scoring

**Research Viability Score (0-100)**:
- Engagement rate percentile (30%)
- Authenticity (20%)
- Content quality (25%)
- Relevance (15%)
- Geographic match (10%)

**Partnership Viability Score (0-100)**:
- Brand alignment (30%)
- Audience size (25%)
- Professionalism (20%)
- Consistency (15%)
- Prior partnerships (10%)

### Failover Logic

Automatic method switching when primary scraper fails:

```
Instagram:
  1. Try Apify Instagram Scraper (primary)
  2. If fails → Try Instaloader (fallback)
  3. If 429 error → Activate circuit breaker (stop 24h)

TikTok:
  1. Try Apify TikTok Scraper (primary)
  2. If fails → Try Playwright headless browser
  3. If CAPTCHA → Skip and log
```

### Circuit Breaker (Instagram Protection)

```python
# Automatically stops scraping if Instagram ban detected
class CircuitBreaker:
    def trigger(self):
        logger.critical("🚨 INSTAGRAM BAN DETECTED")
        logger.critical("⏸️ Stopping for 24 hours")
        # Wait 24 hours before retrying
```

---

## 🧪 Testing

### Preflight Checklist

Before full deployment, complete all items in:
📄 `docs/API-INTEGRATION-PREFLIGHT.md`

**Required Tests:**
- [ ] YouTube API returns results
- [ ] Etsy OAuth flow completes
- [ ] Apify credits available
- [ ] Instaloader rate limiting works
- [ ] Playwright launches successfully
- [ ] Claude API classification returns valid JSON
- [ ] SQLite database created
- [ ] All logs writing to file

### Example Test Run

```bash
# Test with 10 creators across all platforms
python3 << EOF
from modules.creator_intelligence.core.orchestrator import CreatorIntelligenceOrchestrator

orchestrator = CreatorIntelligenceOrchestrator(tier=2)
results = orchestrator.run_analysis(
    platforms=['youtube', 'etsy', 'instagram', 'tiktok'],
    keywords=['LED lighting'],
    target_creator_count=10  # Small test
)

print(f"✅ Test complete! Found {results['creators_discovered']} creators")
print(f"Reports: {results['reports']}")
EOF
```

---

## 🚨 Troubleshooting

### YouTube 403 Quota Exceeded
**Solution**: Request quota increase at https://support.google.com/youtube/contact/yt_api_form

### Instagram 429 Ban
**Solution**: Circuit breaker activated - wait 24 hours, then use Apify only

### TikTok CAPTCHA Challenge
**Solution**: Switch to Apify, skip Playwright for this run

### Apify Credits Depleted
**Solution**: Upgrade to paid tier ($49/month for 50K credits) or wait for monthly reset

### LLM Classification Errors
**Solution**: Adjust confidence threshold in `analyzers/content_classifier.py` (default: 0.70)

---

## 📈 Performance

### Estimated Runtime (500 Creators)

| Phase | Time | Notes |
|-------|------|-------|
| YouTube discovery | 5-10 min | API calls + caching |
| Etsy discovery | 5-10 min | API calls + OAuth |
| Instagram (Apify) | 15-20 min | Managed scraper |
| TikTok (Apify) | 15-20 min | Managed scraper |
| LLM content classification | 5-10 min | Claude Sonnet 4 batch |
| Pain point extraction | 10-15 min | Claude Sonnet 4 |
| Language extraction | 10-15 min | Claude Sonnet 4 |
| Scoring | 2-5 min | Pure computation |
| Report generation | 3-5 min | HTML + Excel + JSON |
| **TOTAL** | **70-120 min** | ~1.5-2 hours for 500 creators |

### Cost Estimate (500 Creators)

| Component | Cost | Notes |
|-----------|------|-------|
| YouTube API | $0 | Free tier (may need quota increase) |
| Etsy API | $0 | Free tier |
| Apify | $0-49 | Free tier: 5K credits (~400 profiles) |
| Claude Sonnet 4 | ~$12 | LLM analysis (~500K tokens) |
| **TOTAL** | **$12-61** | Depends on Apify usage |

---

## 🔐 Security & Compliance

### API Key Storage
- All keys in `.env` file (gitignored)
- Never hardcode credentials
- Use `python-dotenv` with `override=True`

### Grey-Area Scraping Disclaimer
⚠️ **Instagram/TikTok scraping may violate Terms of Service**
- For market research and competitive intelligence only
- Do not redistribute scraped data
- Obtain legal review before commercial use
- GDPR/CCPA: Only scrape public data, honor deletion requests

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **README.md** | Quick start and overview (this file) |
| **PRD-creator-intelligence.md** | Complete product requirements |
| **TECHNICAL-ARCHITECTURE.md** | System design and code structure |
| **API-INTEGRATION-PREFLIGHT.md** | Pre-implementation setup checklist |
| **RISK-ASSESSMENT.md** | Risk mitigation strategies |
| **DATABASE-SCHEMA.md** | SQLite/PostgreSQL schema |

---

## 🤝 Support

### Issues & Questions
1. Check troubleshooting section above
2. Review docs/ directory for detailed guides
3. Check logs in `data/logs/creator_intelligence.log`

### Related Modules
- **Expert Authority**: Reddit/Stack Exchange analysis (reference implementation)
- **Consumer Video**: YouTube JTBD analysis (shared patterns)
- **YouTube Datasource**: Whisper + LLaVA pipeline (multimodal analysis)

---

## 📄 License

Proprietary - 3M Lighting Project

---

**Status**: 📋 Ready for implementation after preflight completion

**Next Steps**:
1. Complete API Integration Preflight Checklist
2. Run small test (10 creators)
3. Validate outputs (manual spot-check)
4. Scale to full production (500+ creators)
