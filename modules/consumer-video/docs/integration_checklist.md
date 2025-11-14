# Consumer Video Module Integration Checklist

1. **Provision Storage**
   - Ensure `/Volumes/DATA/media/<client>/<project>/raw/consumer-video/` contains source files.
   - Create a PostgreSQL schema `jtbd` within `storage/db/<client>_<project>`.
2. **Configure Module**
   - Copy `modules/consumer-video/config/templates/consumer_video.yaml` into the project `configs/` folder.
   - Update processing tier, language model paths, and confidence thresholds.
3. **Execute Pipeline**
   - Use the orchestration scripts in `modules/consumer-video/scripts/` or call `process_batch.py` with project config.
   - Direct all output paths to `clients/<client>/projects/<project>/runs/consumer-video/<timestamp>/`.
4. **Synthesize Outputs**
   - Push generated markdown/decks into `clients/<client>/projects/<project>/docs/modules/consumer-video/`.
   - Register artifacts in the project README and audit ledger.
5. **Quality Review**
   - Validate job tagging counts against manual spot checks.
   - Update the `jobs_framework.md` in the project docs with any new insights.
