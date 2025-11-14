#!/bin/bash
# Complete end-to-end pipeline execution

set -e

PROJECT_NAME="${1:-}"
if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: ./run-full-pipeline.sh \"Project Name\""
    exit 1
fi

WORK_DIR="projects/$PROJECT_NAME"
LOG_FILE="$WORK_DIR/logs/pipeline-$(date +%s).log"
mkdir -p "$WORK_DIR/logs"

echo "========================================" | tee "$LOG_FILE"
echo "Running Full Pipeline for: $PROJECT_NAME" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Phase 1: Data Gathering
echo "[1/5] Data Gathering..." | tee -a "$LOG_FILE"
if bash ./01-collect-data.sh "$PROJECT_NAME" >> "$LOG_FILE" 2>&1; then
    echo "✓ Data gathering complete" | tee -a "$LOG_FILE"
else
    echo "✗ Data gathering failed" | tee -a "$LOG_FILE"
    exit 1
fi
echo "" | tee -a "$LOG_FILE"

# Phase 2: Data Processing
echo "[2/5] Data Processing..." | tee -a "$LOG_FILE"
if bash ./02-process-data.sh "$PROJECT_NAME" >> "$LOG_FILE" 2>&1; then
    echo "✓ Data processing complete" | tee -a "$LOG_FILE"
else
    echo "✗ Data processing failed" | tee -a "$LOG_FILE"
    exit 1
fi
echo "" | tee -a "$LOG_FILE"

# Phase 3: Analysis
echo "[3/5] Running Analysis..." | tee -a "$LOG_FILE"
if bash ./03-run-analysis.sh "$PROJECT_NAME" >> "$LOG_FILE" 2>&1; then
    echo "✓ Analysis complete" | tee -a "$LOG_FILE"
else
    echo "✗ Analysis failed" | tee -a "$LOG_FILE"
    exit 1
fi
echo "" | tee -a "$LOG_FILE"

# Phase 4: Audit Trail
echo "[4/5] Generating Audit Trail..." | tee -a "$LOG_FILE"
if bash ./04-generate-audit.sh "$PROJECT_NAME" >> "$LOG_FILE" 2>&1; then
    echo "✓ Audit trail complete" | tee -a "$LOG_FILE"
else
    echo "✗ Audit trail generation failed" | tee -a "$LOG_FILE"
    exit 1
fi
echo "" | tee -a "$LOG_FILE"

# Phase 5: Final Mile
echo "[5/5] Building Deliverables..." | tee -a "$LOG_FILE"
if bash ./05-build-deliverable.sh "$PROJECT_NAME" >> "$LOG_FILE" 2>&1; then
    echo "✓ Deliverables complete" | tee -a "$LOG_FILE"
else
    echo "✗ Deliverable build failed" | tee -a "$LOG_FILE"
    exit 1
fi
echo "" | tee -a "$LOG_FILE"

# Final Summary
echo "========================================" | tee -a "$LOG_FILE"
echo "Pipeline Complete!" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "Deliverables:" | tee -a "$LOG_FILE"
echo "- 03-EXECUTIVE_SUMMARY.html" | tee -a "$LOG_FILE"
echo "- 02-AUDIT_TRAIL_AND_SOURCES.html" | tee -a "$LOG_FILE"
echo "- design-system.css" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "Log file: $LOG_FILE" | tee -a "$LOG_FILE"
echo ""
