#!/usr/bin/env python3
"""
CHECKPOINT 05: Extract REAL Instagram Reels
Uses BrightData API to collect real Instagram Reels from relevant profiles

NO SIMULATION - ALL DATA FROM BRIGHTDATA API
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Any
import requests

class InstagramExtractor:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.snapshot_ids = []
        self.total_api_calls = 0
        self.base_url = "https://api.brightdata.com/datasets/v3"

    def extract(self) -> Dict[str, Any]:
        """
        Extract REAL Instagram Reels using BrightData API

        Target: ~500 reels from garage organization influencers
        Method: Scrape reels from relevant Instagram profiles
        """
        print("\n" + "="*70)
        print("CHECKPOINT 05: EXTRACT REAL INSTAGRAM REELS")
        print("="*70)
        print(f"🔄 Starting Instagram extraction from relevant profiles...")

        # Popular garage organization Instagram profiles
        profiles = [
            "https://www.instagram.com/neatmethod/",
            "https://www.instagram.com/thehomeedit/",
            "https://www.instagram.com/organizewithkatie/",
            "https://www.instagram.com/thecontainerstore/",
            "https://www.instagram.com/neat_karrie/",
            "https://www.instagram.com/organizedish/",
            "https://www.instagram.com/organizemyhouse/",
            "https://www.instagram.com/iheartorganizing/",
            "https://www.instagram.com/theorganizedmama/",
            "https://www.instagram.com/simplifiedorganizing/"
        ]

        print(f"   Target profiles: {len(profiles)}")
        print(f"   Posts per profile: 50 reels")
        print(f"   Expected total: ~{len(profiles) * 50} reels")

        # Trigger scraping for each profile
        for profile_url in profiles:
            print(f"\n   Triggering: {profile_url}")
            snapshot_id = self._trigger_instagram_scrape(profile_url, num_posts=50)

            if snapshot_id:
                self.snapshot_ids.append(snapshot_id)
                print(f"      ✅ Snapshot ID: {snapshot_id}")
            else:
                print(f"      ⚠️  Failed to trigger")

        print(f"\n✅ Triggered {len(self.snapshot_ids)} Instagram profile scrapes")
        print(f"   Total API calls: {self.total_api_calls}")

        return self._create_output()

    def _trigger_instagram_scrape(self, profile_url: str, num_posts: int = 50) -> str:
        """Trigger Instagram profile scrape via BrightData API"""
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

        # BrightData dataset ID for Instagram Posts (includes reels)
        dataset_id = "gd_lyclm20il4r5helnj"

        # Payload structure for Instagram profile reels
        payload = {
            "input": [
                {
                    "url": profile_url,
                    "num_of_posts": num_posts,
                    "start_date": "2022-01-01",
                    "end_date": "2025-11-12"
                }
            ]
        }

        # API endpoint - using discover_by=url_all_reels for reels only
        url = f"{self.base_url}/scrape?dataset_id={dataset_id}&notify=false&include_errors=true&type=discover_new&discover_by=url_all_reels"

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=120
            )

            self.total_api_calls += 1

            if response.status_code == 202:
                result = response.json()
                snapshot_id = result.get('snapshot_id')
                return snapshot_id
            else:
                print(f"         API Error {response.status_code}: {response.text[:100]}")
                return None

        except Exception as e:
            print(f"         Exception: {str(e)}")
            return None

    def _create_output(self) -> Dict[str, Any]:
        """Create complete output with snapshot IDs"""
        output = {
            "manifest": {
                "file_name": "instagram_videos_raw.json",
                "extraction_date": datetime.now().isoformat() + "Z",
                "extraction_source": "BrightData API (Instagram Posts - Reels Only)",
                "total_records": 0,
                "quality_gates": {
                    "total_api_calls": self.total_api_calls,
                    "profiles_scraped": len(self.snapshot_ids)
                },
                "checkpoint_metadata": {
                    "checkpoint_name": "CHECKPOINT_05_INSTAGRAM_EXTRACTION",
                    "checkpoint_date": datetime.now().isoformat() + "Z",
                    "checkpoint_status": "SNAPSHOTS_PENDING",
                    "validation_passed": False,
                    "next_checkpoint": "CHECKPOINT_05_INSTAGRAM_DOWNLOAD",
                    "data_source": "REAL - BrightData API"
                },
                "snapshot_ids": self.snapshot_ids,
                "note": "Instagram extraction initiated. Snapshots are being collected. Run download_instagram_snapshots.py after ~5 minutes to retrieve data."
            },
            "videos": []
        }
        return output

def main():
    api_token = "8967cbcf-6c3a-4fd4-8254-ac4c6d466503"
    output_file = "/Volumes/DATA/consulting/garage-organizer-data-collection/raw-data/instagram_videos_raw.json"

    extractor = InstagramExtractor(api_token)
    output = extractor.extract()

    # Save output with snapshot IDs
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    file_size_kb = os.path.getsize(output_file) / 1024

    print(f"\n✅ Output saved: {output_file}")
    print(f"   File size: {file_size_kb:.1f} KB")
    print(f"   Snapshot IDs: {len(output['manifest']['snapshot_ids'])}")
    print(f"   API calls: {extractor.total_api_calls}")
    print(f"   Source: REAL BrightData API")
    print(f"\n⏸️  Wait ~5 minutes for BrightData to process snapshots")
    print(f"   Then run: python3 download_instagram_snapshots.py")

if __name__ == "__main__":
    main()
