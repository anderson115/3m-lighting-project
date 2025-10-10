# Social Signal Module

**Purpose:** Visual analysis of Pinterest, Instagram, TikTok, and social platforms to identify lighting trends, pain points, and consumer behavior through images and short-form content.

## Quick Start

```bash
# Scrape Pinterest boards
python scripts/pinterest_scraper.py --keyword "lighting installation"

# Analyze visual content
python scripts/visual_analyzer.py --input data/raw/pinterest_images/

# Extract social signals
python scripts/social_signal_extractor.py

# Generate trend report
python scripts/generate_social_report.py
```

## Module Structure

```
social-signal/
├── scripts/
│   ├── pinterest_scraper.py         # Pinterest board/pin scraper
│   ├── instagram_scraper.py         # Instagram post/reel collector
│   ├── visual_analyzer.py           # Image analysis (Qwen2.5-VL)
│   ├── trend_detector.py            # Identify viral patterns
│   ├── social_signal_extractor.py   # Extract pain points from visuals
│   └── generate_social_report.py    # Visual trend deliverable
├── data/
│   ├── raw/
│   │   ├── pinterest/               # Downloaded pins (images + metadata)
│   │   ├── instagram/               # Instagram posts (images + captions)
│   │   └── tiktok/                  # TikTok thumbnails + metadata
│   ├── processed/
│   │   ├── visual_analysis.json     # Per-image analysis results
│   │   ├── trend_clusters.json      # Grouped visual patterns
│   │   └── social_signals.json      # Extracted insights
│   └── deliverables/
│       └── Social_Trend_Report.html # Visual trend report
├── config/
│   ├── platforms.yaml               # Platform API configs
│   └── visual_keywords.yaml         # Image search keywords
├── docs/
│   └── SPECIFICATION.md             # Implementation specs
└── README.md                        # This file
```

## Target Platforms

### Primary Visual Sources
- **Pinterest** - DIY lighting boards, installation guides, aesthetic trends
- **Instagram** - #homelighting, #DIYlighting, before/after posts
- **TikTok** - Lighting hacks, installation tutorials, product reviews

### Secondary Sources
- **Houzz** - Professional lighting installations, design trends
- **YouTube Thumbnails** - Visual signals from DIY channels (metadata only)

## Analysis Pipeline

### Phase 1: Visual Collection
1. **Platform Scraping** - Download images + metadata (captions, engagement)
2. **Deduplication** - Remove duplicate/similar images (perceptual hash)
3. **Quality Filtering** - Remove ads, low-quality, irrelevant images

### Phase 2: Visual Analysis
4. **Image Analysis** - Qwen2.5-VL description (lighting fixtures, problems, context)
5. **OCR Extraction** - Text overlays, product names, instructions
6. **Object Detection** - Identify specific products, tools, materials

### Phase 3: Signal Extraction
7. **Trend Detection** - Cluster similar visual patterns (aesthetic styles, techniques)
8. **Pain Point Inference** - Before/after, DIY fails, workarounds visible
9. **Engagement Correlation** - Map high-engagement visuals to insights

### Phase 4: Synthesis
10. **Trend Clustering** - Group similar visual signals
11. **Social Proof Scoring** - Weight by saves, likes, shares
12. **Client Reporting** - Visual trend report with image examples

## Key Metrics

### Visual Signal Types
- **Aesthetic Trends** - Popular lighting styles (industrial, minimalist, RGB)
- **DIY Techniques** - Installation methods shown visually
- **Pain Point Indicators** - Visible failures, workarounds, frustrations
- **Product Appearances** - Brand visibility, user-generated content
- **Before/After** - Transformation documentation

### Engagement Metrics
- **Pinterest** - Saves, repins, comments
- **Instagram** - Likes, saves, shares, comments
- **TikTok** - Views, likes, shares, completion rate

## Output Files

### Raw Data (`data/raw/`)
- Platform-specific folders with images + metadata JSON
- Filename convention: `{platform}_{post_id}_{timestamp}.jpg`
- Metadata: caption, author, engagement, tags, timestamp

### Processed Insights (`data/processed/`)
- `visual_analysis.json` - Per-image Qwen2.5-VL analysis
- `trend_clusters.json` - Grouped visual patterns
- `social_signals.json` - Extracted pain points, solutions, trends

### Client Deliverables (`data/deliverables/`)
- `Social_Trend_Report.html` - Visual trend analysis with embedded images
- Top trends, viral patterns, consumer behavior insights

## Visual Analysis Approach

### Computer Vision Tasks
1. **Scene Understanding** - Room type, lighting context, installation stage
2. **Object Detection** - Fixtures, tools, products, materials
3. **Text Recognition** - Product labels, DIY instructions, annotations
4. **Quality Assessment** - Before/after comparison, installation success

### Signal Extraction
- **Explicit Signals** - Text overlays, captions, hashtags
- **Implicit Signals** - Visual pain points (tangled wires, visible adhesive, uneven lighting)
- **Emotional Signals** - Aesthetic satisfaction vs. frustration indicators

## Technical Stack

- **Scraping** - Playwright (Pinterest, Instagram), TikTok API
- **Vision Models** - Qwen2.5-VL (scene analysis), Tesseract OCR (text)
- **Deduplication** - Perceptual hashing (imagehash library)
- **Clustering** - CLIP embeddings + HDBSCAN for trend detection

## Status

📋 **Planning Stage** - Module scaffolded, implementation pending

## Scope & Constraints

### In Scope
- Static image analysis (Pinterest pins, Instagram photos)
- Text overlay extraction (DIY instructions, product names)
- Trend clustering based on visual similarity
- Engagement-weighted insight scoring

### Out of Scope
- Full video analysis (use consumer-video module for long-form)
- Real-time social listening (batch analysis only)
- Influencer relationship management (use creator-discovery)
- Paid ad content (organic only)

## Privacy & Ethics

- **Public Content Only** - No private accounts, DMs, or gated content
- **Attribution Preserved** - Original creator credited in citations
- **No Personal Data** - Aggregate trends only, no individual profiling
- **Terms of Service Compliant** - Respect platform rate limits, robots.txt

## Integration Points

### Synergy with Other Modules
- **consumer-video** - Visual thumbnails supplement video analysis
- **creator-discovery** - Social profiles inform creator database
- **expert-authority** - Pinterest/Instagram posts by verified experts

## Next Steps

1. Implement Pinterest scraper (Playwright-based)
2. Design visual trend clustering algorithm
3. Build Qwen2.5-VL batch analysis pipeline
4. Create visual report template with image embeds
5. Validate on 3M lighting hashtags
