# Category Intelligence Module

**Version:** 2.0 (Agentic System)
**Status:** Production Ready
**Last Updated:** 2025-10-16

> **For Developers/LLMs**: See [`MODULE_GUIDE.md`](MODULE_GUIDE.md) for complete technical documentation, architecture, and coding standards.
> **Quick Reference**: See [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md) for test commands, key files, and metrics summary.

---

## Overview

The **Category Intelligence Module** performs institutional-grade market research for any product category, delivering comprehensive analysis with zero fabrication tolerance.

### Research Standard

Every category analysis delivers:

- **50+ brands** across 5 market tiers with revenue estimates and market share
- **Comprehensive taxonomy** with quantitative metrics (market size, units, brands, growth rates)
- **Product-level pricing** with volume data and competitive dynamics
- **Market sizing** with historical data (5 years) and projections (3-4 years)
- **Competitive landscape** analysis with threats and opportunities
- **30-40 curated resources** with URLs for validation

### Output Format

**HTML Report:** Clean, table-based professional report (150-250KB) with:
- Executive Summary
- Brand Landscape & Market Share (data table)
- Category Structure & Taxonomy (data table)
- Pricing Analysis (data tables per subcategory)
- Market Size & Growth Analysis
- Appendix: Resources & References

---

## Quick Start

```bash
# Run analysis for any category
python modules/category-intelligence/run_analysis.py --category "your category" --output "output_name"

# Example
python modules/category-intelligence/run_analysis.py --category "smart home security" --output "smart_home_security"

# Output: modules/category_intelligence/outputs/smart_home_security_Category_Intelligence.html
```

---

## Research Methodology

### 1. Brand Discovery (50+ brands)

**Objective:** Identify ALL significant brands across the competitive landscape

**Tier Structure:**
- **Tier 1:** National brands (>$500M annual revenue)
- **Tier 2:** Major retail private labels ($200M-$500M)
- **Tier 3:** Specialized/premium brands ($50M-$200M)
- **Tier 4:** Emerging & regional brands ($10M-$50M)
- **Tier 5:** Import, niche, and online-only brands

**Data Per Brand:**
- Parent company
- Estimated category revenue
- Market share percentage
- Market position
- Distribution channels
- Competitive strengths/weaknesses
- Growth trend
- Confidence level

**Research Sources:**
- Public company financial filings
- Retailer category data (Home Depot, Lowe's, Amazon, Walmart)
- Industry reports (IBISWorld, Grand View Research)
- Consumer purchase panels (NPD, Circana)

**Quality Standard:** 98%+ market coverage, unbiased across all channels

---

### 2. Taxonomy & Category Structure (4-8 subcategories)

**Objective:** Map complete category structure with quantitative metrics

**Subcategory Metrics:**
- Market Size (USD revenue range)
- Market Share (% of category)
- Units Sold (annual volume)
- Active Brands (brand count)
- Average Price Point
- Growth Rate (YoY %)

**Product-Level Detail:**
- 4-5 product types per subcategory
- Market share and pricing per product type
- Top brands per product type

**Keyword Research:**
- Consumer language (search terms, colloquial names)
- Industry language (technical terms, trade terminology)
- Category-level keywords and search terms

---

### 3. Pricing Analysis (by subcategory)

**Objective:** Comprehensive pricing intelligence organized by subcategory

**Data Per Subcategory:**
- Overall price range
- Average transaction value
- Median price
- Price distribution tiers

**Product-Level Pricing:**
- Typical price range per product type
- Average price
- Units sold annually
- Market share
- Top brands with prices
- Price drivers

**Volume Dynamics:**
- Total units/year
- Total revenue/year
- Average selling price trends
- Seasonal patterns

**Competitive Dynamics:**
- Price competition level
- Commoditization risk
- Premium segment growth
- Price erosion areas

**Research Sources:** 10,000+ SKUs from retailer databases, Amazon, manufacturer MSRPs

---

### 4. Market Share Research (15-25 top brands)

**Objective:** Validate brand positions with multi-source triangulation

**Brand-Level Analysis:**
- Market share percentage
- Category revenue
- Market position
- Competitive strengths
- Weaknesses
- Growth trend
- Confidence level

**Market Structure:**
- Concentration ratio (CR4, CR8)
- Fragmentation analysis
- Barriers to entry

**Competitive Landscape:**
- Key competitive factors
- Emerging threats
- Strategic opportunities

**Methodology Documentation:**
- Data sources (minimum 3 per brand)
- Calculation method
- Validation approach
- Confidence scoring

---

### 5. Market Sizing & Growth (historical + projections)

**Objective:** Quantify market with historical context and forward projections

**Current Market Size:**
- Total market in USD
- Geographic scope
- Confidence level
- Calculation basis

**Historical Growth (5 years back):**
- Annual market size
- YoY growth rates
- Key events

**Forward Projections (3-4 years):**
- Projected size
- Growth rate
- Confidence level
- Assumptions

**Subcategory Sizing:**
- Size and share per subcategory
- Growth rates
- Dynamics

**Growth Drivers (7-10 factors):**
- Driver name
- Impact level
- Description
- Quantified impact

**Growth Inhibitors (5-7 factors):**
- Inhibitor name
- Impact level
- Description
- Mitigation strategies

**Key Trends (5-8 trends):**
- Trend name
- Adoption status
- Description
- Category impact

---

### 6. Resource Curation (30-40 sources)

**Objective:** Compile authoritative sources for validation

**Resource Categories:**
1. Industry Reports & Market Research
2. Retailer Buying Guides
3. DIY & How-To Resources
4. Trade Publications
5. Community Forums & UGC
6. Video Content & Tutorials
7. Manufacturer Resources
8. Professional Organizations
9. Consumer Reports & Testing
10. Government & Economic Data

**Data Per Resource:**
- Title
- Provider
- Direct URL
- Access requirements
- Description
- Relevance level
- Last updated

**Quality Standards:**
- Authority: Industry-recognized sources only
- Relevance: Directly applicable
- Recency: <2 years preferred
- Accessibility: Publicly available when possible

---

## Data Quality Standards

### Confidence Levels

**High (±5-10%):**
- Direct revenue data from filings
- Panel data from NPD/Circana
- Cross-validated (3+ sources)

**Medium (±10-20%):**
- Triangulated from proxies
- Industry reports
- Retailer category data

**Low (±15-30%):**
- Single-source estimates
- Regional extrapolations
- Emerging categories

### Validation Requirements

Every data point includes:
1. Source attribution
2. Methodology
3. Confidence level
4. Reasoning

### Quality Principles

✅ Document methodology
✅ Provide confidence levels
✅ Cross-validate critical metrics
✅ Include reasoning
✅ Cover full competitive landscape

❌ Never fabricate data
❌ Never extrapolate beyond bounds
❌ Never cite unverified sources
❌ Never present estimates as facts
❌ Never cherry-pick data

---

## Module Architecture

### **⚠️ IMPORTANT: Dual System During Migration**

This module currently has TWO systems:
1. **Legacy System** (Currently Active) - `core/orchestrator.py` with `collectors/`
2. **Agentic System** (New) - `agents/orchestrator.py` with AI-guided validation

**Migration Status**: Stages 1-2 complete (Validation + Orchestrator), Stages 3-7 in progress.

```
category_intelligence/
│
├── 📄 MODULE_GUIDE.md              ← DEVELOPERS START HERE
├── 📄 README.md                    ← USER DOCUMENTATION (this file)
├── 📄 IMPLEMENTATION_CHECKLIST.md  ← Migration progress tracker
│
├── 🤖 agents/                      ← NEW AGENTIC SYSTEM (100% real data)
│   ├── orchestrator.py                 # AI coordinator (ACCEPT/REJECT/REFINE)
│   ├── validators.py                   # 4 validation agents
│   ├── collectors.py                   # Data collection agents
│   └── base.py                         # Agent framework & message protocol
│
├── 📦 collectors/                  ← LEGACY COLLECTORS (being migrated)
│   ├── brand_discovery.py              # Brand profiling (50+ brands)
│   ├── market_researcher.py            # Market share & sizing
│   ├── pricing_analyzer.py             # Product pricing analysis
│   ├── resource_curator.py             # Learning resources
│   ├── taxonomy_builder.py             # Category structure
│   └── consumer_insights.py            # JTBD analysis
│
├── ⚙️ core/                        ← SHARED INFRASTRUCTURE
│   ├── orchestrator.py                 # Legacy pipeline coordinator
│   ├── config.py                       # Configuration management
│   └── source_tracker.py               # Source validation & audit
│
├── 📊 generators/                  ← REPORT GENERATION
│   └── html_reporter.py                # Professional HTML reports
│
├── 🛠️ utils/                       ← UTILITIES
│   └── data_storage.py                 # Data persistence helpers
│
├── 📤 outputs/                     ← GENERATED REPORTS
│   ├── audit/                          # Source audit trails
│   └── *.html                          # Category intelligence reports
│
└── 🚀 run_analysis.py              ← CLI ENTRY POINT
```

### **Documentation Files**
- **MODULE_GUIDE.md** - Complete technical guide for LLMs/developers
- **AGENTIC_ARCHITECTURE.md** - Agent system design (validation, orchestration)
- **DATA_SOURCE_MAPPING.md** - All verified data sources & APIs
- **SCRAPING_ARCHITECTURE.md** - Web scraping infrastructure (Scrapling)
- **IMPLEMENTATION_CHECKLIST.md** - Migration progress (7 stages)

---

## Offbrain Insight Framework

**🎯 CRITICAL:** Before writing any consumer insights, review the framework:

📄 **[Offbrain Insight Framework](../../docs/CONSUMER_INSIGHTS_FRAMEWORK.md)**

This framework ensures all consumer insights are:
- Based on **observed behavior** (not just stated attitudes)
- Grounded in **context** (who, what, when, where)
- Revealing **subconscious drivers** (the real "why")
- **Specific and actionable** (not generic observations)

### Key Principles
- **95% of decisions** are subconscious - design research accordingly
- **Belief ≠ Behavior** - observe what people do, not just what they say
- **Context drives behavior** - recreate real decision environments
- **Use the 4 W's** to infer the WHY (Who, What, When, Where)

---

## Research Workflow

```
0. REVIEW INSIGHTS FRAMEWORK ⚠️ REQUIRED
   ↓ Read docs/CONSUMER_INSIGHTS_FRAMEWORK.md
   ↓ Apply behavioral science principles

1. BRAND DISCOVERY
   ↓ Identify 50+ brands across all tiers
   ↓ Revenue, market share, distribution, positioning

2. TAXONOMY BUILDING
   ↓ Map 4-8 subcategories with quantitative metrics
   ↓ Market size, units, brands, prices, growth
   ↓ Consumer & industry keywords

3. PRICING ANALYSIS
   ↓ Analyze pricing by subcategory
   ↓ Price ranges, volumes, competitive dynamics

4. MARKET SHARE RESEARCH
   ↓ Validate brand positions with multi-source data
   ↓ Competitive landscape, threats, opportunities

5. MARKET SIZING
   ↓ Quantify market with historical & projections
   ↓ Growth drivers, inhibitors, trends

6. RESOURCE CURATION
   ↓ Compile 30-40 authoritative sources with URLs

7. VALIDATION
   ↓ Cross-check sources and confidence levels

8. HTML REPORT GENERATION ⚠️ APPLY INSIGHTS FRAMEWORK
   ↓ Generate clean, table-based report
   ↓ Ensure consumer insights follow framework principles
```

---

## Expected Deliverables

### Quantitative Outputs
- **Brands profiled:** 50-70
- **Subcategories mapped:** 4-8
- **Product types analyzed:** 20-40
- **Pricing data points:** 100+
- **Market share estimates:** 15-25 brands
- **Growth projections:** 3-4 years
- **Resources curated:** 30-40

### Qualitative Outputs
- Brand positioning & competitive analysis
- Category dynamics & market trends
- Growth drivers & inhibitors
- Competitive threats & opportunities
- Consumer & industry language
- Methodology documentation

### Report Metrics
- **HTML file:** 150-300 KB
- **Audit trail:** Complete source tracking
- **Generation time:** <5 seconds

---

## Quality Assurance Checklist

Before delivering:

### Consumer Insights Quality
- [ ] **Reviewed Consumer Insights Framework** (docs/CONSUMER_INSIGHTS_FRAMEWORK.md)
- [ ] **ZERO FABRICATION:** All insights rooted in actual research signal
- [ ] **NO PLACEHOLDERS:** No made-up quotes, emotions, or behaviors
- [ ] **SOURCE TRACEABLE:** Every insight cites specific signal (transcript/video/data)
- [ ] Insights based on **observed behavior**, not just stated attitudes
- [ ] Each insight includes **context** (who, what, when, where)
- [ ] Insights reveal **subconscious drivers** and emotional motivations (from actual data)
- [ ] Insights are **specific** with behavioral examples (not generic)
- [ ] Avoided asking "why" directly - used 4 W's approach
- [ ] Combined explicit (what they say) + implicit (what they do) understanding

### Research Quality
- [ ] 50+ brands across all tiers
- [ ] Unbiased coverage (small/regional/import brands)
- [ ] Quantitative metrics for all subcategories
- [ ] Product-level pricing with volumes
- [ ] Consumer & industry keywords
- [ ] 15-25 brands with market share
- [ ] 5-year historical growth
- [ ] 3-4 year projections with confidence
- [ ] 7-10 growth drivers, 5-7 inhibitors
- [ ] 30-40 resources with URLs
- [ ] Methodology documented
- [ ] Confidence levels assigned
- [ ] Critical metrics cross-validated

---

## Offbrain Insights Standards

This module adheres to **Zero Fabrication Tolerance**:

> Every data point must be sourced, every estimate must be reasoned, every confidence level must be justified. We deliver authentic consumer intelligence with complete transparency.

**Report Footer:**
> "Offbrain Insights | Authentic Consumer Intelligence | Zero Fabrication Tolerance"

---

## File Locations

```
# Generated reports
modules/category_intelligence/outputs/[output_name]_Category_Intelligence.html

# Audit trails
modules/category_intelligence/outputs/audit/source_audit.json
modules/category_intelligence/outputs/audit/citations.json

# Run analysis
modules/category-intelligence/run_analysis.py
```

---

## Dependencies

```
pydantic>=2.5.0
PyYAML>=6.0
python-dotenv>=1.0.0
```

Install:
```bash
pip install pydantic PyYAML python-dotenv
```

---

## Module Status

**Production Ready** - This module performs institutional-grade research with validated methodologies.

If data cannot be validated, it is marked as low confidence or omitted. **Quality over comprehensiveness.**

---

## License

Internal use only - Offbrain Insights proprietary module

**Created:** 2025-10-15
**Owner:** Offbrain Insights Development Team
