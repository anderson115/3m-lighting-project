#!/usr/bin/env python3
"""
Collect 3M Claw YouTube videos using free YouTube Data API v3.
Target: 100+ videos about 3M Claw products.
"""

import os
import json
import requests
from datetime import datetime

# YouTube Data API v3 endpoint
YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"

# Search queries for 3M Claw
SEARCH_QUERIES = [
    "3M Claw hooks",
    "3M Claw review",
    "3M Claw drywall hangers",
    "3M Claw installation",
    "3M Claw picture hanger",
    "3M Claw garage organization",
    "3M Claw vs Command hooks",
    "3M Claw how to use",
    "3M Claw product review",
    "3M Claw unboxing",
]

def search_youtube(api_key, query, max_results=15):
    """Search YouTube and get video metadata."""
    print(f"\n🎥 Searching: '{query}' (target: {max_results} videos)")

    # Search for videos
    search_url = f"{YOUTUBE_API_BASE}/search"
    search_params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": api_key,
        "order": "relevance"
    }

    try:
        response = requests.get(search_url, params=search_params)
        response.raise_for_status()
        search_data = response.json()

        if "items" not in search_data:
            print(f"   ✗ No results found")
            return []

        video_ids = [item["id"]["videoId"] for item in search_data["items"]]

        # Get detailed video statistics
        videos_url = f"{YOUTUBE_API_BASE}/videos"
        videos_params = {
            "part": "snippet,statistics,contentDetails",
            "id": ",".join(video_ids),
            "key": api_key
        }

        response = requests.get(videos_url, params=videos_params)
        response.raise_for_status()
        videos_data = response.json()

        videos = []
        for item in videos_data.get("items", []):
            videos.append({
                "video_id": item["id"],
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "channel": item["snippet"]["channelTitle"],
                "channel_id": item["snippet"]["channelId"],
                "views": int(item["statistics"].get("viewCount", 0)),
                "likes": int(item["statistics"].get("likeCount", 0)),
                "comments": int(item["statistics"].get("commentCount", 0)),
                "upload_date": item["snippet"]["publishedAt"],
                "duration": item["contentDetails"]["duration"],
                "url": f"https://youtube.com/watch?v={item['id']}",
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
                "search_query": query
            })

        print(f"   ✓ Collected {len(videos)} videos")
        return videos

    except requests.exceptions.RequestException as e:
        print(f"   ✗ Error: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"   Response: {e.response.text}")
        return []

def main():
    """Collect 3M Claw YouTube videos."""

    print("="*70)
    print("3M CLAW YOUTUBE VIDEO COLLECTION (FREE API)")
    print("="*70)
    print(f"Queries: {len(SEARCH_QUERIES)}")
    print(f"Target: ~{len(SEARCH_QUERIES) * 15} videos")
    print()

    # Check API key
    api_key = os.environ.get('YOUTUBE_API_KEY')
    if not api_key:
        print("ERROR: YOUTUBE_API_KEY not set")
        print("Get a free API key from: https://console.cloud.google.com/apis/credentials")
        print("\nAttempting to load from .env file...")
        try:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.environ.get('YOUTUBE_API_KEY')
            if not api_key:
                print("ERROR: YOUTUBE_API_KEY not found in .env file")
                return
        except ImportError:
            print("ERROR: python-dotenv not installed")
            return

    all_videos = []

    for i, query in enumerate(SEARCH_QUERIES, 1):
        print(f"[{i}/{len(SEARCH_QUERIES)}]", end="")
        videos = search_youtube(api_key, query, max_results=15)
        all_videos.extend(videos)

    # Remove duplicates by video_id
    unique_videos = {}
    for video in all_videos:
        vid_id = video.get('video_id')
        if vid_id and vid_id not in unique_videos:
            unique_videos[vid_id] = video

    final_videos = list(unique_videos.values())

    print(f"\n{'='*70}")
    print(f"COLLECTION COMPLETE")
    print(f"{'='*70}")
    print(f"Total collected: {len(all_videos)} videos")
    print(f"After deduplication: {len(final_videos)} unique videos")
    print(f"Target met: {'✓ YES' if len(final_videos) >= 100 else f'✗ NO ({len(final_videos)}/100)'}")
    print(f"{'='*70}\n")

    # Save results
    if final_videos:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"outputs/3m_claw_youtube_videos_{timestamp}.json"

        os.makedirs("outputs", exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(final_videos, f, indent=2)

        print(f"✓ Saved to: {output_file}")
        print(f"  Total videos: {len(final_videos)}")
        print(f"  Total views: {sum(v.get('views', 0) for v in final_videos):,}")

        # Show top channels
        channels = {}
        for v in final_videos:
            ch = v.get('channel', 'Unknown')
            channels[ch] = channels.get(ch, 0) + 1

        print(f"\n  Top channels:")
        for ch, count in sorted(channels.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"    {ch}: {count} videos")
    else:
        print("\n✗ No videos collected")

if __name__ == "__main__":
    main()
