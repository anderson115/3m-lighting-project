# Claude Category Intelligence – Development Blueprint

**Status:** Drafted 2025-10-24  
**Maintainers:** Offbrain Insights Dev Squad  
**Primary Use Case:** Enterprise-grade Category Intelligence across any retail vertical, first beta on *Garage Organization* (hooks, hangers, rail & slatwall systems) for Chris' request.  
**Zero-Fabrication Mandate:** Enforced via agentic validation, human QA, and audit trails.

---

## 1. Mission & Deliverables

| Output | Description | Format | Storage |
| --- | --- | --- | --- |
| Category Intelligence Report | Consulting-style narrative with data tables, charts, and citations; supports conversion to PowerPoint/GSlides | Markdown (`reports/{category}/{timestamp}.md`) | Versioned + archived in Postgres (see §8) |
| Keyword Opportunity Addendum | "Hidden keyword gems" surfaced with context, CPC gap, and validation | Markdown section + CSV | Same as above |
| Product Intelligence Workbook | Up to 400 best-selling SKUs per retailer with enriched attributes | Excel (`workbooks/{category}_{date}.xlsx`) + Parquet snapshot | Stored & indexed in Postgres + file cache |
| Source Audit | Complete list of URLs, retrieval timestamps, extraction confidence | JSON + SQL tables | Postgres (`/Volumes/DATA/storage/postgresql`) |

The system must scale to any category by swapping retailer taxonomy rules and keyword harvest seeds without code rewrites.

---

## 2. Architecture Overview

### Dual Orchestration (Legacy → Agentic)
1. **Legacy Core (stable)** – `core/orchestrator.py` continues to run until new agents are fully migrated.  
2. **Agentic Layer (new)** – `agents/orchestrator.py` coordinates collectors (brand, market, pricing, keyword, product ranking) with validators and reviewers.

A Sentinel monitors pipeline health; failures halt downstream stages rather than inserting placeholders.

### Key Pipelines
1. **Market & Brand Intelligence** – existing collectors (brand discovery, market sizing, pricing, taxonomy) updated to real data.  
2. **Keyword Signals** – new pipeline for emergent language and CPC gaps (§4).  
3. **Product Ranking Aggregator** – new pipeline to capture top products per retailer with rich attributes (§5).  
4. **Synthesis & Reporting** – transforms structured data into Markdown narrative + Excel workbook.

Shared utilities (real web search, source tracker, data storage) are reused wherever possible. Minimal new scripts; agents handle reasoning and orchestration logic.

---

## 3. Core Category Intelligence Pipeline (Reusable for Any Vertical)

| Stage | Agent / Module | Responsibilities | Notes |
| --- | --- | --- | --- |
| 0. Preflight | `SourceSentinelAgent` | Verify API credentials, quotas, retailer endpoints, cache writability | Runs before every job; logs to Postgres `pipeline_runs` |
| 1. Brand Discovery | `BrandDiscoveryReal` (agents + collectors) | Query + extract ≥50 brands across tiers, cross-validate | Reuses `collectors/brand_discovery_real.py`; fallback to curated seeds if coverage < threshold |
| 2. Taxonomy Builder | `TaxonomyAgent` | Map retailer taxonomy → unified category schema (4–8 subcategories) | No hardcoding; uses retailer category breadcrumbs + NLP clustering |
| 3. Pricing Analyzer | `PricingCollectorReal` | Gather price ranges, median, unit volumes per subcategory | Pulls from retailer listings + manufacturer data; flagged when stock data missing |
| 4. Market Sizing | `MarketResearcherReal` | Historical & forecast sizes, growth drivers/inhibitors | Uses web search + economic APIs; citations tracked |
| 5. Resource Curator | `ResourceCurationAgent` | 30–40 authoritative resources | Weighted by authority, recency, relevance |
| 6. Consumer Insight (optional linkage) | `ConsumerInsightAgent` | Summaries from transcripts / UGC when available | Interfaces with Consumer Video module |
| 7. Quality Gate | `ValidatorAgents` | Validate coverage, citation counts, numeric sanity | No progression if coverage thresholds unmet |
| 8. Reporting | `ReportComposer` | Assemble Markdown narrative, tables, charts metadata | Works with `generators/html_reporter.py` (future: PPT export) |

All stages write structured outputs (JSON/Parquet) plus audit metadata into Postgres for traceability.

---

## 4. Keyword Signals Module (Integrated)

### Scope & Success Criteria
- Detect ≥10 emerging/undervalued keywords per category with supporting evidence.  
- Provide novelty score, CPC gap, cultural context, and recommended action.  
- No fabricated gaps—if CPC/volume unavailable, recorded as "data unavailable" with reason.

### Data Source Stack (Ordered by Priority)
| Rank | Source | Acquisition | Stability | Notes |
| --- | --- | --- | --- | --- |
| 1 | Reddit (target subs, r/Ask*, r/NoStupidQuestions) | Reddit API + Pushshift; agent selects high-velocity threads | High | Primary corpus; reused from Expert Authority cache |
| 2 | YouTube captions & comments (creators <50k subs) | YouTube Data API + transcript puller; velocity filter | Medium | Share quota + utilities with Creator Intelligence |
| 3 | TikTok hashtags & transcripts | Apify TikTok Scraper + Playwright fallback | Medium | Borrow stealth configs from Creator Intelligence; low-frequency pulls |
| 4 | Amazon Q&A & discussions | Scrapling fetcher; targeted product URLs | Medium | Focus on under-the-radar language |
| 5 | Google Autocomplete drift | Headless agent monthly snapshots | High | Measures mainstream uptake |
| 6 | Discord / niche forums | Human-approved capture | Low | Optional exploratory |
| 7 | Substack comments, newsletters | RSS + HTML parser | Medium | Adds expert lexicon |
| 8 | X/Twitter Spaces transcripts | Community recordings + Whisper | Low | Use opportunistically |

### Agentic Pipeline
| Stage | Function | Key Checks |
| --- | --- | --- |
| Sentinel | Monitor source availability; route to backups | Logs uptime, triggers alerts |
| Harvest | Collect fresh corpora with metadata | Ensure min volume per source; dedupe |
| Novelty Extraction | Compare against historical corpus; score acceleration | Embeddings + freq slope; reject boilerplate |
| Cross-Source Validation | Confirm relevance, measure spread, fetch CPC proxies | Uses Google Ads Planner / TikTok Ads sandbox; fallback to public CPC APIs |
| Intent Profiler | Summarize why the term matters (JTBD snippet, sentiment) | Cites quotes; uses local LLM from `/Volumes/TARS/llm-models` |
| Opportunity Ranking | Score (novelty × cultural lift ÷ paid saturation) | Weights configurable per category |
| Reviewer QA | Analyst reviews evidence before release | Mandatory approval; rejects slop |
| Output Writer | Append to Markdown + CSV; push to Postgres | Fails if <10 validated terms |

Outputs feed both the narrative (dedicated section) and structured files for downstream teams.

---

## 5. Product Ranking Aggregator (Top 400 SKUs per Retailer)

### Retailers Covered
Amazon, Home Depot, Lowe’s, Menards, Target, Walmart. Pipeline must support quick onboarding of additional retailers via config files (selectors, pagination pattern, attribute map).

### Data Capture Requirements
- Up to 400 best-selling/most-popular items per retailer (if fewer exist, log coverage).  
- Attributes: name, brand, product URL, retailer taxonomy path, image link, price, star rating, material, color, weight capacity/claim (only usage capacity, never product weight), retailer name, rail/slat participation (Yes/No + role: rail/slat vs. attachment vs. kit), hook/hanger flag, list position.  
- Sales Rank: Amazon uses official Best Seller Rank; other retailers capture list position in "best seller/most popular" ordering (documented in `rank_type`).

### Collector Strategy
| Retailer | Primary Method | Backup | Notes |
| --- | --- | --- | --- |
| Amazon | Product Advertising API or on-demand HTML scrape | Apify Amazon scraper | Extracts BSR, price, rating reliably |
| Home Depot | Category listing sorted by "Best Seller" | Headless browser pagination | Rank stored as list position |
| Lowe’s | Similar to Home Depot | API feed if available | |
| Menards | HTML scrape with load-more handling | Manual CSV import (if gating occurs) | |
| Target | Public API (TGT) sorted by popularity | Playwright fallback | |
| Walmart | Search API sorted by "best sellers" | HTML fallback | |

### Enrichment & Validation
- Detail scraper fetches additional attributes (materials, color, weight capacity).  
- Classification agent (local LLM) labels rail/slat involvement and hook/hanger.  
- Image URL validated (200 OK).  
- Missing attributes flagged `Not listed` with reason; no substitution.  
- Excel workbook generated via shared reporter; Parquet + SQL tables created for analytics.

---

## 6. Data Storage & Persistence

- **Relational DB:** Postgres instance at `/Volumes/DATA/storage/postgresql`.  
  - Tables: `pipeline_runs`, `brand_insights`, `market_metrics`, `pricing_snapshots`, `keyword_opportunities`, `retailer_products`, `citations`.  
  - Use SQLAlchemy layer under `utils/data_storage.py` to write/append records.  
  - Enforce schema migrations via Alembic.
- **File Cache:** Under `modules/category-intelligence/data/` organized by category/run.  
- **Models:** Local inference via `/Volumes/TARS/llm-models` (e.g., Qwen2.5-VL, embedding models). Configure loader to prefer local path before remote API usage.  
- **Secrets:** Environment variables loaded from `.env` (never committed).  
- **Backups:** Daily DB backup to `/Volumes/DATA/storage/backups` (coordinated with infra team).

---

## 7. Quality, Monitoring & Human-in-the-Loop

- **Automated Checks:** Coverage thresholds, numeric sanity (prices, sizes), citation count per insight, duplication detection.  
- **Human QA:** Reviewer must approve keyword opportunities and final report before release.  
- **Run Logs:** Each pipeline stage logs counts, errors, execution time to Postgres + console.  
- **Alerts:** If critical source fails twice consecutively, send Slack/email alert (integration TBD).  
- **Versioning:** Each report references pipeline commit hash for reproducibility.

---

## 8. Implementation Phases & Timeline (High-Level)

| Phase | Duration | Focus | Key Deliverables |
| --- | --- | --- | --- |
| 1. Infrastructure Setup | 1 week | Sentinel agent, DB schemas, cache directories, env config | DB tables, health checks, run registry |
| 2. Retailer Collectors | 2 weeks | Implement + harden Amazon/Home Depot → remaining retailers | 400-SKU Excel prototype per retailer |
| 3. Keyword Pipeline MVP | 1 week | Reddit + Google Autocomplete; novelty engine | Keyword CSV + review workflow |
| 4. Validation Layer | 1 week | CPC gap lookup, cross-source corroboration, QA tooling | Promotion to beta |
| 5. Full Category Synthesis | 1 week | Integrate outputs into Markdown report; human QA process | Garage Organizer draft report + workbook |
| 6. Hardening & Scale | 1 week | Load tests, failover drills, documentation updates | Production-ready blueprint |

Total estimate ≈6 weeks (parallel execution possible across teams).

---

## 9. Reuse & Cross-Project Alignment

- **Social Signal Module:** Provide TikTok/Pinterest scrapers & CLIP embeddings for visual insights if needed.  
- **Creator Intelligence:** Share Apify/Playwright configs, YouTube parsing.  
- **Expert Authority:** Leverage Reddit caches & sentiment heuristics.  
- **Consumer Video:** Optional integration for qualitative quotes.  
All shared assets documented in `docs/integration_guide.md` updates.

---

## 10. Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Retailer anti-scrape blocks | Data gaps, delays | Respect rate limits, rotate headers, maintain backup APIs, log failures transparently |
| API quota exhaustion | Partial coverage | Schedule runs, share quota dashboards, implement caching |
| Keyword false positives | Weak insights | Multi-source validation + human reviewer; thresholds on novelty & CPC gap |
| Report slop | Client dissatisfaction | Quality gates + manual QA; fail run if insight density < target |
| Schema drift | Integration breakage | Enforce schema tests; versioned migrations |

---

## 11. Next Actions

1. Confirm access to retailer APIs/scrapers; request credentials where needed.  
2. Stand up Postgres connection strings and test write/read from `/Volumes/DATA/storage/postgresql`.  
3. Configure local model loader pointing to `/Volumes/TARS/llm-models`.  
4. Kick off Phase 1: implement Sentinel agent + run registry.  
5. Coordinate cross-module meeting (Category, Creator, Social) to align on shared scrapers and quotas.  
6. Begin Amazon + Home Depot collector development (garage organizer focus) while documenting taxonomy mapping.

Once Phase 2 completes, we can begin delivering beta outputs for Garage Organization while finalizing keyword and reporting layers for full production rollout.
