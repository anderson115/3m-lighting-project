# Category Intelligence Data Organization

**Last Updated**: October 26, 2025
**Project**: 3M Garage Organization Category Intelligence

---

## Data Structure Overview

```
category-intelligence/
├── data/                          # All raw and processed data
│   ├── retailers/                 # Retailer product data (consolidated)
│   │   ├── amazon_products.json
│   │   ├── walmart_products.json
│   │   ├── homedepot_products.json
│   │   ├── target_products.json
│   │   └── etsy_products.json
│   │
│   ├── youtube_videos/            # YouTube consumer video files
│   ├── youtube_audio/             # Extracted audio from YouTube
│   ├── youtube_transcripts/       # Whisper transcriptions (119 files)
│   ├── youtube_garage_consumer_insights.json
│   │
│   ├── tiktok_videos/             # TikTok consumer video files
│   ├── tiktok_audio/              # Extracted audio from TikTok
│   ├── tiktok_transcripts/        # Whisper transcriptions (231 files)
│   ├── tiktok_garage_consumer_insights.json
│   │
│   ├── teardown_videos/           # Product teardown/review videos
│   ├── teardown_audio/            # Extracted audio
│   ├── teardown_transcripts/      # Whisper transcriptions (221 files)
│   │
│   ├── bsr_tracking.db            # Amazon BSR tracking database
│   ├── garage_organizers_final_with_workbenches.json  # Master product dataset
│   ├── amazon_keywords.json       # Amazon keyword data
│   └── DATA_INVENTORY.json        # Complete data catalog
│
└── outputs/                       # All analysis results and reports
    ├── TEARDOWN ANALYSIS:
    │   ├── FINAL_TEARDOWN_REPORT.md
    │   ├── all_teardown_reports.json
    │   ├── additional_teardown_videos.json
    │   ├── curated_teardown_videos.json
    │   ├── teardown_videos_search_results.json
    │   └── teardown_reports/      # Individual product reports
    │
    ├── KEYWORD/LANGUAGE:
    │   ├── comprehensive_keyword_analysis_full.json
    │   ├── expert_keyword_strategic_report.json
    │   └── garage_keyword_language.json
    │
    ├── BSR/BESTSELLER:
    │   ├── bsr_complete_analysis.json
    │   ├── bsr_estimates_remaining.json
    │   └── top20_bestsellers_for_teardown.json
    │
    ├── TRENDS:
    │   └── emerging_trend_gap_analysis.json
    │
    └── REVIEWS:
        └── benefit_taxonomy_analysis.json
```

---

## Data Sources Summary

### Retailer Product Data
| Retailer   | Products | File Size | Coverage |
|------------|----------|-----------|----------|
| Amazon     | 514      | 433 KB    | Garage organizers |
| Walmart    | 8,218    | 8.9 MB    | Full category |
| Home Depot | 1,022    | 612 KB    | Full category |
| Target     | 430      | 332 KB    | Garage storage |
| Etsy       | 104      | 88 KB     | Artisan/custom |
| **TOTAL**  | **10,288** | **~10 MB** | - |

### Video Content Data
| Source              | Videos | Transcripts | Purpose |
|---------------------|--------|-------------|---------|
| Product Teardowns   | 0      | 221         | Technical R&D insights, materials, construction |
| YouTube Consumer    | 119    | 119         | Consumer language, jobs-to-be-done |
| TikTok Consumer     | 231    | 231         | Trending concerns, social proof |
| **TOTAL**           | **350** | **571**     | - |

---

## Key Data Files

### Master Product Dataset
**File**: `data/garage_organizers_final_with_workbenches.json`
**Size**: ~11.6 MB
**Products**: 12,929
**Sources**: Amazon, Walmart, Home Depot, Target, Etsy
**Coverage**: Hooks, shelving, cabinets, slatwall, workbenches, overhead storage

### BSR Tracking Database
**File**: `data/bsr_tracking.db` (SQLite)
**Size**: 180 KB
**Purpose**: Time-series Amazon Best Seller Rank tracking
**Tables**: `bsr_snapshots`, `products`
**Updates**: Periodic scraping for sales velocity estimation

### Keyword Intelligence
**File**: `data/amazon_keywords.json`
**Size**: 6.4 MB
**Keywords**: Amazon search terms, volumes, competitive density

---

## Analysis Outputs

### Teardown Analysis
**Primary Report**: `outputs/FINAL_TEARDOWN_REPORT.md`

**Key Findings**:
- 19 products analyzed from top 20 bestsellers
- 28,770 units/month market size
- Materials taxonomy: Steel (159 mentions), Magnets (141), Adhesives (46)
- Premium positioning opportunity for 3M

**Supporting Data**:
- `outputs/all_teardown_reports.json` - Individual product analyses
- `outputs/teardown_reports/` - Per-product detailed reports

### Keyword Analysis
**Files**:
- `comprehensive_keyword_analysis_full.json` - Full keyword strategy
- `expert_keyword_strategic_report.json` - Strategic recommendations
- `garage_keyword_language.json` - Consumer language patterns

### BSR Analysis
**Files**:
- `bsr_complete_analysis.json` - Complete bestseller rankings
- `top20_bestsellers_for_teardown.json` - Top products with sales estimates

### Trend Analysis
**File**: `emerging_trend_gap_analysis.json`
**Purpose**: Google Trends + Pinterest emerging product opportunities

### Review Analysis
**File**: `benefit_taxonomy_analysis.json`
**Purpose**: Consumer benefit classification from reviews

---

## Data Collection Methods

### Retailer Scraping
- **Tools**: Playwright, BeautifulSoup
- **Frequency**: On-demand batch collection
- **Storage**: JSON files in `data/retailers/`

### Video Collection & Transcription
- **Search**: yt-dlp for YouTube, Apify/BrightData for TikTok
- **Download**: Best audio format extraction
- **Transcription**: OpenAI Whisper (base model)
- **Quality**: 100% success rate with retry logic (3 attempts, 300s timeout)

### BSR Tracking
- **Method**: Periodic Amazon scraping
- **Storage**: SQLite database
- **Estimation**: Jungle Scout formula for sales velocity

---

## Data Quality Controls

### Video Curation Filters
1. **Duration**: Minimum 90 seconds for meaningful content
2. **Relevance**: Product-specific keyword matching
3. **Exclusions**: Pranks, fails, unrelated content
4. **Quality Tiers**:
   - High-value: Reviews, tests, installations, unboxings
   - Standard: General organization content

### Product Data Validation
- Price range validation
- BSR validation (1-999,999)
- Duplicate detection by ASIN/product ID
- Missing field imputation where possible

---

## Storage Conventions

### File Naming
- **Transcripts**: `{video_id}.txt`
- **Audio**: `{video_id}.wav`
- **Videos**: `{video_id}.mp4`
- **Reports**: Descriptive names with underscores

### JSON Schema Standards
- All products: `{asin, title, price, bsr, category, ...}`
- All videos: `{video_id, title, url, duration, view_count, ...}`
- All analysis: `{timestamp, data_sources, methodology, results, ...}`

---

## Data Maintenance

### Cleanup Performed
- ✅ Removed test directories (`*_test`)
- ✅ Consolidated retailer data to `data/retailers/`
- ✅ Created data inventory (`DATA_INVENTORY.json`)
- ✅ Organized outputs by analysis type

### Ongoing Maintenance
- Update `DATA_INVENTORY.json` after new data collection
- Archive old analysis outputs to timestamped folders
- Clean up temporary audio files after transcription

---

## Usage Guide

### Loading Master Product Dataset
```python
import json
from pathlib import Path

products = json.loads(
    Path("data/garage_organizers_final_with_workbenches.json").read_text()
)
print(f"Total products: {len(products)}")
```

### Accessing Transcripts
```python
from pathlib import Path

# Get all teardown transcripts
transcript_dir = Path("data/teardown_transcripts")
for transcript_file in transcript_dir.glob("*.txt"):
    text = transcript_file.read_text()
    print(f"{transcript_file.stem}: {len(text)} chars")
```

### Querying BSR Database
```python
import sqlite3

conn = sqlite3.connect("data/bsr_tracking.db")
cursor = conn.cursor()

# Get latest BSR for product
cursor.execute("""
    SELECT asin, bsr, timestamp
    FROM bsr_snapshots
    WHERE asin = ?
    ORDER BY timestamp DESC
    LIMIT 1
""", ("B0ABCD123",))
```

---

## Data Inventory

Full machine-readable inventory available at:
**`data/DATA_INVENTORY.json`**

Contains:
- Complete file manifest
- Record counts per data source
- Last update timestamps
- Data source metadata
