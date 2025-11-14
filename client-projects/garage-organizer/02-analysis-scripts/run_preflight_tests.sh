#!/bin/bash
#
# COMPREHENSIVE PREFLIGHT TESTING
# Verify all data, scripts, and organization before execution
#

set -e  # Exit on any error

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DATA_VOLUME="/Volumes/DATA/consulting/garage-organizer-data-collection/raw-data"

echo "================================================================================"
echo "PREFLIGHT TESTING: Garage Organizer Slide Recreation"
echo "================================================================================"
echo "Start Time: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# ==============================================================================
# PHASE 1: DATA ACCESS VERIFICATION
# ==============================================================================
echo "PHASE 1: DATA ACCESS VERIFICATION"
echo "--------------------------------------------------------------------------------"

# Test 1.1: Verify /Volumes/DATA is mounted
if [ -d "/Volumes/DATA" ]; then
    echo "✅ Test 1.1: /Volumes/DATA is mounted"
else
    echo "❌ Test 1.1: /Volumes/DATA NOT FOUND - external drive not mounted"
    exit 1
fi

# Test 1.2: Verify data collection folder exists
if [ -d "$DATA_VOLUME" ]; then
    echo "✅ Test 1.2: Data collection folder exists: $DATA_VOLUME"
else
    echo "❌ Test 1.2: Data collection folder NOT FOUND"
    exit 1
fi

# Test 1.3: Verify YouTube data
if [ -f "$DATA_VOLUME/youtube_videos_raw.json" ]; then
    YT_SIZE=$(du -h "$DATA_VOLUME/youtube_videos_raw.json" | cut -f1)
    echo "✅ Test 1.3: YouTube data exists ($YT_SIZE)"
else
    echo "❌ Test 1.3: YouTube data NOT FOUND"
    exit 1
fi

# Test 1.4: Verify TikTok data
if [ -f "$DATA_VOLUME/tiktok_videos_raw.json" ]; then
    TT_SIZE=$(du -h "$DATA_VOLUME/tiktok_videos_raw.json" | cut -f1)
    echo "✅ Test 1.4: TikTok data exists ($TT_SIZE)"
else
    echo "❌ Test 1.4: TikTok data NOT FOUND"
    exit 1
fi

# Test 1.5: Verify Instagram data
if [ -f "$DATA_VOLUME/instagram_videos_raw.json" ]; then
    IG_SIZE=$(du -h "$DATA_VOLUME/instagram_videos_raw.json" | cut -f1)
    echo "✅ Test 1.5: Instagram data exists ($IG_SIZE)"
else
    echo "❌ Test 1.5: Instagram data NOT FOUND"
    exit 1
fi

# Test 1.6: Verify legacy social media data
if [ -f "$PROJECT_DIR/01-raw-data/social_media_posts_final.json" ]; then
    LEGACY_SIZE=$(du -h "$PROJECT_DIR/01-raw-data/social_media_posts_final.json" | cut -f1)
    echo "✅ Test 1.6: Legacy social media data exists ($LEGACY_SIZE)"
else
    echo "❌ Test 1.6: Legacy social media data NOT FOUND"
    exit 1
fi

echo ""

# ==============================================================================
# PHASE 2: DATA INTEGRITY CHECKS
# ==============================================================================
echo "PHASE 2: DATA INTEGRITY CHECKS"
echo "--------------------------------------------------------------------------------"

# Test 2.1: Verify YouTube JSON is valid
if python3 -c "import json; json.load(open('$DATA_VOLUME/youtube_videos_raw.json'))" 2>/dev/null; then
    echo "✅ Test 2.1: YouTube JSON is valid"
else
    echo "❌ Test 2.1: YouTube JSON is corrupted"
    exit 1
fi

# Test 2.2: Verify TikTok JSON is valid
if python3 -c "import json; json.load(open('$DATA_VOLUME/tiktok_videos_raw.json'))" 2>/dev/null; then
    echo "✅ Test 2.2: TikTok JSON is valid"
else
    echo "❌ Test 2.2: TikTok JSON is corrupted"
    exit 1
fi

# Test 2.3: Verify Instagram JSON is valid
if python3 -c "import json; json.load(open('$DATA_VOLUME/instagram_videos_raw.json'))" 2>/dev/null; then
    echo "✅ Test 2.3: Instagram JSON is valid"
else
    echo "❌ Test 2.3: Instagram JSON is corrupted"
    exit 1
fi

# Test 2.4: Verify legacy data JSON is valid
if python3 -c "import json; json.load(open('$PROJECT_DIR/01-raw-data/social_media_posts_final.json'))" 2>/dev/null; then
    echo "✅ Test 2.4: Legacy JSON is valid"
else
    echo "❌ Test 2.4: Legacy JSON is corrupted"
    exit 1
fi

# Test 2.5: Verify record counts
echo "✅ Test 2.5: Verifying record counts..."
python3 << 'EOF'
import json

# YouTube
with open('/Volumes/DATA/consulting/garage-organizer-data-collection/raw-data/youtube_videos_raw.json') as f:
    yt_data = json.load(f)
    yt_count = len(yt_data.get('videos', []))
    print(f"   YouTube: {yt_count} videos")
    assert yt_count >= 250, f"YouTube count too low: {yt_count}"

# TikTok
with open('/Volumes/DATA/consulting/garage-organizer-data-collection/raw-data/tiktok_videos_raw.json') as f:
    tt_data = json.load(f)
    tt_count = len(tt_data.get('videos', []))
    print(f"   TikTok: {tt_count} videos")
    assert tt_count >= 750, f"TikTok count too low: {tt_count}"

# Instagram
with open('/Volumes/DATA/consulting/garage-organizer-data-collection/raw-data/instagram_videos_raw.json') as f:
    ig_data = json.load(f)
    ig_count = len(ig_data.get('videos', []))
    print(f"   Instagram: {ig_count} reels")
    assert ig_count >= 100, f"Instagram count too low: {ig_count}"

# Legacy
with open('/Users/anderson115/00-interlink/12-work/3m-lighting-project/client-projects/garage-organizer/01-raw-data/social_media_posts_final.json') as f:
    legacy_data = json.load(f)
    legacy_count = len(legacy_data)
    print(f"   Legacy: {legacy_count} posts")
    assert legacy_count >= 1800, f"Legacy count too low: {legacy_count}"

print("   ✅ All record counts verified")
EOF

echo ""

# ==============================================================================
# PHASE 3: SCRIPT EXECUTION TESTS
# ==============================================================================
echo "PHASE 3: SCRIPT EXECUTION TESTS"
echo "--------------------------------------------------------------------------------"

# Test 3.1: Verify Python 3 available
if command -v python3 &> /dev/null; then
    PY_VERSION=$(python3 --version)
    echo "✅ Test 3.1: Python 3 available ($PY_VERSION)"
else
    echo "❌ Test 3.1: Python 3 NOT FOUND"
    exit 1
fi

# Test 3.2: Verify required Python modules
echo "✅ Test 3.2: Checking Python modules..."
python3 << 'EOF'
try:
    import json
    import re
    from collections import Counter, defaultdict
    from datetime import datetime
    print("   ✅ All required modules available")
except ImportError as e:
    print(f"   ❌ Missing module: {e}")
    exit(1)
EOF

# Test 3.3: Verify analysis scripts exist
REQUIRED_SCRIPTS=(
    "comprehensive_multi_platform_analysis.py"
    "audit_all_data_quality.py"
    "validate_data_sufficiency_for_slides.py"
)

for script in "${REQUIRED_SCRIPTS[@]}"; do
    if [ -f "$SCRIPT_DIR/$script" ]; then
        echo "✅ Test 3.3.$script: Script exists"
    else
        echo "❌ Test 3.3.$script: Script NOT FOUND"
        exit 1
    fi
done

echo ""

# ==============================================================================
# PHASE 4: FOLDER ORGANIZATION CHECK
# ==============================================================================
echo "PHASE 4: FOLDER ORGANIZATION CHECK"
echo "--------------------------------------------------------------------------------"

# Test 4.1: Verify project structure
REQUIRED_DIRS=(
    "01-raw-data"
    "02-analysis-scripts"
    "03-analysis-output"
    "04-expert-validation"
    "05-design-briefs"
    "06-final-deliverables"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$PROJECT_DIR/$dir" ]; then
        echo "✅ Test 4.1.$dir: Folder exists"
    else
        echo "❌ Test 4.1.$dir: Folder NOT FOUND"
        exit 1
    fi
done

# Test 4.2: Check for large files in wrong location
echo "✅ Test 4.2: Checking for large files in project directory..."
LARGE_FILES=$(find "$PROJECT_DIR" -type f -size +10M -not -path "*/Volumes/DATA/*" 2>/dev/null | wc -l)
if [ "$LARGE_FILES" -eq 0 ]; then
    echo "   ✅ No large files found in project directory"
else
    echo "   ⚠️  Warning: $LARGE_FILES large files found in project directory"
    find "$PROJECT_DIR" -type f -size +10M -not -path "*/Volumes/DATA/*" 2>/dev/null
fi

# Test 4.3: Verify analysis output exists
if [ -f "$PROJECT_DIR/03-analysis-output/iteration_1_analysis.json" ]; then
    echo "✅ Test 4.3: Iteration 1 analysis exists"
else
    echo "❌ Test 4.3: Iteration 1 analysis NOT FOUND"
    exit 1
fi

echo ""

# ==============================================================================
# PHASE 5: AUDIT TRAIL VERIFICATION
# ==============================================================================
echo "PHASE 5: AUDIT TRAIL VERIFICATION"
echo "--------------------------------------------------------------------------------"

# Test 5.1: Verify audit trail exists
if [ -f "$PROJECT_DIR/03-analysis-output/complete_audit_trail.json" ]; then
    AUDIT_COUNT=$(python3 -c "import json; print(len(json.load(open('$PROJECT_DIR/03-analysis-output/complete_audit_trail.json'))))")
    echo "✅ Test 5.1: Audit trail exists ($AUDIT_COUNT entries)"
else
    echo "❌ Test 5.1: Audit trail NOT FOUND"
    exit 1
fi

# Test 5.2: Verify audit entries have required fields
echo "✅ Test 5.2: Verifying audit entry structure..."
python3 << 'EOF'
import json

with open('/Users/anderson115/00-interlink/12-work/3m-lighting-project/client-projects/garage-organizer/03-analysis-output/complete_audit_trail.json') as f:
    audit = json.load(f)

required_fields = ['insight', 'source_type', 'source_count', 'confidence']
sample_entry = audit[0] if audit else {}

missing = [f for f in required_fields if f not in sample_entry]
if missing:
    print(f"   ❌ Missing fields: {missing}")
    exit(1)
else:
    print(f"   ✅ All required fields present")
EOF

echo ""

# ==============================================================================
# SUMMARY
# ==============================================================================
echo "================================================================================"
echo "PREFLIGHT TEST SUMMARY"
echo "================================================================================"
echo ""
echo "✅ PHASE 1: Data Access - ALL TESTS PASSED"
echo "✅ PHASE 2: Data Integrity - ALL TESTS PASSED"
echo "✅ PHASE 3: Script Execution - ALL TESTS PASSED"
echo "✅ PHASE 4: Folder Organization - ALL TESTS PASSED"
echo "✅ PHASE 5: Audit Trail - ALL TESTS PASSED"
echo ""
echo "🎉 ALL PREFLIGHT TESTS PASSED - READY FOR EXECUTION"
echo ""
echo "End Time: $(date '+%Y-%m-%d %H:%M:%S')"
echo "================================================================================"
