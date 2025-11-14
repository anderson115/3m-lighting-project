#!/usr/bin/env python3
"""
Collect 3M Claw consumer insights from YouTube and TikTok.
Target: 100+ videos combined across platforms.
"""

import os
import json
import requests
from pathlib import Path
from time import sleep
from datetime import datetime

# Bright Data API endpoint
BRIGHTDATA_API_URL = "https://api.brightdata.com/datasets/v3/scrape"
YOUTUBE_DATASET_ID = "gd_lk56epmy2i5g7lzu0k"
TIKTOK_DATASET_ID = "gd_lu702nij2f790tmv9h"  # TikTok dataset

# YouTube search queries for 3M Claw
YOUTUBE_SEARCHES = [
    {
        "keyword": "3M Claw hooks",
        "num_of_posts": "30",
        "start_date": "01-01-2023",
        "end_date": "12-31-2025",
        "country": ""
    },
    {
        "keyword": "3M Claw drywall hangers",
        "num_of_posts": "25",
        "start_date": "01-01-2023",
        "end_date": "12-31-2025",
        "country": ""
    },
    {
        "keyword": "3M Claw review",
        "num_of_posts": "20",
        "start_date": "01-01-2023",
        "end_date": "12-31-2025",
        "country": ""
    },
    {
        "keyword": "3M Claw installation",
        "num_of_posts": "15",
        "start_date": "01-01-2023",
        "end_date": "12-31-2025",
        "country": ""
    },
    {
        "keyword": "3M Claw garage",
        "num_of_posts": "15",
        "start_date": "01-01-2023",
        "end_date": "12-31-2025",
        "country": ""
    },
    {
        "keyword": "3M Claw picture hanger",
        "num_of_posts": "15",
        "start_date": "01-01-2023",
        "end_date": "12-31-2025",
        "country": ""
    }
]

# TikTok search queries for 3M Claw
TIKTOK_SEARCHES = [
    {
        "keyword": "3M Claw",
        "num_of_posts": "20",
        "start_date": "01-01-2023",
        "end_date": "12-31-2025"
    },
    {
        "keyword": "3M Claw hooks",
        "num_of_posts": "15",
        "start_date": "01-01-2023",
        "end_date": "12-31-2025"
    },
    {
        "keyword": "3M Claw review",
        "num_of_posts": "10",
        "start_date": "01-01-2023",
        "end_date": "12-31-2025"
    }
]

def collect_youtube_data(api_token: str):
    """Collect YouTube data for 3M Claw."""

    print("="*70)
    print("COLLECTING 3M CLAW YOUTUBE VIDEOS")
    print("Target: 120 videos across 6 search queries")
    print("="*70)
    print()

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    # Convert queries to Bright Data format
    input_data = []
    for query in YOUTUBE_SEARCHES:
        input_data.append({
            "keyword_search": query["keyword"],
            "upload_date": "This year",
            "type": "Video",
            "country": query.get("country", "")
        })

    params = {
        "dataset_id": YOUTUBE_DATASET_ID,
        "notify": "false",
        "include_errors": "true",
        "type": "discover_new",
        "discover_by": "search_filters"
    }

    payload = {"input": input_data}

    print(f"\nSending batch request for {len(YOUTUBE_SEARCHES)} queries")

    all_videos = []

    try:
        response = requests.post(
            BRIGHTDATA_API_URL,
            params=params,
            headers=headers,
            json=payload,
            timeout=120
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✓ Success: {len(data) if isinstance(data, list) else 'Response received'}")
            if isinstance(data, list):
                all_videos.extend(data)
            else:
                print(f"Response: {data}")
        else:
            print(f"✗ Error {response.status_code}: {response.text}")

    except Exception as e:
        print(f"✗ Exception: {str(e)}")

    print(f"\n{'='*70}")
    print(f"YOUTUBE TOTAL: {len(all_videos)} videos collected")
    print(f"{'='*70}\n")

    return all_videos

def collect_tiktok_data(api_token: str):
    """Collect TikTok data for 3M Claw."""

    print("="*70)
    print("COLLECTING 3M CLAW TIKTOK VIDEOS")
    print("Target: 45 videos across 3 search queries")
    print("="*70)
    print()

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    # Convert queries to Bright Data format (TikTok uses search_keyword)
    input_data = []
    for query in TIKTOK_SEARCHES:
        input_data.append({
            "search_keyword": query["keyword"],
            "country": query.get("country", "")
        })

    params = {
        "dataset_id": TIKTOK_DATASET_ID,
        "notify": "false",
        "include_errors": "true",
        "type": "discover_new",
        "discover_by": "keyword"
    }

    payload = {"input": input_data}

    print(f"\nSending batch request for {len(TIKTOK_SEARCHES)} queries")

    all_videos = []

    try:
        response = requests.post(
            BRIGHTDATA_API_URL,
            params=params,
            headers=headers,
            json=payload,
            timeout=120
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✓ Success: {len(data) if isinstance(data, list) else 'Response received'}")
            if isinstance(data, list):
                all_videos.extend(data)
            else:
                print(f"Response: {data}")
        else:
            print(f"✗ Error {response.status_code}: {response.text}")

    except Exception as e:
        print(f"✗ Exception: {str(e)}")

    print(f"\n{'='*70}")
    print(f"TIKTOK TOTAL: {len(all_videos)} videos collected")
    print(f"{'='*70}\n")

    return all_videos

def save_results(youtube_videos, tiktok_videos):
    """Save collected videos to JSON files."""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save YouTube results
    youtube_file = f"outputs/3m_claw_youtube_videos_{timestamp}.json"
    with open(youtube_file, 'w') as f:
        json.dump(youtube_videos, f, indent=2)
    print(f"✓ Saved YouTube videos to: {youtube_file}")

    # Save TikTok results
    tiktok_file = f"outputs/3m_claw_tiktok_videos_{timestamp}.json"
    with open(tiktok_file, 'w') as f:
        json.dump(tiktok_videos, f, indent=2)
    print(f"✓ Saved TikTok videos to: {tiktok_file}")

    # Save combined results
    combined = {
        "youtube": youtube_videos,
        "tiktok": tiktok_videos,
        "total_count": len(youtube_videos) + len(tiktok_videos),
        "youtube_count": len(youtube_videos),
        "tiktok_count": len(tiktok_videos),
        "collected_at": timestamp
    }

    combined_file = f"outputs/3m_claw_all_videos_{timestamp}.json"
    with open(combined_file, 'w') as f:
        json.dump(combined, f, indent=2)
    print(f"✓ Saved combined results to: {combined_file}")

    return combined_file

def main():
    """Main execution."""

    # Check for Bright Data API token
    api_token = os.getenv('BRIGHTDATA_API_TOKEN')

    if not api_token:
        print("ERROR: BRIGHTDATA_API_TOKEN environment variable not set")
        print("\nPlease set your Bright Data API token:")
        print("  export BRIGHTDATA_API_TOKEN='your_token_here'")
        return

    # Collect YouTube videos
    youtube_videos = collect_youtube_data(api_token)

    # Collect TikTok videos
    tiktok_videos = collect_tiktok_data(api_token)

    # Summary
    total = len(youtube_videos) + len(tiktok_videos)
    print(f"\n{'='*70}")
    print(f"COLLECTION COMPLETE")
    print(f"{'='*70}")
    print(f"YouTube videos: {len(youtube_videos)}")
    print(f"TikTok videos: {len(tiktok_videos)}")
    print(f"Total collected: {total}")
    print(f"Target met: {'✓ YES' if total >= 100 else '✗ NO (target: 100)'}")
    print(f"{'='*70}\n")

    # Save results
    if total > 0:
        output_file = save_results(youtube_videos, tiktok_videos)
        print(f"\n✓ All data saved successfully")
        print(f"  Main file: {output_file}")
    else:
        print("\n✗ No videos collected - check API token and queries")

if __name__ == "__main__":
    main()
