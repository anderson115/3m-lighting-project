# 3M Lighting Project - Module Architecture

**Standard Module Structure v1.0**

---

## 📁 **Standard Module Template**

All modules in this project follow this standardized structure:

```
modules/{module-name}/
├── README.md                  # Complete module documentation
├── config/                    # Configuration files
│   ├── .env.example           # Template for API keys
│   ├── .env                   # Actual credentials (gitignored)
│   └── .gitignore             # Protect sensitive files
├── core/                      # Core business logic
│   ├── orchestrator.py        # Main pipeline coordinator
│   ├── config.py              # Configuration management
│   └── __init__.py
├── {component-dirs}/          # Feature-specific directories
│   ├── *.py                   # Implementation files
│   └── __init__.py
├── data/                      # Input/output data
│   ├── cache/                 # Cached API responses
│   └── reports/               # Generated reports
├── docs/                      # Technical documentation
│   ├── PRD-{module-name}.md   # Product requirements
│   └── TECHNICAL-ARCHITECTURE.md
└── tests/                     # Test files (optional)
    └── test_*.py
```

---

## 🔧 **Active Modules**

### **expert-authority** ✅ PRODUCTION
**Purpose**: Reddit & Stack Exchange expert discussion analysis

**Structure**:
```
modules/expert-authority/
├── README.md                               # Full documentation
├── config/                                 # API credentials
│   ├── .env.example
│   ├── .env (gitignored)
│   └── .gitignore
├── core/                                   # Pipeline coordination
│   ├── orchestrator.py                     # Main analysis pipeline
│   ├── config.py                           # Configuration management
│   └── __init__.py
├── scrapers/                               # Data collection
│   ├── reddit_scraper.py                   # PRAW Reddit scraper
│   ├── stackexchange_scraper.py            # Stack Exchange REST API
│   └── __init__.py
├── analyzers/                              # Semantic analysis
│   ├── production_analyzer.py              # LLM-powered analysis
│   └── __init__.py
├── reporters/                              # Report generation
│   ├── html_reporter.py                    # HTML reports
│   ├── excel_reporter.py                   # Excel workbooks
│   └── __init__.py
├── data/                                   # Outputs
│   ├── cache/                              # API response cache
│   │   ├── reddit/                         # Reddit JSON data
│   │   └── stackexchange/                  # Stack Exchange JSON
│   └── reports/                            # Generated reports
│       ├── *.html                          # HTML deliverables
│       └── *.xlsx                          # Excel workbooks
├── docs/                                   # Documentation
│   ├── PRD-expert-authority.md
│   ├── TECHNICAL-ARCHITECTURE.md
│   ├── CITATION-INTEGRITY-PROTOCOL.md
│   └── DATA-SOURCE-ACCESS-METHODS.md
└── tests/                                  # Test suite
    └── (empty - tests at project root)
```

**Key Features**:
- 3-tier analysis system (Tier 1/2/3)
- 100% citation validation
- Claude Opus 4 semantic analysis
- Multi-format reports (HTML + Excel)

---

### **consumer-video** ✅ PRODUCTION
**Purpose**: YouTube consumer interview JTBD analysis

**Structure**:
```
modules/consumer-video/
├── README.md
├── config/
├── scripts/                                # Analysis pipeline
│   ├── consumer_analyzer.py
│   ├── jtbd_extractor.py
│   ├── emotion_analyzer.py
│   ├── product_tracker.py
│   └── generate_client_report.py
├── data/
│   ├── processed/                          # Analysis outputs
│   └── deliverables/                       # Client reports
├── docs/
└── prompts/                                # LLM prompts
```

---

### **youtube-datasource** ✅ PRODUCTION
**Purpose**: YouTube video download & multimodal analysis

**Structure**:
```
modules/youtube-datasource/
├── README.md
└── scripts/
    ├── video_downloader.py                 # YouTube download
    └── multimodal_analyzer.py              # Whisper + LLaVA
```

---

### **social-signal** 📋 PLANNED
**Purpose**: Visual social media trend analysis (Pinterest, Instagram, TikTok)

---

### **creator-intelligence** 📋 PRE-DEVELOPMENT (Documentation Complete)
**Purpose**: Multi-platform creator analysis for lighting industry (YouTube, Etsy, Instagram, TikTok)

**Structure**:
```
modules/creator-intelligence/
├── README.md                               # Full documentation
├── config/                                 # API credentials
│   ├── .env.example
│   ├── .env (gitignored)
│   └── .gitignore
├── core/                                   # Pipeline coordination
│   ├── orchestrator.py                     # Main analysis pipeline
│   ├── config.py                           # Configuration management
│   └── database.py                         # SQLite operations
├── scrapers/                               # Multi-platform data collection
│   ├── youtube_scraper.py                  # YouTube Data API v3
│   ├── etsy_scraper.py                     # Etsy API v3 (OAuth)
│   ├── instagram_scraper.py                # Apify + Instaloader fallback
│   ├── tiktok_scraper.py                   # Apify + Playwright fallback
│   ├── apify_client.py                     # Apify SDK wrapper
│   ├── failover_pool.py                    # Scraper failover logic
│   └── __init__.py
├── analyzers/                              # LLM-powered analysis
│   ├── content_classifier.py               # Relevance classification
│   ├── pain_point_detector.py              # Pain point extraction
│   ├── language_extractor.py               # Consumer language extraction
│   ├── trend_analyzer.py                   # Theme clustering
│   ├── creator_scorer.py                   # Research/partnership scoring
│   └── __init__.py
├── reporters/                              # Report generation
│   ├── html_reporter.py                    # HTML reports
│   ├── excel_reporter.py                   # Excel workbooks
│   ├── json_exporter.py                    # JSON export
│   └── __init__.py
├── data/                                   # Outputs
│   ├── cache/                              # Raw scraped data (JSON)
│   │   ├── youtube/
│   │   ├── etsy/
│   │   ├── instagram/
│   │   └── tiktok/
│   ├── database/                           # SQLite database
│   │   └── creators.db
│   ├── reports/                            # Generated reports
│   │   ├── *.html
│   │   ├── *.xlsx
│   │   └── *.json
│   └── logs/                               # Error logs
├── docs/                                   # Documentation
│   ├── PRD-creator-intelligence.md         # Product requirements v1.0
│   ├── TECHNICAL-ARCHITECTURE.md           # System design
│   ├── API-INTEGRATION-PREFLIGHT.md        # Setup checklist
│   ├── RISK-ASSESSMENT.md                  # Risk mitigation
│   └── DATABASE-SCHEMA.md                  # Database documentation
└── tests/                                  # Test suite
    └── (to be implemented)
```

**Key Features**:
- 3-tier data collection (Official APIs → Managed scrapers → Aggressive scraping)
- Hybrid 70% scripted / 30% LLM analysis
- Triple intelligence: Creator trends, consumer language dictionary, partnership database
- Viability scoring (Research score + Partnership score 0-100)
- Grey-area scraping for Instagram/TikTok with risk mitigation
- Multi-format reports (HTML + Excel + JSON)

**Status**: Documentation complete (PRD, Architecture, Preflight, Risk Assessment, Database Schema, README)

---

## 🎯 **Module Development Checklist**

When creating a new module:

- [ ] Create standardized folder structure
- [ ] Add comprehensive README.md
- [ ] Set up config/ with .env.example and .gitignore
- [ ] Implement core/orchestrator.py for main pipeline
- [ ] Create data/ directories (cache/, reports/)
- [ ] Write docs/PRD-{module-name}.md
- [ ] Add tests/ directory
- [ ] Update project README.md modules section
- [ ] Verify module imports work: `from modules.{module}.core.orchestrator import *`

---

## 📝 **Naming Conventions**

- **Module Names**: Lowercase with hyphens (e.g., `expert-authority`)
- **Python Files**: Lowercase with underscores (e.g., `production_analyzer.py`)
- **Classes**: PascalCase (e.g., `ExpertAuthorityOrchestrator`)
- **Functions**: snake_case (e.g., `run_analysis()`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DEFAULT_TIER_CONFIG`)

---

## 🔐 **Security Standards**

All modules must:
- Store API keys in `.env` files (gitignored)
- Provide `.env.example` templates
- Use `python-dotenv` with `override=True`
- Never hardcode credentials
- Include `.gitignore` in config/ directories

---

## 📊 **Quality Standards**

All production modules must have:
- ✅ Comprehensive README.md with usage examples
- ✅ 100% citation/source validation (where applicable)
- ✅ Error handling with graceful fallbacks
- ✅ Logging with appropriate levels
- ✅ Data caching to minimize API calls
- ✅ Multiple output formats (HTML/Excel/JSON)

---

**Version**: 1.0.0
**Last Updated**: 2025-10-10
**Maintainer**: 3M Lighting Project Team
