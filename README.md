# 3M Lighting Project
**YouTube Research Automation for Lighting Pain Points**

---

## 🎯 **Overview**

Automated YouTube video analysis platform using multimodal AI to extract Jobs-to-be-Done insights from lighting installation and home improvement content.

**Pipeline:** Whisper large-v3 (audio transcription) + LLaVA 7B (visual analysis) + JTBD extraction

**Current Status:** Production-ready, simplified architecture (HuBERT removed, dependencies reduced 56%)

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.11+ (tested on 3.13)
- Ollama (for LLaVA vision model)
- FFmpeg (for video/audio processing)
- 16GB+ RAM (64GB recommended for batch processing)

### **Setup**
```bash
# 1. Clone repository
git clone https://github.com/anderson115/3m-lighting-project.git
cd 3m-lighting-project

# 2. Install Python dependencies
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows
pip install -r requirements.txt

# 3. Install Ollama and pull LLaVA model
brew install ollama  # or download from ollama.com
ollama pull llava:latest

# 4. Verify Ollama is running
ollama list  # Should show llava:latest

# 5. Configure environment (optional for API models)
cp .env.example .env
# Edit .env if using OpenAI/Gemini/Zhipu models
```

### **Run Analysis**
```bash
# Run preflight analysis (3 test videos)
python scripts/run_preflight_analysis.py

# Output: data/preflight_analysis/{video_id}/analysis.json
# Summary: data/preflight_analysis/summary_report.json
```

---

## 📁 **Project Structure**

```
3m-lighting-project/
├── scripts/                          # Analysis pipeline
│   ├── run_preflight_analysis.py    # MAIN: Orchestrator for 3 test videos
│   ├── multimodal_analyzer.py       # Core: Whisper + LLaVA + JTBD extraction
│   ├── video_downloader.py          # YouTube download + frame extraction
│   ├── test_local_models.py         # Local model benchmarking
│   ├── test_api_comprehensive.py    # API model testing
│   └── validate_pipeline.py         # End-to-end validation
│
├── modules/
│   ├── consumer-video/              # ✅ Consumer interview analysis (PRODUCTION)
│   │   ├── scripts/                 # JTBD + emotion + product extraction
│   │   ├── data/processed/          # Analysis outputs + client deliverables
│   │   └── README.md                # Full documentation
│   ├── youtube-datasource/          # ✅ YouTube video analysis (PRODUCTION)
│   │   └── scripts/                 # Whisper + LLaVA pipeline
│   ├── expert-authority/            # 📋 Expert discussion analysis (PLANNED)
│   │   └── README.md                # Reddit, Quora, forums scraping
│   ├── social-signal/               # 📋 Visual social analysis (PLANNED)
│   │   └── README.md                # Pinterest, Instagram, TikTok trends
│   └── creator-discovery/           # 📋 Creator identification (PLANNED)
│       └── README.md                # Multi-platform creator profiling
│
├── data/
│   ├── preflight/                   # Input: Preflight test videos
│   │   ├── beginner/                # Beginner-level video
│   │   ├── intermediate/            # Intermediate-level video
│   │   └── advanced/                # Advanced-level video
│   ├── preflight_analysis/          # Output: Analysis results
│   │   ├── {video_id}/              # Per-video analysis
│   │   │   ├── analysis.json        # Full multimodal analysis
│   │   │   ├── audio.wav            # Extracted audio (16kHz mono)
│   │   │   └── frames/              # Keyframes (30s intervals)
│   │   ├── summary_report.json      # Aggregated insights
│   │   └── preflight_summary.json   # Performance metrics
│   └── 3m_lighting/
│       └── archives/                # Completed analysis runs
│
├── config/
│   └── model_paths.yaml             # Model configuration (Whisper + LLaVA)
│
├── docs/
│   ├── model-price-plan.md          # ⭐ MASTER: Vision model scorecard
│   ├── youtube-datasource-README.md # Complete setup + usage guide
│   ├── local-models-comparison.md   # Qualitative model comparisons
│   └── jtbd-extraction-plan.md      # Jobs-to-be-Done methodology
│
├── requirements.txt                 # Python dependencies (62 packages)
├── .env.example                     # API key template
└── README.md                        # This file
```

---

## 🔧 **Architecture**

### **Processing Pipeline**

```
1. VIDEO INGESTION
   └─ yt-dlp: YouTube URL → MP4 download

2. PREPROCESSING
   ├─ ffmpeg: Video → 16kHz mono WAV audio
   └─ ffmpeg: Video → Keyframes (1 frame per 30s)

3. MULTIMODAL ANALYSIS
   ├─ Whisper large-v3: Audio → Transcript with timestamps
   └─ LLaVA 7B: Frames → Visual analysis (lighting fixtures, installations)

4. JTBD EXTRACTION
   └─ Keyword-based extraction from transcripts + visual data
      ├─ Pain points (dark, dim, glare, problem, issue)
      ├─ Solutions (LED, strip light, dimmer, fix, install)
      ├─ Verbatim quotes (top pain points)
      └─ Timestamp mapping

5. OUTPUT GENERATION
   ├─ Per-video analysis.json (full multimodal data)
   ├─ summary_report.json (aggregated insights)
   └─ preflight_summary.json (performance metrics)
```

### **Models Used**

| Model | Purpose | Device | Size | Speed |
|-------|---------|--------|------|-------|
| **Whisper large-v3** | Audio transcription | CPU (MPS backend) | 1.5GB | ~6 min/video |
| **LLaVA 7B** | Visual frame analysis | Ollama (local) | 4.5GB | ~60s/frame |

**Note:** HuBERT emotion analysis was removed (1.2GB savings, no functional impact). System now runs Whisper + LLaVA only.

---

## 🔍 **Current Status**

### **Preflight Complete ✅**
- **Videos analyzed:** 3 (beginner, intermediate, advanced)
- **Pain points found:** 11
- **Solutions identified:** 21
- **Verbatim quotes:** 10
- **Processing time:** 25.3 minutes total (8.4 min avg per video)

### **Recent Updates**
- ✅ **2025-10-08:** Simplified architecture (removed HuBERT, -56% dependencies)
- ✅ **2025-10-07:** Model benchmarking complete (9 models tested)
- ✅ **2025-10-05:** Initial preflight run successful

### **Results Location**
```bash
data/preflight_analysis/
├── 6YlrdMaM0dw/          # Beginner: Easy DIY LED Shelf Lighting
├── ZoWPdtYkdCc/          # Intermediate: Baking Polymer Clay
├── IE8iCsXYp_Y/          # Advanced: 10 HomeKit Automations
├── summary_report.json   # Aggregated insights
└── preflight_summary.json # Performance metrics
```

---

## 📚 **Documentation**

| Document | Purpose |
|----------|---------|
| **`docs/model-price-plan.md`** | ⭐ Complete vision model scorecard (9 models tested) |
| **`docs/youtube-datasource-README.md`** | Detailed setup guide with troubleshooting |
| **`docs/local-models-comparison.md`** | Qualitative analysis of local models |
| **`docs/model-output-comparison.md`** | Side-by-side model output examples |
| **`README.md`** | This file - quick start and overview |

---

## 🧪 **Validation**

```bash
# Validate complete pipeline
python scripts/validate_pipeline.py

# Test vision models (benchmark 4 local models)
python scripts/test_local_models.py

# Test API models (benchmark 5 API models)
python scripts/test_api_comprehensive.py
```

---

## 🛠️ **Troubleshooting**

### **Ollama Issues**
```bash
# Check if Ollama is running
ollama list

# Start Ollama service
ollama serve

# Pull LLaVA model if missing
ollama pull llava:latest

# Test LLaVA with sample image
echo "Describe this image" | ollama run llava:latest < test_image.jpg
```

###  **FFmpeg Not Found**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Verify installation
ffmpeg -version
```

### **Memory Issues**
- **Whisper FP16 warning:** Normal on CPU, automatically uses FP32
- **Out of memory:** Reduce `batch_size` in `config/model_paths.yaml`
- **LLaVA crashes:** Ensure Ollama has sufficient memory (4GB+ available)

### **Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python version (requires 3.11+)
python --version
```

---

## 📊 **Performance Notes**

- **Whisper large-v3:** ~6 minutes per 9-minute video (CPU with MPS backend)
- **LLaVA 7B:** ~60 seconds per frame (varies by complexity)
- **Total pipeline:** ~8.4 minutes per video average (3 videos = 25 minutes)
- **Simplified vs original:** -56% dependencies, -15s startup time, same functionality

---

## 📄 **License**

Proprietary - 3M Lighting Research Project
