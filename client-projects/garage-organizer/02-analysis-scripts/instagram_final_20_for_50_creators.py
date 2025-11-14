#!/usr/bin/env python3
"""
Instagram Final Round: 20 profiles for 50+ total creators
Budget: $15 max (~20 profiles × 5 reels × $0.03 = $3)
"""

import json
import requests
from datetime import datetime
import time

API_TOKEN = "8967cbcf-6c3a-4fd4-8254-ac4c6d466503"
BASE_URL = "https://api.brightdata.com/datasets/v3"
DATASET_ID = "gd_lyclm20il4r5helnj"

# 20 NEW diverse garage/organization creators (not previously tried)
PROFILES = [
    "https://www.instagram.com/organizedbyamber/",
    "https://www.instagram.com/organize_my_house/",
    "https://www.instagram.com/theorganizedhousewife/",
    "https://www.instagram.com/organizedspace/",
    "https://www.instagram.com/organization_queen/",
    "https://www.instagram.com/garage_organization_ideas/",
    "https://www.instagram.com/garage.storage.solutions/",
    "https://www.instagram.com/organized_garage_life/",
    "https://www.instagram.com/homeorganizers/",
    "https://www.instagram.com/organize.everything/",
    "https://www.instagram.com/tidy.at.home/",
    "https://www.instagram.com/organize.with.me/",
    "https://www.instagram.com/theorganizer/",
    "https://www.instagram.com/minimal_home/",
    "https://www.instagram.com/organize.home/",
    "https://www.instagram.com/garage.workshop/",
    "https://www.instagram.com/workshop.organized/",
    "https://www.instagram.com/tool.organization/",
    "https://www.instagram.com/garage.tools/",
    "https://www.instagram.com/organized.workshop/",
]

def trigger_scrape(profile_url, num_posts=5):
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
        return None
    except:
        return None

print("="*80)
print("INSTAGRAM FINAL ROUND: 20 profiles → 50+ total creators")
print("="*80)
print(f"Current: 34 creators | Target: 50+ creators")
print(f"Strategy: 20 profiles × 5 reels = 100 expected, ~16+ new creators\n")

snapshot_ids = []

for i, profile_url in enumerate(PROFILES, 1):
    profile_name = profile_url.split('/')[-2]
    print(f"[{i:2d}/20] {profile_name:35s}", end=" ", flush=True)

    snapshot_id = trigger_scrape(profile_url, num_posts=5)

    if snapshot_id:
        snapshot_ids.append(snapshot_id)
        print(f"✅ {snapshot_id}")
    else:
        print(f"⚠️  Failed")

    time.sleep(1.5)

print(f"\n{'='*80}")
print(f"✅ Triggered: {len(snapshot_ids)}/20 profiles")
print(f"   Expected new creators: ~{int(len(snapshot_ids) * 0.8)}")
print(f"   Projected total: 34 + {int(len(snapshot_ids) * 0.8)} = {34 + int(len(snapshot_ids) * 0.8)} creators")

output = {
    "expansion_date": datetime.now().isoformat() + "Z",
    "snapshot_ids": snapshot_ids,
    "current_creators": 34,
    "target_creators": 50,
    "expected_new_creators": int(len(snapshot_ids) * 0.8)
}

with open('/Volumes/DATA/consulting/garage-organizer-data-collection/raw-data/instagram_final_20_snapshots.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n⏸️  Wait 5-7 minutes, then download with updated script")
