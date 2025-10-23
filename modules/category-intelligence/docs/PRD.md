# Category Intelligence Module - Product Requirements Document

**Version:** 1.0.0
**Date:** 2025-10-15
**Author:** Offbrain Insights
**Status:** Draft

---

## Executive Summary

The **Category Intelligence Module** generates comprehensive, client-ready industry reports for any product category. It conducts foundational research combining web scraping, API data collection, and multi-source intelligence gathering to produce fully documented, citation-backed reports with 100% authentic data.

**Core Principle:** Zero fabrication tolerance. Every data point must be traceable to original sources with working citations.

---

## Problem Statement

Clients need rapid, comprehensive category analysis to understand market dynamics, competitive landscapes, and category structures. Manual research takes weeks and often lacks proper source documentation. Existing solutions either:
- Provide shallow, high-level overviews
- Include fabricated/estimated data without sources
- Lack proper citation trails for audit verification
- Don't capture current market conditions

---

## Solution Overview

An automated research pipeline that:
1. **Discovers** major brands and market players through multi-source search
2. **Categorizes** products into hierarchy (category → subcategory → product type)
3. **Analyzes** pricing across market segments
4. **Estimates** market share and sales where data is publicly available
5. **Projects** market size using verifiable industry reports
6. **Documents** every finding with working source citations
7. **Generates** client-ready HTML reports with Offbrain Insights branding

---

## Core Requirements

### 1. Data Collection (MUST BE 100% AUTHENTIC)

#### Required Data Points
| Data Point | Sources | Verification Method |
|------------|---------|---------------------|
| **Major Brands** | - Web search results<br>- Industry reports<br>- Market research sites<br>- News articles | Cross-reference 3+ sources |
| **Product Categorization** | - E-commerce sites (Amazon, Walmart)<br>- Manufacturer websites<br>- Industry taxonomies | Manual validation required |
| **Price Points** | - E-commerce listings<br>- Manufacturer MSRPs<br>- Retailer websites | Live pricing data with timestamps |
| **Market Share** | - Public financial filings<br>- Industry analyst reports<br>- News articles | Flag as "estimated" if not from official source |
| **Market Size** | - Statista<br>- IBISWorld<br>- Grand View Research<br>- Industry associations | Require publication date + methodology |
| **Category Learning Resources** | - Industry publications<br>- Trade associations<br>- Academic research<br>- Professional blogs | Validate domain authority |

#### Data Collection Rules
- ✅ **MUST**: Include source URL, access date, exact quote/data point
- ✅ **MUST**: Archive source content for audit trail
- ✅ **MUST**: Flag estimated vs. confirmed data
- ✅ **MUST**: Use current date (2025-10-15) for "as of" statements
- ❌ **NEVER**: Use placeholder data ("~$X billion", "approximately Y%")
- ❌ **NEVER**: Infer data without explicit source
- ❌ **NEVER**: Use outdated sources (>2 years old) without disclosure

### 2. Research Pipeline

```
[Category Input]
    ↓
[Web Search: Brands + Market Reports]
    ↓
[Scrape E-commerce: Product Hierarchy + Pricing]
    ↓
[Collect Financial Data: Market Share + Revenue]
    ↓
[Gather Industry Reports: Market Size + Projections]
    ↓
[Validate All Sources: Working URLs + Accuracy Check]
    ↓
[Generate Report: HTML + Support Files]
```

#### Pipeline Stages

**Stage 1: Brand Discovery**
- Input: Category name (e.g., "Smart Home Lighting")
- Process:
  - Google/Bing search: "{category} major brands"
  - Wikipedia category pages
  - Industry association member lists
  - News articles mentioning market leaders
- Output: List of 10-25 major brands with source citations

**Stage 2: Product Categorization**
- Input: Category + identified brands
- Process:
  - Scrape Amazon/Walmart category hierarchies
  - Extract manufacturer product lines
  - Identify subcategories and product types
- Output: Hierarchical taxonomy with examples

**Stage 3: Pricing Analysis**
- Input: Product categories + brands
- Process:
  - Collect current pricing from e-commerce sites
  - Group by price tiers (entry/mid/premium)
  - Calculate price ranges per subcategory
- Output: Price distribution with source URLs

**Stage 4: Market Share Research**
- Input: Brand list
- Process:
  - Search financial news for market share data
  - Check public company filings (if applicable)
  - Review industry analyst reports (Statista, IBISWorld)
- Output: Market share estimates with confidence levels

**Stage 5: Market Size Analysis**
- Input: Category name
- Process:
  - Query market research databases
  - Extract projections from industry reports
  - Validate methodology and publication dates
- Output: Current market size + 5-year projections with sources

**Stage 6: Learning Resources**
- Input: Category name
- Process:
  - Identify trade associations
  - Find industry publications
  - Locate academic research
  - Discover professional communities
- Output: Curated resource list with descriptions

### 3. Source Documentation

Every data point must include:
```json
{
  "data_point": "Market size: $2.4B USD (2024)",
  "source": {
    "url": "https://www.statista.com/...",
    "title": "Smart Lighting Market Size 2024",
    "publisher": "Statista",
    "access_date": "2025-10-15",
    "excerpt": "The global smart lighting market was valued at...",
    "archived_path": "sources/statista_smart_lighting_2024.html",
    "confidence": "high",
    "data_type": "confirmed"
  }
}
```

### 4. Report Output

#### Primary Deliverable: HTML Report
- **Format**: Single HTML file with embedded CSS
- **Styling**: Offbrain Insights branding (match 3M Consumer Lighting report)
- **Sections**:
  1. Executive Summary
  2. Category Overview
  3. Major Brands & Market Players
  4. Product Categorization
  5. Pricing Analysis
  6. Market Share Estimates
  7. Market Size & Projections
  8. Learning Resources
  9. Methodology
  10. Source Citations

#### Supporting Files
```
outputs/
  {category_name}_Category_Intelligence.html     # Primary report
  sources/
    archived_page_001.html                       # Archived source content
    archived_page_002.pdf
    ...
  data/
    brands.json                                  # Structured data with sources
    pricing.json
    market_share.json
    market_size.json
    taxonomy.json
  audit/
    source_verification.json                     # Audit trail
    data_validation_log.txt
```

---

## Technical Architecture

### Module Structure
```
modules/category-intelligence/
├── README.md
├── PRD.md (this file)
├── core/
│   ├── __init__.py
│   ├── orchestrator.py          # Main pipeline coordinator
│   ├── config.py                # Configuration management
│   └── source_tracker.py        # Source citation manager
├── collectors/
│   ├── __init__.py
│   ├── brand_discovery.py       # Brand identification
│   ├── product_taxonomy.py      # Category hierarchy
│   ├── pricing_collector.py    # Price data gathering
│   ├── market_share.py          # Market share research
│   ├── market_size.py           # Industry size/projections
│   └── resource_finder.py       # Learning resources
├── scrapers/
│   ├── __init__.py
│   ├── ecommerce.py             # Amazon/Walmart/etc scraping
│   ├── financial.py             # Company filings
│   └── news.py                  # Industry news
├── validators/
│   ├── __init__.py
│   ├── source_validator.py      # URL/citation verification
│   └── data_validator.py        # Data quality checks
├── generators/
│   ├── __init__.py
│   ├── html_report.py           # HTML generation
│   └── templates/
│       └── category_report.html # Report template
├── utils/
│   ├── __init__.py
│   ├── web_fetcher.py           # HTTP requests with retry
│   ├── archiver.py              # Save source content
│   └── date_utils.py            # Current date handling
├── data/                        # Output storage
├── outputs/                     # Generated reports
└── tests/
    └── test_category_intelligence.py
```

### Key Components

**CategoryIntelligenceOrchestrator**
- Coordinates all research stages
- Manages source tracking
- Validates data authenticity
- Generates final report

**SourceTracker**
- Records every source URL
- Archives source content
- Verifies citations are working
- Generates audit trail

**DataValidator**
- Flags estimated vs. confirmed data
- Checks source recency
- Verifies cross-references
- Ensures no placeholders

---

## Data Quality Standards

### Confidence Levels
- **High**: Primary source, official publication, current data (<6 months)
- **Medium**: Secondary source, industry report, recent data (<1 year)
- **Low**: Tertiary source, news mention, older data (>1 year)
- **Unverified**: Single source, cannot confirm, outdated (>2 years)

### Required Source Quality
- ✅ Working URL at time of report generation
- ✅ Reputable publisher (industry authority, major publication)
- ✅ Publication date clearly stated
- ✅ Methodology disclosed (for market research)
- ✅ Data is current or explicitly dated

### Red Flags (Auto-Reject)
- ❌ Broken/dead URLs
- ❌ Paywalled content without access
- ❌ Sources >3 years old for market data
- ❌ Blogs/forums without expertise verification
- ❌ Data without attribution

---

## API & Tool Requirements

### Required Integrations
- **Web Search**: Google Custom Search API or SerpAPI
- **Web Scraping**: BeautifulSoup4, Selenium (for dynamic content)
- **Data Storage**: JSON files with full source metadata
- **Web Archiving**: Save full HTML of source pages
- **HTTP Handling**: Requests with retry logic, user-agent rotation

### Optional Enhancements
- **Market Research APIs**: Statista API (paid), Data.gov
- **Financial Data**: SEC EDGAR API (for public companies)
- **E-commerce APIs**: Amazon Product API, Walmart API
- **News APIs**: NewsAPI, Google News RSS

---

## Success Metrics

### Quality Metrics
- **Source Verification**: 100% working URLs at generation time
- **Data Authenticity**: 0% fabricated/placeholder data
- **Citation Completeness**: Every claim has ≥1 source
- **Cross-Validation**: ≥2 sources for key market data

### Output Metrics
- **Brands Identified**: ≥10 major players per category
- **Price Data Points**: ≥50 products with current pricing
- **Market Size Data**: Current + 5-year projection with source
- **Learning Resources**: ≥5 authoritative sources

### Performance Metrics
- **Generation Time**: <30 minutes for standard category
- **Source Archive Size**: <500MB per report
- **Report Completeness**: All 10 sections populated

---

## User Workflow

### Input
```bash
python run_category_intelligence.py --category "Smart Home Lighting"
```

### Process (Automated)
1. Validate category input
2. Run research pipeline (6 stages)
3. Validate all sources
4. Generate HTML report + support files
5. Create audit trail

### Output
```
✅ Report Generated: outputs/Smart_Home_Lighting_Category_Intelligence.html
📊 Data Files: 5 JSON files in outputs/data/
📚 Sources: 47 archived sources in outputs/sources/
✅ Audit Trail: outputs/audit/source_verification.json

Report Summary:
- 15 major brands identified
- 6 product subcategories
- 73 price points analyzed
- Market size: $X.XB (source: [citation])
- 12 learning resources curated

⚠️ Confidence Notes:
- Market share data: Medium confidence (industry estimates)
- All sources verified as of 2025-10-15
```

---

## Risk Mitigation

### Risk: Data Not Available
**Mitigation**:
- Clearly mark sections as "Data Not Available"
- Explain why (e.g., "No public market share data found after reviewing 20+ sources")
- Never fill gaps with estimates

### Risk: Outdated Sources
**Mitigation**:
- Flag sources >1 year old
- Search explicitly for "2024" or "2025" data
- Disclose data vintage in report

### Risk: Paywalled Content
**Mitigation**:
- Document paywall existence
- Use free abstracts/summaries where available
- Note "Full report requires subscription"

### Risk: Broken URLs
**Mitigation**:
- Archive source content locally
- Include archived copy in support files
- Verify URLs at generation time

---

## Development Phases

### Phase 1: Core Pipeline (Week 1)
- ✅ Module structure setup
- ✅ Orchestrator implementation
- ✅ Brand discovery collector
- ✅ Source tracking system
- ✅ Basic HTML report generation

### Phase 2: Data Collection (Week 2)
- Product taxonomy collector
- Pricing collector
- Market share research
- Market size analysis
- Source validation

### Phase 3: Quality & Polish (Week 3)
- Source archiving system
- Data validation rules
- Confidence level tagging
- HTML styling (Offbrain branding)
- Comprehensive testing

### Phase 4: Enhancement (Future)
- API integrations (Statista, etc.)
- Advanced scraping (JavaScript rendering)
- Multi-category comparison reports
- Dashboard/web interface

---

## Testing Strategy

### Test Cases
1. **End-to-End**: Run full pipeline for "Smart Home Lighting"
2. **Source Validation**: Verify all URLs are working
3. **Data Authenticity**: Audit all data points for sources
4. **Edge Cases**:
   - Niche category with limited data
   - Category with ambiguous name
   - Category with no market research available
5. **Output Validation**:
   - HTML renders correctly
   - All sections populated
   - Citations formatted properly

### Validation Checklist
- [ ] All data points have sources
- [ ] All source URLs work
- [ ] No placeholder/estimated data without disclosure
- [ ] Report uses current date (2025-10-15)
- [ ] Confidence levels assigned
- [ ] Archive files present
- [ ] Audit trail complete

---

## Dependencies

### Python Packages
```
requests>=2.31.0
beautifulsoup4>=4.12.0
selenium>=4.15.0
pydantic>=2.5.0
jinja2>=3.1.2
urllib3>=2.1.0
```

### External Tools
- Chrome/ChromeDriver (for Selenium)
- Internet connection (obviously)

---

## Appendix: Example Output

### Example Report Structure
```html
<!DOCTYPE html>
<html>
<head>
    <title>Smart Home Lighting | Category Intelligence Report</title>
    <!-- Offbrain Insights Styling -->
</head>
<body>
    <h1>Smart Home Lighting Category Intelligence</h1>
    <p class="meta">Prepared by: Offbrain Insights | Date: 2025-10-15</p>

    <section id="executive-summary">
        <h2>Executive Summary</h2>
        <p>The smart home lighting market is valued at $X.XB as of 2024
           <a href="#source-1">[1]</a>, with projected growth to $Y.YB by 2029
           <a href="#source-2">[2]</a>.</p>
    </section>

    <!-- ... other sections ... -->

    <section id="sources">
        <h2>Source Citations</h2>
        <ol>
            <li id="source-1">
                <strong>Statista:</strong> "Smart Lighting Market Size 2024"
                <br>URL: https://...
                <br>Accessed: 2025-10-15
                <br><a href="sources/archived_page_001.html">Archived Copy</a>
            </li>
        </ol>
    </section>
</body>
</html>
```

---

## Document Control

**Version History:**
- v1.0.0 (2025-10-15): Initial PRD creation

**Approvals Required:**
- [ ] Technical Lead
- [ ] Product Manager
- [ ] Data Quality Team

**Next Steps:**
1. Review and approve PRD
2. Bootstrap module structure
3. Implement Phase 1 components
4. Run test category analysis
