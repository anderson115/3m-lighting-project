# Consumer Video Analysis Module

**Purpose:** Multimodal analysis of consumer lighting installation interviews extracting JTBD, product insights, emotions, and workarounds

## Version Information

This module has two implementations:

### Version 2.0 (Current - October 21, 2025) - **RECOMMENDED**
**Location:** `v2/` subdirectory

Complete methodology overhaul with integrated multimodal analysis pipeline:
- **Visual + Audio + Transcript** cross-modal synthesis
- **Qwen2.5-VL** for behavioral observation
- **HuBERT-Large** for emotional context
- **Whisper Large-V3-Turbo** for high-accuracy transcription
- **Confidence scoring** across all modalities
- **82 videos cataloged** with complete file manifest
- **Processing workspace:** `/Volumes/Data/consulting/3m-lighting-processed/`

📖 **See:** `v2/MASTER_PLAN_Consumer_Video_Analysis.md` for complete execution plan
📖 **See:** `v2/VERSION_HISTORY.md` for detailed v2 improvements

### Version 1.0 (October 6-20, 2025) - Legacy
**Location:** Main module directory (this folder)

Initial transcript-based implementation with basic JTBD extraction. Files and scripts in the main directory represent the v1 baseline analysis.

---

## v1 Quick Start (Legacy Implementation)

```bash
# Analyze single video
python scripts/consumer_analyzer.py path/to/video.mp4

# Batch analysis
python scripts/run_batch_5videos.py

# Generate client deliverables
python scripts/generate_compact_deliverable.py
python scripts/generate_multimodal_report.py
```

## Module Structure

```
consumer-video/
├── scripts/
│   ├── consumer_analyzer.py          # Main analysis pipeline
│   ├── emotion_analyzer.py           # Prosodic emotion detection
│   ├── jtbd_extractor.py             # Jobs-to-be-Done extraction
│   ├── product_tracker.py            # 3M product mention tracking
│   ├── workaround_detector.py        # Compensating behavior detection
│   ├── jtbd_emotion_mapper.py        # JTBD-emotion cross-mapping
│   ├── pattern_clusterer.py          # Cross-video pattern aggregation
│   ├── generate_compact_deliverable.py    # 2-page client report
│   ├── generate_multimodal_report.py      # Multimodal signal documentation
│   └── run_batch_5videos.py          # Batch processing script
├── data/
│   ├── raw_videos/                   # Source videos (gitignored)
│   ├── processed/                    # Per-video analysis outputs
│   │   ├── consumer01-05/            # Individual video results
│   │   ├── 3M_Consumer_Insights_Report_Compact.html
│   │   └── 3M_Consumer_Insights_Report_Multimodal.html
│   └── processed_baseline/           # Baseline comparison data
├── docs/
│   ├── ENHANCEMENT_SUMMARY.md        # Implementation specifications
│   └── BASELINE_VS_ENHANCED_COMPARISON.md
└── README.md                         # This file
```

## Analysis Pipeline

### Phase 1: Core Analysis
1. **Transcription** - Whisper large-v3 with word-level timestamps
2. **Visual Analysis** - Qwen2.5-VL frame analysis (30s intervals)
3. **Emotion Detection** - Librosa prosodic features (pitch, energy, rate)

### Phase 2: Enhanced Extraction
4. **JTBD Extraction** - Semantic pattern matching (functional/social/emotional)
5. **Product Tracking** - 3M product mentions with usage context
6. **Workaround Detection** - Intent→Barrier→Solution pattern identification

### Phase 3: Advanced Analytics
7. **JTBD-Emotion Mapping** - Cross-reference jobs with emotion events (±5s)
8. **Pattern Clustering** - Aggregate similar patterns across videos
9. **Client Deliverables** - Compact report + multimodal documentation

## Models & Technologies

- **Whisper large-v3** - Transcription with word-level timestamps
- **Qwen2.5-VL** - Visual frame analysis
- **Librosa** - Prosodic feature extraction
- **Semantic Regex** - Evidence-first pattern matching

## Output Files

### Per-Video Analysis (`data/processed/consumer0X/`)
- `analysis.json` - Complete analysis with all layers
- `frames/` - Extracted keyframes
- `audio/` - Extracted audio track

### Client Deliverables (`data/processed/`)
- `3M_Consumer_Insights_Report_Compact.html` - 2-page executive report
- `3M_Consumer_Insights_Report_Multimodal.html` - Multimodal signal documentation with embedded images

## Key Metrics (5-Video Baseline)

- **19 JTBD instances** (100% functional, 0 social/emotional)
- **2 Product mentions** (generic adhesive)
- **23 Emotion events** (9 high-confidence ≥0.7)
- **0 Workarounds detected** (patterns expanded, needs refinement)

## Critical Discoveries

1. **Arizona Extreme Heat** - Generic adhesive failing in high temperatures, consumer developed workaround technique
2. **Electrical Knowledge Barrier** - Non-electricians avoid hardwiring, drives battery-powered preference
3. **Evidence-First Methodology** - Zero false positives, novel patterns emerged naturally

## Evidence-First Principles

- **Extract → Validate → Categorize** (not Framework → Search → Force-fit)
- **Verbatim citations required** with timestamps
- **Confidence thresholds enforced** (JTBD ≥0.6, Products ≥0.7)
- **Anti-bias filters** (reject opinions, hypotheticals, about-others)
- **Context windows validated** (±30-45s for relevance)

## Status

✅ **Production Ready** - Phase 2 optimizations complete
- Core pipeline: Transcription + Visual + Emotion ✅
- Enhanced extraction: JTBD + Products + Workarounds ✅
- Advanced analytics: Emotion mapping + Clustering ✅
- Client deliverables: Compact + Multimodal reports ✅

## Documentation

- `docs/ENHANCEMENT_SUMMARY.md` - Full implementation specifications
- `docs/BASELINE_VS_ENHANCED_COMPARISON.md` - Performance analysis
