#!/usr/bin/env python3
"""
YouTube Video Download Pipeline
Downloads videos from discovered creators for multi-modal analysis

Input: data/creators/creator_database.json
Output: data/videos/{video_id}/video.mp4 + metadata.json
"""
import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment
project_root = Path(__file__).parent.parent
load_dotenv(project_root / '.env')

# Download configuration
MAX_VIDEOS_PER_CREATOR = 2  # Top 2 recent videos per creator
MAX_TOTAL_VIDEOS = 30       # Total video limit
VIDEO_DURATION_MIN = 240    # 4 minutes minimum
VIDEO_DURATION_MAX = 1200   # 20 minutes maximum
VIDEO_QUALITY = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'

class VideoDownloader:
    """YouTube video downloader using yt-dlp"""

    def __init__(self, creator_db_path: Path, output_dir: Path):
        self.creator_db = self.load_creator_database(creator_db_path)
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.downloaded_count = 0
        self.skipped_count = 0
        self.failed_count = 0

    def load_creator_database(self, db_path: Path) -> Dict:
        """Load creator database from JSON"""
        if not db_path.exists():
            print(f"❌ Creator database not found: {db_path}")
            print("   Run: python scripts/creator_discovery.py")
            sys.exit(1)

        with open(db_path) as f:
            return json.load(f)

    def get_video_info(self, video_id: str) -> Optional[Dict]:
        """
        Fetch video metadata using yt-dlp

        Returns video info dict or None if failed
        """
        try:
            cmd = [
                'yt-dlp',
                '--dump-json',
                '--no-download',
                f'https://www.youtube.com/watch?v={video_id}'
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return None

        except Exception as e:
            print(f"   ⚠️  Failed to get info: {str(e)[:50]}")
            return None

    def should_download(self, video_info: Dict) -> tuple[bool, str]:
        """
        Check if video meets download criteria

        Returns (should_download, reason)
        """
        # Check duration
        duration = video_info.get('duration', 0)
        if duration < VIDEO_DURATION_MIN:
            return False, f"Too short ({duration//60}m)"
        if duration > VIDEO_DURATION_MAX:
            return False, f"Too long ({duration//60}m)"

        # Check if already downloaded
        video_id = video_info['id']
        video_dir = self.output_dir / video_id
        if (video_dir / 'video.mp4').exists():
            return False, "Already downloaded"

        # Check availability
        if video_info.get('is_live', False):
            return False, "Live stream"

        if video_info.get('availability') not in ['public', 'unlisted', None]:
            return False, "Not available"

        return True, "OK"

    def download_video(self, video_id: str, video_info: Dict) -> bool:
        """
        Download video and save metadata

        Returns True if successful
        """
        video_dir = self.output_dir / video_id
        video_dir.mkdir(parents=True, exist_ok=True)

        video_path = video_dir / 'video.mp4'
        metadata_path = video_dir / 'metadata.json'

        print(f"   📥 Downloading to: {video_dir.name}/")

        try:
            # Download video
            cmd = [
                'yt-dlp',
                '-f', VIDEO_QUALITY,
                '--merge-output-format', 'mp4',
                '-o', str(video_path),
                '--no-playlist',
                '--quiet',
                '--progress',
                f'https://www.youtube.com/watch?v={video_id}'
            ]

            result = subprocess.run(
                cmd,
                timeout=600,  # 10 minute timeout
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                print(f"   ❌ Download failed: {result.stderr[:100]}")
                return False

            # Verify file exists
            if not video_path.exists():
                print(f"   ❌ Video file not created")
                return False

            file_size_mb = video_path.stat().st_size / (1024 * 1024)
            print(f"   ✅ Downloaded: {file_size_mb:.1f} MB")

            # Save metadata
            metadata = {
                'video_id': video_id,
                'title': video_info['title'],
                'channel': video_info['channel'],
                'channel_id': video_info['channel_id'],
                'duration': video_info['duration'],
                'view_count': video_info.get('view_count', 0),
                'like_count': video_info.get('like_count', 0),
                'comment_count': video_info.get('comment_count', 0),
                'upload_date': video_info.get('upload_date'),
                'description': video_info.get('description', ''),
                'tags': video_info.get('tags', []),
                'categories': video_info.get('categories', []),
                'thumbnail': video_info.get('thumbnail'),
                'file_size_mb': file_size_mb,
                'downloaded_at': datetime.now().isoformat(),
                'video_path': str(video_path),
                'url': f"https://www.youtube.com/watch?v={video_id}"
            }

            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)

            return True

        except subprocess.TimeoutExpired:
            print(f"   ❌ Download timeout (>10min)")
            return False
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:100]}")
            return False

    def download_from_creators(self) -> List[Dict]:
        """
        Download videos from all creators in database

        Returns list of downloaded video metadata
        """
        print("\n" + "=" * 60)
        print("📥 YOUTUBE VIDEO DOWNLOAD PIPELINE")
        print("=" * 60)

        creators = self.creator_db['creators']
        print(f"Creators: {len(creators)}")
        print(f"Target: {MAX_VIDEOS_PER_CREATOR} videos/creator, max {MAX_TOTAL_VIDEOS} total")
        print(f"Duration: {VIDEO_DURATION_MIN//60}-{VIDEO_DURATION_MAX//60} minutes")
        print(f"Quality: {VIDEO_QUALITY}")

        downloaded_videos = []

        for i, creator in enumerate(creators, 1):
            if self.downloaded_count >= MAX_TOTAL_VIDEOS:
                print(f"\n⚠️  Reached max videos ({MAX_TOTAL_VIDEOS}) - stopping")
                break

            creator_name = creator['title']
            print(f"\n[{i}/{len(creators)}] {creator_name}")

            # Get recent videos
            recent_videos = creator.get('recent_videos', [])[:MAX_VIDEOS_PER_CREATOR]

            for j, video in enumerate(recent_videos, 1):
                if self.downloaded_count >= MAX_TOTAL_VIDEOS:
                    break

                video_id = video['video_id']
                video_title = video['title'][:50]

                print(f"   [{j}/{len(recent_videos)}] {video_title}...")

                # Get full video info
                video_info = self.get_video_info(video_id)
                if not video_info:
                    print(f"   ⚠️  Could not fetch info")
                    self.failed_count += 1
                    continue

                # Check if should download
                should_dl, reason = self.should_download(video_info)
                if not should_dl:
                    print(f"   ⏭️  Skipped: {reason}")
                    self.skipped_count += 1
                    continue

                # Download
                if self.download_video(video_id, video_info):
                    self.downloaded_count += 1
                    downloaded_videos.append({
                        'video_id': video_id,
                        'creator': creator_name,
                        'title': video_title
                    })
                else:
                    self.failed_count += 1

        return downloaded_videos

    def save_manifest(self, downloaded_videos: List[Dict]):
        """Save download manifest"""
        manifest_path = self.output_dir / 'download_manifest.json'

        manifest = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_downloaded': self.downloaded_count,
                'total_skipped': self.skipped_count,
                'total_failed': self.failed_count,
                'config': {
                    'max_videos_per_creator': MAX_VIDEOS_PER_CREATOR,
                    'max_total_videos': MAX_TOTAL_VIDEOS,
                    'duration_range': f"{VIDEO_DURATION_MIN//60}-{VIDEO_DURATION_MAX//60} min",
                    'quality': VIDEO_QUALITY
                }
            },
            'videos': downloaded_videos
        }

        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        print(f"\n💾 Manifest saved: {manifest_path}")

    def generate_summary(self):
        """Print download summary"""
        print("\n" + "=" * 60)
        print("📊 DOWNLOAD SUMMARY")
        print("=" * 60)
        print(f"✅ Downloaded: {self.downloaded_count}")
        print(f"⏭️  Skipped: {self.skipped_count}")
        print(f"❌ Failed: {self.failed_count}")

        # Calculate storage
        total_size_mb = 0
        for video_dir in self.output_dir.iterdir():
            if video_dir.is_dir():
                video_file = video_dir / 'video.mp4'
                if video_file.exists():
                    total_size_mb += video_file.stat().st_size / (1024 * 1024)

        print(f"💾 Total size: {total_size_mb:.1f} MB ({total_size_mb/1024:.2f} GB)")
        print(f"📂 Location: {self.output_dir}")


def check_dependencies():
    """Verify yt-dlp is installed"""
    try:
        result = subprocess.run(
            ['yt-dlp', '--version'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ yt-dlp version: {result.stdout.strip()}")
            return True
        else:
            print("❌ yt-dlp not working properly")
            return False
    except FileNotFoundError:
        print("❌ yt-dlp not installed")
        print("   Install: pip install yt-dlp")
        return False


def main():
    """Main entry point"""

    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)

    # Paths
    creator_db_path = project_root / 'data' / 'creators' / 'creator_database.json'
    output_dir = project_root / 'data' / 'videos'

    # Run downloader
    downloader = VideoDownloader(creator_db_path, output_dir)
    downloaded_videos = downloader.download_from_creators()

    # Save results
    if downloaded_videos:
        downloader.save_manifest(downloaded_videos)
        downloader.generate_summary()
        print(f"\n✅ Video download complete!")
        print(f"   Next: python scripts/multimodal_analyzer.py")
    else:
        print("\n⚠️  No videos downloaded")
        sys.exit(1)


if __name__ == "__main__":
    main()
