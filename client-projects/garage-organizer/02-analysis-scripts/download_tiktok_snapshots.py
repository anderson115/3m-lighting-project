#!/usr/bin/env python3
"""
Download TikTok data from BrightData snapshots
"""

import json
import requests
from datetime import datetime

API_TOKEN = "8967cbcf-6c3a-4fd4-8254-ac4c6d466503"
BASE_URL = "https://api.brightdata.com/datasets/v3"

SNAPSHOT_IDS = [
    "sd_mhwtgcbc2ojj4nu9my",
    "sd_mhwthmx31ol4wkw8g6",
    "sd_mhwtixi52pevvet5ca",
    "sd_mhwtk83z1hejvbffq5",
    "sd_mhwtlj5f21avjfcycf",
    "sd_mhwtmtqapsqgah62",
    "sd_mhwto4dd13d4ridxjj",
    "sd_mhwtpf0a10k74zxx27"
]

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
        print(f"   Downloaded {len(data)} videos")
        return data
    except:
        print(f"❌ {snapshot_id}: Parse error")
        return []

def main():
    print("Downloading TikTok snapshots from BrightData...")
    print("="*70)

    all_videos = []

    for snapshot_id in SNAPSHOT_IDS:
        videos = download_snapshot(snapshot_id)
        all_videos.extend(videos)

    print(f"\n✅ Total videos downloaded: {len(all_videos)}")

    # Save raw data
    output = {
        "manifest": {
            "file_name": "tiktok_videos_raw.json",
            "extraction_date": datetime.now().isoformat() + "Z",
            "extraction_source": "BrightData Web Scraper API (TikTok Posts)",
            "total_records": len(all_videos),
            "snapshot_ids": SNAPSHOT_IDS,
            "checkpoint_metadata": {
                "checkpoint_name": "CHECKPOINT_04_TIKTOK_EXTRACTION",
                "checkpoint_date": datetime.now().isoformat() + "Z",
                "checkpoint_status": "COMPLETE",
                "validation_passed": False,
                "next_checkpoint": "CHECKPOINT_04_TIKTOK_VALIDATION",
                "data_source": "REAL - BrightData Web Scraper API"
            }
        },
        "videos": all_videos
    }

    output_file = "/Volumes/DATA/consulting/garage-organizer-data-collection/raw-data/tiktok_videos_raw.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"✅ Saved to: {output_file}")

if __name__ == "__main__":
    main()
