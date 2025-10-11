"""
Creator viability scorer for research and partnership potential.
Calculates 0-100 scores based on engagement, authenticity, and content quality.
"""

import logging
from typing import Dict, List
import math

logger = logging.getLogger(__name__)


class CreatorScorer:
    """
    Calculates viability scores for creators.
    Two scores: Research viability (0-100) and Partnership viability (0-100).
    """

    def __init__(self):
        """Initialize creator scorer."""
        logger.info("✅ CreatorScorer initialized")

    def score_creator(self, creator: Dict, contents: List[Dict] = None) -> Dict:
        """
        Calculate viability scores for a creator.

        Args:
            creator: Creator profile dictionary
            contents: List of creator's content (optional, improves accuracy)

        Returns:
            Dictionary with research_score and partnership_score
        """
        # Calculate research viability score (0-100)
        research_score = self._calculate_research_score(creator, contents or [])

        # Calculate partnership viability score (0-100)
        partnership_score = self._calculate_partnership_score(creator, contents or [])

        logger.debug(f"Scored {creator.get('username')}: R={research_score}, P={partnership_score}")

        return {
            'username': creator.get('username'),
            'platform': creator.get('platform'),
            'research_viability_score': research_score,
            'partnership_viability_score': partnership_score,
            'scoring_breakdown': {
                'research': self._get_research_breakdown(creator, contents or []),
                'partnership': self._get_partnership_breakdown(creator, contents or [])
            }
        }

    def _calculate_research_score(self, creator: Dict, contents: List[Dict]) -> int:
        """
        Calculate research viability score (0-100).
        Good research participants: authentic, engaged audience, relevant content.
        """
        score = 0.0

        # 1. Follower count (0-25 points) - Sweet spot: 1K-100K
        followers = creator.get('follower_count', 0)
        if 1000 <= followers <= 100000:
            score += 25
        elif 500 <= followers < 1000:
            score += 20
        elif 100000 < followers <= 500000:
            score += 20
        elif followers > 500000:
            score += 10  # Too big, less personal connection
        else:
            score += 5  # Too small

        # 2. Engagement rate (0-25 points)
        engagement = creator.get('engagement_rate', 0)
        if engagement >= 5:
            score += 25
        elif engagement >= 3:
            score += 20
        elif engagement >= 1:
            score += 15
        elif engagement > 0:
            score += 10
        else:
            score += 5

        # 3. Content quality (0-25 points)
        if contents:
            avg_relevance = sum(c.get('relevance_score', 0) for c in contents) / len(contents)
            highly_relevant = sum(1 for c in contents if c.get('classification') == 'highly_relevant')

            relevance_score = avg_relevance * 15  # Up to 15 points
            highly_relevant_score = min(highly_relevant / len(contents) * 10, 10)  # Up to 10 points

            score += relevance_score + highly_relevant_score
        else:
            score += 10  # Default moderate score

        # 4. Authenticity indicators (0-25 points)
        authenticity_score = 0

        # Has bio/description
        if creator.get('bio'):
            authenticity_score += 5

        # Reasonable content count (not spam)
        content_count = creator.get('content_count', 0)
        if 10 <= content_count <= 1000:
            authenticity_score += 10
        elif content_count > 0:
            authenticity_score += 5

        # Not verified (more authentic/real person)
        if not creator.get('is_verified', False):
            authenticity_score += 5

        # Has location
        if creator.get('location'):
            authenticity_score += 5

        score += authenticity_score

        return int(max(0, min(100, score)))

    def _calculate_partnership_score(self, creator: Dict, contents: List[Dict]) -> int:
        """
        Calculate partnership viability score (0-100).
        Good partners: professional, engaged, aligned with brand.
        """
        score = 0.0

        # 1. Reach (0-30 points) - Larger following = better reach
        followers = creator.get('follower_count', 0)
        if followers >= 100000:
            score += 30
        elif followers >= 50000:
            score += 25
        elif followers >= 10000:
            score += 20
        elif followers >= 5000:
            score += 15
        elif followers >= 1000:
            score += 10
        else:
            score += 5

        # 2. Engagement (0-25 points)
        engagement = creator.get('engagement_rate', 0)
        if engagement >= 5:
            score += 25
        elif engagement >= 3:
            score += 20
        elif engagement >= 2:
            score += 15
        elif engagement >= 1:
            score += 10
        else:
            score += 5

        # 3. Content alignment (0-25 points)
        if contents:
            highly_relevant = sum(1 for c in contents if c.get('classification') == 'highly_relevant')
            relevant = sum(1 for c in contents if c.get('classification') == 'relevant')

            alignment_ratio = (highly_relevant + relevant * 0.5) / len(contents)
            score += alignment_ratio * 25
        else:
            score += 10

        # 4. Professionalism (0-20 points)
        professionalism_score = 0

        # Verified account (more professional)
        if creator.get('is_verified', False):
            professionalism_score += 5

        # Business account
        if creator.get('is_business', False):
            professionalism_score += 5

        # Has external URL (website/portfolio)
        if creator.get('metadata', {}).get('external_url') or creator.get('metadata', {}).get('bio_link'):
            professionalism_score += 5

        # Good content volume
        content_count = creator.get('content_count', 0)
        if content_count >= 50:
            professionalism_score += 5
        elif content_count >= 20:
            professionalism_score += 3

        score += professionalism_score

        return int(max(0, min(100, score)))

    def _get_research_breakdown(self, creator: Dict, contents: List[Dict]) -> Dict:
        """Get detailed breakdown of research score components."""
        followers = creator.get('follower_count', 0)
        engagement = creator.get('engagement_rate', 0)

        return {
            'follower_range': self._get_follower_range(followers),
            'engagement_tier': self._get_engagement_tier(engagement),
            'content_quality': f"{len([c for c in contents if c.get('classification') in ['highly_relevant', 'relevant']])}/{len(contents)}" if contents else "unknown",
            'authenticity': 'high' if not creator.get('is_verified') and creator.get('bio') else 'medium'
        }

    def _get_partnership_breakdown(self, creator: Dict, contents: List[Dict]) -> Dict:
        """Get detailed breakdown of partnership score components."""
        followers = creator.get('follower_count', 0)
        engagement = creator.get('engagement_rate', 0)

        return {
            'reach_tier': self._get_reach_tier(followers),
            'engagement_tier': self._get_engagement_tier(engagement),
            'content_alignment': f"{len([c for c in contents if c.get('classification') == 'highly_relevant'])}/{len(contents)}" if contents else "unknown",
            'professionalism': 'high' if creator.get('is_verified') or creator.get('is_business') else 'medium'
        }

    def _get_follower_range(self, followers: int) -> str:
        """Get follower range category."""
        if followers < 500:
            return "micro (<500)"
        elif followers < 5000:
            return "nano (500-5K)"
        elif followers < 50000:
            return "mid (5K-50K)"
        elif followers < 500000:
            return "macro (50K-500K)"
        else:
            return "mega (>500K)"

    def _get_reach_tier(self, followers: int) -> str:
        """Get reach tier."""
        if followers >= 100000:
            return "high (>100K)"
        elif followers >= 10000:
            return "medium (10K-100K)"
        else:
            return "low (<10K)"

    def _get_engagement_tier(self, engagement: float) -> str:
        """Get engagement tier."""
        if engagement >= 5:
            return "excellent (>5%)"
        elif engagement >= 3:
            return "good (3-5%)"
        elif engagement >= 1:
            return "fair (1-3%)"
        else:
            return "low (<1%)"

    def score_batch(self, creators_with_content: List[tuple]) -> List[Dict]:
        """
        Score multiple creators with their content.

        Args:
            creators_with_content: List of (creator_dict, contents_list) tuples

        Returns:
            List of scoring results
        """
        results = []
        for i, (creator, contents) in enumerate(creators_with_content):
            logger.info(f"Scoring creator {i+1}/{len(creators_with_content)}: {creator.get('username')}")
            result = self.score_creator(creator, contents)
            results.append(result)

        logger.info(f"✅ Scored {len(results)} creators")
        return results


if __name__ == "__main__":
    # Test creator scorer
    scorer = CreatorScorer()

    # Test creator
    test_creator = {
        'username': 'led_lighting_pro',
        'platform': 'youtube',
        'follower_count': 15000,
        'engagement_rate': 4.2,
        'bio': 'LED lighting tutorials and reviews',
        'is_verified': False,
        'is_business': True,
        'content_count': 85,
        'location': 'Los Angeles, CA',
        'metadata': {
            'external_url': 'https://ledlightingpro.com'
        }
    }

    # Test content
    test_contents = [
        {'classification': 'highly_relevant', 'relevance_score': 0.95},
        {'classification': 'highly_relevant', 'relevance_score': 0.90},
        {'classification': 'relevant', 'relevance_score': 0.75},
    ]

    result = scorer.score_creator(test_creator, test_contents)

    import json
    print(json.dumps(result, indent=2))
