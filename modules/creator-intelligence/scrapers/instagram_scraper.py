"""
Instagram scraper using instagrapi library (free GitHub solution).
Primary method for Instagram data collection with circuit breaker protection.
"""

import time
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired,
    PleaseWaitFewMinutes,
    ChallengeRequired,
    RateLimitError
)

logger = logging.getLogger(__name__)


class InstagramCircuitBreaker:
    """Circuit breaker to prevent ban escalation."""

    def __init__(self):
        self.ban_detected = False
        self.ban_timestamp = None
        self.consecutive_errors = 0
        self.max_consecutive_errors = 3

    def trigger_circuit_breaker(self):
        """Trigger circuit breaker on ban detection."""
        self.ban_detected = True
        self.ban_timestamp = datetime.now()
        logger.critical("🚨 INSTAGRAM BAN DETECTED - STOPPING FOR 24 HOURS")

    def is_open(self) -> bool:
        """Check if circuit breaker is open (blocking requests)."""
        if not self.ban_detected:
            return False

        # Auto-reset after 24 hours
        hours_since_ban = (datetime.now() - self.ban_timestamp).total_seconds() / 3600
        if hours_since_ban >= 24:
            logger.info("✅ Circuit breaker reset after 24 hours")
            self.ban_detected = False
            self.consecutive_errors = 0
            return False

        return True

    def record_error(self):
        """Record an error and possibly trigger circuit breaker."""
        self.consecutive_errors += 1
        if self.consecutive_errors >= self.max_consecutive_errors:
            self.trigger_circuit_breaker()

    def record_success(self):
        """Record a successful request."""
        self.consecutive_errors = 0


class InstagramScraper:
    """
    Instagram scraper using instagrapi (free GitHub library).
    Implements rate limiting and circuit breaker protection.
    """

    def __init__(self, cache_dir: Path, rate_limit_seconds: int = 150):
        """
        Initialize Instagram scraper.

        Args:
            cache_dir: Directory for caching responses
            rate_limit_seconds: Seconds between requests (default 150 = 2.5 min)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.rate_limit = rate_limit_seconds
        self.circuit_breaker = InstagramCircuitBreaker()
        self.client = Client()
        self.last_request_time = 0
        self.session_file = self.cache_dir / "instagram_session.json"

        # Try to load existing session
        self._load_session()

        logger.info(f"✅ InstagramScraper initialized (rate limit: {rate_limit_seconds}s)")

    def _load_session(self):
        """Load saved session if available."""
        if self.session_file.exists():
            try:
                self.client.load_settings(str(self.session_file))
                logger.info("✅ Loaded existing Instagram session")
            except Exception as e:
                logger.warning(f"⚠️  Could not load session: {e}")

    def _save_session(self):
        """Save current session."""
        try:
            self.client.dump_settings(str(self.session_file))
            logger.debug("Session saved")
        except Exception as e:
            logger.warning(f"⚠️  Could not save session: {e}")

    def _rate_limit_wait(self):
        """Enforce rate limiting between requests."""
        if self.circuit_breaker.is_open():
            raise Exception("Circuit breaker is open - Instagram scraping disabled for 24 hours")

        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            sleep_time = self.rate_limit - elapsed
            logger.info(f"⏳ Rate limiting: sleeping {sleep_time:.0f}s")
            time.sleep(sleep_time)

        self.last_request_time = time.time()

    def login(self, username: str, password: str):
        """
        Login to Instagram (only needed for private accounts).

        Args:
            username: Instagram username
            password: Instagram password
        """
        try:
            self.client.login(username, password)
            self._save_session()
            logger.info(f"✅ Logged in as {username}")
        except Exception as e:
            logger.error(f"❌ Login failed: {e}")
            raise

    def search_users(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search for Instagram users by query.

        Args:
            query: Search query (e.g., "LED lighting")
            limit: Maximum number of results

        Returns:
            List of user dictionaries
        """
        self._rate_limit_wait()

        try:
            logger.info(f"🔍 Searching Instagram users: '{query}'")
            users = self.client.search_users(query, amount=limit)

            results = []
            for user in users:
                results.append({
                    'platform': 'instagram',
                    'username': user.username,
                    'display_name': user.full_name,
                    'profile_url': f"https://instagram.com/{user.username}",
                    'follower_count': user.follower_count,
                    'bio': user.biography,
                    'is_verified': user.is_verified,
                    'is_business': user.is_business,
                    'category': user.category,
                    'metadata': {
                        'user_id': str(user.pk),
                        'following_count': user.following_count,
                        'media_count': user.media_count,
                        'is_private': user.is_private,
                        'external_url': user.external_url,
                        'profile_pic_url': user.profile_pic_url.unicode_string() if user.profile_pic_url else None
                    }
                })

            self.circuit_breaker.record_success()
            logger.info(f"✅ Found {len(results)} users")

            # Cache results
            cache_file = self.cache_dir / f"search_{query.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json"
            with open(cache_file, 'w') as f:
                json.dump(results, f, indent=2)

            return results

        except (PleaseWaitFewMinutes, RateLimitError) as e:
            logger.error(f"🚨 Rate limit hit: {e}")
            self.circuit_breaker.record_error()
            raise

        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            self.circuit_breaker.record_error()
            raise

    def get_user_info(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed user information.

        Args:
            username: Instagram username

        Returns:
            User dictionary or None if not found
        """
        self._rate_limit_wait()

        try:
            logger.info(f"📥 Fetching user info: {username}")
            user_id = self.client.user_id_from_username(username)
            user = self.client.user_info(user_id)

            result = {
                'platform': 'instagram',
                'username': user.username,
                'display_name': user.full_name,
                'profile_url': f"https://instagram.com/{user.username}",
                'follower_count': user.follower_count,
                'bio': user.biography,
                'is_verified': user.is_verified,
                'is_business': user.is_business,
                'category': user.category,
                'content_count': user.media_count,
                'metadata': {
                    'user_id': str(user.pk),
                    'following_count': user.following_count,
                    'is_private': user.is_private,
                    'external_url': user.external_url,
                    'profile_pic_url': user.profile_pic_url.unicode_string() if user.profile_pic_url else None,
                    'public_email': user.public_email,
                    'contact_phone_number': user.contact_phone_number,
                    'city_name': user.city_name,
                    'address_street': user.address_street
                }
            }

            self.circuit_breaker.record_success()

            # Cache result
            cache_file = self.cache_dir / f"user_{username}_{datetime.now().strftime('%Y%m%d')}.json"
            with open(cache_file, 'w') as f:
                json.dump(result, f, indent=2)

            return result

        except (PleaseWaitFewMinutes, RateLimitError) as e:
            logger.error(f"🚨 Rate limit hit: {e}")
            self.circuit_breaker.record_error()
            raise

        except Exception as e:
            logger.error(f"❌ Failed to fetch user {username}: {e}")
            return None

    def get_user_medias(self, username: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get recent media posts from user.

        Args:
            username: Instagram username
            limit: Maximum number of posts

        Returns:
            List of media dictionaries
        """
        self._rate_limit_wait()

        try:
            logger.info(f"📥 Fetching {limit} posts from {username}")
            user_id = self.client.user_id_from_username(username)
            medias = self.client.user_medias(user_id, amount=limit)

            results = []
            for media in medias:
                results.append({
                    'creator_id': None,  # Will be filled by orchestrator
                    'platform': 'instagram',
                    'content_id': media.code,
                    'content_type': media.media_type.name.lower(),  # PHOTO, VIDEO, ALBUM
                    'title': media.title or '',
                    'description': media.caption_text if media.caption_text else '',
                    'url': f"https://instagram.com/p/{media.code}/",
                    'view_count': media.view_count if hasattr(media, 'view_count') else None,
                    'like_count': media.like_count,
                    'comment_count': media.comment_count,
                    'published_at': media.taken_at.isoformat(),
                    'metadata': {
                        'media_id': str(media.pk),
                        'thumbnail_url': media.thumbnail_url.unicode_string() if media.thumbnail_url else None,
                        'video_url': media.video_url.unicode_string() if media.video_url else None,
                        'location': media.location.name if media.location else None,
                        'tagged_users': [u.username for u in (media.usertags or [])]
                    }
                })

            self.circuit_breaker.record_success()
            logger.info(f"✅ Retrieved {len(results)} posts")

            # Cache results
            cache_file = self.cache_dir / f"medias_{username}_{datetime.now().strftime('%Y%m%d')}.json"
            with open(cache_file, 'w') as f:
                json.dump(results, f, indent=2)

            return results

        except (PleaseWaitFewMinutes, RateLimitError) as e:
            logger.error(f"🚨 Rate limit hit: {e}")
            self.circuit_breaker.record_error()
            raise

        except Exception as e:
            logger.error(f"❌ Failed to fetch medias for {username}: {e}")
            return []

    def get_hashtag_medias(self, hashtag: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent posts for a hashtag.

        Args:
            hashtag: Hashtag to search (without #)
            limit: Maximum number of posts

        Returns:
            List of media dictionaries with creator info
        """
        self._rate_limit_wait()

        try:
            logger.info(f"🔍 Searching hashtag: #{hashtag}")
            medias = self.client.hashtag_medias_recent(hashtag, amount=limit)

            results = []
            for media in medias:
                results.append({
                    'creator_username': media.user.username,
                    'creator_follower_count': media.user.follower_count,
                    'platform': 'instagram',
                    'content_id': media.code,
                    'content_type': media.media_type.name.lower(),
                    'title': media.title or '',
                    'description': media.caption_text if media.caption_text else '',
                    'url': f"https://instagram.com/p/{media.code}/",
                    'like_count': media.like_count,
                    'comment_count': media.comment_count,
                    'published_at': media.taken_at.isoformat(),
                })

            self.circuit_breaker.record_success()
            logger.info(f"✅ Found {len(results)} posts for #{hashtag}")

            return results

        except (PleaseWaitFewMinutes, RateLimitError) as e:
            logger.error(f"🚨 Rate limit hit: {e}")
            self.circuit_breaker.record_error()
            raise

        except Exception as e:
            logger.error(f"❌ Failed to search hashtag #{hashtag}: {e}")
            return []


if __name__ == "__main__":
    # Test Instagram scraper
    from creator_intelligence.core.config import config

    scraper = InstagramScraper(
        cache_dir=config.instagram_cache,
        rate_limit_seconds=config.instagram_rate_limit
    )

    # Test search
    users = scraper.search_users("LED lighting", limit=5)
    print(f"Found {len(users)} users")

    if users:
        # Test getting user info
        user_info = scraper.get_user_info(users[0]['username'])
        print(f"User info: {json.dumps(user_info, indent=2)}")
