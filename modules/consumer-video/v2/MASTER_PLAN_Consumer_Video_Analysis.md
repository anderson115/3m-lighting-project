# 3M LIGHTING PROJECT: CONSUMER VIDEO ANALYSIS MASTER PLAN
**Version:** 2.0 Final Execution Plan  
**Date:** October 21, 2025  
**Platform:** Claude Code 4.5 + Mac Studio M3 (64GB RAM)  
**Project Status:** Ready for execution

---

## VIDEO FILE MANIFEST

**Source Location:** `/Volumes/Data/consulting/3m-lighting-consumer-videos/`

### Summary
- **Total Videos:** 82 raw consumer video files
- **Total Size:** 8.5GB
- **Participants:** 15 unique consumers
- **Date Range:** June 16-July 7, 2025
- **File Formats:** MOV (47), WEBM (21), MP4 (14)

### Directory Structure
```
/Volumes/Data/consulting/3m-lighting-consumer-videos/
├── Intro Videos/                    # Q1 introduction videos (14 files)
│   ├── AlanG_Q1_2025-06-23_092217_1.mov
│   ├── AlysonT_Q1_2025-06-23_021844_1.mov
│   ├── CarrieS_Q1_2025-06-22_033645_1.mov
│   ├── ChristianL_Q1_2025-06-17_065739_1.mp4
│   ├── DianaL_Q1_2025-06-16_031723_1.mov
│   ├── EllenB_Q1_2025-06-22_064429_1.mp4
│   ├── FarahN_Q1_2025-06-20_064419_1.mov
│   ├── FrederickK_Q1_2025-06-18_065110_1.mp4
│   ├── GeneK_Q1_2025-06-20_045554_1.mov
│   ├── MarkR_Q1_2025-06-17_020436_1.mov
│   ├── RachelL_Q1_2025-06-20_083945_1.MOV
│   ├── RobinL_Q1_2025-06-24_073537_1.mp4
│   ├── TiffanyO_Q1_2025-06-19_112125_1.mov
│   └── TylrD_Q1_2025-06-20_075938_1.mov
│   └── WilliamS_Q1_2025-06-16_052959_1.MOV
└── Intro Videos/core videos/        # Activity videos (68 files)
    └── [Activities 1-10 for each participant]
```

### Participant Video Count
| Participant | Video Count | Primary Format |
|------------|-------------|----------------|
| TylrD | 10 videos | .mov |
| MarkR | 10 videos | .mov |
| GeneK | 10 videos | .webm |
| FrederickK | 9 videos | .mp4 |
| WilliamS | 8 videos | .webm |
| FarahN | 8 videos | .MOV |
| ChristianL | 4 videos | .MOV/.mp4 |
| RobinL | 3 videos | .webm/.mp4 |
| RachelL | 3 videos | .MOV |
| EllenB | 3 videos | .mp4 |
| DianaL | 3 videos | .mov |
| CarrieS | 3 videos | .MOV |
| AlysonT | 3 videos | .webm/.mov |
| AlanG | 3 videos | .MOV/.mov |
| TiffanyO | 2 videos | .webm/.mov |

### Activity Categories Captured
- Activity 1: Introductions
- Activity 2: Your Style and Philosophy
- Activity 3: Project Motivation
- Activity 4: Sources of Inspiration
- Activity 5: Lighting Choices
- Activity 6: Step-by-Step Walkthrough
- Activity 7: Tools and Materials
- Activity 8: Pain Points
- Activity 9: Future Improvements
- Activity 10: Write a Letter

### File Naming Convention
`[ParticipantName]_[Activity]_[Date]_[Timestamp]_[Version].[ext]`

Example: `FarahN_Activity5LightingChoices_2025-07-02_080337_1.MOV`

### Processing Notes
- All video files located at `/Volumes/Data/consulting/3m-lighting-consumer-videos/`
- Copy relevant videos to `/Volumes/Data/consulting/3m-lighting-processed/raw_videos/` before processing
- Priority videos: Activities 5, 6, 7, 8, 9 (installation-focused content)
- Some participants have duplicate activity recordings (e.g., ChristianL_Activity9 has 2 versions)

---

## EXECUTIVE SUMMARY

**Objective:** Extract Jobs-to-Be-Done insights from 15 consumer lighting installation videos using multimodal analysis (visual + audio + transcript) with hybrid semantic-targeted methodology.

**Proven Stack:** Qwen2.5-VL-7B + Whisper Large-V3-Turbo + HuBERT-Large (validated via sample report: 5 interviews, 284s, 19 JTBD extracted)

**Timeline:** 3-5 days depending on processing tier selection

**Deliverables:**
1. Ranked pain points (top 5-7) with severity scores
2. Curated quotes library (15-20 highest-impact verbatims)
3. 3M adjacency map (Command/Scotch product touchpoints)
4. Golden moments documentation (success language)
5. Workaround inventory (compensating behaviors)

---

## PHASE 1: ENVIRONMENT SETUP & VALIDATION (Day 1)

### 1.1 Directory Structure Creation
```bash
/Volumes/DATA/consulting/3m-lighting-processed/
├── raw_videos/              # Consumer interview source files
├── processed/
│   ├── video_01/
│   │   ├── audio.wav
│   │   ├── frames/
│   │   ├── transcript.json
│   │   ├── visual_analysis.json
│   │   ├── emotion_analysis.json
│   │   └── synthesis.json
│   └── [video_02 through video_15]
├── outputs/
│   ├── final_synthesis_report.md
│   ├── pain_points_ranked.json
│   ├── quotes_library.json
│   ├── 3m_adjacency_map.json
│   ├── golden_moments.json
│   └── workarounds_inventory.json
└── logs/
    └── processing_log.txt
```

### 1.2 Model Installation & Testing
**Claude Code Tasks:**
1. Install dependencies: `transformers`, `torch`, `whisper`, `pyannote-audio`, `ffmpeg-python`, `librosa`
2. Download models to `/Volumes/TARS/llm-models/`:
   - Qwen2.5-VL-7B-Instruct (via Ollama)
   - Whisper Large-V3-Turbo
   - HuBERT-Large
3. Verify MPS backend compatibility for Mac M3
4. Run test pipeline with 1-minute sample video

**Success Criteria:** All three models process test video and output structured JSON

---

## PHASE 2: MULTIMODAL EXTRACTION PIPELINE (Days 2-3)

### 2.1 Video Preprocessing Module
**Inputs:** Raw MP4/MOV files from `/raw_videos/`

**Claude Code Implementation:**
```python
class VideoPreprocessor:
    def extract_audio(self, video_path):
        """Extract audio track → WAV (16kHz mono for Whisper)"""
        
    def sample_frames(self, video_path, interval=5):
        """Sample 1 frame per 5 seconds → JPEG sequence"""
        
    def generate_transcript(self, audio_path):
        """Whisper Large-V3-Turbo → timestamped JSON"""
        return {
            'segments': [
                {'start': 0.0, 'end': 5.2, 'text': '...'},
                ...
            ]
        }
```

**Outputs:**
- `audio.wav` (full extraction)
- `frames/frame_0000.jpg` through `frame_NNNN.jpg`
- `transcript.json` with word-level timestamps

---

### 2.2 Analysis Modules (Parallel Processing)

#### Module A: Visual Context Analyzer (Qwen2.5-VL)
**Semantic Detection (No Keyword Lists):**
```python
def analyze_visual_context(frames, metadata):
    """Extract behavioral signals without keyword matching"""
    
    prompt = f"""
    Analyze this lighting installation video frame sequence.
    
    Identify through visual observation:
    1. Product types shown (fixtures, adhesives, tools, surfaces)
    2. Installation methods and techniques
    3. Struggle indicators (fumbling, re-doing steps, improvisation)
    4. Environmental constraints (space, existing fixtures, surfaces)
    5. Workaround behaviors (tape usage, improvised mounts, pre-positioning)
    
    Output structured observations with confidence scores.
    """
    
    return {
        'products_shown': [],
        'struggle_moments': [],
        'workarounds_detected': [],
        'surface_contexts': [],
        'confidence_scores': {}
    }
```

**Key Capabilities Leveraged:**
- Object localization with bounding boxes
- Temporal event capture across frame sequence
- Context understanding (not just object detection)

---

#### Module B: Transcript Semantic Analyzer (Hybrid Approach)
**Primary Method: Semantic JTBD Extraction**
```python
def extract_jobs_from_transcript(transcript_segments):
    """Ulwick 8-step job mapping + compensating behavior detection"""
    
    job_categories = {
        'define': extract_goal_language(segments),      # Planning/intent expressions
        'locate': extract_resource_gathering(segments),  # "I needed to find..."
        'prepare': extract_setup_activities(segments),   # Pre-installation steps
        'confirm': extract_validation_patterns(segments), # "Made sure it was..."
        'execute': extract_task_performance(segments),   # Core installation
        'monitor': extract_progress_checks(segments),    # "Checking if..."
        'modify': extract_adjustment_language(segments), # "Had to redo..."
        'conclude': extract_completion_signals(segments) # Success/failure language
    }
    
    # Compensating behavior detection (workaround signals)
    workarounds = detect_compensating_behaviors(segments)
    
    return {
        'jobs_extracted': job_categories,
        'workarounds': workarounds,
        'pain_point_expressions': extract_frustration_language(segments),
        'satisfaction_expressions': extract_success_language(segments)
    }
```

**Targeted Validation (Secondary):**
- 3M product mentions: "Command", "Scotch", "tape", "adhesive", "strip"
- Pain point categories: electrical complexity, heat issues, adhesive failure, weight limits
- Golden moment triggers: "finally worked", "perfect", "exactly what I needed"

---

#### Module C: Audio Emotion Analyzer (HuBERT + Librosa)
**Prosodic Feature Extraction:**
```python
def analyze_emotional_context(audio_file, transcript_timestamps):
    """Detect frustration/satisfaction through audio signals"""
    
    # HuBERT emotion recognition
    emotions = hubert_emotion_classifier(audio_file)
    
    # Librosa prosodic analysis
    prosodic_features = {
        'pitch_variance': extract_pitch_variance(audio_file),
        'energy_levels': extract_energy(audio_file),
        'speech_rate': calculate_speech_rate(audio_file),
        'zero_crossing_rate': extract_zcr(audio_file)
    }
    
    # Align with transcript timestamps
    emotion_timeline = align_emotions_to_transcript(
        emotions, prosodic_features, transcript_timestamps
    )
    
    return {
        'frustration_peaks': identify_frustration_events(emotion_timeline),
        'satisfaction_moments': identify_relief_patterns(emotion_timeline),
        'emphasis_points': detect_vocal_emphasis(prosodic_features),
        'confidence_scores': calculate_confidence(emotion_timeline)
    }
```

**Output Example (From Sample Report):**
```json
{
    "timestamp": 5.3,
    "emotion": "frustration",
    "intensity": 0.80,
    "pitch_variance": 9025,
    "energy": 0.0540,
    "associated_text": "used tape that was sticky enough..."
}
```

---

### 2.3 Synthesis Engine (Multimodal Integration)
**Cross-Modal Alignment:**
```python
def synthesize_multimodal_insights(visual, transcript, audio):
    """Combine all three analyses into unified JTBD insights"""
    
    # Temporal alignment (±5 second window)
    aligned_events = []
    
    for timestamp in get_all_timestamps():
        window_data = {
            'visual': get_visual_context(timestamp, window=5),
            'transcript': get_transcript_segment(timestamp, window=5),
            'audio_emotion': get_emotion_at_time(timestamp, window=5)
        }
        
        # Pattern matching
        if (window_data['visual']['struggle_detected'] and 
            'frustration' in window_data['audio_emotion'] and
            contains_pain_language(window_data['transcript'])):
            
            aligned_events.append({
                'type': 'high_confidence_pain_point',
                'timestamp': timestamp,
                'visual_evidence': window_data['visual'],
                'verbatim': window_data['transcript']['text'],
                'emotion_intensity': window_data['audio_emotion']['intensity'],
                'confidence': calculate_multimodal_confidence(window_data)
            })
    
    return prioritize_and_categorize(aligned_events)
```

**Opportunity Scoring Algorithm:**
```
Severity Score = (Visual Evidence Weight × 0.3) + 
                 (Emotional Intensity × 0.4) + 
                 (Frequency Across Videos × 0.3)

Priority Ranking:
1. Multimodal-validated pain points (all 3 modalities agree)
2. Dual-validated insights (2 of 3 modalities)
3. Single-modality signals (lower confidence)
```

---

## PHASE 3: BATCH PROCESSING & VALIDATION (Day 3-4)

### 3.1 Orchestration Script
**Claude Code Implementation:**
```python
class VideoProcessingOrchestrator:
    def __init__(self, config):
        self.tier = config['processing_tier']  # FREE, PLUS, PRO
        self.confidence_threshold = config['confidence_threshold']
        self.priority_questions = config['priority_questions']
        
    def process_batch(self, video_directory):
        """Process all videos with resume capability"""
        
        videos = discover_videos(video_directory)
        progress_tracker = load_or_create_progress()
        
        for video_id, video_path in enumerate(videos):
            if progress_tracker.is_complete(video_id):
                continue  # Resume from last successful
                
            try:
                # Step 1: Preprocessing
                preprocessed = self.preprocess_video(video_path)
                
                # Step 2: Parallel analysis
                visual = self.analyze_visual(preprocessed['frames'])
                transcript = self.analyze_transcript(preprocessed['transcript'])
                audio = self.analyze_audio(preprocessed['audio'])
                
                # Step 3: Synthesis
                synthesis = self.synthesize_insights(visual, transcript, audio)
                
                # Step 4: Save intermediate results
                save_video_results(video_id, synthesis)
                progress_tracker.mark_complete(video_id)
                
            except Exception as e:
                log_error(video_id, e)
                continue  # Don't stop entire batch
        
        # Step 5: Cross-video aggregation
        return self.aggregate_all_videos()
```

---

### 3.2 Processing Tier Options

#### FREE Tier (Fully Local, Zero API Cost)
- **Visual:** Qwen2.5-VL-7B (local via Ollama)
- **Transcript:** Whisper + Claude Code built-in semantic analysis
- **Audio:** HuBERT-Large (local)
- **Synthesis:** Claude Code Sonnet 4.5 (local reasoning)
- **Speed:** ~6-8 min per 5-min video
- **Total Runtime:** ~2.5 hours for 15 videos

#### PLUS Tier (Hybrid)
- **Visual:** Claude Sonnet 4.5 API (superior context understanding)
- **Transcript:** Whisper + Claude Sonnet 4.5 API
- **Audio:** HuBERT (local)
- **Synthesis:** Claude Sonnet 4.5 API
- **Speed:** ~3-4 min per 5-min video
- **Total Runtime:** ~1.5 hours for 15 videos
- **Cost Estimate:** ~$15-25 for batch

#### PRO Tier (Maximum Quality)
- **Visual:** Claude Opus 4.1 API
- **Transcript:** Whisper + Claude Opus 4.1 API
- **Audio:** HuBERT + Opus 4.1 validation
- **Synthesis:** Claude Opus 4.1 API
- **Speed:** ~2-3 min per 5-min video
- **Total Runtime:** ~1 hour for 15 videos
- **Cost Estimate:** ~$40-60 for batch

**Tier Selection Config:**
```python
# config.py
PROCESSING_CONFIG = {
    'tier': 'PLUS',  # Options: FREE, PLUS, PRO
    'confidence_threshold': 0.75,
    'priority_questions': [3, 7, 8],  # From discussion guide
    'focus_areas': ['pain_points', '3m_adjacency', 'golden_moments', 'workarounds'],
    'emotion_sensitivity': 'high',  # low, medium, high
    'quote_preference': 'impactful'  # impactful vs representative
}
```

---

## PHASE 4: DELIVERABLE GENERATION (Day 5)

### 4.1 Final Synthesis Report Structure
**Automated Markdown Generation:**
```markdown
# 3M Consumer Lighting Insights Report
**Date:** [Auto-generated]  
**Sample:** 15 Consumer Interviews | [Total Duration] | Multimodal Analysis

## Executive Summary
[Auto-generated from top 3 pain points + primary barrier + environmental factor + user innovation]

## Critical Discoveries
[Highest severity pain points with multimodal evidence]

### Pain Point #1: [Auto-extracted title]
**Finding:** [Semantic description]  
**Evidence:**
- Visual: [What was observed in frames]
- Verbatim: "[Exact quote from transcript]"
- Emotion: [Frustration level + prosodic data]
- Frequency: [X of 15 participants]
- Confidence: [Multimodal validation score]

**Implication:** [3M opportunity statement]

## Key Insights with Multimodal Citations
[Organized by JTBD category: functional/social/emotional]

## Jobs-to-Be-Done Analysis
**Total Extracted:** [N jobs]  
**Category Distribution:** [Functional % | Social % | Emotional %]

[Table of jobs with confidence scores and participant attribution]

## 3M Adjacency Map
[Where Command/Scotch products currently appear + white space opportunities]

## Golden Moments
[Success language with functional/emotional/social outcomes]

## Workaround Inventory
[Compensating behaviors observed = unmet product needs]

## Strategic Recommendations
### Product Development
[Heat-resistant adhesive, battery kits, installation guides, etc.]

### Positioning & Messaging
[Region-specific, segment-specific messaging derived from jobs]

## Methodology
[Transparent documentation of multimodal analysis approach]
```

---

### 4.2 Structured Data Outputs

**pain_points_ranked.json:**
```json
{
  "pain_points": [
    {
      "rank": 1,
      "title": "Extreme Heat Adhesive Failure",
      "severity_score": 0.85,
      "frequency": "2 of 15 participants",
      "evidence": {
        "visual": ["Frame timestamps showing failure events"],
        "verbatim": "used tape that was sticky enough to stick...",
        "emotion_data": {
          "intensity": 0.80,
          "type": "frustration",
          "timestamp": 5.3
        }
      },
      "3m_opportunity": "Heat-resistant adhesive rated 100°F+ for Southwest markets"
    }
  ]
}
```

**quotes_library.json:**
```json
{
  "quotes": [
    {
      "text": "because I'm not an electrician and I don't necessarily know how...",
      "participant": "AlanG",
      "timestamp": 32.6,
      "context": "electrical_knowledge_barrier",
      "emotion": "uncertainty",
      "confidence": 0.70,
      "impact_score": 0.88,
      "related_job": "execute_installation_without_professional_help"
    }
  ]
}
```

---

## QUALITY ASSURANCE FRAMEWORK

### Confidence Scoring Methodology
```python
def calculate_confidence(data_point):
    """Multi-factor confidence scoring"""
    
    factors = {
        'multimodal_alignment': 0.0,  # Do visual + audio + transcript agree?
        'temporal_precision': 0.0,     # How tight is timestamp alignment?
        'quote_verification': 0.0,     # Does quote exist verbatim in transcript?
        'emotion_clarity': 0.0,        # How distinct is emotional signal?
        'cross_participant': 0.0       # Appears in multiple interviews?
    }
    
    # Weighted calculation
    confidence = (
        factors['multimodal_alignment'] * 0.35 +
        factors['temporal_precision'] * 0.20 +
        factors['quote_verification'] * 0.20 +
        factors['emotion_clarity'] * 0.15 +
        factors['cross_participant'] * 0.10
    )
    
    return confidence
```

### Validation Checkpoints
1. **Quote Integrity:** Every extracted quote verified against source transcript
2. **Timestamp Alignment:** Visual/audio/transcript events within ±5s window
3. **Emotion Validation:** HuBERT scores cross-checked with transcript sentiment
4. **JTBD Fidelity:** All jobs map to Ulwick 8-step framework categories
5. **3M Adjacency:** Product mentions verified through both visual and transcript
6. **No Hallucination:** Zero tolerance for fabricated data—flag low-confidence items

---

## EXECUTION WORKFLOW

### Day 1: Setup
```bash
# Claude Code command
claude code: "Initialize 3M consumer video analysis pipeline. 
Install Qwen2.5-VL, Whisper Large-V3-Turbo, HuBERT-Large. 
Create directory structure at /Volumes/DATA/consulting/3m-lighting-processed/. 
Test all models with sample video."
```

### Day 2-3: Pipeline Development
```bash
claude code: "Build multimodal analysis pipeline per master plan. 
Implement video preprocessor, three analysis modules, and synthesis engine. 
Test on single consumer video. 
Validate outputs match sample report structure."
```

### Day 3-4: Batch Processing
```bash
claude code: "Process all 15 consumer videos in /raw_videos/ using PLUS tier configuration. 
Run overnight batch processing. 
Generate intermediate JSON outputs for each video."
```

### Day 5: Report Generation
```bash
claude code: "Aggregate all video results. 
Generate final synthesis report following template structure. 
Output all deliverable files to /outputs/."
```

---

## RISK MITIGATION

### Technical Safeguards
| Risk | Mitigation | Recovery |
|------|-----------|----------|
| Model download failure | Retry with CDN mirrors | Manual download instructions |
| Video file corruption | Skip + flag in report | Manual review of source file |
| API quota exceeded (PLUS/PRO) | Auto-fallback to local processing | Continue with FREE tier |
| Out of memory | Batch size reduction | Process 5 videos at a time |
| Timestamp misalignment | ±5s tolerance window | Flag low-confidence events |
| Transcript errors | Confidence scoring filters | Manual review of <70% confidence |

### Data Integrity
- **Intermediate Saves:** Every video's results saved independently
- **Progress Tracking:** Resume capability prevents data loss
- **Error Logging:** Full stack traces for debugging
- **Validation Reports:** Auto-generated quality metrics per video

---

## SUCCESS CRITERIA

### Quantitative Metrics
- [ ] All 15 videos processed successfully
- [ ] Minimum 25 high-confidence pain points extracted
- [ ] 15-20 impactful quotes with >75% confidence
- [ ] All 19 JTBD categories represented (per sample)
- [ ] Minimum 5 multimodal-validated insights (visual+audio+transcript aligned)
- [ ] Zero fabricated data (100% quote verification pass rate)

### Qualitative Deliverables
- [ ] Final synthesis report matches sample structure
- [ ] 3M adjacency map identifies current product touchpoints + white space
- [ ] Golden moments documented with functional/emotional/social outcomes
- [ ] Workaround inventory shows compensating behaviors
- [ ] Strategic recommendations tied directly to JTBD insights

---

## APPENDIX A: SAMPLE OUTPUT VALIDATION

**Reference:** `consumervideosamplereport.pdf`
- 5 interviews, 284 seconds analyzed
- 19 JTBD extracted (100% functional category)
- 2 product mentions tracked
- 9 emotion events detected
- 2 critical discoveries flagged (electrical barrier, extreme heat adhesive)

**This Master Plan Must Replicate:**
- Multimodal citation format (visual + verbatim + emotion data)
- Confidence scoring transparency
- JTBD categorization methodology
- Strategic recommendation structure
- No hallucination—evidence-first approach

---

## APPENDIX B: TECHNICAL SPECIFICATIONS

**Hardware Requirements:**
- Mac Studio M3 (Apple Silicon)
- 64GB RAM minimum
- 200GB free storage (models + processing temp files)
- Stable internet (for PLUS/PRO tier API calls)

**Software Dependencies:**
- Python 3.10+
- PyTorch 2.0+ with MPS backend
- Transformers 4.35+
- Whisper (OpenAI)
- Librosa 0.10+
- ffmpeg 6.0+
- Ollama (for Qwen2.5-VL local deployment)

**Model Storage:**
- `/Volumes/TARS/llm-models/qwen2.5-vl-7b-instruct/`
- `/Volumes/TARS/llm-models/whisper-large-v3-turbo/`
- `/Volumes/TARS/llm-models/hubert-large/`

**Project Storage:**
- `/Volumes/DATA/consulting/3m-lighting-processed/`

---

## VERSION HISTORY

**v2.0 (October 21, 2025)** - Final execution plan
- Integrated sample report validation
- Added hybrid semantic-targeted methodology
- Defined three processing tiers
- Established confidence scoring framework
- Clarified directory structure and file locations

**v1.0 (October 20, 2025)** - Initial draft
- Original zero-keyword concept
- Preliminary pipeline design

---

**NEXT ACTION:** Execute Day 1 setup with Claude Code 4.5

**PLAN STATUS:** ✅ READY FOR EXECUTION
