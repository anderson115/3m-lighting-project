#!/usr/bin/env python3
"""
Instagram Massive Expansion: 50 diverse profiles for 300+ reels
Target: 50 profiles × 10 reels = 500 expected, filter to 300 diverse
"""

import json
import requests
from datetime import datetime
import time

API_TOKEN = "8967cbcf-6c3a-4fd4-8254-ac4c6d466503"
BASE_URL = "https://api.brightdata.com/datasets/v3"
DATASET_ID = "gd_lyclm20il4r5helnj"

# 50 diverse garage/DIY/organization influencers
PROFILES = [
    # Garage specific
    "https://www.instagram.com/garage_goals/",
    "https://www.instagram.com/my_organized_garage/",
    "https://www.instagram.com/thegaragejournal/",
    "https://www.instagram.com/garage_therapy/",
    "https://www.instagram.com/epic_garage/",

    # DIY/Home improvement with garage content
    "https://www.instagram.com/diywithjesse/",
    "https://www.instagram.com/diycreators/",
    "https://www.instagram.com/handyman_startup/",
    "https://www.instagram.com/woodworking_diy/",
    "https://www.instagram.com/thehandyma/",
    "https://www.instagram.com/diy_homeimprovement/",
    "https://www.instagram.com/fixthisbuildthat/",
    "https://www.instagram.com/theweekendwoodworker/",
    "https://www.instagram.com/shanty2chic/",
    "https://www.instagram.com/younghouselove/",

    # Storage/Organization
    "https://www.instagram.com/thecontainerstore/",
    "https://www.instagram.com/ikea/",
    "https://www.instagram.com/organized.life/",
    "https://www.instagram.com/organizing_with_style/",
    "https://www.instagram.com/neatmethod/",
    "https://www.instagram.com/getcalm.co/",
    "https://www.instagram.com/containerstore/",
    "https://www.instagram.com/minimal.mama/",
    "https://www.instagram.com/tidyhappy/",
    "https://www.instagram.com/neatbymeg/",

    # Home organization general
    "https://www.instagram.com/mrshinch/",
    "https://www.instagram.com/tidyingupwithmiami/",
    "https://www.instagram.com/thesortedspace/",
    "https://www.instagram.com/organization.junkie/",
    "https://www.instagram.com/organizewithmarcy/",
    "https://www.instagram.com/neat_caroline/",
    "https://www.instagram.com/organization_by_design/",
    "https://www.instagram.com/organized.by.design/",
    "https://www.instagram.com/get.organized/",
    "https://www.instagram.com/organize.my.life/",

    # Garage gym (relevant niche)
    "https://www.instagram.com/garagegymlab/",
    "https://www.instagram.com/garagegymlife/",
    "https://www.instagram.com/homegym/",
    "https://www.instagram.com/garage.gym/",
    "https://www.instagram.com/garagegymaddict/",

    # Maker/Builder community
    "https://www.instagram.com/diypete/",
    "https://www.instagram.com/makersmovement/",
    "https://www.instagram.com/woodshop_diaries/",
    "https://www.instagram.com/thehandymansdaughter/",
    "https://www.instagram.com/jaimecostiglio/",
    "https://www.instagram.com/bobvila/",
    "https://www.instagram.com/thisoldhouse/",
    "https://www.instagram.com/familyhandyman/",
    "https://www.instagram.com/loweshomeimprovement/",
    "https://www.instagram.com/homedepot/",
]

def trigger_scrape(profile_url, num_posts=10):
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
print("INSTAGRAM MASSIVE EXPANSION: 50 profiles → 300+ diverse reels")
print("="*80)
print(f"Current: 64 reels (22 creators)")
print(f"Target: 300 reels (60+ creators)")
print(f"Strategy: 50 profiles × 10 reels = 500, filter to 300 with diversity\n")

snapshot_ids = []
failed = 0

for i, profile_url in enumerate(PROFILES, 1):
    profile_name = profile_url.split('/')[-2]
    print(f"[{i:2d}/50] {profile_name:30s}", end=" ", flush=True)

    snapshot_id = trigger_scrape(profile_url)

    if snapshot_id:
        snapshot_ids.append(snapshot_id)
        print(f"✅ {snapshot_id}")
    else:
        failed += 1
        print(f"⚠️  Failed")

    time.sleep(1.5)  # Rate limiting

print(f"\n{'='*80}")
print(f"✅ Triggered: {len(snapshot_ids)}/50 profiles")
print(f"⚠️  Failed: {failed}")
print(f"   Expected reels: ~{len(snapshot_ids) * 10}")
print(f"   Projected total: 64 + {len(snapshot_ids) * 10} = {64 + len(snapshot_ids) * 10}")

# Save snapshot IDs
output = {
    "expansion_date": datetime.now().isoformat() + "Z",
    "snapshot_ids": snapshot_ids,
    "current_count": 64,
    "expected_additional": len(snapshot_ids) * 10,
    "projected_total": 64 + len(snapshot_ids) * 10
}

with open('/Volumes/DATA/consulting/garage-organizer-data-collection/raw-data/instagram_massive_expansion_snapshots.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n⏸️  Wait 7-10 minutes for processing")
print(f"   Then run: python3 download_instagram_all_snapshots.py")
