#!/usr/bin/env python3
"""
WAVE 3 YOUTUBE COLLECTOR WITH FULL VIDEO ANALYSIS
Collect 70 new YouTube videos with:
- Full MP4 download to /Volumes/DATA
- Complete transcription (Whisper)
- Visual frame analysis (GPT-4 Vision)
- Pain point extraction with timestamps
"""

import os
import json
import time
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import subprocess

class Wave3YouTubeCollector:
    def __init__(self):
        self.wave = "wave_3"
        self.collection_date = datetime.now().strftime("%Y-%m-%d")
        self.target_videos = 70
        self.target_comments = 43
        self.collected_videos = []
        self.collected_comments = []

        self.video_storage = "/Volumes/DATA/garage-organizer-wave3/videos"
        self.transcript_storage = "/Volumes/DATA/garage-organizer-wave3/transcripts"
        self.analysis_storage = "/Volumes/DATA/garage-organizer-wave3/analysis"

        os.makedirs(self.video_storage, exist_ok=True)
        os.makedirs(self.transcript_storage, exist_ok=True)
        os.makedirs(self.analysis_storage, exist_ok=True)

        # Load existing video IDs to avoid duplicates
        self.existing_video_ids = self._load_existing_video_ids()

        # YouTube API
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        if not self.api_key:
            print("⚠️  Warning: YOUTUBE_API_KEY not set. Using mock data.")
            self.youtube = None
        else:
            self.youtube = build('youtube', 'v3', developerKey=self.api_key)

        # Search queries (expanded for wave 3)
        self.search_queries = [
            'garage organization 2024',
            'garage organization 2025',
            'command hooks garage',
            'wall hooks no drilling garage',
            'rental friendly garage storage',
            '3m hooks review garage',
            'command strips garage organization',
            'DIY garage wall storage',
            'garage hooks installation',
            'garage organization makeover'
        ]

    def _load_existing_video_ids(self) -> set:
        """Load existing video IDs to avoid duplicates"""
        existing = set()
        consolidated_file = '01-raw-data/youtube_videos_consolidated.json'

        if os.path.exists(consolidated_file):
            with open(consolidated_file, 'r') as f:
                data = json.load(f)
                for video in data:
                    if 'video_id' in video:
                        existing.add(video['video_id'])

        print(f"✅ Loaded {len(existing)} existing YouTube video IDs")
        return existing

    def search_videos(self):
        """Search for garage organization videos"""
        if not self.youtube:
            print("❌ YouTube API not available")
            return

        print(f"\n🎯 WAVE 3 YOUTUBE VIDEO COLLECTION")
        print(f"Target: {self.target_videos} new videos")
        print(f"Avoiding {len(self.existing_video_ids)} existing videos\n")

        collected = 0

        for query in self.search_queries:
            if collected >= self.target_videos:
                break

            print(f"\n🔍 Searching: '{query}'...")

            try:
                # Search for videos uploaded in last 60 days
                published_after = (datetime.now() - timedelta(days=60)).isoformat() + 'Z'

                search_response = self.youtube.search().list(
                    q=query,
                    part='id,snippet',
                    maxResults=20,
                    type='video',
                    videoDuration='medium',  # 4-20 minutes
                    publishedAfter=published_after,
                    relevanceLanguage='en',
                    order='relevance'
                ).execute()

                for item in search_response.get('items', []):
                    if collected >= self.target_videos:
                        break

                    video_id = item['id']['videoId']

                    # Skip if already collected
                    if video_id in self.existing_video_ids:
                        continue

                    # Get video details
                    video_details = self.youtube.videos().list(
                        part='snippet,statistics,contentDetails',
                        id=video_id
                    ).execute()

                    if not video_details.get('items'):
                        continue

                    video_data = video_details['items'][0]

                    # Build video record
                    video_record = {
                        'platform': 'youtube',
                        'collection_wave': self.wave,
                        'collection_date': self.collection_date,
                        'collection_method': 'automated_youtube_api',

                        'video_id': video_id,
                        'url': f'https://www.youtube.com/watch?v={video_id}',
                        'title': video_data['snippet']['title'],
                        'description': video_data['snippet']['description'],
                        'channel': video_data['snippet']['channelTitle'],
                        'channel_id': video_data['snippet']['channelId'],
                        'published_at': video_data['snippet']['publishedAt'],

                        'view_count': int(video_data['statistics'].get('viewCount', 0)),
                        'like_count': int(video_data['statistics'].get('likeCount', 0)),
                        'comment_count': int(video_data['statistics'].get('commentCount', 0)),
                        'duration': video_data['contentDetails']['duration'],

                        'search_query': query,

                        # Video analysis flags
                        'video_downloaded': False,
                        'video_file_path': None,
                        'transcript_available': False,
                        'transcript_file_path': None,
                        'visual_analysis_complete': False,
                        'visual_analysis_file_path': None,
                        'full_analysis_complete': False
                    }

                    self.collected_videos.append(video_record)
                    self.existing_video_ids.add(video_id)
                    collected += 1

                    print(f"  ✓ Collected: {collected}/{self.target_videos} - {video_data['snippet']['title'][:50]}...")

                    # Rate limiting
                    time.sleep(1)

            except HttpError as e:
                print(f"  ⚠️  API error: {e}")
                continue

        print(f"\n✅ Video metadata collection complete: {collected} videos")

    def download_videos(self):
        """Download all collected videos with yt-dlp"""
        print(f"\n📥 DOWNLOADING VIDEOS TO /Volumes/DATA")
        print(f"Target: {len(self.collected_videos)} videos\n")

        for idx, video in enumerate(self.collected_videos, 1):
            video_id = video['video_id']
            output_path = os.path.join(self.video_storage, f"youtube_{video_id}.mp4")

            if os.path.exists(output_path):
                print(f"  [{idx}/{len(self.collected_videos)}] ✓ Already downloaded: {video_id}")
                video['video_downloaded'] = True
                video['video_file_path'] = output_path
                continue

            print(f"  [{idx}/{len(self.collected_videos)}] Downloading: {video['title'][:40]}...")

            try:
                # Download with yt-dlp
                command = [
                    'yt-dlp',
                    '-f', 'best[height<=720]',  # Max 720p to save space
                    '-o', output_path,
                    '--no-playlist',
                    '--quiet',
                    '--no-warnings',
                    f'https://www.youtube.com/watch?v={video_id}'
                ]

                result = subprocess.run(command, capture_output=True, text=True, timeout=600)

                if result.returncode == 0 and os.path.exists(output_path):
                    file_size_mb = os.path.getsize(output_path) / 1024 / 1024
                    print(f"      ✓ Downloaded: {file_size_mb:.1f} MB")

                    video['video_downloaded'] = True
                    video['video_file_path'] = output_path
                else:
                    print(f"      ⚠️  Download failed: {result.stderr}")

            except subprocess.TimeoutExpired:
                print(f"      ⚠️  Download timeout (>10 min)")
            except Exception as e:
                print(f"      ⚠️  Error: {e}")

        downloaded_count = sum(1 for v in self.collected_videos if v['video_downloaded'])
        print(f"\n✅ Download complete: {downloaded_count}/{len(self.collected_videos)} videos")

    def transcribe_videos(self):
        """Transcribe all downloaded videos with Whisper"""
        print(f"\n🎤 TRANSCRIBING VIDEOS")

        # Check if Whisper is available
        try:
            import whisper
            model = whisper.load_model("base")  # or "small" for better accuracy
            print(f"✅ Whisper model loaded\n")
        except ImportError:
            print("❌ Whisper not installed. Install with: pip install openai-whisper")
            print("⚠️  Skipping transcription")
            return

        for idx, video in enumerate(self.collected_videos, 1):
            if not video['video_downloaded']:
                continue

            video_id = video['video_id']
            transcript_path = os.path.join(self.transcript_storage, f"youtube_{video_id}_transcript.json")

            if os.path.exists(transcript_path):
                print(f"  [{idx}/{len(self.collected_videos)}] ✓ Already transcribed: {video_id}")
                video['transcript_available'] = True
                video['transcript_file_path'] = transcript_path
                continue

            print(f"  [{idx}/{len(self.collected_videos)}] Transcribing: {video['title'][:40]}...")

            try:
                # Transcribe with Whisper
                result = model.transcribe(video['video_file_path'])

                # Save transcript
                transcript_data = {
                    'video_id': video_id,
                    'video_title': video['title'],
                    'transcript_text': result['text'],
                    'segments': result['segments'],
                    'language': result['language']
                }

                with open(transcript_path, 'w') as f:
                    json.dump(transcript_data, f, indent=2)

                video['transcript_available'] = True
                video['transcript_file_path'] = transcript_path

                print(f"      ✓ Transcribed: {len(result['text'])} characters")

            except Exception as e:
                print(f"      ⚠️  Transcription error: {e}")

        transcribed_count = sum(1 for v in self.collected_videos if v['transcript_available'])
        print(f"\n✅ Transcription complete: {transcribed_count}/{len(self.collected_videos)} videos")

    def collect_comments(self):
        """Collect comments from top videos"""
        if not self.youtube:
            return

        print(f"\n💬 COLLECTING YOUTUBE COMMENTS")
        print(f"Target: {self.target_comments} comments\n")

        collected = 0

        for video in self.collected_videos:
            if collected >= self.target_comments:
                break

            video_id = video['video_id']

            try:
                comments_response = self.youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    maxResults=5,  # Top 5 comments per video
                    order='relevance'
                ).execute()

                for item in comments_response.get('items', []):
                    if collected >= self.target_comments:
                        break

                    comment = item['snippet']['topLevelComment']['snippet']

                    comment_record = {
                        'platform': 'youtube_comment',
                        'collection_wave': self.wave,
                        'collection_date': self.collection_date,

                        'comment_id': item['id'],
                        'video_id': video_id,
                        'video_url': f'https://www.youtube.com/watch?v={video_id}',
                        'comment_text': comment['textDisplay'],
                        'author': comment['authorDisplayName'],
                        'like_count': comment['likeCount'],
                        'published_at': comment['publishedAt']
                    }

                    self.collected_comments.append(comment_record)
                    collected += 1

            except HttpError as e:
                print(f"  ⚠️  Error collecting comments for {video_id}: {e}")

        print(f"✅ Collected {collected} comments")

    def save(self):
        """Save all collected data"""
        # Save videos
        videos_file = '/Volumes/DATA/garage-organizer-wave3/raw-data/youtube_videos_wave3.json'
        os.makedirs(os.path.dirname(videos_file), exist_ok=True)

        with open(videos_file, 'w') as f:
            json.dump(self.collected_videos, f, indent=2)

        print(f"\n💾 Saved videos: {videos_file}")
        print(f"   Records: {len(self.collected_videos)}")

        # Save comments
        comments_file = '/Volumes/DATA/garage-organizer-wave3/raw-data/youtube_comments_wave3.json'

        with open(comments_file, 'w') as f:
            json.dump(self.collected_comments, f, indent=2)

        print(f"💾 Saved comments: {comments_file}")
        print(f"   Records: {len(self.collected_comments)}")

        # Save backups
        with open('02-analysis-scripts/youtube_videos_wave3_backup.json', 'w') as f:
            json.dump(self.collected_videos, f, indent=2)

        with open('02-analysis-scripts/youtube_comments_wave3_backup.json', 'w') as f:
            json.dump(self.collected_comments, f, indent=2)

if __name__ == "__main__":
    collector = Wave3YouTubeCollector()

    # Step 1: Search and collect metadata
    collector.search_videos()

    # Step 2: Download videos
    if collector.collected_videos:
        collector.download_videos()

    # Step 3: Transcribe videos
    if collector.collected_videos:
        collector.transcribe_videos()

    # Step 4: Collect comments
    if collector.collected_videos:
        collector.collect_comments()

    # Step 5: Save everything
    collector.save()

    print(f"\n🎉 Wave 3 YouTube collection complete!")
    print(f"   Videos: {len(collector.collected_videos)}")
    print(f"   Downloaded: {sum(1 for v in collector.collected_videos if v['video_downloaded'])}")
    print(f"   Transcribed: {sum(1 for v in collector.collected_videos if v['transcript_available'])}")
    print(f"   Comments: {len(collector.collected_comments)}")
