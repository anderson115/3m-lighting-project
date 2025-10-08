# 🚀 DEVELOPMENT PLAN - YouTube Research Platform
**Date:** 2025-10-06
**Phase:** Backend API Development (Frontend TBD)
**Status:** In Progress

---

## 📊 **PROJECT OVERVIEW**

### **Objective**
Build subscription-based YouTube research automation backend that:
1. Downloads and analyzes YouTube videos
2. Extracts JTBD insights using multimodal AI
3. Provides tier-based API access (Standard/Pro/Admin)
4. **Prepares for future frontend integration** (not in current scope)

### **Current Scope: Backend Only**
- ✅ YouTube data ingestion
- ✅ Multimodal AI processing (Whisper + LLaVA + LLM)
- ✅ Tiered API model access
- ✅ JSON/CSV/HTML output
- ❌ Web UI (future phase)
- ❌ User authentication (future phase)
- ❌ Real-time dashboard (future phase)

---

## 🎯 **YOUTUBE DATA SOURCE IMPLEMENTATION**

### **Status: Partially Implemented**

**What Exists:**
- ✅ `scripts/video_downloader.py` - YouTube download via yt-dlp
- ✅ YouTube API key in `.env`
- ✅ Whisper transcription working
- ✅ LLaVA visual analysis working

**What's Missing:**
- ❌ `core/data_sources/youtube.py` - Centralized YouTube module
- ❌ Search query API integration
- ❌ Playlist/channel batch processing
- ❌ Video metadata extraction
- ❌ Rate limit handling
- ❌ Deduplication logic

---

## 📁 **REQUIRED FILE STRUCTURE**

### **Core Backend Structure**

```
video-research-platform/
├── core/
│   ├── data_sources/           # ← NEEDS CREATION
│   │   ├── __init__.py
│   │   ├── youtube.py          # YouTube API client
│   │   └── validators.py       # Video/data validation
│   │
│   ├── pipeline/
│   │   ├── __init__.py         ✅ Exists
│   │   ├── perception.py       # ← NEEDS CREATION (Whisper + LLaVA)
│   │   ├── extraction.py       ✅ Exists (LLM JTBD)
│   │   └── reporting.py        # ← NEEDS CREATION (HTML/JSON/CSV)
│   │
│   ├── models/
│   │   ├── __init__.py         ✅ Exists
│   │   ├── model_registry.py   ✅ Exists (All API models)
│   │   └── tier_manager.py     ✅ Exists (Subscription tiers)
│   │
│   └── api/                    # ← FUTURE: REST API endpoints
│       ├── __init__.py
│       ├── routes.py           # FastAPI routes
│       ├── auth.py             # Authentication (future)
│       └── schemas.py          # Pydantic models
│
├── clients/
│   └── 3m_lighting/
│       ├── config.yaml         ✅ Exists
│       ├── prompts.yaml        ✅ Exists
│       └── search_queries.yaml # ← NEEDS CREATION
│
├── scripts/
│   ├── run_research.py         # ← NEEDS CREATION (Main pipeline)
│   ├── video_downloader.py     ✅ Exists
│   └── validate_setup.py       # ← NEEDS CREATION
│
└── config/
    ├── model_paths.yaml        ✅ Exists
    └── model_tiers.yaml        ✅ Exists
```

---

## 🔧 **PHASE 1: YOUTUBE DATA SOURCE (CURRENT)**

### **Module: `core/data_sources/youtube.py`**

**Purpose:** Centralized YouTube API interaction

**Required Functions:**
```python
class YouTubeDataSource:
    def __init__(self, api_key: str):
        """Initialize YouTube Data API v3 client"""

    def search_videos(
        self,
        query: str,
        max_results: int = 50,
        order: str = 'relevance'
    ) -> List[Dict]:
        """
        Search YouTube videos by keyword

        Returns:
            List of video metadata (id, title, description, stats)
        """

    def get_video_metadata(self, video_id: str) -> Dict:
        """
        Get detailed metadata for a video

        Returns:
            {
                'id': str,
                'title': str,
                'description': str,
                'channel': str,
                'published_at': str,
                'duration': int (seconds),
                'view_count': int,
                'like_count': int,
                'comment_count': int
            }
        """

    def download_video(
        self,
        video_id: str,
        output_dir: Path,
        quality: str = 'best'
    ) -> Path:
        """
        Download video using yt-dlp

        Returns:
            Path to downloaded video file
        """

    def extract_audio(
        self,
        video_path: Path,
        output_dir: Path
    ) -> Path:
        """
        Extract audio track to WAV for Whisper

        Returns:
            Path to audio file
        """

    def is_duplicate(
        self,
        video_id: str,
        existing_videos: List[str]
    ) -> bool:
        """Check if video already processed"""
```

**Dependencies:**
```python
import os
from pathlib import Path
from typing import List, Dict, Optional
import yt_dlp
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
```

**Integration Points:**
- Input: Search queries from `clients/{client}/search_queries.yaml`
- Output: Video files + metadata to `data/{client}/videos/`
- Used by: `core/pipeline/perception.py`

---

## 🔧 **PHASE 2: PERCEPTION PIPELINE**

### **Module: `core/pipeline/perception.py`**

**Purpose:** Multimodal analysis (audio + visual)

**Required Functions:**
```python
class PerceptionPipeline:
    def __init__(self, model_registry: ModelRegistry):
        """Initialize Whisper + LLaVA models"""

    def analyze_video(
        self,
        video_path: Path,
        output_dir: Path
    ) -> Dict:
        """
        Full multimodal analysis

        Returns:
            {
                'transcription': {...},  # Whisper output
                'visual_analyses': [...],  # LLaVA frames
                'metadata': {...}
            }
        """

    def transcribe_audio(
        self,
        audio_path: Path
    ) -> Dict:
        """
        Whisper transcription

        Returns:
            {
                'text': str,
                'segments': [
                    {
                        'start': float,
                        'end': float,
                        'text': str
                    }
                ],
                'language': str,
                'duration': float
            }
        """

    def analyze_frames(
        self,
        video_path: Path,
        interval: int = 30
    ) -> List[Dict]:
        """
        LLaVA visual analysis at intervals

        Returns:
            [
                {
                    'timestamp': float,
                    'frame_path': str,
                    'analysis': str (LLaVA description)
                }
            ]
        """

    def extract_keyframes(
        self,
        video_path: Path,
        output_dir: Path,
        interval: int = 30
    ) -> List[Path]:
        """Extract frames every N seconds"""
```

**Integration Points:**
- Input: Video files from YouTube data source
- Output: Analysis JSON to `data/{client}/analysis/{video_id}/`
- Used by: `core/pipeline/extraction.py`

---

## 🔧 **PHASE 3: REPORTING MODULE**

### **Module: `core/pipeline/reporting.py`**

**Purpose:** Generate client deliverables

**Required Functions:**
```python
class ReportGenerator:
    def __init__(self, client_config: Dict):
        """Initialize with client branding/config"""

    def generate_html_report(
        self,
        insights: List[Dict],
        output_path: Path
    ) -> Path:
        """
        HTML report with insights

        Sections:
        - Executive summary
        - Pain points (table + visualizations)
        - Solutions demonstrated
        - 3M product adjacencies
        - Verbatim quotes
        - Video references
        """

    def generate_json_export(
        self,
        insights: List[Dict],
        output_path: Path
    ) -> Path:
        """
        Structured JSON for API consumption

        Format:
        {
            "client": str,
            "generated_at": ISO datetime,
            "videos_analyzed": int,
            "insights": {
                "pain_points": [...],
                "solutions": [...],
                "adjacencies": [...],
                "verbatims": [...]
            },
            "metadata": {...}
        }
        """

    def generate_csv_export(
        self,
        insights: List[Dict],
        output_dir: Path
    ) -> List[Path]:
        """
        CSV files for Excel analysis

        Files:
        - pain_points.csv
        - solutions.csv
        - adjacencies.csv
        - verbatims.csv
        """
```

**Integration Points:**
- Input: Extracted insights from `extraction.py`
- Output: Reports to `clients/{client}/reports/`
- **API-Ready:** JSON output format ready for REST API

---

## 🔧 **PHASE 4: MAIN PIPELINE ORCHESTRATOR**

### **Script: `scripts/run_research.py`**

**Purpose:** Main entry point for research execution

**CLI Interface:**
```bash
# Run full research pipeline
python scripts/run_research.py \
    --client 3m_lighting \
    --mode production \
    --tier admin \
    --max-videos 100

# Preflight test (3 videos)
python scripts/run_research.py \
    --client 3m_lighting \
    --mode preflight \
    --tier pro

# Search only (no processing)
python scripts/run_research.py \
    --client 3m_lighting \
    --search-only \
    --save-results queries.json
```

**Workflow:**
```python
def main(client: str, mode: str, tier: str, max_videos: int):
    """
    1. Load client configuration
    2. Search YouTube videos
    3. Download + deduplicate
    4. Perception analysis (Whisper + LLaVA)
    5. JTBD extraction (tier-based LLM)
    6. Generate reports
    7. Save to archives
    """
```

**Progress Tracking:**
```python
# Real-time progress output
📥 Searching YouTube...
   Found 127 videos matching queries
   Filtered to 100 (deduplicated, sorted by relevance)

📦 Downloading videos... [████████░░] 80/100 (12 min remaining)

🧠 Processing with Gemini 2.0 Flash (Pro tier)
   Video 1/100: LED Shelf Lighting [✓ 28s]
   Video 2/100: Under Cabinet Install [✓ 31s]
   ...

📊 Generating reports...
   ✓ HTML: reports/3m_lighting_2025-10-06.html
   ✓ JSON: reports/3m_lighting_2025-10-06.json
   ✓ CSV: reports/pain_points.csv

✅ Complete! 100 videos analyzed in 1.2 hours
```

---

## 🔧 **PHASE 5: API PREPARATION (Backend Ready for Frontend)**

### **Module: `core/api/routes.py`** (Future Phase)

**Purpose:** REST API endpoints for frontend

**Planned Endpoints:**
```python
# Research Jobs
POST   /api/research/create
GET    /api/research/{job_id}
GET    /api/research/{job_id}/progress
GET    /api/research/{job_id}/results

# Video Management
GET    /api/videos/search
POST   /api/videos/analyze
GET    /api/videos/{video_id}/insights

# Client Management
GET    /api/clients/{client_id}/config
GET    /api/clients/{client_id}/reports
POST   /api/clients/{client_id}/queries

# Subscription Tiers
GET    /api/tiers
GET    /api/user/tier
GET    /api/user/usage
```

**Response Format (JSON):**
```json
{
  "status": "success|error|processing",
  "data": {...},
  "metadata": {
    "tier": "pro",
    "cost": 0.75,
    "processing_time": 28.5
  }
}
```

**Authentication (Future):**
- JWT tokens
- API key authentication
- Tier validation middleware

---

## 📊 **DATA FLOW DIAGRAM**

```
┌─────────────────┐
│  YouTube API    │
│  (Data Source)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Video Download  │  ← scripts/video_downloader.py
│ + Metadata      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Perception    │  ← core/pipeline/perception.py
│ Whisper + LLaVA │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Extraction    │  ← core/pipeline/extraction.py
│  (Tier-based)   │  ← core/models/tier_manager.py
│ Llama|Gemini|..│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Reporting     │  ← core/pipeline/reporting.py
│ HTML/JSON/CSV   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Client Reports │
│  + JSON API     │  → Future: REST API endpoints
└─────────────────┘
```

---

## ✅ **IMPLEMENTATION CHECKLIST**

### **Phase 1: YouTube Data Source (Priority 1)**
- [ ] Create `core/data_sources/__init__.py`
- [ ] Implement `core/data_sources/youtube.py`
  - [ ] Search API integration
  - [ ] Video metadata extraction
  - [ ] Download wrapper (yt-dlp)
  - [ ] Audio extraction (FFmpeg)
  - [ ] Deduplication logic
- [ ] Create `clients/3m_lighting/search_queries.yaml`
- [ ] Test: Search → Download → Validate

### **Phase 2: Perception Pipeline (Priority 2)**
- [ ] Create `core/pipeline/perception.py`
  - [ ] Whisper transcription
  - [ ] LLaVA frame analysis
  - [ ] Temporal alignment
  - [ ] JSON output format
- [ ] Integrate with model_registry.py
- [ ] Test: Video → Transcript + Visual analysis

### **Phase 3: Reporting Module (Priority 3)**
- [ ] Create `core/pipeline/reporting.py`
  - [ ] HTML template (Jinja2)
  - [ ] JSON export (API-ready)
  - [ ] CSV export (Excel-ready)
- [ ] Add client branding support
- [ ] Test: Insights → HTML/JSON/CSV

### **Phase 4: Main Pipeline (Priority 4)**
- [ ] Create `scripts/run_research.py`
  - [ ] CLI argument parsing
  - [ ] Orchestration logic
  - [ ] Progress tracking
  - [ ] Error handling
- [ ] Integrate tier_manager for model selection
- [ ] Add cost tracking per tier
- [ ] Test: End-to-end pipeline

### **Phase 5: API Prep (Priority 5 - Future)**
- [ ] Design REST API schema
- [ ] Create FastAPI routes
- [ ] Add authentication middleware
- [ ] Document API endpoints
- [ ] Create OpenAPI spec

---

## 📚 **EXISTING VS NEW DOCUMENTATION**

### **Documents to KEEP (Current State)**
1. ✅ `README.md` - High-level overview
2. ✅ `TIERED_MODEL_DEPLOYMENT.md` - Subscription system (latest)
3. ✅ `MODEL_EVALUATION_FINAL_REPORT.md` - Model comparison results
4. ✅ `config/model_tiers.yaml` - Tier configuration (active)

### **Documents to ARCHIVE (Superseded)**
1. ⚠️ `COMPLETE_MODEL_ANALYSIS.md` → Superseded by `MODEL_EVALUATION_FINAL_REPORT.md`
2. ⚠️ `MODEL_OPTIMIZATION_REPORT.md` → Superseded by `MODEL_EVALUATION_FINAL_REPORT.md`
3. ⚠️ `PHASE_2_COMPLETE.md` → Historical, move to docs/archive/
4. ⚠️ `OBJECTIVE_EVALUATION.md` → Historical, move to docs/archive/

### **Documents to CREATE**
1. 🆕 `DEVELOPMENT_PLAN.md` (this file) - Current dev roadmap
2. 🆕 `API_SPECIFICATION.md` - REST API design (future phase)
3. 🆕 `YOUTUBE_DATA_SOURCE.md` - YouTube integration details

---

## 🎯 **IMMEDIATE NEXT STEPS**

### **This Session:**
1. Create `core/data_sources/youtube.py`
2. Create `clients/3m_lighting/search_queries.yaml`
3. Test YouTube search + download
4. Archive superseded documentation

### **Next Session:**
1. Implement `core/pipeline/perception.py`
2. Create `scripts/run_research.py`
3. End-to-end pipeline test
4. Generate first production report

---

## 🚨 **FRONTEND FUTURE CONSIDERATIONS**

### **API-Ready Design Principles**
1. **JSON-First:** All outputs in structured JSON
2. **Stateless:** Backend doesn't track frontend state
3. **Idempotent:** Safe to retry operations
4. **Paginated:** Large result sets paginated
5. **Versioned:** API v1, v2 compatibility

### **Planned Frontend Features (Out of Scope Now)**
- Dashboard for job monitoring
- User authentication/registration
- Tier selection UI
- Report viewer (HTML/PDF)
- Video player with insight timeline
- Search query builder
- Cost/usage analytics

### **Backend → Frontend Data Contract**
```json
{
  "research_job": {
    "id": "uuid",
    "client": "3m_lighting",
    "status": "completed",
    "tier": "pro",
    "videos_analyzed": 100,
    "total_cost": 0.75,
    "created_at": "2025-10-06T12:00:00Z",
    "completed_at": "2025-10-06T13:15:00Z"
  },
  "insights": {
    "pain_points": [...],
    "solutions": [...],
    "adjacencies": [...]
  },
  "reports": {
    "html_url": "/reports/3m_lighting_2025-10-06.html",
    "json_url": "/api/research/job-123/export.json",
    "csv_url": "/api/research/job-123/export.csv"
  }
}
```

---

**Status:** ✅ Backend design complete, YouTube module implementation ready to begin
**Next Milestone:** YouTube data source + perception pipeline (Phases 1-2)
**ETA:** 2-3 hours development + testing
