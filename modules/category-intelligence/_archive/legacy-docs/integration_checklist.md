# Category Intelligence Integration Checklist

1. **Project Setup**
   - Confirm the client project folder (e.g., `clients/<client>/projects/<project>/`) exists with `configs/` and `runs/` subdirectories.
2. **Configuration**
   - Copy the template config and adjust retailers, brand aliases, and currency assumptions.
   - Store sensitive tokens in `configs/credentials/` and reference them via environment variables.
3. **Data Paths**
   - Map raw scrape output to `/Volumes/DATA/media/<client>/<project>/raw/category-intel/`.
   - Define processed output paths in PostgreSQL under `storage/db/<client>_<project>__category`.
4. **Execution**
   - Run the ETL scripts from `modules/category-intelligence/src/` (use virtualenv + requirements file).
   - Log each run in `clients/<client>/projects/<project>/runs/category-intelligence/<timestamp>/`.
5. **Handover**
   - Publish cleaned datasets and markdown reports to `clients/<client>/projects/<project>/docs/modules/category-intelligence/`.
   - Update the project `README.md` with links to the latest outputs.
6. **Deliverable Package**
   - Assemble the client payload in the project `deliverables/` folder: narrative report (Markdown), HTML slide flow, appendix, and a raw-data manifest.
   - Ensure the manifest links every appendix component to the exact files on `/Volumes/DATA/...` and to the Postgres tables (via `project_key`).
   - Keep the description flexible—document the paths and sources, but avoid hard-coding category-specific assumptions.
