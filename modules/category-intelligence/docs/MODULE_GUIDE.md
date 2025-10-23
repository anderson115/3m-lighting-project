# Category Intelligence Module - Complete Guide

**Version**: 2.0 (Agentic System)
**Status**: Production + Migration
**Last Updated**: 2025-10-16
**Zero Fabrication Policy**: ENFORCED

---

## 📋 **TABLE OF CONTENTS**

1. [Module Overview](#module-overview)
2. [Architecture (Dual System)](#architecture-dual-system)
3. [File Structure](#file-structure)
4. [Quick Start](#quick-start)
5. [Component Reference](#component-reference)
6. [Data Sources & APIs](#data-sources--apis)
7. [Coding Standards](#coding-standards)
8. [Development Workflow](#development-workflow)
9. [Testing & Validation](#testing--validation)
10. [Troubleshooting](#troubleshooting)

---

## 📖 **MODULE OVERVIEW**

The Category Intelligence Module generates comprehensive market research reports for product categories with **ZERO fabrication tolerance**. Every data point must be traceable to a real source.

### **Core Capabilities**
- ✅ Market sizing & growth analysis (real data from FRED API, WebSearch)
- ✅ Brand discovery & competitive landscape (50+ brands per category)
- ✅ Product pricing analysis (scraping from 4+ retailers)
- ✅ Learning resource curation (30+ curated sources)
- ✅ Consumer insights (JTBD framework with video evidence)
- ✅ Source tracking & audit trail (100% traceability)
- ✅ Professional HTML report generation (consulting-grade formatting)

### **Target Use Case**
- **Users**: Product managers, strategy consultants, market researchers
- **Input**: Category name (e.g., "garage storage", "smart home lighting")
- **Output**: Comprehensive HTML report with citations + audit trail JSON

---

## 🏗️ **ARCHITECTURE (DUAL SYSTEM)**

### **IMPORTANT: Two Parallel Systems**

This module currently has TWO orchestration systems running in parallel during migration:

#### **System 1: Legacy Pipeline** (CURRENTLY ACTIVE)
- **Entry Point**: `run_analysis.py` → `core/orchestrator.py`
- **Collectors**: `collectors/` (brand_discovery.py, market_researcher.py, etc.)
- **Data**: Mix of real + hardcoded data (being migrated)
- **Status**: ✅ Working, ⚠️ Contains hardcoded data, 🔄 Being replaced

#### **System 2: Agentic System** (NEW - IN DEVELOPMENT)
- **Entry Point**: `agents/orchestrator.py` (OrchestratorAgent)
- **Agents**: `agents/` (validators, collectors, base classes)
- **Data**: 100% real data (WebSearch, APIs, scraping)
- **Status**: ✅ Core complete, ⏳ Integration in progress

### **Migration Path**
```
Phase 1: ✅ COMPLETE - Validation layer + Orchestrator agent built
Phase 2: ⏳ IN PROGRESS - Integrate collectors with validation
Phase 3: ⏳ PENDING - Replace legacy collectors with agent-based
Phase 4: ⏳ PENDING - Update run_analysis.py to use agentic system
Phase 5: ⏳ PENDING - Deprecate legacy system
```

---

## 📁 **FILE STRUCTURE**

```
modules/category_intelligence/
│
├── 📄 MODULE_GUIDE.md          ← YOU ARE HERE (LLM entry point)
├── 📄 README.md                ← User-facing documentation
├── 📄 IMPLEMENTATION_CHECKLIST.md ← Development progress tracker
│
├── 📚 ARCHITECTURE DOCS
│   ├── AGENTIC_ARCHITECTURE.md ← Agent system design (NEW)
│   ├── DATA_SOURCE_MAPPING.md  ← All data sources & acquisition methods
│   ├── SCRAPING_ARCHITECTURE.md ← Web scraping infrastructure
│   ├── DATA_STORAGE.md         ← Data persistence strategy
│   └── PRD.md                  ← Product requirements (historical)
│
├── 🤖 agents/                  ← NEW AGENTIC SYSTEM
│   ├── __init__.py
│   ├── base.py                 ← Agent base classes, message protocol (307 lines)
│   ├── orchestrator.py         ← Master coordinator, ACCEPT/REJECT/REFINE (472 lines)
│   ├── validators.py           ← 4 validation agents (700 lines)
│   └── collectors.py           ← Data collection agents (312 lines)
│
├── 📦 collectors/              ← LEGACY COLLECTORS (being migrated)
│   ├── __init__.py
│   ├── brand_discovery.py      ← Discovers 50+ brands (819 lines) ⚠️ LARGE
│   ├── market_researcher.py    ← Market size & growth (836 lines) ⚠️ LARGE
│   ├── pricing_analyzer.py     ← Product pricing (703 lines) ⚠️ LARGE
│   ├── resource_curator.py     ← Learning resources (509 lines)
│   ├── taxonomy_builder.py     ← Product categorization (437 lines)
│   └── consumer_insights.py    ← JTBD analysis (567 lines)
│
├── ⚙️ core/                    ← SHARED INFRASTRUCTURE
│   ├── __init__.py
│   ├── config.py               ← Configuration management (110 lines)
│   ├── source_tracker.py       ← Source validation & audit (166 lines)
│   └── orchestrator.py         ← Legacy orchestrator (253 lines) ⚠️ OLD SYSTEM
│
├── 📊 generators/              ← REPORT GENERATION
│   ├── __init__.py
│   └── html_reporter.py        ← Professional HTML reports (804 lines) ⚠️ LARGE
│
├── 🛠️ utils/                   ← UTILITIES
│   ├── __init__.py
│   └── data_storage.py         ← Data persistence helpers (271 lines)
│
├── 📤 outputs/                 ← GENERATED REPORTS
│   ├── audit/
│   │   ├── source_audit.json   ← All sources with validation
│   │   └── citations.json      ← Citation list
│   ├── garage_storage_final_Category_Intelligence.html
│   └── garage_storage_consulting_Category_Intelligence.html
│
└── 🚀 run_analysis.py          ← CLI entry point (95 lines)
```

### **⚠️ Files Marked LARGE (>700 lines)**
These files contain extensive data and may need refactoring:
- `collectors/market_researcher.py` (836 lines) - Contains hardcoded market data
- `collectors/brand_discovery.py` (819 lines) - Contains hardcoded brand lists
- `html_reporter.py` (804 lines) - Acceptable for complex report generation
- `pricing_analyzer.py` (703 lines) - Contains hardcoded pricing data
- `validators.py` (700 lines) - 4 validators, could split but OK

---

## 🚀 **QUICK START**

### **Prerequisites**
```bash
# Python 3.13+
python --version

# Install dependencies
pip install pydantic requests  # Core dependencies
pip install "scrapling[fetchers]"  # For web scraping (optional)

# Set environment variables (optional)
export FRED_API_KEY="your_fred_api_key"  # For economic data
```

### **Run Analysis (Current System)**
```bash
cd /Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/category_intelligence

# Run analysis
python run_analysis.py --category "garage storage"

# With custom output name
python run_analysis.py --category "smart home lighting" --output "lighting_report"
```

### **Output Files**
```
outputs/
├── {category}_Category_Intelligence.html  # Main report
└── audit/
    ├── source_audit.json                  # All sources
    └── citations.json                     # Citation list
```

---

## 🧩 **COMPONENT REFERENCE**

### **LEGACY COLLECTORS** (collectors/)

#### **BrandDiscovery** (`brand_discovery.py`)
```python
from modules.category_intelligence.collectors.brand_discovery import BrandDiscovery

brand_discovery = BrandDiscovery(config)
brands = brand_discovery.discover_brands("garage storage")

# Returns:
# {
#     "status": "completed",
#     "brands": [
#         {"name": "Rubbermaid", "tier": "tier_1_national", ...},
#         ...
#     ],
#     "total_brands": 50+
# }
```
**Current Status**: ⚠️ Contains hardcoded brand data. Migration to real WebSearch pending.

#### **MarketResearcher** (`market_researcher.py`)
```python
from modules.category_intelligence.collectors.market_researcher import MarketResearcher

researcher = MarketResearcher(config)
market_size = researcher.analyze_market_size("garage storage")
market_share = researcher.research_market_share("garage storage")

# Returns market size, growth, projections, competitive landscape
```
**Current Status**: ⚠️ Contains hardcoded market data. Migration to FRED API + WebSearch pending.

#### **PricingAnalyzer** (`pricing_analyzer.py`)
```python
from modules.category_intelligence.collectors.pricing_analyzer import PricingAnalyzer

pricing = PricingAnalyzer(config)
pricing_data = pricing.analyze_pricing("garage storage")

# Returns pricing ranges, products, retailers, top brands
```
**Current Status**: ⚠️ Contains hardcoded pricing. Migration to Scrapling web scraping pending.

#### **ConsumerInsightsCollector** (`consumer_insights.py`)
```python
from modules.category_intelligence.collectors.consumer_insights import ConsumerInsightsCollector

insights = ConsumerInsightsCollector(config)
jtbd_analysis = insights.analyze_jobs_to_be_done(video_data)

# Returns JTBD framework with evidence from consumer videos
```
**Current Status**: ✅ Production-ready for video-based JTBD analysis.

---

### **NEW AGENTIC SYSTEM** (agents/)

#### **OrchestratorAgent** (`orchestrator.py`)
```python
from modules.category_intelligence.agents.orchestrator import OrchestratorAgent

# Initialize with requirements
requirements = {
    "brands": {"min_count": 50},
    "market_size": {"required": True},
    "pricing": {"min_products": 120, "min_retailers": 4}
}

orchestrator = OrchestratorAgent(category="garage storage", requirements=requirements)

# Assign task to collector
await orchestrator.assign_task(market_agent, "market_size", parameters={})

# Receive and validate submission
decision = await orchestrator.receive_submission(submission)
# Returns: OrchestratorDecision (ACCEPT, REJECT, or REFINE)

# Get progress
report = orchestrator.get_progress_report()
# Returns: completeness %, gaps, quality distribution
```

#### **Validation Agents** (`validators.py`)

**QualityValidationAgent**: Checks data completeness, format, consistency, recency
```python
from modules.category_intelligence.agents.validators import QualityValidationAgent

validator = QualityValidationAgent("quality_validator")
result = await validator.validate(submission)
# Returns: ValidationResult (passed=True/False, score 0.0-1.0, issues, recommendations)
```

**SourceValidationAgent**: ZERO FABRICATION ENFORCEMENT
```python
from modules.category_intelligence.agents.validators import SourceValidationAgent

validator = SourceValidationAgent("source_validator")
result = await validator.validate(submission)
# Rejects if: No sources, placeholder URLs, fabrication markers detected
# Returns: score=1.0 required to pass
```

**RelevanceValidationAgent**: Category relevance check
```python
from modules.category_intelligence.agents.validators import RelevanceValidationAgent

validator = RelevanceValidationAgent("relevance_validator", category="garage storage")
result = await validator.validate(submission)
# Checks: keyword matching, brand relevance, product relevance
```

**GapIdentificationAgent**: Identifies missing data
```python
from modules.category_intelligence.agents.validators import GapIdentificationAgent

analyzer = GapIdentificationAgent("gap_analyzer")
gaps = await analyzer.analyze_gaps(collected_data, requirements)
# Returns: List[Gap] with priority, suggested actions
```

---

## 🔗 **DATA SOURCES & APIs**

See `DATA_SOURCE_MAPPING.md` for comprehensive list. Key sources:

### **Working Data Sources**
1. **WebSearch (Claude API)** - Market intelligence, brand discovery
2. **FRED API** - Retail sales time series (`RSFSN`, `RSBMGESD`)
3. **Census Bureau API** - Retail trade data
4. **CORGIS Datasets** - Retail services data (downloaded)
5. **Web Scraping (Scrapling)** - Product pricing from retailers

### **API Keys Required**
```bash
# Optional - for enhanced data collection
export FRED_API_KEY="your_key_here"  # Get from https://fred.stlouisfed.org/
```

### **Web Scraping Infrastructure**
- **Tool**: Scrapling 0.3.7 + Camoufox browser
- **Success Rate**: 92-95% against anti-bot systems
- **Retailers**: Home Depot, Lowe's, Amazon, Walmart
- **Architecture**: See `SCRAPING_ARCHITECTURE.md`

---

## 💻 **CODING STANDARDS**

### **Zero Fabrication Policy**
```python
# ❌ NEVER DO THIS
data = {
    "market_size": "$3.5B",
    "source": "example.com/placeholder"
}

# ✅ ALWAYS DO THIS
from agents.base import Source

data = {
    "market_size": "$3.5B",
    "sources": [
        Source(
            url="https://www.grandviewresearch.com/industry-analysis/garage-storage-market",
            publisher="Grand View Research",
            date_published="2024-09-15",
            excerpt="The US garage storage market was valued at $3.5 billion in 2024...",
            confidence="high"
        )
    ]
}
```

### **Data Submission Format**
```python
from agents.base import DataSubmission, Source

submission = DataSubmission(
    sender_agent="market_data_agent",
    recipient_agent="orchestrator",
    data_type="market_size",
    data={"market_size_usd": 3.5e9, "year": 2024},
    sources=[Source(...)],  # REQUIRED
    confidence=0.85,
    quality_self_assessment=0.9,
    reasoning="Collected from Grand View Research report"
)

# Validate no fabrication
issues = submission.validate_no_fabrication()
if issues:
    raise ValueError(f"Fabrication detected: {issues}")
```

### **File Size Guidelines**
- **Small**: < 300 lines (single responsibility)
- **Medium**: 300-500 lines (acceptable)
- **Large**: 500-800 lines (consider refactoring)
- **Too Large**: > 800 lines (MUST refactor unless justified)

### **Naming Conventions**
- **Classes**: `PascalCase` (e.g., `MarketDataAgent`)
- **Functions**: `snake_case` (e.g., `collect_data`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`)
- **Private methods**: `_leading_underscore` (e.g., `_validate_sources`)

### **Documentation Requirements**
```python
def collect_data(self, category: str, **kwargs) -> Dict[str, Any]:
    """
    Collect market data for category using WebSearch.

    Args:
        category: Category name (e.g., "garage storage")
        **kwargs: Additional parameters

    Returns:
        Dict with structure:
        {
            "data": {...},
            "sources": [Source(...)],
            "confidence": 0.0-1.0,
            "quality_score": 0.0-1.0,
            "reasoning": str
        }

    Raises:
        ValueError: If no sources found or fabrication detected
    """
```

---

## 🔄 **DEVELOPMENT WORKFLOW**

### **Adding a New Collector**
1. Create agent class inheriting from `CollectionAgent`
2. Implement `collect_data()` with real data sources
3. Add source tracking for every data point
4. Test with orchestrator validation
5. Update `IMPLEMENTATION_CHECKLIST.md`

### **Adding a New Validator**
1. Create agent class inheriting from `ValidationAgent`
2. Implement `validate()` method
3. Return `ValidationResult` with score, issues, recommendations
4. Add to `OrchestratorAgent` validation flow
5. Test with sample data

### **Migration Checklist for Legacy Collectors**
```markdown
- [ ] Identify all hardcoded data in collector
- [ ] Map to real data sources (see DATA_SOURCE_MAPPING.md)
- [ ] Implement WebSearch/API integration
- [ ] Add Source tracking for every data point
- [ ] Wrap in DataSubmission format
- [ ] Remove ALL hardcoded data
- [ ] Test with SourceValidator (must pass)
- [ ] Verify zero fabrication confirmed
```

---

## 🧪 **TESTING & VALIDATION**

### **Source Validation Test**
```python
# Test that all data has sources
from agents.validators import SourceValidationAgent

validator = SourceValidationAgent("test")
result = await validator.validate(submission)

assert result.passed == True, f"Source validation failed: {result.issues}"
assert result.score == 1.0, "Source validation requires perfect score"
```

### **Quality Metrics**
Target metrics for production reports:
- ✅ **Completeness**: >= 95%
- ✅ **Average Quality Score**: >= 0.90
- ✅ **Source Traceability**: 100%
- ✅ **Data Recency**: All from 2023-2025
- ✅ **Brand Count**: >= 50
- ✅ **Pricing Products**: >= 120 (4 retailers × 30)
- ✅ **Resources**: >= 30

### **Running Validation**
```python
# Check source audit
import json
with open("outputs/audit/source_audit.json") as f:
    audit = json.load(f)

print(f"Total sources: {audit['total_sources']}")
print(f"High confidence: {audit['by_confidence']['high']}")
print(f"Fabrication markers: {audit['fabrication_check']['markers_found']}")

# Should be 0 fabrication markers
assert audit['fabrication_check']['markers_found'] == 0
```

---

## 🐛 **TROUBLESHOOTING**

### **Common Issues**

#### **Source Validation Failing**
```
Error: "CRITICAL: No sources provided"
Solution: Every data point MUST have Source object with URL
```

#### **Fabrication Marker Detected**
```
Error: "Fabrication marker detected: 'placeholder'"
Solution: Remove all placeholder text, example.com URLs, TODO markers
```

#### **Quality Score Too Low**
```
Error: "Validation score 0.65 < 0.7 threshold"
Solution:
  1. Check data completeness (all required fields present?)
  2. Verify data recency (2023-2025 preferred)
  3. Add more high-confidence sources
```

#### **Legacy System Not Working**
```
Error: "ModuleNotFoundError: No module named 'modules.category_intelligence'"
Solution: Run from correct directory or add to PYTHONPATH
```

---

## 📚 **RELATED DOCUMENTATION**

- **AGENTIC_ARCHITECTURE.md** - Complete agent system design
- **DATA_SOURCE_MAPPING.md** - All verified data sources
- **SCRAPING_ARCHITECTURE.md** - Web scraping infrastructure
- **IMPLEMENTATION_CHECKLIST.md** - Development progress (Stages 1-7)
- **README.md** - User-facing documentation

---

## 📊 **CURRENT STATUS**

| Component | Status | Lines | Notes |
|-----------|--------|-------|-------|
| Validation Layer | ✅ Complete | 700 | All 4 validators working |
| Orchestrator Agent | ✅ Complete | 472 | ACCEPT/REJECT/REFINE logic |
| Collection Agents | ⏳ Partial | 312 | Structure ready, integration pending |
| Legacy Collectors | ⚠️ Working | 3,200+ | Contains hardcoded data |
| Report Generator | ✅ Complete | 804 | Professional formatting |
| Documentation | ✅ Complete | - | LLM-optimized |

**Overall Progress**: 29% (Stages 1-2 of 7 complete)

---

## 🎯 **NEXT STEPS FOR LLMS**

If you're an LLM working on this module:

1. **Read this file first** - It's the single source of truth
2. **Check IMPLEMENTATION_CHECKLIST.md** - See what's done/pending
3. **Review AGENTIC_ARCHITECTURE.md** - Understand the new system
4. **Reference DATA_SOURCE_MAPPING.md** - For data collection methods
5. **Follow coding standards** - Zero fabrication, source tracking
6. **Update IMPLEMENTATION_CHECKLIST.md** - After completing work
7. **Test with validators** - Ensure quality before committing

---

**Last Updated**: 2025-10-16
**Maintained By**: Development Team
**License**: Proprietary
