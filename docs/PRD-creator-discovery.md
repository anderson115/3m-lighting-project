# Product Requirements Document: Creator Discovery Module

**Project:** 3M Lighting Research Platform
**Module:** Creator Discovery
**Version:** 1.0 Draft
**Date:** 2025-10-08
**Status:** Planning

---

## 📋 Executive Summary

Automated creator discovery and cataloging system for identifying, analyzing, and qualifying social media creators across YouTube, TikTok, and Instagram within specific niches (starting with DIY lighting projects). Enables data-driven decisions for consumer research recruitment, brand partnerships, and audience understanding.

---

## 🎯 Problem Statement

**Current Challenge:**
Marketing teams manually search for creators in their niche, spending hours browsing platforms, taking screenshots, and maintaining spreadsheets. No systematic way to:
- Identify all relevant creators in a niche
- Compare creators by key metrics
- Qualify creators for different engagement types
- Understand aggregate audience demographics
- Track creator growth and content trends over time

**Business Impact:**
- Inefficient creator outreach (hours per creator)
- Missed partnership opportunities
- Limited audience insights
- No data-driven selection criteria
- Inconsistent vetting process

---

## 🎯 Goals & Success Metrics

### Primary Goals
1. **Automate Creator Discovery** - Find 100+ creators in target niche in <1 hour
2. **Enable Use Case Matching** - Classify creators by suitability (research, partnerships, audience insights)
3. **Provide Actionable Insights** - Demographics, psychographics, and engagement metrics in digestible format

### Success Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| **Discovery Speed** | 100+ creators in 60 min | Time from query to results |
| **Coverage Accuracy** | 90%+ relevant creators | Manual validation sample |
| **Use Case Match Rate** | 80%+ correctly classified | Team feedback on recommendations |
| **Time Savings** | 10x vs manual process | Hours saved per research cycle |
| **Adoption Rate** | 100% of team using module | Active users per month |

---

## 👥 Target Users & Use Cases

### Primary Users
1. **Marketing Managers** - Strategic partnerships, campaign planning
2. **UX Researchers** - Consumer research recruitment
3. **Product Managers** - Market understanding, audience insights
4. **Brand Strategists** - Influencer strategy, trend analysis

### Use Cases

#### 1️⃣ Consumer Research Participation
**Scenario:** Recruiting 10-15 DIY creators for lighting pain point interviews

**Requirements:**
- **Audience Size:** 5K-100K followers (authentic engagement, not mega-influencers)
- **Content Type:** Tutorial-focused, demonstrates lighting solutions
- **Engagement:** High comment activity (shows audience trust)
- **Location:** US/Canada preferred (timezone alignment)
- **Screening Criteria:** Clear audio, on-camera presence, relatable personality

**Output Needed:**
- Creator contact info (email, DM links)
- Content samples (top 5 videos with timestamps)
- Engagement metrics (avg views, comments, shares)
- Audience demographics (age, gender, interests)
- Qualification score (1-10 for research suitability)

#### 2️⃣ Brand Partnerships & Sponsorships
**Scenario:** Identifying 5-10 creators for 3M Command Hook lighting campaign

**Requirements:**
- **Audience Size:** 50K-500K followers (meaningful reach)
- **Brand Alignment:** Family-friendly, safety-conscious, DIY enthusiasts
- **Past Sponsorships:** Track record with home improvement brands
- **Engagement Rate:** 3%+ (indicates active, trusting audience)
- **Content Quality:** High production value, clear demonstrations
- **Growth Trajectory:** 20%+ YoY follower growth

**Output Needed:**
- Media kit summary (or generated from data)
- Estimated campaign reach
- Cost benchmarks (industry standard CPM/CPE)
- Brand safety score
- Past partnership performance (if available)
- Recommended partnership structure (product seeding, paid sponsorship, affiliate)

#### 3️⃣ Audience Demographics & Psychographics
**Scenario:** Understanding the DIY lighting audience to inform product development

**Requirements:**
- **Sample Size:** 50+ creators analyzed
- **Diversity:** Mix of nano, micro, mid-tier creators
- **Content Range:** Beginner to advanced DIY projects
- **Platform Mix:** YouTube, TikTok, Instagram representation

**Output Needed:**
- **Aggregate Demographics:**
  - Age distribution (18-24, 25-34, 35-44, 45+)
  - Gender breakdown
  - Geographic concentration
  - Income indicators (homeownership rate, property type)
- **Psychographics:**
  - DIY skill level (beginner, intermediate, expert)
  - Content preferences (quick tips vs. deep tutorials)
  - Pain points mentioned (lighting problems discussed)
  - Adjacent interests (home decor, organization, gardening)
- **Media Preferences:**
  - Platform preference (YouTube long-form vs. TikTok short-form)
  - Optimal video length per platform
  - Peak engagement times
  - Content format preferences (voiceover, face-to-camera, B-roll)

---

## 🔧 Functional Requirements

### Core Features

#### 1. Multi-Platform Creator Search
**Description:** Query YouTube, TikTok, Instagram APIs for creators in specified niche

**Inputs:**
- Niche keywords (e.g., "DIY lighting", "home lighting projects", "LED installations")
- Platform selection (YouTube, TikTok, Instagram, or All)
- Audience size filters (min/max followers)
- Location filters (country, region)
- Date range (active in last X months)

**Processing:**
- API calls to each platform
- Content keyword matching
- Channel metadata extraction
- Deduplication across platforms
- Initial relevance scoring

**Outputs:**
- List of creator profiles (name, handle, platform, URL)
- Basic metrics (followers, avg views, post frequency)
- Content categories/tags
- Discovery timestamp

**Technical Notes:**
- YouTube Data API v3 (quota: 10,000 units/day)
- TikTok Research API (requires Academic/Business access)
- Instagram Graph API (requires Business accounts)
- Fallback to web scraping if API quotas exceeded (ethical scraping only)

---

#### 2. Creator Profile Enrichment
**Description:** Deep analysis of each creator's channel, content, and audience

**Data Collection:**
- **Channel Metrics:**
  - Total subscribers/followers
  - Total views/likes
  - Join date / account age
  - Verification status
  - Post frequency (videos per month)
  - Growth rate (30-day, 90-day, 1-year)

- **Content Analysis:**
  - Recent video titles (last 20 videos)
  - Video descriptions
  - Tags/hashtags
  - Categories
  - Average video length
  - Content themes (extracted via NLP)

- **Engagement Metrics:**
  - Average views per video
  - Like rate (likes/views)
  - Comment rate (comments/views)
  - Share rate (if available)
  - Engagement rate (total engagement/followers)
  - Audience retention (if available via API)

- **Audience Insights:**
  - Age distribution (from platform analytics if accessible)
  - Gender breakdown
  - Top geographic locations
  - Device types (mobile vs. desktop)
  - Viewing times (peak engagement hours)

**Processing:**
- Batch API calls with rate limiting
- NLP analysis on titles/descriptions (keyword extraction, sentiment)
- Statistical aggregation of metrics
- Trend analysis (growth trajectories)
- Quality scoring (content consistency, production value indicators)

**Outputs:**
- Enriched creator profiles (JSON format)
- Time-series data (growth charts)
- Content summary (most popular videos, themes)
- Audience profile (demographics, behavior)

---

#### 3. Use Case Classification
**Description:** Automatically score and classify creators for each use case

**Classification Logic:**

**Consumer Research (Score: 0-100)**
- Audience size: 5K-100K (optimal), 1K-5K (acceptable), 100K+ (too large)
- Engagement rate: >5% (excellent), 3-5% (good), <3% (poor)
- Comment quality: High reply rate, detailed responses (manual sampling)
- Content type: Tutorial-focused (+20), review-focused (+10), vlog-style (-5)
- Production quality: Clear audio (+10), on-camera presence (+10)
- Location: US/Canada (+10), English-speaking countries (+5)

**Brand Partnerships (Score: 0-100)**
- Audience size: 50K-500K (optimal), 20K-50K (acceptable), 500K+ (premium)
- Engagement rate: >3% (excellent), 2-3% (good), <2% (poor)
- Brand alignment: Family-friendly content (+15), safety mentions (+10)
- Past sponsorships: Has sponsored content (+20), brand mentions (+10)
- Growth trajectory: >20% YoY (+15), 10-20% (+10), <10% (neutral)
- Content quality: High production value (+10), consistent posting (+10)
- Brand safety: No controversial content (+10), positive sentiment (+5)

**Audience Insights (Score: 0-100)**
- Content relevance: Lighting-focused (+20), home DIY (+15), general DIY (+10)
- Audience accessibility: Public analytics (+20), engaged comments (+10)
- Content diversity: Multiple project types (+10), beginner to advanced (+10)
- Consistency: 4+ videos/month (+10), 2-3 videos/month (+5)

**Outputs:**
- Classification scores per use case
- Rank-ordered lists per use case
- Qualification notes (why recommended/not recommended)
- Red flags (brand safety issues, fake engagement indicators)

---

#### 4. Aggregate Audience Analysis
**Description:** Combine data across multiple creators to understand niche demographics

**Analysis Components:**

**Demographics Aggregation:**
- Age distribution (weighted by audience size)
- Gender breakdown (weighted)
- Geographic heatmap (top cities, regions)
- Income proxies (homeownership mentions, property types shown)

**Psychographic Clustering:**
- Content preference analysis (video length, format, style)
- Skill level distribution (beginner, intermediate, advanced viewers)
- Pain point frequency analysis (most common problems mentioned)
- Interest graph (co-occurring topics: lighting + decor, lighting + organization)

**Media Behavior Patterns:**
- Platform preference strength (YouTube long-form vs. TikTok short-form engagement)
- Optimal content length per platform
- Peak engagement windows (day of week, time of day)
- Content format preferences (tutorial, review, inspiration, vlog)

**Processing:**
- Statistical aggregation across 50+ creator datasets
- Weighted averages by audience size
- Clustering algorithms for psychographic segments
- Visualization generation (charts, heatmaps, word clouds)

**Outputs:**
- Executive summary report (PDF)
- Interactive dashboard (Tableau/Looker)
- Audience persona cards (3-5 key segments)
- Insight briefs (top 10 findings)

---

#### 5. Reporting & Export
**Description:** Generate actionable reports tailored to each use case

**Report Types:**

**1. Creator Shortlist Report (Research Recruitment)**
- Top 20 creators ranked by research suitability
- 1-page profile per creator:
  - Headshot
  - Contact info (email, social handles)
  - Key metrics (followers, engagement rate, location)
  - Content sample (top 3 videos with links)
  - Qualification notes (why suitable for research)
  - Suggested outreach message template
- Export formats: PDF, CSV, Notion database

**2. Partnership Deck (Brand Sponsorships)**
- Top 10 creators ranked by partnership potential
- Media kit style layout:
  - Creator bio
  - Audience demographics
  - Engagement stats
  - Past partnerships (if available)
  - Campaign reach estimate
  - Cost benchmarks (CPM, estimated fee)
  - Recommended partnership type
- Export formats: PDF, PowerPoint, Google Slides

**3. Audience Insights Report (Market Understanding)**
- Executive summary (1-page key findings)
- Demographics deep-dive (charts, tables)
- Psychographic segments (persona cards)
- Media preferences analysis
- Content strategy recommendations
- Trend analysis (growing topics, emerging creators)
- Competitive landscape (adjacent niches)
- Export formats: PDF, Interactive dashboard link

---

## 🔐 Non-Functional Requirements

### Performance
- **Discovery Speed:** 100 creators in <60 minutes
- **API Rate Limits:** Stay within platform quotas (implement caching, batch requests)
- **Data Freshness:** Update creator metrics every 7 days
- **Scalability:** Support 1000+ creators in catalog without performance degradation

### Reliability
- **Uptime:** 99% availability for search and reporting features
- **Data Accuracy:** 95%+ accuracy on metrics (validated against platform native data)
- **Error Handling:** Graceful degradation if API limits hit (queue requests, notify user)

### Security & Privacy
- **API Keys:** Secure storage (environment variables, secrets manager)
- **Data Storage:** Encrypted at rest, secure database access
- **PII Handling:** Creator contact info (email) stored securely, GDPR compliant
- **Rate Limiting:** Respect platform TOS, implement exponential backoff

### Usability
- **Setup Time:** <10 minutes from launch to first results
- **Learning Curve:** Non-technical users can run full discovery in <30 min
- **Documentation:** Step-by-step guides for each use case
- **Error Messages:** Clear, actionable (e.g., "API quota exceeded, try again in 2 hours")

---

## 🛠️ Technical Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│  (CLI / Web Dashboard / API Endpoints)                  │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│              Creator Discovery Engine                    │
│  • Search orchestrator                                   │
│  • Multi-platform queries                                │
│  • Deduplication & merging                              │
└────────────────┬────────────────────────────────────────┘
                 │
     ┌───────────┼───────────┐
     │           │           │
┌────▼─────┐ ┌──▼──────┐ ┌──▼────────┐
│ YouTube  │ │ TikTok  │ │ Instagram │
│ API      │ │ API     │ │ API       │
│ Client   │ │ Client  │ │ Client    │
└──────────┘ └─────────┘ └───────────┘
     │           │           │
     └───────────┼───────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│           Profile Enrichment Pipeline                    │
│  • Content analysis (NLP)                                │
│  • Engagement metrics calculation                        │
│  • Audience insights extraction                          │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│         Use Case Classification Engine                   │
│  • Scoring algorithms (research, partnerships, insights) │
│  • Ranking & filtering                                   │
│  • Red flag detection                                    │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│            Reporting & Export Layer                      │
│  • Report generation (PDF, CSV, dashboards)              │
│  • Data visualization                                    │
│  • Export to external tools (Notion, Airtable)          │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│                  Data Storage                            │
│  • Creator profiles (PostgreSQL)                         │
│  • Metrics time-series (TimescaleDB / InfluxDB)         │
│  • Content cache (Redis)                                 │
│  • Reports archive (S3 / local files)                   │
└──────────────────────────────────────────────────────────┘
```

### Technology Stack (Proposed)

**Backend:**
- **Language:** Python 3.11+
- **Framework:** FastAPI (for API endpoints if needed)
- **Database:** PostgreSQL (creator profiles), Redis (caching)
- **Task Queue:** Celery (async API calls, batch processing)
- **APIs:**
  - `google-api-python-client` (YouTube Data API)
  - `TikTokApi` or custom (TikTok Research API)
  - `python-instagram` or custom (Instagram Graph API)

**Data Processing:**
- **NLP:** `spaCy` or `transformers` (content analysis, keyword extraction)
- **Data Analysis:** `pandas`, `numpy` (metrics aggregation)
- **Visualization:** `matplotlib`, `plotly` (charts for reports)

**Reporting:**
- **PDF Generation:** `reportlab` or `weasyprint`
- **CSV Export:** Built-in `csv` module
- **Dashboard:** Streamlit or Plotly Dash (optional interactive view)

**Deployment:**
- **Local:** Standalone Python scripts (like current project structure)
- **Cloud (Future):** Docker container, AWS Lambda (batch jobs)

---

## 📊 Data Model

### Creator Profile Schema

```json
{
  "creator_id": "uuid",
  "discovery_date": "2025-10-08T12:00:00Z",
  "last_updated": "2025-10-08T12:00:00Z",

  "basic_info": {
    "name": "Jane's DIY Workshop",
    "handle": "@janesdiy",
    "profile_url": "https://youtube.com/@janesdiy",
    "platform": "youtube",
    "verified": true,
    "bio": "DIY home improvement tutorials...",
    "location": "Austin, TX",
    "contact_email": "jane@example.com"
  },

  "channel_metrics": {
    "followers": 75000,
    "total_views": 5000000,
    "total_videos": 120,
    "join_date": "2020-01-15",
    "account_age_days": 1728,
    "post_frequency_per_month": 8,
    "growth_rate_30d": 0.05,
    "growth_rate_90d": 0.15,
    "growth_rate_1y": 0.30
  },

  "engagement_metrics": {
    "avg_views_per_video": 15000,
    "avg_likes_per_video": 800,
    "avg_comments_per_video": 120,
    "like_rate": 0.053,
    "comment_rate": 0.008,
    "engagement_rate": 0.061,
    "estimated_reach": 50000
  },

  "content_analysis": {
    "primary_topics": ["lighting", "LED installation", "home DIY"],
    "content_themes": ["tutorial", "product review", "beginner tips"],
    "avg_video_length_sec": 480,
    "most_popular_videos": [
      {
        "title": "Easy LED Strip Light Installation",
        "url": "https://...",
        "views": 250000,
        "published": "2024-06-15"
      }
    ],
    "hashtags": ["#diylighting", "#homeimprovement", "#ledlights"],
    "production_quality_score": 85
  },

  "audience_insights": {
    "age_distribution": {
      "18-24": 0.15,
      "25-34": 0.35,
      "35-44": 0.30,
      "45+": 0.20
    },
    "gender_distribution": {
      "female": 0.55,
      "male": 0.42,
      "other": 0.03
    },
    "top_locations": [
      {"country": "US", "percentage": 0.60},
      {"country": "Canada", "percentage": 0.15},
      {"country": "UK", "percentage": 0.10}
    ],
    "peak_engagement_hours": [18, 19, 20, 21]
  },

  "use_case_scores": {
    "consumer_research": {
      "score": 85,
      "rank": 5,
      "notes": "Great engagement, US-based, tutorial-focused",
      "red_flags": []
    },
    "brand_partnerships": {
      "score": 78,
      "rank": 12,
      "notes": "Good reach, past sponsorships visible",
      "red_flags": ["Growth slowing slightly"]
    },
    "audience_insights": {
      "score": 92,
      "rank": 2,
      "notes": "Diverse content, public analytics available",
      "red_flags": []
    }
  },

  "partnership_data": {
    "past_sponsors": ["Home Depot", "3M (Command Hooks)"],
    "brand_safety_score": 95,
    "estimated_cpm": 15.00,
    "estimated_campaign_cost": 5000
  }
}
```

---

## 🚀 Implementation Phases

### Phase 1: MVP - YouTube Discovery (Weeks 1-3)
**Goal:** Prove core functionality with single platform

**Deliverables:**
- YouTube API integration
- Basic creator search (keyword-based)
- Profile enrichment (channel metrics, recent videos)
- Simple scoring for consumer research use case
- CSV export of top 20 creators

**Success Criteria:**
- Find 100+ DIY lighting creators on YouTube in <60 min
- 90%+ relevance rate on manual review
- Team can recruit 5 creators for interviews using tool

### Phase 2: Multi-Platform + Classification (Weeks 4-6)
**Goal:** Expand to TikTok/Instagram, add use case classification

**Deliverables:**
- TikTok API integration
- Instagram API integration
- Cross-platform deduplication
- All 3 use case scoring algorithms
- Ranked lists per use case
- PDF report generation (research shortlist)

**Success Criteria:**
- Discover creators across 3 platforms
- Accurately classify 80%+ creators by use case
- Generate partnership deck for top 10 creators

### Phase 3: Audience Insights + Dashboard (Weeks 7-10)
**Goal:** Aggregate analysis, interactive reporting

**Deliverables:**
- Audience demographics aggregation (50+ creator sample)
- Psychographic clustering
- Interactive dashboard (Streamlit/Plotly Dash)
- Audience insights report generation
- Automated refresh (weekly cron job)

**Success Criteria:**
- Identify 3-5 audience segments with confidence
- Dashboard used by product team for strategy decisions
- Insights report informs campaign targeting

### Phase 4: Automation + Scale (Weeks 11-12)
**Goal:** Production-ready, scalable system

**Deliverables:**
- Batch processing pipeline (100+ creators in parallel)
- Data caching (reduce API costs)
- Scheduled updates (weekly refresh of metrics)
- API endpoints (integrate with other tools)
- Admin UI (manage queries, view history)

**Success Criteria:**
- Process 500+ creators without manual intervention
- API quota management (stay within free tiers)
- 99% uptime over 30 days

---

## 🎨 User Interface (Proposed)

### CLI Workflow (MVP)

```bash
# Phase 1: Discovery
python scripts/creator_discovery.py \
  --niche "DIY lighting projects" \
  --platform youtube \
  --min-followers 5000 \
  --max-followers 100000 \
  --location US \
  --output research_candidates.csv

# Phase 2: Classification
python scripts/classify_creators.py \
  --input research_candidates.csv \
  --use-case consumer_research \
  --output research_ranked.csv

# Phase 3: Report Generation
python scripts/generate_report.py \
  --input research_ranked.csv \
  --report-type research_shortlist \
  --output 3M_Research_Candidates.pdf
```

### Web Dashboard (Phase 3+)

**Home Screen:**
- Search bar: "Enter niche keywords"
- Platform toggles: [YouTube] [TikTok] [Instagram]
- Filters: Audience size, location, engagement rate
- Use case selector: Research / Partnerships / Insights
- [Search Creators] button

**Results View:**
- Creator cards (grid layout)
  - Profile pic, name, handle, platform
  - Key metrics: followers, engagement rate, score
  - [View Profile] [Add to Shortlist] buttons
- Sorting: By score, followers, engagement
- Filtering: By location, content type, growth rate

**Creator Detail Page:**
- Full profile (all metrics)
- Recent videos (thumbnails, titles, metrics)
- Audience demographics (charts)
- Use case scores (gauges)
- [Export to PDF] [Add to Campaign] buttons

**Reports Dashboard:**
- Saved reports list
- [Generate New Report] button
- Report types: Research Shortlist / Partnership Deck / Audience Insights
- Preview and download options

---

## 🧪 Testing & Validation

### Testing Strategy

**Unit Tests:**
- API client functions (mock responses)
- Scoring algorithms (test cases with known inputs)
- Data processing (metrics calculations)

**Integration Tests:**
- End-to-end discovery flow (sandbox API keys)
- Cross-platform deduplication
- Report generation (sample data)

**User Acceptance Testing:**
- Marketing team validates creator relevance (90%+ target)
- UX researchers test recruitment workflow
- Product managers review audience insights accuracy

**Performance Testing:**
- Benchmark API response times
- Load test with 500+ creator dataset
- Measure report generation time

---

## 🚧 Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **API quota limits exceeded** | High | Medium | Implement caching, batch requests, request queuing |
| **TikTok/Instagram API access denied** | High | Medium | Start with YouTube only (still valuable), explore web scraping fallback |
| **Data accuracy issues** | Medium | Medium | Validate against platform native analytics, manual spot checks |
| **Creator contact info unavailable** | Medium | High | Provide platform DM links, scrape from bio if public |
| **Low creator relevance** | High | Low | Refine keyword matching, add manual review step in Phase 1 |
| **Fake engagement detected** | Medium | Medium | Implement fraud detection (sudden spikes, bot-like patterns) |
| **GDPR/Privacy concerns** | Low | Low | Only collect public data, secure storage, allow creator opt-out |

---

## 💰 Cost Estimate

### Development Costs (Internal Time)
- **Phase 1:** 60 hours (1.5 weeks @ 40hr/wk)
- **Phase 2:** 80 hours (2 weeks)
- **Phase 3:** 120 hours (3 weeks)
- **Phase 4:** 80 hours (2 weeks)
- **Total:** 340 hours (~2 months development)

### API Costs (Recurring)
- **YouTube Data API:** Free tier (10,000 units/day) - $0/month (stay within quota)
- **TikTok Research API:** Free academic tier or $500/month business tier
- **Instagram Graph API:** Free (requires business accounts)
- **Total:** $0-$500/month depending on TikTok access

### Infrastructure Costs
- **Database (PostgreSQL):** Self-hosted or AWS RDS (~$20/month)
- **Storage (S3 for reports):** <$5/month
- **Compute:** Local execution (Phase 1-3), AWS Lambda if scaled (~$10/month)
- **Total:** $35-$535/month

---

## 📚 Appendices

### A. Example Niche Keywords (DIY Lighting)
- "DIY lighting projects"
- "home lighting installation"
- "LED strip lights tutorial"
- "accent lighting DIY"
- "under cabinet lighting"
- "smart lighting setup"
- "lighting hacks"
- "home improvement lighting"

### B. Platform API Documentation Links
- **YouTube Data API:** https://developers.google.com/youtube/v3
- **TikTok Research API:** https://developers.tiktok.com/products/research-api
- **Instagram Graph API:** https://developers.facebook.com/docs/instagram-api

### C. Sample Use Case Scoring Rubric

**Consumer Research Score = Base (100) + Adjustments**
- Audience size: 5K-100K (+0), 1K-5K (-10), 100K+ (-20)
- Engagement rate: >5% (+15), 3-5% (+10), <3% (-10)
- Content type: Tutorial (+20), Review (+10), Vlog (-5)
- Production quality: Clear audio (+10), On-camera (+10)
- Location: US/CA (+10), English-speaking (+5), Other (+0)
- Activity: Posted in last 30 days (+10), 90 days (+5), 180+ days (-10)

**Maximum Possible:** 100
**Minimum Possible:** 0

### D. Related Projects
- **Video Research Platform:** Existing module (YouTube video analysis with Whisper + LLaVA)
- **Consumer Interviews:** Upcoming module (post-recruitment interview analysis)
- **Campaign Tracking:** Future module (monitor creator partnerships over time)

---

## 🔄 Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 Draft | 2025-10-08 | Claude Code | Initial PRD creation based on client requirements |

---

## ✅ Approval & Sign-Off

**Document Status:** Draft - Awaiting Review

**Stakeholders:**
- [ ] Product Owner (approval)
- [ ] Engineering Lead (technical review)
- [ ] Marketing Manager (use case validation)
- [ ] UX Researcher (research workflow review)

**Next Steps:**
1. Review PRD with stakeholders
2. Refine requirements based on feedback
3. Prioritize Phase 1 features
4. Assign development resources
5. Set kickoff meeting for implementation

---

**END OF DOCUMENT**
