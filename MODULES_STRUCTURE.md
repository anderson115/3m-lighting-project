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

### **creator-discovery** 📋 PLANNED
**Purpose**: Multi-platform creator identification and profiling

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
