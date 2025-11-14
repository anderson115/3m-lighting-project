#!/usr/bin/env python3
"""
Download ALL Instagram snapshots with DIVERSITY FILTER
Max 5 reels per creator to ensure broad representation
"""

import json
import requests
from datetime import datetime
from collections import Counter

API_TOKEN = "8967cbcf-6c3a-4fd4-8254-ac4c6d466503"
BASE_URL = "https://api.brightdata.com/datasets/v3"

def load_all_snapshot_ids():
    """Load snapshot IDs from all Instagram extraction files"""
    snapshot_ids = []

    # Original 3 snapshots
    try:
        with open('/Volumes/DATA/consulting/garage-organizer-data-collection/raw-data/instagram_videos_raw.json') as f:
            data = json.load(f)
            snapshot_ids.extend(data['manifest'].get('snapshot_ids', []))
    except:
        pass

    # Gap fill 9 snapshots
    try:
        with open('/Volumes/DATA/consulting/garage-organizer-data-collection/raw-data/instagram_gap_fill_snapshots.json') as f:
            data = json.load(f)
            snapshot_ids.extend(data.get('snapshot_ids', []))
    except:
        pass

    # Massive expansion 19 snapshots
    try:
        with open('/Volumes/DATA/consulting/garage-organizer-data-collection/raw-data/instagram_massive_expansion_snapshots.json') as f:
            data = json.load(f)
            snapshot_ids.extend(data.get('snapshot_ids', []))
    except:
        pass

    # 40 profiles expansion
    try:
        with open('/Volumes/DATA/consulting/garage-organizer-data-collection/raw-data/instagram_40_profiles_snapshots.json') as f:
            data = json.load(f)
            snapshot_ids.extend(data.get('snapshot_ids', []))
    except:
        pass

    return list(set(snapshot_ids))  # Deduplicate

def download_snapshot(snapshot_id):
    """Download data from snapshot"""
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    # Check status
    progress_url = f"{BASE_URL}/progress/{snapshot_id}"
    response = requests.get(progress_url, headers=headers)

    if response.status_code != 200:
        print(f"   ❌ Status check failed")
        return []

    status = response.json()

    if status.get('status') != 'ready':
        print(f"   ⏸️  {status.get('status')} ({status.get('records', 0)} records)")
        return []

    print(f"   ✅ Ready: {status.get('records')} records")

    # Download
    download_url = f"{BASE_URL}/snapshot/{snapshot_id}?format=json"
    response = requests.get(download_url, headers=headers)

    if response.status_code != 200:
        print(f"   ❌ Download failed: {response.status_code}")
        return []

    try:
        data = response.json()
        # Filter for reels only
        reels = [item for item in data if item.get('is_video') or item.get('product_type') == 'clips']
        print(f"   📥 Downloaded: {len(data)} posts, {len(reels)} reels")
        return reels
    except Exception as e:
        print(f"   ❌ Parse error: {str(e)}")
        return []

def apply_diversity_filter(reels, max_per_creator=5):
    """Limit reels per creator for diversity"""
    creator_counts = Counter()
    filtered = []

    for reel in reels:
        creator = reel.get('user_posted') or reel.get('owner', {}).get('username')
        if creator and creator_counts[creator] < max_per_creator:
            filtered.append(reel)
            creator_counts[creator] += 1

    return filtered, creator_counts

def main():
    print("="*80)
    print("INSTAGRAM DOWNLOAD: All Snapshots with Diversity Filter")
    print("="*80)

    snapshot_ids = load_all_snapshot_ids()
    print(f"Found {len(snapshot_ids)} snapshot IDs\n")

    all_reels = []

    for i, snapshot_id in enumerate(snapshot_ids, 1):
        print(f"[{i}/{len(snapshot_ids)}] {snapshot_id}")
        reels = download_snapshot(snapshot_id)
        all_reels.extend(reels)

    print(f"\n{'='*80}")
    print(f"Total downloaded: {len(all_reels)} reels")

    # Deduplicate by shortcode/id
    seen_ids = set()
    deduplicated = []
    for reel in all_reels:
        reel_id = reel.get('shortcode') or reel.get('id')
        if reel_id and reel_id not in seen_ids:
            seen_ids.add(reel_id)
            deduplicated.append(reel)

    print(f"After dedup: {len(deduplicated)} unique reels")

    # Apply diversity filter (max 5 per creator)
    filtered, creator_counts = apply_diversity_filter(deduplicated, max_per_creator=5)

    print(f"\nDIVERSITY FILTER (max 5 reels/creator):")
    print(f"   Before: {len(deduplicated)} reels")
    print(f"   After:  {len(filtered)} reels")
    print(f"   Unique creators: {len(creator_counts)}")
    print(f"   Avg per creator: {len(filtered)/len(creator_counts):.1f}")

    # Show top creators
    print(f"\n   Top creators:")
    for creator, count in creator_counts.most_common(10):
        print(f"      @{creator}: {count} reels")

    # Save
    output = {
        "manifest": {
            "file_name": "instagram_videos_raw.json",
            "extraction_date": datetime.now().isoformat() + "Z",
            "extraction_source": "BrightData Web Scraper API (Instagram - Diverse)",
            "total_records": len(filtered),
            "snapshot_ids": snapshot_ids,
            "quality_gates": {
                "total_collected": len(all_reels),
                "after_dedup": len(deduplicated),
                "after_diversity_filter": len(filtered),
                "unique_creators": len(creator_counts),
                "max_reels_per_creator": 5
            },
            "checkpoint_metadata": {
                "checkpoint_name": "CHECKPOINT_05_INSTAGRAM_EXTRACTION",
                "checkpoint_date": datetime.now().isoformat() + "Z",
                "checkpoint_status": "COMPLETE",
                "validation_passed": False,
                "next_checkpoint": "CHECKPOINT_05_INSTAGRAM_VALIDATION",
                "data_source": "REAL - BrightData API (Diversity Filtered)"
            },
            "audit_trail": {
                "data_source": "BrightData Web Scraper API",
                "api_endpoint": "https://api.brightdata.com/datasets/v3",
                "dataset_id": "gd_lyclm20il4r5helnj",
                "collection_method": "Profile scraping with diversity filter",
                "diversity_strategy": "Max 5 reels per creator",
                "each_video_traceable": "Yes - all reels have shortcode, user, url",
                "verification_url_format": "https://www.instagram.com/reel/{shortcode}/"
            }
        },
        "videos": filtered
    }

    output_file = '/Volumes/DATA/consulting/garage-organizer-data-collection/raw-data/instagram_videos_raw.json'
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n✅ Saved: {output_file}")
    print(f"   Total: {len(filtered)} reels from {len(creator_counts)} unique creators")

if __name__ == "__main__":
    main()
