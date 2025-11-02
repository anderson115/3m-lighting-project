# 3M Garage Organization Market Intelligence - Execution Plan
**Status:** Ready for final approval
**Timeline:** 4 weeks
**Next:** Data collection upon approval

---

## 🎯 CORE PRINCIPLE: Strategic Brevity

**Main Deck:** "Sorry I didn't have time to write a shorter letter"
- Every word earns its place
- One insight per slide
- Maximum clarity, minimum text
- Strategic altitude, not tactical detail

**Appendix:** Comprehensive defense
- All data, all methods, all evidence
- Complete audit trail
- Defend every claim

---

## 📊 DELIVERABLES

### Google Slides
**Main Deck:** 18-22 slides (strategically concise)
**Appendix:** 30-40 slides (comprehensively defensive)

### Google Sheets: "3M Market Intelligence Data"
1. Market Structure
2. Jobs-to-be-Done
3. Pain Points (90% coverage)
4. Brand Perceptions (Command/Scotch/Claw)
5. Product Performance
6. Topic Analysis
7. Sentiment Summary
8. Source Index (audit trail)
9. Opportunity Matrix
10. **Product Catalog** (NEW)
    - All scraped products
    - Columns: Sub-category | Brand | Product | Price | Review Score | Retailer | Product URL
    - Merged clean table from all sources

---

## 🔄 EXECUTION PHASES

### PHASE 0: Data Collection
**Duration:** 5 days
**Output:** 3,800 records across 3 brands

**Tasks:**
- [ ] Amazon: Scotch products (400-500 reviews)
- [ ] Amazon: 3M Claw products (300-400 reviews)
- [ ] YouTube/Reddit: Targeted garage searches (+200 posts)
- [ ] Consolidate + validate
- [ ] Create product catalog table

**CHECKPOINT 1:** Data collection complete - validate counts

---

### PHASE 1: Analysis
**Duration:** 10 days
**Output:** All data analyzed via GPT-4

**Week 1 Tasks:**
- [ ] GPT-4 batch: Sentiment (all 3,800 records)
- [ ] GPT-4 batch: Topics (12-15 topics)
- [ ] GPT-4 batch: Entities & brand mentions
- [ ] Market structure analysis
- [ ] Jobs-to-be-done extraction
- [ ] Pain points (90% comprehensive)

**Week 2 Tasks:**
- [ ] Brand perception synthesis (Command/Scotch/Claw)
- [ ] Competitive positioning
- [ ] Strategic intersection analysis
- [ ] Top 3 opportunities + Top 3 issues

**CHECKPOINT 2:** Analysis complete - synthesis review
- Share findings summary for feedback
- Validate strategic direction
- Adjust before deck creation

---

### PHASE 2: Deck Design
**Duration:** 10 days
**Output:** Polished consulting-grade deck

**Week 3 Tasks:**
- [ ] Setup Python-PPTX with reference deck styling
- [ ] Create 3 SAMPLE SLIDES (different types)
  - Title/section slide
  - Data visualization slide
  - Framework/concept slide
- [ ] **Document design system:**
  - Color palette (exact hex codes)
  - Fonts (names, sizes, weights)
  - Layout templates (margins, spacing)
  - Chart styling (colors, labels, legends)
  - Icon library
  - Reusable code modules

**CHECKPOINT 3:** Design system validated
- Share 3 sample slides
- Get approval on visual style
- Confirm repeatability of design process
- Must be able to apply to ALL remaining slides

**Week 3 continued:**
- [ ] Build main deck (18-22 slides)
- [ ] Build appendix (30-40 slides)
- [ ] Populate Google Sheets (all 10 tabs)
- [ ] Visual QA vs reference deck

**Week 4 Tasks:**
- [ ] Feedback incorporation
- [ ] Final polish
- [ ] Export all deliverables

---

## 🛠️ TECHNICAL STACK

**Data Collection:**
- Playwright + Chrome CDP (Amazon)
- yt-dlp (YouTube)
- Existing scraping protocols

**Analysis:**
- GPT-4 Turbo (primary engine)
- Python/pandas (data processing)
- PostgreSQL (data warehouse)

**Visualization:**
- Python-PPTX (slide generation)
- matplotlib/seaborn (charts)
- Export to Google Slides

---

## 📋 MAIN DECK STRUCTURE (18-22 slides)

**Strategic brevity applied to every slide**

### Section 1: Executive Summary (3)
1. Strategic thesis
2. Top 3 opportunities
3. Top 3 critical issues

### Section 2: Market Structure (5-6)
4. Category landscape
5. Brand ecosystem
6. Product segmentation
7. Sub-category distribution
8. Established vs emerging dynamics

### Section 3: Consumer Intelligence (5-6)
9. Jobs-to-be-done framework
10. Context & use cases
11. Pain points landscape
12. Unmet needs
13. Garage organizing mindset

### Section 4: Brand Perception (5-6)
14. Command brand truth
15. Scotch brand truth
16. 3M Claw brand truth
17. 3M parent brand halo
18. Competitive perception map

### Section 5: Strategic Synthesis (3)
19. Strategic intersection (3-circle Venn)
20. Opportunity prioritization
21. Critical issues navigation
22. Strategic implications for discussion

---

## 📎 APPENDIX STRUCTURE (30-40 slides)

**Comprehensive defense of all claims**

### A. Data & Methodology (5-6)
- Collection approach
- Dataset composition (3,800 breakdown)
- GPT-4 methodology
- Quality validation
- Limitations

### B. Detailed Analysis (15-20)
- Complete sentiment tables
- Full topic results
- Comprehensive pain points (90%)
- Complete jobs taxonomy
- All product scorecards
- Detailed use case mapping
- Brand frequencies
- Co-occurrence matrices

### C. Supporting Evidence (8-10)
- Representative verbatims
- Sentiment distributions
- Topic visualizations
- Rating charts
- Cross-platform comparisons

### D. Source Audit Trail (5-8)
- Amazon reviews index (product IDs, dates)
- Reddit posts index (URLs, timestamps)
- YouTube index (video IDs, metadata)
- Product catalog (all scraped products)
- Data lineage

---

## ✅ QUALITY GATES

**After Phase 0:**
- ✅ 3,800 records collected
- ✅ No duplicates
- ✅ Product catalog complete
- ✅ Quality validated

**After Phase 1:**
- ✅ Analysis complete for all sources
- ✅ Synthesis reviewed and approved
- ✅ Strategic direction confirmed

**After Phase 2:**
- ✅ Design system validated (3 samples)
- ✅ Deck matches reference style
- ✅ Main deck < 25 slides
- ✅ Appendix complete with audit trail
- ✅ Google Sheets populated

---

## 🚦 CHECKPOINTS (STOP POINTS)

### ⛔ CHECKPOINT 1: Data Collection Complete
**When:** After Phase 0 (Day 5)
**Share:** Dataset stats, product catalog preview
**Get:** Approval to proceed to analysis

### ⛔ CHECKPOINT 2: Synthesis Review
**When:** After Phase 1 (Day 15)
**Share:** Key findings summary (2-3 pages)
- Market structure insights
- Jobs-to-be-done framework
- Pain points summary
- Brand perception synthesis
- Top 3 opportunities + Top 3 issues
**Get:** Feedback, strategic direction confirmation

### ⛔ CHECKPOINT 3: Design System Validation (CRITICAL)
**When:** Phase 2, Week 3 (Day 18)
**Share:** 3 sample slides in PowerPoint
- Slide 1: Title/section slide
- Slide 2: Data visualization slide
- Slide 3: Framework/concept slide
**Share:** Design documentation
- Color palette (hex codes)
- Font specs
- Layout templates
- Chart styling guide
- Reusable code modules
**Get:** Design approval before building remaining slides

---

## 📁 FILE STRUCTURE

```
modules/brand-perceptions/
├── PROJECT_EXECUTION_PLAN.md (this file)
├── data/
│   ├── collected/
│   │   ├── amazon_reviews_raw/
│   │   ├── reddit_raw/
│   │   └── youtube_raw/
│   ├── consolidated/
│   │   ├── product_reviews_full.json (3,800 reviews)
│   │   ├── social_media_posts_full.json
│   │   └── product_catalog.json (NEW)
│   └── analysis/
│       ├── sentiment_scores.json
│       ├── topics.json
│       ├── brand_perception.json
│       └── strategic_synthesis.json
├── analysis/
│   ├── scripts/
│   │   ├── gpt4_sentiment.py
│   │   ├── gpt4_topics.py
│   │   └── synthesis.py
│   └── reports/
│       ├── CHECKPOINT_2_SYNTHESIS.md
│       └── ANALYSIS_SUMMARY.md
└── deck/
    ├── design_system/
    │   ├── DESIGN_SPECS.md
    │   ├── colors.json
    │   ├── fonts.json
    │   └── templates/
    ├── scripts/
    │   ├── create_slide.py (reusable module)
    │   ├── generate_chart.py
    │   └── build_deck.py
    ├── samples/
    │   └── CHECKPOINT_3_SAMPLES.pptx (3 slides)
    └── output/
        └── 3M_Market_Intelligence.pptx
```

---

## 🎨 DESIGN SYSTEM (Phase 2)

### Must Document at Checkpoint 3:
1. **Color Palette**
   - Primary colors (hex codes from reference deck)
   - Secondary colors
   - Text colors (headings, body, labels)
   - Chart colors (data series)

2. **Typography**
   - Heading font (name, size, weight)
   - Body font (name, size, weight)
   - Label font (charts, captions)
   - Hierarchy rules

3. **Layout Templates**
   - Margins (top, bottom, left, right)
   - Title placement
   - Content area dimensions
   - Footer/header specs

4. **Chart Styling**
   - Bar chart template
   - Line chart template
   - Pie/donut chart template
   - Scatter plot template
   - Color assignments
   - Label formatting
   - Legend placement

5. **Reusable Modules**
   - `create_title_slide(title, subtitle)`
   - `create_section_slide(section_name)`
   - `create_data_slide(title, chart, bullets)`
   - `create_framework_slide(title, diagram)`
   - `apply_theme(slide)`

---

## 📊 GOOGLE SHEETS TAB SPECS

### Tab 10: Product Catalog (NEW)

**Columns:**
- Sub-Category (e.g., "Hooks - Heavy Duty", "Mounting Tape - Permanent")
- Brand (Command, Scotch, 3M Claw, Navona, etc.)
- Product Name (full title)
- Price (USD, as scraped)
- Review Score (e.g., "4.2 out of 5 stars")
- Review Count (number of reviews)
- Retailer (Amazon, Home Depot, etc.)
- Product URL (link to source page)
- ASIN/Product ID
- Collected Date

**Format:**
- Clean table, sortable
- Color-coded by brand
- Filterable by sub-category
- Hyperlinked URLs

**Purpose:**
- Complete product universe documented
- Source traceability
- Price/performance benchmarking
- Market coverage analysis

---

## 🔍 COMMUNICATION PRINCIPLES (Offbrain)

### Main Deck: Strategic Brevity
- "Sorry I didn't have time to write a shorter letter"
- Every word must earn its place
- Distill complexity to essential truth
- Takes MORE time and thinking
- One clear insight per slide
- No verbal vomit
- Dense with meaning, light on words

### Appendix: Comprehensive Defense
- More is better
- Show all work
- Defend every claim
- Complete data tables
- Full methodology
- Audit trail to sources

### Checkpoints: Flow Mode
- Bullets, emojis, <100 words
- Concrete actions/results
- No theoretical explanations
- Show, don't tell

---

## ⏱️ TIMELINE SUMMARY

| Phase | Duration | Output | Checkpoint |
|-------|----------|--------|------------|
| 0: Data Collection | 5 days | 3,800 records | ✋ Review dataset |
| 1: Analysis | 10 days | Synthesis complete | ✋ Review findings |
| 2: Design Setup | 3 days | 3 sample slides | ✋ Approve design |
| 2: Deck Build | 7 days | Full deck | - |
| 3: Polish | 5 days | Final deliverables | - |

**Total: 30 days (4 weeks full-time)**

---

## 🚀 IMMEDIATE NEXT STEPS

**After final approval:**
1. Begin data collection (Scotch + 3M Claw products)
2. Run YouTube/Reddit searches
3. Build product catalog
4. Validate dataset
5. **STOP at Checkpoint 1** for review

---

**Status:** ✅ READY FOR FINAL APPROVAL
**Waiting on:** Go/no-go decision
**First action:** Start Amazon scraping (Scotch products)
