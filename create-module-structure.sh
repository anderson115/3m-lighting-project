#!/bin/bash
# Create standardized modular structure

echo "📦 Creating modular structure..."

# Create modules directory
mkdir -p modules

# Module 1: YouTube Data Source (move existing)
echo "  📁 Module 1: youtube-datasource"
mkdir -p modules/youtube-datasource/{scripts,data,config,docs,tests}

# Move existing youtube/social scripts and data
if [ -d "data/3m_lighting" ]; then
    mv data/3m_lighting modules/youtube-datasource/data/ 2>/dev/null || echo "    ℹ️  data already moved"
fi

# Copy shared scripts to module
cp scripts/multimodal_analyzer.py modules/youtube-datasource/scripts/ 2>/dev/null || true
cp scripts/run_preflight_analysis.py modules/youtube-datasource/scripts/ 2>/dev/null || true

# Create module README
cat > modules/youtube-datasource/README.md << 'YOUTUBE_README'
# YouTube Data Source Module

**Purpose:** Analyze YouTube videos for lighting installation pain points and solutions

## Structure
- `scripts/` - Analysis scripts (multimodal_analyzer.py, etc.)
- `data/` - Processed video data
- `config/` - Module-specific configuration
- `docs/` - Module documentation
- `tests/` - Unit tests

## Models Used
- Whisper large-v3 (transcription)
- LLaVA 7B (visual analysis)

## Status
✅ Production-ready (96% checkpoint success rate)
YOUTUBE_README

# Module 2: Consumer Video Analysis
echo "  📁 Module 2: consumer-video"
mkdir -p modules/consumer-video/{scripts,data/{raw_videos,processed,deliverables},prompts,config,docs,tests}

cat > modules/consumer-video/README.md << 'CONSUMER_README'
# Consumer Video Analysis Module

**Purpose:** Analyze consumer lighting installation interviews for pain points, emotions, and workarounds

## Structure
- `scripts/` - Analysis pipeline (consumer_analyzer.py, emotion_analyzer.py)
- `data/raw_videos/` - Source videos (gitignored)
- `data/processed/` - Per-video analysis outputs
- `data/deliverables/` - Final reports
- `prompts/` - Domain-specific extraction prompts
- `config/` - Module configuration
- `docs/` - Implementation plans and specifications
- `tests/` - Validation scripts

## Models Used
- Whisper large-v3 (transcription)
- LLaVA 7B (visual analysis)
- SpeechBrain wav2vec2 (emotion recognition)
- Librosa (prosodic features)

## Status
📋 Development plan ready (see docs/consumer-video-FINAL-PLAN.md)
CONSUMER_README

# Module 3: Creator Discovery (placeholder)
echo "  📁 Module 3: creator-discovery"
mkdir -p modules/creator-discovery/{scripts,data,config,docs,tests}

cat > modules/creator-discovery/README.md << 'CREATOR_README'
# Creator Discovery Module

**Purpose:** Discover and catalog creators on YouTube, TikTok, Instagram in lighting niche

## Structure
- `scripts/` - Discovery and profiling scripts
- `data/` - Creator databases and metrics
- `config/` - API keys and search parameters
- `docs/` - PRD and specifications
- `tests/` - Validation tests

## Status
📋 PRD complete (see docs/PRD-creator-discovery.md)
CREATOR_README

echo "✅ Module structure created"

# Create shared config symlinks
echo "🔗 Creating shared config links..."
ln -sf ../../../config/model_paths.yaml modules/youtube-datasource/config/model_paths.yaml 2>/dev/null || true
ln -sf ../../../config/model_paths.yaml modules/consumer-video/config/model_paths.yaml 2>/dev/null || true
ln -sf ../../../config/model_paths.yaml modules/creator-discovery/config/model_paths.yaml 2>/dev/null || true

echo "✅ Shared configs linked"
