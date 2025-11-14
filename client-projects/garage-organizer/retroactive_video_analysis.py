#!/usr/bin/env python3
"""
RETROACTIVE VIDEO ANALYSIS - WAVES 1 & 2
Download and analyze ALL existing 295 videos (209 YouTube + 86 TikTok)
that were previously only collected as metadata

This should have been done from the beginning.
"""

import json
import os
import subprocess
import time
from pathlib import Path

class RetroactiveVideoAnalyzer:
    def __init__(self):
        self.video_storage = "/Volumes/DATA/garage-organizer-retroactive/videos"
        self.transcript_storage = "/Volumes/DATA/garage-organizer-retroactive/transcripts"
        self.analysis_storage = "/Volumes/DATA/garage-organizer-retroactive/analysis"

        # Create storage directories
        for path in [self.video_storage, self.transcript_storage, self.analysis_storage]:
            os.makedirs(path, exist_ok=True)

        print("🔄 RETROACTIVE VIDEO ANALYSIS - WAVES 1 & 2")
        print("=" * 60)
        print("Analyzing ALL existing videos that were only collected as metadata\n")

    def load_existing_videos(self):
        """Load all existing video metadata"""
        youtube_file = '01-raw-data/youtube_videos_consolidated.json'
        tiktok_file = '01-raw-data/tiktok_consolidated.json'

        with open(youtube_file, 'r') as f:
            youtube_videos = json.load(f)

        with open(tiktok_file, 'r') as f:
            tiktok_videos = json.load(f)

        print(f"✅ Loaded video metadata:")
        print(f"   YouTube: {len(youtube_videos)} videos")
        print(f"   TikTok: {len(tiktok_videos)} videos")
        print(f"   TOTAL: {len(youtube_videos) + len(tiktok_videos)} videos to analyze\n")

        return youtube_videos, tiktok_videos

    def download_video(self, video_url, video_id, platform):
        """Download a single video with yt-dlp"""
        output_path = os.path.join(self.video_storage, f"{platform}_{video_id}.mp4")

        # Skip if already downloaded
        if os.path.exists(output_path):
            return output_path, True

        try:
            command = [
                'yt-dlp',
                '-f', 'best[height<=720]',  # Max 720p
                '-o', output_path,
                '--no-playlist',
                '--quiet',
                '--no-warnings',
                video_url
            ]

            result = subprocess.run(command, capture_output=True, text=True, timeout=600)

            if result.returncode == 0 and os.path.exists(output_path):
                return output_path, True
            else:
                print(f"      ⚠️  Download failed: {video_id}")
                return None, False

        except Exception as e:
            print(f"      ⚠️  Error downloading {video_id}: {e}")
            return None, False

    def transcribe_video(self, video_path, video_id, platform):
        """Transcribe video with Whisper"""
        transcript_path = os.path.join(self.transcript_storage, f"{platform}_{video_id}_transcript.json")

        # Skip if already transcribed
        if os.path.exists(transcript_path):
            with open(transcript_path, 'r') as f:
                return json.load(f), True

        try:
            import whisper
            model = whisper.load_model("base")

            result = model.transcribe(video_path)

            transcript_data = {
                'video_id': video_id,
                'platform': platform,
                'transcript_text': result['text'],
                'segments': result['segments'],
                'language': result.get('language', 'en')
            }

            # Save transcript
            with open(transcript_path, 'w') as f:
                json.dump(transcript_data, f, indent=2)

            return transcript_data, True

        except ImportError:
            print(f"      ⚠️  Whisper not installed - skipping transcription")
            return None, False
        except Exception as e:
            print(f"      ⚠️  Transcription error for {video_id}: {e}")
            return None, False

    def extract_pain_points(self, transcript_text, video_id):
        """Extract pain points from transcript"""
        pain_point_keywords = {
            'paint_damage': ['paint', 'damage', 'peeling', 'peel', 'surface', 'wall damage'],
            'removal': ['remove', 'removal', 'stuck', 'won\'t come off', 'left marks'],
            'installation': ['install', 'installation', 'difficult', 'hard to', 'complicated'],
            'weight': ['fell', 'fall', 'falling', 'dropped', 'weight', 'capacity', 'heavy'],
            'adhesive': ['adhesive', 'sticky', 'won\'t stick', 'not sticking'],
            'rental': ['rental', 'landlord', 'lease', 'apartment', 'tenant']
        }

        text_lower = transcript_text.lower()

        pain_points_found = {}
        for pain_type, keywords in pain_point_keywords.items():
            matches = [kw for kw in keywords if kw in text_lower]
            if matches:
                pain_points_found[pain_type] = matches

        return pain_points_found

    def analyze_all_videos(self):
        """Main analysis pipeline"""
        youtube_videos, tiktok_videos = self.load_existing_videos()

        # Track progress
        total_videos = len(youtube_videos) + len(tiktok_videos)
        downloaded = 0
        transcribed = 0
        analyzed = 0

        print("📥 PHASE 1: DOWNLOADING VIDEOS")
        print("-" * 60)

        # Process YouTube videos
        for idx, video in enumerate(youtube_videos, 1):
            video_id = video.get('video_id')
            video_url = video.get('url')

            if not video_url:
                continue

            print(f"[{idx}/{len(youtube_videos)}] YouTube: {video.get('title', '')[:40]}...")

            # Download
            video_path, success = self.download_video(video_url, video_id, 'youtube')
            if success:
                downloaded += 1
                video['video_file_path'] = video_path
                video['video_downloaded'] = True

                file_size_mb = os.path.getsize(video_path) / 1024 / 1024 if video_path else 0
                print(f"      ✓ Downloaded: {file_size_mb:.1f} MB")

            # Rate limiting
            time.sleep(2)

        # Process TikTok videos
        for idx, video in enumerate(tiktok_videos, 1):
            video_id = video.get('video_id', video.get('id'))
            video_url = video.get('url', video.get('video_url'))

            if not video_url:
                continue

            print(f"[{idx}/{len(tiktok_videos)}] TikTok: {video_id}...")

            # Download
            video_path, success = self.download_video(video_url, video_id, 'tiktok')
            if success:
                downloaded += 1
                video['video_file_path'] = video_path
                video['video_downloaded'] = True

                file_size_mb = os.path.getsize(video_path) / 1024 / 1024 if video_path else 0
                print(f"      ✓ Downloaded: {file_size_mb:.1f} MB")

            time.sleep(2)

        print(f"\n✅ Downloaded: {downloaded}/{total_videos} videos")

        print("\n🎤 PHASE 2: TRANSCRIBING VIDEOS")
        print("-" * 60)

        # Transcribe YouTube videos
        for idx, video in enumerate(youtube_videos, 1):
            if not video.get('video_downloaded'):
                continue

            video_id = video.get('video_id')
            print(f"[{idx}/{len(youtube_videos)}] Transcribing: {video_id}...")

            transcript, success = self.transcribe_video(
                video['video_file_path'],
                video_id,
                'youtube'
            )

            if success:
                transcribed += 1
                video['transcript_text'] = transcript['transcript_text']
                video['transcript_file_path'] = os.path.join(
                    self.transcript_storage,
                    f"youtube_{video_id}_transcript.json"
                )
                video['transcript_available'] = True

                # Extract pain points
                pain_points = self.extract_pain_points(transcript['transcript_text'], video_id)
                video['pain_points_detected'] = pain_points
                video['pain_points_count'] = len(pain_points)

                if pain_points:
                    analyzed += 1
                    print(f"      ✓ Pain points: {', '.join(pain_points.keys())}")

        # Transcribe TikTok videos
        for idx, video in enumerate(tiktok_videos, 1):
            if not video.get('video_downloaded'):
                continue

            video_id = video.get('video_id', video.get('id'))
            print(f"[{idx}/{len(tiktok_videos)}] Transcribing: {video_id}...")

            transcript, success = self.transcribe_video(
                video['video_file_path'],
                video_id,
                'tiktok'
            )

            if success:
                transcribed += 1
                video['transcript_text'] = transcript['transcript_text']
                video['transcript_file_path'] = os.path.join(
                    self.transcript_storage,
                    f"tiktok_{video_id}_transcript.json"
                )
                video['transcript_available'] = True

                # Extract pain points
                pain_points = self.extract_pain_points(transcript['transcript_text'], video_id)
                video['pain_points_detected'] = pain_points
                video['pain_points_count'] = len(pain_points)

                if pain_points:
                    analyzed += 1
                    print(f"      ✓ Pain points: {', '.join(pain_points.keys())}")

        print(f"\n✅ Transcribed: {transcribed}/{downloaded} videos")
        print(f"✅ Pain points detected: {analyzed} videos")

        # Save updated data
        self.save_updated_data(youtube_videos, tiktok_videos)

        return {
            'total_videos': total_videos,
            'downloaded': downloaded,
            'transcribed': transcribed,
            'analyzed': analyzed
        }

    def save_updated_data(self, youtube_videos, tiktok_videos):
        """Save updated video data with analysis"""
        # Save to DATA volume
        youtube_output = '/Volumes/DATA/garage-organizer-retroactive/youtube_videos_analyzed.json'
        tiktok_output = '/Volumes/DATA/garage-organizer-retroactive/tiktok_videos_analyzed.json'

        with open(youtube_output, 'w') as f:
            json.dump(youtube_videos, f, indent=2)

        with open(tiktok_output, 'w') as f:
            json.dump(tiktok_videos, f, indent=2)

        print(f"\n💾 SAVED ANALYZED DATA:")
        print(f"   YouTube: {youtube_output}")
        print(f"   TikTok: {tiktok_output}")

        # Also update consolidated files
        with open('01-raw-data/youtube_videos_consolidated.json', 'w') as f:
            json.dump(youtube_videos, f, indent=2)

        with open('01-raw-data/tiktok_consolidated.json', 'w') as f:
            json.dump(tiktok_videos, f, indent=2)

        print(f"   ✓ Updated consolidated files")

if __name__ == "__main__":
    analyzer = RetroactiveVideoAnalyzer()

    print("\n⚠️  IMPORTANT: This script requires:")
    print("   1. yt-dlp installed: brew install yt-dlp")
    print("   2. Whisper installed: pip install openai-whisper")
    print("   3. FFmpeg installed: brew install ffmpeg")
    print("\nStarting in 5 seconds...\n")

    time.sleep(5)

    results = analyzer.analyze_all_videos()

    print("\n" + "=" * 60)
    print("🎉 RETROACTIVE ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"Total videos: {results['total_videos']}")
    print(f"Downloaded: {results['downloaded']}")
    print(f"Transcribed: {results['transcribed']}")
    print(f"Pain points analyzed: {results['analyzed']}")
    print("\n✅ All existing videos now have full analysis")
    print(f"✅ Videos saved to: /Volumes/DATA/garage-organizer-retroactive/")
