# Creator Discovery Module

**Purpose:** Identify, catalog, and profile lighting-focused creators across YouTube, TikTok, Instagram, and Pinterest for partnership opportunities and content analysis.

## Quick Start

```bash
# Discover creators by platform
python scripts/youtube_discovery.py --keyword "DIY lighting installation"

# Profile creator channels
python scripts/creator_profiler.py --channel_ids data/raw/youtube_channels.json

# Score partnership fit
python scripts/partnership_scorer.py

# Generate creator database
python scripts/generate_creator_db.py
```

## Module Structure

```
creator-discovery/
├── scripts/
│   ├── youtube_discovery.py         # YouTube channel discovery
│   ├── tiktok_discovery.py          # TikTok creator search
│   ├── instagram_discovery.py       # Instagram profile finder
│   ├── creator_profiler.py          # Multi-platform profile builder
│   ├── partnership_scorer.py        # Brand fit scoring algorithm
│   ├── content_analyzer.py          # Creator content themes
│   └── generate_creator_db.py       # Creator database generator
├── data/
│   ├── raw/
│   │   ├── youtube_channels.json    # Discovered YouTube channels
│   │   ├── tiktok_creators.json     # TikTok creator profiles
│   │   └── instagram_profiles.json  # Instagram lighting accounts
│   ├── processed/
│   │   ├── creator_database.json    # Unified creator catalog
│   │   ├── partnership_scores.json  # Brand fit rankings
│   │   └── content_themes.json      # Creator content analysis
│   └── deliverables/
│       ├── Creator_Database.html    # Searchable creator catalog
│       └── Partnership_Report.html  # Top creator recommendations
├── config/
│   ├── discovery_keywords.yaml      # Search keywords per platform
│   ├── scoring_criteria.yaml        # Partnership fit criteria
│   └── platforms.yaml               # API configurations
├── docs/
│   ├── PRD-creator-discovery.md     # Original PRD
│   └── SPECIFICATION.md             # Implementation specs
└── README.md                        # This file
```

## Target Platforms

### Primary Discovery Sources
- **YouTube** - DIY channels, electrician tutorials, home improvement
- **TikTok** - Short-form lighting hacks, installation tips
- **Instagram** - Lighting designers, DIY influencers, before/after accounts
- **Pinterest** - High-engagement DIY boards (creator identification)

### Creator Types
- **DIY Educators** - Tutorial-focused, tool reviews, installation guides
- **Electricians/Professionals** - Technical expertise, safety-focused
- **Interior Designers** - Aesthetic lighting, trend-setters
- **Product Reviewers** - Unboxing, comparison, stress tests
- **Home Improvement Generalists** - Multi-topic creators with lighting content

## Analysis Pipeline

### Phase 1: Discovery
1. **Keyword Search** - Platform-specific API queries (lighting, installation, DIY)
2. **Channel Filtering** - Minimum thresholds (subscribers, engagement, content volume)
3. **Relevance Scoring** - Lighting content percentage, niche focus

### Phase 2: Profiling
4. **Metadata Collection** - Subscribers, views, upload frequency, engagement rate
5. **Content Analysis** - Top videos, common themes, product mentions
6. **Audience Demographics** - Age, gender, geography (when available)
7. **Cross-Platform Linking** - Identify multi-platform creators

### Phase 3: Scoring
8. **Partnership Fit Algorithm** - Brand alignment, audience match, engagement quality
9. **Content Theme Mapping** - DIY tutorials, product reviews, trends, troubleshooting
10. **Risk Assessment** - Controversy check, brand safety, content consistency

### Phase 4: Cataloging
11. **Creator Database** - Unified profile across platforms
12. **Tiered Categorization** - Tier 1 (top partners), Tier 2 (potential), Tier 3 (monitor)
13. **Client Deliverable** - Searchable creator catalog with recommendations

## Key Metrics

### Creator Quality Signals
- **Audience Size** - Subscribers/followers (platform-specific thresholds)
- **Engagement Rate** - Views-to-subscribers ratio, comments, likes
- **Upload Consistency** - Frequency, regularity, content volume
- **Niche Focus** - % of content related to lighting/home improvement
- **Production Quality** - Video quality, editing, professionalism

### Partnership Fit Criteria
- **Brand Alignment** - Content tone, values, safety-consciousness
- **Audience Demographics** - Homeowners, DIYers, age 25-55
- **Product Affinity** - Existing 3M mentions, adhesive usage, tool compatibility
- **Engagement Quality** - Comment sentiment, community interaction
- **Growth Trajectory** - Subscriber growth rate, trending topics

## Output Files

### Raw Data (`data/raw/`)
- Platform-specific JSON files with discovered creator profiles
- Metadata: channel ID, name, URL, subscribers, recent videos

### Processed Database (`data/processed/`)
- `creator_database.json` - Unified creator profiles with scoring
- `partnership_scores.json` - Ranked list by brand fit
- `content_themes.json` - Creator content categorization

### Client Deliverables (`data/deliverables/`)
- `Creator_Database.html` - Searchable catalog (filterable by tier, platform, theme)
- `Partnership_Report.html` - Top 20 creator recommendations with rationale

## Partnership Scoring Algorithm

### Scoring Components (0-100 scale)
1. **Audience Match (30%)** - Demographics, homeowner likelihood, geography
2. **Content Relevance (25%)** - Lighting content %, DIY focus, technical depth
3. **Engagement Quality (20%)** - Comments/views ratio, sentiment, community health
4. **Brand Safety (15%)** - Content consistency, controversy check, professionalism
5. **Growth Potential (10%)** - Subscriber growth, trending topics, innovation

### Tier Classification
- **Tier 1 (80-100)** - Top partnership candidates, immediate outreach
- **Tier 2 (60-79)** - Potential partners, monitor for growth
- **Tier 3 (40-59)** - Watch list, niche relevance but lower priority
- **Below 40** - Not recommended for partnership

## Technical Stack

- **YouTube** - YouTube Data API v3 (channel search, metadata, analytics)
- **TikTok** - Unofficial API/scraping (Playwright-based)
- **Instagram** - Graph API (limited) + web scraping
- **Cross-Platform** - Manual linking + fuzzy name matching
- **Storage** - JSON database, SQLite for querying

## Status

📋 **Planning Stage** - PRD complete, module scaffolded, implementation pending

## Scope & Constraints

### In Scope
- Creator discovery and profiling (metadata only)
- Partnership fit scoring based on public data
- Content theme analysis (video titles, descriptions)
- Multi-platform creator linking

### Out of Scope
- Direct creator outreach (CRM integration separate)
- Contract negotiation, payment processing
- Real-time monitoring (quarterly batch updates)
- Sentiment analysis of creator's audience comments (Phase 2)

## Privacy & Compliance

- **Public Data Only** - No private messages, analytics, or gated content
- **API Terms Compliance** - Respect rate limits, caching, attribution
- **No Scraping Abuse** - Ethical scraping with delays, robots.txt respect
- **GDPR/Privacy** - Aggregate creator data only, no individual tracking

## Integration Points

### Synergy with Other Modules
- **consumer-video** - Analyze content from discovered creators
- **social-signal** - Pinterest/Instagram creators feed visual analysis
- **expert-authority** - Verified professional creators (electricians, designers)

## Use Cases

1. **Partnership Pipeline** - Identify top 20 creators for 3M brand partnerships
2. **Content Gap Analysis** - What lighting topics lack quality creators?
3. **Competitive Intelligence** - Which creators promote competitor products?
4. **Trend Forecasting** - Emerging creator content themes signal market shifts
5. **Influencer Marketing ROI** - Score existing partnerships, suggest alternatives

## Next Steps

1. Implement YouTube Data API integration
2. Design partnership scoring algorithm (weights validation)
3. Build multi-platform creator linking (fuzzy matching)
4. Create searchable creator database UI (HTML report)
5. Validate on lighting niche (baseline 100 creators)
