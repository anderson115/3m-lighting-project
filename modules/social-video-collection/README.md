# Social Video Collection Module

**Version:** 1.0.0
**Status:** Production Ready
**Purpose:** Platform-agnostic social video data collection pipeline

---

## Overview

The Social Video Collection Module is a reusable, stable data collection system designed to extract structured raw data from social media videos (TikTok, Instagram Reels, YouTube Shorts) for downstream agentic analysis.

### Key Principle: Separation of Concerns

**This Module:** Data collection ONLY (stable, deterministic, reusable)
**Analysis Module:** Insight extraction (agentic, flexible, client-specific)

---

## Features

### Data Collection Pipeline

1. **Video Discovery & Metadata** - Platform-specific search with Apify scrapers
2. **Video Download** - yt-dlp batch download with metadata preservation
3. **Transcription** - Whisper large-v3 (local) with timestamped segments
4. **Visual Extraction** - FFmpeg keyframe extraction + LLaVA neutral descriptions
5. **Audio Features** - Librosa prosodic feature extraction (pitch, energy, pauses)

### Key Characteristics

- **Zero Interpretation:** Collects raw data only, no insight extraction
- **Fully Timestamped:** All data points have precise timestamps
- **Citation-Ready:** Video IDs, sources, metadata preserved
- **Reusable:** Configurable per category, client, platform
- **Local-First:** Uses local models (Whisper, LLaVA) - $0 cost

---

## Technology Stack

### Local Models (Cost: $0)
- **Whisper large-v3** (`/Volumes/TARS/llm-models/whisper/`) - Audio transcription
- **LLaVA** (`/Volumes/TARS/llm-models/llava/`) - Visual frame descriptions
- **Librosa** (Python library) - Audio feature extraction

### External APIs
- **Apify** - TikTok/Instagram video scraping
- **yt-dlp** - Video download
- **FFmpeg** - Video/audio processing

---

## Installation

### Prerequisites
```bash
# Install FFmpeg (if not already installed)
brew install ffmpeg

# Install yt-dlp
brew install yt-dlp

# Python dependencies
pip install librosa soundfile yt-dlp apify-client
```

### Environment Setup
```bash
cd modules/social-video-collection
cp .env.example .env
# Edit .env with your Apify API token
```

---

## Configuration

### Category Configuration (`config/collection_config.yaml`)

```yaml
category: "garage organizers"
platform: "tiktok"
collection_target:
  min_videos: 250
  max_videos: 500

search_strategy:
  keywords:
    - "garage hooks fail"
    - "command strips broken"
    - "garage organization disaster"
  hashtags:
    - "#garagefail"
    - "#organizationfail"

filters:
  min_views: 1000
  has_audio: true
  language: "en"

output:
  data_dir: "data/processed/garage-organizers-tiktok"
```

---

## Usage

### Quick Start

```bash
# 1. Configure category
cd modules/social-video-collection
cp config/examples/garage_organizers.yaml config/collection_config.yaml

# 2. Run collection (with 1Password secrets)
op run --env-file=../../.env.template -- python scripts/run_collection.py

# 3. Check output
ls -lh data/processed/garage-organizers-tiktok/
```

### Full Pipeline

```bash
# Step 1: Search and download videos
python scripts/01_search_videos.py --config config/collection_config.yaml

# Step 2: Transcribe audio
python scripts/02_transcribe.py --config config/collection_config.yaml

# Step 3: Extract visual data
python scripts/03_extract_visuals.py --config config/collection_config.yaml

# Step 4: Extract audio features
python scripts/04_audio_features.py --config config/collection_config.yaml

# OR run full pipeline
python scripts/run_collection.py --config config/collection_config.yaml
```

---

## Output Structure

### Raw Data Format

```
data/processed/{category}-{platform}/
├── videos/
│   └── {video_id}/
│       ├── video.mp4              # Original video
│       ├── metadata.json          # Platform metadata
│       ├── transcript.json        # Whisper timestamped transcript
│       ├── audio_features.json    # Librosa prosodic features
│       └── frames/
│           ├── frame_0001.jpg
│           ├── frame_0002.jpg
│           └── descriptions.json  # LLaVA frame descriptions
└── collection_summary.json        # Collection metadata
```

### Example Output (`transcript.json`)

```json
{
  "video_id": "7234567890123456789",
  "language": "en",
  "duration": 47.3,
  "segments": [
    {
      "start": 0.0,
      "end": 3.2,
      "text": "So I tried these command strips for my garage hooks",
      "confidence": 0.94
    },
    {
      "start": 3.5,
      "end": 6.8,
      "text": "and they literally fell off the wall within 2 hours",
      "confidence": 0.96
    }
  ],
  "full_text": "So I tried these command strips..."
}
```

### Example Output (`audio_features.json`)

```json
{
  "video_id": "7234567890123456789",
  "segments": [
    {
      "start": 3.5,
      "end": 6.8,
      "text": "and they literally fell off the wall within 2 hours",
      "features": {
        "pitch_mean": 187.3,
        "pitch_variance": 1450.2,
        "energy": 0.067,
        "speech_rate": 3.2,
        "pause_before": 0.3,
        "has_fillers": false
      }
    }
  ]
}
```

---

## Performance

### Processing Time (Per Video)
- **Search & Download:** 5-10 seconds
- **Transcription (Whisper):** 3-6 minutes (depends on video length)
- **Visual Extraction:** 30-60 seconds
- **Audio Features:** 10-20 seconds
- **Total:** ~4-8 minutes per video

### Batch Processing (250 Videos)
- **Sequential:** ~16-32 hours
- **Recommended:** Overnight batch processing
- **Cost:** $0 (local models) + Apify API usage (~$5-10 for 250 videos)

---

## Module Architecture

### Design Principles

1. **Data Collection Only** - No insight extraction, no pattern analysis
2. **Fully Timestamped** - Everything has precise temporal markers
3. **Zero Interpretation** - LLaVA provides neutral descriptions, not analysis
4. **Citation-Ready** - All data traceable to source video + timestamp
5. **Reusable** - Configurable for any category/platform/client

### Comparison to Analysis Modules

| Module | Purpose | AI Usage | Output |
|--------|---------|----------|--------|
| social-video-collection | **Data collection** | Local models, neutral descriptions | Raw structured JSON |
| category-intelligence | **Insight extraction** | Agentic Claude, pattern detection | Strategic insights |
| consumer-video | **JTBD analysis** | Agentic Claude, pattern clustering | Jobs, pain points |

---

## Dependencies

### Python Packages
```txt
apify-client>=1.7.0
yt-dlp>=2023.11.0
librosa>=0.10.0
soundfile>=0.12.0
openai-whisper>=20231117
torch>=2.0.0
pyyaml>=6.0
```

### System Dependencies
- FFmpeg
- yt-dlp
- Ollama (for LLaVA)

---

## Configuration Examples

### Example 1: Garage Organizers (TikTok)
```yaml
category: "garage organizers"
platform: "tiktok"
search_strategy:
  keywords: ["garage hooks fail", "command strips broken"]
  hashtags: ["#garagefail"]
collection_target:
  min_videos: 250
```

### Example 2: LED Installation (YouTube Shorts)
```yaml
category: "LED strip installation"
platform: "youtube_shorts"
search_strategy:
  keywords: ["LED strip installation fail", "LED lights not sticking"]
collection_target:
  min_videos: 100
```

---

## Troubleshooting

### Error: Whisper model not found
```bash
# Download Whisper large-v3 to local models directory
# Already available at: /Volumes/TARS/llm-models/whisper/large-v3.pt
```

### Error: Apify API token not set
```bash
# Run with 1Password secret injection
op run --env-file=../../.env.template -- python scripts/run_collection.py
```

### Error: LLaVA not responding
```bash
# Start Ollama service
ollama serve
```

---

## Future Enhancements

- [ ] Instagram Reels support
- [ ] YouTube Shorts support
- [ ] Parallel processing (batch mode)
- [ ] Resume interrupted collections
- [ ] Incremental updates (avoid re-processing)

---

## Related Modules

- **category-intelligence** - Agentic analysis for market research
- **consumer-video** - JTBD extraction from interview videos
- **expert-authority** - Expert consensus pattern detection

---

## License

Proprietary - 3M Lighting Project

---

**Last Updated:** 2025-10-29
**Module Status:** ✅ Production Ready
