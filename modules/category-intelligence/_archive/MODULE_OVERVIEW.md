# Category Intelligence Module - Folder Overview

**Project:** 3M Garage Organization Market Analysis
**Module:** category-intelligence
**Total Size:** ~4.1GB of data + 1.5MB analysis/outputs
**Last Updated:** October 30, 2025

---

## 📁 Directory Structure

```
category-intelligence/
├── 📊 data/              (4.1 GB) - Raw and processed market data
├── 📈 analysis/          (1.2 MB) - Statistical analysis and validation
├── 📄 outputs/           (364 KB) - Analysis reports and insights
├── 🔧 src/               Python source code (pipeline, analysis, reporting)
├── 📚 docs/              Documentation and archived reports
├── 🧪 tests/             Unit tests and coverage reports
├── 📜 scripts/           Standalone analysis scripts
├── 🏛️ archive/           Legacy code and deprecated versions
└── 📋 logs/              Runtime logs
```

---

## 📊 /data/ (4.1 GB) - Market Data Repository

### Primary Product Datasets

**Combined/Final Datasets:**
- `garage_organizers_final_b_plus.json` (12.3 MB) - Final curated dataset with B+ products
- `garage_organizers_final_with_workbenches.json` (11.6 MB) - Includes workbench expansion
- `garage_organizers_final.json` (10.6 MB) - Core final dataset
- `garage_organizers_complete.json` (11.5 MB) - Complete collection before filtering
- `garage_organizers_combined.json` (9.8 MB) - Initial combined dataset

**Retailer-Specific Raw Data:**
- `amazon_garage_organizers_mined.json` (444 KB)
- `homedepot_garage_organizers_mined.json` (627 KB)
- `walmart_garage_organizers_mined.json` (via retailers/ subfolder)

**Keywords & Search Data:**
- `amazon_keywords.json` (6.4 MB) - Amazon search keyword data
- `homedepot_keyword.json` (11.2 MB) - Home Depot search data

**Consumer Insights:**
- `reddit_pullpush_sample.json` (624 KB) - Reddit discussions
- `reddit_sample.json` (114 KB) - Reddit sample data
- `google_trends_emerging_products.json` (31 KB) - Emerging trends

**Other Marketplaces:**
- `etsy_listings.json` (90 KB) - Etsy handmade/artisan products
- `target_products.json` (340 KB) - Target retail data

**Tracking Databases:**
- `bsr_tracking.db` (180 KB) - Best Seller Rank tracking
- `amazon_graph_test.db` (37 KB) - Amazon product graph

### /data/retailers/ (Processed Retail Data)

**Individual Retailer Files:**
- `amazon_products.json` - Amazon product catalog
- `homedepot_products.json` - Home Depot catalog
- `walmart_products.json` - Walmart catalog
- `lowes_products.json` - Lowe's catalog
- `target_products.json` - Target catalog
- `etsy_products.json` - Etsy catalog

**Combined/Enhanced:**
- `all_products_final_with_lowes.json` - Final combined dataset (all 5+ retailers)
- `all_products_enhanced_final.json` - Enhanced with AI extraction
- `all_products_enhanced_with_images.json` - Includes product images
- `all_products_with_images.json` - Image-enhanced version

**Manual Parsing:**
- `manual_grok_parsed/` - Manually parsed retailer data
  - `ace-garage-organizers.md`
  - `homedepot-garage-organizer.md`
  - `menards-garage-organizers.md`

### /data/youtube_* (Video Content Analysis)

**YouTube Video Data:**
- `youtube_videos/` - Downloaded YouTube videos
- `youtube_audio/` - Extracted audio files
- `youtube_transcripts/` - Video transcripts

**TikTok Video Data:**
- `tiktok_videos/` - TikTok videos
- `tiktok_audio/` - Audio files
- `tiktok_transcripts/` - Transcripts

**Teardown Video Data:**
- `teardown_videos/` - Product teardown/review videos
- `teardown_audio/` - Extracted audio
- `teardown_transcripts/` - Transcripts

---

## 📈 /analysis/ (1.2 MB) - Statistical Analysis

**Walmart Data Validation:**
- `walmart_cleaned_rightsized.xlsx` - Cleaned Walmart dataset
- `walmart_removed_products.xlsx` - Out-of-scope products removed
- `walmart_out_of_scope_products.xlsx` - Products excluded from analysis
- `walmart_rightsizing_summary.json` - Summary of data cleaning

**Distribution Bias Analysis:**
- `distribution_bias_analysis.xlsx` - Statistical bias analysis
- `DISTRIBUTION_BIAS_SUMMARY.txt` - Text summary

**Product Statistics:**
- `product_statistics_detailed.xlsx` - Detailed product stats
- `product_statistics_summary.json` - JSON summary
- `validation_and_walmart_analysis_summary.json` - Validation report

---

## 📄 /outputs/ (364 KB) - Analysis Reports & Insights

### Video Analysis Reports

**Teardown Analysis:**
- `FINAL_TEARDOWN_REPORT.md` - Complete teardown video analysis report
- `all_teardown_reports.json` - All teardown reports aggregated
- `teardown_videos_search_results.json` - Search results
- `additional_teardown_videos.json` - Supplemental videos
- `curated_teardown_videos.json` - Curated selection
- `top20_bestsellers_for_teardown.json` - Top 20 products for teardown
- `teardown_reports/` - Individual teardown reports

**Consumer Video Insights:**
- `full_garage_organizer_videos.json` - Complete video dataset (571+ videos analyzed)
- `garage_keyword_language.json` - Consumer language patterns

### Market Analysis Reports

**Keyword & Language Analysis:**
- `comprehensive_keyword_analysis_full.json` - Complete keyword analysis
- `expert_keyword_strategic_report.json` - Strategic keyword recommendations

**Market Trends:**
- `emerging_trend_gap_analysis.json` - Gap analysis and emerging trends
- `benefit_taxonomy_analysis.json` - Product benefit categorization

**BSR (Best Seller Rank) Analysis:**
- `bsr_complete_analysis.json` - Complete BSR tracking analysis
- `bsr_estimates_remaining.json` - Remaining estimates

---

## 🔧 /src/ - Python Source Code

### Source Code Structure:
```
src/
├── pipeline/     - Data collection and processing pipelines
├── analysis/     - Analysis engines and algorithms
├── reporting/    - Report generation modules
└── storage/      - Data storage and database management
```

---

## 📚 /docs/ - Documentation

### Documentation Files:
```
docs/
├── archive/      - Archived documentation
└── reports/      - Generated reports
```

---

## 📋 Root-Level Documents (Analysis Reports)

### Executive Reports (Client-Ready)

**01_EXECUTIVE_BRIEFING.md** (9.3 KB)
- Executive summary and market opportunity
- Quality gap analysis
- Consumer insights and behavioral patterns
- Market entry strategy and financial projections

**02_CATEGORY_INTELLIGENCE_DEEP_DIVE.md** (16 KB)
- Market structure and segmentation analysis
- Competitive intelligence assessment
- Brand landscape mapping
- Price architecture analysis

**03_PRODUCT_DEVELOPMENT_ROADMAP.md** (18 KB)
- Product specifications for VHB™ Heavy-Duty Hook System
- Technical innovation elements
- Development timeline and milestones
- Bill of materials and cost structure

### Excel Data Deliverables

**Primary Dataset:**
- `04_CATEGORY_DATA_ALL_PRODUCTS.xlsx` (1.4 MB) - Complete product database

**Variations:**
- `04_CATEGORY_DATA_ALL_PRODUCTS_WEIGHTED.xlsx` (1.4 MB) - Weighted version
- `04_CATEGORY_DATA_RIGHTSIZED_WITH_SUBCATS_FIXED.xlsx` (634 KB) - Cleaned with subcategories
- `04_CATEGORY_DATA_COMPLETE.xlsx` (231 KB) - Complete version
- `04_CATEGORY_DATA_FINAL.xlsx` (233 KB) - Final version

### Methodology & Validation Documentation

**Data Quality:**
- `DATA_METHODOLOGY_AND_CORRECTIONS.md` (13 KB) - Data collection methodology
- `STATISTICAL_ANALYSIS_SUMMARY.md` (18 KB) - Statistical validation
- `BIAS_CORRECTION_GUIDE.md` (28 KB) - Bias correction procedures
- `ROOT_CAUSE_AND_TOP_FIXES.md` (14 KB) - Root cause analysis

**Validation Reports:**
- `MANUAL_SCRAPE_VALIDATION_SUMMARY.md` (12 KB) - Manual scraping validation
- `WALMART_RIGHTSIZING_REPORT.md` (10 KB) - Walmart data cleaning report

**Project Status:**
- `FINAL_DELIVERABLE_STATUS.md` (6 KB) - Final deliverable status
- `STATUS_DATA_COLLECTION.md` (2 KB) - Data collection status
- `README.md` (4 KB) - Module overview

---

## 🧪 /tests/ - Unit Tests

**Test Coverage:**
- Unit tests for all source modules
- Coverage reports in `tests/coverage_html/`

---

## 📜 /scripts/ - Standalone Analysis Scripts

**Analysis Scripts:**
- Data collection scripts
- Analysis automation
- Report generation
- One-off data processing tasks

---

## 🏛️ /archive/ - Legacy Code

**Archived Components:**
```
archive/
└── legacy/       - Deprecated code and old versions
```

---

## 🔑 Key Data Sources Summary

### Retail Channels (5 major retailers)
1. **Amazon** - 501 products
2. **Walmart** - 7,499 products
3. **Home Depot** - 940 products
4. **Lowe's** - 371 products
5. **Target** - 244 products

**Total Products:** 9,555 unique SKUs

### Consumer Research Sources
1. **YouTube Videos** - 571+ videos analyzed
2. **TikTok Content** - Consumer behavior patterns
3. **Reddit Discussions** - Consumer conversations
4. **Product Reviews** - 2,847 negative reviews analyzed
5. **Teardown Videos** - Product failure analysis

### Market Intelligence
- **Best Seller Rank Tracking** - Real-time market position
- **Keyword Analysis** - Consumer search patterns
- **Google Trends** - Emerging product categories
- **Benefit Taxonomy** - Consumer job-to-be-done mapping

---

## 📊 Data Lineage & Processing Flow

```
1. RAW DATA COLLECTION
   ├── Retailer scraping → data/retailers/*.json
   ├── Video collection → data/*_videos/
   └── Consumer insights → data/reddit*, data/google_trends*

2. DATA CLEANING & ENHANCEMENT
   ├── Combined datasets → data/garage_organizers_*.json
   ├── AI extraction → data/retailers/all_products_enhanced*.json
   └── Image enrichment → data/retailers/all_products_with_images.json

3. VALIDATION & ANALYSIS
   ├── Statistical validation → analysis/*.xlsx
   ├── Bias correction → analysis/distribution_bias*
   └── Walmart cleaning → analysis/walmart_*

4. INSIGHTS GENERATION
   ├── Keyword analysis → outputs/keyword_analysis*.json
   ├── Video analysis → outputs/teardown*, outputs/full_garage_organizer_videos.json
   └── Market trends → outputs/emerging_trend_gap_analysis.json

5. CLIENT DELIVERABLES
   ├── Executive reports → 01_*, 02_*, 03_*.md
   ├── Excel database → 04_CATEGORY_DATA*.xlsx
   └── Methodology docs → *_SUMMARY.md, *_GUIDE.md
```

---

## 🎯 Quick Access Guide

### For Market Overview:
→ Start with `01_EXECUTIVE_BRIEFING.md`

### For Product Data:
→ Use `04_CATEGORY_DATA_ALL_PRODUCTS.xlsx` (Excel)
→ Or `data/retailers/all_products_final_with_lowes.json` (JSON)

### For Consumer Insights:
→ Check `outputs/full_garage_organizer_videos.json` (571+ videos)
→ Read `outputs/FINAL_TEARDOWN_REPORT.md`

### For Competitive Analysis:
→ Review `02_CATEGORY_INTELLIGENCE_DEEP_DIVE.md`

### For Product Development:
→ See `03_PRODUCT_DEVELOPMENT_ROADMAP.md`

### For Data Quality/Methodology:
→ Read `DATA_METHODOLOGY_AND_CORRECTIONS.md`
→ Check `STATISTICAL_ANALYSIS_SUMMARY.md`

---

## 📈 Data Statistics

- **Total Products Analyzed:** 9,555 SKUs
- **Retailers Covered:** 5 major channels
- **Consumer Videos:** 571+ analyzed
- **Total Video Views:** 47.9M
- **Review Analysis:** 2,847 negative reviews
- **Price Range:** $5 - $500+
- **Data Collection Period:** October 2025
- **Total Dataset Size:** ~4.1 GB

---

## 🚀 Module Purpose

This module provides comprehensive category intelligence for the garage organization market, enabling 3M to:

1. **Identify Market Opportunities** - Quality gaps, premium segment white space
2. **Understand Consumer Needs** - Jobs-to-be-done, pain points, unmet needs
3. **Assess Competitive Landscape** - Brand positioning, market share, feature gaps
4. **Guide Product Development** - Specifications based on market failures
5. **Validate Business Case** - Revenue potential, ROI projections, risk assessment

---

**Generated:** November 3, 2025
**Module Owner:** offbrain Category Intelligence Team
**Project:** 3M Garage Organization Market Analysis
