# Social Video Collection - Quick Start Guide

**Version:** 1.0.0
**Date:** 2025-10-29

---

## Prerequisites

### Required Tools
```bash
# Install FFmpeg
brew install ffmpeg

# Install yt-dlp
brew install yt-dlp

# Check installations
ffmpeg -version
yt-dlp --version
ollama --version  # For LLaVA
```

### Python Dependencies
```bash
cd modules/social-video-collection
pip install -r requirements.txt

# Or install individually:
pip install apify-client yt-dlp librosa soundfile openai-whisper torch pyyaml
```

---

## Step 1: Configure Your Collection

### Option A: Use Existing Example (Garage Organizers)
```bash
cd modules/social-video-collection
cp config/examples/garage_organizers_tiktok.yaml config/collection_config.yaml
```

### Option B: Create Custom Configuration
```bash
# Copy template
cp config/collection_config.yaml config/my_category.yaml

# Edit with your keywords, hashtags, filters
nano config/my_category.yaml
```

**Key Configuration Sections:**
- `category`: Product category name
- `search_strategy.keywords`: Search terms
- `search_strategy.hashtags`: Relevant hashtags
- `filters`: Min views, duration limits
- `collection_target`: How many videos to collect

---

## Step 2: Set Up Secrets

### Using 1Password (Recommended)
```bash
# Secrets already configured in project .env.template
# Just run with op run:
op run --env-file=../../.env.template -- python scripts/run_collection.py
```

### Manual Setup
```bash
# Copy .env template
cp .env.example .env

# Edit with your API tokens
nano .env

# Add:
# APIFY_TOKEN=your_token_here
```

---

## Step 3: Test Run (10 Videos)

```bash
# Run test collection (small dataset)
cd modules/social-video-collection

# With 1Password
op run --env-file=../../.env.template -- \
  python scripts/run_collection.py \
  --config config/collection_config.yaml \
  --test

# Expected: ~1-2 hours for 10 videos
```

**What Happens:**
1. Searches TikTok for matching videos
2. Downloads first 10 videos
3. Transcribes audio with Whisper
4. Extracts frames and visual descriptions
5. Extracts audio features (pitch, energy, etc.)

**Output Location:**
```
data/processed/garage-organizers-tiktok/
├── videos/
│   ├── {video_id_1}/
│   │   ├── video.mp4
│   │   ├── metadata.json
│   │   ├── transcript.json
│   │   ├── audio_features.json
│   │   └── frames/
│   │       └── descriptions.json
│   └── ...
├── search_results.json
├── download_summary.json
├── transcription_summary.json
├── visual_extraction_summary.json
└── audio_features_summary.json
```

---

## Step 4: Review Test Data

### Check Data Quality
```bash
# List collected videos
ls -lh data/processed/*/videos/

# Check transcripts
cat data/processed/*/videos/*/transcript.json | jq '.full_text' | head

# Check visual descriptions
cat data/processed/*/videos/*/frames/descriptions.json | jq '.descriptions[0].description'

# Check audio features
cat data/processed/*/videos/*/audio_features.json | jq '.segments[0].features'
```

### Verify Data Completeness
```bash
# Count videos with complete data
cd data/processed/*/videos/
for dir in */; do
  echo "Checking $dir..."
  ls $dir/video.mp4 $dir/transcript.json $dir/audio_features.json $dir/frames/descriptions.json 2>/dev/null | wc -l
done
```

---

## Step 5: Run Full Collection (250+ Videos)

```bash
# Remove --test flag for full collection
op run --env-file=../../.env.template -- \
  python scripts/run_collection.py \
  --config config/collection_config.yaml

# Expected: ~16-32 hours for 250 videos
# Recommendation: Run overnight
```

### Monitor Progress
```bash
# In separate terminal, watch progress
watch -n 30 'ls data/processed/*/videos/ | wc -l'

# Check current processing step
tail -f data/processed/*/transcription_summary.json
```

---

## Step 6: Run Individual Steps (Optional)

If you need to re-run specific steps:

```bash
# Step 1: Search only
python scripts/01_search_videos.py --config config/collection_config.yaml

# Step 2: Download only
python scripts/02_download_videos.py

# Step 3: Transcribe only
python scripts/03_transcribe.py

# Step 4: Visual extraction only
python scripts/04_extract_visuals.py --frame-interval 3

# Step 5: Audio features only
python scripts/05_audio_features.py
```

---

## Troubleshooting

### Error: "APIFY_TOKEN not set"
```bash
# Ensure running with 1Password:
op run --env-file=../../.env.template -- python scripts/run_collection.py

# Or check .env file exists:
ls -la .env
```

### Error: "Whisper model not found"
```bash
# Model should be at: /Volumes/TARS/llm-models/whisper/large-v3.pt
ls -lh /Volumes/TARS/llm-models/whisper/large-v3.pt

# If missing, Whisper will auto-download (2.9GB)
```

### Error: "LLaVA not responding"
```bash
# Start Ollama service
ollama serve

# Verify LLaVA model
ollama list | grep llava
```

### Videos Failing to Download
```bash
# Check yt-dlp can access TikTok
yt-dlp --version
yt-dlp "https://www.tiktok.com/@username/video/1234567890123456789"

# Update yt-dlp if needed
brew upgrade yt-dlp
```

### Transcription Running Slow
```bash
# Check if using Metal acceleration
python -c "import torch; print('MPS available:', torch.backends.mps.is_available())"

# Expected: MPS available: True (on M1/M2/M3 Macs)
```

---

## Expected Processing Times

### Per Video (Average 30-60 second video)
- Search & Download: 10 seconds
- Transcription (Whisper): 3-6 minutes
- Visual Extraction: 30-60 seconds (10-20 frames)
- Audio Features: 10-20 seconds
- **Total: ~4-8 minutes per video**

### Full Collection (250 Videos)
- **Estimated Time: 16-32 hours**
- Recommendation: Run overnight or over weekend
- Cost: $0 (local models) + ~$5-10 Apify API usage

---

## Next Steps After Collection

1. **Validate Data Quality**
   - Check all videos have complete data
   - Verify transcripts are accurate
   - Review visual descriptions

2. **Feed to Analysis Module**
   - Use category-intelligence module
   - Agentic extraction of pain points, JTBD, product ideas
   - Generate consolidated reports

3. **Archive Raw Data**
   - Backup to external drive
   - Keep videos for future re-analysis
   - Document collection metadata

---

## Common Use Cases

### Use Case 1: Product Pain Points
```yaml
category: "LED strip lights"
keywords:
  - "LED strip not sticking"
  - "LED strip adhesive fail"
hashtags:
  - "#ledfail"
```

### Use Case 2: Installation Problems
```yaml
category: "garage hooks"
keywords:
  - "garage hooks fell off"
  - "command strips broken"
hashtags:
  - "#garagefail"
  - "#organizationfail"
```

### Use Case 3: Product Reviews (Negative)
```yaml
category: "smart lights"
keywords:
  - "smart bulb not connecting"
  - "smart light won't work"
hashtags:
  - "#smarthomefail"
```

---

## Tips for Best Results

### 1. Keyword Strategy
- Use **emotional triggers**: "fail", "broke", "frustrated"
- Combine with **product names**: "command strips broken"
- Include **action verbs**: "fell off", "won't stick", "doesn't work"

### 2. Hashtag Selection
- Use **failure hashtags**: #fail, #disaster, #broken
- Add **category tags**: #garageorganization, #homeimprovement
- Limit to **top 5** most relevant

### 3. Filters
- Set **min_views: 1000** (quality content)
- Set **min_likes: 50** (engagement filter)
- Duration **10-180 seconds** (avoid shorts and long videos)

### 4. Collection Size
- **Test run: 10 videos** (verify quality)
- **Pilot: 50 videos** (validate insights)
- **Full collection: 250+ videos** (comprehensive analysis)

---

**Questions?** See README.md for full documentation.
