# 📹 Consumer Video Corpus Analysis & Processing Strategy

**Generated**: 2025-10-13
**Analyst**: Claude Code
**Purpose**: Preflight analysis and chunking recommendations for full video corpus processing

---

## 📊 **VIDEO CORPUS INVENTORY**

### **Total Videos**: 82 processable videos
- **15 Intro Videos** (participant introductions)
- **67 Core Activity Videos** (10 activity types across participants)
- **Location**: `/Volumes/DATA/consulting/3m-lighting-consumer-videos/`

### **Participants**: 15 lighting enthusiasts
- AlanG, AlysonT, CarrieS, ChristianL, DianaL
- EllenB, FarahN, FrederickK, GeneK, MarkR
- RachelL, RobinL, TiffanyO, TylrD, WilliamS

### **Storage Analysis**
- **Intro Videos**: ~2.5 GB (15 files, avg 163 MB)
- **Core Activity Videos**: ~5.9 GB (67 files, avg 88 MB)
- **Total Source**: ~8.4 GB raw video
- **Estimated Output**: ~6 GB processed data (transcripts, frames, analysis)

---

## 🎯 **ACTIVITY TYPE BREAKDOWN**

### **High-Value Activities** (Critical for JTBD)
| Activity | Videos | Participants | Priority |
|----------|--------|--------------|----------|
| **Activity 8: Pain Points** | 13 | 13/15 | 🔴 CRITICAL |
| **Activity 9: Future Improvements** | 14 | 14/15 | 🔴 CRITICAL |
| Activity 6: Step-by-Step Walkthrough | 9 | 9/15 | 🟠 HIGH |
| Activity 5: Lighting Choices | 9 | 9/15 | 🟠 HIGH |

### **Context Activities** (Supporting insights)
| Activity | Videos | Participants | Priority |
|----------|--------|--------------|----------|
| Activity 1: Introductions | 8 | 8/15 | 🟡 MEDIUM |
| Activity 2: Style & Philosophy | 8 | 8/15 | 🟡 MEDIUM |
| Activity 3: Project Motivation | 8 | 8/15 | 🟡 MEDIUM |
| Activity 4: Sources of Inspiration | 7 | 7/15 | 🟢 LOW |
| Activity 7: Tools and Materials | 4 | 4/15 | 🟢 LOW |
| Activity 10: Write a letter | 2 | 2/15 | 🟢 LOW |

### **Notable Gaps**
- **TiffanyO**: Only has Activity 9 video (no Activity 8)
- **FrederickK**: Missing Activity 8, but has comprehensive set otherwise
- **Most Complete**: MarkR (10 activities), TylrD (10 activities), GeneK (9 activities)

---

## ⚙️ **SYSTEM READINESS CHECK**

### ✅ **Hardware Capabilities**
```
CPU:        12 cores (M2 Ultra equivalent)
RAM:        64 GB (22.4 GB available)
Storage:    13 GB free (local), 217 GB free (external)
Platform:   macOS 25.0.0 with Python 3.13.5
```

**Verdict**: ✅ **READY** - System can handle parallel processing (4+ videos simultaneously)

### ✅ **Software Stack**
```
Whisper:    large-v3 (fastest-whisper implementation)
Vision:     Qwen2.5-VL multimodal LLM
Emotion:    Librosa FREE tier (fast audio analysis)
JTBD:       Evidence-first extraction (no paid APIs)
```

**Verdict**: ✅ **READY** - All dependencies tested with 5-video sample

### ⚠️ **Resource Constraints**
```
Disk Space: 13 GB local (TIGHT - need 6GB for outputs)
Processing: ~20 hours sequential, ~5 hours parallel (4x)
```

**Recommendation**: Write outputs to external drive to conserve local space

---

## 🎬 **PROCESSING TIME ESTIMATES**

### **Per-Video Breakdown**
| Component | Time | Notes |
|-----------|------|-------|
| Whisper Transcription | ~10 min | 5min video × 2min/min ratio |
| Emotion Analysis | ~0.5 min | Librosa is fast |
| JTBD Extraction | ~1 min | Pattern matching |
| **Total per video** | **~11.5 min** | Conservative estimate |

### **Full Corpus Estimates**
| Strategy | Time | Feasibility |
|----------|------|-------------|
| Sequential (1 at a time) | ~20.7 hours | ⏰ Overnight + day |
| Parallel 2x | ~10.4 hours | 🟡 Workday |
| Parallel 4x | ~5.2 hours | 🟢 Half day |
| Parallel 8x | ~2.6 hours | ⚡ Fastest (may strain system) |

**Recommended**: **4x parallel processing** (~5 hours)

---

## 🎯 **RECOMMENDED CHUNKING STRATEGIES**

### **OPTION 1: Priority-Based (RECOMMENDED)**
**Best for**: Getting insights ASAP

#### **Chunk 1: Critical JTBD Videos** (~3 hours)
```
Activity 8 (Pain Points): 13 videos
Activity 9 (Future Improvements): 14 videos
Total: 27 videos × 11.5min = 5.2 hours sequential, 1.3 hours parallel (4x)
```

**Why first**: These videos contain the richest JTBD insights (pain points + solutions)

#### **Chunk 2: High-Value Context** (~2.5 hours)
```
Activity 5 (Lighting Choices): 9 videos
Activity 6 (Walkthrough): 9 videos
Total: 18 videos × 11.5min = 3.5 hours sequential, 0.9 hours parallel (4x)
```

**Why second**: Provides context for what users chose and how they implemented

#### **Chunk 3: Participant Introductions** (~3 hours)
```
Intro Videos: 15 videos (all participants)
Total: 15 videos × 11.5min = 2.9 hours sequential, 0.7 hours parallel (4x)
```

**Why third**: Establishes participant profiles and motivations

#### **Chunk 4: Supporting Context** (~4 hours)
```
Activities 1-4, 7, 10: 22 videos
Total: 22 videos × 11.5min = 4.2 hours sequential, 1.1 hours parallel (4x)
```

**Why last**: Nice-to-have context, lower priority for JTBD analysis

**Total Time (4x parallel)**: ~7 hours spread across 4 sessions

---

### **OPTION 2: Participant-Based**
**Best for**: Understanding individual user journeys

#### **Chunk by completeness**:
1. **Most Complete** (MarkR, TylrD, GeneK, FarahN, FrederickK, WilliamS): 6 participants × ~8 videos = 48 videos
2. **Moderate** (CarrieS, DianaL, EllenB, AlanG, AlysonT): 5 participants × ~3 videos = 15 videos
3. **Minimal** (ChristianL, RachelL, RobinL, TiffanyO): 4 participants × ~3 videos = 12 videos

**Pros**: Complete user stories, easier to spot patterns per person
**Cons**: Delays cross-participant insights until later chunks

---

### **OPTION 3: Time-Based**
**Best for**: Consistent progress tracking

#### **Process in batches of 20 videos** (~4 hours each):
- Batch 1: 20 videos (4 hours parallel)
- Batch 2: 20 videos (4 hours parallel)
- Batch 3: 20 videos (4 hours parallel)
- Batch 4: 22 videos (4.5 hours parallel)

**Pros**: Predictable scheduling, easy to pause/resume
**Cons**: No thematic coherence, harder to generate interim reports

---

## 🚀 **RECOMMENDED PROCESSING PLAN**

### **Phase 1: Quick Wins** (Day 1 - 3 hours)
```bash
# Process Activity 8 + Activity 9 (27 videos)
# JTBD gold mine: pain points + desired improvements
Runtime: ~1.5 hours (4x parallel)
Output: Initial JTBD insights report
```

### **Phase 2: Context** (Day 2 - 2 hours)
```bash
# Process Activity 5 + Activity 6 (18 videos)
# Understand what they chose and how they implemented
Runtime: ~1 hour (4x parallel)
Output: Product choices and implementation insights
```

### **Phase 3: Profiles** (Day 2 - 1 hour)
```bash
# Process all Intro videos (15 videos)
# Build participant profiles
Runtime: ~45 min (4x parallel)
Output: Participant segmentation
```

### **Phase 4: Complete Picture** (Day 3 - 1 hour)
```bash
# Process remaining activities (22 videos)
# Fill in gaps for comprehensive analysis
Runtime: ~1 hour (4x parallel)
Output: Final comprehensive report
```

**Total Time**: ~5.5 hours active processing across 3 days
**Cost**: $0 (all FREE tier models)

---

## ⚠️ **RISK MITIGATION**

### **Disk Space Management**
```bash
# Write outputs to external drive
OUTPUT_DIR="/Volumes/DATA/consulting/3m-lighting-processed/"

# Enable incremental processing (save after each video)
# Allows resume if process interrupted
```

### **Error Handling**
```python
# Skip videos that fail (don't block entire batch)
# Log failures for manual review
# Continue processing remaining videos
```

### **Quality Assurance**
```bash
# After each chunk, generate quick stats:
# - Videos processed
# - JTBDs extracted
# - Pain points identified
# - Products mentioned
```

---

## 📋 **PREFLIGHT CHECKLIST**

### **Before Processing**
- [ ] External drive mounted and accessible
- [ ] 217 GB free space on external drive (verified ✅)
- [ ] Python venv activated
- [ ] Whisper large-v3 model downloaded
- [ ] LM Studio running (if using local LLM)
- [ ] Output directory created on external drive

### **Configuration Changes Needed**
- [ ] Update video_dir path to point to external drive
- [ ] Update output_dir to write to external drive (preserve local space)
- [ ] Modify batch script to process by activity type
- [ ] Add resume capability (checkpoint after each video)

### **Post-Processing**
- [ ] Generate interim report after Chunk 1 (Activity 8+9)
- [ ] Review JTBD patterns before proceeding
- [ ] Adjust priorities if needed based on early insights

---

## 📊 **EXPECTED INSIGHTS OUTPUT**

### **From Activity 8 (Pain Points)** - 13 videos
- 30-50 distinct pain points
- Workaround patterns (Intent → Barrier → Solution)
- Emotion mapping (frustration peaks)
- Product failure modes

### **From Activity 9 (Future Improvements)** - 14 videos
- 40-60 desired improvements
- Unmet JTBD categories (functional/social/emotional)
- Feature wishlists
- Competitive product mentions

### **Cross-Activity Patterns**
- JTBD clusters across all participants
- 3M product mentions with context
- Emotion-JTBD correlations
- Market opportunity gaps

---

## 🎯 **FINAL RECOMMENDATION**

**Use OPTION 1: Priority-Based Chunking**

**Rationale**:
1. **Fastest Time-to-Insights**: Get critical JTBD data in 1.5 hours
2. **Resource Efficient**: Can process chunks when system is idle
3. **Actionable Interim Reports**: Generate insights after each chunk
4. **Low Risk**: Start with highest-value data first
5. **Flexible**: Can stop after Chunk 2 if insights are sufficient

**Next Steps**:
1. Create batch processing script for Activity 8+9 videos
2. Configure output to external drive
3. Run Chunk 1 (27 videos, ~1.5 hours)
4. Generate interim JTBD report
5. Proceed with remaining chunks based on insights

---

**Ready to Process**: ✅ YES
**Blocker**: None - all systems green
**Estimated Completion**: 5.5 hours active processing across 3 days
