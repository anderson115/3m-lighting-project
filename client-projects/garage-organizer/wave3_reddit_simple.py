#!/usr/bin/env python3
"""
Wave 3 Reddit Collector - Using Public JSON API (no PRAW needed)
Collect 376 new posts using Reddit's public .json endpoints
"""

import requests
import json
import time
from datetime import datetime
import os

class SimpleRedditCollector:
    def __init__(self):
        self.wave = "wave_3"
        self.collection_date = datetime.now().strftime("%Y-%m-%d")
        self.target_new_posts = 376
        self.collected_posts = []

        # Load existing URLs to avoid duplicates
        self.existing_urls = set()
        consolidated_path = '/Users/anderson115/00-interlink/12-work/3m-lighting-project/client-projects/garage-organizer/01-raw-data/reddit_consolidated.json'
        if os.path.exists(consolidated_path):
            with open(consolidated_path, 'r') as f:
                data = json.load(f)
                for post in data:
                    if 'post_url' in post:
                        self.existing_urls.add(post['post_url'])

        print(f"✅ Loaded {len(self.existing_urls)} existing Reddit URLs")

        self.subreddits = [
            'HomeImprovement',
            'DIY',
            'organization',
            'CleaningTips',
            'Renters',
            'ApartmentLiving',
            'homeowners',
            'interiordecorating',
            'DesignMyRoom',
            'declutter',
            'HomeDecorating',
            'Apartments',
            'SmallSpace',
            'OrganizationPorn'
        ]

        self.search_terms = [
            'command hooks',
            '3m hooks',
            'wall hooks',
            'garage organization',
            'damage free hanging',
            'adhesive hooks',
            'removable hooks',
            'wall damage hooks',
            'command strips',
            'hanging without nails',
            'rental friendly hooks',
            'temporary hooks'
        ]

    def collect(self):
        print(f"\n🎯 WAVE 3 REDDIT COLLECTION")
        print(f"Target: {self.target_new_posts} new posts\n")

        headers = {'User-Agent': 'GarageOrganizerResearch/1.0'}
        collected = 0

        for subreddit in self.subreddits:
            if collected >= self.target_new_posts:
                break

            print(f"\n📍 r/{subreddit}")

            for search_term in self.search_terms:
                if collected >= self.target_new_posts:
                    break

                try:
                    # Reddit public JSON API
                    url = f"https://www.reddit.com/r/{subreddit}/search.json"
                    params = {
                        'q': search_term,
                        't': 'all',  # All time
                        'limit': 100,
                        'restrict_sr': 1,
                        'sort': 'relevance'
                    }

                    response = requests.get(url, headers=headers, params=params, timeout=10)

                    if response.status_code != 200:
                        print(f"  ⚠️  API error {response.status_code}")
                        time.sleep(5)
                        continue

                    data = response.json()

                    for post in data.get('data', {}).get('children', []):
                        if collected >= self.target_new_posts:
                            break

                        post_data = post['data']
                        post_url = f"https://www.reddit.com{post_data['permalink']}"

                        # Skip if already collected
                        if post_url in self.existing_urls:
                            continue

                        # Quality filters
                        if post_data.get('score', 0) < 3:
                            continue

                        if len(post_data.get('selftext', '')) < 20:
                            continue

                        # Build record
                        record = {
                            'platform': 'reddit',
                            'collection_wave': self.wave,
                            'collection_date': self.collection_date,
                            'collection_method': 'public_json_api',

                            'post_id': post_data['id'],
                            'post_url': post_url,
                            'title': post_data['title'],
                            'post_text': post_data['selftext'],
                            'author': post_data['author'],
                            'subreddit': post_data['subreddit'],
                            'score': post_data['score'],
                            'num_comments': post_data['num_comments'],
                            'created_utc': post_data['created_utc'],
                            'created_date': datetime.fromtimestamp(post_data['created_utc']).isoformat(),

                            'search_term': search_term
                        }

                        self.collected_posts.append(record)
                        self.existing_urls.add(post_url)
                        collected += 1

                        print(f"  ✓ {collected}/{self.target_new_posts}")

                    # Reddit rate limit: 1 request/second
                    time.sleep(2)

                except Exception as e:
                    print(f"  ⚠️  Error: {e}")
                    time.sleep(5)
                    continue

        print(f"\n✅ Collection complete: {collected} new posts")
        return self.collected_posts

    def save(self):
        output_file = '/Volumes/DATA/garage-organizer-wave3/raw-data/reddit_wave3.json'
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(self.collected_posts, f, indent=2)

        print(f"\n💾 Saved to: {output_file}")
        print(f"   Records: {len(self.collected_posts)}")

if __name__ == "__main__":
    collector = SimpleRedditCollector()
    posts = collector.collect()

    if posts:
        collector.save()
        print(f"\n🎉 Wave 3 Reddit complete: {len(posts)} posts")
