# YouTube Data Source - Master Documentation

## Overview
Automated YouTube video analysis system for 3M Lighting Project, extracting visual insights using local and cloud-based vision models.

**Status:** Phase 2 Complete (Local model integration)
**Last Updated:** 2025-10-07
**Hardware:** Apple M2 Max, 64GB unified memory

---

## 🎯 Core Capabilities

### Video Processing
- **YouTube Live Stream Capture**: Download and frame extraction
- **Keyword Detection**: Timestamp identification for relevant moments
- **Frame Analysis**: Vision model processing of extracted frames
- **JTBD Extraction**: Jobs-to-be-Done framework analysis
- **Multi-Model Support**: 9 models (4 local, 5 API)

### Vision Model Tiers
1. **Local Models** (Primary): MiniCPM-V 8B, Llama 3.2 Vision 11B, Qwen 7B/3B
2. **API Models** (Fallback): GLM-4V, GPT-4o, Gemini 2.0 Flash
3. **Cost**: $0.00 for local, near-free for API

---

## 📂 Project Structure

```
3m-lighting-project/
├── scripts/
│   ├── run_preflight_analysis.py     # MAIN: Full pipeline orchestrator
│   ├── multimodal_analyzer.py        # Core: Video+Audio+Visual+JTBD analyzer
│   ├── video_downloader.py           # YouTube download + frame extraction
│   ├── test_local_models.py          # Local model benchmarking (MiniCPM, Llama, Qwen)
│   ├── test_api_comprehensive.py     # API model testing (GLM, GPT, Gemini)
│   ├── validate_pipeline.py          # End-to-end validation
│   └── wait_for_lmstudio.sh          # LM Studio health check
│
├── docs/
│   ├── model-price-plan.md           # ⭐ MASTER: Complete vision model scorecard
│   ├── youtube-datasource-README.md  # THIS FILE: Setup + usage guide
│   ├── local-models-comparison.md    # Qualitative model comparison
│   └── jtbd-extraction-plan.md       # Jobs-to-be-Done methodology
│
├── data/
│   ├── preflight_analysis/           # Main output: Analysis results
│   │   ├── {video_id}/               # Per-video analysis
│   │   │   ├── analysis.json         # Full multimodal analysis
│   │   │   ├── audio.wav             # Extracted audio
│   │   │   └── frames/               # Keyframes (JPEG)
│   │   ├── summary_report.json       # Aggregated insights
│   │   └── preflight_summary.json    # Performance metrics
│   ├── youtube_live_test/            # Legacy: API model testing
│   │   ├── frames/                   # Test frames
│   │   └── local_models_comparison.json
│   └── jtbd_output/                  # JTBD extraction results
│
├── venv/                              # Python virtual environment
└── requirements.txt                   # Python dependencies
```

---

## 🤖 Local Vision Models

### 1. MiniCPM-V 8B ⭐ (PRIMARY - RECOMMENDED)
**Score:** 85.0 | **Size:** 5.5 GB | **Speed:** 21s/frame | **Output:** 1,825 chars

**Installation:**
```bash
# Download model from Ollama
ollama pull minicpm-v:8b

# Verify installation
ollama list | grep minicpm
# Should show: minicpm-v:8b    5.5 GB

# Test with sample image
ollama run minicpm-v:8b "Describe this image" < test_image.jpg
```

**System Requirements:**
- **RAM**: 16GB minimum (4GB with int4 quantization)
- **Storage**: 5.5 GB disk space
- **GPU**: Optional (MPS/CUDA acceleration), works on CPU
- **OS**: macOS (Apple Silicon), Linux, Windows

**Strengths:**
- Best speed/quality ratio globally (85.0 score)
- Beats GPT-4o on OpenCompass benchmark (77.0 score)
- Most detailed local model (1,825 chars avg)
- No crashes with 1920x1080 images
- Production-ready quality
- No special configuration required

**Use Cases:**
- ✅ Primary recommendation for all users
- ✅ Detailed technical analysis (lighting fixtures, installations)
- ✅ Privacy-sensitive applications (HIPAA/GDPR compliant)
- ✅ Cost-conscious deployments (unlimited free usage)
- ✅ High-volume batch processing (no rate limits)

---

### 2. Llama 3.2 Vision 11B (SECONDARY - STRUCTURED OUTPUT)
**Score:** 78.0 | **Size:** 7.8 GB | **Speed:** 38s/frame | **Output:** 1,229 chars

**Installation:**
```bash
# Download Meta's official vision model
ollama pull llama3.2-vision:11b

# Verify installation
ollama list | grep llama3.2-vision
# Should show: llama3.2-vision:11b    7.8 GB

# Test with structured output
ollama run llama3.2-vision:11b "List all visible components" < test_image.jpg
```

**System Requirements:**
- **RAM**: 8GB minimum (optimized quantization)
- **Storage**: 7.8 GB disk space
- **GPU**: Optional (Apple Metal/NVIDIA CUDA)
- **OS**: macOS, Linux, Windows

**Strengths:**
- Most structured output (bullet lists, numbered sections)
- Meta's official vision model (well-maintained)
- 1 point behind GPT-4o on benchmarks
- Excellent for educational content
- Consistent performance across all test images
- No hallucinations observed in testing

**Use Cases:**
- ✅ When structured output is preferred (reports, documentation)
- ✅ Documentation creation (markdown-friendly format)
- ✅ Educational/instructional content (step-by-step breakdowns)
- ✅ Systematic technical analysis (component inventories)
- ✅ Workshop/training materials

---

### 3. Qwen2.5-VL 7B (OCR SPECIALIST - REQUIRES SETUP)
**Score:** 72.0 | **Size:** 6.0 GB | **Speed:** 51s/frame | **Output:** 1,060 chars

**Installation (REQUIRES CUSTOM MODELFILE):**
```bash
# Step 1: Download base model
ollama pull qwen2.5vl:7b

# Step 2: Create custom Modelfile to prevent GPU crashes
cat > /tmp/Modelfile.qwen7b << 'EOF'
FROM qwen2.5vl:7b
PARAMETER num_gpu 0
PARAMETER num_thread 8
EOF

# Step 3: Build custom model with CPU-only inference
ollama create qwen7b-cpu -f /tmp/Modelfile.qwen7b

# Step 4: Verify custom model
ollama list | grep qwen7b-cpu
# Should show: qwen7b-cpu    6.0 GB

# Step 5: Test with image
ollama run qwen7b-cpu "Extract all text from this image" < test_image.jpg
```

**⚠️ Why Custom Modelfile Required?**
- **Problem**: Qwen 7B crashes with GPU on high-resolution images
  - High-res images (1920x1080) create 80GB+ RAM tensors
  - Exceeds M2 Max 64GB unified memory capacity
  - Error: "model runner has unexpectedly stopped"
- **Solution**: `PARAMETER num_gpu 0` forces CPU-only inference
  - Reduces memory footprint to manageable levels
  - Works perfectly with full 1920x1080 images
  - Stable operation, no crashes

**System Requirements:**
- **RAM**: 8GB minimum (CPU mode reduces memory usage)
- **Storage**: 6.0 GB disk space
- **CPU**: 8+ threads recommended (set via `num_thread`)
- **GPU**: Must disable GPU inference (use Modelfile above)
- **OS**: macOS, Linux, Windows

**Strengths:**
- Best OCR capabilities among local models
- Alibaba's flagship VL model (top benchmark scores)
- Excellent for multilingual text (English, Japanese, Arabic, Chinese)
- Contextual understanding (workshop setting, tools, environment)
- Narrative-style detailed responses (1,060 chars avg)
- Superior chart/table extraction

**Use Cases:**
- ✅ OCR-heavy workloads (charts, tables, signs, labels)
- ✅ Multilingual text extraction (international content)
- ✅ When maximum detail is needed (willing to wait 51s)
- ✅ Backup option if MiniCPM unavailable
- ✅ Research/testing scenarios

**Troubleshooting:**
- If crashes persist: Verify Modelfile with `ollama show qwen7b-cpu --modelfile`
- Should show: `PARAMETER num_gpu 0`
- Alternative: Use Qwen 3B (faster, less detail) instead

---

### 4. Qwen2.5-VL 3B (LIGHTWEIGHT BACKUP - REQUIRES CPU MODE)
**Score:** 52.0 | **Size:** 3.2 GB | **Speed:** 25s/frame | **Output:** Variable

**Installation & Usage (REQUIRES CPU MODE):**
```bash
# Step 1: Download model
ollama pull qwen2.5vl:3b

# Step 2: Verify installation
ollama list | grep qwen2.5vl:3b
# Should show: qwen2.5vl:3b    3.2 GB

# Step 3: Set CPU mode environment variable (CRITICAL)
export OLLAMA_LLM_LIBRARY=cpu

# Step 4: Use with chat API (not generate API)
curl http://localhost:11434/api/chat -d '{
  "model": "qwen2.5vl:3b",
  "messages": [
    {
      "role": "user",
      "content": "Describe this image",
      "images": ["<base64_encoded_image>"]
    }
  ],
  "stream": false
}'
```

**⚠️ Why CPU Mode Required?**
- **Problem**: GPU mode returns empty responses
  - Model loads successfully but outputs: `"text": ""`
  - Processing time varies but always 0 characters
  - Error: Model runner stops unexpectedly
- **Solution**: `export OLLAMA_LLM_LIBRARY=cpu` before requests
  - Forces CPU-only inference
  - Must use `/api/chat` endpoint (not `/api/generate`)
  - See `scripts/test_local_models.py` for Python implementation

**System Requirements:**
- **RAM**: 4GB minimum (smallest local model)
- **Storage**: 3.2 GB disk space
- **CPU**: Multi-core recommended
- **GPU**: Must disable via environment variable
- **OS**: macOS, Linux, Windows

**Strengths:**
- Fastest Qwen model (25s vs 51s for 7B)
- Smallest memory footprint (3.2 GB)
- Works with full-resolution images (CPU mode)
- Good fallback option when larger models unavailable
- Faster than Llama 11B (25s vs 38s)

**Weaknesses:**
- Requires CPU mode environment variable (extra setup)
- Less detailed than larger models (basic analysis)
- Lower quality than MiniCPM/Llama (52.0 vs 85.0/78.0 scores)
- Must use chat API (more complex integration)

**Use Cases:**
- ✅ Memory-constrained environments (4GB RAM)
- ✅ When speed matters more than depth (25s fast)
- ✅ Backup/fallback option (if primary models fail)
- ✅ Testing and development (quick iterations)
- ✅ Edge devices with limited resources

**Python Integration Example:**
```python
import subprocess, json, base64

# Set CPU mode
env = {"OLLAMA_LLM_LIBRARY": "cpu"}

# Prepare request (chat API format)
request = {
    "model": "qwen2.5vl:3b",
    "messages": [{
        "role": "user",
        "content": "Describe this lighting fixture",
        "images": [base64_image]
    }],
    "stream": False
}

# Make request with CPU mode
result = subprocess.run(
    ['curl', '-s', 'http://localhost:11434/api/chat',
     '-d', json.dumps(request)],
    capture_output=True,
    env={**os.environ, **env}
)

response = json.loads(result.stdout)
text = response['message']['content']
```

---

### ❌ LLaVA - DEPRECATED
**Status:** REMOVED due to severe hallucinations

**Issues:**
- Frame 1: Claimed "optical illusion" (actual: single switch)
- Frame 2: Said "cardboard cutout" (actual: real demo board)
- Frame 3: Described "man next to mirror" (actual: light fixtures)

**Replacement:** Use MiniCPM-V 8B instead (superior in all metrics)

---

## 🌐 API Models (Fallback)

### GLM-4V Flash (Best API Value)
- **Score:** 60.8 | **Cost:** $0.00 (near-free) | **Speed:** 5.3s
- **Best for:** When local models unavailable, speed-critical

### GLM-4V Plus (Structured)
- **Score:** 58.6 | **Cost:** $0.000003 | **Speed:** 5.7s
- **Best for:** Troubleshooting, structured analysis

### GPT-4o-mini (Most Verbose API)
- **Score:** 56.8 | **Cost:** $0.005680 | **Speed:** 7.7s
- **Best for:** OpenAI ecosystem integration

### Gemini 2.0 Flash (Speed King)
- **Score:** 54.6 | **Cost:** $0.00 | **Speed:** 2.7s
- **Best for:** Real-time analysis, 10x faster than local

### GPT-4o (Premium)
- **Score:** 39.8 | **Cost:** $0.004596 | **Speed:** 8.1s
- **Best for:** Edge cases (not recommended due to poor ROI)

**Full details:** See `docs/model-price-plan.md`

---

## 🚀 Quick Start

### Prerequisites
```bash
# Install Ollama
brew install ollama

# Install Python dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Pull primary local model
ollama pull minicpm-v:8b
ollama pull llama3.2-vision:11b
```

### Environment Variables
```bash
# Required for API models
export OPENAI_API_KEY="your_key_here"
export ZHIPU_API_KEY="your_key_here"      # For GLM models
export GEMINI_API_KEY="your_key_here"

# Optional for Qwen 3B
export OLLAMA_LLM_LIBRARY=cpu
```

### Basic Usage

#### 1. Download YouTube Video + Extract Frames
```bash
python scripts/youtube_live.py \
  --video-id "-qYonWEwPko" \
  --keywords "light,switch,fixture,install"
```

**Output:**
- `data/youtube_live_test/videos/-qYonWEwPko.mp4`
- `data/youtube_live_test/frames/-qYonWEwPko/frame_*.jpg`

#### 2. Analyze Frames with Vision Models
```bash
python scripts/analyze_frames.py \
  --frames-dir "data/youtube_live_test/frames/-qYonWEwPko" \
  --model "minicpm-v:8b" \
  --output "data/analysis/results.json"
```

#### 3. Extract JTBD Insights
```bash
python scripts/extract_jtbd.py \
  --input "data/analysis/results.json" \
  --output "data/jtbd_output/insights.json"
```

#### 4. Full Pipeline (Automated)
```bash
python scripts/run_preflight_analysis.py
```

---

## 📊 Model Selection Guide

### Decision Tree
```
START: What's your priority?

├─ Quality = Top Priority
│  └─ Use: MiniCPM-V 8B (85.0 score, 1,825 chars, 21s, free)
│
├─ Structure = Top Priority
│  └─ Use: Llama 3.2 Vision 11B (78.0 score, bullet lists, 38s, free)
│
├─ Speed = Top Priority
│  └─ Use: Gemini 2.0 Flash (2.7s, API, free)
│
├─ OCR/Multilingual = Top Priority
│  └─ Use: Qwen 7B CPU (72.0 score, best OCR, requires Modelfile)
│
└─ Cost = Top Priority
   └─ Use: Any local model ($0.00, no limits)
```

### Pricing Tiers

**Standard Tier (FREE):**
- MiniCPM-V 8B (primary)
- Llama 3.2 Vision 11B (secondary)
- GLM-4V Flash (API fallback)
- **Best for:** 95% of users

**Pro Tier ($4.99/month):**
- All Standard models
- Gemini 2.0 Flash (2.7s speed)
- GLM-4V Plus (structured)
- GPT-4o-mini (most verbose)
- Qwen 7B CPU (OCR specialist)
- **Best for:** Speed-critical, OCR-heavy workloads

**Admin Tier (Custom):**
- All Pro models
- GPT-4o access
- Custom model testing
- **Best for:** Research, comparative analysis

---

## 🔧 Troubleshooting

### Qwen 7B Crashes
**Error:** "model runner has unexpectedly stopped"

**Solution:** Use custom Modelfile with `num_gpu 0`:
```bash
cat > Modelfile.qwen7b << 'EOF'
FROM qwen2.5vl:7b
PARAMETER num_gpu 0
PARAMETER num_thread 8
EOF
ollama create qwen7b-cpu -f Modelfile.qwen7b
```

**Why:** High-resolution images (1920x1080) create 80GB+ RAM tensors that exceed M2 Max capacity.

---

### Qwen 3B Empty Responses
**Error:** `"text": ""` with `"success": true`

**Solution:** Use CPU mode + chat API:
```bash
export OLLAMA_LLM_LIBRARY=cpu
```

**In code:**
```python
env = {"OLLAMA_LLM_LIBRARY": "cpu"}
request = {
    "model": "qwen2.5vl:3b",
    "messages": [{"role": "user", "content": prompt, "images": [image_base64]}],
    "stream": False
}
```

---

### Ollama Server Not Running
```bash
# Start Ollama service
ollama serve

# Check status
curl http://localhost:11434/api/tags
```

---

### Memory Issues (Local Models)
- **MiniCPM 8B**: Requires ~16GB RAM (or 4GB with int4 quantization)
- **Llama 11B**: Requires ~8GB RAM
- **Qwen 7B**: Use CPU mode (Modelfile) to avoid GPU memory overflow
- **Qwen 3B**: Use CPU mode environment variable

---

## 📈 Performance Benchmarks

### Processing Time (50 frames @ 1920x1080)

| Model | Time | Cost | Chars/Frame | Score |
|-------|------|------|-------------|-------|
| **MiniCPM-V 8B** | 17.5 min | $0.00 | 1,825 | 85.0 ⭐ |
| **Llama 11B** | 31.7 min | $0.00 | 1,229 | 78.0 |
| **Qwen 7B CPU** | 42.5 min | $0.00 | 1,060 | 72.0 |
| GLM-4V Flash | 4.4 min | $0.0003 | 858 | 60.8 |
| Gemini 2.0 Flash | 2.2 min | $0.00 | 484 | 54.6 |
| GPT-4o-mini | 6.4 min | $0.28 | 1,288 | 56.8 |
| GPT-4o | 6.7 min | $0.23 | 904 | 39.8 |

**Key Insight:** Local models offer best quality at zero cost. APIs offer speed (2-6 min vs 17-42 min).

---

## 🔐 Security & Privacy

### Local Models (Privacy-First)
- **No external API calls**: All inference runs locally
- **No data transmission**: Images never leave your machine
- **HIPAA/GDPR compliant**: Suitable for sensitive data
- **No rate limits**: Process unlimited frames

### API Models (Cloud-Based)
- **Data transmission**: Images sent to cloud providers
- **Privacy policies apply**: Review vendor terms
- **Rate limits**: Check provider quotas
- **Costs apply**: Monitor usage to avoid surprises

---

## 📝 Key Files Reference

### Core Scripts
1. **`scripts/run_preflight_analysis.py`** ⭐ MAIN ORCHESTRATOR
   - Full pipeline: Download → Extract → Transcribe → Analyze → JTBD
   - Processes 3 preflight videos (beginner, intermediate, advanced)
   - Outputs: Analysis JSON, summary reports, performance metrics
   - Usage: `python scripts/run_preflight_analysis.py`

2. **`scripts/multimodal_analyzer.py`** - Core Analysis Engine
   - Multimodal analysis: Video + Audio + Visual + JTBD
   - Integrates: Whisper (transcription), HuBERT (emotion), LLaVA (vision)
   - Keyframe extraction and intelligent sampling
   - Used by: `run_preflight_analysis.py`

3. **`scripts/video_downloader.py`** - YouTube Download
   - YouTube video download via yt-dlp
   - Frame extraction at configurable intervals
   - Metadata extraction (title, channel, duration)
   - Used by: `multimodal_analyzer.py`

4. **`scripts/test_local_models.py`** - Local Model Benchmarking
   - Tests: MiniCPM-V 8B, Llama 11B, Qwen 7B, Qwen 3B
   - Handles Qwen CPU mode configuration
   - 5 random frames, standardized output
   - Generates: `local_models_comparison.json`

5. **`scripts/test_api_comprehensive.py`** - API Model Testing
   - Tests: GLM-4V (Flash/Plus), GPT-4o, Gemini 2.0 Flash
   - Full scorecard generation with 6-dimensional metrics
   - Cost/speed/quality analysis
   - Generates: `comprehensive_test_raw_results.json`

6. **`scripts/validate_pipeline.py`** - End-to-End Validation
   - Validates full pipeline from download to JTBD
   - Checks: Dependencies, models, API keys, disk space
   - Health checks for Ollama and LM Studio
   - Pre-flight validation before batch processing

### Documentation
1. **`docs/model-price-plan.md`** ⭐ MASTER SCORECARD
   - Complete performance testing: 9 models (4 local, 5 API)
   - 6-dimensional scoring (cost, speed, breadth, depth, uniqueness, accuracy)
   - Pricing tier recommendations (Standard/Pro/Admin)
   - Qualitative analysis and sample outputs

2. **`docs/youtube-datasource-README.md`** - THIS FILE
   - Project overview and setup guide
   - Local model installation with troubleshooting
   - Quick start and usage examples
   - Key files reference

3. **`docs/local-models-comparison.md`** - Qualitative Comparison
   - Side-by-side comparison of local models on same frames
   - Detailed analysis of strengths/weaknesses
   - Real output examples from testing

4. **`docs/jtbd-extraction-plan.md`** - JTBD Methodology
   - Jobs-to-be-Done framework explanation
   - Pain point identification strategies
   - Solution extraction patterns
   - Verbatim quote selection criteria

### Data Outputs
1. **`data/preflight_analysis/{video_id}/analysis.json`** - Full Analysis
   - Complete multimodal analysis per video
   - Structure: video_info, transcript, emotion, visual_analysis, jtbd_insights
   - Used for: Downstream processing, reports, dashboards

2. **`data/preflight_analysis/summary_report.json`** - Aggregated Insights
   - Combined insights across all videos
   - Pain points, solutions, verbatims aggregated
   - Used for: Executive summaries, trend analysis

3. **`data/preflight_analysis/preflight_summary.json`** - Performance Metrics
   - Processing time per video and total
   - Results breakdown by difficulty level
   - Used for: Performance monitoring, optimization

4. **`data/youtube_live_test/local_models_comparison.json`** - Benchmarks
   - Raw results from local model testing
   - Performance data: Speed, output length, success rate
   - Used for: Model selection, scorecard updates

### Configuration
1. **`requirements.txt`** - Python Dependencies
   - Core: yt-dlp, opencv-python, whisper, transformers
   - Vision: ollama-python, openai, anthropic
   - ML: torch, numpy, pillow, librosa

2. **`.env`** - API Keys (NOT IN REPO)
   - Required: `OPENAI_API_KEY`, `ZHIPU_API_KEY`, `GEMINI_API_KEY`
   - Optional: `ANTHROPIC_API_KEY` (for Claude models)
   - Create from: `.env.example` template

3. **`Modelfile.qwen7b`** - Custom Qwen 7B Config (CREATE MANUALLY)
   - Required for: Qwen 7B to work without crashes
   - Contents: `FROM qwen2.5vl:7b`, `PARAMETER num_gpu 0`
   - Build: `ollama create qwen7b-cpu -f Modelfile.qwen7b`

---

## 🎓 Additional Resources

### Model Documentation
- **MiniCPM-V**: [openbmb/MiniCPM-V](https://github.com/OpenBMB/MiniCPM-V)
- **Llama 3.2 Vision**: [Meta AI](https://ai.meta.com/llama/)
- **Qwen2.5-VL**: [QwenLM/Qwen2-VL](https://github.com/QwenLM/Qwen2-VL)
- **Ollama**: [ollama.com/library](https://ollama.com/library)

### API Providers
- **GLM-4V**: [BigModel.cn](https://bigmodel.cn/)
- **GPT-4o**: [OpenAI Platform](https://platform.openai.com/)
- **Gemini**: [Google AI Studio](https://aistudio.google.com/)

### Methodology
- **JTBD Framework**: [Jobs to Be Done](https://jtbd.info/)
- **Vision Model Benchmarks**: [OpenCompass](https://opencompass.org.cn/)

---

## 🚀 Roadmap

### Phase 1: Complete ✅
- YouTube video download and frame extraction
- API model testing (5 models)
- Initial JTBD extraction prototype

### Phase 2: Complete ✅
- Local model integration (4 models)
- Model comparison benchmarking
- Qwen 7B/3B CPU mode fixes
- Comprehensive documentation

### Phase 3: In Progress 🔄
- JTBD integration with perception data
- Full pipeline orchestrator
- Automated testing suite

### Phase 4: Planned 📋
- Real-time video analysis
- Multi-video batch processing
- Advanced JTBD clustering
- Dashboard visualization

---

## 📞 Support

### Common Issues
1. **Qwen models crash**: Use custom Modelfile (7B) or CPU mode (3B)
2. **Ollama not found**: Install via `brew install ollama`
3. **Out of memory**: Use smaller models or reduce image resolution
4. **API errors**: Check API keys in `.env` file

### Getting Help
- Check `docs/model-price-plan.md` for detailed model specs
- Review troubleshooting section above
- Verify Ollama status: `ollama list`
- Test with single frame before batch processing

---

**Last Updated:** 2025-10-07
**Version:** 2.1 (Documentation complete with model setup instructions)
**Contact:** 3M Lighting Project Team

---

## 📋 Quick Reference Card

### Model Installation Checklist
```bash
# ✅ PRIMARY (Install this first)
ollama pull minicpm-v:8b

# ✅ SECONDARY (Structured output)
ollama pull llama3.2-vision:11b

# ⚠️ OPTIONAL: Qwen 7B (Requires Modelfile - see above)
ollama pull qwen2.5vl:7b
# Then: Create Modelfile, run `ollama create qwen7b-cpu -f Modelfile.qwen7b`

# ⚠️ OPTIONAL: Qwen 3B (Requires CPU mode - see above)
ollama pull qwen2.5vl:3b
# Then: `export OLLAMA_LLM_LIBRARY=cpu` before use
```

### Model Selection Quick Guide
| Priority | Use This Model | Why |
|----------|---------------|-----|
| **Best Overall** | MiniCPM-V 8B | 85.0 score, 21s, 1,825 chars, no setup |
| **Structured Output** | Llama 3.2 Vision 11B | 78.0 score, bullet lists, reports |
| **OCR/Multilingual** | Qwen 7B (with Modelfile) | Best OCR, charts, tables |
| **Speed (API)** | Gemini 2.0 Flash | 2.7s, 10x faster than local |
| **Cost (API)** | GLM-4V Flash | Near-free, 5.3s, good quality |

### Common Commands
```bash
# Check installed models
ollama list

# Test model with image
ollama run minicpm-v:8b "Describe this" < image.jpg

# Check Ollama server status
curl http://localhost:11434/api/tags

# Run full analysis pipeline
python scripts/run_preflight_analysis.py

# Validate environment
python scripts/validate_pipeline.py
```
