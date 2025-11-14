#!/usr/bin/env python3
"""
Data Consolidation and Cleanup Script
Merges all data sources, adds wave flags, deduplicates, and cleans up project folder.
"""

import json
import os
from datetime import datetime
from collections import defaultdict
from pathlib import Path

# Paths
LOCAL_RAW = Path("01-raw-data")
EXTERNAL_RAW = Path("/Volumes/DATA/consulting/garage-organizer-data-collection/raw-data")
OUTPUT_DIR = Path("01-raw-data")

print("=" * 80)
print("DATA CONSOLIDATION AND CLEANUP")
print("=" * 80)
print()

# Track all data sources
data_sources = {
    'reddit': [],
    'youtube_videos': [],
    'youtube_comments': [],
    'tiktok': [],
    'instagram': [],
}

wave_info = {}

# ============================================================================
# PHASE 1: READ ALL DATA SOURCES
# ============================================================================

print("PHASE 1: Reading all data sources...")
print()

# 1.1 Local Reddit + YouTube Comments (social_media_posts_final.json)
social_file = LOCAL_RAW / "social_media_posts_final.json"
if social_file.exists():
    with open(social_file) as f:
        social_data = json.load(f)

    print(f"✅ {social_file.name}: {len(social_data):,} records")

    # All records in this file are Reddit or YouTube comments
    for record in social_data:
        if 'post_url' in record and 'reddit.com' in record.get('post_url', ''):
            record['platform'] = 'reddit'
            record['collection_wave'] = 'wave_1_initial'
            record['collection_date'] = '2024-11-12'
            data_sources['reddit'].append(record)
        elif 'comment_text' in record or 'youtube.com' in str(record.get('post_url', '')):
            record['platform'] = 'youtube_comment'
            record['collection_wave'] = 'wave_1_initial'
            record['collection_date'] = '2024-11-12'
            data_sources['youtube_comments'].append(record)
        else:
            # Fallback - check content
            record['platform'] = 'reddit'  # Most are Reddit
            record['collection_wave'] = 'wave_1_initial'
            record['collection_date'] = '2024-11-12'
            data_sources['reddit'].append(record)

    print(f"   Reddit: {len(data_sources['reddit']):,}")
    print(f"   YouTube Comments: {len(data_sources['youtube_comments']):,}")
print()

# 1.2 Local YouTube Videos (youtube_videos.json)
youtube_file = LOCAL_RAW / "youtube_videos.json"
if youtube_file.exists():
    with open(youtube_file) as f:
        youtube_data = json.load(f)

    # Handle both list and dict structures
    if isinstance(youtube_data, dict) and 'videos' in youtube_data:
        youtube_records = youtube_data['videos']
    elif isinstance(youtube_data, list):
        youtube_records = youtube_data
    else:
        youtube_records = []

    print(f"✅ {youtube_file.name}: {len(youtube_records):,} records")

    for record in youtube_records:
        if isinstance(record, dict):
            record['platform'] = 'youtube'
            record['collection_wave'] = 'wave_1_initial'
            record['collection_date'] = '2024-11-12'
            data_sources['youtube_videos'].append(record)
print()

# 1.3 Local YouTube Videos - Full Collection (full_garage_organizer_videos.json)
full_youtube_file = LOCAL_RAW / "full_garage_organizer_videos.json"
if full_youtube_file.exists():
    with open(full_youtube_file) as f:
        full_youtube_data = json.load(f)

    print(f"✅ {full_youtube_file.name}: {len(full_youtube_data):,} records")

    for record in full_youtube_data:
        record['platform'] = 'youtube'
        record['collection_wave'] = 'wave_1_expansion'
        record['collection_date'] = '2024-11-12'
        data_sources['youtube_videos'].append(record)
print()

# 1.4 Local TikTok (tiktok_videos.json)
tiktok_file = LOCAL_RAW / "tiktok_videos.json"
if tiktok_file.exists():
    with open(tiktok_file) as f:
        tiktok_data = json.load(f)

    # Handle both list and dict structures
    if isinstance(tiktok_data, dict) and 'videos' in tiktok_data:
        tiktok_records = tiktok_data['videos']
    elif isinstance(tiktok_data, dict):
        # Dict of video_id -> record
        tiktok_records = [v for v in tiktok_data.values() if isinstance(v, dict)]
    elif isinstance(tiktok_data, list):
        tiktok_records = tiktok_data
    else:
        tiktok_records = []

    print(f"✅ {tiktok_file.name}: {len(tiktok_records)} records")

    for record in tiktok_records:
        if isinstance(record, dict):
            record['platform'] = 'tiktok'
            record['collection_wave'] = 'wave_1_initial'
            record['collection_date'] = '2024-11-12'
            data_sources['tiktok'].append(record)
print()

# 1.5 External YouTube (youtube_videos_raw.json)
if EXTERNAL_RAW.exists():
    ext_youtube_file = EXTERNAL_RAW / "youtube_videos_raw.json"
    if ext_youtube_file.exists():
        with open(ext_youtube_file) as f:
            ext_youtube_data = json.load(f)

        # Handle various data structures
        if isinstance(ext_youtube_data, list):
            ext_youtube_records = [r for r in ext_youtube_data if isinstance(r, dict)]
        elif isinstance(ext_youtube_data, dict):
            ext_youtube_records = [v for v in ext_youtube_data.values() if isinstance(v, dict)]
        else:
            ext_youtube_records = []

        print(f"✅ {ext_youtube_file.name}: {len(ext_youtube_records):,} records")

        for record in ext_youtube_records:
            record['platform'] = 'youtube'
            record['collection_wave'] = 'wave_2_extended'
            record['collection_date'] = '2024-11-12'
            data_sources['youtube_videos'].append(record)
    print()

    # 1.6 External TikTok (tiktok_videos_raw.json)
    ext_tiktok_file = EXTERNAL_RAW / "tiktok_videos_raw.json"
    if ext_tiktok_file.exists():
        with open(ext_tiktok_file) as f:
            ext_tiktok_data = json.load(f)

        # Handle various data structures
        if isinstance(ext_tiktok_data, list):
            ext_tiktok_records = [r for r in ext_tiktok_data if isinstance(r, dict)]
        elif isinstance(ext_tiktok_data, dict):
            ext_tiktok_records = [v for v in ext_tiktok_data.values() if isinstance(v, dict)]
        else:
            ext_tiktok_records = []

        print(f"✅ {ext_tiktok_file.name}: {len(ext_tiktok_records):,} records")

        for record in ext_tiktok_records:
            record['platform'] = 'tiktok'
            record['collection_wave'] = 'wave_2_extended'
            record['collection_date'] = '2024-11-12'
            data_sources['tiktok'].append(record)
    print()

    # 1.7 External Instagram (instagram_videos_raw.json)
    ext_insta_file = EXTERNAL_RAW / "instagram_videos_raw.json"
    if ext_insta_file.exists():
        with open(ext_insta_file) as f:
            ext_insta_data = json.load(f)

        # Handle various data structures
        if isinstance(ext_insta_data, list):
            ext_insta_records = [r for r in ext_insta_data if isinstance(r, dict)]
        elif isinstance(ext_insta_data, dict):
            ext_insta_records = [v for v in ext_insta_data.values() if isinstance(v, dict)]
        else:
            ext_insta_records = []

        print(f"✅ {ext_insta_file.name}: {len(ext_insta_records):,} records")

        for record in ext_insta_records:
            record['platform'] = 'instagram'
            record['collection_wave'] = 'wave_1_initial'
            record['collection_date'] = '2024-11-12'
            data_sources['instagram'].append(record)
    print()

print()
print("=" * 80)
print("PHASE 2: Deduplication by URL")
print("=" * 80)
print()

# Deduplicate each platform by URL
deduplicated_data = {}

for platform, records in data_sources.items():
    seen_urls = set()
    unique_records = []
    duplicates = 0

    for record in records:
        # Determine URL field
        url = record.get('post_url') or record.get('video_url') or record.get('url') or record.get('link')

        if not url:
            # No URL - keep it but log warning
            unique_records.append(record)
            continue

        if url in seen_urls:
            duplicates += 1
            continue

        seen_urls.add(url)
        unique_records.append(record)

    deduplicated_data[platform] = unique_records

    print(f"{platform:20s}: {len(records):,} → {len(unique_records):,} ({duplicates:,} duplicates removed)")

print()
print("=" * 80)
print("PHASE 3: Data Validation")
print("=" * 80)
print()

validation_report = {}

for platform, records in deduplicated_data.items():
    validation = {
        'total_records': len(records),
        'has_url': 0,
        'has_text': 0,
        'has_metadata': 0,
        'missing_url': [],
    }

    for i, record in enumerate(records):
        url = record.get('post_url') or record.get('video_url') or record.get('url') or record.get('link')
        text = record.get('post_text') or record.get('title') or record.get('description') or record.get('text')

        if url:
            validation['has_url'] += 1
        else:
            validation['missing_url'].append(i)

        if text:
            validation['has_text'] += 1

        if len(record) > 5:  # Has substantial metadata
            validation['has_metadata'] += 1

    validation_report[platform] = validation

    print(f"{platform}:")
    print(f"  Total: {validation['total_records']:,}")
    print(f"  Has URL: {validation['has_url']:,} ({validation['has_url']/max(validation['total_records'],1)*100:.1f}%)")
    print(f"  Has text: {validation['has_text']:,} ({validation['has_text']/max(validation['total_records'],1)*100:.1f}%)")
    print(f"  Has metadata: {validation['has_metadata']:,} ({validation['has_metadata']/max(validation['total_records'],1)*100:.1f}%)")
    if validation['missing_url']:
        print(f"  ⚠️  {len(validation['missing_url'])} records missing URLs")
    print()

print()
print("=" * 80)
print("PHASE 4: Save Consolidated Files")
print("=" * 80)
print()

# Save each platform to separate file
consolidated_files = {}

for platform, records in deduplicated_data.items():
    if not records:
        print(f"⏭️  Skipping {platform} (no records)")
        continue

    filename = f"{platform}_consolidated.json"
    filepath = OUTPUT_DIR / filename

    with open(filepath, 'w') as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    file_size_mb = filepath.stat().st_size / (1024 * 1024)
    consolidated_files[platform] = {
        'file': filename,
        'records': len(records),
        'size_mb': round(file_size_mb, 2)
    }

    print(f"✅ {filename}: {len(records):,} records ({file_size_mb:.2f} MB)")

print()
print("=" * 80)
print("PHASE 5: Generate Consolidation Report")
print("=" * 80)
print()

consolidation_report = {
    'consolidation_date': datetime.now().isoformat(),
    'total_records_before': sum(len(v) for v in data_sources.values()),
    'total_records_after': sum(len(v) for v in deduplicated_data.values()),
    'duplicates_removed': sum(len(data_sources[k]) - len(v) for k, v in deduplicated_data.items()),
    'platforms': {},
    'consolidated_files': consolidated_files,
    'validation_report': validation_report,
}

for platform, records in deduplicated_data.items():
    consolidation_report['platforms'][platform] = {
        'records': len(records),
        'waves': list(set(r.get('collection_wave', 'unknown') for r in records)),
        'date_range': {
            'earliest': min((r.get('collection_date', '2024-11-12') for r in records), default='unknown'),
            'latest': max((r.get('collection_date', '2024-11-12') for r in records), default='unknown'),
        }
    }

report_file = OUTPUT_DIR / "DATA_CONSOLIDATION_REPORT.json"
with open(report_file, 'w') as f:
    json.dump(consolidation_report, f, indent=2)

print(f"✅ Consolidation report saved: {report_file.name}")
print()

print("=" * 80)
print("SUMMARY")
print("=" * 80)
print()
print(f"Total records before: {consolidation_report['total_records_before']:,}")
print(f"Total records after:  {consolidation_report['total_records_after']:,}")
print(f"Duplicates removed:   {consolidation_report['duplicates_removed']:,}")
print()
print("By Platform:")
for platform, info in consolidation_report['platforms'].items():
    print(f"  {platform:20s}: {info['records']:,} records")
print()
print("✅ Consolidation complete!")
print()
print("Next steps:")
print("  1. Review consolidated files in 01-raw-data/")
print("  2. Check DATA_CONSOLIDATION_REPORT.json for details")
print("  3. Update analysis scripts to use consolidated files")
print()
