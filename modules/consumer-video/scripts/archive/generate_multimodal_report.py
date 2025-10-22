#!/usr/bin/env python3
"""
Generate Multimodal Signal Documentation Report
Demonstrates audio (emotion), visual (frames), and text (transcription) signal convergence
"""

import json
import base64
from pathlib import Path
from typing import Dict, List

def encode_image_to_base64(image_path: Path) -> str:
    """Convert image to base64 for embedding in HTML"""
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def find_closest_frame(timestamp: float, frames: List[Dict]) -> Dict:
    """Find the frame closest to a given timestamp"""
    if not frames:
        return None

    closest = min(frames, key=lambda f: abs(f['timestamp'] - timestamp))
    return closest

def generate_multimodal_html():
    """Generate multimodal signal report with embedded images"""

    # Load analysis files
    processed_dir = Path(__file__).parent.parent / 'data' / 'processed'
    analyses = []

    for consumer_dir in sorted(processed_dir.glob('consumer0[1-5]')):
        analysis_file = consumer_dir / 'analysis.json'
        if analysis_file.exists():
            with open(analysis_file) as f:
                analyses.append(json.load(f))

    # Collect key multimodal moments
    multimodal_moments = []

    for analysis in analyses:
        video_id = analysis['metadata']['video_id']
        emotion_segments = analysis.get('emotion_analysis', {}).get('segments', [])
        visual_frames = analysis.get('visual_analysis', {}).get('frames', [])
        jtbd_list = analysis.get('jtbd', [])
        products = analysis.get('products_3m', [])

        # Find high-confidence emotion events
        for seg in emotion_segments:
            if seg.get('confidence', 0) >= 0.7:
                indicators = seg.get('indicators', [])
                if not indicators:
                    continue

                closest_frame = find_closest_frame(seg['timestamp'], visual_frames)

                # Find nearby JTBD or product mention
                nearby_jtbd = None
                for jtbd in jtbd_list:
                    if abs(jtbd['timestamp'] - seg['timestamp']) <= 5.0:
                        nearby_jtbd = jtbd
                        break

                nearby_product = None
                for prod in products:
                    if abs(prod['timestamp'] - seg['timestamp']) <= 5.0:
                        nearby_product = prod
                        break

                multimodal_moments.append({
                    'video_id': video_id,
                    'timestamp': seg['timestamp'],
                    'text': seg['text'],
                    'emotion': indicators[0]['emotion'],
                    'confidence': indicators[0]['confidence'],
                    'acoustic_features': seg.get('acoustic_features', {}),
                    'evidence': indicators[0].get('evidence', []),
                    'visual_frame': closest_frame,
                    'jtbd': nearby_jtbd,
                    'product': nearby_product
                })

    # Sort by confidence (highest first)
    multimodal_moments.sort(key=lambda x: x['confidence'], reverse=True)

    # Generate HTML
    html_lines = []
    html_lines.append('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>3M Multimodal Signal Documentation</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, Helvetica, sans-serif;
            font-size: 10pt;
            line-height: 1.3;
            color: #1a1a1a;
            max-width: 8.5in;
            margin: 0 auto;
            padding: 0.4in;
        }
        h1 {
            font-size: 18pt;
            font-weight: bold;
            color: #0f62fe;
            margin-bottom: 4pt;
            text-align: center;
        }
        h2 {
            font-size: 13pt;
            font-weight: bold;
            color: #0f62fe;
            margin-top: 8pt;
            margin-bottom: 4pt;
            border-bottom: 2px solid #0f62fe;
            padding-bottom: 2pt;
        }
        h3 {
            font-size: 11pt;
            font-weight: bold;
            color: #0353e9;
            margin-top: 6pt;
            margin-bottom: 3pt;
        }
        .header {
            background: linear-gradient(135deg, #0f62fe, #0353e9);
            color: white;
            padding: 8pt;
            text-align: center;
            margin-bottom: 8pt;
        }
        .header h1 { color: white; margin: 0; }
        .header .meta { font-size: 9pt; margin-top: 3pt; }
        .multimodal-card {
            background: #f8f9fa;
            border-left: 4pt solid #0f62fe;
            padding: 6pt;
            margin: 6pt 0;
            page-break-inside: avoid;
        }
        .signal-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 6pt;
            margin: 4pt 0;
        }
        .signal-box {
            background: white;
            border: 1pt solid #e9ecef;
            padding: 4pt;
            border-radius: 3pt;
        }
        .signal-box h4 {
            font-size: 9pt;
            font-weight: bold;
            color: #0f62fe;
            margin-bottom: 2pt;
        }
        .signal-box p {
            font-size: 8pt;
            margin: 1pt 0;
        }
        .frame-img {
            width: 100%;
            max-width: 180pt;
            height: auto;
            border-radius: 3pt;
            margin: 3pt 0;
        }
        .badge {
            display: inline-block;
            padding: 1pt 4pt;
            border-radius: 3pt;
            font-size: 8pt;
            font-weight: bold;
            margin-right: 3pt;
        }
        .badge-emotion { background: #d3f9d8; color: #2b8a3e; }
        .badge-frustration { background: #ffe0e0; color: #c92a2a; }
        .badge-conf { background: #e6f2ff; color: #0353e9; }
        .quote {
            font-style: italic;
            background: white;
            padding: 4pt;
            margin: 3pt 0;
            border-left: 2pt solid #0f62fe;
            font-size: 9pt;
        }
        .prosodic {
            font-family: monospace;
            font-size: 8pt;
            color: #495057;
        }
        .insight {
            background: #fff3bf;
            padding: 4pt;
            margin: 2pt 0;
            font-size: 9pt;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>3M Consumer Lighting: Multimodal Signal Documentation</h1>
        <div class="meta">Demonstrating Audio + Visual + Text Signal Convergence</div>
    </div>

    <h2>Introduction: Three Signal Sources</h2>
    <p>This report demonstrates how offbrain's multimodal analysis captures consumer insights across three simultaneous channels:</p>
    <ul style="margin: 4pt 0 4pt 16pt; font-size: 9pt;">
        <li><strong>Audio Signal:</strong> Emotion detection from prosodic features (pitch variance, energy, speech rate)</li>
        <li><strong>Visual Signal:</strong> Frame analysis showing participant environment and expressions</li>
        <li><strong>Text Signal:</strong> Verbatim transcription capturing exact words and context</li>
    </ul>
    <p style="margin-top: 4pt; font-size: 9pt;">When all three signals align, confidence in the insight increases dramatically. Below are the highest-confidence multimodal moments from 5 consumer interviews.</p>

    <h2>High-Confidence Multimodal Moments</h2>
''')

    # Add multimodal moments (top 10)
    for i, moment in enumerate(multimodal_moments[:10], 1):
        video_id = moment['video_id']
        timestamp = moment['timestamp']
        emotion = moment['emotion']
        confidence = moment['confidence']
        text = moment['text']
        acoustic = moment['acoustic_features']
        evidence = moment['evidence']
        visual_frame = moment['visual_frame']

        # Emotion badge color
        badge_class = 'badge-frustration' if emotion == 'frustration' else 'badge-emotion'

        html_lines.append(f'''
    <div class="multimodal-card">
        <h3>Moment {i}: {video_id.upper()} @ {timestamp:.1f}s <span class="badge {badge_class}">{emotion.title()} {confidence:.0%}</span></h3>

        <div class="quote">"{text}"</div>
''')

        # Signal grid
        html_lines.append('''
        <div class="signal-grid">
''')

        # Audio signal
        pitch_var = acoustic.get('pitch_variance', 0)
        energy = acoustic.get('energy', 0)
        html_lines.append(f'''
            <div class="signal-box">
                <h4>🎵 Audio Signal</h4>
                <p><strong>Emotion:</strong> {emotion.title()}</p>
                <p class="prosodic">Pitch Var: {pitch_var:.0f}</p>
                <p class="prosodic">Energy: {energy:.4f}</p>
                <p style="font-size: 7pt; margin-top: 2pt;">Evidence: {', '.join(evidence[:2])}</p>
            </div>
''')

        # Visual signal
        if visual_frame:
            frame_path = Path(visual_frame['frame_path'])
            if frame_path.exists():
                img_b64 = encode_image_to_base64(frame_path)
                visual_analysis = visual_frame.get('analysis', '')[:150] + '...'
                html_lines.append(f'''
            <div class="signal-box">
                <h4>📹 Visual Signal</h4>
                <img class="frame-img" src="data:image/jpeg;base64,{img_b64}" alt="Frame @ {timestamp:.0f}s">
                <p style="font-size: 7pt;">{visual_analysis}</p>
            </div>
''')
            else:
                html_lines.append('''
            <div class="signal-box">
                <h4>📹 Visual Signal</h4>
                <p>Frame not available</p>
            </div>
''')
        else:
            html_lines.append('''
            <div class="signal-box">
                <h4>📹 Visual Signal</h4>
                <p>No frame at this timestamp</p>
            </div>
''')

        # Text signal (JTBD or product)
        if moment['jtbd']:
            jtbd = moment['jtbd']
            html_lines.append(f'''
            <div class="signal-box">
                <h4>📝 Text Signal (JTBD)</h4>
                <p><strong>Job:</strong> {jtbd.get('verbatim', '')[:80]}</p>
                <p><strong>Category:</strong> {', '.join(jtbd.get('categories', []))}</p>
                <p><strong>Confidence:</strong> {jtbd.get('confidence', 0):.0%}</p>
            </div>
''')
        elif moment['product']:
            prod = moment['product']
            html_lines.append(f'''
            <div class="signal-box">
                <h4>📝 Text Signal (Product)</h4>
                <p><strong>Product:</strong> {prod.get('product_name', 'Unknown')}</p>
                <p><strong>Type:</strong> {prod.get('product_type', '')}</p>
                <p><strong>Verbatim:</strong> "{prod.get('mention_verbatim', '')[:60]}..."</p>
            </div>
''')
        else:
            html_lines.append(f'''
            <div class="signal-box">
                <h4>📝 Text Signal</h4>
                <p>Verbatim transcription with word-level timestamps</p>
                <p style="font-size: 8pt;">"{text}"</p>
            </div>
''')

        html_lines.append('''
        </div>
''')

        # Insight synthesis
        if moment['jtbd'] or moment['product']:
            html_lines.append(f'''
        <div class="insight">
            ✨ Multimodal Convergence: {emotion.title()} emotion (audio) + visual context + {"JTBD" if moment['jtbd'] else "product mention"} (text) = High-confidence insight
        </div>
''')

        html_lines.append('''
    </div>
''')

    # Summary statistics
    total_audio_signals = sum(len(a.get('emotion_analysis', {}).get('timeline', [])) for a in analyses)
    total_visual_frames = sum(a.get('visual_analysis', {}).get('analyzed_frames', 0) for a in analyses)
    total_jtbd = sum(len(a.get('jtbd', [])) for a in analyses)
    total_products = sum(len(a.get('products_3m', [])) for a in analyses)

    html_lines.append(f'''
    <h2>Multimodal Analysis Summary</h2>
    <div class="signal-grid">
        <div class="signal-box">
            <h4>🎵 Audio Analysis</h4>
            <p><strong>{total_audio_signals}</strong> emotion events detected</p>
            <p>Prosodic features: pitch, energy, rate</p>
        </div>
        <div class="signal-box">
            <h4>📹 Visual Analysis</h4>
            <p><strong>{total_visual_frames}</strong> frames analyzed</p>
            <p>LLaVA/Qwen2.5-VL vision model</p>
        </div>
        <div class="signal-box">
            <h4>📝 Text Analysis</h4>
            <p><strong>{total_jtbd}</strong> JTBD instances</p>
            <p><strong>{total_products}</strong> product mentions</p>
        </div>
    </div>

    <div style="text-align: center; font-size: 8pt; color: #666; margin-top: 8pt; padding-top: 6pt; border-top: 1pt solid #e9ecef;">
        <p><strong>3M Multimodal Signal Documentation</strong> | Generated: October 9, 2025 | offbrain video intelligence platform</p>
        <p>Demonstrates Audio (Emotion) + Visual (Frames) + Text (Transcription) signal convergence</p>
    </div>
</body>
</html>
''')

    return '\n'.join(html_lines)

def main():
    """Generate and save multimodal report"""
    print("🎬 Generating Multimodal Signal Documentation Report...")

    html_content = generate_multimodal_html()

    output_path = Path(__file__).parent.parent / 'data' / 'processed' / '3M_Consumer_Insights_Report_Multimodal.html'

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Multimodal report generated: {output_path}")
    print(f"📊 File size: {output_path.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    main()
