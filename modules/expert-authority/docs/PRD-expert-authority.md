# Expert Authority Module - Product Requirements Document v4.0

**Document Version:** 4.0 (Final)
**Last Updated:** 2025-10-09
**Status:** Ready for Implementation

---

## Executive Summary

**Purpose:** Extract authoritative insights from expert discussions on Reddit, Quora, and Stack Exchange where professionals debate lighting installation, electrical safety, and home improvement solutions.

**Goal:** Validate consumer findings with expert consensus, discover professional-grade solutions, and identify market opportunities through emergent theme analysis.

**Deliverable:** Tiered analysis packages (Essential/Professional/Enterprise) with expert-validated insights, controversy mapping, and competitive intelligence.

---

## Design Principles

### Core Philosophy
- **Emergent Discovery** > Keyword forcing (minimize bias)
- **Semantic Analysis** > Pattern matching (capture nuance)
- **Production Stability** > Cutting-edge complexity (Claude-developable)
- **Visible Differentiation** > Hidden model swaps (tier value clarity)

### Technical Requirements
✅ No complex ML pipelines (no training, no fine-tuning)
✅ Deterministic where possible (reproducible results)
✅ Graceful degradation (works even if APIs fail)
✅ Clear error handling (no silent failures)
✅ Modular architecture (swap components independently)
✅ Testable (unit tests for each stage)
✅ Observable (logs + progress tracking)

---

## Three-Tier Product Structure

### 🥉 Tier 1: Essential ($299/analysis)
**Target:** Small businesses, initial validation
**Promise:** "Validate consumer findings with expert consensus"

**Deliverable:**
- Reddit-only data (r/electricians, r/homeimprovement)
- Rule-based theme extraction (6-8 themes)
- Basic consumer alignment (keyword matching)
- 3-page text HTML report
- Top 5 consensus patterns
- 100 discussions analyzed
- 3-day turnaround

### 🥈 Tier 2: Professional ($799/analysis)
**Target:** Market research teams, product managers
**Promise:** "Discover hidden patterns across expert communities"

**Deliverable (Everything in Tier 1 PLUS):**
- Multi-platform data (Reddit + Quora + Stack Exchange)
- LLM-powered theme discovery (Claude Sonnet 4)
- Semantic consumer alignment (embedding-based)
- 10-page interactive HTML report with visualizations
- Controversy mapping (where experts disagree)
- Safety warnings extraction
- Novel insight detection
- 300 discussions analyzed
- 5-day turnaround

### 🥇 Tier 3: Enterprise ($1,999/analysis)
**Target:** Fortune 500, agencies, deep research
**Promise:** "Industry-grade intelligence with competitive analysis"

**Deliverable (Everything in Tier 2 PLUS):**
- Professional forum access (Electrician Talk, Contractor Talk)
- Extended reasoning models (Claude Opus 4 + GPT-4o)
- Temporal trend analysis (2-year historical patterns)
- Competitive product mention tracking
- Expert influencer identification (top 20 authorities)
- Cross-module synthesis (consumer + expert + creator data)
- 25-page strategic report + PowerPoint slides + Excel export
- 500+ discussions analyzed
- 7-day turnaround + 1 revision round

---

## Technical Architecture

### Stage 1: Data Collection (Stable Scraping)
```
Input:  Platform + Category (e.g., "Reddit + lighting")
Process: Scrape discussions with minimal filtering
Output: Raw JSON files (1 file per platform)
Fallback: Cached data if API fails
```

**Platforms:**
- Tier 1: Reddit (PRAW API)
- Tier 2: Reddit + Quora (Selenium) + Stack Exchange API
- Tier 3: All above + Professional forums (custom scrapers)

### Stage 2: Semantic Analysis (LLM-Powered)
```
Input:  Raw discussion JSON
Process: Batch LLM analysis (themed discovery)
Output: Structured insights JSON
Fallback: Rule-based extraction if LLM unavailable
```

**Analysis Methods:**
- Tier 1: Rule-based keyword patterns (deterministic)
- Tier 2: Claude Sonnet 4 emergent discovery (semantic)
- Tier 3: Claude Opus 4 + GPT-4o cross-validation (extended reasoning)

### Stage 3: Synthesis (Template-Based Reporting)
```
Input:  Insights JSON + Consumer data JSON
Process: Cross-reference + HTML generation
Output: Tiered reports (3/10/25 pages)
Fallback: Always succeeds (even with partial data)
```

---

## Anti-Bias Methodology

### Problem with Keyword-Only Approach
❌ Search: "LED strip adhesive failing"
→ Only finds discussions that use exact phrase
→ Misses: "tape won't stick", "mounting issues", "fell off ceiling"
→ Self-fulfilling: We only discover what we already expect

### Three-Stage Anti-Bias Pipeline

#### Stage 1: Wide-Net Discovery
- **Topic Modeling:** LDA on all discussions (unsupervised)
- **Seed-and-Expand:** Start with generic queries, follow network effects
- **Expert-Led Discovery:** Scrape top contributors' history (what do experts care about?)

#### Stage 2: Semantic Pattern Recognition
- **Frustration Signal Detection:** NLP markers (repeated failure, confusion, safety concerns)
- **Consensus Emergence:** Agreement graph + PageRank (not just upvotes)
- **Controversy Detection:** Semantic divergence in embedding space

#### Stage 3: Consumer Validation
- **Blind Cross-Reference:** Test if consumer pain points appear in expert discussions WITHOUT pre-filtering
- **Novel Discovery:** Identify expert pain points consumers DIDN'T mention

### Validation Metrics
- **Novelty Score:** ≥40% of pain points NOT in seed keywords
- **Cross-Platform Replication:** ≥60% themes appear on 2+ platforms
- **Disconfirmation Rate:** 10-20% of findings get challenged (healthy skepticism)
- **Expert Diversity:** No single expert >15% of citations

---

## Implementation Roadmap

### Week 1: Core Infrastructure
- [ ] `reddit_scraper.py` with PRAW + caching
- [ ] `analyze_themes.py` with LLM + rule-based fallback
- [ ] `align_with_consumer.py` with keyword/semantic matching
- [ ] Unit tests for each component

### Week 2: Tier System
- [ ] `tier1_essential.py` (rule-based, Reddit-only)
- [ ] `tier2_professional.py` (LLM, multi-platform)
- [ ] `tier3_enterprise.py` (extended reasoning, competitive)
- [ ] `run_tiered_analysis.py` orchestrator

### Week 3: Validation & Documentation
- [ ] Run preflight on 100 real discussions
- [ ] Verify LLM vs rule-based output quality
- [ ] Test offline mode (no API keys)
- [ ] Update all documentation

---

## Success Criteria

### Quantitative Metrics
- **Coverage:** 100/300/500+ discussions per tier
- **Expert Quality:** 60%+ posts from verified/high-karma experts
- **Consensus Detection:** Identify 5+/10+/15+ widely-agreed solutions per tier
- **Consumer Alignment:** 80%+ consumer pain points validated by experts
- **Processing Time:** Complete within tier SLA (3/5/7 days)

### Qualitative Outcomes
- **Validation:** Consumer findings confirmed by professional consensus
- **New Insights:** Discover 3+ expert-identified pain points consumers missed
- **Safety Value:** Extract 5+ code-compliant best practices
- **Controversy Clarity:** Map 2+ debated topics with nuanced explanations

---

## Citation Integrity & Validation

**MANDATORY:** All tiers must implement Citation Integrity Protocol.

**See:** `docs/CITATION-INTEGRITY-PROTOCOL.md` for complete specification

**Key Requirements:**
- ✅ Every insight must link to original discussion (permanent URL)
- ✅ All quotes verified against raw scraped data (no fabrication)
- ✅ Statistics recomputed from source data (no hallucination)
- ✅ 95%+ citations must pass validation before delivery
- ✅ Audit trail generated for every report
- ✅ Deleted content flagged with archive.org fallback

**Validation Pipeline:**
1. **Pre-Processing:** URL accessibility check during scraping
2. **Post-Processing:** Quote verification against raw JSON
3. **Pre-Delivery:** Generate citation audit trail (100% verification required)

**Client Deliverable Includes:**
- Main report with inline citations [View Original] links
- Citation index with all source URLs
- Validation audit trail proving integrity
- Raw data package (Tier 3 only)

**Anti-Hallucination Safeguards:**
- LLM outputs constrained to reference only provided discussions
- Cross-reference validation (themes must match raw data)
- Quote authenticity verification (fuzzy matching 95%+ similarity)
- Statistical claims recomputed from source (±1% tolerance)

---

## Dependencies

### Required
- Python 3.11+
- PRAW (Reddit API)
- Anthropic SDK (Claude)
- OpenAI SDK (embeddings, optional GPT-4o for Tier 3)
- requests (URL validation)
- hashlib (content integrity verification)

### Optional (Tier-Dependent)
- Selenium (Quora scraping, Tier 2+)
- python-pptx (PowerPoint generation, Tier 3)
- pandas + openpyxl (Excel export, Tier 2+)

### Configuration Required
- Reddit API credentials (client_id, client_secret)
- Anthropic API key
- OpenAI API key (Tier 2+ for embeddings, Tier 3 for GPT-4o)

---

## Risk Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| API rate limits hit | Scraping delays | Medium | Exponential backoff, cache responses |
| Low expert engagement | Insufficient data | Low | Expand time window to 24 months |
| Platform TOS changes | Legal/access issues | Low | Monitor quarterly, alternative sources ready |
| Spam/low-quality posts | Noisy data | Medium | Credibility scoring filters out low-tier |
| LLM API downtime | Analysis blocked | Medium | Rule-based fallback always available |

---

## Deliverable Specifications

### Tier 1: Essential Report (3 pages)
- **Format:** HTML
- **Sections:** Key Themes (6-8), Top 5 Consensus Patterns, Consumer Alignment
- **Visuals:** None (text-only)
- **Badge:** "ESSENTIAL TIER" gray badge

### Tier 2: Professional Report (10 pages)
- **Format:** HTML + Excel
- **Sections:** Multi-Platform Analysis, Theme Discovery, Controversies, Safety Warnings, Consumer Alignment, Novel Insights
- **Visuals:** Plotly charts (theme frequency, controversy heatmap)
- **Badge:** "PROFESSIONAL TIER" teal badge

### Tier 3: Enterprise Package (25+ pages)
- **Formats:** HTML + Excel + PowerPoint + Executive Summary
- **Sections:** Strategic Analysis, Temporal Trends, Competitive Intelligence, Expert Influencer Profiles, Cross-Module Synthesis, Market Opportunities
- **Visuals:** Interactive dashboards, trend graphs, brand mention charts
- **Badge:** "ENTERPRISE TIER" gold badge

---

## Open Questions for Client Review

1. **Reddit API Credentials:** Can client provide Reddit app credentials, or should we create dedicated account?

2. **Professional Forum Access:** Tier 3 includes Electrician Talk / Contractor Talk - acceptable to create free accounts under research purposes?

3. **Competitive Tracking:** Which brands should we monitor in Tier 3? (Default: 3M, Philips, GE, Lutron, Leviton, Amazon Basics)

4. **Update Frequency:** Should this be one-time analysis or quarterly updates? (Pricing assumes one-time)

5. **Raw Data Delivery:** Tier 3 includes raw JSON/CSV - any privacy concerns with sharing scraped public data?

---

## Appendix: Sample Outputs

### Tier 1: Rule-Based Theme Example
```json
{
  "theme": "Adhesive/Mounting Issues",
  "frequency_pct": 18.5,
  "keywords": ["adhesive", "tape", "stick", "mount", "falling"],
  "examples": [
    "LED strip adhesive failing in hot garage",
    "3M tape won't hold under cabinet lights",
    "Best mounting method for outdoor LED strips"
  ]
}
```

### Tier 2: LLM-Discovered Theme Example
```json
{
  "theme": "Heat-Related Installation Failures",
  "description": "Adhesive degradation in high-temperature environments (garages, outdoor, near heat sources). Experts converge on VHB tape rated for 150°F+",
  "frequency_pct": 15.2,
  "category": "pain_point",
  "strategic_insight": "Temperature-rated adhesive products underrepresented in consumer market",
  "examples": ["Arizona outdoor LED failure", "Garage ceiling mount falling"]
}
```

### Tier 3: Temporal Trend Example
```json
{
  "theme": "Smart Home Integration",
  "direction": "📈 Rapidly Growing",
  "frequency_by_year": {
    "2023": 8.3,
    "2024": 14.7,
    "2025": 22.1
  },
  "insight": "Expert discussions about smart lighting compatibility tripled in 2 years. Opportunity: Develop smart-home-ready adhesive mounting solutions."
}
```

---

## Sign-Off

**PRD Approval Required From:**
- [ ] Product Manager
- [ ] Technical Lead (Claude Code)
- [ ] Client Stakeholder

**Implementation Start:** Upon approval + Reddit API credentials provided

**Estimated Delivery:** 3 weeks from start (Week 1: Core, Week 2: Tiers, Week 3: Validation)
