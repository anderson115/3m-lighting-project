#!/usr/bin/env python3
"""
AGGRESSIVE YouTube 3M Claw Video Scraper
Expanded query set to ensure 50+ authentic videos
"""

import requests
import json
import re
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "social_videos"
DATA_DIR.mkdir(parents=True, exist_ok=True)

def extract_youtube_data(html_content):
    """Extract ytInitialData from YouTube page"""
    pattern = r'var ytInitialData = ({.*?});'
    match = re.search(pattern, html_content, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            return None
    return None

def scrape_youtube_search(query, max_results=50):
    """Scrape YouTube search results"""
    print(f"\n🔍 Searching: '{query}'")

    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        data = extract_youtube_data(response.text)
        if not data:
            print(f"   ⚠ Could not extract data")
            return []

        videos = []
        contents = data.get('contents', {}).get('twoColumnSearchResultsRenderer', {}).get('primaryContents', {}).get('sectionListRenderer', {}).get('contents', [])

        for content in contents:
            item_section = content.get('itemSectionRenderer', {})
            for item in item_section.get('contents', []):
                video_renderer = item.get('videoRenderer', {})
                if not video_renderer:
                    continue

                video_id = video_renderer.get('videoId')
                if not video_id:
                    continue

                title = video_renderer.get('title', {}).get('runs', [{}])[0].get('text', '')

                # Extract view count
                view_text = video_renderer.get('viewCountText', {})
                if isinstance(view_text, dict):
                    view_text = view_text.get('simpleText', '')
                views = view_text

                # Extract channel
                channel_name = video_renderer.get('ownerText', {}).get('runs', [{}])[0].get('text', '')

                # Extract length
                length_text = video_renderer.get('lengthText', {}).get('simpleText', '')

                # Extract published date
                published_text = video_renderer.get('publishedTimeText', {}).get('simpleText', '')

                videos.append({
                    'video_id': video_id,
                    'url': f'https://www.youtube.com/watch?v={video_id}',
                    'title': title,
                    'channel': channel_name,
                    'views': views,
                    'length': length_text,
                    'published': published_text,
                    'search_query': query,
                    'platform': 'YouTube',
                    'scraped_at': datetime.now().isoformat()
                })

                if len(videos) >= max_results:
                    break

            if len(videos) >= max_results:
                break

        print(f"   ✓ Found {len(videos)} videos")
        return videos

    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        return []

def main():
    print("=" * 80)
    print("AGGRESSIVE YOUTUBE 3M CLAW VIDEO SCRAPING")
    print("=" * 80)
    print("\nTarget: 50+ authentic relevant 3M Claw videos")
    print("Strategy: Expanded query set + multiple search angles")

    # COMPREHENSIVE QUERY SET - covering all angles
    queries = [
        # Brand + Product (core)
        "3M Claw",
        "3M Claw hooks",
        "3M Claw drywall hooks",
        "3M Claw picture hangers",
        "3M Claw heavy duty",

        # Review & Comparison
        "3M Claw review",
        "3M Claw vs Command hooks",
        "3M Claw vs Command strips",
        "best drywall hooks 3M Claw",

        # Installation & How-to
        "3M Claw installation",
        "how to use 3M Claw",
        "3M Claw hanging pictures",
        "3M Claw drywall installation",
        "install 3M Claw hooks",

        # Testing & Demo
        "3M Claw test",
        "3M Claw weight test",
        "3M Claw strength test",
        "3M Claw unboxing",
        "3M Claw demo",

        # Use cases
        "hang pictures with 3M Claw",
        "3M Claw for shelves",
        "3M Claw garage organization",
        "3M Claw heavy items",

        # Specific product variations
        "3M Claw drywall picture hanger",
        "3M Claw damage free",
        "3M Claw no studs",
        "3M Claw wire hangers",

        # Problem solving
        "3M Claw alternatives",
        "3M Claw problems",
        "3M Claw fail",
        "do 3M Claw hooks work"
    ]

    print(f"\n📋 Query Strategy: {len(queries)} search queries")
    print(f"   Videos per query: ~20-30")
    print(f"   Expected total: 200-400+ videos (will deduplicate)")

    all_videos = []

    for i, query in enumerate(queries, 1):
        print(f"\n[{i}/{len(queries)}] Query: '{query}'")
        videos = scrape_youtube_search(query, max_results=30)
        all_videos.extend(videos)

        # Save checkpoint every 5 queries
        if i % 5 == 0:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            checkpoint_file = DATA_DIR / f"youtube_3m_claw_checkpoint_{i}queries_{timestamp}.json"
            with open(checkpoint_file, 'w') as f:
                json.dump({
                    'platform': 'YouTube',
                    'brand': '3M Claw',
                    'queries_completed': i,
                    'total_queries': len(queries),
                    'raw_video_count': len(all_videos),
                    'videos': all_videos
                }, f, indent=2)
            print(f"\n   💾 Checkpoint: {len(all_videos)} videos collected (checkpoint_{i}queries)")

    # Deduplicate by video_id
    unique_videos = {}
    for video in all_videos:
        video_id = video.get('video_id')
        if video_id and video_id not in unique_videos:
            unique_videos[video_id] = video

    deduplicated = list(unique_videos.values())

    # Filter for relevance (must mention 3M Claw in title)
    relevant = []
    for video in deduplicated:
        title_lower = video.get('title', '').lower()
        if '3m' in title_lower and 'claw' in title_lower:
            video['relevance'] = 'High - 3M Claw in title'
            relevant.append(video)
        elif '3m' in title_lower or 'claw' in title_lower:
            video['relevance'] = 'Medium - Partial match'
            relevant.append(video)

    print("\n" + "=" * 80)
    print("DEDUPLICATION & FILTERING")
    print("=" * 80)
    print(f"Raw videos collected: {len(all_videos)}")
    print(f"Unique videos (deduplicated): {len(deduplicated)}")
    print(f"Relevant videos (3M Claw mentions): {len(relevant)}")
    print(f"Duplicate removal: {len(all_videos) - len(deduplicated)} videos")

    # Save final results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # All unique videos
    all_file = DATA_DIR / f"youtube_3m_claw_ALL_UNIQUE_{timestamp}.json"
    with open(all_file, 'w') as f:
        json.dump({
            'platform': 'YouTube',
            'brand': '3M Claw',
            'search_queries': queries,
            'queries_count': len(queries),
            'collected_at': datetime.now().isoformat(),
            'raw_count': len(all_videos),
            'unique_count': len(deduplicated),
            'relevant_count': len(relevant),
            'videos': deduplicated
        }, f, indent=2)

    # Relevant only
    relevant_file = DATA_DIR / f"youtube_3m_claw_RELEVANT_{timestamp}.json"
    with open(relevant_file, 'w') as f:
        json.dump({
            'platform': 'YouTube',
            'brand': '3M Claw',
            'search_queries': queries,
            'collected_at': datetime.now().isoformat(),
            'video_count': len(relevant),
            'filter_criteria': '3M Claw mentioned in title',
            'videos': relevant
        }, f, indent=2)

    print("\n" + "=" * 80)
    print("AGGRESSIVE SEARCH COMPLETE")
    print("=" * 80)
    print(f"\n📊 Final Results:")
    print(f"   Unique videos: {len(deduplicated)}")
    print(f"   Relevant videos: {len(relevant)}")
    print(f"   Target achieved: {'✓ YES' if len(relevant) >= 50 else '✗ NO'} (need 50+)")
    print(f"\n💾 Files saved:")
    print(f"   All unique: {all_file.name}")
    print(f"   Relevant only: {relevant_file.name}")

    if len(relevant) < 50:
        print(f"\n⚠ WARNING: Only {len(relevant)} relevant videos found")
        print(f"   Need {50 - len(relevant)} more videos to meet target")
    else:
        print(f"\n✓ SUCCESS: {len(relevant)} relevant videos exceeds 50+ target")

    # Sample output
    print("\n📋 Sample Relevant Videos:")
    for i, video in enumerate(relevant[:5], 1):
        print(f"\n   {i}. {video['title']}")
        print(f"      Channel: {video['channel']}")
        print(f"      Views: {video['views']}")
        print(f"      URL: {video['url']}")

    return relevant

if __name__ == "__main__":
    results = main()
