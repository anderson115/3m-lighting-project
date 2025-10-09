# 3M LIGHTING PROJECT - STRUCTURE & STANDARDS

**Project:** Multi-Module Research Automation Platform
**Client:** 3M Lighting
**Date:** 2025-10-08
**Status:** Modular Architecture Established

---

## 📁 PROJECT STRUCTURE

```
3m-lighting-project/
├── modules/                          # All analysis modules (modular architecture)
│   ├── youtube-datasource/           # ✅ PRODUCTION
│   │   ├── scripts/                  # multimodal_analyzer.py, run_preflight_analysis.py
│   │   ├── data/3m_lighting/         # Processed YouTube videos
│   │   ├── config/                   # Symlink to shared config
│   │   ├── docs/                     # Module documentation
│   │   ├── tests/                    # Module tests
│   │   └── README.md                 # Module overview
│   │
│   ├── consumer-video/               # 📋 PLANNED (ready for dev)
│   │   ├── scripts/                  # consumer_analyzer.py, emotion_analyzer.py
│   │   ├── data/
│   │   │   ├── raw_videos/           # Client-provided interviews (gitignored)
│   │   │   ├── processed/            # Per-video analysis JSON
│   │   │   └── deliverables/         # Final reports
│   │   ├── prompts/                  # Domain-specific extraction prompts
│   │   ├── config/                   # Symlink to shared config
│   │   ├── docs/                     # Implementation plans
│   │   ├── tests/                    # Validation scripts
│   │   └── README.md
│   │
│   └── creator-discovery/            # 📋 PLANNED (PRD complete)
│       ├── scripts/                  # Discovery, profiling, classification
│       ├── data/                     # Creator databases
│       ├── config/                   # API keys, search params
│       ├── docs/                     # PRD and specifications
│       ├── tests/                    # Validation tests
│       └── README.md
│
├── config/                           # SHARED CONFIGURATION
│   └── model_paths.yaml              # Model locations on TARS volume
│
├── scripts/                          # LEGACY/SHARED SCRIPTS (being migrated to modules)
│   ├── multimodal_analyzer.py        # Core analyzer (copied to youtube module)
│   ├── run_preflight_analysis.py     # YouTube analysis orchestrator
│   └── checkpoint_test_5videos.py    # Validation test
│
├── data/                             # LEGACY DATA (being migrated to modules)
│   ├── 3m_lighting/                  # → modules/youtube-datasource/data/
│   ├── checkpoint_test_5videos/      # Test data
│   ├── checkpoint_test_output/       # Test results
│   └── consumer-interviews/          # → modules/consumer-video/data/raw_videos/
│
├── docs/                             # PROJECT DOCUMENTATION
│   ├── README.md                     # Main project overview
│   ├── PROJECT-STRUCTURE.md          # This file
│   ├── consumer-video-FINAL-PLAN.md  # Consumer video implementation plan
│   ├── PRD-creator-discovery.md      # Creator discovery PRD
│   ├── EMOTION-ANALYSIS-BEST-OPTIONS-2025.md  # Emotion model research
│   ├── model-price-plan.md           # Model comparison and costs
│   └── youtube-datasource-README.md  # YouTube module documentation
│
├── tests/                            # PROJECT-LEVEL TESTS
│   └── (module-specific tests in module folders)
│
├── venv/                             # Python virtual environment
├── requirements.txt                  # Shared dependencies
├── .gitignore                        # Git exclusions (media files)
├── .env.example                      # Environment template
└── README.md                         # Quick start guide
```

---

## 🎯 MODULE STANDARDS

### Required Structure (All Modules)
```
module-name/
├── scripts/          # All Python scripts for this module
├── data/             # Module-specific data (gitignored if large)
├── config/           # Module configuration (symlink to shared or module-specific)
├── docs/             # Module documentation
├── tests/            # Module unit tests
└── README.md         # Module overview, status, models used
```

### Required Documentation (Each Module)
1. **README.md** - Overview, purpose, status
2. **Status badge** - ✅ Production, 🔄 Development, 📋 Planned
3. **Models used** - List all AI models and dependencies
4. **Structure** - Folder descriptions
5. **Quick start** - How to run the module

### Shared Resources
- **config/model_paths.yaml** - All modules symlink to this
- **requirements.txt** - Shared Python dependencies
- **/Volumes/TARS/llm-models/** - All models stored here

---

## 🔧 TECHNOLOGY STACK

### Core Models (Shared)
| Model | Purpose | Location | Size |
|-------|---------|----------|------|
| Whisper large-v3 | Audio transcription | TARS/llm-models/whisper/ | 1.5GB |
| LLaVA 7B | Visual analysis | Ollama (llava:latest) | 4.5GB |
| MiniCPM-V 8B | Vision (optional upgrade) | Ollama (minicpm-v:latest) | 5.5GB |

### Module-Specific Models
| Model | Module | Purpose | Location | Size |
|-------|--------|---------|----------|------|
| SpeechBrain wav2vec2-IEMOCAP | consumer-video | Emotion recognition | TARS/llm-models/speechbrain/ | 460MB |

### Frameworks
- **Python 3.13** - Primary language
- **PyTorch 2.8.0** - ML framework (MPS acceleration)
- **FFmpeg** - Video/audio processing
- **Ollama** - Local LLM serving
- **librosa** - Audio signal processing
- **SpeechBrain** - Speech emotion recognition

---

## 📊 MODULE STATUS

### ✅ Production Modules
**youtube-datasource**
- Status: Production-ready
- Validation: 96% success rate (5/5 videos, 46.6 min total)
- Models: Whisper large-v3, LLaVA 7B
- Output: Pain points, solutions, JTBD insights
- Performance: ~8-9 min per video

### 🔄 Development Modules
**consumer-video**
- Status: Implementation plan ready
- Plan: docs/consumer-video-FINAL-PLAN.md
- Models: Whisper, LLaVA, SpeechBrain wav2vec2, librosa
- Output: Pain points, emotions, 3M adjacency, workarounds
- Timeline: 12-16 hours development

### 📋 Planned Modules
**creator-discovery**
- Status: PRD complete
- PRD: docs/PRD-creator-discovery.md
- APIs: YouTube, TikTok, Instagram
- Output: Creator profiles, demographics, psychographics
- Timeline: 12 weeks (4 phases)

---

## 🔄 MIGRATION STATUS

### Completed
- ✅ Created modular folder structure
- ✅ Module READMEs created
- ✅ Shared config established (model_paths.yaml)
- ✅ Documentation consolidated

### In Progress
- 🔄 Migrating youtube scripts to modules/youtube-datasource/
- 🔄 Migrating data to module folders
- 🔄 Updating import paths

### Pending
- ⏳ consumer-video module implementation
- ⏳ creator-discovery module implementation

---

## 🚀 QUICK START (By Module)

### YouTube Data Source
```bash
cd modules/youtube-datasource
source ../../venv/bin/activate
python scripts/run_preflight_analysis.py
```

### Consumer Video (Once Implemented)
```bash
cd modules/consumer-video
source ../../venv/bin/activate
python scripts/run_batch_analysis.py --input data/raw_videos/ --output data/processed/
```

### Creator Discovery (Once Implemented)
```bash
cd modules/creator-discovery
source ../../venv/bin/activate
python scripts/discover_creators.py --niche "DIY lighting" --platforms youtube,tiktok
```

---

## 📋 DEVELOPMENT STANDARDS

### Code Style
- **PEP 8** compliant
- **Type hints** on all functions
- **Docstrings** for all classes and functions
- **Error handling** with try/except and logging

### Testing
- **Unit tests** in module tests/ folder
- **Integration tests** for full pipeline
- **Validation tests** with known-good data
- **Minimum 70% coverage**

### Documentation
- **README.md** in every module
- **Inline comments** for complex logic
- **CHANGELOG.md** for version tracking
- **API documentation** for public functions

### Git Workflow
- **main** branch for production code
- **Feature branches** for development
- **Descriptive commits** with context
- **Tags** for releases (v1.0.0-module-name)

---

## 🔐 SECURITY & PRIVACY

### Sensitive Data
- ✅ `.env` files gitignored
- ✅ API keys never committed
- ✅ Consumer videos gitignored (large media files)
- ✅ Personal data scrubbed from outputs

### Model Security
- ✅ All models local (no external API by default)
- ✅ TARS volume for centralized model storage
- ✅ PRO tier API calls optional (user consent required)

---

## 📦 DEPENDENCIES

### Current (requirements.txt)
```txt
openai-whisper>=20231117
torch>=2.8.0
torchaudio>=2.8.0
torchvision>=0.19.0
moviepy>=1.0.3
Pillow>=10.0.0
requests>=2.31.0
pyyaml>=6.0
ollama>=0.1.0

# Planned additions for consumer-video
speechbrain>=1.0.0
librosa>=0.10.0
soundfile>=0.12.0
```

### System Requirements
- **Python:** 3.13+
- **RAM:** 32GB minimum (64GB recommended)
- **Storage:** 50GB+ free on TARS volume
- **GPU:** Mac M2/M3 with MPS, or NVIDIA CUDA

---

## 🎯 PROJECT GOALS

1. **Modularity** - Each data source is independent module
2. **Reusability** - Shared models and configuration
3. **Maintainability** - Clear structure, consistent docs
4. **Scalability** - Easy to add new modules
5. **Quality** - 80%+ accuracy on all extractions
6. **Speed** - <10 min per video processing time

---

## 📞 SUPPORT

**Documentation:** See `docs/` folder for detailed guides
**Issues:** Track in GitHub Issues
**Questions:** Check module README.md files first

---

**Last Updated:** 2025-10-08
**Version:** 1.0.0 (modular architecture established)
