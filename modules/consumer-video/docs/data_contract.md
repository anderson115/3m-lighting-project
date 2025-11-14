# Consumer Video Module Data Contract

| Asset | Location | Owner | Notes |
|-------|----------|-------|-------|
| Raw video/audio | `/Volumes/DATA/media/<client>/<project>/raw/consumer-video/` | Client project | Large files kept off repo |
| Processed transcripts | `/Volumes/DATA/media/<client>/<project>/processed/consumer-video/` | Module pipeline | Intermediate files can be regenerated |
| Segment table | `storage/db/<client>_<project>__jtbd.segments` | Analytics DB | Fact table for downstream analysis |
| Insight exports | `clients/<client>/projects/<project>/docs/modules/consumer-video/` | Insights team | Markdown, slide specs, summaries |
| Run logs | `clients/<client>/projects/<project>/runs/consumer-video/<timestamp>/` | Ops | Include config snapshot + metrics |

Adhere to this contract to keep code portable between clients and to simplify audits.
