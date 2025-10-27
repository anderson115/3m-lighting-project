#!/usr/bin/env python3
"""
Collect TikTok consumer insights using Apify TikTok Scraper.
Downloads videos for transcript extraction.
"""

import os
import json
import time
from pathlib import Path
from apify_client import ApifyClient

# Initialize Apify client
APIFY_TOKEN = os.getenv('APIFY_API_TOKEN', 'YOUR_TOKEN_HERE')
client = ApifyClient(APIFY_TOKEN)

# TikTok hashtags for garage organization
HASHTAGS = [
    "garageorganization",
    "garagemakeover",
    "garagehacks",
    "garagestorage",
    "organizedgarage",
    "garagetransformation",
    "DIYgarage"
]

print("="*70)
print("TIKTOK CONSUMER INSIGHTS COLLECTION (APIFY)")
print("Target: Consumer language, viral trends, DIY hacks")
print("="*70)
print()

# Configuration for TikTok scraper
run_input = {
    "hashtags": HASHTAGS,
    "resultsPerPage": 50,  # 50 videos per hashtag
    "shouldDownloadVideos": True,  # CRITICAL - downloads video files
    "shouldDownloadCovers": False,
    "shouldDownloadSlideshowImages": False
}

print(f"Hashtags: {', '.join(HASHTAGS)}")
print(f"Videos per hashtag: 50")
print(f"Expected total: ~{len(HASHTAGS) * 50} videos")
print(f"Video downloads: ENABLED")
print()

try:
    print("Starting Apify TikTok scraper...")
    print("This will take 10-20 minutes...")
    print()

    # Run the Actor and wait for it to finish
    run = client.actor("clockworks/tiktok-scraper").call(run_input=run_input)

    print(f"✅ Scraper completed!")
    print(f"Run ID: {run['id']}")
    print(f"Dataset ID: {run['defaultDatasetId']}")
    print()

    # Fetch results from the dataset
    print("Fetching results from dataset...")
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    print(f"✅ Retrieved {len(items)} TikTok videos")
    print()

    # Create output directory
    output_dir = Path(__file__).parent / "data"
    output_dir.mkdir(exist_ok=True)

    video_dir = output_dir / "tiktok_videos"
    video_dir.mkdir(exist_ok=True)

    # Process and save data
    processed_videos = []

    for i, item in enumerate(items, 1):
        video_data = {
            "id": item.get("id"),
            "text": item.get("text", ""),  # Caption
            "hashtags": item.get("hashtags", []),
            "likes": item.get("diggCount", 0),
            "comments": item.get("commentCount", 0),
            "shares": item.get("shareCount", 0),
            "views": item.get("playCount", 0),
            "author": item.get("authorMeta", {}).get("name", ""),
            "music": item.get("musicMeta", {}).get("musicName", ""),
            "video_url": item.get("videoUrl", ""),
            "download_url": item.get("videoUrlNoWaterMark", "") or item.get("videoUrl", ""),
            "created_at": item.get("createTimeISO", "")
        }

        processed_videos.append(video_data)

        # Download video if URL available
        if video_data["download_url"]:
            try:
                import requests
                video_filename = video_dir / f"{video_data['id']}.mp4"

                if not video_filename.exists():
                    response = requests.get(video_data["download_url"], timeout=30)
                    if response.status_code == 200:
                        with open(video_filename, 'wb') as f:
                            f.write(response.content)
                        print(f"  [{i}/{len(items)}] Downloaded: {video_data['id']}.mp4")
                    else:
                        print(f"  [{i}/{len(items)}] Download failed: HTTP {response.status_code}")
                else:
                    print(f"  [{i}/{len(items)}] Already exists: {video_data['id']}.mp4")
            except Exception as e:
                print(f"  [{i}/{len(items)}] Error downloading: {str(e)[:50]}")

    # Save metadata
    output_data = {
        "platform": "TikTok",
        "collected_at": time.strftime("%Y-%m-%d"),
        "purpose": "Consumer language, viral trends, DIY hacks analysis",
        "hashtags": HASHTAGS,
        "video_count": len(processed_videos),
        "total_views": sum(v.get("views", 0) for v in processed_videos),
        "total_likes": sum(v.get("likes", 0) for v in processed_videos),
        "videos": processed_videos
    }

    output_file = output_dir / "tiktok_garage_consumer_insights.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print()
    print("="*70)
    print("TIKTOK COLLECTION COMPLETE")
    print("="*70)
    print(f"Total videos: {len(processed_videos)}")
    print(f"Total views: {output_data['total_views']:,}")
    print(f"Total likes: {output_data['total_likes']:,}")
    print()
    print(f"Metadata saved: {output_file.name}")
    print(f"Videos saved: {video_dir}")
    print()

    # Calculate engagement stats
    if processed_videos:
        avg_views = output_data['total_views'] / len(processed_videos)
        avg_likes = output_data['total_likes'] / len(processed_videos)

        print("Quick Stats:")
        print(f"  Average views per video: {avg_views:,.0f}")
        print(f"  Average likes per video: {avg_likes:,.0f}")

        # Top hashtags
        from collections import Counter
        all_hashtags = []
        for v in processed_videos:
            all_hashtags.extend(v.get("hashtags", []))

        if all_hashtags:
            hashtag_counts = Counter(all_hashtags)
            print()
            print("Top hashtags found:")
            for tag, count in hashtag_counts.most_common(10):
                print(f"  #{tag}: {count} uses")

    print()
    print("="*70)
    print("NEXT STEP: Transcript extraction with Whisper")
    print("="*70)

except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
