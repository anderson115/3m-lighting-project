# Expert Authority Module

**Purpose:** Extract authoritative insights from expert discussions on Reddit, Quora, and Stack Exchange where professionals debate lighting installation, electrical safety, and home improvement solutions.

**Status:** ✅ Preflight Complete - Ready for Production Implementation

## Quick Start

```bash
# Run preflight test (no API credentials required)
python scripts/preflight_test.py

# For production use (requires Reddit API credentials):
# 1. Set up config/reddit_auth.json with your credentials
# 2. Run tier-based analysis (coming in Week 2)
```

## Preflight Test Results

✅ **All 5 tests passed** (2025-10-09)
- 5 themes extracted via rule-based method
- 5 consensus patterns identified
- 4 controversial topics detected
- 100% consumer pain point validation rate
- HTML report generated (6.4 KB)

## Module Structure

```
expert-authority/
├── scripts/
│   └── preflight_test.py          # ✅ Preflight validation (complete)
├── data/
│   ├── raw/                       # Scraped forum threads (JSON)
│   ├── processed/                 # Analysis outputs
│   │   └── preflight_test_results.json
│   └── deliverables/              # Client reports
│       └── Preflight_Test_Report.html
├── config/                        # Configuration files
├── docs/
│   └── PRD-expert-authority.md    # ✅ Complete PRD v4.0
└── README.md                      # This file
```

## Target Platforms

### Primary Sources
- **Reddit** - r/homeimprovement, r/electricians, r/lighting, r/DIY
- **Quora** - Lighting, electrical installation, home improvement spaces
- **Stack Exchange** - Home Improvement, DIY, Electronics

### Secondary Sources
- **Professional Forums** - Electrician Talk, Contractor Talk
- **Technical Communities** - Engineer's Edge, Physics Forums

## Analysis Pipeline

### Phase 1: Discovery & Collection
1. **Forum Scraping** - Collect threads matching lighting keywords
2. **Expert Identification** - Score users by karma, verified status, post history
3. **Thread Classification** - Pain points, solutions, product recommendations, warnings

### Phase 2: Authority Analysis
4. **Consensus Detection** - Identify widely-agreed solutions (upvotes, agreement language)
5. **Controversy Mapping** - Flag areas of expert disagreement
6. **Citation Extraction** - Pull verbatim expert quotes with attribution

### Phase 3: Insight Synthesis
7. **Authority Scoring** - Weight insights by expert credibility
8. **Pattern Clustering** - Group similar expert opinions
9. **Client Reporting** - Generate expert authority report with citations

## Key Metrics

### Expert Credibility Signals
- **Karma/Reputation** - Platform-specific reputation scores
- **Verified Status** - Professional flair, credentials
- **Post Quality** - Length, detail, technical accuracy
- **Peer Validation** - Upvotes, awards, agreement responses

### Insight Types
- **Consensus Solutions** - Widely-agreed best practices
- **Warning Signals** - Common mistakes, safety issues
- **Product Recommendations** - Expert-endorsed products
- **Controversial Topics** - Areas of disagreement
- **Emerging Trends** - New techniques, materials

## Output Files

### Raw Data (`data/raw/`)
- Platform-specific JSON files (reddit_threads.json, quora_answers.json)
- Timestamp, author, content, metadata (karma, upvotes)

### Processed Insights (`data/processed/`)
- `expert_insights.json` - Scored and categorized expert opinions
- `consensus_patterns.json` - Widely-agreed solutions
- `controversy_map.json` - Areas of expert disagreement

### Client Deliverables (`data/deliverables/`)
- `Expert_Authority_Report.html` - Cited expert insights
- `Consensus_vs_Controversy.html` - Agreement/disagreement analysis

## Evidence-First Principles

- **Verbatim Quotes Required** - All insights cited with source
- **Authority Scoring Transparent** - Show expert credibility metrics
- **Multiple Sources** - Validate across platforms when possible
- **Timestamp Citations** - Include discussion date for currency
- **Context Preservation** - Maintain original discussion thread context

## Technical Stack

- **Scraping** - PRAW (Reddit), Beautiful Soup (Quora/forums), Selenium (dynamic)
- **NLP** - Sentiment analysis, consensus detection, keyword extraction
- **Authority Scoring** - Multi-factor credibility algorithm
- **Storage** - JSON for raw data, processed insights

## Three-Tier Pricing Structure

### 🥉 Tier 1: Essential ($299)
- Reddit-only, rule-based analysis
- 100 discussions, 3-page text report
- Top 5 consensus patterns
- 3-day turnaround

### 🥈 Tier 2: Professional ($799)
- Multi-platform (Reddit + Quora + Stack Exchange)
- LLM-powered theme discovery (Claude Sonnet 4)
- 10-page interactive report with charts
- Controversy mapping + safety warnings
- 5-day turnaround

### 🥇 Tier 3: Enterprise ($1,999)
- All platforms + professional forums
- Extended reasoning (Claude Opus + GPT-4o)
- 25-page strategic report + PowerPoint + Excel
- Temporal trend analysis (2-year)
- Competitive brand tracking
- 7-day turnaround + 1 revision

## Implementation Roadmap

### ✅ Week 0: Foundation (Complete)
- [x] PRD v4.0 finalized
- [x] Module structure created
- [x] Preflight test passing (100% validation rate)

### 📋 Week 1: Core Infrastructure (Pending)
- [ ] Reddit scraper with PRAW + caching
- [ ] Theme analyzer with LLM + fallback
- [ ] Consumer alignment module
- [ ] Unit tests

### 📋 Week 2: Tier System (Pending)
- [ ] Tier 1 Essential (rule-based)
- [ ] Tier 2 Professional (LLM + multi-platform)
- [ ] Tier 3 Enterprise (extended reasoning)
- [ ] CLI tier selector

### 📋 Week 3: Production (Pending)
- [ ] Run on 100+ real discussions
- [ ] Validate LLM vs rule-based quality
- [ ] Test offline mode
- [ ] Final documentation

## Technical Requirements

**Dependencies:**
- Python 3.11+
- PRAW (Reddit API) - Tier 1+
- Anthropic SDK (Claude) - Tier 2+
- OpenAI SDK (embeddings/GPT-4o) - Tier 2+/Tier 3

**Configuration Required:**
- Reddit API credentials (client_id, client_secret)
- Anthropic API key
- OpenAI API key (Tier 2+)

## Integration Points

### Synergy with Other Modules
- **consumer-video**: Validate consumer pain points with expert consensus
- **creator-discovery**: Identify expert creators (high-karma contributors)
- **social-signal**: Cross-reference Pinterest/Instagram trends with expert recommendations
