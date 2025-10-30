# Brand Perceptions Module

**Map 3M brand portfolio strengths against garage organization category opportunities using consumer perception data.**

## Strategic Challenge

Create a repeatable, automated system that answers: *"Which 3M brands can credibly stretch into which garage organization innovations based on consumer perception data?"*

## Module Phases

### Phase 1: Brand Portfolio Scoping
- Identify 3M brands with garage organization relevance
- Filter by adhesive/mounting/organization heritage
- Output: Prioritized list of 5-8 brands with rationale

### Phase 2: Brand Perception Data Collection (THIS MODULE)
- **Target**: 200+ data points per brand across sources
- **Timeframe**: Last 18 months
- **Sources**: Reddit, YouTube, Amazon, TikTok/Instagram (free + $50 paid)

### Phase 3: Automated Perception Analysis
- Core perception extraction
- Love/hate clustering
- Brand elasticity mapping
- Garage category fit scoring (6 dimensions)

### Phase 4: Innovation Fit Matrix
- Match category opportunities × consumer jobs × brand strengths
- Score and rank innovation concepts

### Phase 5: Deliverable Automation
- Brand perception profiles
- Innovation recommendations matrix
- Strategic guardrails (green/yellow/red zones)

## Directory Structure

```
brand-perceptions/
├── config/
│   ├── examples/              # Example brand configs
│   └── brands.yaml           # Active brand list
├── scripts/
│   ├── collectors/           # Data collection scripts
│   ├── 01_scope_brands.py    # Phase 1: Brand portfolio scoping
│   ├── 02_collect_reddit.py  # Phase 2: Reddit data collection
│   ├── 03_collect_youtube.py # Phase 2: YouTube comments
│   ├── 04_collect_amazon.py  # Phase 2: Amazon reviews
│   └── 05_collect_social.py  # Phase 2: TikTok/Instagram
├── data/
│   ├── raw/                  # Raw scraped data by source
│   ├── processed/            # Cleaned & structured data
│   └── outputs/              # Analysis outputs
├── docs/
│   ├── COLLECTION_GUIDE.md   # Data collection protocols
│   └── API_SETUP.md          # API key setup instructions
└── tests/

```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys (if using paid sources)
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Run Brand Scoping
```bash
python scripts/01_scope_brands.py
```

### 4. Collect Perception Data
```bash
# Free sources (no API keys required)
python scripts/02_collect_reddit.py
python scripts/03_collect_youtube.py

# Paid sources (requires API keys in .env)
python scripts/04_collect_amazon.py
python scripts/05_collect_social.py
```

## Data Collection Parameters

- **Minimum per brand**: 200 data points
- **Timeframe**: Last 18 months
- **Focus queries**:
  - `[Brand] + garage`
  - `[Brand] + organization`
  - `[Brand] + storage`
  - `[Brand] + DIY`

## Budget

- **Free sources**: Reddit, YouTube, basic scraping
- **Paid sources**: $50 total (Bright Data + Apify)
- **Processing**: $0 (Claude Code local)

## Output Format

Each brand generates:
- `data/raw/{brand}/{source}/` - Raw scraped data
- `data/processed/{brand}/` - Cleaned perception data
- `data/outputs/{brand}_profile.json` - Structured analysis

## Module Performance Criteria

- **Scalability**: Process 8 brands in 24 hours
- **Repeatability**: Zero manual intervention after data collection
- **Stability**: 100% claims traceable to source data
- **Power**: 200+ verbatims per brand minimum
- **Nuance**: Multi-dimensional brand assessment

## Next Steps

1. Run `01_scope_brands.py` to generate brand list
2. Review `config/brands.yaml` and adjust priorities
3. Run collectors for each data source
4. Proceed to Phase 3 (analysis) in separate module
