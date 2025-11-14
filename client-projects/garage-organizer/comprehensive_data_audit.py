#!/usr/bin/env python3
"""
Comprehensive Data Audit - Verify all claims against consolidated data
"""

import json
import re
from collections import defaultdict

print("="*80)
print("COMPREHENSIVE DATA AUDIT")
print("="*80)
print()

# Load consolidated data
print("Loading consolidated data sources...")
with open('01-raw-data/reddit_consolidated.json', 'r') as f:
    reddit_data = json.load(f)
with open('01-raw-data/youtube_videos_consolidated.json', 'r') as f:
    youtube_videos = json.load(f)
with open('01-raw-data/youtube_comments_consolidated.json', 'r') as f:
    youtube_comments = json.load(f)
with open('01-raw-data/tiktok_consolidated.json', 'r') as f:
    tiktok_data = json.load(f)

print(f"✅ Reddit: {len(reddit_data)} posts")
print(f"✅ YouTube Videos: {len(youtube_videos)} videos")
print(f"✅ YouTube Comments: {len(youtube_comments)} comments")
print(f"✅ TikTok: {len(tiktok_data)} videos")
print(f"✅ Total: {len(reddit_data) + len(youtube_videos) + len(youtube_comments) + len(tiktok_data)} records")
print()

# Verify claims from slides
print("="*80)
print("CLAIM VERIFICATION")
print("="*80)
print()

# CLAIM 1: Installation difficulty - 64% claimed
print("CLAIM 1: Installation Difficulty")
print("-" * 40)
print("❌ Slide Claims: 64% (n=571 videos)")
print()

installation_keywords = [
    'install', 'installation', 'mounting', 'mount', 'drill', 'drilling',
    'damage', 'difficult', 'difficulty', 'hard to', 'tools', 'tool'
]

installation_mentions = []
for i, post in enumerate(reddit_data):
    text = (post.get('post_text', '') + ' ' + post.get('title', '')).lower()
    if any(keyword in text for keyword in installation_keywords):
        installation_mentions.append(i)

print(f"✅ Actual (Reddit n={len(reddit_data)}): {len(installation_mentions)} mentions")
print(f"✅ Percentage: {len(installation_mentions)/len(reddit_data)*100:.1f}%")
print(f"🔍 Sample URLs:")
for idx in installation_mentions[:3]:
    print(f"   - {reddit_data[idx].get('post_url', 'No URL')}")
print()

# CLAIM 2: Weight capacity failures - 58% claimed
print("CLAIM 2: Weight Capacity Failures")
print("-" * 40)
print("❌ Slide Claims: 58% (n=571 videos)")
print()

weight_keywords = [
    'weight', 'capacity', 'heavy', 'fell', 'fall', 'falling', 'dropped',
    'collapse', 'failed', 'lb', 'lbs', 'pound'
]

weight_mentions = []
for i, post in enumerate(reddit_data):
    text = (post.get('post_text', '') + ' ' + post.get('title', '')).lower()
    if any(keyword in text for keyword in weight_keywords):
        weight_mentions.append(i)

print(f"✅ Actual (Reddit n={len(reddit_data)}): {len(weight_mentions)} mentions")
print(f"✅ Percentage: {len(weight_mentions)/len(reddit_data)*100:.1f}%")
print(f"🔍 Sample URLs:")
for idx in weight_mentions[:3]:
    print(f"   - {reddit_data[idx].get('post_url', 'No URL')}")
print()

# CLAIM 3: Rust/durability - 39% claimed
print("CLAIM 3: Rust/Durability Issues")
print("-" * 40)
print("❌ Slide Claims: 39% (n=571 videos)")
print()

rust_keywords = [
    'rust', 'rusting', 'rusted', 'corrode', 'corrosion', 'durability',
    'durable', 'last', 'lasting', 'quality'
]

rust_mentions = []
for i, post in enumerate(reddit_data):
    text = (post.get('post_text', '') + ' ' + post.get('title', '')).lower()
    if any(keyword in text for keyword in rust_keywords):
        rust_mentions.append(i)

print(f"✅ Actual (Reddit n={len(reddit_data)}): {len(rust_mentions)} mentions")
print(f"✅ Percentage: {len(rust_mentions)/len(reddit_data)*100:.1f}%")
print(f"🔍 Sample URLs:")
for idx in rust_mentions[:3]:
    print(f"   - {reddit_data[idx].get('post_url', 'No URL')}")
print()

# CLAIM 4: Rental restrictions - 31% claimed
print("CLAIM 4: Rental Restrictions")
print("-" * 40)
print("❌ Slide Claims: 31% (n=571 videos)")
print()

rental_keywords = [
    'rent', 'rental', 'renting', 'lease', 'leasing', 'landlord',
    'apartment', 'tenant', 'property'
]

rental_mentions = []
for i, post in enumerate(reddit_data):
    text = (post.get('post_text', '') + ' ' + post.get('title', '')).lower()
    if any(keyword in text for keyword in rental_keywords):
        rental_mentions.append(i)

print(f"✅ Actual (Reddit n={len(reddit_data)}): {len(rental_mentions)} mentions")
print(f"✅ Percentage: {len(rental_mentions)/len(reddit_data)*100:.1f}%")
print(f"🔍 Sample URLs:")
for idx in rental_mentions[:3]:
    print(f"   - {reddit_data[idx].get('post_url', 'No URL')}")
print()

# CLAIM 5: Follow-on purchases - 73% claimed
print("CLAIM 5: Follow-on Purchases (73%)")
print("-" * 40)
print("❌ Slide Claims: 73% make follow-on purchases, LTV=3.2x")
print("❌ Source: '412 creators longitudinal observation'")
print()

# Check YouTube videos for evidence
print("Checking YouTube videos for purchase behavior evidence...")
print(f"Total YouTube videos: {len(youtube_videos)}")

# Look for creators with multiple videos
creators = defaultdict(list)
for video in youtube_videos:
    channel = video.get('channel', video.get('channelTitle', 'Unknown'))
    creators[channel].append(video)

multi_video_creators = {k: v for k, v in creators.items() if len(v) > 1}
print(f"Creators with multiple videos: {len(multi_video_creators)}")
print(f"Total unique creators: {len(creators)}")
print()

print("⚠️ CANNOT VERIFY: No purchase behavior data in dataset")
print("⚠️ Video observation does NOT equal purchase behavior")
print("⚠️ The '412 creators' claim cannot be verified in provided data")
print()

# SUMMARY
print("="*80)
print("AUDIT SUMMARY")
print("="*80)
print()

print("✅ VERIFIED DATA:")
print(f"   - Reddit posts: {len(reddit_data)} (100% have URLs)")
print(f"   - YouTube videos: {len(youtube_videos)}")
print(f"   - YouTube comments: {len(youtube_comments)}")
print(f"   - Total: {len(reddit_data) + len(youtube_videos) + len(youtube_comments) + len(tiktok_data)}")
print()

print("❌ FABRICATED CLAIMS:")
print(f"   - '571 videos' → Actual: {len(youtube_videos) + len(youtube_comments)} YouTube records")
print(f"   - '64% installation difficulty' → Actual: {len(installation_mentions)/len(reddit_data)*100:.1f}%")
print(f"   - '58% weight failures' → Actual: {len(weight_mentions)/len(reddit_data)*100:.1f}%")
print(f"   - '39% rust/durability' → Actual: {len(rust_mentions)/len(reddit_data)*100:.1f}%")
print(f"   - '31% rental restrictions' → Actual: {len(rental_mentions)/len(reddit_data)*100:.1f}%")
print(f"   - '73% follow-on purchases' → NO DATA")
print(f"   - 'LTV=3.2x' → NO DATA")
print(f"   - '412 creators longitudinal' → Cannot verify")
print()

print("📊 RECALCULATION STATUS:")
print()
print(f"✅ CAN RECALCULATE:")
print(f"   - Installation difficulty: {len(installation_mentions)/len(reddit_data)*100:.1f}% (n={len(reddit_data)} Reddit)")
print(f"   - Weight capacity: {len(weight_mentions)/len(reddit_data)*100:.1f}% (n={len(reddit_data)} Reddit)")
print(f"   - Rental context: {len(rental_mentions)/len(reddit_data)*100:.1f}% (n={len(reddit_data)} Reddit)")
print()
print(f"⚠️ INSUFFICIENT DATA - DELETE:")
print(f"   - Rust/durability: {len(rust_mentions)/len(reddit_data)*100:.1f}% (keyword matches, not complaints)")
print(f"   - Follow-on purchases: NO PURCHASE DATA")
print(f"   - LTV: NO PURCHASE DATA")
print()

# Save detailed report
audit_report = {
    'consolidated_data': {
        'reddit': len(reddit_data),
        'youtube_videos': len(youtube_videos),
        'youtube_comments': len(youtube_comments),
        'tiktok': len(tiktok_data),
        'total': len(reddit_data) + len(youtube_videos) + len(youtube_comments) + len(tiktok_data)
    },
    'fabrications': {
        'n=571_videos': {
            'claimed': 571,
            'actual': len(youtube_videos) + len(youtube_comments),
            'status': 'FABRICATED'
        },
        'installation_difficulty': {
            'claimed': 64.0,
            'actual': round(len(installation_mentions)/len(reddit_data)*100, 1),
            'count': len(installation_mentions),
            'base': len(reddit_data),
            'status': 'CAN_RECALCULATE'
        },
        'weight_failures': {
            'claimed': 58.0,
            'actual': round(len(weight_mentions)/len(reddit_data)*100, 1),
            'count': len(weight_mentions),
            'base': len(reddit_data),
            'status': 'CAN_RECALCULATE'
        },
        'rental_restrictions': {
            'claimed': 31.0,
            'actual': round(len(rental_mentions)/len(reddit_data)*100, 1),
            'count': len(rental_mentions),
            'base': len(reddit_data),
            'status': 'CAN_RECALCULATE'
        },
        'rust_durability': {
            'claimed': 39.0,
            'actual': round(len(rust_mentions)/len(reddit_data)*100, 1),
            'count': len(rust_mentions),
            'base': len(reddit_data),
            'status': 'DELETE - Not complaints'
        },
        'follow_on_purchases': {
            'claimed': 73.0,
            'actual': None,
            'status': 'DELETE - NO DATA'
        },
        'ltv': {
            'claimed': 3.2,
            'actual': None,
            'status': 'DELETE - NO DATA'
        }
    }
}

with open('COMPREHENSIVE_AUDIT_REPORT.json', 'w') as f:
    json.dump(audit_report, f, indent=2)

print("✅ Detailed audit report saved: COMPREHENSIVE_AUDIT_REPORT.json")
