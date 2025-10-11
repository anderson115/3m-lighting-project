"""
YouTube scraper using official YouTube Data API v3 (Tier 1).
Free tier with 10,000 units/day quota.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)


class YouTubeScraper:
    """
    YouTube scraper using official Data API v3.
    Quota-aware implementation (10,000 units/day default).
    """

    # API quota costs
    QUOTA_COSTS = {
        'search': 100,
        'channels': 1,
        'videos': 1,
        'playlistItems': 1
    }

    def __init__(self, api_key: str, cache_dir: Path):
        """
        Initialize YouTube scraper.

        Args:
            api_key: YouTube Data API v3 key
            cache_dir: Directory for caching responses
        """
        self.api_key = api_key
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.quota_used = 0

        logger.info(f"✅ YouTubeScraper initialized")

    def _log_quota(self, operation: str):
        """Log quota usage."""
        cost = self.QUOTA_COSTS.get(operation, 1)
        self.quota_used += cost
        logger.debug(f"📊 Quota used: {self.quota_used} units (+{cost} for {operation})")

    def search_channels(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search for YouTube channels by keyword.

        Args:
            query: Search query (e.g., "LED lighting tutorial")
            limit: Maximum number of results

        Returns:
            List of channel dictionaries
        """
        try:
            logger.info(f"🔍 Searching YouTube channels: '{query}'")

            # Search for channels (100 quota units)
            search_response = self.youtube.search().list(
                q=query,
                type='channel',
                part='snippet',
                maxResults=min(limit, 50),  # API max is 50
                order='relevance'
            ).execute()
            self._log_quota('search')

            # Extract channel IDs
            channel_ids = [item['snippet']['channelId'] for item in search_response.get('items', [])]

            if not channel_ids:
                logger.warning(f"No channels found for query: {query}")
                return []

            # Get detailed channel info (1 quota unit per channel batch)
            channels_response = self.youtube.channels().list(
                id=','.join(channel_ids),
                part='snippet,statistics,contentDetails'
            ).execute()
            self._log_quota('channels')

            results = []
            for channel in channels_response.get('items', []):
                snippet = channel['snippet']
                stats = channel['statistics']

                results.append({
                    'platform': 'youtube',
                    'username': snippet['customUrl'] if 'customUrl' in snippet else channel['id'],
                    'display_name': snippet['title'],
                    'profile_url': f"https://youtube.com/channel/{channel['id']}",
                    'follower_count': int(stats.get('subscriberCount', 0)),
                    'bio': snippet.get('description', ''),
                    'content_count': int(stats.get('videoCount', 0)),
                    'location': snippet.get('country', ''),
                    'metadata': {
                        'channel_id': channel['id'],
                        'view_count': int(stats.get('viewCount', 0)),
                        'thumbnail_url': snippet['thumbnails']['high']['url'] if 'thumbnails' in snippet else None,
                        'published_at': snippet['publishedAt'],
                        'uploads_playlist_id': channel['contentDetails']['relatedPlaylists']['uploads']
                    }
                })

            logger.info(f"✅ Found {len(results)} YouTube channels")

            # Cache results
            cache_file = self.cache_dir / f"search_{query.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json"
            with open(cache_file, 'w') as f:
                json.dump(results, f, indent=2)

            return results

        except HttpError as e:
            logger.error(f"❌ YouTube API error: {e}")
            return []
        except Exception as e:
            logger.error(f"❌ YouTube search failed: {e}")
            return []

    def get_channel_info(self, channel_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed channel information.

        Args:
            channel_id: YouTube channel ID

        Returns:
            Channel dictionary or None if not found
        """
        try:
            logger.info(f"📥 Fetching YouTube channel: {channel_id}")

            response = self.youtube.channels().list(
                id=channel_id,
                part='snippet,statistics,contentDetails,brandingSettings'
            ).execute()
            self._log_quota('channels')

            items = response.get('items', [])
            if not items:
                logger.warning(f"Channel not found: {channel_id}")
                return None

            channel = items[0]
            snippet = channel['snippet']
            stats = channel['statistics']

            result = {
                'platform': 'youtube',
                'username': snippet.get('customUrl', channel_id),
                'display_name': snippet['title'],
                'profile_url': f"https://youtube.com/channel/{channel_id}",
                'follower_count': int(stats.get('subscriberCount', 0)),
                'bio': snippet.get('description', ''),
                'content_count': int(stats.get('videoCount', 0)),
                'location': snippet.get('country', ''),
                'metadata': {
                    'channel_id': channel_id,
                    'view_count': int(stats.get('viewCount', 0)),
                    'thumbnail_url': snippet['thumbnails']['high']['url'] if 'thumbnails' in snippet else None,
                    'published_at': snippet['publishedAt'],
                    'uploads_playlist_id': channel['contentDetails']['relatedPlaylists']['uploads'],
                    'keywords': channel.get('brandingSettings', {}).get('channel', {}).get('keywords', '')
                }
            }

            # Calculate engagement estimate
            if result['content_count'] > 0:
                avg_views_per_video = result['metadata']['view_count'] / result['content_count']
                result['metadata']['avg_views_per_video'] = int(avg_views_per_video)

            # Cache result
            cache_file = self.cache_dir / f"channel_{channel_id}_{datetime.now().strftime('%Y%m%d')}.json"
            with open(cache_file, 'w') as f:
                json.dump(result, f, indent=2)

            return result

        except HttpError as e:
            logger.error(f"❌ YouTube API error: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Failed to fetch channel {channel_id}: {e}")
            return None

    def get_channel_videos(self, channel_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent videos from a channel.

        Args:
            channel_id: YouTube channel ID
            limit: Maximum number of videos

        Returns:
            List of video dictionaries
        """
        try:
            logger.info(f"📥 Fetching {limit} videos from channel {channel_id}")

            # Get uploads playlist ID
            channel_response = self.youtube.channels().list(
                id=channel_id,
                part='contentDetails'
            ).execute()
            self._log_quota('channels')

            items = channel_response.get('items', [])
            if not items:
                return []

            uploads_playlist_id = items[0]['contentDetails']['relatedPlaylists']['uploads']

            # Get playlist items (video IDs)
            playlist_response = self.youtube.playlistItems().list(
                playlistId=uploads_playlist_id,
                part='contentDetails',
                maxResults=min(limit, 50)
            ).execute()
            self._log_quota('playlistItems')

            video_ids = [item['contentDetails']['videoId'] for item in playlist_response.get('items', [])]

            if not video_ids:
                return []

            # Get video details
            videos_response = self.youtube.videos().list(
                id=','.join(video_ids),
                part='snippet,statistics,contentDetails'
            ).execute()
            self._log_quota('videos')

            results = []
            for video in videos_response.get('items', []):
                snippet = video['snippet']
                stats = video['statistics']

                results.append({
                    'creator_id': None,  # Will be filled by orchestrator
                    'platform': 'youtube',
                    'content_id': video['id'],
                    'content_type': 'video',
                    'title': snippet['title'],
                    'description': snippet['description'],
                    'url': f"https://youtube.com/watch?v={video['id']}",
                    'view_count': int(stats.get('viewCount', 0)),
                    'like_count': int(stats.get('likeCount', 0)),
                    'comment_count': int(stats.get('commentCount', 0)),
                    'published_at': snippet['publishedAt'],
                    'metadata': {
                        'duration': video['contentDetails']['duration'],
                        'thumbnail_url': snippet['thumbnails']['high']['url'] if 'thumbnails' in snippet else None,
                        'tags': snippet.get('tags', []),
                        'category_id': snippet.get('categoryId', ''),
                        'default_language': snippet.get('defaultLanguage', ''),
                        'favorite_count': int(stats.get('favoriteCount', 0))
                    }
                })

            logger.info(f"✅ Retrieved {len(results)} videos")

            # Cache results
            cache_file = self.cache_dir / f"videos_{channel_id}_{datetime.now().strftime('%Y%m%d')}.json"
            with open(cache_file, 'w') as f:
                json.dump(results, f, indent=2)

            return results

        except HttpError as e:
            logger.error(f"❌ YouTube API error: {e}")
            return []
        except Exception as e:
            logger.error(f"❌ Failed to fetch videos for channel {channel_id}: {e}")
            return []

    def search_videos(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search for videos by keyword.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of video dictionaries with channel info
        """
        try:
            logger.info(f"🔍 Searching YouTube videos: '{query}'")

            # Search for videos
            search_response = self.youtube.search().list(
                q=query,
                type='video',
                part='snippet',
                maxResults=min(limit, 50),
                order='relevance'
            ).execute()
            self._log_quota('search')

            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]

            if not video_ids:
                return []

            # Get video details
            videos_response = self.youtube.videos().list(
                id=','.join(video_ids),
                part='snippet,statistics'
            ).execute()
            self._log_quota('videos')

            results = []
            for video in videos_response.get('items', []):
                snippet = video['snippet']
                stats = video['statistics']

                results.append({
                    'creator_channel_id': snippet['channelId'],
                    'creator_channel_title': snippet['channelTitle'],
                    'platform': 'youtube',
                    'content_id': video['id'],
                    'content_type': 'video',
                    'title': snippet['title'],
                    'description': snippet['description'],
                    'url': f"https://youtube.com/watch?v={video['id']}",
                    'view_count': int(stats.get('viewCount', 0)),
                    'like_count': int(stats.get('likeCount', 0)),
                    'comment_count': int(stats.get('commentCount', 0)),
                    'published_at': snippet['publishedAt']
                })

            logger.info(f"✅ Found {len(results)} videos")

            return results

        except HttpError as e:
            logger.error(f"❌ YouTube API error: {e}")
            return []
        except Exception as e:
            logger.error(f"❌ Failed to search videos: {e}")
            return []


if __name__ == "__main__":
    # Test YouTube scraper
    from creator_intelligence.core.config import config

    scraper = YouTubeScraper(
        api_key=config.youtube_api_key,
        cache_dir=config.youtube_cache
    )

    # Test channel search
    channels = scraper.search_channels("LED lighting tutorial", limit=5)
    print(f"Found {len(channels)} channels")
    print(f"Quota used: {scraper.quota_used} units")

    if channels:
        # Test getting channel info
        channel_info = scraper.get_channel_info(channels[0]['metadata']['channel_id'])
        print(f"Channel info: {json.dumps(channel_info, indent=2)}")
