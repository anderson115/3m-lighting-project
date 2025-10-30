#!/usr/bin/env python3
"""
Step 2: Download Videos

Downloads TikTok videos using yt-dlp from search results.
Preserves metadata and organizes into structured folders.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class VideoDownloader:
    """Download videos using yt-dlp"""

    def __init__(self, search_results_path: Path, output_dir: Path):
        self.search_results_path = search_results_path
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load search results
        with open(search_results_path) as f:
            data = json.load(f)
            self.videos = data['videos']
            self.metadata = data['metadata']

        print(f"Loaded {len(self.videos)} videos from search results")

    def download_video(self, video: Dict) -> bool:
        """
        Download single video using yt-dlp

        Args:
            video: Video metadata dict from search results

        Returns:
            True if successful, False otherwise
        """
        video_id = video.get('id')
        if not video_id:
            print("  Error: No video ID")
            return False

        # Create video directory
        video_dir = self.output_dir / 'videos' / video_id
        video_dir.mkdir(parents=True, exist_ok=True)

        # Check if already downloaded
        video_file = video_dir / 'video.mp4'
        if video_file.exists():
            print(f"  Already downloaded: {video_id}")
            return True

        # Get video URL
        video_url = video.get('webVideoUrl') or video.get('shareUrl')
        if not video_url:
            print(f"  Error: No video URL for {video_id}")
            return False

        print(f"  Downloading: {video_id}")
        print(f"    URL: {video_url}")

        # yt-dlp command
        cmd = [
            'yt-dlp',
            '--quiet',
            '--no-warnings',
            '--output', str(video_file),
            '--format', 'best',
            '--no-playlist',
            video_url
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=120,
                check=True
            )

            if video_file.exists():
                size_mb = video_file.stat().st_size / (1024 * 1024)
                print(f"    ✅ Downloaded: {size_mb:.1f} MB")

                # Save metadata
                self._save_video_metadata(video, video_dir)
                return True
            else:
                print(f"    ❌ Download failed: File not created")
                return False

        except subprocess.TimeoutExpired:
            print(f"    ❌ Timeout downloading video")
            return False
        except subprocess.CalledProcessError as e:
            print(f"    ❌ Error: {e.stderr.decode()[:100] if e.stderr else 'Unknown'}")
            return False
        except Exception as e:
            print(f"    ❌ Error: {str(e)[:100]}")
            return False

    def _save_video_metadata(self, video: Dict, video_dir: Path):
        """Save video metadata to JSON"""
        metadata_file = video_dir / 'metadata.json'

        # Extract key metadata
        metadata = {
            'video_id': video.get('id'),
            'author': video.get('author', {}).get('uniqueId'),
            'author_name': video.get('author', {}).get('nickname'),
            'description': video.get('desc'),
            'created_time': video.get('createTime'),
            'duration': video.get('video', {}).get('duration'),
            'stats': {
                'views': video.get('stats', {}).get('playCount', 0),
                'likes': video.get('stats', {}).get('diggCount', 0),
                'comments': video.get('stats', {}).get('commentCount', 0),
                'shares': video.get('stats', {}).get('shareCount', 0),
            },
            'music': video.get('music', {}).get('title'),
            'hashtags': [tag.get('name') for tag in video.get('textExtra', []) if tag.get('hashtagName')],
            'url': video.get('webVideoUrl'),
            'download_date': datetime.now().isoformat()
        }

        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)

    def download_all(self) -> Dict:
        """
        Download all videos from search results

        Returns:
            Summary dict with success/fail counts
        """
        print("\n" + "="*60)
        print("Downloading Videos")
        print("="*60)

        success_count = 0
        fail_count = 0
        skip_count = 0

        for i, video in enumerate(self.videos, 1):
            print(f"\n[{i}/{len(self.videos)}]")

            video_id = video.get('id')
            video_dir = self.output_dir / 'videos' / video_id
            video_file = video_dir / 'video.mp4'

            # Check if already downloaded
            if video_file.exists():
                print(f"  Skipping (already downloaded): {video_id}")
                skip_count += 1
                continue

            # Download
            if self.download_video(video):
                success_count += 1
            else:
                fail_count += 1

        # Save summary
        summary = {
            'total_videos': len(self.videos),
            'downloaded': success_count,
            'failed': fail_count,
            'skipped': skip_count,
            'download_date': datetime.now().isoformat()
        }

        summary_file = self.output_dir / 'download_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)

        print("\n" + "="*60)
        print("Download Complete")
        print(f"  Downloaded: {success_count}")
        print(f"  Failed: {fail_count}")
        print(f"  Skipped: {skip_count}")
        print("="*60)

        return summary


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Download TikTok videos')
    parser.add_argument(
        '--search-results',
        type=Path,
        help='Path to search_results.json from step 1'
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Output directory for downloaded videos'
    )

    args = parser.parse_args()

    # Auto-detect search results if not provided
    if not args.search_results:
        # Look for most recent search_results.json
        possible_paths = list(Path('data/processed').glob('*/search_results.json'))
        if not possible_paths:
            print("Error: No search results found. Run 01_search_videos.py first.")
            sys.exit(1)

        # Use most recent
        args.search_results = max(possible_paths, key=lambda p: p.stat().st_mtime)
        print(f"Using search results: {args.search_results}")

    if not args.search_results.exists():
        print(f"Error: Search results not found: {args.search_results}")
        sys.exit(1)

    # Auto-detect output dir
    if not args.output:
        args.output = args.search_results.parent

    # Download
    downloader = VideoDownloader(args.search_results, args.output)
    summary = downloader.download_all()

    if summary['downloaded'] == 0 and summary['skipped'] == 0:
        print("\nWarning: No videos downloaded!")
        sys.exit(1)

    print(f"\nNext step: python scripts/03_transcribe.py")


if __name__ == "__main__":
    main()
