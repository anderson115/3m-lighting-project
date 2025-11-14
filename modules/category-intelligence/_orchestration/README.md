# Orchestration & Workflow Automation

End-to-end workflow management for repeatable client deliverables.

## Workflow Phases

### Phase 1: Data Gathering (01-data-gathering/)
- **Run:** `./workflows/01-collect-data.sh PROJECT_NAME`
- **Inputs:** Scraping configs, source URLs
- **Outputs:** Raw JSON files in 09-raw-data/
- **Duration:** Variable (hours to days)

### Phase 2: Data Processing (02-data-processing/)
- **Run:** `./workflows/02-process-data.sh PROJECT_NAME`
- **Inputs:** Raw JSON files
- **Outputs:** Consolidated, cleaned datasets
- **Duration:** 30-60 minutes

### Phase 3: Analysis (03-analysis/)
- **Run:** `./workflows/03-run-analysis.sh PROJECT_NAME`
- **Inputs:** Processed data, PDF presentation
- **Outputs:** Statistics, insights, findings
- **Duration:** 1-2 hours

### Phase 4: Audit Trail (04-audit-trail/)
- **Run:** `./workflows/04-generate-audit.sh PROJECT_NAME`
- **Inputs:** Analysis results, raw data verification
- **Outputs:** 02-AUDIT_TRAIL_AND_SOURCES.html
- **Duration:** 30 minutes

### Phase 5: Final Mile (05-final-mile/)
- **Run:** `./workflows/05-build-deliverable.sh PROJECT_NAME`
- **Inputs:** Project config, audit trail, analysis
- **Outputs:** 03-EXECUTIVE_SUMMARY.html, styled assets
- **Duration:** 20 minutes

## Quick Start for New Project

```bash
# Initialize new project
./workflows/init-project.sh "Client Name" "Product Category"

# Run full pipeline
./workflows/run-full-pipeline.sh "Client Name"

# Or run individual phases
./workflows/01-collect-data.sh "Client Name"
./workflows/02-process-data.sh "Client Name"
./workflows/03-run-analysis.sh "Client Name"
./workflows/04-generate-audit.sh "Client Name"
./workflows/05-build-deliverable.sh "Client Name"
```

## Quality Gates

1. **Data Validation:** All claims require source verification
2. **Design Consistency:** HTML/CSS checked against master template
3. **Audit Verification:** Every statistic cross-referenced to PDF
4. **Fabrication Check:** Automated detection of unsourced insights

## Configuration Management

- Store project configs in `configs/`
- Use `project-template.yaml` as baseline
- Override only necessary fields
- Track config versions in git
