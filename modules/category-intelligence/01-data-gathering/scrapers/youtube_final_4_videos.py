#!/usr/bin/env python3
"""
Final push: Find 4 more authentic 3M Claw videos with very specific queries
"""

import requests
import json
import re
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "social_videos"

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

def scrape_youtube_search(query, max_results=20):
    """Scrape YouTube search results"""
    print(f"\n🔍 '{query}'")

    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        data = extract_youtube_data(response.text)
        if not data:
            return []

        videos = []
        contents = data.get('contents', {}).get('twoColumnSearchResultsRenderer', {}).get('primaryContents', {}).get('sectionListRenderer', {}).get('contents', [])

        for content in contents:
            for item in content.get('itemSectionRenderer', {}).get('contents', []):
                video_renderer = item.get('videoRenderer', {})
                if not video_renderer:
                    continue

                video_id = video_renderer.get('videoId')
                if not video_id:
                    continue

                title = video_renderer.get('title', {}).get('runs', [{}])[0].get('text', '')

                # STRICT FILTER: Only 3M Claw explicitly
                if not ('3m' in title.lower() and 'claw' in title.lower()):
                    continue

                view_text = video_renderer.get('viewCountText', {})
                if isinstance(view_text, dict):
                    view_text = view_text.get('simpleText', '')

                videos.append({
                    'video_id': video_id,
                    'url': f'https://www.youtube.com/watch?v={video_id}',
                    'title': title,
                    'channel': video_renderer.get('ownerText', {}).get('runs', [{}])[0].get('text', ''),
                    'views': view_text,
                    'length': video_renderer.get('lengthText', {}).get('simpleText', ''),
                    'published': video_renderer.get('publishedTimeText', {}).get('simpleText', ''),
                    'search_query': query,
                    'platform': 'YouTube',
                    'scraped_at': datetime.now().isoformat()
                })

                if len(videos) >= max_results:
                    break

        print(f"   Found {len(videos)} 3M Claw videos")
        return videos

    except Exception as e:
        print(f"   Error: {e}")
        return []

print("=" * 80)
print("FINAL PUSH: 4 MORE 3M CLAW VIDEOS")
print("=" * 80)

# Very specific queries we haven't tried yet
new_queries = [
    "3M Claw 45 lb",
    "3M Claw 25 lb",
    "3M Claw 15 lb",
    "3M Claw spot marker",
    "3M Claw damage test",
    "3M Claw removal",
    "3M Claw variety pack",
    "3M Claw lightweight",
    "hanging mirror 3M Claw",
    "3M Claw shelf"
]

all_new_videos = []

for query in new_queries:
    videos = scrape_youtube_search(query, max_results=10)
    all_new_videos.extend(videos)

# Load existing honest dataset to check for duplicates
honest_file = max(DATA_DIR.glob("youtube_3m_claw_HONEST_VERIFIED_*.json"))
with open(honest_file, 'r') as f:
    existing_data = json.load(f)

existing_ids = {v.get('video_id') for v in existing_data['videos'] if v.get('video_id')}

# Filter out duplicates
new_unique = [v for v in all_new_videos if v['video_id'] not in existing_ids]

# Deduplicate within new videos
unique_dict = {v['video_id']: v for v in new_unique}
new_unique = list(unique_dict.values())

print("\n" + "=" * 80)
print(f"New unique 3M Claw videos found: {len(new_unique)}")
print("=" * 80)

if new_unique:
    for i, video in enumerate(new_unique[:10], 1):
        print(f"\n{i}. {video['title']}")
        print(f"   Channel: {video['channel']}")
        print(f"   Views: {video['views']}")

# Merge with existing
all_videos = existing_data['videos'] + new_unique

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
final_file = DATA_DIR / f"youtube_3m_claw_FINAL_{timestamp}.json"

with open(final_file, 'w') as f:
    json.dump({
        'platform': 'YouTube',
        'brand': '3M Claw',
        'finalized_at': datetime.now().isoformat(),
        'video_count': len(all_videos),
        'previous_count': len(existing_data['videos']),
        'new_videos_added': len(new_unique),
        'videos': all_videos
    }, f, indent=2)

print(f"\n💾 Saved: {final_file.name}")
print(f"\n🎯 FINAL COUNT: {len(all_videos)} authentic 3M Claw videos")

if len(all_videos) >= 50:
    print(f"   ✓ TARGET ACHIEVED: {len(all_videos)}/50 videos")
    print(f"   Surplus: +{len(all_videos) - 50} videos")
else:
    print(f"   STATUS: {len(all_videos)}/50 videos")
    print(f"   Still need: {50 - len(all_videos)} more videos")
