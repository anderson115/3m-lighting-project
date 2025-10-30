#!/usr/bin/env python3
"""Select top 25 videos from additional collection based on engagement"""

import json
from pathlib import Path
from typing import List, Dict

# Paths
project_root = Path(__file__).parent
additional_collection = project_root / "modules/social-video-collection/data/processed/garage-organizers-additional/videos"

def calculate_engagement_score(metadata: Dict) -> float:
    """Calculate engagement score: views + (likes * 10) + (comments * 20)"""
    views = metadata.get('views', 0)
    likes = metadata.get('likes', 0)
    comments = metadata.get('comments', 0)

    # Weight: comments > likes > views (comments indicate deeper engagement)
    return views + (likes * 10) + (comments * 20)

def is_fully_complete(video_dir: Path) -> bool:
    """Check if video has all required data"""
    required_files = [
        'metadata.json',
        'transcript.json',
        'visual_analysis.json',
        'audio_features.json',
        'emotion_analysis.json'
    ]

    for file in required_files:
        if not (video_dir / file).exists():
            return False

    # Check that emotion analysis isn't empty
    emotion_file = video_dir / "emotion_analysis.json"
    try:
        with open(emotion_file) as f:
            emotion_data = json.load(f)
            if not emotion_data.get('primary_emotion'):
                return False
    except:
        return False

    return True

# Find all complete videos
print("="*80)
print("SELECTING TOP 25 VIDEOS FROM ADDITIONAL COLLECTION")
print("="*80)

complete_videos = []

for video_dir in sorted(additional_collection.iterdir()):
    if not video_dir.is_dir():
        continue

    if not is_fully_complete(video_dir):
        continue

    # Load metadata
    metadata_file = video_dir / "metadata.json"
    with open(metadata_file) as f:
        metadata = json.load(f)

    # Load emotion data
    emotion_file = video_dir / "emotion_analysis.json"
    with open(emotion_file) as f:
        emotion_data = json.load(f)

    engagement_score = calculate_engagement_score(metadata)

    description = metadata.get('description') or ''
    complete_videos.append({
        'video_id': metadata['video_id'],
        'views': metadata.get('views', 0),
        'likes': metadata.get('likes', 0),
        'comments': metadata.get('comments', 0),
        'engagement_score': engagement_score,
        'emotion': emotion_data.get('primary_emotion', 'unknown'),
        'emotion_confidence': emotion_data.get('confidence', 0.0),
        'description': description[:80] if description else ''
    })

print(f"\n✓ Found {len(complete_videos)} fully complete videos")

if len(complete_videos) < 25:
    print(f"\n❌ ERROR: Only {len(complete_videos)} complete videos, need 25!")
    print("   Need to process more videos from additional collection")
    exit(1)

# Sort by engagement score (descending)
complete_videos.sort(key=lambda x: x['engagement_score'], reverse=True)

# Select top 25
top_25 = complete_videos[:25]

print(f"\n{'='*80}")
print("TOP 25 VIDEOS SELECTED")
print(f"{'='*80}\n")

print(f"{'Rank':<5} {'Video ID':<20} {'Views':>10} {'Likes':>8} {'Comments':>10} {'Score':>12} {'Emotion':<20}")
print("-"*100)

for i, video in enumerate(top_25, 1):
    print(f"{i:<5} {video['video_id']:<20} {video['views']:>10,} {video['likes']:>8,} {video['comments']:>10,} {video['engagement_score']:>12,.0f} {video['emotion']:<20}")

print(f"\n{'='*80}")
print("ENGAGEMENT STATISTICS")
print(f"{'='*80}\n")

total_views = sum(v['views'] for v in top_25)
total_likes = sum(v['likes'] for v in top_25)
total_comments = sum(v['comments'] for v in top_25)
avg_engagement = sum(v['engagement_score'] for v in top_25) / 25

print(f"Total Views:       {total_views:>12,}")
print(f"Total Likes:       {total_likes:>12,}")
print(f"Total Comments:    {total_comments:>12,}")
print(f"Avg Engagement:    {avg_engagement:>12,.0f}")

print(f"\n{'='*80}")
print("EMOTION DISTRIBUTION (TOP 25)")
print(f"{'='*80}\n")

from collections import Counter
emotion_dist = Counter(v['emotion'] for v in top_25)

for emotion, count in emotion_dist.most_common():
    pct = count/25*100
    print(f"  {emotion:<30} {count:>3} ({pct:>5.1f}%)")

# Save selection
output_file = project_root / "top_25_selection.json"
with open(output_file, 'w') as f:
    json.dump({
        'selection_criteria': 'engagement_score = views + (likes * 10) + (comments * 20)',
        'total_candidates': len(complete_videos),
        'selected': [v['video_id'] for v in top_25],
        'details': top_25
    }, f, indent=2)

print(f"\n✓ Selection saved to: {output_file.name}")

print(f"\n{'='*80}")
print("NEXT STEPS")
print(f"{'='*80}\n")
print("1. Review top 25 selection")
print("2. Consolidate with original 128 videos = 153 total")
print("3. Generate final summary statistics")
print(f"\n{'='*80}")
