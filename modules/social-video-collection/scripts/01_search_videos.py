#!/usr/bin/env python3
"""
Step 1: Search and Collect Video Metadata

Uses Apify TikTok scraper to find videos matching search criteria.
Outputs: video URLs, metadata, engagement stats (NO video download yet)
"""

import os
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from apify_client import ApifyClient

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TikTokVideoSearcher:
    """Search TikTok for videos matching category/keywords"""

    def __init__(self, config_path: Path):
        self.config = self._load_config(config_path)

        # Get Apify token from environment
        self.apify_token = os.getenv('APIFY_TOKEN')
        if not self.apify_token:
            raise ValueError(
                "APIFY_TOKEN not set. Run with: "
                "op run --env-file=../../.env.template -- python 01_search_videos.py"
            )

        self.client = ApifyClient(self.apify_token)

        # Setup output directory
        self.output_dir = Path(self.config['output']['base_dir'])
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _load_config(self, config_path: Path) -> Dict:
        """Load YAML configuration"""
        with open(config_path) as f:
            return yaml.safe_load(f)

    def build_search_queries(self) -> List[str]:
        """
        Build optimized TikTok search queries from config

        Strategy: Combine keywords + emotional triggers for problem-focused content
        """
        queries = []

        keywords = self.config['search_strategy']['keywords']
        hashtags = self.config['search_strategy'].get('hashtags', [])

        # Add direct keywords
        queries.extend(keywords)

        # Add hashtag searches
        for tag in hashtags[:5]:  # Limit to top 5 hashtags
            queries.append(f"#{tag}")

        print(f"Built {len(queries)} search queries")
        return queries

    def search_tiktok(self, query: str, max_results: int = 100) -> List[Dict]:
        """
        Search TikTok using Apify scraper

        Args:
            query: Search query
            max_results: Maximum videos to return

        Returns:
            List of video metadata dicts
        """
        print(f"\nSearching TikTok: '{query}'")

        # Apify actor input
        run_input = {
            "searchQueries": [query],
            "resultsPerPage": min(max_results, 20),
            "excludePinnedPosts": False,
        }

        # Run the actor
        actor_id = self.config['apify'].get(
            'actor_id',
            'clockworks/free-tiktok-scraper'
        )

        try:
            run = self.client.actor(actor_id).call(run_input=run_input)

            # Get results
            results = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                results.append(item)

            print(f"  Found {len(results)} videos")
            return results

        except Exception as e:
            print(f"  Error searching: {str(e)[:100]}")
            return []

    def filter_videos(self, videos: List[Dict]) -> List[Dict]:
        """
        Filter videos based on config criteria

        Filters:
        - Min views
        - Min likes
        - Min author followers
        - Has audio
        - Language
        - Duration
        """
        filters = self.config['filters']
        filtered = []

        for video in videos:
            # Extract metadata - Apify returns stats at top level
            views = video.get('playCount', 0)
            likes = video.get('diggCount', 0)

            # Apply engagement filters
            if views < filters.get('min_views', 0):
                continue
            if likes < filters.get('min_likes', 0):
                continue

            # Author quality filter
            author_meta = video.get('authorMeta', {})
            author_followers = author_meta.get('fans', 0)
            min_followers = filters.get('min_author_followers', 0)
            if author_followers < min_followers:
                continue

            # Duration filter - Apify returns this in videoMeta
            video_meta = video.get('videoMeta', {})
            duration = video_meta.get('duration', 0)
            if duration < filters.get('duration', {}).get('min', 0):
                continue
            if duration > filters.get('duration', {}).get('max', 999):
                continue

            filtered.append(video)

        print(f"  Filtered: {len(videos)} → {len(filtered)} videos (views≥{filters.get('min_views', 0)}, likes≥{filters.get('min_likes', 0)}, followers≥{filters.get('min_author_followers', 0)})")
        return filtered

    def score_creator_relevance(self, video: Dict) -> float:
        """
        Score video based on creator type (favor DIY/maker content)

        Returns score between 0-1, higher = better
        """
        score = 0.5  # Base score

        # DIY/maker keywords
        diy_keywords = [
            'diy', 'maker', 'build', 'handmade', 'custom', 'craft',
            'woodwork', 'workshop', 'garage', 'project', 'home improvement',
            'renovation', 'repair', 'fix', 'install', 'construction'
        ]

        # Check author bio/signature
        author_meta = video.get('authorMeta', {})
        signature = author_meta.get('signature', '').lower()
        nickname = author_meta.get('nickName', '').lower()
        username = author_meta.get('name', '').lower()

        # Check video description
        description = video.get('text', '').lower()

        # Check hashtags
        hashtags = [tag.get('name', '').lower() for tag in video.get('hashtags', [])]

        # Score based on DIY indicators
        all_text = f"{signature} {nickname} {username} {description} {' '.join(hashtags)}"

        matches = sum(1 for keyword in diy_keywords if keyword in all_text)
        if matches > 0:
            score += min(0.5, matches * 0.1)  # Up to 0.5 bonus

        return score

    def deduplicate_videos(self, videos: List[Dict]) -> List[Dict]:
        """Remove duplicate videos based on video ID"""
        seen = set()
        unique = []

        for video in videos:
            video_id = video.get('id')
            if video_id and video_id not in seen:
                seen.add(video_id)
                unique.append(video)

        print(f"Deduplicated: {len(videos)} → {len(unique)} videos")
        return unique

    def prioritize_diy_creators(self, videos: List[Dict]) -> List[Dict]:
        """Sort videos to prioritize DIY/maker creators"""
        # Score each video
        scored = [(video, self.score_creator_relevance(video)) for video in videos]

        # Sort by score (descending), then by engagement
        sorted_videos = sorted(
            scored,
            key=lambda x: (x[1], x[0].get('playCount', 0)),
            reverse=True
        )

        return [video for video, score in sorted_videos]

    def save_search_results(self, videos: List[Dict]) -> Path:
        """Save search results to JSON"""
        output_file = self.output_dir / 'search_results.json'

        output_data = {
            'metadata': {
                'collection_name': self.config.get('collection_name'),
                'category': self.config.get('category'),
                'platform': self.config.get('platform'),
                'search_date': datetime.now().isoformat(),
                'total_videos': len(videos)
            },
            'config': self.config,
            'videos': videos
        }

        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)

        print(f"\nSaved {len(videos)} videos to: {output_file}")
        return output_file

    def run_search(self, test_mode: bool = False) -> int:
        """
        Run full search workflow

        Args:
            test_mode: If True, limit to test_limit from config

        Returns:
            Number of videos found
        """
        print("="*60)
        print(f"TikTok Video Search")
        print(f"Category: {self.config.get('category')}")

        # Determine target
        if test_mode and 'test_limit' in self.config['collection_target']:
            target = self.config['collection_target']['test_limit']
            print(f"Mode: TEST (limit {target} videos)")
        else:
            target = self.config['collection_target']['min_videos']
            print(f"Mode: FULL COLLECTION (target {target} videos)")

        print("="*60)

        # Build queries
        queries = self.build_search_queries()

        # Search each query
        all_videos = []

        for query in queries:
            if len(all_videos) >= target:
                print(f"\nReached target: {len(all_videos)}/{target} videos")
                break

            results = self.search_tiktok(query, max_results=50)
            filtered = self.filter_videos(results)
            all_videos.extend(filtered)

        # Deduplicate
        unique_videos = self.deduplicate_videos(all_videos)

        # Prioritize DIY/maker creators
        print("\nPrioritizing DIY/maker creators...")
        unique_videos = self.prioritize_diy_creators(unique_videos)

        # Trim to target if in test mode
        if test_mode and len(unique_videos) > target:
            print(f"Trimming to test limit: {len(unique_videos)} → {target} videos")
            unique_videos = unique_videos[:target]

        # Save results
        self.save_search_results(unique_videos)

        print("\n" + "="*60)
        print(f"Search Complete: {len(unique_videos)} unique videos found")
        print("="*60)

        return len(unique_videos)


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Search TikTok for videos')
    parser.add_argument(
        '--config',
        type=Path,
        default=Path('config/examples/garage_organizers_tiktok.yaml'),
        help='Path to collection config YAML'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test mode: limit to test_limit from config'
    )

    args = parser.parse_args()

    if not args.config.exists():
        print(f"Error: Config file not found: {args.config}")
        sys.exit(1)

    # Run search
    searcher = TikTokVideoSearcher(args.config)
    num_videos = searcher.run_search(test_mode=args.test)

    if num_videos == 0:
        print("\nWarning: No videos found!")
        sys.exit(1)

    print(f"\nNext step: python scripts/02_download_videos.py --config {args.config}")


if __name__ == "__main__":
    main()
