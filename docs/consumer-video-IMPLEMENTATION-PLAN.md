# CONSUMER VIDEO ANALYSIS MODULE - IMPLEMENTATION PLAN

**For:** 3M Lighting Project - Consumer Interview Analysis
**Author:** Claude Code Sonnet 4.5
**Date:** 2025-10-08
**Status:** Ready for Implementation
**Confidence:** High (based on proven youtube-datasource patterns)

---

## 🎯 EXECUTIVE SUMMARY

### What We're Building
Automated analysis pipeline for 15 consumer lighting installation videos to extract:
1. **Pain Points** - Installation struggles, product failures, frustrations
2. **3M Adjacency** - Where 3M products mentioned/shown, opportunities
3. **Golden Moments** - Success language, satisfaction indicators
4. **Workarounds** - Improvised solutions, compensating behaviors
5. **Product Mentions** - What they used, how they described it

### Strategic Scope Decisions

**✅ SCOPED IN (High Confidence)**
- Reuse proven Whisper + LLaVA architecture (96% checkpoint test success)
- Adapt multimodal_analyzer.py patterns (validated stable)
- Local-first processing (FREE tier, $0 cost)
- Structured extraction with domain-specific prompts
- Cross-video aggregation for pattern detection

**⚠️ SCOPED WITH MODIFICATIONS**
- Emotion analysis: From transcript language only (no HuBERT - removed from project)
- Vision model: Use LLaVA 7B initially, upgrade to MiniCPM-V 8B if needed
- API tier: Optional PRO mode with Claude API for synthesis (not required for MVP)

**❌ SCOPED OUT (Complexity vs. Value)**
- Real-time processing (batch overnight is acceptable)
- Custom fine-tuned models (current models sufficient)
- Multi-language support (English only for MVP)
- Video editing/clipping features (analysis only)

---

## 🏗️ MODULE ARCHITECTURE

### Folder Structure
```
3m-lighting-project/
├── modules/
│   ├── youtube-datasource/          # ✅ EXISTING (proven stable)
│   │   ├── scripts/multimodal_analyzer.py
│   │   ├── data/3m_lighting/
│   │   └── config/model_paths.yaml (shared)
│   │
│   └── consumer-video/              # 🆕 NEW MODULE
│       ├── scripts/
│       │   ├── consumer_analyzer.py      # Adapted from multimodal_analyzer.py
│       │   ├── run_batch_analysis.py     # Process all 15 videos
│       │   ├── cross_video_synthesis.py  # Aggregate insights
│       │   └── generate_report.py        # Create deliverable markdown
│       │
│       ├── data/
│       │   ├── raw_videos/              # Client provides (gitignored)
│       │   ├── processed/               # Per-video JSON outputs
│       │   │   ├── video01/
│       │   │   │   ├── audio.wav
│       │   │   │   ├── frames/
│       │   │   │   ├── transcript.json
│       │   │   │   ├── visual_analysis.json
│       │   │   │   └── insights.json
│       │   │   └── ...
│       │   └── deliverables/            # Final client reports
│       │       ├── consumer_insights_report.md
│       │       ├── pain_points_ranked.json
│       │       └── quotes_library.json
│       │
│       ├── prompts/
│       │   ├── pain_point_extraction.txt
│       │   ├── 3m_adjacency_detection.txt
│       │   ├── visual_analysis_lighting.txt
│       │   └── synthesis_aggregate.txt
│       │
│       ├── config/
│       │   └── consumer_analysis_config.yaml
│       │
│       └── tests/
│           └── test_single_video.py
│
├── config/
│   └── model_paths.yaml              # SHARED CONFIG (both modules)
│
└── requirements.txt                   # SHARED DEPENDENCIES
```

### Code Reuse Strategy
1. **90% Reuse:** Copy `multimodal_analyzer.py` → `consumer_analyzer.py`
2. **10% Adapt:** Change prompts for consumer video domain
3. **New Components:** Synthesis + report generation (not in youtube module)

---

## 🚀 IMPLEMENTATION PHASES

### PHASE 1: Module Scaffolding (2-3 hours)
**Goal:** Create folder structure and validate 1 video end-to-end

**Tasks:**
```bash
# 1. Create module structure
mkdir -p modules/consumer-video/{scripts,data/{raw_videos,processed,deliverables},prompts,config,tests}

# 2. Copy and adapt analyzer
cp modules/youtube-datasource/scripts/multimodal_analyzer.py \
   modules/consumer-video/scripts/consumer_analyzer.py

# 3. Create test with 1 consumer video
# Use existing consumer-interviews data as starting point
```

**Deliverables:**
- ✅ Folder structure created
- ✅ consumer_analyzer.py functional (adapted from proven code)
- ✅ 1 test video processed successfully
- ✅ Output format validated

**Success Criteria:**
- Single video → audio extracted, transcribed, frames analyzed
- JSON outputs match expected schema
- No crashes, clean error handling

---

### PHASE 2: Domain-Specific Prompts (2-3 hours)
**Goal:** Optimize extraction for lighting installation domain

**Transcript Analysis Prompt:**
```
Role: You are analyzing a consumer interview about DIY lighting installation.

Extract the following from this transcript segment:

1. PAIN POINTS (struggles, failures, complaints)
   - Format: {"text": "exact quote", "timestamp": X, "severity": 1-5, "category": "adhesive|installation|cost|brightness|other"}
   - Look for: "didn't stick", "kept falling", "too dim", "hard to install", "waste of money"

2. 3M PRODUCT MENTIONS
   - Format: {"product": "name", "context": "positive|negative|neutral", "quote": "text", "timestamp": X}
   - Look for: Command Hooks, Command Strips, Scotch tape, 3M adhesive

3. WORKAROUNDS (improvised solutions)
   - Format: {"action": "what they did", "reason": "why", "timestamp": X}
   - Look for: "used double-sided tape instead", "propped it with books", "held it with wire"

4. SUCCESS LANGUAGE (satisfaction indicators)
   - Format: {"text": "exact quote", "timestamp": X, "intensity": 1-5}
   - Look for: "love it", "so much better", "exactly what I needed", "turned out great"

5. TECHNICAL DETAILS
   - Surfaces: drywall, tile, wood, glass, etc.
   - Tools: drill, screwdriver, level, etc.
   - Time mentioned: "took 20 minutes", "spent all day"

Return JSON only, no explanations.
```

**Visual Analysis Prompt (for LLaVA):**
```
Analyze this frame from a consumer lighting installation video.

Identify:

1. PRODUCTS VISIBLE
   - Lighting: LED strips, bulbs, fixtures (brand if visible)
   - Mounting: adhesive strips, screws, clips, brackets
   - 3M products: Command Hooks, strips, any 3M branding

2. INSTALLATION CONTEXT
   - Surface: wall/ceiling/under-cabinet/other
   - Room: kitchen/bedroom/garage/bathroom
   - Quality: professional/DIY/struggling

3. STRUGGLE INDICATORS
   - Damaged surface (holes, marks, torn paint)
   - Failed adhesive (products falling, peeling)
   - Temporary fixes (tape, objects propping things up)
   - Frustrated body language or gestures

4. SUCCESS INDICATORS
   - Clean installation (no damage)
   - Product functioning (lights on, properly mounted)
   - Satisfied expression or gesture
   - Finished/polished result

Output structured analysis with confidence 1-5 for each observation.
```

**Deliverables:**
- ✅ 4 prompt files created in `prompts/`
- ✅ consumer_analyzer.py uses new prompts
- ✅ Tested on 3 different videos
- ✅ Extraction quality validated (catches known pain points)

---

### PHASE 3: Batch Processing (3-4 hours)
**Goal:** Process all 15 videos reliably

**run_batch_analysis.py:**
```python
#!/usr/bin/env python3
"""
Process all consumer videos in batch.
Resumes from last successful video if interrupted.
"""

import json
from pathlib import Path
from consumer_analyzer import ConsumerAnalyzer

def process_all_videos(video_dir, output_dir):
    """Process all videos with progress tracking"""

    videos = sorted(video_dir.glob("*.mp4"))
    analyzer = ConsumerAnalyzer(video_dir, output_dir)

    results = []
    for i, video_path in enumerate(videos, 1):
        video_id = video_path.stem

        # Skip if already processed
        output_file = output_dir / video_id / "insights.json"
        if output_file.exists():
            print(f"[{i}/{len(videos)}] ✅ {video_id} (already processed)")
            continue

        print(f"[{i}/{len(videos)}] 🔄 Processing {video_id}...")

        try:
            result = analyzer.analyze_video(video_id)
            results.append({"video_id": video_id, "success": True})
            print(f"✅ {video_id} complete")
        except Exception as e:
            print(f"❌ {video_id} failed: {e}")
            results.append({"video_id": video_id, "success": False, "error": str(e)})
            continue  # Don't crash, process remaining videos

    # Save batch summary
    summary = {
        "total": len(videos),
        "successful": sum(1 for r in results if r["success"]),
        "failed": sum(1 for r in results if not r["success"]),
        "results": results
    }

    with open(output_dir / "batch_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    return summary

if __name__ == "__main__":
    video_dir = Path("modules/consumer-video/data/raw_videos")
    output_dir = Path("modules/consumer-video/data/processed")

    summary = process_all_videos(video_dir, output_dir)
    print(f"\n📊 Batch Complete: {summary['successful']}/{summary['total']} successful")
```

**Features:**
- Resume capability (skip already-processed videos)
- Error handling (one failure doesn't crash batch)
- Progress tracking
- Summary report

**Deliverables:**
- ✅ run_batch_analysis.py script
- ✅ Tested on 5 videos minimum
- ✅ Resume/skip logic validated
- ✅ Batch summary JSON generated

---

### PHASE 4: Cross-Video Synthesis (3-4 hours)
**Goal:** Aggregate insights across all 15 videos

**cross_video_synthesis.py:**
```python
#!/usr/bin/env python3
"""
Synthesize insights across all processed videos.
Find patterns, rank pain points, select best quotes.
"""

import json
from pathlib import Path
from collections import defaultdict

def aggregate_pain_points(processed_dir):
    """
    Collect all pain points from all videos.
    Rank by frequency + severity.
    """
    pain_points = []

    for video_dir in processed_dir.iterdir():
        if not video_dir.is_dir():
            continue

        insights_file = video_dir / "insights.json"
        if not insights_file.exists():
            continue

        with open(insights_file) as f:
            data = json.load(f)

        for pp in data.get("pain_points", []):
            pp["video_id"] = video_dir.name
            pain_points.append(pp)

    # Rank by frequency of similar pain points
    # Group by category and text similarity
    ranked = rank_by_importance(pain_points)

    return ranked

def aggregate_3m_mentions(processed_dir):
    """Find all 3M product mentions across videos"""
    mentions = defaultdict(list)

    for video_dir in processed_dir.iterdir():
        if not video_dir.is_dir():
            continue

        insights_file = video_dir / "insights.json"
        if not insights_file.exists():
            continue

        with open(insights_file) as f:
            data = json.load(f)

        for mention in data.get("3m_products", []):
            product = mention["product"]
            mentions[product].append({
                "video_id": video_dir.name,
                "context": mention["context"],
                "quote": mention["quote"]
            })

    return dict(mentions)

def select_best_quotes(processed_dir, max_quotes=20):
    """
    Select most impactful quotes across all videos.
    Criteria: high severity, clear language, diverse themes
    """
    all_quotes = []

    for video_dir in processed_dir.iterdir():
        if not video_dir.is_dir():
            continue

        insights_file = video_dir / "insights.json"
        if not insights_file.exists():
            continue

        with open(insights_file) as f:
            data = json.load(f)

        # Collect pain point quotes
        for pp in data.get("pain_points", []):
            all_quotes.append({
                "text": pp["text"],
                "video_id": video_dir.name,
                "type": "pain_point",
                "severity": pp.get("severity", 3),
                "category": pp.get("category", "other")
            })

        # Collect success quotes
        for success in data.get("success_language", []):
            all_quotes.append({
                "text": success["text"],
                "video_id": video_dir.name,
                "type": "success",
                "intensity": success.get("intensity", 3)
            })

    # Rank and select top quotes
    # Ensure diversity across categories
    selected = select_diverse_quotes(all_quotes, max_quotes)

    return selected

def synthesize_all(processed_dir, output_dir):
    """Generate all synthesis outputs"""

    synthesis = {
        "pain_points_ranked": aggregate_pain_points(processed_dir),
        "3m_adjacency_map": aggregate_3m_mentions(processed_dir),
        "golden_quotes": select_best_quotes(processed_dir),
        "workarounds_inventory": aggregate_workarounds(processed_dir),
        "summary_stats": calculate_summary_stats(processed_dir)
    }

    # Save individual files
    for key, data in synthesis.items():
        output_file = output_dir / f"{key}.json"
        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)

    return synthesis

if __name__ == "__main__":
    processed_dir = Path("modules/consumer-video/data/processed")
    output_dir = Path("modules/consumer-video/data/deliverables")
    output_dir.mkdir(exist_ok=True)

    synthesis = synthesize_all(processed_dir, output_dir)
    print("✅ Synthesis complete")
```

**Deliverables:**
- ✅ cross_video_synthesis.py script
- ✅ Aggregation logic for each insight type
- ✅ Ranking/scoring algorithms
- ✅ 5 JSON output files in deliverables/

---

### PHASE 5: Report Generation (2 hours)
**Goal:** Create markdown report ready for client

**generate_report.py:**
```python
#!/usr/bin/env python3
"""
Generate final client-ready markdown report.
"""

import json
from pathlib import Path
from datetime import datetime

def generate_markdown_report(deliverables_dir):
    """Create comprehensive markdown report"""

    # Load synthesis data
    pain_points = load_json(deliverables_dir / "pain_points_ranked.json")
    adjacency = load_json(deliverables_dir / "3m_adjacency_map.json")
    quotes = load_json(deliverables_dir / "golden_quotes.json")
    workarounds = load_json(deliverables_dir / "workarounds_inventory.json")
    stats = load_json(deliverables_dir / "summary_stats.json")

    report = f"""# Consumer Video Analysis Report
**3M Lighting Project - Consumer Insights**
**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Videos Analyzed:** {stats['total_videos']}

---

## Executive Summary

This report synthesizes insights from {stats['total_videos']} consumer lighting installation videos, identifying pain points, 3M product opportunities, and user workarounds.

**Key Findings:**
- {stats['total_pain_points']} pain points identified across {stats['pain_point_categories']} categories
- {stats['total_3m_mentions']} 3M product mentions ({stats['positive_mentions']} positive, {stats['negative_mentions']} negative)
- {stats['total_workarounds']} improvised workarounds observed

---

## 1. Top Pain Points (Ranked by Severity × Frequency)

{format_pain_points(pain_points[:15])}

---

## 2. 3M Adjacency Opportunities

{format_3m_adjacency(adjacency)}

---

## 3. Golden Moments (Success Language)

{format_golden_quotes(quotes['success'][:10])}

---

## 4. Workarounds & Compensating Behaviors

{format_workarounds(workarounds)}

---

## 5. Representative Quotes

{format_all_quotes(quotes[:20])}

---

## Appendix: Methodology

- **Transcription:** Whisper large-v3 (OpenAI)
- **Visual Analysis:** LLaVA 7B (local)
- **Processing Time:** {stats['total_processing_minutes']} minutes
- **Analysis Date:** {stats['analysis_date']}
"""

    # Save report
    report_file = deliverables_dir / "consumer_insights_report.md"
    with open(report_file, "w") as f:
        f.write(report)

    return report_file

if __name__ == "__main__":
    deliverables_dir = Path("modules/consumer-video/data/deliverables")
    report_file = generate_markdown_report(deliverables_dir)
    print(f"✅ Report generated: {report_file}")
```

**Deliverables:**
- ✅ generate_report.py script
- ✅ Markdown formatting helpers
- ✅ Final report generated
- ✅ Report validated (readable, complete, actionable)

---

## 🔧 CONFIGURATION FILES

### modules/consumer-video/config/consumer_analysis_config.yaml
```yaml
# Consumer Video Analysis Configuration

project:
  name: "3M Lighting Consumer Insights"
  client: "3M"
  analyst: "Claude Code Sonnet 4.5"

processing:
  frame_interval_seconds: 30  # Extract 1 frame per 30 seconds
  batch_size: 5  # Process 5 videos at a time
  resume_on_failure: true
  save_intermediate: true

models:
  tier: "FREE"  # FREE or PRO

  whisper:
    model_size: "large-v3"
    language: "en"
    device: "cpu"

  vision:
    model: "llava:latest"  # Via Ollama
    max_tokens: 2000
    temperature: 0.3  # Lower = more factual

extraction:
  pain_point_keywords:
    - "didn't work"
    - "kept falling"
    - "wouldn't stick"
    - "too dim"
    - "waste of money"
    - "frustrating"
    - "gave up"

  3m_product_names:
    - "Command Hook"
    - "Command Strip"
    - "Scotch"
    - "3M"
    - "VHB tape"

  success_keywords:
    - "love it"
    - "perfect"
    - "exactly what I needed"
    - "so much better"
    - "turned out great"

output:
  format: "json"
  include_confidence_scores: true
  min_confidence_threshold: 0.6
  max_quotes_per_video: 10
```

---

## 📊 IMPLEMENTATION TIMELINE

### Realistic Schedule (Based on Proven Patterns)

**Day 1 (6-8 hours total):**
- Morning: Phase 1 (Module scaffolding, 1 test video) - 3 hours
- Afternoon: Phase 2 (Domain prompts, test on 3 videos) - 3 hours
- Evening: Phase 3 start (Batch script, test on 5 videos) - 2 hours

**Day 2 (6-8 hours total):**
- Morning: Phase 3 complete (Run all 15 videos overnight ready) - 2 hours
- Afternoon: Phase 4 (Cross-video synthesis) - 4 hours
- Evening: Phase 5 (Report generation) - 2 hours

**Total:** 12-16 hours of focused development time

**If Running Overnight:**
- Day 1: Build pipeline, test on 5 videos
- Overnight: Process all 15 videos (2.5 hours unattended)
- Day 2: Synthesis + reporting (6 hours)

---

## ✅ SUCCESS CRITERIA

### Technical Validation
- ✅ All 15 videos processed without crashes
- ✅ Transcript accuracy >90% (spot-check 3 videos)
- ✅ Visual analysis detects products in frames
- ✅ Timestamps align across audio/visual
- ✅ JSON outputs valid and complete

### Quality Validation
- ✅ Report includes 15+ distinct pain points
- ✅ 3M products mentioned/shown are captured
- ✅ Quotes are exact (match transcript)
- ✅ Workarounds make sense (validated by human)
- ✅ Severity rankings seem reasonable

### Deliverable Validation
- ✅ consumer_insights_report.md is readable
- ✅ Client can understand findings without technical background
- ✅ Actionable insights (not just raw data)
- ✅ Processing took <3 hours total runtime

---

## 🚨 RISK MITIGATION

### Known Risks & Mitigations

**Risk:** Video audio quality poor (background noise, mumbling)
- **Mitigation:** Test Whisper on worst-case video first, flag low-confidence transcripts

**Risk:** Visual analysis misses products (off-camera, blurry)
- **Mitigation:** Rely more on transcript mentions, flag visual gaps

**Risk:** Consumer uses non-standard terminology
- **Mitigation:** Broad keyword matching, include "other" category

**Risk:** Processing takes longer than estimated
- **Mitigation:** Run overnight, batch resumable

**Risk:** Synthesis logic produces nonsense rankings
- **Mitigation:** Human spot-check top 10 pain points, adjust weights

---

## 🔄 ITERATION PLAN

### MVP → Production

**MVP (This Plan):**
- FREE tier only (local models)
- Rule-based synthesis
- Manual validation required

**V1.1 (If Needed):**
- Add PRO tier (Claude API for synthesis)
- Automated confidence scoring
- Comparative analysis (vs. competitor products)

**V1.2 (If Requested):**
- Upgrade to MiniCPM-V 8B for vision
- Fine-tune extraction prompts based on results
- Add video clipping (extract pain point moments)

**V2.0 (Future):**
- Real-time analysis UI
- Multi-language support
- Custom model fine-tuning

---

## 🎯 FINAL RECOMMENDATION

### Go/No-Go Assessment

**✅ GO - High Confidence**

**Reasons:**
1. **Proven Foundation:** 96% success on youtube-datasource checkpoint (5/5 videos)
2. **Code Reuse:** 90% of logic already working and tested
3. **Clear Scope:** Well-defined deliverables, no ambiguity
4. **Validated Models:** Whisper + LLaVA confirmed working on lighting domain
5. **Realistic Timeline:** 12-16 hours based on actual measured performance

**Expected Outcome:**
- Working pipeline in 2 days
- 15 videos processed successfully
- Client-ready report generated
- $0 cost (FREE tier)
- Reusable for future consumer video analysis

### Next Step
Create module structure and begin Phase 1.
