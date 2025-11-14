#!/usr/bin/env python3
"""
CROSS-PLATFORM AGGREGATION: Combine ALL 2,974+ records
Show base sizes, prove no fabrication, full transparency
"""

import json
from collections import Counter, defaultdict

def load_iteration_1():
    """Load the iteration 1 analysis with all platforms"""
    with open('../03-analysis-output/iteration_1_analysis.json') as f:
        return json.load(f)

def aggregate_pain_points(data):
    """Combine pain points across ALL platforms"""

    # Aggregate counts across all platforms
    combined_counts = Counter()
    combined_examples = defaultdict(list)
    total_records = 0

    # Platform breakdown for transparency
    platform_breakdown = {}

    platforms = [
        'reddit',
        'youtube_videos_legacy',
        'youtube_videos_new',
        'youtube_comments',
        'tiktok',
        'instagram'
    ]

    for platform in platforms:
        if platform not in data:
            continue

        platform_data = data[platform]
        platform_total = platform_data['total_records']
        total_records += platform_total

        platform_breakdown[platform] = {
            'total_records': platform_total,
            'pain_points': {}
        }

        pain_points = platform_data.get('pain_points', {})

        for pain_point, info in pain_points.items():
            count = info['count']
            combined_counts[pain_point] += count

            # Store platform breakdown
            platform_breakdown[platform]['pain_points'][pain_point] = {
                'count': count,
                'percentage': info['percentage']
            }

            # Collect examples from each platform (max 3 per platform)
            examples = info.get('examples', [])[:3]
            for ex in examples:
                ex['platform'] = platform
                combined_examples[pain_point].append(ex)

    # Calculate combined percentages
    combined_results = {
        'total_records_all_platforms': total_records,
        'combined_pain_points': {},
        'platform_breakdown': platform_breakdown
    }

    for pain_point, total_count in combined_counts.most_common():
        percentage = (total_count / total_records * 100) if total_records > 0 else 0

        combined_results['combined_pain_points'][pain_point] = {
            'total_count': total_count,
            'percentage': round(percentage, 1),
            'base_size': total_records,
            'examples': combined_examples[pain_point][:10],  # Top 10 examples
            'platforms_mentioning': sum(
                1 for p in platform_breakdown.values()
                if pain_point in p['pain_points']
            )
        }

    return combined_results

def generate_receipts_report(combined):
    """Generate a SHOW YOUR WORK report"""

    print("="*80)
    print("CROSS-PLATFORM AGGREGATION: SHOWING ALL WORK")
    print("="*80)
    print()

    print(f"TOTAL BASE SIZE: {combined['total_records_all_platforms']:,} records")
    print()

    print("PLATFORM BREAKDOWN:")
    print("-" * 80)
    for platform, info in combined['platform_breakdown'].items():
        print(f"  {platform:25} {info['total_records']:>6} records")
    print()

    print("COMBINED PAIN POINT ANALYSIS:")
    print("-" * 80)

    for pain_point, info in combined['combined_pain_points'].items():
        print(f"\n{pain_point.upper().replace('_', ' ')}")
        print(f"  Total Mentions: {info['total_count']} out of {info['base_size']:,} records")
        print(f"  Percentage: {info['percentage']}%")
        print(f"  Platforms: {info['platforms_mentioning']}/6 platforms mention this")

        print(f"  Platform Breakdown:")
        for platform, pdata in combined['platform_breakdown'].items():
            if pain_point in pdata['pain_points']:
                pinfo = pdata['pain_points'][pain_point]
                print(f"    - {platform:25} {pinfo['count']:>3} mentions ({pinfo['percentage']}%)")

        print(f"  Sample Sources (showing 3):")
        for i, ex in enumerate(info['examples'][:3], 1):
            print(f"    {i}. [{ex['platform']}] {ex.get('url', 'N/A')}")

    print()
    print("="*80)

def main():
    print("Loading iteration 1 analysis...")
    data = load_iteration_1()

    print("Aggregating across all platforms...")
    combined = aggregate_pain_points(data)

    # Generate report
    generate_receipts_report(combined)

    # Save combined results
    output_file = '../03-analysis-output/combined_cross_platform_analysis.json'
    with open(output_file, 'w') as f:
        json.dump(combined, f, indent=2)

    print(f"\n✅ Saved combined analysis to: {output_file}")

    # Print summary for slides
    print("\n" + "="*80)
    print("SUMMARY FOR SLIDES (USE THESE NUMBERS):")
    print("="*80)

    for pain_point, info in sorted(
        combined['combined_pain_points'].items(),
        key=lambda x: x[1]['percentage'],
        reverse=True
    ):
        print(f"{pain_point:25} {info['percentage']:>5.1f}% ({info['total_count']:>4} / {info['base_size']:>5,})")

if __name__ == "__main__":
    main()
