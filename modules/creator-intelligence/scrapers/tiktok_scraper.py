"""
TikTok scraper using TikTokApi library (free GitHub solution).
Primary method for TikTok data collection with rate limiting.
"""

import time
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
from TikTokApi import TikTokApi

logger = logging.getLogger(__name__)


class TikTokScraper:
    """
    TikTok scraper using TikTokApi (free GitHub library).
    Implements rate limiting to avoid detection.
    """

    def __init__(self, cache_dir: Path, rate_limit_seconds: int = 5):
        """
        Initialize TikTok scraper.

        Args:
            cache_dir: Directory for caching responses
            rate_limit_seconds: Seconds between requests (default 5)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.rate_limit = rate_limit_seconds
        self.last_request_time = 0
        self.api = None  # Will be initialized on first use

        logger.info(f"✅ TikTokScraper initialized (rate limit: {rate_limit_seconds}s)")

    async def _get_api(self) -> TikTokApi:
        """Get or create TikTokApi instance."""
        if self.api is None:
            self.api = TikTokApi()
        return self.api

    def _rate_limit_wait(self):
        """Enforce rate limiting between requests."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            sleep_time = self.rate_limit - elapsed
            logger.debug(f"⏳ Rate limiting: sleeping {sleep_time:.1f}s")
            time.sleep(sleep_time)
        self.last_request_time = time.time()

    async def search_users(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search for TikTok users by keyword.

        Args:
            query: Search query (e.g., "LED lighting")
            limit: Maximum number of results

        Returns:
            List of user dictionaries
        """
        self._rate_limit_wait()

        try:
            logger.info(f"🔍 Searching TikTok users: '{query}'")
            api = await self._get_api()

            # Search for users
            users = []
            async for user in api.search.users(query, count=limit):
                self._rate_limit_wait()  # Rate limit between each user fetch

                users.append({
                    'platform': 'tiktok',
                    'username': user.username,
                    'display_name': user.nickname,
                    'profile_url': f"https://tiktok.com/@{user.username}",
                    'follower_count': user.follower_count,
                    'bio': user.signature,
                    'is_verified': user.verified,
                    'content_count': user.video_count,
                    'metadata': {
                        'user_id': user.id,
                        'following_count': user.following_count,
                        'heart_count': user.heart_count,  # Total likes received
                        'avatar_url': user.avatar_url,
                        'is_private': getattr(user, 'private_account', False)
                    }
                })

            logger.info(f"✅ Found {len(users)} TikTok users")

            # Cache results
            cache_file = self.cache_dir / f"search_{query.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json"
            with open(cache_file, 'w') as f:
                json.dump(users, f, indent=2)

            return users

        except Exception as e:
            logger.error(f"❌ TikTok search failed: {e}")
            return []

    async def get_user_info(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed TikTok user information.

        Args:
            username: TikTok username (without @)

        Returns:
            User dictionary or None if not found
        """
        self._rate_limit_wait()

        try:
            logger.info(f"📥 Fetching TikTok user: @{username}")
            api = await self._get_api()
            user = api.user(username)
            user_data = await user.info()

            result = {
                'platform': 'tiktok',
                'username': user_data['username'],
                'display_name': user_data['nickname'],
                'profile_url': f"https://tiktok.com/@{user_data['username']}",
                'follower_count': user_data['followerCount'],
                'bio': user_data['signature'],
                'is_verified': user_data.get('verified', False),
                'content_count': user_data['videoCount'],
                'metadata': {
                    'user_id': user_data['id'],
                    'following_count': user_data['followingCount'],
                    'heart_count': user_data['heartCount'],
                    'avatar_url': user_data.get('avatarLarger', ''),
                    'is_private': user_data.get('privateAccount', False),
                    'bio_link': user_data.get('bioLink', {}).get('link', '')
                }
            }

            # Calculate engagement rate
            if result['follower_count'] > 0 and result['content_count'] > 0:
                avg_likes_per_video = result['metadata']['heart_count'] / result['content_count']
                engagement_rate = (avg_likes_per_video / result['follower_count']) * 100
                result['engagement_rate'] = round(engagement_rate, 2)

            # Cache result
            cache_file = self.cache_dir / f"user_{username}_{datetime.now().strftime('%Y%m%d')}.json"
            with open(cache_file, 'w') as f:
                json.dump(result, f, indent=2)

            logger.info(f"✅ Retrieved user @{username}")
            return result

        except Exception as e:
            logger.error(f"❌ Failed to fetch TikTok user @{username}: {e}")
            return None

    async def get_user_videos(self, username: str, limit: int = 30) -> List[Dict[str, Any]]:
        """
        Get recent videos from TikTok user.

        Args:
            username: TikTok username (without @)
            limit: Maximum number of videos

        Returns:
            List of video dictionaries
        """
        self._rate_limit_wait()

        try:
            logger.info(f"📥 Fetching {limit} videos from @{username}")
            api = await self._get_api()
            user = api.user(username)

            videos = []
            count = 0
            async for video in user.videos(count=limit):
                if count >= limit:
                    break

                self._rate_limit_wait()  # Rate limit between video fetches

                videos.append({
                    'creator_id': None,  # Will be filled by orchestrator
                    'platform': 'tiktok',
                    'content_id': video.id,
                    'content_type': 'video',
                    'title': '',  # TikTok doesn't have separate titles
                    'description': video.desc,
                    'url': f"https://tiktok.com/@{username}/video/{video.id}",
                    'view_count': video.stats.get('playCount', 0),
                    'like_count': video.stats.get('diggCount', 0),
                    'comment_count': video.stats.get('commentCount', 0),
                    'published_at': datetime.fromtimestamp(video.createTime).isoformat(),
                    'metadata': {
                        'share_count': video.stats.get('shareCount', 0),
                        'duration': video.video.get('duration', 0),
                        'music_title': video.music.get('title', ''),
                        'music_author': video.music.get('authorName', ''),
                        'hashtags': [tag['name'] for tag in video.challenges] if hasattr(video, 'challenges') else [],
                        'video_url': video.video.get('playAddr', ''),
                        'cover_url': video.video.get('cover', '')
                    }
                })
                count += 1

            logger.info(f"✅ Retrieved {len(videos)} videos from @{username}")

            # Cache results
            cache_file = self.cache_dir / f"videos_{username}_{datetime.now().strftime('%Y%m%d')}.json"
            with open(cache_file, 'w') as f:
                json.dump(videos, f, indent=2)

            return videos

        except Exception as e:
            logger.error(f"❌ Failed to fetch videos from @{username}: {e}")
            return []

    async def search_hashtag(self, hashtag: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search videos by hashtag.

        Args:
            hashtag: Hashtag to search (without #)
            limit: Maximum number of videos

        Returns:
            List of video dictionaries with creator info
        """
        self._rate_limit_wait()

        try:
            logger.info(f"🔍 Searching TikTok hashtag: #{hashtag}")
            api = await self._get_api()

            videos = []
            count = 0
            async for video in api.hashtag(name=hashtag).videos(count=limit):
                if count >= limit:
                    break

                self._rate_limit_wait()

                videos.append({
                    'creator_username': video.author.username,
                    'creator_follower_count': video.author.follower_count if hasattr(video.author, 'follower_count') else None,
                    'platform': 'tiktok',
                    'content_id': video.id,
                    'content_type': 'video',
                    'description': video.desc,
                    'url': f"https://tiktok.com/@{video.author.username}/video/{video.id}",
                    'view_count': video.stats.get('playCount', 0),
                    'like_count': video.stats.get('diggCount', 0),
                    'comment_count': video.stats.get('commentCount', 0),
                    'published_at': datetime.fromtimestamp(video.createTime).isoformat(),
                })
                count += 1

            logger.info(f"✅ Found {len(videos)} videos for #{hashtag}")

            # Cache results
            cache_file = self.cache_dir / f"hashtag_{hashtag}_{datetime.now().strftime('%Y%m%d')}.json"
            with open(cache_file, 'w') as f:
                json.dump(videos, f, indent=2)

            return videos

        except Exception as e:
            logger.error(f"❌ Failed to search hashtag #{hashtag}: {e}")
            return []

    async def close(self):
        """Close API connection."""
        if self.api:
            await self.api.close()
            logger.info("TikTok API connection closed")


# Synchronous wrapper functions for easier use
def sync_search_users(cache_dir: Path, query: str, limit: int = 50, rate_limit: int = 5) -> List[Dict]:
    """Synchronous wrapper for search_users."""
    import asyncio
    scraper = TikTokScraper(cache_dir, rate_limit)
    try:
        return asyncio.run(scraper.search_users(query, limit))
    finally:
        asyncio.run(scraper.close())


def sync_get_user_info(cache_dir: Path, username: str, rate_limit: int = 5) -> Optional[Dict]:
    """Synchronous wrapper for get_user_info."""
    import asyncio
    scraper = TikTokScraper(cache_dir, rate_limit)
    try:
        return asyncio.run(scraper.get_user_info(username))
    finally:
        asyncio.run(scraper.close())


def sync_get_user_videos(cache_dir: Path, username: str, limit: int = 30, rate_limit: int = 5) -> List[Dict]:
    """Synchronous wrapper for get_user_videos."""
    import asyncio
    scraper = TikTokScraper(cache_dir, rate_limit)
    try:
        return asyncio.run(scraper.get_user_videos(username, limit))
    finally:
        asyncio.run(scraper.close())


if __name__ == "__main__":
    # Test TikTok scraper
    import asyncio
    from creator_intelligence.core.config import config

    async def test():
        scraper = TikTokScraper(
            cache_dir=config.tiktok_cache,
            rate_limit_seconds=config.tiktok_rate_limit
        )

        # Test search
        users = await scraper.search_users("LED lighting", limit=5)
        print(f"Found {len(users)} users")

        if users:
            # Test getting user info
            user_info = await scraper.get_user_info(users[0]['username'])
            print(f"User info: {json.dumps(user_info, indent=2)}")

        await scraper.close()

    asyncio.run(test())
