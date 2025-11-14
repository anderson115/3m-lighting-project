#!/usr/bin/env python3
"""
Instagram Final: 40 profiles for 50+ creators
Budget: $6 (40 profiles × 5 reels × $0.03 = $6)
"""

import json
import requests
from datetime import datetime
import time

API_TOKEN = "8967cbcf-6c3a-4fd4-8254-ac4c6d466503"
BASE_URL = "https://api.brightdata.com/datasets/v3"
DATASET_ID = "gd_lyclm20il4r5helnj"

# 40 diverse garage/organization/DIY profiles
PROFILES = [
    # Garage specific
    "https://www.instagram.com/garageorganizers/",
    "https://www.instagram.com/garage.life/",
    "https://www.instagram.com/organized.garage/",
    "https://www.instagram.com/garage.solutions/",
    "https://www.instagram.com/mygaragespace/",

    # Organization pros
    "https://www.instagram.com/organizedbyamber/",
    "https://www.instagram.com/theorganizedhousewife/",
    "https://www.instagram.com/organizedspace/",
    "https://www.instagram.com/homeorganizers/",
    "https://www.instagram.com/organize.everything/",
    "https://www.instagram.com/tidy.at.home/",
    "https://www.instagram.com/theorganizer/",
    "https://www.instagram.com/minimal_home/",
    "https://www.instagram.com/organize.home/",
    "https://www.instagram.com/organized.by.tidy/",

    # DIY/Workshop
    "https://www.instagram.com/workshop.organized/",
    "https://www.instagram.com/garage.workshop/",
    "https://www.instagram.com/tool.organization/",
    "https://www.instagram.com/workshopdesign/",
    "https://www.instagram.com/diy.garage/",
    "https://www.instagram.com/buildwithbobby/",
    "https://www.instagram.com/workshop_life/",
    "https://www.instagram.com/garage.build/",

    # Home improvement
    "https://www.instagram.com/diyhomeimprovement/",
    "https://www.instagram.com/home.renovation/",
    "https://www.instagram.com/homeimprovement_diy/",
    "https://www.instagram.com/renovate.design/",
    "https://www.instagram.com/homemakeover/",
    "https://www.instagram.com/home.projects/",

    # Storage brands/retailers
    "https://www.instagram.com/rubbermaid/",
    "https://www.instagram.com/gladiatorgarageworks/",
    "https://www.instagram.com/craftsman/",
    "https://www.instagram.com/dewalt/",
    "https://www.instagram.com/milwaukeetool/",
    "https://www.instagram.com/ridgid/",

    # Organization lifestyle
    "https://www.instagram.com/organized.living/",
    "https://www.instagram.com/neat.life/",
    "https://www.instagram.com/tidy.home/",
    "https://www.instagram.com/organized.daily/",
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
print("INSTAGRAM FINAL: 40 profiles × 5 reels = 200 reels ($6 budget)")
print("="*80)
print(f"Current: 34 creators | Target: 50+ creators | Budget: $6")
print(f"Strategy: Account for 50% failure rate, expect 20 new profiles × 5 reels\n")

snapshot_ids = []

for i, profile_url in enumerate(PROFILES, 1):
    profile_name = profile_url.split('/')[-2]
    print(f"[{i:2d}/40] {profile_name:30s}", end=" ", flush=True)

    snapshot_id = trigger_scrape(profile_url, num_posts=5)

    if snapshot_id:
        snapshot_ids.append(snapshot_id)
        print(f"✅ {snapshot_id}")
    else:
        print(f"⚠️  Failed")

    time.sleep(1.2)

print(f"\n{'='*80}")
print(f"✅ Triggered: {len(snapshot_ids)}/40 profiles")
print(f"   Expected new creators: ~{int(len(snapshot_ids) * 0.75)}")
print(f"   Projected total: 34 + {int(len(snapshot_ids) * 0.75)} = {34 + int(len(snapshot_ids) * 0.75)} creators")
print(f"   Est cost: ${len(snapshot_ids) * 5 * 0.03:.2f}")

output = {
    "expansion_date": datetime.now().isoformat() + "Z",
    "snapshot_ids": snapshot_ids,
    "current_creators": 34,
    "target_creators": 50,
    "triggered_profiles": len(snapshot_ids),
    "estimated_cost": len(snapshot_ids) * 5 * 0.03
}

with open('/Volumes/DATA/consulting/garage-organizer-data-collection/raw-data/instagram_40_profiles_snapshots.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n⏸️  Wait 7 minutes for processing")
