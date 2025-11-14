#!/usr/bin/env python3
"""
WAVE 3 REDDIT COLLECTOR
Collect 376 new Reddit posts with wave_3 flags
Target: 33% increase from existing 1,129 posts
"""

import praw
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict
import time

class Wave3RedditCollector:
    def __init__(self):
        self.wave = "wave_3"
        self.collection_date = datetime.now().strftime("%Y-%m-%d")
        self.target_new_posts = 376
        self.collected_posts = []

        # Load existing URLs to avoid duplicates
        self.existing_urls = self._load_existing_urls()

        # Reddit configuration
        self.subreddits = [
            'HomeImprovement',
            'DIY',
            'organization',
            'GarageStorage',
            'CleaningTips',
            'Renters',
            'ApartmentLiving',
            'homeowners',
            'fixit'
        ]

        self.keywords = [
            'command hooks',
            'command strips',
            '3m hooks',
            '3m command',
            'command hooks failed',
            'command hooks fell',
            'garage organization hooks',
            'pegboard alternative',
            'gorilla hooks',
            'monkey hooks',
            'wall hooks rental'
        ]

    def _load_existing_urls(self) -> set:
        """Load existing Reddit URLs to avoid duplicates"""
        existing = set()
        consolidated_file = '01-raw-data/reddit_consolidated.json'

        if os.path.exists(consolidated_file):
            with open(consolidated_file, 'r') as f:
                data = json.load(f)
                for post in data:
                    if 'post_url' in post:
                        existing.add(post['post_url'])

        print(f"✅ Loaded {len(existing)} existing Reddit URLs")
        return existing

    def _init_reddit(self):
        """Initialize Reddit API client"""
        # Try to use PRAW with credentials
        try:
            reddit = praw.Reddit(
                client_id=os.getenv('REDDIT_CLIENT_ID'),
                client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                user_agent='GarageOrganizerResearch/1.0'
            )
            print("✅ Reddit API authenticated")
            return reddit
        except Exception as e:
            print(f"❌ Reddit API authentication failed: {e}")
            print("⚠️  Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET environment variables")
            return None

    def collect(self):
        """Collect wave 3 Reddit posts"""
        reddit = self._init_reddit()
        if not reddit:
            print("❌ Cannot proceed without Reddit API credentials")
            return

        print(f"\n🎯 WAVE 3 REDDIT COLLECTION")
        print(f"Target: {self.target_new_posts} new posts")
        print(f"Avoiding {len(self.existing_urls)} existing posts\n")

        collected = 0
        attempts = 0

        for subreddit_name in self.subreddits:
            if collected >= self.target_new_posts:
                break

            print(f"\n📍 Searching r/{subreddit_name}...")
            subreddit = reddit.subreddit(subreddit_name)

            # Search each keyword
            for keyword in self.keywords:
                if collected >= self.target_new_posts:
                    break

                try:
                    # Search recent posts (last 90 days)
                    time_filter = 'month'  # Recent posts
                    results = subreddit.search(keyword, time_filter=time_filter, limit=50)

                    for submission in results:
                        attempts += 1

                        # Skip if already collected
                        post_url = f"https://www.reddit.com{submission.permalink}"
                        if post_url in self.existing_urls:
                            continue

                        # Quality filters
                        if submission.score < 3:  # At least 3 upvotes
                            continue

                        if len(submission.selftext) < 20:  # Substantial content
                            continue

                        # Build post data
                        post_data = {
                            'platform': 'reddit',
                            'collection_wave': self.wave,
                            'collection_date': self.collection_date,
                            'collection_method': 'automated_praw',

                            'post_id': submission.id,
                            'post_url': post_url,
                            'title': submission.title,
                            'post_text': submission.selftext,
                            'author': str(submission.author),
                            'subreddit': submission.subreddit.display_name,
                            'score': submission.score,
                            'num_comments': submission.num_comments,
                            'created_utc': submission.created_utc,
                            'created_date': datetime.fromtimestamp(submission.created_utc).isoformat(),

                            'search_keyword': keyword,
                            'gilded': submission.gilded,
                            'is_self': submission.is_self,
                            'over_18': submission.over_18,
                            'spoiler': submission.spoiler
                        }

                        # Collect top comments (up to 10)
                        submission.comments.replace_more(limit=0)
                        comments = []
                        for comment in submission.comments[:10]:
                            if hasattr(comment, 'body'):
                                comments.append({
                                    'comment_id': comment.id,
                                    'author': str(comment.author),
                                    'body': comment.body,
                                    'score': comment.score,
                                    'created_utc': comment.created_utc
                                })

                        post_data['comments'] = comments

                        self.collected_posts.append(post_data)
                        self.existing_urls.add(post_url)
                        collected += 1

                        print(f"  ✓ Collected: {collected}/{self.target_new_posts} (r/{submission.subreddit.display_name})")

                        if collected >= self.target_new_posts:
                            break

                        # Rate limiting
                        time.sleep(2)

                except Exception as e:
                    print(f"  ⚠️  Error searching '{keyword}': {e}")
                    continue

        print(f"\n✅ Collection complete!")
        print(f"   Attempted: {attempts} posts")
        print(f"   Collected: {collected} new posts")
        print(f"   Duplicates avoided: {attempts - collected}")

        return self.collected_posts

    def save(self):
        """Save wave 3 Reddit data"""
        output_file = '/Volumes/DATA/garage-organizer-wave3/raw-data/reddit_wave3.json'
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(self.collected_posts, f, indent=2)

        print(f"\n💾 Saved to: {output_file}")
        print(f"   Records: {len(self.collected_posts)}")
        print(f"   Size: {os.path.getsize(output_file) / 1024 / 1024:.2f} MB")

        # Also save local backup
        backup_file = '02-analysis-scripts/reddit_wave3_backup.json'
        with open(backup_file, 'w') as f:
            json.dump(self.collected_posts, f, indent=2)
        print(f"   Backup: {backup_file}")

if __name__ == "__main__":
    collector = Wave3RedditCollector()
    posts = collector.collect()

    if posts:
        collector.save()
        print(f"\n🎉 Wave 3 Reddit collection complete: {len(posts)} posts")
    else:
        print("\n❌ No posts collected. Check Reddit API credentials.")
