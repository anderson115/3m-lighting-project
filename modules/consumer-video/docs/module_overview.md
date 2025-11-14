# Consumer Video / JTBD Module Overview

The consumer video module extracts structured Jobs-to-be-Done insights from qualitative video and transcript sources. Core capabilities include:

- Automated transcript ingestion and segmentation with speaker + activity tagging.
- Laddering logic that classifies functional, emotional, and social jobs.
- Insight synthesis that generates markdown summaries and presentation-ready assets.
- Configurable scoring to compare brand delivery across identified jobs.

## Inputs

1. **Transcript Sources** – JSON, TXT, or CSV files stored under `/Volumes/DATA/media/<client>/<project>/raw/consumer-video/`.
2. **Configuration** – Module settings in the client project (`configs/consumer_video.yaml`) controlling tiers, thresholds, and model paths.
3. **Reference Tables** – JTBD taxonomy and prompt templates located in `modules/consumer-video/config/`.

## Outputs

- Structured segment table persisted to PostgreSQL (`storage/db/<client>_<project>__jtbd`).
- Markdown and deck outlines exported to `clients/<client>/projects/<project>/docs/modules/consumer-video/`.
- Run logs and intermediate JSON/TSV files captured under `clients/<client>/projects/<project>/runs/consumer-video/`.
