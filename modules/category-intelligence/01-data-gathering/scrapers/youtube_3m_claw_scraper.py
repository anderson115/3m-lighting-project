#!/usr/bin/env python3
"""
YouTube scraper specifically for 3M Claw brand content
Uses simple HTTP requests to YouTube search
"""

import requests
import json
import time
import re
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "social_videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class YouTubeCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        })

    def search_youtube(self, query, max_results=50):
        """Search YouTube and extract video data"""
        print(f"\n🎥 Searching YouTube: {query}")

        search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"

        try:
            response = self.session.get(search_url, timeout=30)
            time.sleep(2)

            if response.status_code != 200:
                print(f"  ❌ Status {response.status_code}")
                return []

            # Extract video data from page
            html = response.text
            videos = []

            # Find ytInitialData JSON
            match = re.search(r'var ytInitialData = ({.+?});', html)
            if match:
                try:
                    data = json.loads(match.group(1))

                    # Navigate to video renderer
                    contents = data.get('contents', {}).get('twoColumnSearchResultsRenderer', {}).get('primaryContents', {}).get('sectionListRenderer', {}).get('contents', [])

                    for section in contents:
                        item_section = section.get('itemSectionRenderer', {})
                        for item in item_section.get('contents', []):
                            video = item.get('videoRenderer', {})
                            if video:
                                video_id = video.get('videoId')
                                title = video.get('title', {}).get('runs', [{}])[0].get('text', '')

                                # View count
                                view_text = video.get('viewCountText', {}).get('simpleText', '')
                                views = self._parse_view_count(view_text)

                                # Duration
                                duration_text = video.get('lengthText', {}).get('simpleText', '')

                                # Channel
                                channel_name = video.get('ownerText', {}).get('runs', [{}])[0].get('text', '')

                                # Published date
                                published_text = video.get('publishedTimeText', {}).get('simpleText', '')

                                # Thumbnail
                                thumbnails = video.get('thumbnail', {}).get('thumbnails', [])
                                thumbnail_url = thumbnails[-1].get('url') if thumbnails else None

                                if video_id and title:
                                    videos.append({
                                        'video_id': video_id,
                                        'title': title,
                                        'url': f'https://www.youtube.com/watch?v={video_id}',
                                        'channel': channel_name,
                                        'views': views,
                                        'view_text': view_text,
                                        'duration': duration_text,
                                        'published': published_text,
                                        'thumbnail': thumbnail_url,
                                        'search_query': query,
                                        'scraped_at': datetime.now().isoformat()
                                    })

                                    if len(videos) >= max_results:
                                        break

                        if len(videos) >= max_results:
                            break

                except json.JSONDecodeError as e:
                    print(f"  ⚠ JSON parse error: {e}")

            print(f"  ✓ Found {len(videos)} videos")
            return videos

        except Exception as e:
            print(f"  ❌ Error: {e}")
            return []

    def _parse_view_count(self, view_text):
        """Parse view count from text like '1.2M views' or '150K views'"""
        if not view_text:
            return None

        try:
            # Remove 'views' and extra spaces
            text = view_text.lower().replace('views', '').replace(',', '').strip()

            if 'k' in text:
                return int(float(text.replace('k', '')) * 1000)
            elif 'm' in text:
                return int(float(text.replace('m', '')) * 1000000)
            elif 'b' in text:
                return int(float(text.replace('b', '')) * 1000000000)
            else:
                return int(''.join(filter(str.isdigit, text)))
        except:
            return None


def main():
    crawler = YouTubeCrawler()

    # 3M Claw specific search queries
    search_queries = [
        "3M Claw hooks",
        "3M Claw drywall hooks",
        "3M Claw review",
        "3M Claw installation",
        "3M Claw vs Command",
        "3M Claw heavy duty",
        "3M Claw garage",
        "3M Claw test",
        "3M Claw unboxing",
        "3M Claw hanging pictures",
        "3M Claw wall hooks",
        "3M Claw strength test"
    ]

    print("=" * 80)
    print("YOUTUBE 3M CLAW VIDEO SCRAPING")
    print("=" * 80)

    all_videos = []

    for query in search_queries:
        videos = crawler.search_youtube(query, max_results=30)
        all_videos.extend(videos)
        time.sleep(3)  # Polite delay

    # Remove duplicates
    unique_videos = {}
    for v in all_videos:
        vid_id = v.get('video_id')
        if vid_id and vid_id not in unique_videos:
            unique_videos[vid_id] = v

    all_videos = list(unique_videos.values())

    # Save results
    output_file = OUTPUT_DIR / f"youtube_3m_claw_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump({
            'platform': 'YouTube',
            'brand': '3M Claw',
            'collected_at': datetime.now().isoformat(),
            'search_queries': search_queries,
            'video_count': len(all_videos),
            'total_views': sum(v.get('views', 0) for v in all_videos if v.get('views')),
            'videos': all_videos
        }, f, indent=2)

    print("\n" + "=" * 80)
    print("YOUTUBE SCRAPING COMPLETE")
    print("=" * 80)
    print(f"Total unique videos: {len(all_videos)}")
    print(f"Total views: {sum(v.get('views', 0) for v in all_videos if v.get('views')):,}")
    print(f"\nSaved to: {output_file}")


if __name__ == "__main__":
    main()
