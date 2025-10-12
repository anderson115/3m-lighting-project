"""
Main orchestrator for Creator Intelligence Module.
Coordinates multi-platform data collection, LLM analysis, and database storage.
"""

import logging
from pathlib import Path
from typing import List, Dict, Optional
import sys

# Add parent directory to path for imports
module_root = Path(__file__).parent.parent
sys.path.insert(0, str(module_root))

from core.config import config
from core.database import CreatorDatabase
from scrapers.youtube_scraper import YouTubeScraper
from scrapers.instagram_scraper import InstagramScraper
from scrapers.tiktok_scraper import TikTokScraper, sync_search_users as tiktok_sync_search
from scrapers.pinterest_scraper import PinterestScraper, sync_search_and_capture
from analyzers.content_classifier import ContentClassifier
from analyzers.creator_scorer import CreatorScorer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CreatorIntelligenceOrchestrator:
    """
    Main orchestrator for Creator Intelligence Module.
    Manages end-to-end pipeline: scraping → classification → scoring → database storage.
    """

    def __init__(self, config_override: Optional[Dict] = None):
        """
        Initialize orchestrator.

        Args:
            config_override: Optional config overrides
        """
        self.config = config
        if config_override:
            for key, value in config_override.items():
                setattr(self.config, key, value)

        # Validate config
        if not self.config.validate():
            raise ValueError("Configuration validation failed")

        # Initialize components
        self.db = CreatorDatabase(self.config.database_path)
        self.classifier = ContentClassifier(
            api_key=self.config.get_llm_api_key(),
            model=self.config.llm_model
        )
        self.scorer = CreatorScorer()

        # Initialize scrapers
        self.scrapers = {}
        if self.config.enable_youtube:
            self.scrapers['youtube'] = YouTubeScraper(
                api_key=self.config.youtube_api_key,
                cache_dir=self.config.youtube_cache
            )

        if self.config.enable_instagram:
            self.scrapers['instagram'] = InstagramScraper(
                cache_dir=self.config.instagram_cache,
                rate_limit_seconds=self.config.instagram_rate_limit
            )

        if self.config.enable_tiktok:
            # TikTok uses sync wrappers due to async architecture
            pass

        # Pinterest support - uses sync wrappers (no config attribute yet)
        # if self.config.enable_pinterest:
        #     pass

        logger.info(f"✅ CreatorIntelligenceOrchestrator initialized with {len(self.scrapers)} scrapers")

    def analyze_creators(
        self,
        keywords: List[str],
        platforms: List[str] = None,
        limit_per_platform: int = 10
    ) -> Dict:
        """
        Full pipeline: search creators → analyze content → score → save to database.

        Args:
            keywords: Search keywords (e.g., ["LED lighting", "home lighting"])
            platforms: Platforms to search (default: all enabled)
            limit_per_platform: Max creators per platform

        Returns:
            Summary statistics
        """
        if platforms is None:
            platforms = list(self.scrapers.keys())
            if self.config.enable_tiktok and 'tiktok' not in platforms:
                platforms.append('tiktok')
            # if self.config.enable_pinterest and 'pinterest' not in platforms:
            #     platforms.append('pinterest')

        logger.info(f"🚀 Starting creator analysis")
        logger.info(f"   Keywords: {keywords}")
        logger.info(f"   Platforms: {platforms}")
        logger.info(f"   Limit: {limit_per_platform} per platform")

        all_creators = []

        # Step 1: Search creators on each platform
        for platform in platforms:
            for keyword in keywords:
                logger.info(f"\n📍 Searching {platform} for '{keyword}'")

                creators = self._search_platform(platform, keyword, limit_per_platform)
                logger.info(f"   Found {len(creators)} creators on {platform}")

                all_creators.extend(creators)

        logger.info(f"\n✅ Total creators found: {len(all_creators)}")

        # Step 2: Get content for each creator and classify
        creators_with_content = []
        failed_creators = []

        for i, creator in enumerate(all_creators):
            try:
                logger.info(f"\n📥 Processing creator {i+1}/{len(all_creators)}: {creator['username']} ({creator['platform']})")

                # Get creator content
                contents = self._get_creator_content(creator, limit=20)
                logger.info(f"   Retrieved {len(contents)} pieces of content")

                if not contents:
                    logger.warning(f"   Skipping {creator['username']} - no content found")
                    continue

                # Classify content
                logger.info(f"   Classifying content...")
                classified_contents = self.classifier.classify_batch(contents)

                # Add creator_id to contents (will be updated after DB insert)
                for content, classification in zip(contents, classified_contents):
                    content.update(classification)

                creators_with_content.append((creator, contents))

            except Exception as e:
                logger.error(f"   ❌ Failed processing {creator['username']}: {e}")
                failed_creators.append((creator, str(e)))
                continue  # Continue with remaining creators

        logger.info(f"\n✅ Successfully processed {len(creators_with_content)} creators")
        if failed_creators:
            logger.warning(f"⚠️  Failed processing {len(failed_creators)} creators - see logs above")

        # Step 3: Score creators
        logger.info(f"\n📊 Scoring creators...")
        scored_creators = self.scorer.score_batch(creators_with_content)

        # Step 4: Save to database
        logger.info(f"\n💾 Saving to database...")
        saved_count = 0

        for (creator, contents), scores in zip(creators_with_content, scored_creators):
            # Update creator with scores
            creator.update({
                'research_viability_score': scores['research_viability_score'],
                'partnership_viability_score': scores['partnership_viability_score'],
                'classification': self._get_overall_classification(contents)
            })

            # Save creator
            creator_id = self.db.upsert_creator(creator)
            saved_count += 1

            # Save content
            for content in contents:
                content['creator_id'] = creator_id
                self.db.upsert_content(content)

                # Extract and save consumer language
                for phrase in content.get('consumer_language', []):
                    if phrase:
                        self.db.add_consumer_language(
                            phrase=phrase,
                            category='consumer_language',
                            platform=creator['platform'],
                            context=content.get('description', '')[:200]
                        )

                # Extract and save pain points
                for pain_point in content.get('pain_points', []):
                    if pain_point:
                        self.db.add_consumer_language(
                            phrase=pain_point,
                            category='pain_point',
                            platform=creator['platform'],
                            context=content.get('description', '')[:200]
                        )

        logger.info(f"✅ Saved {saved_count} creators to database")

        # Generate summary stats
        stats = self.db.get_stats()

        logger.info(f"\n" + "=" * 80)
        logger.info(f"📊 ANALYSIS COMPLETE")
        logger.info(f"=" * 80)
        logger.info(f"Creators by platform: {stats['creators_by_platform']}")
        logger.info(f"Content by platform: {stats['content_by_platform']}")
        logger.info(f"Total language phrases: {stats['total_language_phrases']}")
        logger.info(f"Classification breakdown: {stats['classification_breakdown']}")

        return {
            'total_creators_analyzed': saved_count,
            'failed_creators_count': len(failed_creators),
            'success_rate': f"{(saved_count / len(all_creators) * 100):.1f}%" if all_creators else "0%",
            'database_stats': stats,
            'llm_tokens_used': self.classifier.total_tokens_used
        }

    def _search_platform(self, platform: str, keyword: str, limit: int) -> List[Dict]:
        """Search a platform for creators."""
        try:
            if platform == 'youtube' and 'youtube' in self.scrapers:
                return self.scrapers['youtube'].search_channels(keyword, limit=limit)

            elif platform == 'instagram' and 'instagram' in self.scrapers:
                return self.scrapers['instagram'].search_users(keyword, limit=limit)

            elif platform == 'tiktok' and self.config.enable_tiktok:
                return tiktok_sync_search(
                    cache_dir=self.config.tiktok_cache,
                    query=keyword,
                    limit=limit,
                    rate_limit=self.config.tiktok_rate_limit
                )

            # elif platform == 'pinterest' and self.config.enable_pinterest:
            #     # Pinterest returns pin data, not creators
            #     # Extract unique creators from pins
            #     result = sync_search_and_capture(
            #         cache_dir=self.config.cache_dir / 'pinterest',
            #         screenshot_dir=self.config.module_root / 'data' / 'screenshots' / 'pinterest',
            #         query=keyword,
            #         limit=limit
            #     )
            #
            #     # Convert pins to creator format (unique board owners)
            #     creators_map = {}
            #     for pin in result.get('pins', []):
            #         # Pinterest doesn't give us creator info easily
            #         # Just log that we captured visual data
            #         pass
            #
            #     logger.info(f"   Captured {len(result.get('pins', []))} Pinterest pins (visual data)")
            #     return []  # Pinterest is visual-only, no structured creator data

            else:
                logger.warning(f"   Platform {platform} not enabled or not supported")
                return []

        except Exception as e:
            logger.error(f"   Failed to search {platform}: {e}")
            return []

    def _get_creator_content(self, creator: Dict, limit: int = 20) -> List[Dict]:
        """Get content from a creator."""
        platform = creator['platform']

        try:
            if platform == 'youtube' and 'youtube' in self.scrapers:
                channel_id = creator['metadata']['channel_id']
                return self.scrapers['youtube'].get_channel_videos(channel_id, limit=limit)

            elif platform == 'instagram' and 'instagram' in self.scrapers:
                return self.scrapers['instagram'].get_user_medias(creator['username'], limit=limit)

            elif platform == 'tiktok':
                # Use sync wrapper
                from scrapers.tiktok_scraper import sync_get_user_videos
                return sync_get_user_videos(
                    cache_dir=self.config.tiktok_cache,
                    username=creator['username'],
                    limit=limit,
                    rate_limit=self.config.tiktok_rate_limit
                )

            else:
                return []

        except Exception as e:
            logger.error(f"   Failed to get content for {creator['username']}: {e}")
            return []

    def _get_overall_classification(self, contents: List[Dict]) -> str:
        """Determine overall creator classification from content."""
        if not contents:
            return 'not_relevant'

        highly_relevant = sum(1 for c in contents if c.get('classification') == 'highly_relevant')
        relevant = sum(1 for c in contents if c.get('classification') == 'relevant')

        if highly_relevant >= len(contents) * 0.7:
            return 'highly_relevant'
        elif (highly_relevant + relevant) >= len(contents) * 0.5:
            return 'relevant'
        elif relevant > 0:
            return 'tangentially_relevant'
        else:
            return 'not_relevant'

    def get_top_creators(self, score_type: str = 'research', limit: int = 20) -> List[Dict]:
        """Get top creators by score."""
        return self.db.get_creators_by_score(score_type=score_type, min_score=0, limit=limit)

    def get_consumer_language_dictionary(self, category: str = None, min_frequency: int = 2) -> List[Dict]:
        """Get consumer language dictionary."""
        return self.db.get_consumer_language_by_category(category=category, min_frequency=min_frequency)

    def close(self):
        """Close database connection."""
        self.db.close()


if __name__ == "__main__":
    # Example usage
    orchestrator = CreatorIntelligenceOrchestrator()

    # Run analysis
    results = orchestrator.analyze_creators(
        keywords=["LED lighting tutorial"],
        platforms=["youtube"],
        limit_per_platform=5
    )

    print(f"\nResults: {results}")

    # Get top research candidates
    top_research = orchestrator.get_top_creators(score_type='research', limit=10)
    print(f"\nTop 10 research candidates:")
    for i, creator in enumerate(top_research):
        print(f"{i+1}. {creator.get('display_name')} (@{creator.get('username')}) - Score: {creator.get('research_viability_score')}")

    orchestrator.close()
