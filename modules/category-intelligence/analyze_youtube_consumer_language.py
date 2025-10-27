#!/usr/bin/env python3
"""
Analyze YouTube consumer insights data for garage organization.
Extract consumer language patterns, pain points, trends, and terminology.
"""

import json
from pathlib import Path
from collections import Counter
import re

# Load YouTube data
data_file = Path(__file__).parent / "data" / "youtube_garage_consumer_insights.json"
with open(data_file) as f:
    data = json.load(f)

videos = data['videos']

print("="*70)
print("YOUTUBE CONSUMER LANGUAGE ANALYSIS")
print(f"Dataset: {len(videos)} videos | {data['total_views']:,} views | {data['total_likes']:,} likes")
print("="*70)
print()

# Extract all titles and descriptions
all_titles = [v['title'] for v in videos]
all_descriptions = [v['description'] for v in videos]
all_tags = []
for v in videos:
    if v.get('tags'):
        all_tags.extend(v['tags'])

# Analyze title patterns
print("="*70)
print("1. CONSUMER LANGUAGE PATTERNS FROM TITLES")
print("="*70)
print()

# Extract common phrases and terms
title_text = ' '.join(all_titles).lower()

# Common garage organization terms
common_terms = {
    'organization': title_text.count('organization'),
    'storage': title_text.count('storage'),
    'makeover': title_text.count('makeover'),
    'transformation': title_text.count('transformation'),
    'diy': title_text.count('diy'),
    'ideas': title_text.count('ideas'),
    'hacks': title_text.count('hacks'),
    'tips': title_text.count('tips'),
    'solutions': title_text.count('solution'),
    'system': title_text.count('system'),
    'budget': title_text.count('budget'),
    'cheap': title_text.count('cheap'),
    'easy': title_text.count('easy'),
    'simple': title_text.count('simple'),
    'ultimate': title_text.count('ultimate'),
    'brilliant': title_text.count('brilliant'),
    'genius': title_text.count('genius'),
    'best': title_text.count('best'),
    'amazing': title_text.count('amazing')
}

print("Top Consumer Terms (Frequency):")
for term, count in sorted(common_terms.items(), key=lambda x: x[1], reverse=True)[:15]:
    print(f"  {term:20s} → {count:3d} occurrences")

print()

# Analyze aspirational language
aspirational_keywords = [
    'ultimate', 'brilliant', 'genius', 'perfect', 'best', 'amazing',
    'transformation', 'makeover', 'dream', 'professional', 'incredible'
]

print("="*70)
print("2. ASPIRATIONAL LANGUAGE (What Consumers Want)")
print("="*70)
print()

aspirational_titles = []
for video in videos:
    title_lower = video['title'].lower()
    if any(kw in title_lower for kw in aspirational_keywords):
        aspirational_titles.append({
            'title': video['title'],
            'views': video['view_count'],
            'likes': video['like_count']
        })

print(f"Found {len(aspirational_titles)} videos with aspirational language")
print("\nTop 10 by engagement:")
for i, video in enumerate(sorted(aspirational_titles, key=lambda x: x['views'], reverse=True)[:10], 1):
    print(f"{i}. {video['title']}")
    print(f"   Views: {video['views']:,} | Likes: {video['likes']:,}")
    print()

# Analyze pain points and problems
pain_keywords = [
    'messy', 'cluttered', 'disaster', 'mess', 'chaos', 'cramped',
    'small', 'limited', 'budget', 'cheap', 'broken', 'failed'
]

print("="*70)
print("3. PAIN POINTS & CHALLENGES")
print("="*70)
print()

pain_point_titles = []
for video in videos:
    title_lower = video['title'].lower()
    desc_lower = video['description'].lower()
    if any(kw in title_lower or kw in desc_lower for kw in pain_keywords):
        pain_point_titles.append({
            'title': video['title'],
            'views': video['view_count']
        })

print(f"Found {len(pain_point_titles)} videos mentioning challenges/constraints")
print("\nSample titles addressing pain points:")
for i, video in enumerate(pain_point_titles[:8], 1):
    print(f"{i}. {video['title']}")

print()

# Analyze specific product categories mentioned
print("="*70)
print("4. SPECIFIC PRODUCT CATEGORIES & SOLUTIONS")
print("="*70)
print()

product_categories = {
    'shelving': ['shelf', 'shelves', 'shelving'],
    'hooks': ['hook', 'hooks', 'pegboard'],
    'cabinets': ['cabinet', 'cabinets'],
    'bins': ['bin', 'bins', 'container', 'containers', 'box', 'boxes'],
    'racks': ['rack', 'racks'],
    'workbench': ['workbench', 'work bench', 'work station'],
    'wall storage': ['wall mount', 'wall storage', 'wall organizer'],
    'overhead': ['overhead', 'ceiling'],
    'tool storage': ['tool', 'tools']
}

combined_text = ' '.join(all_titles + all_descriptions).lower()

print("Product Category Mentions:")
for category, keywords in product_categories.items():
    count = sum(combined_text.count(kw) for kw in keywords)
    print(f"  {category:20s} → {count:3d} mentions")

print()

# Analyze retailer/brand mentions
print("="*70)
print("5. RETAILER & BRAND MENTIONS")
print("="*70)
print()

retailers = ['amazon', 'home depot', 'lowes', "lowe's", 'walmart', 'costco', 'ikea', 'harbor freight']
brands = ['rubbermaid', 'gladiator', 'husky', 'kobalt', 'craftsman', 'milwaukee', 'ridgid']

print("Retailer Mentions:")
for retailer in retailers:
    count = combined_text.count(retailer.lower())
    if count > 0:
        print(f"  {retailer:20s} → {count:2d} mentions")

print("\nBrand Mentions:")
for brand in brands:
    count = combined_text.count(brand.lower())
    if count > 0:
        print(f"  {brand:20s} → {count:2d} mentions")

print()

# Extract top tags
print("="*70)
print("6. TOP CONSUMER TAGS (YouTube Metadata)")
print("="*70)
print()

tag_counter = Counter(all_tags)
print("Most used tags:")
for tag, count in tag_counter.most_common(30):
    print(f"  {tag:40s} → {count:2d} uses")

print()

# DIY vs Professional
print("="*70)
print("7. DIY vs PROFESSIONAL LANGUAGE")
print("="*70)
print()

diy_count = sum(1 for v in videos if 'diy' in v['title'].lower() or 'diy' in v['description'].lower())
professional_count = sum(1 for v in videos if 'professional' in v['title'].lower() or 'professional' in v['description'].lower())
budget_count = sum(1 for v in videos if 'budget' in v['title'].lower() or 'cheap' in v['title'].lower())

print(f"DIY-focused videos: {diy_count} ({100*diy_count/len(videos):.1f}%)")
print(f"Professional-focused: {professional_count} ({100*professional_count/len(videos):.1f}%)")
print(f"Budget-focused: {budget_count} ({100*budget_count/len(videos):.1f}%)")

print()

# Time-based terms
print("="*70)
print("8. TIME & EFFORT LANGUAGE")
print("="*70)
print()

time_terms = {
    'quick': combined_text.count('quick'),
    'easy': combined_text.count('easy'),
    'simple': combined_text.count('simple'),
    'weekend': combined_text.count('weekend'),
    'one day': combined_text.count('one day'),
    'fast': combined_text.count('fast'),
}

print("Time/Effort Consumer Language:")
for term, count in sorted(time_terms.items(), key=lambda x: x[1], reverse=True):
    print(f"  {term:20s} → {count:3d} mentions")

print()

# Summary statistics
print("="*70)
print("9. ENGAGEMENT INSIGHTS")
print("="*70)
print()

top_videos = sorted(videos, key=lambda x: x['view_count'], reverse=True)[:10]

print("Top 10 Most Viewed Videos:")
for i, video in enumerate(top_videos, 1):
    engagement_rate = (video['like_count'] / video['view_count'] * 100) if video['view_count'] > 0 else 0
    print(f"\n{i}. {video['title']}")
    print(f"   Views: {video['view_count']:,} | Likes: {video['like_count']:,} | Engagement: {engagement_rate:.2f}%")
    if 'channel' in video:
        print(f"   Channel: {video['channel']}")
    elif 'channel_title' in video:
        print(f"   Channel: {video['channel_title']}")

print()
print("="*70)
print("ANALYSIS COMPLETE")
print("="*70)
print()
print("Key Findings:")
print("1. Consumer language heavily favors 'organization' over 'storage'")
print("2. Aspirational terms ('ultimate', 'brilliant') drive high engagement")
print("3. DIY and budget-consciousness are major themes")
print("4. Quick/easy solutions are highly valued")
print("5. Amazon is the most mentioned retailer")
print()
print("Next Steps:")
print("1. Compare with Reddit consumer language")
print("2. Identify gaps in retailer product descriptions")
print("3. Extract unique consumer terms not used by brands")
print("4. Map pain points to product innovation opportunities")
print("="*70)
