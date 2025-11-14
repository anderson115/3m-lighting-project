# Client Projects

Each subfolder corresponds to a distinct client project or engagement.

## Naming Convention

Projects use `yymmdd-client-workstream` format:
- `251106-3m-accent-lighting` - 2025-11-06, 3M, accent lighting research
- `garage-organizer` - Category intelligence for garage organization

Archived projects live under `archive/`

## Folder Structure Standard

All client projects follow the **5-Phase Architecture**:

```
[PROJECT_NAME]/
├── 00-configs/           Project configuration & metadata
├── 01-raw-data/          Collected source data (unchanged)
├── 02-data-processing/   Cleaned & consolidated data
├── 03-analysis/          Statistical insights & analysis
├── 04-audit-trail/       Source verification & validation
├── 05-final-mile/        Design briefs & deliverables
└── 99-archive/           Legacy work & old iterations
```

**See:** [`FOLDER_STRUCTURE_STANDARD.md`](./FOLDER_STRUCTURE_STANDARD.md) for complete documentation.

## Quick Reference

| Phase | Purpose | Owner | Duration |
|-------|---------|-------|----------|
| 00-configs | Configuration & metadata | PM | — |
| 01-raw-data | Collect data | Engineers | Hours-Days |
| 02-data-processing | Clean & consolidate | Engineers | 30-60 min |
| 03-analysis | Extract insights | Analysts | 1-2 hours |
| 04-audit-trail | Verify claims | QA | 30 min |
| 05-final-mile | Build deliverables | Design/Frontend | 20 min |

## Initialize New Project

```bash
cd modules/category-intelligence/_orchestration/workflows
./init-project.sh "Client Name" "Product Category"
```

This creates the standard folder structure and configuration template automatically.

## Current Projects

- **garage-organizer** - Garage organization products market research
- **251106-3m-accent-lighting** - 3M accent lighting category intelligence
