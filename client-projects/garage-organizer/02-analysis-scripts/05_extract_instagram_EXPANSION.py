#!/usr/bin/env python3
"""
INSTAGRAM EXPANSION: Fill gap to reach 200+ reels
Trigger additional garage organization Instagram profiles
"""

import json
import requests
from datetime import datetime

API_TOKEN = "8967cbcf-6c3a-4fd4-8254-ac4c6d466503"
BASE_URL = "https://api.brightdata.com/datasets/v3"
DATASET_ID = "gd_lyclm20il4r5helnj"

# Expanded list of garage/organization influencers
PROFILES = [
    # Already collected (skip):
    # "https://www.instagram.com/neatmethod/",
    # "https://www.instagram.com/thehomeedit/",
    # "https://www.instagram.com/neat_karrie/",

    # NEW - Garage specific:
    "https://www.instagram.com/garagegymreviews/",
    "https://www.instagram.com/garagejournal/",
    "https://www.instagram.com/theshelfdude/",
    "https://www.instagram.com/garagestorage/",
    "https://www.instagram.com/flowwall/",

    # NEW - Organization (with garage content):
    "https://www.instagram.com/cleanmama/",
    "https://www.instagram.com/neatbynicole/",
    "https://www.instagram.com/clutterbug_me/",
    "https://www.instagram.com/casabella/",
    "https://www.instagram.com/mrshinch/",
    "https://www.instagram.com/organization_obsessed/",
    "https://www.instagram.com/arrangeandorganize/",
    "https://www.instagram.com/athomewithashley/",
    "https://www.instagram.com/professionalorganizer/",
    "https://www.instagram.com/simplyorganized/",
]

def trigger_scrape(profile_url, num_posts=30):
    """Trigger Instagram profile scrape"""
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
            print(f"      Error {response.status_code}")
            return None
    except Exception as e:
        print(f"      Exception: {str(e)}")
        return None

def main():
    print("="*80)
    print("INSTAGRAM EXPANSION: Filling coverage gap to 200+ reels")
    print("="*80)
    print(f"Targeting {len(PROFILES)} additional profiles (30 reels each)")
    print(f"Expected: ~{len(PROFILES) * 30} additional reels")

    snapshot_ids = []

    for profile_url in PROFILES:
        profile_name = profile_url.split('/')[-2]
        print(f"\n   Triggering: @{profile_name}")
        snapshot_id = trigger_scrape(profile_url)

        if snapshot_id:
            snapshot_ids.append(snapshot_id)
            print(f"      ✅ {snapshot_id}")
        else:
            print(f"      ⚠️  Failed")

    print(f"\n✅ Triggered {len(snapshot_ids)} new Instagram scrapes")
    print(f"   Snapshot IDs: {snapshot_ids}")

    # Save snapshot IDs
    output = {
        "expansion_date": datetime.now().isoformat() + "Z",
        "snapshot_ids": snapshot_ids,
        "profiles_targeted": PROFILES,
        "expected_reels": len(snapshot_ids) * 30
    }

    with open('/Volumes/DATA/consulting/garage-organizer-data-collection/raw-data/instagram_expansion_snapshots.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n⏸️  Wait ~5 minutes, then run: python3 download_instagram_expansion.py")

if __name__ == "__main__":
    main()
