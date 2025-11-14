#!/usr/bin/env python3
"""
Alternative TikTok scraper using direct HTTP requests (no browser needed).
Bypasses Bright Data KYC restriction by using public TikTok API endpoints.
"""

import json
import requests
from datetime import datetime
import time

# TikTok search queries
TIKTOK_QUERIES = [
    "3M Claw",
    "3M Claw hooks",
    "3M Claw review",
    "3M Claw drywall",
    "3M Claw hanger",
    "claw drywall hanger",
    "3M picture hanger",
    "3M hooks review",
]

def search_tiktok_web(query, count=50):
    """Search TikTok using web scraping approach."""
    print(f"\n📱 TikTok: Searching '{query}' (target: {count} videos)")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Referer': 'https://www.tiktok.com/',
    }

    try:
        # TikTok public search endpoint (used by website)
        url = f"https://www.tiktok.com/api/search/general/full/"
        params = {
            'keyword': query,
            'offset': 0,
            'count': count,
            'type': 1,  # Video search
        }

        response = requests.get(url, headers=headers, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            videos = []

            # Parse TikTok API response
            if 'data' in data:
                for item in data.get('data', []):
                    if 'item' in item:
                        video = item['item']
                        videos.append({
                            'video_id': video.get('id', ''),
                            'title': video.get('desc', ''),
                            'url': f"https://www.tiktok.com/@{video.get('author', {}).get('uniqueId', '')}/video/{video.get('id', '')}",
                            'channel': video.get('author', {}).get('uniqueId', ''),
                            'views': video.get('stats', {}).get('playCount', 0),
                            'likes': video.get('stats', {}).get('diggCount', 0),
                            'shares': video.get('stats', {}).get('shareCount', 0),
                            'platform': 'tiktok',
                            'search_query': query
                        })

            print(f"   ✓ Collected {len(videos)} videos")
            return videos
        else:
            print(f"   ✗ HTTP {response.status_code}")
            return []

    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        return []

def main():
    """Collect TikTok videos using alternative method."""

    print("="*70)
    print("3M CLAW TIKTOK COLLECTION (ALTERNATIVE METHOD)")
    print("="*70)
    print(f"Queries: {len(TIKTOK_QUERIES)}")
    print(f"Method: Direct API (no browser required)")
    print()

    all_videos = []

    for i, query in enumerate(TIKTOK_QUERIES, 1):
        print(f"[{i}/{len(TIKTOK_QUERIES)}]", end="")
        videos = search_tiktok_web(query, count=50)
        all_videos.extend(videos)
        time.sleep(2)  # Rate limiting

    # Remove duplicates
    unique_videos = {}
    for video in all_videos:
        vid_id = video.get('video_id')
        if vid_id and vid_id not in unique_videos:
            unique_videos[vid_id] = video

    final_videos = list(unique_videos.values())

    print(f"\n{'='*70}")
    print(f"TIKTOK COLLECTION COMPLETE")
    print(f"{'='*70}")
    print(f"Total collected: {len(all_videos)} videos")
    print(f"After deduplication: {len(final_videos)} unique videos")
    print(f"{'='*70}\n")

    # Save results
    if final_videos:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"outputs/3m_claw_tiktok_alternative_{timestamp}.json"

        with open(output_file, 'w') as f:
            json.dump({
                'total_count': len(final_videos),
                'platform': 'tiktok',
                'method': 'direct_api',
                'collected_at': timestamp,
                'videos': final_videos
            }, f, indent=2)

        print(f"✓ Saved to: {output_file}")
        print(f"  Total videos: {len(final_videos)}")
        print(f"  Total views: {sum(v.get('views', 0) for v in final_videos):,}")

        # Top creators
        creators = {}
        for v in final_videos:
            ch = v.get('channel', 'Unknown')
            if ch:
                creators[ch] = creators.get(ch, 0) + 1

        print(f"\n  Top creators:")
        for ch, count in sorted(creators.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"    @{ch}: {count} videos")
    else:
        print("\n✗ No videos collected")

if __name__ == "__main__":
    main()
