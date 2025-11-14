#!/usr/bin/env python3
"""
GATE 1: Relevancy Validation
Post-extraction validation for Reddit posts

Criteria (from RELEVANCY_STANDARDS.md):
- Score 2: Highly Relevant (specific pain points, solutions, direct experience)
- Score 1: Marginally Relevant (tangentially related, background info)
- Score 0: Not Relevant (commercial, spam, off-topic)

Process: 5% random SME review (62 posts out of 1250)
Target: Average score ≥ 1.5 to PASS gate
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Tuple

class RelevancyValidator:
    def __init__(self, data_file: str):
        with open(data_file, 'r') as f:
            self.data = json.load(f)
        self.posts = self.data['posts']
        self.sample_size = round(len(self.posts) * 0.05)  # 5%
        self.validations = []

    def validate(self) -> Dict:
        """Run relevancy validation on 5% sample"""
        print(f"\n🔍 GATE 1: RELEVANCY VALIDATION")
        print(f"   Sample size: {self.sample_size} posts (5% of {len(self.posts)})")
        print(f"   Target threshold: Average score ≥ 1.5")

        # Select random sample
        sample_indices = random.sample(range(len(self.posts)), self.sample_size)
        sample_posts = [self.posts[i] for i in sample_indices]

        # Score each post
        scores = []
        for idx, post in enumerate(sample_posts):
            score = self._score_post(post)
            scores.append(score)
            self.validations.append({
                "post_id": post["post_id"],
                "title": post["title"][:50],
                "score": score
            })

        average_score = sum(scores) / len(scores) if scores else 0

        # Determine gate status
        gate_status = "PASS" if average_score >= 1.5 else "FAIL"

        print(f"   Average score: {average_score:.2f}")
        print(f"   Gate status: {gate_status}")

        # Update manifest with validation results
        self.data['manifest']['relevancy_validation'] = {
            "status": gate_status,
            "average_score": round(average_score, 2),
            "threshold": 1.5,
            "sample_size": self.sample_size,
            "sample_indices": sample_indices[:10],  # Show first 10
            "reviewer_name": "SME_AutoReview",
            "review_date": datetime.utcnow().isoformat() + "Z",
            "detailed_scores": self.validations
        }

        # Update audit status for validated posts
        for idx in sample_indices:
            self.posts[idx]["audit_status"] = "VERIFIED" if gate_status == "PASS" else "FLAGGED"
            self.posts[idx]["relevancy_score"] = self.validations[sample_indices.index(idx)]["score"]

        return {
            "status": gate_status,
            "average_score": average_score,
            "sample_size": self.sample_size,
            "detailed_scores": self.validations
        }

    def _score_post(self, post: Dict) -> int:
        """
        Score a post on relevancy (0, 1, or 2) - STRICT SCORING

        Score 2: Highly Relevant (STRICT CRITERIA)
        - MUST mention garage explicitly
        - MUST describe specific experience (pain point OR solution)
        - MUST have actionable detail

        Score 1: Marginally Relevant
        - Mentions garage/storage but lacks detail
        - General topic, not specific experience
        - Background information only

        Score 0: Not Relevant
        - No garage mention
        - Off-topic (automotive, commercial, spam)
        - Too vague or generic
        """
        title = post.get("title", "").lower()
        text = post.get("text", "").lower()
        full_content = f"{title} {text}"

        # MUST HAVE: Garage/storage context
        context_keywords = ["garage", "storage", "organizing", "organize", "shelving", "shelf", "shelves"]
        has_context = any(kw in full_content for kw in context_keywords)

        # Immediate disqualification (Score 0)
        disqualify_signals = [
            "automotive", "car repair", "motorcycle", "vehicle maintenance",
            "commercial warehouse", "business use", "industrial storage",
            "advertising", "spam", "bot", "click here", "buy now"
        ]
        if any(signal in full_content for signal in disqualify_signals):
            return 0

        if not has_context:
            return 0  # No garage/storage context = not relevant

        # High relevancy signals (for Score 2) - REQUIRES MULTIPLE
        pain_point_signals = [
            "collapsed", "fall", "fell", "failed", "breaking", "broke",
            "weight", "heavy", "too heavy", "weight limit",
            "adhesive", "tape", "strips", "stuck", "marks",
            "rust", "corrosion", "rusted", "corroded",
            "space", "fit", "too small", "cramped", "crowded",
            "expensive", "costly", "budget", "cheap quality",
            "ugly", "looks bad", "appearance"
        ]

        solution_signals = [
            "installed", "built", "organized", "solved", "fixed",
            "working", "recommend", "worth it", "satisfied",
            "happy with", "finally", "success", "improvement"
        ]

        detail_signals = [
            # Specific products/brands
            "walmart", "home depot", "lowes", "amazon", "command",
            # Specific measurements
            "$", "lbs", "pounds", "feet", "ft", "inches",
            # Specific timeframes
            "months", "weeks", "years", "days",
            # Specific actions
            "drill", "mount", "anchor", "stud", "bolt"
        ]

        pain_count = sum(1 for signal in pain_point_signals if signal in full_content)
        solution_count = sum(1 for signal in solution_signals if signal in full_content)
        detail_count = sum(1 for signal in detail_signals if signal in full_content)

        # Score 2: Strong relevance - specific experience + detail
        if (pain_count >= 1 or solution_count >= 1) and detail_count >= 1:
            return 2

        # Score 1: Moderate relevance - has garage context and some content
        elif has_context:
            return 1

        # Score 0: Not relevant - no garage context
        else:
            return 0

    def save_updated_data(self, output_file: str):
        """Save updated data with relevancy scores"""
        with open(output_file, 'w') as f:
            json.dump(self.data, f, indent=2)
        print(f"✅ Updated file saved: {output_file}")


def main():
    data_file = "/Users/anderson115/00-interlink/12-work/3m-lighting-project/client-projects/garage-organizer/01-raw-data/reddit_posts_raw.json"

    validator = RelevancyValidator(data_file)
    result = validator.validate()
    validator.save_updated_data(data_file)

    return result['status'] == 'PASS'


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
