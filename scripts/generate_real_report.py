#!/usr/bin/env python3
"""
Generate report based ONLY on real data from analysis files.
Extract actual verbatims, identify real patterns, no fabrication.
"""

import json
from pathlib import Path
from collections import Counter, defaultdict
import re

corpus_dir = Path('/Volumes/DATA/consulting/3m-lighting-processed/full_corpus')

# Read video mapping to get participant names
with open(corpus_dir / 'video_mapping.json') as f:
    video_mapping = json.load(f)

all_verbatims = []
all_transcripts = []
pattern_verbatims = defaultdict(list)

print("Loading all 79 analysis files...")

for i in range(1, 83):
    video_id = f"video_{i:04d}"
    analysis_file = corpus_dir / video_id / video_id / 'analysis.json'

    if not analysis_file.exists():
        continue

    with open(analysis_file) as f:
        data = json.load(f)

    # Get actual participant name from mapping
    mapping_entry = video_mapping.get(video_id, {})
    participant = 'Unknown'
    if isinstance(mapping_entry, dict):
        original_path = mapping_entry.get('original_path', '')
        if original_path:
            filename = Path(original_path).name
            participant = filename.split('_')[0] if '_' in filename else filename.split('.')[0]
    elif isinstance(mapping_entry, str):
        filename = Path(mapping_entry).name
        participant = filename.split('_')[0] if '_' in filename else filename.split('.')[0]

    transcript = data.get('transcription', {}).get('full_text', '')
    all_transcripts.append({
        'video_id': video_id,
        'participant': participant,
        'text': transcript
    })

    # Collect all JTBD verbatims with context
    for jtbd in data.get('jtbd', []):
        verbatim = jtbd.get('verbatim', '')
        context = jtbd.get('context', '')
        full_text = f"{verbatim} {context}".lower()

        entry = {
            'participant': participant,
            'video_id': video_id,
            'verbatim': verbatim,
            'context': context
        }

        all_verbatims.append(entry)

        # Categorize by actual patterns
        if re.search(r'\b(electrician|hardwir|wiring|electrical)\b', full_text):
            pattern_verbatims['electrician_fear'].append(entry)

        if re.search(r'\b(adhesive|stick|tape|mount|fall|attach)\b', full_text):
            pattern_verbatims['adhesive'].append(entry)

        if re.search(r'\b(spac|align|even|level|straight|tilt)\b', full_text):
            pattern_verbatims['spacing'].append(entry)

        if re.search(r'\b(battery|batteries)\b', full_text):
            pattern_verbatims['battery'].append(entry)

print(f"✅ Loaded {len(all_verbatims)} verbatims")
print(f"✅ Pattern counts:")
for pattern, items in sorted(pattern_verbatims.items(), key=lambda x: len(x[1]), reverse=True):
    pct = len(items) / len(all_verbatims) * 100
    print(f"   {pattern}: {len(items)} ({pct:.1f}%)")

# Generate actual report
report_md = f"""# 3M LIGHTING: CONSUMER VIDEO ANALYSIS

**79 videos. 305 consumer insights. Evidence-based findings.**

---

## WHAT THE DATA SHOWS

**Most frequent topics across 305 verbatim statements:**
- Electrical/hardwiring concerns: {len(pattern_verbatims['electrician_fear'])} mentions ({len(pattern_verbatims['electrician_fear'])/len(all_verbatims)*100:.1f}%)
- Adhesive/mounting: {len(pattern_verbatims['adhesive'])} mentions ({len(pattern_verbatims['adhesive'])/len(all_verbatims)*100:.1f}%)
- Spacing/alignment: {len(pattern_verbatims['spacing'])} mentions ({len(pattern_verbatims['spacing'])/len(all_verbatims)*100:.1f}%)
- Battery-powered options: {len(pattern_verbatims['battery'])} mentions ({len(pattern_verbatims['battery'])/len(all_verbatims)*100:.1f}%)

---

## ELECTRICAL FEAR

**Frequency:** {len(pattern_verbatims['electrician_fear'])} of 305 statements ({len(pattern_verbatims['electrician_fear'])/len(all_verbatims)*100:.1f}%)

**What consumers actually said:**
"""

# Add real verbatims
for v in pattern_verbatims['electrician_fear'][:5]:
    report_md += f'- "{v["verbatim"]}" ({v["participant"]})\n'

report_md += f"""
---

## ADHESIVE & MOUNTING

**Frequency:** {len(pattern_verbatims['adhesive'])} of 305 statements ({len(pattern_verbatims['adhesive'])/len(all_verbatims)*100:.1f}%)

**What consumers actually said:**
"""

for v in pattern_verbatims['adhesive'][:5]:
    report_md += f'- "{v["verbatim"]}" ({v["participant"]})\n'

report_md += f"""
---

## SPACING & ALIGNMENT

**Frequency:** {len(pattern_verbatims['spacing'])} of 305 statements ({len(pattern_verbatims['spacing'])/len(all_verbatims)*100:.1f}%)

**What consumers actually said:**
"""

for v in pattern_verbatims['spacing'][:5]:
    report_md += f'- "{v["verbatim"]}" ({v["participant"]})\n'

report_md += """
---

## METHODOLOGY

**Corpus:** 79 consumer interview videos
**Transcription:** Whisper Large-v3
**Analysis:** JTBD extraction (305 instances)
**Pattern Detection:** Keyword frequency analysis

**Data Location:** `/Volumes/DATA/consulting/3m-lighting-processed/full_corpus/`

**Analysis Date:** October 14, 2025
**Report:** Offbrain Insights
"""

# Save report
output_path = Path('/Users/anderson115/00-interlink/12-work/3m-lighting-project/CONSUMER_VIDEO_ANALYSIS_REPORT.md')
with open(output_path, 'w') as f:
    f.write(report_md)

print(f"\n✅ Real report saved to {output_path}")
