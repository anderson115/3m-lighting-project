#!/bin/bash
# Initialize new project structure

set -e

PROJECT_NAME="${1:-New Project}"
CATEGORY="${2:-Product Category}"
WORK_DIR="projects/$PROJECT_NAME"

echo "Initializing project: $PROJECT_NAME"
echo "Category: $CATEGORY"
echo ""

# Create project directory structure
mkdir -p "$WORK_DIR"/{01-data-gathering,02-data-processing,03-analysis,04-audit-trail,05-final-mile}/outputs
mkdir -p "$WORK_DIR"/{logs,configs}

# Copy template configuration
cp ../configs/project-template.yaml "$WORK_DIR/configs/project.yaml"

# Update project metadata in config
sed -i '' "s/Client Brand Name/$PROJECT_NAME/g" "$WORK_DIR/configs/project.yaml"
sed -i '' "s/Product Category/$CATEGORY/g" "$WORK_DIR/configs/project.yaml"

# Create initial README
cat > "$WORK_DIR/README.md" << EOF
# $PROJECT_NAME - Market Intelligence Project

**Category:** $CATEGORY
**Status:** Initialized
**Created:** $(date)

## Project Structure

- **01-data-gathering/** - Raw data collection
- **02-data-processing/** - Data consolidation and cleaning
- **03-analysis/** - Market insights and statistics
- **04-audit-trail/** - Verification and sources
- **05-final-mile/** - Final deliverables (HTML, CSS, etc.)
- **configs/** - Project configuration
- **logs/** - Execution logs

## Workflow

1. Gather data from sources
2. Process and consolidate
3. Run analysis
4. Generate audit trail
5. Build final deliverables

## Configuration

Edit \`configs/project.yaml\` to customize:
- Client colors and branding
- PDF and slides URLs
- Data sources
- Content sections

## Quality Gates

All claims must be:
- Verifiable against raw data
- Cited with sources
- Non-fabricated
- Consistent with design system
EOF

# Create .gitkeep for empty directories
find "$WORK_DIR" -type d -exec touch {}/.gitkeep \;

echo "✓ Project initialized at: $WORK_DIR"
echo ""
echo "Next steps:"
echo "1. Edit $WORK_DIR/configs/project.yaml"
echo "2. Run: ./workflows/01-collect-data.sh \"$PROJECT_NAME\""
echo ""
