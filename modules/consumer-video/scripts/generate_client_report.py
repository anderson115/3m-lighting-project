#!/usr/bin/env python3
"""
Generate practice client deliverable report with citations
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def format_timestamp(seconds):
    """Convert seconds to MM:SS format"""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}:{secs:02d}"

def load_analysis(video_id, processed_dir):
    """Load analysis JSON for a video"""
    analysis_path = processed_dir / video_id / 'analysis.json'
    if not analysis_path.exists():
        return None
    with open(analysis_path) as f:
        return json.load(f)

def extract_participant(title):
    """Extract participant name from title"""
    # Titles like "AlanG Q1 Interview" or "CarrieS Activity8 Pain Points"
    parts = title.split()
    if parts:
        return parts[0]
    return "Unknown"

def generate_report(processed_dir, output_path):
    """Generate client deliverable report"""

    # Load all 5 videos
    video_ids = ['consumer01', 'consumer02', 'consumer03', 'consumer04', 'consumer05']
    analyses = {}

    for video_id in video_ids:
        analysis = load_analysis(video_id, processed_dir)
        if analysis:
            analyses[video_id] = analysis

    if not analyses:
        print("❌ No analyses found")
        return

    # Start building report
    report = []
    report.append("# 3M LIGHTING CONSUMER RESEARCH")
    report.append("## Video Analysis Report - Practice Deliverable")
    report.append("")
    report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**Videos Analyzed:** {len(analyses)}")
    report.append("")
    report.append("---")
    report.append("")

    # Executive Summary
    report.append("## EXECUTIVE SUMMARY")
    report.append("")

    total_duration = sum(a['metadata']['duration'] for a in analyses.values())
    total_emotions = sum(len(a.get('emotion_analysis', {}).get('timeline', [])) for a in analyses.values())

    report.append(f"This report analyzes **{len(analyses)} consumer interviews** totaling **{total_duration//60} minutes {total_duration%60} seconds** of video content. ")
    report.append(f"Using multimodal AI analysis (Whisper transcription + prosodic emotion detection + visual analysis), ")
    report.append(f"we extracted **{total_emotions} emotional moments** and identified key pain points and solutions.")
    report.append("")
    report.append("**Key Findings:**")

    # Count dominant emotions across all videos
    all_emotions = []
    for analysis in analyses.values():
        timeline = analysis.get('emotion_analysis', {}).get('timeline', [])
        all_emotions.extend([e['emotion'] for e in timeline])

    emotion_counts = defaultdict(int)
    for emotion in all_emotions:
        emotion_counts[emotion] += 1

    for emotion, count in sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:3]:
        report.append(f"- **{emotion.capitalize()}**: {count} instances across videos")

    report.append("")
    report.append("---")
    report.append("")

    # Section 1: Pain Points
    report.append("## 1. PAIN POINTS & FRUSTRATIONS")
    report.append("")
    report.append("Moments where consumers expressed frustration, identified problems, or struggled with existing lighting solutions.")
    report.append("")

    pain_point_num = 1
    for video_id, analysis in analyses.items():
        metadata = analysis['metadata']
        participant = extract_participant(metadata['title'])

        # Find frustration moments
        emotion_segments = analysis.get('emotion_analysis', {}).get('segments', [])

        for segment in emotion_segments:
            indicators = segment.get('indicators', [])

            for indicator in indicators:
                if indicator['emotion'] == 'frustration' and indicator['confidence'] >= 0.5:
                    report.append(f"### {pain_point_num}. {segment['text'][:60]}...")
                    report.append("")
                    report.append(f"**Source:** `{video_id}` ({metadata['title']})")
                    report.append(f"**Participant:** {participant}")
                    report.append(f"**Timestamp:** {format_timestamp(segment['timestamp'])} ({segment['timestamp']:.1f}s)")
                    report.append(f"**Confidence:** {indicator['confidence']:.2f}")
                    report.append("")
                    report.append("**Verbatim Quote:**")
                    report.append(f"> \"{segment['text']}\"")
                    report.append("")
                    report.append("**Evidence:**")
                    for evidence in indicator.get('evidence', []):
                        report.append(f"- {evidence}")
                    report.append("")
                    report.append("**Acoustic Features:**")
                    acoustic = segment.get('acoustic_features', {})
                    report.append(f"- Pitch variance: {acoustic.get('pitch_variance', 0):.1f} Hz²")
                    report.append(f"- Energy: {acoustic.get('energy', 0):.4f}")
                    report.append(f"- Spectral centroid: {acoustic.get('spectral_centroid', 0):.1f} Hz")
                    report.append("")
                    report.append("---")
                    report.append("")
                    pain_point_num += 1

    # Section 2: Satisfaction Moments
    report.append("## 2. SATISFACTION & POSITIVE EXPERIENCES")
    report.append("")
    report.append("Moments where consumers expressed satisfaction with lighting solutions or praised product features.")
    report.append("")

    satisfaction_num = 1
    for video_id, analysis in analyses.items():
        metadata = analysis['metadata']
        participant = extract_participant(metadata['title'])

        emotion_segments = analysis.get('emotion_analysis', {}).get('segments', [])

        for segment in emotion_segments:
            indicators = segment.get('indicators', [])

            for indicator in indicators:
                if indicator['emotion'] == 'satisfaction' and indicator['confidence'] >= 0.5:
                    report.append(f"### {satisfaction_num}. {segment['text'][:60]}...")
                    report.append("")
                    report.append(f"**Source:** `{video_id}` ({metadata['title']})")
                    report.append(f"**Participant:** {participant}")
                    report.append(f"**Timestamp:** {format_timestamp(segment['timestamp'])} ({segment['timestamp']:.1f}s)")
                    report.append(f"**Confidence:** {indicator['confidence']:.2f}")
                    report.append("")
                    report.append("**Verbatim Quote:**")
                    report.append(f"> \"{segment['text']}\"")
                    report.append("")
                    report.append("**Evidence:**")
                    for evidence in indicator.get('evidence', []):
                        report.append(f"- {evidence}")
                    report.append("")
                    report.append("---")
                    report.append("")
                    satisfaction_num += 1

    # Section 3: Emotional Timeline Summary
    report.append("## 3. EMOTIONAL JOURNEY ANALYSIS")
    report.append("")
    report.append("Emotion detection timeline for each participant.")
    report.append("")

    for video_id, analysis in analyses.items():
        metadata = analysis['metadata']
        participant = extract_participant(metadata['title'])

        report.append(f"### {participant} - {metadata['title']}")
        report.append("")
        report.append(f"**Source:** `{video_id}`")
        report.append(f"**Duration:** {format_timestamp(metadata['duration'])}")
        report.append("")

        timeline = analysis.get('emotion_analysis', {}).get('timeline', [])

        if timeline:
            report.append("**Emotion Timeline:**")
            report.append("")
            report.append("| Time | Emotion | Confidence |")
            report.append("|------|---------|------------|")
            for event in timeline:
                timestamp = format_timestamp(event['timestamp'])
                emotion = event['emotion'].capitalize()
                confidence = event['confidence']
                report.append(f"| {timestamp} | {emotion} | {confidence:.2f} |")
            report.append("")

        summary = analysis.get('emotion_analysis', {}).get('summary', {})
        if summary:
            report.append(f"**Dominant Emotion:** {summary.get('dominant_emotion', 'N/A').capitalize()}")

            distribution = summary.get('emotion_distribution', {})
            if distribution:
                report.append("")
                report.append("**Emotion Distribution:**")
                for emotion, count in sorted(distribution.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / sum(distribution.values())) * 100
                    report.append(f"- {emotion.capitalize()}: {count} ({percentage:.1f}%)")

        report.append("")
        report.append("---")
        report.append("")

    # Appendix: Full Citation Index
    report.append("## APPENDIX: FULL CITATION INDEX")
    report.append("")
    report.append("Complete reference for all insights in this report.")
    report.append("")

    for video_id, analysis in analyses.items():
        metadata = analysis['metadata']
        participant = extract_participant(metadata['title'])

        report.append(f"### {video_id}")
        report.append("")
        report.append(f"- **Title:** {metadata['title']}")
        report.append(f"- **Participant:** {participant}")
        report.append(f"- **Duration:** {format_timestamp(metadata['duration'])}")
        report.append(f"- **Analyzed:** {metadata['analyzed_at']}")
        report.append(f"- **Full Transcript Available:** Yes")
        report.append(f"- **Analysis File:** `processed/{video_id}/analysis.json`")
        report.append("")

        # Show full transcript
        transcription = analysis.get('transcription', {})
        full_text = transcription.get('full_text', '')

        report.append("**Full Transcript:**")
        report.append("")
        report.append(f"> {full_text}")
        report.append("")
        report.append("---")
        report.append("")

    # Write report
    report_text = "\n".join(report)
    with open(output_path, 'w') as f:
        f.write(report_text)

    print(f"✅ Client report generated: {output_path}")
    print(f"   Total sections: 4 (Executive, Pain Points, Satisfaction, Emotional Journey)")
    print(f"   Total citations: All insights include source, participant, timestamp, verbatim")
    print(f"   Audit trail: Complete in Appendix")

def main():
    """Main entry point"""
    project_root = Path(__file__).parent.parent.parent.parent
    processed_dir = project_root / 'modules' / 'consumer-video' / 'data' / 'processed'
    deliverables_dir = project_root / 'modules' / 'consumer-video' / 'data' / 'deliverables'

    deliverables_dir.mkdir(exist_ok=True)

    output_path = deliverables_dir / 'practice_client_report.md'

    print("="*60)
    print("📊 GENERATING CLIENT DELIVERABLE REPORT")
    print("="*60)
    print()

    generate_report(processed_dir, output_path)

if __name__ == "__main__":
    main()
