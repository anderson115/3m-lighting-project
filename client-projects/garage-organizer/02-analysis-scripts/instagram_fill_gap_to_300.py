#!/usr/bin/env python3
"""
Fill Instagram gap to 300+ reels
Target: 250 additional reels (10 profiles x 30 reels = 300 expected)
"""

import json
import requests
from datetime import datetime
import time

API_TOKEN = "8967cbcf-6c3a-4fd4-8254-ac4c6d466503"
BASE_URL = "https://api.brightdata.com/datasets/v3"
DATASET_ID = "gd_lyclm20il4r5helnj"

# 10 high-quality garage/organization profiles
PROFILES = [
    "https://www.instagram.com/garagegymreviews/",
    "https://www.instagram.com/cleanmama/",
    "https://www.instagram.com/neatbynicole/",
    "https://www.instagram.com/clutterbug_me/",
    "https://www.instagram.com/organization_obsessed/",
    "https://www.instagram.com/athomewithashley/",
    "https://www.instagram.com/professionalorganizer/",
    "https://www.instagram.com/simplyorganized/",
    "https://www.instagram.com/organized_home/",
    "https://www.instagram.com/home.neat.home/",
]

def trigger_scrape(profile_url, num_posts=30):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "input": [{
            "url": profile_url,
            "num_of_posts": num_posts,
            "start_date": "2022-01-01",
            "end_date": "2025-11-12"
        }]
    }

    url = f"{BASE_URL}/scrape?dataset_id={DATASET_ID}&notify=false&include_errors=true&type=discover_new&discover_by=url_all_reels"

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        if response.status_code == 202:
            result = response.json()
            return result.get('snapshot_id')
        else:
            return None
    except:
        return None

print("="*80)
print("INSTAGRAM GAP FILL: 50 → 300+ reels")
print("="*80)
print(f"Targeting 10 profiles x 30 reels = 300 reels expected")
print(f"Current: 50 | Gap: 250 | Target: 300+\n")

snapshot_ids = []

for i, profile_url in enumerate(PROFILES, 1):
    profile_name = profile_url.split('/')[-2]
    print(f"[{i}/10] @{profile_name:30s}", end=" ", flush=True)

    snapshot_id = trigger_scrape(profile_url)

    if snapshot_id:
        snapshot_ids.append(snapshot_id)
        print(f"✅ {snapshot_id}")
    else:
        print(f"⚠️  Failed")

    time.sleep(2)  # Rate limiting

print(f"\n{'='*80}")
print(f"✅ Triggered: {len(snapshot_ids)}/10 profiles")
print(f"   Expected reels: ~{len(snapshot_ids) * 30}")
print(f"   Projected total: 50 + {len(snapshot_ids) * 30} = {50 + len(snapshot_ids) * 30}")

# Save snapshot IDs
output = {
    "expansion_date": datetime.now().isoformat() + "Z",
    "snapshot_ids": snapshot_ids,
    "current_count": 50,
    "gap_fill_target": 250,
    "expected_after": 50 + len(snapshot_ids) * 30
}

with open('/Volumes/DATA/consulting/garage-organizer-data-collection/raw-data/instagram_gap_fill_snapshots.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n⏸️  Wait 5-7 minutes for BrightData processing")
print(f"   Then download with combined script")
