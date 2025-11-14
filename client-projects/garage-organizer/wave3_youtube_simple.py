#!/usr/bin/env python3
"""
Wave 3 YouTube Collector - Using yt-dlp (no API key needed)
Collect 70 new videos with full download and transcription
"""

import json
import os
import subprocess
from datetime import datetime
import time

class SimpleYouTubeCollector:
    def __init__(self):
        self.wave = "wave_3"
        self.collection_date = datetime.now().strftime("%Y-%m-%d")
        self.target_new_videos = 70
        self.collected_videos = []

        # Load existing URLs to avoid duplicates
        self.existing_urls = set()
        consolidated_path = '/Users/anderson115/00-interlink/12-work/3m-lighting-project/client-projects/garage-organizer/01-raw-data/youtube_videos_consolidated.json'
        if os.path.exists(consolidated_path):
            with open(consolidated_path, 'r') as f:
                data = json.load(f)
                for video in data:
                    if 'video_url' in video:
                        self.existing_urls.add(video['video_url'])
                    elif 'url' in video:
                        self.existing_urls.add(video['url'])

        print(f"✅ Loaded {len(self.existing_urls)} existing YouTube URLs")

        # Storage paths
        self.video_storage = '/Volumes/DATA/garage-organizer-wave3/videos'
        self.output_dir = '/Volumes/DATA/garage-organizer-wave3/raw-data'
        os.makedirs(self.video_storage, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

        self.search_queries = [
            'command hooks garage organization',
            '3m hooks garage',
            'adhesive hooks garage storage',
            'damage free garage hooks',
            'wall hooks garage DIY',
            'rental friendly garage organization',
            'command strips heavy duty garage',
            'garage organization without drilling',
            'removable hooks garage',
            'temporary garage storage hooks'
        ]

    def search_and_collect(self):
        print(f"\n🎯 WAVE 3 YOUTUBE COLLECTION")
        print(f"Target: {self.target_new_videos} new videos\n")

        collected = 0

        for query in self.search_queries:
            if collected >= self.target_new_videos:
                break

            print(f"\n🔍 Searching: {query}")

            try:
                # Use yt-dlp to search and get metadata
                cmd = [
                    'yt-dlp',
                    f'ytsearch20:{query}',  # Search for 20 results per query
                    '--dump-json',
                    '--skip-download',
                    '--no-warnings',
                    '--quiet'
                ]

                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

                if result.returncode != 0:
                    print(f"  ⚠️  Search error")
                    continue

                # Parse JSON lines
                for line in result.stdout.strip().split('\n'):
                    if not line:
                        continue

                    if collected >= self.target_new_videos:
                        break

                    try:
                        video_data = json.loads(line)
                        video_url = video_data.get('webpage_url', '')

                        # Skip if already collected
                        if video_url in self.existing_urls:
                            continue

                        # Skip shorts and very short videos
                        duration = video_data.get('duration', 0)
                        if duration < 60 or duration > 3600:  # 1 min to 1 hour
                            continue

                        # Skip if view count is too low
                        view_count = video_data.get('view_count', 0)
                        if view_count < 100:
                            continue

                        # Download video
                        video_id = video_data.get('id')
                        video_path = os.path.join(self.video_storage, f"{video_id}.mp4")

                        print(f"  📥 Downloading: {video_data.get('title', '')[:50]}...")

                        download_cmd = [
                            'yt-dlp',
                            '-f', 'best[height<=720]',  # Max 720p to save space
                            '-o', video_path,
                            '--no-playlist',
                            '--quiet',
                            '--no-warnings',
                            video_url
                        ]

                        download_result = subprocess.run(download_cmd, capture_output=True, timeout=600)

                        if download_result.returncode != 0:
                            print(f"    ⚠️  Download failed")
                            continue

                        # Build record
                        record = {
                            'platform': 'youtube',
                            'collection_wave': self.wave,
                            'collection_date': self.collection_date,
                            'collection_method': 'ytdlp_search',

                            'video_id': video_id,
                            'video_url': video_url,
                            'title': video_data.get('title', ''),
                            'description': video_data.get('description', ''),
                            'channel': video_data.get('channel', ''),
                            'channel_id': video_data.get('channel_id', ''),
                            'upload_date': video_data.get('upload_date', ''),
                            'duration': duration,
                            'view_count': view_count,
                            'like_count': video_data.get('like_count', 0),
                            'comment_count': video_data.get('comment_count', 0),

                            'video_file_path': video_path,
                            'search_query': query
                        }

                        self.collected_videos.append(record)
                        self.existing_urls.add(video_url)
                        collected += 1

                        print(f"    ✓ {collected}/{self.target_new_videos}")

                        # Rate limit
                        time.sleep(2)

                    except json.JSONDecodeError:
                        continue
                    except Exception as e:
                        print(f"    ⚠️  Error: {e}")
                        continue

            except Exception as e:
                print(f"  ⚠️  Query error: {e}")
                continue

        print(f"\n✅ Collection complete: {collected} new videos")
        return self.collected_videos

    def save(self):
        output_file = os.path.join(self.output_dir, 'youtube_wave3.json')

        with open(output_file, 'w') as f:
            json.dump(self.collected_videos, f, indent=2)

        print(f"\n💾 Saved to: {output_file}")
        print(f"   Records: {len(self.collected_videos)}")
        print(f"   Videos downloaded to: {self.video_storage}")

if __name__ == "__main__":
    collector = SimpleYouTubeCollector()
    videos = collector.search_and_collect()

    if videos:
        collector.save()
        print(f"\n🎉 Wave 3 YouTube complete: {len(videos)} videos")
        print(f"\n⏭️  Next step: Run transcription with Whisper")
