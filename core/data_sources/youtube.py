"""
YouTube Data Source Module
Handles video search, download, and metadata extraction
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class YouTubeDataSource:
    """YouTube data source with search, download, and metadata extraction"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize YouTube data source

        Args:
            api_key: YouTube API key (defaults to YOUTUBE_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('YOUTUBE_API_KEY')
        if not self.api_key:
            raise ValueError("YouTube API key required (YOUTUBE_API_KEY env var or api_key param)")

        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def search_videos(
        self,
        query: str,
        max_results: int = 50,
        order: str = 'relevance',
        published_after: Optional[str] = None
    ) -> List[Dict]:
        """
        Search YouTube videos by keyword

        Args:
            query: Search query string
            max_results: Maximum number of results (default 50, max 50 per page)
            order: Sort order (relevance, date, rating, viewCount, title)
            published_after: RFC 3339 timestamp (e.g., '2024-01-01T00:00:00Z')

        Returns:
            List of video metadata dictionaries
        """
        try:
            videos = []
            next_page_token = None
            remaining = max_results

            while remaining > 0:
                # YouTube API max 50 results per page
                page_size = min(remaining, 50)

                # Build search request
                request_params = {
                    'part': 'id,snippet',
                    'q': query,
                    'type': 'video',
                    'maxResults': page_size,
                    'order': order
                }

                if published_after:
                    request_params['publishedAfter'] = published_after

                if next_page_token:
                    request_params['pageToken'] = next_page_token

                # Execute search
                search_response = self.youtube.search().list(**request_params).execute()

                # Extract video data
                for item in search_response.get('items', []):
                    video_id = item['id']['videoId']
                    snippet = item['snippet']

                    videos.append({
                        'video_id': video_id,
                        'title': snippet['title'],
                        'description': snippet['description'],
                        'channel_title': snippet['channelTitle'],
                        'channel_id': snippet['channelId'],
                        'published_at': snippet['publishedAt'],
                        'thumbnail_url': snippet['thumbnails']['high']['url']
                    })

                # Check for next page
                next_page_token = search_response.get('nextPageToken')
                remaining -= page_size

                if not next_page_token:
                    break

            return videos

        except HttpError as e:
            error_content = json.loads(e.content.decode('utf-8'))
            error_message = error_content.get('error', {}).get('message', str(e))
            raise Exception(f"YouTube API error: {error_message}")

    def get_video_metadata(self, video_id: str) -> Dict:
        """
        Get detailed metadata for a video

        Args:
            video_id: YouTube video ID

        Returns:
            Dictionary with video metadata
        """
        try:
            request = self.youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=video_id
            )
            response = request.execute()

            if not response['items']:
                raise ValueError(f"Video {video_id} not found")

            item = response['items'][0]
            snippet = item['snippet']
            content_details = item['contentDetails']
            statistics = item['statistics']

            return {
                'video_id': video_id,
                'title': snippet['title'],
                'description': snippet['description'],
                'channel_title': snippet['channelTitle'],
                'channel_id': snippet['channelId'],
                'published_at': snippet['publishedAt'],
                'duration': content_details['duration'],
                'view_count': int(statistics.get('viewCount', 0)),
                'like_count': int(statistics.get('likeCount', 0)),
                'comment_count': int(statistics.get('commentCount', 0)),
                'thumbnail_url': snippet['thumbnails']['high']['url'],
                'tags': snippet.get('tags', [])
            }

        except HttpError as e:
            error_content = json.loads(e.content.decode('utf-8'))
            error_message = error_content.get('error', {}).get('message', str(e))
            raise Exception(f"YouTube API error: {error_message}")

    def download_video(
        self,
        video_id: str,
        output_dir: Path,
        format: str = 'best'
    ) -> Path:
        """
        Download video using yt-dlp

        Args:
            video_id: YouTube video ID
            output_dir: Directory to save video
            format: Video format ('best', 'bestvideo', etc.)

        Returns:
            Path to downloaded video file
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Output template: video_id.ext
        output_template = str(output_dir / f"{video_id}.%(ext)s")
        url = f"https://www.youtube.com/watch?v={video_id}"

        try:
            # Run yt-dlp command
            cmd = [
                'yt-dlp',
                '-f', format,
                '--no-playlist',
                '--no-warnings',
                '-o', output_template,
                url
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )

            # Find downloaded file
            downloaded_files = list(output_dir.glob(f"{video_id}.*"))
            if not downloaded_files:
                raise FileNotFoundError(f"Downloaded file not found for video {video_id}")

            return downloaded_files[0]

        except subprocess.CalledProcessError as e:
            raise Exception(f"yt-dlp error: {e.stderr}")

    def extract_audio(
        self,
        video_path: Path,
        output_dir: Optional[Path] = None
    ) -> Path:
        """
        Extract audio track to WAV format for Whisper

        Args:
            video_path: Path to video file
            output_dir: Directory to save audio (defaults to video dir)

        Returns:
            Path to extracted WAV audio file
        """
        video_path = Path(video_path)
        if output_dir is None:
            output_dir = video_path.parent

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Output: same name as video but .wav extension
        audio_path = output_dir / f"{video_path.stem}.wav"

        try:
            # Use ffmpeg to extract audio
            cmd = [
                'ffmpeg',
                '-i', str(video_path),
                '-vn',  # No video
                '-acodec', 'pcm_s16le',  # WAV PCM 16-bit
                '-ar', '16000',  # 16kHz sample rate (Whisper optimized)
                '-ac', '1',  # Mono
                '-y',  # Overwrite
                str(audio_path)
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )

            return audio_path

        except subprocess.CalledProcessError as e:
            raise Exception(f"ffmpeg error: {e.stderr}")

    def is_duplicate(
        self,
        video_id: str,
        existing_videos: List[str]
    ) -> bool:
        """
        Check if video already processed

        Args:
            video_id: YouTube video ID to check
            existing_videos: List of already processed video IDs

        Returns:
            True if duplicate, False otherwise
        """
        return video_id in existing_videos


# Checkpoint functions for testing
def test_search(query: str = "DIY home lighting problems", max_results: int = 5):
    """Test video search (CHECKPOINT 1)"""
    print(f"\n🔍 CHECKPOINT 1: Testing video search for '{query}'...")

    yt = YouTubeDataSource()
    results = yt.search_videos(query=query, max_results=max_results)

    print(f"✅ Found {len(results)} videos\n")

    for i, video in enumerate(results, 1):
        print(f"{i}. {video['title']}")
        print(f"   Channel: {video['channel_title']}")
        print(f"   Published: {video['published_at']}")
        print(f"   Video ID: {video['video_id']}")
        print()

    return results


def test_metadata(video_id: str):
    """Test metadata extraction (CHECKPOINT 2)"""
    print(f"\n📊 CHECKPOINT 2: Testing metadata extraction for video {video_id}...")

    yt = YouTubeDataSource()
    metadata = yt.get_video_metadata(video_id)

    print("✅ Metadata extracted:\n")
    print(f"Title: {metadata['title']}")
    print(f"Channel: {metadata['channel_title']}")
    print(f"Duration: {metadata['duration']}")
    print(f"Views: {metadata['view_count']:,}")
    print(f"Likes: {metadata['like_count']:,}")
    print(f"Comments: {metadata['comment_count']:,}")
    print(f"Tags: {', '.join(metadata.get('tags', [])[:5])}")

    return metadata


def test_download(video_id: str, output_dir: str = "/tmp/youtube_test"):
    """Test video download (CHECKPOINT 3)"""
    print(f"\n⬇️  CHECKPOINT 3: Testing video download for {video_id}...")

    yt = YouTubeDataSource()
    video_path = yt.download_video(video_id, Path(output_dir))

    print(f"✅ Video downloaded:\n")
    print(f"Path: {video_path}")
    print(f"Size: {video_path.stat().st_size / (1024*1024):.2f} MB")
    print(f"Extension: {video_path.suffix}")

    return video_path


def test_audio_extraction(video_path: Path):
    """Test audio extraction (CHECKPOINT 4)"""
    print(f"\n🎵 CHECKPOINT 4: Testing audio extraction from {video_path.name}...")

    yt = YouTubeDataSource()
    audio_path = yt.extract_audio(video_path)

    print(f"✅ Audio extracted:\n")
    print(f"Path: {audio_path}")
    print(f"Size: {audio_path.stat().st_size / (1024*1024):.2f} MB")
    print(f"Format: WAV 16kHz mono (Whisper-optimized)")

    return audio_path


def test_deduplication():
    """Test deduplication logic (CHECKPOINT 5)"""
    print(f"\n🔍 CHECKPOINT 5: Testing deduplication logic...")

    yt = YouTubeDataSource()
    existing = ['abc123', 'def456', 'ghi789']

    test_cases = [
        ('abc123', True),
        ('xyz999', False),
        ('def456', True)
    ]

    print("✅ Deduplication tests:\n")
    for video_id, expected in test_cases:
        is_dup = yt.is_duplicate(video_id, existing)
        status = "✅" if is_dup == expected else "❌"
        print(f"{status} {video_id}: {'Duplicate' if is_dup else 'New'} (expected: {'Duplicate' if expected else 'New'})")


if __name__ == "__main__":
    # CHECKPOINT 1: Test search
    results = test_search()

    # CHECKPOINT 2: Test metadata on first result
    if results:
        test_metadata(results[0]['video_id'])
