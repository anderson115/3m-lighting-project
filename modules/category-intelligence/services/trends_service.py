"""
Google Trends Service - Real Keyword Data

Fetches actual trending keyword data using pytrends (no API key required).
Provides consumer search behavior insights.
"""

import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

try:
    from pytrends.request import TrendReq
    PYTRENDS_AVAILABLE = True
except ImportError:
    PYTRENDS_AVAILABLE = False
    logger.warning("pytrends not installed - keyword trending unavailable")


class TrendsService:
    """
    Service for accessing Google Trends data.

    No API key required - uses pytrends library.
    Rate limits apply - use responsibly.
    """

    def __init__(self):
        if not PYTRENDS_AVAILABLE:
            raise ImportError("pytrends library required: pip install pytrends")

        self.pytrends = TrendReq(hl='en-US', tz=360)

    def get_related_keywords(self, category: str, limit: int = 25) -> Dict[str, Any]:
        """
        Get related keywords for a category from Google Trends.

        Args:
            category: Main category keyword
            limit: Maximum keywords to return

        Returns:
            Dict with consumer and industry keywords
        """
        try:
            # Build payload
            self.pytrends.build_payload(
                [category],
                cat=0,
                timeframe='today 12-m',
                geo='US',
                gprop=''
            )

            # Get related queries
            related_queries = self.pytrends.related_queries()

            consumer_keywords = []
            rising_keywords = []

            if category in related_queries:
                # Top related queries (consumer language)
                if 'top' in related_queries[category] and related_queries[category]['top'] is not None:
                    top_df = related_queries[category]['top']
                    consumer_keywords = top_df['query'].head(limit).tolist()

                # Rising queries (emerging trends)
                if 'rising' in related_queries[category] and related_queries[category]['rising'] is not None:
                    rising_df = related_queries[category]['rising']
                    rising_keywords = rising_df['query'].head(10).tolist()

            # Get interest over time
            interest_df = self.pytrends.interest_over_time()
            trend_direction = "stable"

            if not interest_df.empty and category in interest_df.columns:
                recent_avg = interest_df[category].tail(4).mean()
                older_avg = interest_df[category].head(4).mean()

                if recent_avg > older_avg * 1.1:
                    trend_direction = "rising"
                elif recent_avg < older_avg * 0.9:
                    trend_direction = "declining"

            return {
                'consumer_language': consumer_keywords[:limit],
                'rising_keywords': rising_keywords,
                'trend_direction': trend_direction,
                'source_urls': [
                    'https://trends.google.com/trends/'
                ],
                'collected_at': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error fetching trends for '{category}': {e}")
            return {
                'consumer_language': [],
                'rising_keywords': [],
                'trend_direction': 'unknown',
                'source_urls': [],
                'error': str(e)
            }

    def get_regional_interest(self, category: str) -> List[Dict[str, Any]]:
        """
        Get regional interest data for a category.

        Args:
            category: Category keyword

        Returns:
            List of regions with interest scores
        """
        try:
            self.pytrends.build_payload(
                [category],
                cat=0,
                timeframe='today 12-m',
                geo='US'
            )

            # Get interest by region
            region_df = self.pytrends.interest_by_region(
                resolution='COUNTRY',
                inc_low_vol=True,
                inc_geo_code=False
            )

            regions = []
            if not region_df.empty and category in region_df.columns:
                top_regions = region_df[category].nlargest(10)

                for region_name, score in top_regions.items():
                    if score > 0:
                        regions.append({
                            'region': region_name,
                            'interest_score': int(score),
                            'relative_popularity': 'high' if score > 75 else 'medium' if score > 50 else 'low'
                        })

            return regions

        except Exception as e:
            logger.error(f"Error fetching regional interest: {e}")
            return []

    def get_search_terms(self, category: str) -> List[str]:
        """
        Get actual consumer search terms for a category.

        Args:
            category: Category name

        Returns:
            List of search terms people actually use
        """
        result = self.get_related_keywords(category, limit=30)
        return result.get('consumer_language', [])


# Global instance
_trends_service = None


def get_trends_service() -> TrendsService:
    """Get or create Trends service instance."""
    global _trends_service

    if not PYTRENDS_AVAILABLE:
        raise ImportError("pytrends not available - install with: pip install pytrends")

    if _trends_service is None:
        _trends_service = TrendsService()

    return _trends_service
