#!/usr/bin/env python3
"""
Reddit PRAW Scraper - Production Implementation
Scrapes real expert discussions from Reddit using official PRAW API
NO SYNTHETIC DATA - 100% real discussions only
"""

import praw
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import logging

from ..core.config import Config

class RedditScraper:
    """Production Reddit scraper using PRAW official API"""

    def __init__(self, config: Optional[Config] = None):
        """Initialize Reddit scraper with credentials from config"""
        self.config = config or Config()
        self.config.validate_credentials(tier=1)  # Validate Reddit credentials

        # Initialize PRAW Reddit instance
        reddit_config = self.config.get_reddit_config()
        self.reddit = praw.Reddit(
            client_id=reddit_config['client_id'],
            client_secret=reddit_config['client_secret'],
            user_agent=reddit_config['user_agent']
        )
        self.reddit.read_only = True

        # Setup logging
        self.logger = logging.getLogger(__name__)

        # Cache directory
        self.cache_dir = Path(__file__).parent.parent / "data" / "cache" / "reddit"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def scrape(
        self,
        query: str,
        subreddits: List[str],
        limit: int = 100,
        time_filter: str = "all",
        sort: str = "relevance"
    ) -> List[Dict]:
        """
        Scrape Reddit discussions using PRAW API

        Args:
            query: Search query (e.g., "LED lighting")
            subreddits: List of subreddit names (e.g., ["electricians", "homeimprovement"])
            limit: Max discussions to scrape per subreddit
            time_filter: Time filter ("all", "year", "month", "week", "day")
            sort: Sort method ("relevance", "hot", "top", "new")

        Returns:
            List of discussion dictionaries with full metadata
        """
        all_discussions = []

        for subreddit_name in subreddits:
            self.logger.info(f"Scraping r/{subreddit_name} for '{query}'...")

            try:
                subreddit = self.reddit.subreddit(subreddit_name)

                # Search subreddit
                posts = subreddit.search(
                    query=query,
                    limit=limit,
                    time_filter=time_filter,
                    sort=sort
                )

                for post in posts:
                    discussion = self._extract_post_data(post, subreddit_name)
                    all_discussions.append(discussion)

                self.logger.info(f"✅ Scraped {len([d for d in all_discussions if d['subreddit'] == subreddit_name])} posts from r/{subreddit_name}")

            except Exception as e:
                self.logger.error(f"❌ Error scraping r/{subreddit_name}: {e}")
                continue

        self.logger.info(f"🎯 Total scraped: {len(all_discussions)} discussions")
        return all_discussions

    def _extract_post_data(self, post, subreddit_name: str) -> Dict:
        """Extract complete post data including comments"""

        # Get top comments
        post.comments.replace_more(limit=0)  # Remove MoreComments objects
        top_comments = self._get_top_comments(post.comments.list(), limit=10)

        # Generate validation hash
        content = f"{post.id}{post.title}{post.selftext}{post.created_utc}"
        validation_hash = hashlib.sha256(content.encode()).hexdigest()

        discussion = {
            "id": post.id,
            "platform": "reddit",
            "subreddit": subreddit_name,
            "title": post.title,
            "url": f"https://reddit.com{post.permalink}",
            "author": str(post.author) if post.author else "[deleted]",
            "author_flair": post.author_flair_text,
            "score": post.score,
            "upvote_ratio": post.upvote_ratio,
            "num_comments": post.num_comments,
            "created_utc": int(post.created_utc),
            "created_date": datetime.fromtimestamp(post.created_utc).isoformat(),
            "selftext": post.selftext,
            "is_self": post.is_self,
            "link_flair_text": post.link_flair_text,
            "comments": top_comments,
            "validation_hash": validation_hash,
            "scraped_at": datetime.now().isoformat(),
            "api_source": "PRAW_official"
        }

        return discussion

    def _get_top_comments(self, comments: List, limit: int = 10) -> List[Dict]:
        """Extract top comments with metadata"""
        top_comments = []

        # Sort by score
        sorted_comments = sorted(comments, key=lambda c: c.score, reverse=True)[:limit]

        for comment in sorted_comments:
            if hasattr(comment, 'body'):  # Ensure it's a real comment
                top_comments.append({
                    "id": comment.id,
                    "author": str(comment.author) if comment.author else "[deleted]",
                    "author_flair": comment.author_flair_text,
                    "body": comment.body,
                    "score": comment.score,
                    "created_utc": int(comment.created_utc),
                    "created_date": datetime.fromtimestamp(comment.created_utc).isoformat(),
                    "is_submitter": comment.is_submitter,
                    "permalink": f"https://reddit.com{comment.permalink}"
                })

        return top_comments

    def save_to_cache(self, discussions: List[Dict], filename: str) -> Path:
        """Save scraped discussions to JSON cache"""
        cache_file = self.cache_dir / f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump({
                "metadata": {
                    "scraped_at": datetime.now().isoformat(),
                    "total_discussions": len(discussions),
                    "source": "reddit_praw_official"
                },
                "discussions": discussions
            }, f, indent=2, ensure_ascii=False)

        self.logger.info(f"💾 Saved {len(discussions)} discussions to {cache_file}")
        return cache_file

    def load_from_cache(self, cache_file: Path) -> List[Dict]:
        """Load discussions from cache file"""
        with open(cache_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.logger.info(f"📂 Loaded {len(data['discussions'])} discussions from cache")
        return data['discussions']

    def validate_url_accessibility(self, url: str) -> bool:
        """Validate that Reddit post URL is still accessible"""
        try:
            submission = self.reddit.submission(url=url)
            return not submission.removed_by_category  # Returns None if not removed
        except Exception as e:
            self.logger.warning(f"⚠️ URL validation failed for {url}: {e}")
            return False


if __name__ == "__main__":
    # Example usage (requires .env with Reddit credentials)
    logging.basicConfig(level=logging.INFO)

    scraper = RedditScraper()

    # Scrape LED lighting discussions
    discussions = scraper.scrape(
        query="LED strip lighting",
        subreddits=["electricians", "homeimprovement", "DIY"],
        limit=30
    )

    # Save to cache
    scraper.save_to_cache(discussions, "led_lighting_discussions")

    print(f"✅ Scraped {len(discussions)} real Reddit discussions")
    print(f"📊 Example discussion: {discussions[0]['title']}")
    print(f"🔗 URL: {discussions[0]['url']}")
