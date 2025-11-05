#!/bin/bash

# Cleanup script for brand-perceptions iterations
# Keeps only final production files referenced in ALL_SLIDES_MASTER.html

ARCHIVE_DIR="archive/iterations_cleanup_$(date +%Y%m%d)"

echo "🗂️  Creating archive directory: $ARCHIVE_DIR"
mkdir -p "$ARCHIVE_DIR"

# Files to KEEP (final production files)
KEEP_HTML=(
  "ALL_SLIDES_MASTER.html"
  "slide1_FINAL.html"
  "SLIDE2_DEFAULT.html"
  "SLIDE2_KEYNOTE.html"
  "SLIDE3_DEFAULT.html"
  "SLIDE3_KEYNOTE.html"
  "SLIDE4_DEFAULT.html"
  "SLIDE4_KEYNOTE.html"
  "SLIDE5_DEFAULT.html"
  "SLIDE5_KEYNOTE.html"
  "SLIDE6_DEFAULT.html"
  "SLIDE6_KEYNOTE.html"
)

KEEP_MD=(
  "TEMPLATE_SYSTEM_MASTER.md"
  "DESIGN_SPECIFICATIONS.md"
  "SLIDE_TESTS_v3.md"
  "README.md"
)

KEEP_PPTX=(
  "3M_BrandPerceptions_BainQuality_FINAL_20251103_014114.pptx"
)

# Function to check if file is in keep list
should_keep() {
  local file=$1
  for keep in "${KEEP_HTML[@]}" "${KEEP_MD[@]}" "${KEEP_PPTX[@]}"; do
    if [ "$file" = "$keep" ]; then
      return 0
    fi
  done
  return 1
}

echo ""
echo "📦 Moving iteration files to archive..."

# Archive HTML files
for file in *.html; do
  if [ -f "$file" ]; then
    if ! should_keep "$file"; then
      echo "  📄 Archiving: $file"
      mv "$file" "$ARCHIVE_DIR/"
    fi
  fi
done

# Archive markdown documentation (keeping only essential)
for file in *.md; do
  if [ -f "$file" ]; then
    if ! should_keep "$file"; then
      echo "  📄 Archiving: $file"
      mv "$file" "$ARCHIVE_DIR/"
    fi
  fi
done

# Archive test Python scripts
for file in *.py; do
  if [ -f "$file" ]; then
    echo "  🐍 Archiving: $file"
    mv "$file" "$ARCHIVE_DIR/"
  fi
done

# Archive test PPTX files (keep only FINAL)
for file in *.pptx; do
  if [ -f "$file" ]; then
    if ! should_keep "$file"; then
      echo "  📊 Archiving: $file"
      mv "$file" "$ARCHIVE_DIR/"
    fi
  fi
done

# Archive PDFs if any
for file in *.pdf; do
  if [ -f "$file" ]; then
    echo "  📄 Archiving: $file"
    mv "$file" "$ARCHIVE_DIR/"
  fi
done

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📁 Files kept (production):"
for file in "${KEEP_HTML[@]}" "${KEEP_MD[@]}" "${KEEP_PPTX[@]}"; do
  if [ -f "$file" ]; then
    echo "  ✓ $file"
  fi
done

echo ""
echo "🗂️  Archived files location:"
echo "  $ARCHIVE_DIR"
echo ""
echo "📊 Summary:"
echo "  HTML kept: ${#KEEP_HTML[@]}"
echo "  Markdown kept: ${#KEEP_MD[@]}"
echo "  Total archived: $(ls -1 $ARCHIVE_DIR | wc -l)"
