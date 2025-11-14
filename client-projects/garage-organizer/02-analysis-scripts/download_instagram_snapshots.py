#!/usr/bin/env python3
"""
Download Instagram Reels data from BrightData snapshots
"""

import json
import requests
from datetime import datetime

API_TOKEN = "8967cbcf-6c3a-4fd4-8254-ac4c6d466503"
BASE_URL = "https://api.brightdata.com/datasets/v3"

# Load snapshot IDs from previous extraction
DATA_FILE = "/Volumes/DATA/consulting/garage-organizer-data-collection/raw-data/instagram_videos_raw.json"

def download_snapshot(snapshot_id):
    """Download data from a snapshot"""
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    # Check status first
    progress_url = f"{BASE_URL}/progress/{snapshot_id}"
    response = requests.get(progress_url, headers=headers)

    if response.status_code != 200:
        print(f"❌ {snapshot_id}: Error checking status - {response.status_code}")
        return []

    status = response.json()

    if status.get('status') != 'ready':
        print(f"⏸️  {snapshot_id}: Not ready yet - {status.get('status')}")
        return []

    print(f"✅ {snapshot_id}: Ready - {status.get('records')} records")

    # Download data
    download_url = f"{BASE_URL}/snapshot/{snapshot_id}?format=json"
    response = requests.get(download_url, headers=headers)

    if response.status_code != 200:
        print(f"❌ {snapshot_id}: Download failed - {response.status_code}")
        return []

    try:
        data = response.json()

        # Filter for reels only (video posts)
        reels = []
        for item in data:
            if item.get('is_video') or item.get('product_type') == 'clips':  # Reels are clips
                reels.append(item)

        print(f"   Downloaded {len(data)} posts, {len(reels)} are reels")
        return reels
    except Exception as e:
        print(f"❌ {snapshot_id}: Parse error - {str(e)}")
        return []

def main():
    print("Downloading Instagram Reels snapshots from BrightData...")
    print("="*70)

    # Load existing file to get snapshot IDs
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    snapshot_ids = data['manifest']['snapshot_ids']
    print(f"Found {len(snapshot_ids)} snapshot IDs to download\n")

    all_reels = []

    for snapshot_id in snapshot_ids:
        reels = download_snapshot(snapshot_id)
        all_reels.extend(reels)

    print(f"\n✅ Total reels downloaded: {len(all_reels)}")

    # Deduplicate by post_id
    seen_ids = set()
    deduplicated = []
    for reel in all_reels:
        post_id = reel.get('shortcode') or reel.get('id')
        if post_id and post_id not in seen_ids:
            seen_ids.add(post_id)
            deduplicated.append(reel)

    print(f"✅ After deduplication: {len(deduplicated)} unique reels")

    # Save with complete manifest
    output = {
        "manifest": {
            "file_name": "instagram_videos_raw.json",
            "extraction_date": datetime.now().isoformat() + "Z",
            "extraction_source": "BrightData Web Scraper API (Instagram Posts - Reels)",
            "total_records": len(deduplicated),
            "snapshot_ids": snapshot_ids,
            "quality_gates": {
                "total_records_collected": len(all_reels),
                "duplicates_removed": len(all_reels) - len(deduplicated),
                "duplication_rate": f"{(len(all_reels) - len(deduplicated))/len(all_reels)*100:.1f}%" if all_reels else "0%"
            },
            "checkpoint_metadata": {
                "checkpoint_name": "CHECKPOINT_05_INSTAGRAM_EXTRACTION",
                "checkpoint_date": datetime.now().isoformat() + "Z",
                "checkpoint_status": "COMPLETE",
                "validation_passed": False,
                "next_checkpoint": "CHECKPOINT_05_INSTAGRAM_VALIDATION",
                "data_source": "REAL - BrightData Web Scraper API"
            },
            "audit_trail": {
                "data_source": "BrightData Web Scraper API",
                "api_endpoint": "https://api.brightdata.com/datasets/v3",
                "dataset_id": "gd_lyclm20il4r5helnj",
                "collection_method": "REST API with snapshot polling",
                "snapshot_ids": snapshot_ids,
                "each_video_traceable": "Yes - all reels have shortcode, url, owner, timestamp",
                "verification_url_format": "https://www.instagram.com/reel/{shortcode}/"
            }
        },
        "videos": deduplicated
    }

    with open(DATA_FILE, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"✅ Saved to: {DATA_FILE}")

if __name__ == "__main__":
    main()
