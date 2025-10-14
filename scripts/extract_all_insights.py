#!/usr/bin/env python3
"""
Extract ALL insights from the full corpus analysis data.
Generate report based ONLY on actual data, not assumptions.
"""

import json
from pathlib import Path
from collections import Counter, defaultdict

# Load all 79 analysis files
corpus_dir = Path('/Volumes/DATA/consulting/3m-lighting-processed/full_corpus')
all_jtbd = []
all_pain_points = []
all_quotes = []
participant_insights = defaultdict(lambda: {'jtbd_count': 0, 'pain_count': 0, 'videos': []})

print("Loading 79 analysis files...")
for i in range(1, 83):
    video_id = f"video_{i:04d}"
    analysis_file = corpus_dir / video_id / video_id / 'analysis.json'

    if not analysis_file.exists():
        continue

    with open(analysis_file) as f:
        data = json.load(f)

    # Extract participant name from filename
    filename = data['metadata'].get('title', '')
    participant = filename.split('_')[0] if '_' in filename else 'Unknown'

    # Collect JTBD instances
    for jtbd in data.get('jtbd', []):
        all_jtbd.append({
            'participant': participant,
            'video_id': video_id,
            'verbatim': jtbd.get('verbatim', ''),
            'job_category': jtbd.get('job_category', 'unknown'),
            'confidence': jtbd.get('confidence', 0)
        })
        participant_insights[participant]['jtbd_count'] += 1
        if video_id not in participant_insights[participant]['videos']:
            participant_insights[participant]['videos'].append(video_id)

    # Collect pain points
    for pain in data.get('pain_points', []):
        all_pain_points.append({
            'participant': participant,
            'video_id': video_id,
            'description': pain.get('description', ''),
            'category': pain.get('category', 'unknown'),
            'severity': pain.get('severity', 'unknown')
        })
        participant_insights[participant]['pain_count'] += 1

print(f"\n✅ Loaded {len(all_jtbd)} JTBD instances from {len([p for p in corpus_dir.iterdir() if p.is_dir() and p.name.startswith('video_')])} videos")
print(f"✅ Loaded {len(all_pain_points)} pain points")

# Analyze pain point categories
pain_categories = Counter([p['category'] for p in all_pain_points])
print(f"\n📊 Pain Point Categories:")
for category, count in pain_categories.most_common():
    percentage = (count / len(all_pain_points) * 100) if all_pain_points else 0
    print(f"  {category}: {count} ({percentage:.1f}%)")

# Find top participants by insight density
print(f"\n👤 Top Participants by Insight Count:")
for participant, stats in sorted(participant_insights.items(), key=lambda x: x[1]['jtbd_count'], reverse=True)[:5]:
    avg_per_video = stats['jtbd_count'] / len(stats['videos']) if stats['videos'] else 0
    print(f"  {participant}: {stats['jtbd_count']} insights from {len(stats['videos'])} videos ({avg_per_video:.1f} per video)")

# Extract verbatims for top themes
print(f"\n💬 Sample Verbatims by Pain Category:")
for category in pain_categories.most_common(5):
    cat_name = category[0]
    samples = [p for p in all_pain_points if p['category'] == cat_name][:3]
    print(f"\n{cat_name.upper()}:")
    for s in samples:
        desc = s['description'][:100] + '...' if len(s['description']) > 100 else s['description']
        print(f"  - {desc} ({s['participant']})")

# Save full extraction
output = {
    'total_jtbd': len(all_jtbd),
    'total_pain_points': len(all_pain_points),
    'pain_categories': dict(pain_categories),
    'top_participants': {
        p: {'jtbd_count': s['jtbd_count'], 'video_count': len(s['videos'])}
        for p, s in sorted(participant_insights.items(), key=lambda x: x[1]['jtbd_count'], reverse=True)[:10]
    },
    'all_jtbd': all_jtbd,
    'all_pain_points': all_pain_points
}

output_file = Path('/Users/anderson115/00-interlink/12-work/3m-lighting-project/data/reports/full_corpus_extraction.json')
output_file.parent.mkdir(parents=True, exist_ok=True)
with open(output_file, 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n✅ Full extraction saved to {output_file}")
