#!/usr/bin/env python3
"""
Debug script to inspect raw Apify results
"""

import os
import json
from apify_client import ApifyClient

# Get token
apify_token = os.getenv('APIFY_TOKEN')
if not apify_token:
    print("Error: APIFY_TOKEN not set")
    exit(1)

client = ApifyClient(apify_token)

# Test search
query = "garage hooks fail"
run_input = {
    "searchQueries": [query],
    "resultsPerPage": 5,  # Just get 5 for inspection
    "excludePinnedPosts": False,
}

print(f"Searching TikTok for: '{query}'")
print("="*60)

try:
    run = client.actor("clockworks/free-tiktok-scraper").call(run_input=run_input)

    results = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        results.append(item)

    print(f"Found {len(results)} videos\n")

    # Print first video's structure
    if results:
        print("First video structure:")
        print(json.dumps(results[0], indent=2))

        print("\n" + "="*60)
        print("Stats for all videos:")
        for i, video in enumerate(results, 1):
            stats = video.get('stats', {})
            video_info = video.get('video', {})
            print(f"\nVideo {i}:")
            print(f"  ID: {video.get('id', 'N/A')}")
            print(f"  URL: {video.get('webVideoUrl', 'N/A')}")
            print(f"  Views: {stats.get('playCount', 0)}")
            print(f"  Likes: {stats.get('diggCount', 0)}")
            print(f"  Duration: {video_info.get('duration', 0)}s")
            print(f"  Description: {video.get('desc', 'N/A')[:100]}")

except Exception as e:
    print(f"Error: {e}")
