# Category Intelligence (Streamlined)

This module now follows a minimal, modular layout that Codex can maintain easily.

## Structure

```
category-intelligence/
├── archive/legacy/            # Previous implementation retained for reference
├── claude-category-intel.md   # Development blueprint (updated)
├── docs/                      # Architecture, data source guidance (moved from legacy files)
├── outputs/                   # Empty by default; report exports land here
└── src/
    ├── pipeline/              # Brand + product orchestrators
    ├── reporting/             # Markdown/deck renderers
    └── storage/               # Postgres and other persistence adapters
```

## Current Scope (Phase 1)
- Implement live brand collectors using retailer feeds and search APIs.
- Aggregate top products per retailer with transparent ordering and citations.
- Persist data to `/Volumes/DATA/…` Postgres + parquet caches.
- Generate lightweight Markdown summaries (full HTML/PPTX deferred until Phase 2).

## Deferred (Phase 2)
- Keyword opportunity engine (multi-source harvesting + novelty scoring).
- Advanced visualization/deck automation.
- Consumer-insight linkage.

See `claude-category-intel.md` for the detailed blueprint and migration notes.
