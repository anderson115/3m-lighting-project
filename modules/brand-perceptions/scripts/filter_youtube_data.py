#!/usr/bin/env python3
"""
Filter YouTube garage data based on relevance and value criteria.
"""

import json
import re
from typing import Dict, List, Tuple
from collections import defaultdict

# Relevance keywords for garage/workshop context
GARAGE_KEYWORDS = {
    'high': ['garage', 'workshop', 'shed', 'tool storage', 'workbench', 'pegboard'],
    'medium': ['storage', 'organization', 'organize', 'declutter', 'wall mount',
               'hanging', 'hooks', 'adhesive', 'mounting'],
    'general': ['command', 'strips', 'hang', 'wall', 'stick', 'remove', 'damage-free']
}

# Value keywords for comment quality
VALUE_KEYWORDS = {
    'high': ['install', 'installation', 'problem', 'issue', 'failed', 'worked',
             'strong', 'weak', 'compared to', 'vs', 'better than', 'worse than',
             'experience', 'tried', 'tested', 'holds', 'fell', 'broke'],
    'medium': ['good', 'bad', 'great', 'terrible', 'recommend', 'like', 'love',
               'hate', 'easy', 'hard', 'useful', 'useless'],
    'low': ['thanks', 'lol', 'haha', 'first', 'nice', 'cool', 'wow']
}


def score_video_relevance(video: Dict) -> Tuple[str, List[str]]:
    """
    Score video relevance to garage/workshop context.
    Returns: (score, reasons)
    """
    title = video.get('title', '').lower()
    description = video.get('description', '').lower()
    text = f"{title} {description}"

    reasons = []

    # Check for HIGH relevance (garage-specific)
    high_matches = [kw for kw in GARAGE_KEYWORDS['high'] if kw in text]
    if high_matches:
        reasons.append(f"Garage-specific: {', '.join(high_matches)}")
        return 'HIGH', reasons

    # Check for MEDIUM relevance (general organization/product context)
    medium_matches = [kw for kw in GARAGE_KEYWORDS['medium'] if kw in text]
    if len(medium_matches) >= 3:  # Need multiple organization keywords
        reasons.append(f"Organization context: {', '.join(medium_matches[:3])}")
        return 'MEDIUM', reasons

    # LOW relevance (generic Command product content)
    general_matches = [kw for kw in GARAGE_KEYWORDS['general'] if kw in text]
    if general_matches:
        reasons.append(f"Generic product content: {', '.join(general_matches[:2])}")
    else:
        reasons.append("No relevant keywords found")

    return 'LOW', reasons


def score_comment_value(comment: Dict) -> Tuple[str, List[str]]:
    """
    Score comment value for brand perception insights.
    Returns: (score, reasons)
    """
    text = comment.get('text', '').lower()

    if len(text) < 10:  # Too short
        return 'LOW', ['Too short (< 10 chars)']

    reasons = []

    # Check for HIGH value (substantive feedback)
    high_matches = [kw for kw in VALUE_KEYWORDS['high'] if kw in text]
    if len(high_matches) >= 2:  # Multiple experience/comparison keywords
        reasons.append(f"Substantive feedback: {', '.join(high_matches[:3])}")
        return 'HIGH', reasons
    elif high_matches:
        reasons.append(f"Experience mentioned: {', '.join(high_matches)}")
        return 'MEDIUM', reasons

    # Check for MEDIUM value (general opinion)
    medium_matches = [kw for kw in VALUE_KEYWORDS['medium'] if kw in text]
    if medium_matches:
        reasons.append(f"General opinion: {', '.join(medium_matches[:2])}")
        return 'MEDIUM', reasons

    # Check for LOW value (spam/generic)
    low_matches = [kw for kw in VALUE_KEYWORDS['low'] if kw in text]
    if low_matches:
        reasons.append(f"Generic/spam: {', '.join(low_matches)}")
    else:
        reasons.append("No valuable content indicators")

    return 'LOW', reasons


def filter_dataset(data: List[Dict]) -> Dict:
    """
    Filter dataset and create multiple filtered versions.
    Returns statistics and filtered datasets.
    """
    stats = {
        'total_records': len(data),
        'videos': {'total': 0, 'high': 0, 'medium': 0, 'low': 0},
        'comments': {'total': 0, 'high': 0, 'medium': 0, 'low': 0},
        'filtered': {
            'high': {'videos': 0, 'comments': 0},
            'medium': {'videos': 0, 'comments': 0}
        },
        'removal_reasons': defaultdict(int)
    }

    high_filter = []  # HIGH relevance/value only
    medium_filter = []  # HIGH + MEDIUM

    # First, score all videos and create video lookup
    video_scores = {}
    video_lookup = {}

    for record in data:
        if record.get('type') == 'video':
            stats['videos']['total'] += 1
            video_id = record['video_id']
            score, reasons = score_video_relevance(record)

            video_scores[video_id] = score
            video_lookup[video_id] = record.copy()
            video_lookup[video_id]['_relevance_score'] = score
            video_lookup[video_id]['_relevance_reasons'] = reasons

            stats['videos'][score.lower()] += 1

    # Now process all records with video context
    for record in data:
        record_type = record.get('type')

        if record_type == 'video':
            video_id = record['video_id']
            score = video_scores[video_id]
            enriched_record = video_lookup[video_id]

            if score == 'HIGH':
                high_filter.append(enriched_record)
                medium_filter.append(enriched_record)
                stats['filtered']['high']['videos'] += 1
                stats['filtered']['medium']['videos'] += 1
            elif score == 'MEDIUM':
                medium_filter.append(enriched_record)
                stats['filtered']['medium']['videos'] += 1
                stats['removal_reasons']['Video: LOW relevance (generic)'] += 1
            else:  # LOW
                reasons = enriched_record['_relevance_reasons']
                stats['removal_reasons'][f"Video: {reasons[0]}"] += 1

        elif record_type == 'comment':
            stats['comments']['total'] += 1
            video_id = record.get('video_id')
            video_score = video_scores.get(video_id, 'LOW')

            # Only process comments from relevant videos
            if video_score in ['HIGH', 'MEDIUM']:
                comment_score, reasons = score_comment_value(record)
                stats['comments'][comment_score.lower()] += 1

                enriched_comment = record.copy()
                enriched_comment['_value_score'] = comment_score
                enriched_comment['_value_reasons'] = reasons
                enriched_comment['_video_relevance'] = video_score

                if comment_score == 'HIGH' and video_score == 'HIGH':
                    high_filter.append(enriched_comment)
                    stats['filtered']['high']['comments'] += 1

                if comment_score in ['HIGH', 'MEDIUM'] and video_score in ['HIGH', 'MEDIUM']:
                    medium_filter.append(enriched_comment)
                    stats['filtered']['medium']['comments'] += 1

                if comment_score == 'LOW':
                    stats['removal_reasons'][f"Comment: {reasons[0]}"] += 1
            else:
                stats['comments']['low'] += 1
                stats['removal_reasons']['Comment: From LOW relevance video'] += 1

    return {
        'stats': stats,
        'high_filter': high_filter,
        'medium_filter': medium_filter
    }


def main():
    """Main execution function."""
    print("Loading YouTube garage data...")

    input_file = '/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/brand-perceptions/data/collected/youtube_garage_data.json'
    output_dir = '/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/brand-perceptions/data/collected'

    with open(input_file, 'r') as f:
        data = json.load(f)

    print(f"Loaded {len(data)} records")
    print("\nFiltering dataset...")

    results = filter_dataset(data)
    stats = results['stats']

    # Save filtered datasets
    high_output = f"{output_dir}/youtube_garage_filtered_high.json"
    medium_output = f"{output_dir}/youtube_garage_filtered_medium.json"

    with open(high_output, 'w') as f:
        json.dump(results['high_filter'], f, indent=2)

    with open(medium_output, 'w') as f:
        json.dump(results['medium_filter'], f, indent=2)

    print(f"\nCreated filtered datasets:")
    print(f"  - {high_output} ({len(results['high_filter'])} records)")
    print(f"  - {medium_output} ({len(results['medium_filter'])} records)")

    # Print detailed statistics
    print("\n" + "="*80)
    print("FILTERING SUMMARY")
    print("="*80)

    print(f"\nTotal Records: {stats['total_records']}")
    print(f"  - Videos: {stats['videos']['total']}")
    print(f"  - Comments: {stats['comments']['total']}")

    print("\nVIDEO RELEVANCE SCORES:")
    print(f"  - HIGH (garage-specific): {stats['videos']['high']} ({stats['videos']['high']/stats['videos']['total']*100:.1f}%)")
    print(f"  - MEDIUM (organization): {stats['videos']['medium']} ({stats['videos']['medium']/stats['videos']['total']*100:.1f}%)")
    print(f"  - LOW (generic): {stats['videos']['low']} ({stats['videos']['low']/stats['videos']['total']*100:.1f}%)")

    print("\nCOMMENT VALUE SCORES:")
    print(f"  - HIGH (substantive): {stats['comments']['high']} ({stats['comments']['high']/stats['comments']['total']*100:.1f}%)")
    print(f"  - MEDIUM (opinion): {stats['comments']['medium']} ({stats['comments']['medium']/stats['comments']['total']*100:.1f}%)")
    print(f"  - LOW (spam/generic): {stats['comments']['low']} ({stats['comments']['low']/stats['comments']['total']*100:.1f}%)")

    print("\nFILTERED DATASETS:")
    print(f"\nHIGH Filter (garage-specific + substantive):")
    print(f"  - Videos: {stats['filtered']['high']['videos']}")
    print(f"  - Comments: {stats['filtered']['high']['comments']}")
    print(f"  - Total: {stats['filtered']['high']['videos'] + stats['filtered']['high']['comments']}")
    print(f"  - Retention: {(stats['filtered']['high']['videos'] + stats['filtered']['high']['comments'])/stats['total_records']*100:.1f}%")

    print(f"\nMEDIUM Filter (HIGH+MEDIUM relevance/value):")
    print(f"  - Videos: {stats['filtered']['medium']['videos']}")
    print(f"  - Comments: {stats['filtered']['medium']['comments']}")
    print(f"  - Total: {stats['filtered']['medium']['videos'] + stats['filtered']['medium']['comments']}")
    print(f"  - Retention: {(stats['filtered']['medium']['videos'] + stats['filtered']['medium']['comments'])/stats['total_records']*100:.1f}%")

    print("\nTOP REMOVAL REASONS:")
    sorted_reasons = sorted(stats['removal_reasons'].items(), key=lambda x: x[1], reverse=True)
    for reason, count in sorted_reasons[:10]:
        print(f"  - {reason}: {count}")

    # Save detailed stats
    stats_output = f"{output_dir}/youtube_filtering_stats.json"
    with open(stats_output, 'w') as f:
        # Convert defaultdict to regular dict for JSON serialization
        stats_copy = dict(stats)
        stats_copy['removal_reasons'] = dict(stats['removal_reasons'])
        json.dump(stats_copy, f, indent=2)

    print(f"\nDetailed statistics saved to: {stats_output}")

    # Quality assessment
    print("\n" + "="*80)
    print("QUALITY ASSESSMENT")
    print("="*80)

    high_quality = stats['filtered']['high']['videos'] + stats['filtered']['high']['comments']
    medium_quality = stats['filtered']['medium']['videos'] + stats['filtered']['medium']['comments']

    print(f"\nHIGH Filter Quality:")
    if high_quality < 50:
        print(f"  ⚠ Low volume ({high_quality} records) - may need broader criteria")
    elif high_quality < 200:
        print(f"  ✓ Acceptable volume ({high_quality} records) - focused dataset")
    else:
        print(f"  ✓ Good volume ({high_quality} records) - rich dataset")

    print(f"\nMEDIUM Filter Quality:")
    if medium_quality < 100:
        print(f"  ⚠ Low volume ({medium_quality} records) - may need broader criteria")
    elif medium_quality < 400:
        print(f"  ✓ Acceptable volume ({medium_quality} records) - balanced dataset")
    else:
        print(f"  ✓ Good volume ({medium_quality} records) - comprehensive dataset")

    high_comment_ratio = stats['filtered']['high']['comments'] / max(stats['filtered']['high']['videos'], 1)
    medium_comment_ratio = stats['filtered']['medium']['comments'] / max(stats['filtered']['medium']['videos'], 1)

    print(f"\nComment-to-Video Ratio:")
    print(f"  - HIGH filter: {high_comment_ratio:.1f} comments/video")
    print(f"  - MEDIUM filter: {medium_comment_ratio:.1f} comments/video")

    print("\n" + "="*80)


if __name__ == '__main__':
    main()
