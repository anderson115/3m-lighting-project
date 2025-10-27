#!/usr/bin/env python3
"""
Collect YouTube video data about garage organization using Apify.
Focus on consumer language, trends, pain points from video titles/descriptions.
"""

import os
import json
from pathlib import Path
from apify_client import ApifyClient

# Initialize Apify client
client = ApifyClient(os.environ.get('APIFY_API_TOKEN'))

# YouTube scraper actor
YOUTUBE_ACTOR = "bernardo/youtube-scraper"

# Search queries for garage organization content
SEARCH_QUERIES = [
    "garage organization",
    "garage makeover",
    "organize garage",
    "garage storage ideas",
    "garage transformation",
    "DIY garage organization",
    "garage organization hacks",
    "small garage organization"
]

def search_youtube(query, max_results=30):
    """Search YouTube and get video metadata."""
    print(f"🎥 Searching YouTube: '{query}'")

    run_input = {
        "searchKeywords": query,
        "maxResults": max_results,
        "uploadDate": "year",  # Last year for current trends
        "sortBy": "RELEVANCE"
    }

    try:
        run = client.actor(YOUTUBE_ACTOR).call(run_input=run_input)

        videos = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            videos.append({
                "title": item.get("title", ""),
                "description": item.get("description", ""),
                "channel": item.get("channelName", ""),
                "views": item.get("viewCount", 0),
                "likes": item.get("likeCount", 0),
                "published": item.get("publishedAt", ""),
                "url": item.get("url", ""),
                "search_query": query
            })

        print(f"   ✓ Found {len(videos)} videos")
        return videos
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
        return []

def main():
    print("="*70)
    print("YOUTUBE CONSUMER INSIGHTS COLLECTION")
    print("Target: Video trends, DIY language, pain points, aspirations")
    print("="*70)
    print()

    all_videos = []

    for i, query in enumerate(SEARCH_QUERIES, 1):
        print(f"\n[Search {i}/{len(SEARCH_QUERIES)}]")
        videos = search_youtube(query, max_results=25)
        all_videos.extend(videos)

    # Deduplicate by URL
    seen_urls = set()
    unique_videos = []
    for video in all_videos:
        url = video.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_videos.append(video)

    print()
    print("="*70)
    print("YOUTUBE COLLECTION SUMMARY")
    print("="*70)
    print(f"Total videos collected: {len(unique_videos)}")

    # Save results
    output_dir = Path(__file__).parent / "data"
    output_file = output_dir / "youtube_garage_insights.json"

    with open(output_file, 'w') as f:
        json.dump({
            "platform": "YouTube",
            "collected_at": "2025-10-24",
            "purpose": "Consumer language, DIY trends, pain points analysis",
            "searches": SEARCH_QUERIES,
            "video_count": len(unique_videos),
            "videos": unique_videos
        }, f, indent=2)

    print(f"\n✓ Saved to {output_file}")

    # Quick analysis
    if unique_videos:
        total_views = sum(v.get("views", 0) for v in unique_videos)
        avg_views = total_views / len(unique_videos)
        print(f"\nQuick Stats:")
        print(f"  Average views per video: {avg_views:,.0f}")
        print(f"  Total combined views: {total_views:,.0f}")

if __name__ == "__main__":
    main()
