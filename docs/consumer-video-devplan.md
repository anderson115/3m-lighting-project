**Context Remaining: ~73%**

---

# CONSUMER VIDEO ANALYSIS: DEVELOPMENT PLAN

**For:** Claude Code Sonnet 4.5 Execution  
**Date:** October 8, 2025  
**Scope:** Build pipeline to process 15 consumer lighting videos

---

## Claude Code Capabilities (As of Oct 2025)

**What Claude Code Sonnet 4.5 Can Do:**
- Write and execute Python scripts with full libraries (PyTorch, transformers, etc.)
- Install and configure local models (Qwen, Whisper, HuBERT)
- Process video/audio files through ffmpeg and Python
- Call APIs with proper error handling
- Manage multi-step workflows with state tracking
- Read/write files and organize outputs
- Run tests and validate results

**What This Means for Our Pipeline:**
Claude Code can build the entire system itself. We tell it what we want, it writes the code, tests it, and delivers working pipeline.

---

## Development Phases

### PHASE 1: Foundation (Day 1)
**Goal:** Get all models running and tested

**Claude Code Tasks:**
1. Install required packages (transformers, torch, whisper, pyannote, ffmpeg-python)
2. Download and test Qwen2.5-VL-7B-Instruct locally
3. Download and test Whisper Large-V3-Turbo
4. Download and test HuBERT-Large
5. Write test script that runs each model on sample files
6. Verify Mac M3 MPS backend works for all models

**Success Check:** Run 1-minute test video through each model, get outputs

---

### PHASE 2: Video Splitting (Day 1-2)
**Goal:** Break videos into analyzable parts

**Claude Code Tasks:**
1. Write script to extract audio track from video
2. Write script to sample video frames (1 per 5 seconds for efficiency)
3. Write script to generate transcript with Whisper (includes timestamps)
4. Create structured output format (JSON) for each video
5. Add progress tracking and error handling

**Success Check:** Process one full consumer video, get audio file + frames + transcript

---

### PHASE 3: Individual Analysis Modules (Day 2-3)
**Goal:** Build three separate analyzers

**Module 1: Visual Analyzer (Qwen2.5-VL)**
- Input: Video frames + context (this is from lighting installation video)
- Prompt: "Identify: products shown, installation methods, surfaces, tools, moments of struggle"
- Output: Structured list of visual observations with timestamps

**Module 2: Transcript Analyzer (Claude Code)**
- Input: Whisper transcript
- Prompt: "Extract: pain points mentioned, product names, workarounds described, outcome language, 3M product mentions"
- Output: Categorized findings with quotes and timestamps

**Module 3: Audio Emotion Analyzer (HuBERT)**
- Input: Raw audio file
- Process: Run emotion recognition model
- Output: Emotion intensity scores by segment (frustration, relief, pride, neutral)

**Claude Code Tasks:**
- Write Python class for each analyzer
- Each returns standardized JSON format
- Include confidence scores
- Add timestamp alignment across all three

**Success Check:** Run all three on same video, outputs align on timestamps

---

### PHASE 4: Synthesis Engine (Day 3-4)
**Goal:** Combine all three analyses into insights

**Claude Code Tasks:**
1. Write synthesis script that takes all three JSON outputs
2. Align findings by timestamp (e.g., visual shows adhesive + transcript says "kept falling" + audio shows frustration)
3. Score pain point severity (combines visual evidence + language intensity + emotion)
4. Extract quotes with context (what they said + what they were showing + how they felt)
5. Map findings to deliverable categories:
   - Pain points
   - 3M adjacency
   - Golden moments
   - Workarounds
   - Product mentions

**Success Check:** One video produces organized findings ready for report

---

### PHASE 5: Batch Processing (Day 4)
**Goal:** Process all 15 videos efficiently

**Claude Code Tasks:**
1. Write orchestration script that processes videos sequentially
2. Add resume capability (if crash, pick up where left off)
3. Create progress dashboard (shows X of 15 complete)
4. Save intermediate outputs for each video
5. Generate summary statistics (total quotes found, pain points by frequency, etc.)

**Success Check:** Run overnight, wake up to 15 processed videos

---

### PHASE 6: Report Generation (Day 5)
**Goal:** Auto-generate synthesis document

**Claude Code Tasks:**
1. Write script that aggregates all 15 video outputs
2. Rank pain points by: frequency + emotion intensity + visual evidence
3. Select best 15-20 quotes (highest impact + diverse themes)
4. Build 3M adjacency map (where products mentioned/shown)
5. Extract golden moment language (success state descriptions)
6. Create workaround inventory (compensating behaviors observed)
7. Generate markdown report matching deliverable structure

**Success Check:** Report includes all five required sections with real data

---

## Three-Tier Implementation

### Tier Selection Setup
Claude Code writes config file where client sets tier:
```python
# config.py
PROCESSING_TIER = "FREE"  # Options: FREE, PLUS, PRO
```

**FREE Tier (Fully Local):**
- All analysis modules use local models only
- Synthesis uses Claude Code's built-in reasoning
- No API calls, no cost

**PLUS Tier (Hybrid):**
- Visual: Call Claude Sonnet 4.5 API for frame interpretation
- Transcript: Call Claude Sonnet 4.5 API for deeper language analysis
- Audio: Keep local HuBERT
- Synthesis: Claude Sonnet 4.5 API

**PRO Tier (Maximum Quality):**
- Visual: Claude Opus 4.1 API for frame interpretation
- Transcript: Claude Opus 4.1 API for language analysis
- Audio: HuBERT + Claude Opus 4.1 validates emotion interpretation
- Synthesis: Claude Opus 4.1 API

**Claude Code Implementation:**
- Write API wrapper functions with retry logic
- Add cost tracking for PLUS/PRO tiers
- Graceful fallback if API fails (use local model)
- Log which tier was used for each video

---

## Quality Assurance Built-In

**Stability Features:**
- Every step saves intermediate files (never lose progress)
- If a module fails on one video, continue to next
- Final report flags any videos with partial data
- Logs all errors with context for debugging

**Accuracy Features:**
- Confidence scores on all findings (filter low-confidence later)
- Cross-validation: If visual + transcript + audio all agree, boost confidence
- Quote verification: Ensure extracted quotes exist in transcript exactly
- Timestamp alignment: Visual, audio, transcript must sync

**Nuance Features:**
- Audio emotion catches frustration words can't (sighs, pauses, tone)
- Visual catches workarounds not mentioned (product placement, improvisation)
- Synthesis identifies patterns across videos (8 of 15 used Command hooks)
- Context preservation: Keep 20 seconds before/after key moments

---

## Client Workflow

**Step 1: Setup (Claude Code does this)**
```bash
claude code: "Set up consumer video analysis pipeline for 15 videos. Use FREE tier configuration."
```
Claude Code installs everything, downloads models, creates folder structure.

**Step 2: Configure**
Client edits simple text file:
```
Priority questions: 3, 7, 8 (pain points and tools)
What matters most: 3M products, workarounds, pain points
Emotion sensitivity: High
Confidence threshold: 75%
Quote preference: Impactful
```

**Step 3: Run**
```bash
claude code: "Process all videos in /path/to/videos folder"
```
Claude Code runs pipeline overnight.

**Step 4: Review**
```bash
Open: final_synthesis_report.md
```
Report ready for copy-paste into client deliverable.

---

## Deliverables Claude Code Creates

**File Structure:**
```
/consumer_video_analysis/
  /raw_videos/           (client provides)
  /processed/
    /video_01/
      audio.wav
      frames/
      transcript.json
      visual_analysis.json
      emotion_analysis.json
      synthesis.json
    /video_02/
    ...
  /outputs/
    final_synthesis_report.md
    pain_points_ranked.json
    quotes_library.json
    3m_adjacency_map.json
    golden_moments.json
    workarounds_inventory.json
  /logs/
    processing_log.txt
```

**Key Files for Client:**
- `final_synthesis_report.md`: Ready for deliverable
- `quotes_library.json`: All quotes organized by theme
- `pain_points_ranked.json`: Severity-ranked list
- Processing log shows which tier was used, any issues

---

## Timeline

**If running FREE tier:** 5 days (mostly overnight processing)  
**If running PRO tier:** 3 days (faster API processing)

**Daily Breakdown:**
- Day 1: Claude Code builds foundation + video splitting
- Day 2-3: Analysis modules + synthesis engine
- Day 4: Batch process all videos overnight
- Day 5: Generate report, client review

---

## Risk Mitigation

**What Could Go Wrong:**
1. Model download fails → Claude Code retries with mirrors
2. Video file corrupt → Skip, flag in report
3. API quota hit (PLUS/PRO) → Auto-switch to local processing
4. Out of memory → Process videos in smaller batches
5. Timestamp misalignment → Visual tool detects and warns

**Built-In Safety:**
- Every step validates inputs before processing
- Intermediate saves mean never lose more than 1 video of work
- Logs capture everything for debugging
- Client can re-run any single video if needed

---

**Next Step:** Give Claude Code Sonnet 4.5 this development plan. It will build the entire pipeline autonomously and deliver working system in 3-5 days.