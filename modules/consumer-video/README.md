# Consumer Video Module

Reusable toolkit for processing consumer-generated lighting videos, extracting Jobs-to-be-Done ladders, and producing insight packages. Project-specific assets now live under each client project (for example, `clients/3m/projects/lighting-2025/`).

## Repository Layout

```
modules/consumer-video/
├── config/                  # Shared configuration templates
├── data/                    # Placeholder only (no client data committed)
├── docs/                    # Integration + usage documentation
├── scripts/                 # CLI wrappers and orchestration helpers
├── *.py                     # Core processing modules
└── requirements.txt         # (Add as needed per environment)
```

## Execution Flow

1. Stage raw media on `/Volumes/DATA/media/<client>/<project>/raw/consumer-video/`.
2. Copy the template config into `clients/<client>/projects/<project>/configs/consumer_video.yaml` and adjust thresholds.
3. Run `process_batch.py --config <path>` from this directory (or orchestrate via Airflow/Prefect).
4. Persist outputs to PostgreSQL (`storage/db/<client>_<project>__jtbd`) and write exports to the project `runs/` + `docs/` folders.

## Reference Locations

- **Outputs:** `clients/<client>/projects/<project>/docs/modules/consumer-video/`
- **Run Logs:** `clients/<client>/projects/<project>/runs/consumer-video/`
- **Large Files:** `/Volumes/DATA/media/<client>/<project>/`

Keep this module focused on reusable code. Store engagement-specific artefacts in the project tree.
