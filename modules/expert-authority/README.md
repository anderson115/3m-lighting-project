# Expert Authority Module

**Professional Reddit & Stack Exchange Analysis for Market Intelligence**

---

## 🎯 Overview

The Expert Authority Module discovers what professional electricians, contractors, and DIY experts actually recommend by analyzing real discussions from Reddit and Stack Exchange. Powered by multi-tier LLM semantic analysis with 100% citation validation.

**Status**: ✅ Production Ready
**Version**: 1.0.0
**Last Updated**: 2025-10-10

---

## 🚀 Quick Start

### **Installation**

```bash
# 1. Install dependencies
pip install praw anthropic openai python-dotenv openpyxl

# 2. Configure API keys
cp modules/expert-authority/config/.env.example modules/expert-authority/config/.env
# Edit .env with your API keys
```

### **Basic Usage**

```python
from modules.expert_authority.core.orchestrator import ExpertAuthorityOrchestrator

# Tier 1: Rule-based analysis (free, fast)
orchestrator = ExpertAuthorityOrchestrator(tier=1)
results = orchestrator.run_analysis(
    query="LED strip installation best practices",
    project_name="LED_Strip_Research"
)

# Tier 2: LLM semantic analysis + Excel
orchestrator = ExpertAuthorityOrchestrator(tier=2)
results = orchestrator.run_analysis(
    query="LED dimmer compatibility issues",
    project_name="Dimmer_Research",
    reddit_subreddits=["electricians", "HomeImprovement"]
)

# Tier 3: Extended LLM analysis (Claude Opus 4)
orchestrator = ExpertAuthorityOrchestrator(tier=3)
results = orchestrator.run_analysis(
    query="residential LED retrofit challenges",
    project_name="Market_Entry_Analysis"
)
```

### **Command Line**

```bash
# Run complete test suite
python test_expert_authority_complete.py

# Run 10% volume quick test
python test_expert_authority_quick.py

# Run Tier 3 client demo
python run_tier3_client_demo.py
```

---

## 📊 Features

### **Multi-Tier Analysis System**

| Tier | Analysis Method | LLM | Cost | Use Case |
|------|----------------|-----|------|----------|
| **Tier 1** | Rule-based pattern matching | None | Free | Quick theme discovery |
| **Tier 2** | Semantic LLM analysis | Claude Sonnet 4 | ~$0.50/analysis | Professional insights |
| **Tier 3** | Extended LLM deep-dive | Claude Opus 4 | ~$2/analysis | Strategic intelligence |

### **Core Capabilities**

- ✅ **Reddit Scraping**: PRAW official API (r/electricians, r/HomeImprovement, r/DIY)
- ✅ **Stack Exchange**: REST API (diy.stackexchange.com, electronics.stackexchange.com)
- ✅ **Theme Discovery**: Automatic identification of recurring topics
- ✅ **Consensus Extraction**: What professionals agree on
- ✅ **Safety Warnings**: Critical safety concerns (Tier 2+)
- ✅ **Controversy Detection**: Debated topics and mixed opinions (Tier 2+)
- ✅ **100% Citation Validation**: Every insight traces to source discussion
- ✅ **Multi-Format Reports**: HTML + Excel (Tier 2+)
- ✅ **Data Caching**: Automatic caching to minimize API calls

---

## 📁 Module Structure

```
modules/expert-authority/
├── README.md                       # This file
├── config/
│   ├── .env.example                # API key template
│   ├── .env                        # Your API keys (gitignored)
│   └── .gitignore                  # Protects credentials
├── core/
│   ├── config.py                   # Configuration management
│   └── orchestrator.py             # Main pipeline coordinator
├── scrapers/
│   ├── reddit_scraper.py           # Reddit PRAW scraper
│   └── stackexchange_scraper.py    # Stack Exchange REST API
├── analyzers/
│   └── production_analyzer.py      # LLM semantic analysis
├── reporters/
│   ├── html_reporter.py            # HTML report generation
│   └── excel_reporter.py           # Excel workbook generation
├── data/
│   ├── cache/                      # Scraped data cache
│   │   ├── reddit/                 # Reddit JSON data
│   │   └── stackexchange/          # Stack Exchange JSON data
│   └── reports/                    # Generated reports
│       ├── *.html                  # HTML reports
│       └── *.xlsx                  # Excel workbooks
├── docs/
│   ├── PRD-expert-authority.md     # Product requirements
│   ├── TECHNICAL-ARCHITECTURE.md   # Architecture details
│   ├── CITATION-INTEGRITY-PROTOCOL.md
│   └── DATA-SOURCE-ACCESS-METHODS.md
└── tests/
    └── (test files)
```

---

## 🔧 Configuration

### **Required API Keys**

Create `modules/expert-authority/config/.env`:

```bash
# Reddit API (Required for all tiers)
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=YourApp/1.0

# Stack Exchange API (Optional but recommended)
STACK_EXCHANGE_API_KEY=your_stackexchange_key

# Anthropic API (Required for Tier 2+)
ANTHROPIC_API_KEY=sk-ant-api03-...

# OpenAI API (Optional fallback)
OPENAI_API_KEY=sk-proj-...
```

### **Tier Configuration**

Edit `modules/expert_authority/core/config.py` to customize:

- Target discussion volumes (default: 100/300/500 for tiers 1/2/3)
- LLM model selection (Sonnet/Opus)
- Subreddit lists
- Output formats

---

## 📖 Usage Examples

### **Example 1: Market Research**

```python
orchestrator = ExpertAuthorityOrchestrator(tier=2)
results = orchestrator.run_analysis(
    query="smart home lighting automation pain points",
    project_name="Smart_Lighting_Market_Research",
    reddit_subreddits=["homeautomation", "smarthome", "electricians"]
)

# Access results
print(f"HTML Report: {results['reports']['html']}")
print(f"Excel Report: {results['reports']['excel']}")
print(f"Discussions analyzed: {results['discussion_count']}")
```

### **Example 2: Competitive Intelligence**

```python
orchestrator = ExpertAuthorityOrchestrator(tier=3)
results = orchestrator.run_analysis(
    query="Philips Hue vs LIFX comparison electrician recommendations",
    project_name="Competitive_Analysis_Smart_Bulbs"
)
```

### **Example 3: Product Development Insights**

```python
orchestrator = ExpertAuthorityOrchestrator(tier=2)
results = orchestrator.run_analysis(
    query="LED driver failure modes and reliability issues",
    project_name="Product_Reliability_Research",
    reddit_subreddits=["electricians", "AskElectronics"]
)
```

---

## 📊 Output Formats

### **HTML Reports**

Professional web-based reports with:
- Executive summary
- Theme breakdown with frequency percentages
- Consensus patterns
- Safety warnings (Tier 2+)
- Controversies (Tier 2+)
- Clickable citation links to source discussions
- Metadata (date, methodology, discussion count)

### **Excel Workbooks** (Tier 2+)

Multi-sheet workbooks containing:
- **Summary**: Overview statistics
- **Themes**: Detailed theme analysis
- **Consensus**: Agreement patterns
- **Controversies**: Debated topics
- **Safety**: Critical warnings
- **Raw Data**: Full discussion dataset

### **JSON Cache**

Structured JSON files with complete discussion data:
- Platform metadata
- Discussion titles, URLs, scores
- Comment threads
- Timestamps
- Author information

---

## 🔬 Technical Details

### **Data Sources**

| Platform | API | Rate Limits | Data Quality |
|----------|-----|-------------|--------------|
| Reddit | PRAW (official) | 60 req/min | High - professional electricians |
| Stack Exchange | REST API | 10,000 req/day | High - Q&A format |

### **LLM Models**

| Tier | Primary Model | Fallback | Context Window |
|------|--------------|----------|----------------|
| Tier 2 | Claude Sonnet 4 | GPT-4o-mini | 200K tokens |
| Tier 3 | Claude Opus 4 | Claude Sonnet 4 | 200K tokens |

### **Citation Validation**

Every insight includes:
- Discussion ID
- Platform (Reddit/Stack Exchange)
- Direct URL to source
- Validation rate tracked and logged (target: ≥95%)

---

## 🧪 Testing

### **Comprehensive Test Suite**

```bash
# Run all tests (config, citations, Tier 1, Tier 2)
python test_expert_authority_complete.py

# Expected output:
# ✅ Config integrity test: PASSED
# ✅ Citation validation: PASSED (100%)
# ✅ Tier 1 analysis: PASSED
# ✅ Tier 2 LLM analysis: PASSED
```

### **Quick Volume Test**

```bash
# Test at 10% volume (faster, good for validation)
python test_expert_authority_quick.py
```

### **Individual Tier Tests**

```python
# Test Tier 1 only
from modules.expert_authority.core.orchestrator import ExpertAuthorityOrchestrator
orchestrator = ExpertAuthorityOrchestrator(tier=1)
results = orchestrator.run_analysis(
    query="test query",
    project_name="Test_Tier1"
)
```

---

## 🚨 Troubleshooting

### **Common Issues**

**Issue**: `401 Authentication Error` from Anthropic
- **Solution**: Check `ANTHROPIC_API_KEY` in `.env`, ensure `override=True` in config.py line 18

**Issue**: No Reddit data scraped
- **Solution**: Verify Reddit API credentials, check subreddit names are correct

**Issue**: Stack Exchange returns 0 results
- **Solution**: Normal - Stack Exchange has fewer relevant discussions, focus on Reddit

**Issue**: Excel export fails
- **Solution**: Install openpyxl: `pip install openpyxl`

### **Debug Mode**

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now run analysis - will show detailed logs
```

---

## 📈 Performance

### **Typical Runtimes**

| Tier | Discussions | Runtime | Cost (Anthropic API) |
|------|------------|---------|---------------------|
| Tier 1 | 100 | ~30s | $0 (no LLM) |
| Tier 2 | 300 | ~3min | ~$0.50 |
| Tier 3 | 500 | ~5min | ~$2.00 |

### **API Usage**

- **Reddit**: ~2-5 API calls per 100 discussions
- **Stack Exchange**: ~2 API calls per query
- **Anthropic**: 1-2 LLM calls per analysis (prompt batching)

---

## 🔐 Security

- API keys stored in `.env` (gitignored)
- No hardcoded credentials
- `override=True` ensures .env file priority over environment variables
- All API communication over HTTPS

---

## 📝 Changelog

### **v1.0.0** (2025-10-10)
- ✅ Production release
- ✅ Tier 1/2/3 fully functional
- ✅ 100% citation validation
- ✅ Excel export (Tier 2+)
- ✅ Claude Opus 4 integration (Tier 3)
- ✅ Comprehensive test suite
- ✅ Client deliverable generator

---

## 📚 Additional Documentation

- **PRD**: `docs/PRD-expert-authority.md` - Full product requirements
- **Architecture**: `docs/TECHNICAL-ARCHITECTURE.md` - System design
- **Citations**: `docs/CITATION-INTEGRITY-PROTOCOL.md` - Validation protocol
- **Data Sources**: `docs/DATA-SOURCE-ACCESS-METHODS.md` - API details

---

## 🤝 Support

For issues or questions:
1. Check troubleshooting section above
2. Review test suite for examples
3. Inspect log files for detailed error messages

---

## 📜 License

Proprietary - 3M Lighting Project
