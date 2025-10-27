#!/usr/bin/env python3
"""
Collect YouTube consumer insights using Bright Data YouTube API.
Uses existing Bright Data credits.
"""

import os
import json
import requests
from pathlib import Path
from time import sleep

# Bright Data API endpoint
BRIGHTDATA_API_URL = "https://api.brightdata.com/datasets/v3/scrape"
BRIGHTDATA_DATASET_ID = "gd_lk56epmy2i5g7lzu0k"  # YouTube dataset

# Search queries for garage organization consumer insights
YOUTUBE_SEARCHES = [
    {
        "keyword": "garage organization",
        "num_of_posts": "30",
        "start_date": "01-01-2024",
        "end_date": "10-24-2025",
        "country": ""
    },
    {
        "keyword": "garage makeover",
        "num_of_posts": "30",
        "start_date": "01-01-2024",
        "end_date": "10-24-2025",
        "country": ""
    },
    {
        "keyword": "organize garage",
        "num_of_posts": "25",
        "start_date": "01-01-2024",
        "end_date": "10-24-2025",
        "country": ""
    },
    {
        "keyword": "garage storage ideas",
        "num_of_posts": "25",
        "start_date": "01-01-2024",
        "end_date": "10-24-2025",
        "country": ""
    },
    {
        "keyword": "garage transformation",
        "num_of_posts": "25",
        "start_date": "01-01-2024",
        "end_date": "10-24-2025",
        "country": ""
    },
    {
        "keyword": "DIY garage organization",
        "num_of_posts": "25",
        "start_date": "01-01-2024",
        "end_date": "10-24-2025",
        "country": ""
    }
]

def collect_youtube_brightdata(api_token: str):
    """Collect YouTube data using Bright Data API."""

    print("="*70)
    print("YOUTUBE CONSUMER INSIGHTS COLLECTION (BRIGHT DATA)")
    print("Target: Consumer language, viral trends, pain points")
    print("="*70)
    print()

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    params = {
        "dataset_id": BRIGHTDATA_DATASET_ID,
        "notify": "false",
        "include_errors": "true",
        "type": "discover_new",
        "discover_by": "keyword"
    }

    payload = {
        "input": YOUTUBE_SEARCHES
    }

    print(f"Sending request to Bright Data...")
    print(f"Searches: {len(YOUTUBE_SEARCHES)}")
    print(f"Keywords: {', '.join([s['keyword'] for s in YOUTUBE_SEARCHES[:3]])}...")
    print(f"Total videos requested: {sum(int(s['num_of_posts']) for s in YOUTUBE_SEARCHES)}")

    try:
        response = requests.post(
            BRIGHTDATA_API_URL,
            headers=headers,
            params=params,
            json=payload,
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()

            print(f"\n✅ Request successful!")
            print(f"Response: {json.dumps(result, indent=2)[:500]}...")

            # Bright Data typically returns a snapshot_id for async collection
            if 'snapshot_id' in result:
                snapshot_id = result['snapshot_id']
                print(f"\nSnapshot ID: {snapshot_id}")
                print(f"Data will be available at Bright Data dashboard")
                print(f"Or check status at: https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}")

            # Save response
            output_dir = Path(__file__).parent / "data"
            output_file = output_dir / "youtube_brightdata_response.json"

            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)

            print(f"\n✓ Response saved to {output_file.name}")

            return result

        else:
            print(f"\n❌ Error: HTTP {response.status_code}")
            print(f"Response: {response.text[:500]}")

            if response.status_code == 401:
                print("\n⚠️  Authorization failed. Please check Bright Data API token.")
            elif response.status_code == 402:
                print("\n⚠️  Payment required. Bright Data credits may be exhausted.")

            return None

    except requests.exceptions.Timeout:
        print(f"\n❌ Request timeout after 60 seconds")
        return None
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None

def main():
    # Extract credentials from WebSocket URL
    ws_url = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222"

    import re
    match = re.search(r'zone-([^:]+):([^@]+)', ws_url)

    if match:
        zone = match.group(1)
        password = match.group(2)

        print(f"Attempting with credentials from WebSocket URL...")
        print(f"Zone: {zone}")
        print(f"Password: {password[:10]}...")

        # Try using password as API token
        result = collect_youtube_brightdata(password)

        if result:
            print("\n" + "="*70)
            print("YOUTUBE COLLECTION INITIATED")
            print("="*70)
            print("\nNext steps:")
            print("1. Data will be collected asynchronously by Bright Data")
            print("2. Check Bright Data dashboard for results")
            print("3. Download results and save to data/youtube_consumer_insights.json")
            print("\nExpected data:")
            print("  - 180 videos total")
            print("  - Titles, descriptions, tags, engagement metrics")
            print("  - Consumer language patterns")
            print("  - Pain points and aspirational language")

    else:
        print("❌ Could not extract Bright Data credentials")
        print("Please provide Bright Data API token manually")

if __name__ == "__main__":
    main()
