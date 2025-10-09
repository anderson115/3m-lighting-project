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
