# Category Intelligence Module Architecture v1.0

Complete end-to-end system for scalable market research deliverables.

## System Overview

```
PROJECT
├── 01-data-gathering/        Phase 1: Source data collection
├── 02-data-processing/       Phase 2: Consolidation & cleaning
├── 03-analysis/              Phase 3: Insights generation
├── 04-audit-trail/           Phase 4: Verification & sources
├── 05-final-mile/            Phase 5: HTML deliverables
├── _templates/               Master templates (frozen v1.0)
├── _orchestration/           Workflow automation
└── _archive/                 Legacy code & documentation
```

## Phase Descriptions

### 1. Data Gathering (01-data-gathering/)
**Purpose:** Collect raw data from multiple sources

**Subfolders:**
- `scrapers/` - Web scraping scripts
- `collectors/` - API collectors (YouTube, Reddit, TikTok)
- `sources/` - Source configuration files
- `logs/` - Scraping execution logs

**Output:** Raw JSON files → `02-data-processing/inputs/`
**Team:** Data Engineers
**Duration:** Hours to days

### 2. Data Processing (02-data-processing/)
**Purpose:** Clean, consolidate, deduplicate raw data

**Subfolders:**
- `consolidation/` - Multi-source merging
- `cleaning/` - Validation, deduplication
- `transformation/` - Format normalization
- `outputs/` - Consolidated datasets

**Output:** Clean JSON files → `03-analysis/inputs/`
**Team:** Data Engineers
**Duration:** 30-60 minutes

### 3. Analysis (03-analysis/)
**Purpose:** Extract insights, generate statistics

**Subfolders:**
- `scripts/` - Analysis algorithms
- `notebooks/` - Exploratory analysis
- `reports/` - Statistical findings
- `insights/` - Key takeaways

**Output:** Insight objects → `04-audit-trail/` verification
**Team:** Data Scientists / Analysts
**Duration:** 1-2 hours

### 4. Audit Trail (04-audit-trail/)
**Purpose:** Verify every claim against raw data

**Subfolders:**
- `verification/` - Source matching
- `sources/` - Citation references
- `validation/` - Fabrication detection
- `reports/` - 02-AUDIT_TRAIL_AND_SOURCES.html

**Output:** 02-AUDIT_TRAIL_AND_SOURCES.html → deliverables
**Team:** QA / Data Validation
**Duration:** 30 minutes

### 5. Final Mile (05-final-mile/)
**Purpose:** Generate production HTML deliverables

**Subfolders:**
- `templates/` - Master HTML (immutable)
- `styles/` - design-system.css (locked)
- `assets/` - SVG icons, logos
- `builds/` - Generated project outputs

**Output:** 03-EXECUTIVE_SUMMARY.html + CSS
**Team:** Frontend / Design
**Duration:** 20 minutes

## Master Template System (_templates/)

### HTML Template (master-template.html)
- **Status:** FROZEN v1.0 (immutable)
- **Variables:** Project-specific replaced via config
- **Structure:** Header → Sections → Footer
- **Navigation:** Auto-generated from config

### Design System (design-system.css)
- **Status:** FROZEN v1.0 (locked colors, fonts, spacing)
- **Colors:** Constrained palette (5 primary colors)
- **Typography:** Inter sans-serif only
- **Responsive:** Mobile breakpoint at 768px
- **Customization:** CSS variables override via config

### Icon Library (assets/)
- **Format:** SVG (scalable, crisp)
- **Sizes:** 16px (nav), 18px (tabs), 28px (logo)
- **Color:** Uses currentColor for inheritance
- **Set:** 20+ professional business icons

## Orchestration System (_orchestration/)

### Workflow Scripts
```
init-project.sh              Initialize new project
run-full-pipeline.sh         Execute all 5 phases
01-collect-data.sh           Phase 1 only
02-process-data.sh           Phase 2 only
03-run-analysis.sh           Phase 3 only
04-generate-audit.sh         Phase 4 only
05-build-deliverable.sh      Phase 5 only
```

### Configuration Management
- **Template:** `configs/project-template.yaml`
- **Per-Project:** `projects/ClientName/configs/project.yaml`
- **Overrides:** Only customize necessary fields
- **Versioning:** Track in git per project

### Quality Gates
1. **Data Validation:** Verify against raw sources
2. **Design Check:** HTML/CSS matches master template
3. **Audit Trail:** Every insight cited with sources
4. **Fabrication Detection:** Automated unsourced claim detection

## Data Flow

```
Raw Sources
    ↓
[01] Collect → JSON files
    ↓
[02] Process → Consolidated datasets
    ↓
[03] Analyze → Statistics & insights
    ↓
[04] Audit → Verification & sources
    ↓
[05] Build → HTML deliverables
    ↓
Final Output
├── 03-EXECUTIVE_SUMMARY.html
├── 02-AUDIT_TRAIL_AND_SOURCES.html
├── design-system.css
└── assets/
```

## Consistency Guarantees

**80% Identical Structure**
- Same HTML templates
- Same CSS framework
- Same icon library
- Same navigation patterns

**20% Project Variable Content**
- Client colors (within palette)
- Insights (project-specific)
- Data sources (project-specific)
- PDF/slides URLs (project-specific)

**Result:** Professional, consistent deliverables without rigidity

## File Organization Best Practices

### Naming Conventions
- Files: `lowercase-with-hyphens.ext`
- Folders: `##-sequence-descriptive-name/`
- Phases: `01-data-gathering`, `02-data-processing`, etc.

### Git Structure
- **main:** Production-ready code
- **feature/project-name:** Active project development
- **archive/:** Old project branches
- **.gitignore:** Excludes logs, large data, credentials

### Output Locations
- **Raw Data:** `09-raw-data/` (not git-tracked, .gitignore)
- **Processed:** `02-data-processing/outputs/`
- **Deliverables:** `05-final-mile/builds/ProjectName/`

## Extensibility

### Adding New Data Source
1. Create collector in `01-data-gathering/collectors/`
2. Add config to `project.yaml`
3. Integrate into `02-process-data.sh`

### Customizing Design
1. Override CSS variables in `project.yaml`
2. Stays within approved color palette
3. Master template remains untouched

### New Analysis Type
1. Add script to `03-analysis/scripts/`
2. Integrate into `03-run-analysis.sh`
3. Output results for audit verification

## Performance Targets

| Phase | Duration | Target System |
|-------|----------|----------------|
| Data Gathering | Varies | Parallel collectors |
| Data Processing | 30-60 min | Single machine |
| Analysis | 1-2 hours | Multi-core Python |
| Audit Trail | 30 min | Verification queries |
| Final Mile | 20 min | Template rendering |
| **Total** | **4-8 hours** | **Automated pipeline** |

## Security & Compliance

- No synthetic or fabricated data
- All claims verified against raw sources
- Complete audit trail maintained
- Source citations embedded
- Zero credentials in git (use .env)
- Data files in .gitignore

## Future Enhancements

1. **Agent-Based QA:** Automated quality gates
2. **CI/CD Integration:** Auto-run pipeline on commit
3. **MCP Server:** Persistent project metadata
4. **Multi-Client Dashboard:** Track all projects
5. **Template Versioning:** Rolling updates with backwards compatibility
