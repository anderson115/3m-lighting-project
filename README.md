# Video Research Platform
**Multi-Client YouTube Research Automation**

---

## 🎯 **Overview**

Research automation platform for analyzing YouTube videos using multimodal AI (Whisper + LLaVA + LLM extraction) to identify Jobs-to-be-Done insights, pain points, solutions, and product adjacencies.

**Current Client:** 3M Lighting Division (Command Hook adjacency research)

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.11+
- Ollama (running locally)
- FFmpeg
- 64GB RAM (recommended for large models)

### **Setup**
```bash
# Clone and install
git clone <repo>
cd video-research-platform
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with YouTube API key

# Validate setup
python scripts/validate_setup.py
```

### **Run Research**
```bash
# Process videos for a client
python scripts/run_research.py --client 3m_lighting --mode production

# Run preflight test (3 videos)
python scripts/run_research.py --client 3m_lighting --mode preflight
```

---

## 📁 **Project Structure**

```
video-research-platform/
├── core/                    # Client-agnostic engine
│   ├── pipeline/
│   │   ├── perception.py    # Whisper + LLaVA analysis
│   │   ├── extraction.py    # LLM-based JTBD extraction
│   │   └── reporting.py     # Report generation
│   ├── models/
│   │   └── model_registry.py
│   └── utils/
│       ├── video_processing.py
│       └── validation.py
│
├── clients/                 # Client-specific configurations
│   └── 3m_lighting/
│       ├── config.yaml      # Search terms, JTBD framework
│       ├── prompts.yaml     # LLM extraction prompts
│       ├── proposals/       # Client proposals
│       └── reports/         # Generated reports
│
├── data/                    # Data segregated by client
│   └── 3m_lighting/
│       ├── videos/          # Downloaded videos
│       ├── analysis/        # Analysis JSON files
│       └── archives/        # Completed research sprints
│
├── config/
│   └── models.yaml          # Model paths (Whisper, LLaVA, Llama)
│
├── scripts/                 # Runnable workflows
│   ├── run_research.py      # Main entry point
│   └── validate_setup.py    # System validation
│
├── tests/                   # Test suite
└── docs/                    # Documentation
    ├── ARCHITECTURE.md
    ├── CLIENT_SETUP.md
    └── REBUILD_PLAN.md
```

---

## 🔧 **Architecture**

### **Processing Pipeline**

```
1. PERCEPTION (Multimodal Analysis)
   ├─ Whisper large-v3: Audio → Transcript
   └─ LLaVA 7B: Frames → Visual analysis (every 30s)

2. EXTRACTION (LLM-Enhanced)
   └─ Llama 3.1 8B: Combined data → JTBD insights
      ├─ Pain points (functional, social, emotional)
      ├─ Solutions demonstrated
      ├─ Verbatim quotes
      ├─ Golden moments
      └─ Product adjacencies

3. REPORTING
   └─ HTML + JSON + CSV outputs
```

### **Models Used**

| Model | Purpose | Device | Size |
|-------|---------|--------|------|
| Whisper large-v3 | Audio transcription | CPU/MPS | 1.5GB |
| LLaVA 7B | Visual analysis | Ollama | 4.5GB |
| Llama 3.1 8B | JTBD extraction | Ollama | 4.7GB |

---

## 📊 **Client Setup**

See `docs/CLIENT_SETUP.md` for detailed instructions on adding new clients.

**Quick overview:**
1. Create `clients/{client_name}/config.yaml`
2. Define JTBD framework and search terms
3. Create extraction prompts in `prompts.yaml`
4. Run: `python scripts/run_research.py --client {client_name}`

---

## 🔍 **Current Status**

### **3M Lighting Project**

**Phase:** Preflight Complete → Production Enhancement
- ✅ Preflight validated (3 videos, 11 pain points, 21 solutions)
- ✅ Client HTML report delivered
- 🔄 LLM extraction layer (in progress)
- ⏳ Sprint 1 (50-100 videos) - pending

**Archived Results:**
- Preflight videos: `data/3m_lighting/archives/preflight_2025-10-05/`
- HTML report: `data/3m_lighting/archives/preflight_2025-10-05/analysis/PREFLIGHT_REPORT_3M_Lighting.html`

---

## 🧪 **Testing**

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_extraction.py

# Validate pipeline on single video
python scripts/validate_setup.py --video <video_id>
```

---

## 📝 **Development**

### **Key Files**

- `core/pipeline/extraction.py` - LLM-based JTBD extraction (currently being enhanced)
- `core/pipeline/perception.py` - Whisper + LLaVA analysis
- `clients/3m_lighting/config.yaml` - 3M research configuration
- `config/models.yaml` - Model paths and settings

### **Adding Features**

1. Update relevant `core/` module
2. Add tests in `tests/`
3. Update client config if needed
4. Run validation suite

---

## 📚 **Documentation**

- **Architecture:** `docs/ARCHITECTURE.md` - System design and data flow
- **Client Setup:** `docs/CLIENT_SETUP.md` - Adding new research programs
- **Rebuild Plan:** `docs/REBUILD_PLAN.md` - Latest enhancement plan

---

## 🛠️ **Troubleshooting**

**Common Issues:**

1. **Ollama connection errors**
   ```bash
   # Verify Ollama is running
   ollama list
   # Check models are installed
   ollama pull llava:latest
   ollama pull llama3.1:8b
   ```

2. **FFmpeg not found**
   ```bash
   # macOS
   brew install ffmpeg
   # Linux
   sudo apt install ffmpeg
   ```

3. **Out of memory errors**
   - Reduce batch size in `config/models.yaml`
   - Process videos sequentially (set `num_workers: 1`)

---

## 📄 **License**

Proprietary - Offbrain Insights
