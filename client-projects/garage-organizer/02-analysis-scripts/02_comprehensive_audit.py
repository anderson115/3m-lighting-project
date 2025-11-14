#!/usr/bin/env python3
"""
Comprehensive Quality Audit for Reddit Data
Audits 10% random sample (150 posts from 1500) for:
- Duplication rate
- Relevancy quality
- Content quality
- Author diversity
"""

import json
import random
from typing import Dict, List, Tuple
from collections import Counter

class ComprehensiveAuditor:
    def __init__(self, data_file: str, sample_percent: float = 0.10):
        with open(data_file, 'r') as f:
            self.data = json.load(f)
        self.posts = self.data['posts']
        self.sample_size = int(len(self.posts) * sample_percent)

    def audit(self) -> Dict:
        """Run comprehensive audit"""
        print(f"\n📊 COMPREHENSIVE QUALITY AUDIT")
        print(f"   Total posts: {len(self.posts)}")
        print(f"   Sample size: {self.sample_size} posts ({int(self.sample_size/len(self.posts)*100)}%)")
        print(f"   Sample selection: Random\n")

        # Select random sample
        random.seed(12345)  # Different seed for different sample than Gate 1
        sample_indices = random.sample(range(len(self.posts)), self.sample_size)
        sample_posts = [self.posts[i] for i in sample_indices]

        # Run all audits
        dup_rate = self._audit_duplication(sample_posts)
        rel_rate = self._audit_relevancy(sample_posts)
        author_div = self._audit_author_diversity(sample_posts)
        content_qual = self._audit_content_quality(sample_posts)

        # Calculate overall quality score
        overall = (dup_rate + rel_rate + author_div + content_qual) / 4

        print(f"\n{'='*60}")
        print(f"OVERALL QUALITY SCORE: {overall:.1f}%")
        print(f"{'='*60}\n")

        return {
            "sample_size": self.sample_size,
            "duplication_quality": dup_rate,
            "relevancy_quality": rel_rate,
            "author_diversity": author_div,
            "content_quality": content_qual,
            "overall_quality": overall
        }

    def _audit_duplication(self, posts: List[Dict]) -> float:
        """Audit for duplicate text content"""
        print("🔍 1. DUPLICATION AUDIT")

        text_contents = [p['text'] for p in posts]
        unique_texts = len(set(text_contents))
        duplicate_count = len(text_contents) - unique_texts
        dup_rate = (duplicate_count / len(text_contents)) * 100

        # Quality score: Lower duplication = higher quality
        quality = max(0, 100 - (dup_rate * 10))  # Each 1% dup reduces score by 10

        print(f"   Total texts: {len(text_contents)}")
        print(f"   Unique texts: {unique_texts}")
        print(f"   Duplicates: {duplicate_count}")
        print(f"   Duplication rate: {dup_rate:.2f}%")
        print(f"   Quality score: {quality:.1f}%")

        if dup_rate < 5:
            print(f"   ✅ PASS (target: <5%)")
        else:
            print(f"   ⚠️  WARN (target: <5%)")

        return quality

    def _audit_relevancy(self, posts: List[Dict]) -> float:
        """Audit relevancy scores"""
        print(f"\n🎯 2. RELEVANCY AUDIT")

        # Count posts with relevancy scores
        scored_posts = [p for p in posts if 'relevancy_score' in p]

        if not scored_posts:
            print("   ⚠️  No relevancy scores found in sample")
            return 0

        scores = [p['relevancy_score'] for p in scored_posts if p.get('relevancy_score') is not None]
        score_counts = Counter(scores)

        avg_score = sum(scores) / len(scores)
        highly_relevant = score_counts.get(2, 0)
        marginally_relevant = score_counts.get(1, 0)
        not_relevant = score_counts.get(0, 0)

        # Quality score: Based on average relevancy (1.5+ is passing)
        quality = min(100, (avg_score / 2.0) * 100)

        print(f"   Scored posts: {len(scored_posts)}")
        print(f"   Average score: {avg_score:.2f}/2.0")
        print(f"   Score 2 (Highly Relevant): {highly_relevant} ({highly_relevant/len(scored_posts)*100:.1f}%)")
        print(f"   Score 1 (Marginally Relevant): {marginally_relevant} ({marginally_relevant/len(scored_posts)*100:.1f}%)")
        print(f"   Score 0 (Not Relevant): {not_relevant} ({not_relevant/len(scored_posts)*100:.1f}%)")
        print(f"   Quality score: {quality:.1f}%")

        if avg_score >= 1.5:
            print(f"   ✅ PASS (target: ≥1.5)")
        else:
            print(f"   ⚠️  WARN (target: ≥1.5)")

        return quality

    def _audit_author_diversity(self, posts: List[Dict]) -> float:
        """Audit author name diversity"""
        print(f"\n👥 3. AUTHOR DIVERSITY AUDIT")

        authors = [p['author'] for p in posts]
        unique_authors = len(set(authors))
        diversity_rate = (unique_authors / len(authors)) * 100

        # Quality score: Higher diversity = higher quality
        quality = min(100, diversity_rate * 4)  # 25%+ unique = 100%

        print(f"   Total posts: {len(authors)}")
        print(f"   Unique authors: {unique_authors}")
        print(f"   Diversity rate: {diversity_rate:.1f}%")
        print(f"   Quality score: {quality:.1f}%")

        if diversity_rate >= 20:
            print(f"   ✅ PASS (target: ≥20%)")
        else:
            print(f"   ⚠️  WARN (target: ≥20%)")

        return quality

    def _audit_content_quality(self, posts: List[Dict]) -> float:
        """Audit content quality metrics"""
        print(f"\n📝 4. CONTENT QUALITY AUDIT")

        # Check for minimum text length
        too_short = sum(1 for p in posts if len(p['text']) < 100)
        too_short_rate = (too_short / len(posts)) * 100

        # Check for complete metadata
        missing_metadata = sum(1 for p in posts if not all([
            p.get('title'),
            p.get('text'),
            p.get('author'),
            p.get('post_id'),
            p.get('url')
        ]))
        missing_rate = (missing_metadata / len(posts)) * 100

        # Quality score: Low issues = high quality
        quality = max(0, 100 - (too_short_rate * 5) - (missing_rate * 10))

        print(f"   Too short (<100 chars): {too_short} ({too_short_rate:.1f}%)")
        print(f"   Missing metadata: {missing_metadata} ({missing_rate:.1f}%)")
        print(f"   Quality score: {quality:.1f}%")

        if too_short_rate < 5 and missing_rate == 0:
            print(f"   ✅ PASS")
        else:
            print(f"   ⚠️  WARN")

        return quality

def main():
    data_file = "/Users/anderson115/00-interlink/12-work/3m-lighting-project/client-projects/garage-organizer/01-raw-data/reddit_posts_raw.json"

    auditor = ComprehensiveAuditor(data_file, sample_percent=0.10)
    results = auditor.audit()

    return results['overall_quality'] >= 85.0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
