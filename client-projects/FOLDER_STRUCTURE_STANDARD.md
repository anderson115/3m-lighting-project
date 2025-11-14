# Client Projects Folder Structure Standard

## Standard Format

All client projects in `client-projects/` follow this consistent 5-phase architecture:

```
client-projects/[PROJECT_NAME]/
├── 00-configs/           Project configuration, metadata, admin materials
├── 01-raw-data/          Raw collected data from all sources
├── 02-data-processing/   Cleaned, consolidated, deduplicated data
├── 03-analysis/          Statistical insights, analysis output, notebooks
├── 04-audit-trail/       Source verification, citations, validation reports
├── 05-final-mile/        Design briefs, final deliverables (HTML, PDF, etc.)
├── 99-archive/           Old iterations, legacy work, superseded versions
└── README.md             Project overview (optional)
```

## Phase Descriptions

### 00-configs/
- **Purpose:** Project metadata, configuration files, settings
- **Contents:**
  - `project.yaml` - Master configuration (from template)
  - `admin/` - Administrative materials, invoices, contacts
  - Social media configs (Instagram, Reddit, X, TikTok)
  - Spreadsheets and reference materials
- **Ownership:** Project manager / client liaison

### 01-raw-data/
- **Purpose:** Original collected data (unchanged from sources)
- **Contents:**
  - JSON files from YouTube, Reddit, Instagram, TikTok collection
  - Raw product data from retailers (Amazon, Walmart, Lowe's)
  - Video/image metadata
  - Data manifests
- **Ownership:** Data engineers
- **Note:** Immutable - source of truth for auditing

### 02-data-processing/
- **Purpose:** Cleaned and consolidated datasets
- **Contents:**
  - Deduplicated records
  - Merged multi-source data
  - Normalized formats
  - Processing scripts and logs
- **Ownership:** Data engineers
- **Duration:** 30-60 minutes per cycle

### 03-analysis/
- **Purpose:** Statistical insights and exploratory analysis
- **Contents:**
  - Analysis output (JSON, CSV)
  - Jupyter notebooks
  - Statistical reports
  - Keyword frequency analysis
  - Sentiment analysis results
- **Ownership:** Data scientists / analysts
- **Duration:** 1-2 hours per cycle

### 04-audit-trail/
- **Purpose:** Verification and source documentation
- **Contents:**
  - Audit reports (HTML, Markdown, JSON)
  - Source citations and verification results
  - Validation reports
  - Fabrication detection results
- **Ownership:** QA / data validation team
- **Duration:** 30 minutes per cycle

### 05-final-mile/
- **Purpose:** Production-ready deliverables
- **Contents:**
  - `deliverables/` - Final HTML/PDF reports
  - `design-briefs/` - Design specifications and briefs
  - CSS, JavaScript, assets
  - Presentation materials
- **Ownership:** Frontend / design team
- **Duration:** 20 minutes per cycle

### 99-archive/
- **Purpose:** Historical versions and legacy work
- **Contents:**
  - `legacy-docs/` - Superseded documentation
  - `runs/` - Previous execution logs
  - Old iterations of analysis
  - Deprecated scripts
- **Ownership:** Reference only
- **Note:** Not used in current pipeline

## Projects Following This Standard

### ✓ garage-organizer
- Garage organization products market intelligence
- Status: Complete with standardized folders
- Final deliverables: 3M Garage Organization presentation

### ✓ 251106-3m-accent-lighting
- 3M accent lighting category intelligence
- Status: Complete with standardized folders
- Data sources: YouTube, Reddit, Instagram, TikTok, retail

## Benefits of This Standard

1. **Consistency** - Same structure across all projects
2. **Scalability** - New projects can be initialized with template
3. **Clarity** - Phases map to the 5-phase architecture
4. **Automation** - Scripts expect this folder layout
5. **Auditing** - Clear separation of raw vs. processed vs. final
6. **Maintainability** - Easy to locate data in any phase

## New Project Initialization

When starting a new client project:

```bash
cd modules/category-intelligence/_orchestration/workflows
./init-project.sh "Client Name" "Product Category"
```

This automatically creates the standard folder structure and configuration template.

---

**Updated:** November 13, 2025
**Version:** 1.0
**Standard applies to:** All client-projects/
