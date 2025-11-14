#!/usr/bin/env python3
"""
Collect YouTube consumer insights using existing YouTube API.
FREE - uses configured YOUTUBE_API_KEY.
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from project root
project_root = Path(__file__).parent.parent.parent
load_dotenv(project_root / '.env')

# Add core to path
sys.path.insert(0, str(project_root / 'core'))

from data_sources.youtube import YouTubeDataSource

# Search queries for garage organization consumer insights
SEARCH_QUERIES = [
    "garage organization",
    "garage makeover",
    "organize garage",
    "garage storage ideas",
    "garage transformation",
    "DIY garage organization"
]

def collect_youtube_insights():
    """Collect YouTube video metadata for consumer language analysis."""

    print("="*70)
    print("YOUTUBE CONSUMER INSIGHTS COLLECTION")
    print("Target: Consumer language, trends, pain points from YouTube")
    print("="*70)
    print()

    try:
        yt = YouTubeDataSource()
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Please ensure YOUTUBE_API_KEY is set in .env file")
        return []

    all_videos = []
    seen_ids = set()

    for i, query in enumerate(SEARCH_QUERIES, 1):
        print(f"\n[Search {i}/{len(SEARCH_QUERIES)}]")
        print(f"🔍 Searching: '{query}'")

        try:
            # Search with recent videos prioritized
            videos = yt.search_videos(
                query=query,
                max_results=30,  # 30 per query = 180 total
                order='relevance',
                published_after='2024-01-01T00:00:00Z'  # Last year
            )

            new_count = 0
            for video in videos:
                video_id = video['video_id']
                if video_id not in seen_ids:
                    seen_ids.add(video_id)

                    # Get detailed metadata
                    try:
                        metadata = yt.get_video_metadata(video_id)
                        metadata['search_query'] = query
                        all_videos.append(metadata)
                        new_count += 1
                    except Exception as e:
                        print(f"   ⚠️  Skipped {video_id}: {str(e)[:50]}")

            print(f"   ✓ Found {len(videos)} videos, {new_count} unique")
            print(f"   Total collected: {len(all_videos)}")

        except Exception as e:
            print(f"   ❌ Error: {str(e)[:100]}")

    print()
    print("="*70)
    print("YOUTUBE COLLECTION COMPLETE")
    print("="*70)
    print(f"Total unique videos: {len(all_videos)}")

    if all_videos:
        # Calculate stats
        total_views = sum(v.get('view_count', 0) for v in all_videos)
        total_likes = sum(v.get('like_count', 0) for v in all_videos)
        avg_views = total_views / len(all_videos) if all_videos else 0

        print(f"\nQuick Stats:")
        print(f"  Total views across all videos: {total_views:,}")
        print(f"  Total likes across all videos: {total_likes:,}")
        print(f"  Average views per video: {avg_views:,.0f}")

        # Save results
        output_dir = Path(__file__).parent / "data"
        output_file = output_dir / "youtube_garage_consumer_insights.json"

        output_data = {
            "platform": "YouTube",
            "collected_at": "2025-10-24",
            "purpose": "Consumer language, DIY trends, pain points analysis",
            "searches": SEARCH_QUERIES,
            "video_count": len(all_videos),
            "total_views": total_views,
            "total_likes": total_likes,
            "videos": all_videos
        }

        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)

        print(f"\n✓ Saved to {output_file.name}")

        # Extract sample consumer language
        print(f"\n{'='*70}")
        print("SAMPLE CONSUMER LANGUAGE FROM TITLES")
        print(f"{'='*70}")

        for i, video in enumerate(all_videos[:5], 1):
            print(f"\n{i}. {video['title']}")
            print(f"   Views: {video['view_count']:,} | Likes: {video['like_count']:,}")
            if video.get('tags'):
                print(f"   Tags: {', '.join(video['tags'][:5])}")

    return all_videos

if __name__ == "__main__":
    collect_youtube_insights()
