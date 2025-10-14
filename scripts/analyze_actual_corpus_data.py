#!/usr/bin/env python3
"""
Analyze ACTUAL data from the corpus.
Extract insights ONLY from what exists in the analysis files.
"""

import json
from pathlib import Path
from collections import Counter, defaultdict
import re

corpus_dir = Path('/Volumes/DATA/consulting/3m-lighting-processed/full_corpus')

# Storage for actual data
all_jtbd_verbatims = []
all_transcripts = []
participant_data = defaultdict(lambda: {
    'videos': [],
    'jtbd_count': 0,
    'total_transcript_length': 0,
    'verbatims': []
})

print("📊 Analyzing 79 videos...")

# Load ALL analysis files
for i in range(1, 83):
    video_id = f"video_{i:04d}"
    analysis_file = corpus_dir / video_id / video_id / 'analysis.json'

    if not analysis_file.exists():
        continue

    with open(analysis_file) as f:
        data = json.load(f)

    # Extract participant from title
    title = data['metadata'].get('title', '')
    # Try to extract participant name before first underscore or space
    participant = title.split('_')[0] if '_' in title else title.split('.')[0]

    # Store transcript
    transcript = data.get('transcription', {}).get('full_text', '')
    all_transcripts.append({
        'video_id': video_id,
        'participant': participant,
        'text': transcript
    })

    participant_data[participant]['total_transcript_length'] += len(transcript)
    participant_data[participant]['videos'].append(video_id)

    # Store JTBD with full context
    for jtbd in data.get('jtbd', []):
        verbatim = jtbd.get('verbatim', '')
        context = jtbd.get('context', '')

        all_jtbd_verbatims.append({
            'video_id': video_id,
            'participant': participant,
            'verbatim': verbatim,
            'context': context,
            'timestamp': jtbd.get('timestamp', 0)
        })

        participant_data[participant]['jtbd_count'] += 1
        participant_data[participant]['verbatims'].append(verbatim)

print(f"✅ Loaded {len(all_transcripts)} transcripts")
print(f"✅ Loaded {len(all_jtbd_verbatims)} JTBD verbatims")

# Analyze actual patterns from verbatims
print("\n🔍 Analyzing patterns in verbatims...")

# Search for specific topics in verbatims
patterns = {
    'electrician_fear': r'\b(electrician|hardwir|wiring|electrical|power)\b',
    'adhesive': r'\b(adhesive|stick|tape|mount|fall|attach)\b',
    'spacing_alignment': r'\b(spac|align|even|level|straight|tilt)\b',
    'heat_temperature': r'\b(heat|hot|temperature|arizona|desert)\b',
    'battery': r'\b(battery|batter)\b',
    'tool': r'\b(tool|drill|measure)\b'
}

pattern_matches = defaultdict(list)

for jtbd in all_jtbd_verbatims:
    text = (jtbd['verbatim'] + ' ' + jtbd['context']).lower()

    for pattern_name, regex in patterns.items():
        if re.search(regex, text, re.IGNORECASE):
            pattern_matches[pattern_name].append({
                'participant': jtbd['participant'],
                'verbatim': jtbd['verbatim'],
                'context': jtbd['context'][:200]
            })

print("\n📈 Pattern Frequencies:")
for pattern, matches in sorted(pattern_matches.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"  {pattern}: {len(matches)} mentions ({len(matches)/len(all_jtbd_verbatims)*100:.1f}%)")

# Top participants
print(f"\n👤 Top Participants:")
for participant, stats in sorted(participant_data.items(), key=lambda x: x[1]['jtbd_count'], reverse=True)[:10]:
    avg_per_video = stats['jtbd_count'] / len(stats['videos']) if stats['videos'] else 0
    print(f"  {participant}: {stats['jtbd_count']} JTBD from {len(stats['videos'])} videos (avg {avg_per_video:.1f}/video)")

# Save detailed extraction
output = {
    'total_videos': len(all_transcripts),
    'total_jtbd': len(all_jtbd_verbatims),
    'pattern_matches': {k: len(v) for k, v in pattern_matches.items()},
    'top_participants': {
        p: {'jtbd_count': s['jtbd_count'], 'video_count': len(s['videos'])}
        for p, s in sorted(participant_data.items(), key=lambda x: x[1]['jtbd_count'], reverse=True)[:10]
    },
    'pattern_examples': {
        pattern: [
            {'participant': m['participant'], 'verbatim': m['verbatim'][:150]}
            for m in matches[:5]
        ]
        for pattern, matches in sorted(pattern_matches.items(), key=lambda x: len(x[1]), reverse=True)[:5]
    }
}

output_file = Path('/Users/anderson115/00-interlink/12-work/3m-lighting-project/data/reports/actual_corpus_analysis.json')
output_file.parent.mkdir(parents=True, exist_ok=True)
with open(output_file, 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n✅ Analysis saved to {output_file}")

# Print sample verbatims for top patterns
print("\n💬 Sample Verbatims:")
for pattern in list(pattern_matches.keys())[:3]:
    print(f"\n{pattern.upper().replace('_', ' ')}:")
    for match in pattern_matches[pattern][:3]:
        print(f"  - \"{match['verbatim'][:100]}...\" ({match['participant']})")
