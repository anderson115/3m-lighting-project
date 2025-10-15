# Category Intelligence Module

**Version:** 1.0.0
**Status:** Bootstrap Phase
**Last Updated:** 2025-10-15

---

## Overview

The **Category Intelligence Module** generates comprehensive, client-ready industry reports for any product category through automated research, web scraping, and multi-source data collection.

### Core Principles
- **100% Authentic Data**: Zero fabrication tolerance
- **Full Source Documentation**: Every data point traceable with working citations
- **Current Information**: All research as of 2025-10-15
- **Client-Ready Output**: Professional HTML reports with Offbrain Insights branding

---

## Quick Start

```bash
# Run category intelligence analysis
cd /Users/anderson115/00-interlink/12-work/3m-lighting-project
source venv/bin/activate
python -m modules.category_intelligence.run_analysis --category "Smart Home Lighting"
```

---

## Module Structure

```
category-intelligence/
├── core/
│   ├── orchestrator.py          # Main pipeline coordinator
│   ├── config.py                # Configuration management
│   └── source_tracker.py        # Citation tracking
├── collectors/
│   ├── brand_discovery.py       # Brand identification
│   ├── product_taxonomy.py      # Category hierarchy
│   ├── pricing_collector.py    # Price data
│   ├── market_share.py          # Market share research
│   ├── market_size.py           # Industry size/projections
│   └── resource_finder.py       # Learning resources
├── scrapers/
│   ├── ecommerce.py             # Amazon/Walmart scraping
│   ├── financial.py             # Company filings
│   └── news.py                  # Industry news
├── validators/
│   ├── source_validator.py      # URL verification
│   └── data_validator.py        # Data quality checks
├── generators/
│   ├── html_report.py           # HTML generation
│   └── templates/
│       └── category_report.html # Report template
├── utils/
│   ├── web_fetcher.py           # HTTP with retry
│   ├── archiver.py              # Source archiving
│   └── date_utils.py            # Date handling
├── data/                        # Output storage
└── outputs/                     # Generated reports
```

---

## Research Pipeline

```
[Category Input]
    ↓
[Brand Discovery] → 10-25 major brands identified
    ↓
[Product Categorization] → Hierarchical taxonomy created
    ↓
[Pricing Analysis] → Price ranges per tier
    ↓
[Market Share Research] → Share estimates with confidence
    ↓
[Market Size Analysis] → Current + 5-year projections
    ↓
[Learning Resources] → Curated authoritative sources
    ↓
[Source Validation] → All URLs verified
    ↓
[HTML Report Generation] → Client-ready deliverable
```

---

## Output Files

Every analysis generates:

```
outputs/{category_name}_Category_Intelligence.html    # Primary report
outputs/sources/                                       # Archived source content
    archived_page_001.html
    archived_page_002.pdf
    ...
outputs/data/                                          # Structured data
    brands.json
    pricing.json
    market_share.json
    market_size.json
    taxonomy.json
outputs/audit/                                         # Audit trail
    source_verification.json
    data_validation_log.txt
```

---

## Data Quality Standards

### Confidence Levels
- **High**: Primary source, official, current (<6 months)
- **Medium**: Secondary source, recent (<1 year)
- **Low**: Tertiary source, older data (>1 year)
- **Unverified**: Single source, outdated (>2 years)

### Required Metadata
Every data point includes:
- Source URL (working at generation time)
- Publisher/authority
- Access date
- Exact excerpt/quote
- Archived copy path
- Confidence level

---

## Example Usage

### Command Line
```bash
python -m modules.category_intelligence.run_analysis \
    --category "Smart Home Lighting" \
    --output-dir outputs/smart_home_lighting
```

### Python API
```python
from modules.category_intelligence.core.orchestrator import CategoryIntelligenceOrchestrator

orchestrator = CategoryIntelligenceOrchestrator()
report = orchestrator.analyze_category("Smart Home Lighting")

# Report contains:
# - brands: List of major brands with sources
# - taxonomy: Product categorization hierarchy
# - pricing: Price analysis by tier
# - market_share: Share estimates with confidence
# - market_size: Current size + projections
# - resources: Learning resources
# - html_path: Path to generated HTML report
```

---

## Configuration

Edit `core/config.py` to customize:

```python
# Search depth
MAX_BRANDS_TO_DISCOVER = 25
MAX_PRODUCTS_PER_SUBCATEGORY = 50

# Source requirements
MIN_SOURCES_PER_CLAIM = 2
MAX_SOURCE_AGE_MONTHS = 12

# Output options
GENERATE_HTML = True
ARCHIVE_SOURCES = True
CREATE_AUDIT_TRAIL = True
```

---

## Dependencies

```bash
requests>=2.31.0
beautifulsoup4>=4.12.0
selenium>=4.15.0
pydantic>=2.5.0
jinja2>=3.1.2
```

Install:
```bash
pip install -r requirements.txt
```

---

## Testing

```bash
# Run full test suite
pytest modules/category-intelligence/tests/

# Test specific category
python modules/category-intelligence/tests/test_category_intelligence.py --category "LED Bulbs"

# Validate existing report
python modules/category-intelligence/tests/validate_report.py --report outputs/report.html
```

---

## Troubleshooting

### Common Issues

**Issue: "No brands discovered"**
- Category name may be too specific or niche
- Try broader search terms
- Check internet connection

**Issue: "Source URLs not working"**
- Some sources may have moved/changed
- Archived copies available in `outputs/sources/`
- Re-run analysis for updated sources

**Issue: "Market size data unavailable"**
- Some niche categories lack public market research
- Report will clearly indicate data gaps
- Never fabricates placeholder data

---

## Development Status

### Phase 1: Core Pipeline ✅ (Current)
- [x] Module structure setup
- [x] PRD documentation
- [ ] Orchestrator implementation
- [ ] Brand discovery collector
- [ ] Source tracking system
- [ ] Basic HTML generation

### Phase 2: Data Collection (Planned)
- [ ] Product taxonomy
- [ ] Pricing collector
- [ ] Market research
- [ ] Source validation

### Phase 3: Quality & Polish (Future)
- [ ] Full HTML styling
- [ ] Comprehensive testing
- [ ] Performance optimization

---

## Contributing

This module follows strict data authenticity standards:

✅ **MUST**: Include source URLs for every claim
✅ **MUST**: Archive source content
✅ **MUST**: Flag estimated vs. confirmed data
❌ **NEVER**: Use placeholder/fabricated data
❌ **NEVER**: Infer data without sources
❌ **NEVER**: Use outdated sources without disclosure

---

## License

Internal use only - Offbrain Insights proprietary module

---

## Contact

**Module Owner**: Offbrain Insights Development Team
**Created**: 2025-10-15
**Documentation**: See `PRD.md` for complete product requirements
