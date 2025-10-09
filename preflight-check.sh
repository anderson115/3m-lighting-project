#!/bin/bash
# Comprehensive Preflight Check
# Validates: folders, files, docs, TARS volume, dependencies

echo "=========================================="
echo "3M LIGHTING PROJECT - PREFLIGHT CHECK"
echo "=========================================="
echo ""

ERRORS=0
WARNINGS=0

# Check 1: Project structure
echo "✓ CHECK 1: Project Structure"
if [ -d "config" ] && [ -d "scripts" ] && [ -d "data" ] && [ -d "docs" ]; then
    echo "  ✅ Core directories exist"
else
    echo "  ❌ Missing core directories"
    ERRORS=$((ERRORS + 1))
fi

# Check 2: TARS volume
echo ""
echo "✓ CHECK 2: TARS Volume"
if [ -d "/Volumes/TARS/llm-models" ]; then
    echo "  ✅ TARS volume mounted"
    echo "  📊 Models on TARS:"
    du -sh /Volumes/TARS/llm-models/* 2>/dev/null | head -10 || echo "  ⚠️  No models found"
else
    echo "  ❌ TARS volume not mounted"
    ERRORS=$((ERRORS + 1))
fi

# Check 3: Key configuration files
echo ""
echo "✓ CHECK 3: Configuration Files"
for file in config/model_paths.yaml requirements.txt .gitignore README.md; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ Missing: $file"
        ERRORS=$((ERRORS + 1))
    fi
done

# Check 4: Documentation consistency
echo ""
echo "✓ CHECK 4: Documentation"
DOC_COUNT=$(find docs -name "*.md" -type f 2>/dev/null | wc -l)
echo "  📄 Found $DOC_COUNT documentation files"
if [ "$DOC_COUNT" -gt 5 ]; then
    echo "  ✅ Documentation exists"
else
    echo "  ⚠️  Limited documentation"
    WARNINGS=$((WARNINGS + 1))
fi

# Check 5: Virtual environment
echo ""
echo "✓ CHECK 5: Virtual Environment"
if [ -d "venv" ]; then
    echo "  ✅ venv exists"
    if [ -f "venv/bin/python" ]; then
        PYTHON_VERSION=$(venv/bin/python --version 2>&1)
        echo "  ✅ Python: $PYTHON_VERSION"
    fi
else
    echo "  ❌ venv not found"
    ERRORS=$((ERRORS + 1))
fi

# Check 6: Git status
echo ""
echo "✓ CHECK 6: Git Status"
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo "  ✅ Git repository initialized"
    BRANCH=$(git branch --show-current)
    echo "  📍 Current branch: $BRANCH"
    
    # Check for uncommitted changes
    if git diff-index --quiet HEAD --; then
        echo "  ✅ No uncommitted changes"
    else
        echo "  ⚠️  Uncommitted changes detected"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo "  ❌ Not a git repository"
    ERRORS=$((ERRORS + 1))
fi

# Check 7: Module structure
echo ""
echo "✓ CHECK 7: Module Structure"
if [ -d "modules" ]; then
    echo "  ✅ modules/ directory exists"
    MODULE_COUNT=$(find modules -maxdepth 1 -type d | wc -l)
    echo "  📦 Found $((MODULE_COUNT - 1)) modules"
else
    echo "  ⚠️  modules/ directory not found (will create)"
    WARNINGS=$((WARNINGS + 1))
fi

# Summary
echo ""
echo "=========================================="
echo "PREFLIGHT SUMMARY"
echo "=========================================="
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "✅ ALL CHECKS PASSED"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo "⚠️  PASSED WITH $WARNINGS WARNING(S)"
    exit 0
else
    echo "❌ FAILED WITH $ERRORS ERROR(S) AND $WARNINGS WARNING(S)"
    exit 1
fi
