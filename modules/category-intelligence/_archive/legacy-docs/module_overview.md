# Category Intelligence Module Overview

The category intelligence module aggregates secondary research, retailer assortment analysis, pricing benchmarks, and market sizing signals. It provides reusable pipelines for:

- Collecting market data from public economic series (FRED, Census) and industry reports.
- Normalizing retailer product catalogs and mapping them to a shared taxonomy.
- Scoring competitors and brands using configurable heuristics.
- Generating structured markdown and slide-ready summaries for strategic reviews.

## Required Inputs

1. **Configuration** (`configs/category_intel.yaml` in the client project) that sets brand lists, retailer targets, and market assumptions.
2. **Data Sources** specified via environment variables or secure credential files (e.g., API tokens, scraper settings).
3. **Output Paths** defined per client project, typically under `clients/<client>/projects/<project>/runs/category-intelligence/`.

## Outputs

- Normalized datasets ready for storage in PostgreSQL (`storage/db/<schema>`).
- Exported CSV/Parquet extracts for ad-hoc analysis.
- Markdown briefs summarizing key insights.
- Optional slide specifications for downstream presentation tooling.

Keep this document updated as new capabilities or dependencies are introduced.
