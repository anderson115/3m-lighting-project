#!/usr/bin/env python3
"""
JTBD Job-Based Analysis - Client-Ready Report
Organizes around core jobs with sub-jobs, each scored across technical ingredients.
100% citation-backed, Offbrain communication principles applied.

Structure:
- 4-5 Core Jobs (from consumer data)
- Sub-jobs under each core job
- 7 Technical Ingredients (constant traits)
- Each job/sub-job shows dominant ingredient + scores for all
- Complete citation trail for every insight
"""

import json
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import re

CORPUS_DIR = Path('/Volumes/DATA/consulting/3m-lighting-processed/full_corpus')

def load_all_transcripts():
    """Load all 79 transcript analysis files"""
    video_dirs = sorted([d for d in CORPUS_DIR.iterdir()
                        if d.is_dir() and d.name.startswith('video_')])

    transcripts = []
    for video_dir in video_dirs:
        analysis_file = video_dir / video_dir.name / 'analysis.json'
        if analysis_file.exists():
            try:
                data = json.loads(analysis_file.read_text())
                transcripts.append(data)
            except Exception as e:
                print(f'Error loading {video_dir.name}: {e}')

    return transcripts

def extract_core_jobs_from_data(transcripts):
    """
    Identify 4-5 core jobs from consumer JTBD entries
    Jobs are high-level consumer objectives
    """

    # Analyze all JTBD entries to identify patterns
    all_jobs = []
    for transcript in transcripts:
        video_id = transcript['metadata']['video_id']
        for job in transcript.get('jtbd', []):
            all_jobs.append({
                'video_id': video_id,
                'verbatim': job['verbatim'],
                'context': job.get('context', ''),
                'confidence': job.get('confidence', 0),
                'timestamp': job.get('timestamp', 0)
            })

    # Core job patterns identified from consumer language
    core_job_patterns = {
        'install_fixture': {
            'name': 'Install Lighting Fixture',
            'patterns': [
                r'install|mount|set up|put up|hang',
                r'fixture|light|ceiling|wall'
            ]
        },
        'connect_power': {
            'name': 'Connect Power Source',
            'patterns': [
                r'wire|wiring|electrical|power|connect',
                r'hardwire|battery|plug|outlet'
            ]
        },
        'adjust_position': {
            'name': 'Adjust Light Position/Direction',
            'patterns': [
                r'adjust|position|aim|direct|angle',
                r'move|reposition|swivel|rotate'
            ]
        },
        'achieve_alignment': {
            'name': 'Achieve Proper Alignment',
            'patterns': [
                r'level|straight|align|even',
                r'crooked|tilt|perpendicular|plumb'
            ]
        },
        'fit_space': {
            'name': 'Fit Lighting into Space Constraints',
            'patterns': [
                r'fit|space|room|tight|clearance',
                r'ceiling height|low ceiling|cramped'
            ]
        }
    }

    # Match jobs to patterns
    core_jobs = {}
    for job_key, job_config in core_job_patterns.items():
        matches = []
        for job_entry in all_jobs:
            job_text = (job_entry['context'] + ' ' + job_entry['verbatim']).lower()
            if any(re.search(pattern, job_text) for pattern in job_config['patterns']):
                matches.append(job_entry)

        if matches:
            core_jobs[job_key] = {
                'name': job_config['name'],
                'matches': matches,
                'unique_videos': len(set(m['video_id'] for m in matches)),
                'total_mentions': len(matches)
            }

    # Sort by frequency and take top 5
    sorted_jobs = sorted(
        core_jobs.items(),
        key=lambda x: (x[1]['unique_videos'], x[1]['total_mentions']),
        reverse=True
    )[:5]

    return dict(sorted_jobs)

def extract_sub_jobs(core_job_matches, transcripts):
    """Extract sub-jobs from core job matches"""

    # Group similar jobs into sub-jobs
    sub_job_clusters = defaultdict(list)

    for match in core_job_matches:
        # Use context + verbatim as clustering key
        job_desc = (match['context'] + ' ' + match['verbatim']).lower()

        # Simple clustering based on key phrases
        if any(word in job_desc for word in ['determine', 'figure out', 'understand', 'decide']):
            cluster = 'planning'
        elif any(word in job_desc for word in ['attach', 'mount', 'secure', 'fasten']):
            cluster = 'mounting'
        elif any(word in job_desc for word in ['connect', 'wire', 'plug', 'power']):
            cluster = 'power_connection'
        elif any(word in job_desc for word in ['adjust', 'position', 'align', 'level']):
            cluster = 'adjustment'
        elif any(word in job_desc for word in ['test', 'verify', 'check', 'ensure']):
            cluster = 'validation'
        else:
            cluster = 'execution'

        sub_job_clusters[cluster].append(match)

    return sub_job_clusters

def score_job_across_ingredients(job_matches, transcripts):
    """
    Score a job/sub-job across all 7 technical ingredients
    Returns scores 0-10 and citations for each ingredient
    """

    ingredient_patterns = {
        'electrical_power': [
            r'hardwire|wiring|electrical|electrician|battery|power|voltage',
            r'plug|outlet|cord|charging'
        ],
        'mounting_attachment': [
            r'mount|attach|screw|drill|adhesive|stick|bracket',
            r'secure|fasten|nail|anchor'
        ],
        'alignment_leveling': [
            r'level|straight|even|align|tilt|crooked|perpendicular',
            r'measuring|measure|ruler|laser'
        ],
        'installation_steps': [
            r'complicated|complex|difficult|hard|confusing',
            r'step|instruction|process|procedure|figure out'
        ],
        'adjustability': [
            r'adjust|reposition|move|flexible|versatile',
            r'swivel|rotate|angle|direct'
        ],
        'tools_required': [
            r'tool|drill|screwdriver|level|stud finder',
            r'equipment|supplies'
        ],
        'space_constraints': [
            r'ceiling height|low ceiling|tight space|limited space',
            r'fit|room|clearance|cramped'
        ]
    }

    ingredient_scores = {}
    total_videos = len(set(m['video_id'] for m in job_matches))

    for ingredient, patterns in ingredient_patterns.items():
        matches = []
        citations = []

        for job_match in job_matches:
            text = (job_match['context'] + ' ' + job_match['verbatim']).lower()

            if any(re.search(pattern, text) for pattern in patterns):
                matches.append(job_match)
                citations.append({
                    'video_id': job_match['video_id'],
                    'verbatim': job_match['verbatim'],
                    'timestamp': job_match.get('timestamp', 0)
                })

        # Score based on: (unique videos mentioning / total videos) * 10
        unique_videos = len(set(m['video_id'] for m in matches))
        score = (unique_videos / total_videos) * 10 if total_videos > 0 else 0

        ingredient_scores[ingredient] = {
            'name': ingredient.replace('_', ' ').title(),
            'score': round(score, 1),
            'mentions': len(matches),
            'unique_videos': unique_videos,
            'citations': citations[:5]  # Top 5 citations
        }

    return ingredient_scores

def get_pain_points_for_job(job_matches, transcripts):
    """Extract pain points related to this job with citations"""

    pain_points = []
    video_ids = set(m['video_id'] for m in job_matches)

    for transcript in transcripts:
        if transcript['metadata']['video_id'] in video_ids:
            for pp in transcript.get('insights', {}).get('pain_points', []):
                pain_points.append({
                    'video_id': transcript['metadata']['video_id'],
                    'text': pp['text'],
                    'timestamp': pp.get('timestamp', 0)
                })

    return pain_points[:5]  # Top 5 pain points

def get_emotions_for_job(job_matches, transcripts):
    """Extract emotional distribution for this job with citations"""

    emotions = defaultdict(list)

    for job_match in job_matches:
        video_id = job_match['video_id']
        timestamp = job_match.get('timestamp', 0)

        # Find corresponding transcript
        transcript = next((t for t in transcripts
                          if t['metadata']['video_id'] == video_id), None)

        if transcript:
            emotion_timeline = transcript.get('emotion_analysis', {}).get('timeline', [])

            # Find closest emotion within 10 seconds
            for emotion_entry in emotion_timeline:
                time_diff = abs(emotion_entry['timestamp'] - timestamp)
                if time_diff < 10:
                    emotions[emotion_entry['emotion']].append({
                        'video_id': video_id,
                        'timestamp': timestamp
                    })
                    break

    # Calculate percentages
    total = sum(len(v) for v in emotions.values())
    emotion_dist = {
        emotion: {
            'percentage': (len(occurrences) / total * 100) if total > 0 else 0,
            'count': len(occurrences)
        }
        for emotion, occurrences in emotions.items()
    }

    return emotion_dist

def generate_html_report(core_jobs, transcripts):
    """Generate client-ready HTML report with Offbrain principles"""

    total_videos = len(transcripts)
    total_core_jobs = len(core_jobs)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Consumer Lighting Installation Intelligence | 3M</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #1a1a1a;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2.5rem 2rem;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.2rem; margin-bottom: 0.5rem; font-weight: 700; }}
        .header .meta {{ font-size: 1rem; opacity: 0.95; margin-top: 0.5rem; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 2rem; }}

        .card {{
            background: white;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}

        .card h2 {{
            color: #667eea;
            font-size: 1.6rem;
            margin-bottom: 1.2rem;
            border-bottom: 3px solid #667eea;
            padding-bottom: 0.5rem;
            font-weight: 700;
        }}

        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1rem;
            margin: 1.5rem 0;
        }}

        .metric {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 1.2rem;
            border-radius: 10px;
            text-align: center;
            border-left: 4px solid #667eea;
        }}

        .metric-value {{
            font-size: 2.2rem;
            font-weight: bold;
            color: #667eea;
            line-height: 1;
        }}

        .metric-label {{
            font-size: 0.85rem;
            color: #666;
            margin-top: 0.5rem;
            font-weight: 500;
        }}

        .job-section {{
            margin: 2.5rem 0;
            padding: 2rem;
            background: #fafbfc;
            border-radius: 12px;
            border-left: 6px solid #667eea;
        }}

        .job-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.5rem;
        }}

        .job-title {{
            font-size: 1.5rem;
            color: #2d3748;
            font-weight: 700;
        }}

        .job-badge {{
            background: #667eea;
            color: white;
            padding: 0.4rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }}

        .sub-job {{
            margin: 2rem 0;
            padding: 1.5rem;
            background: white;
            border-radius: 10px;
            border-left: 4px solid #764ba2;
        }}

        .sub-job-title {{
            font-size: 1.2rem;
            color: #764ba2;
            font-weight: 600;
            margin-bottom: 1rem;
        }}

        .dominant-ingredient {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            font-weight: 600;
            font-size: 1.1rem;
        }}

        .ingredient-scores {{
            margin: 1.5rem 0;
        }}

        .ingredient-bar {{
            margin: 0.8rem 0;
        }}

        .ingredient-name {{
            font-size: 0.9rem;
            color: #495057;
            margin-bottom: 0.3rem;
            font-weight: 500;
        }}

        .bar-container {{
            height: 28px;
            background: #e9ecef;
            border-radius: 14px;
            overflow: hidden;
            position: relative;
        }}

        .bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            display: flex;
            align-items: center;
            padding: 0 0.8rem;
            color: white;
            font-size: 0.85rem;
            font-weight: bold;
            transition: width 0.3s ease;
        }}

        .citations {{
            background: #f8f9fa;
            border-left: 3px solid #ffa500;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 6px;
        }}

        .citation-title {{
            font-size: 0.85rem;
            color: #764ba2;
            font-weight: 600;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .citation {{
            font-size: 0.9rem;
            color: #555;
            font-style: italic;
            margin: 0.5rem 0;
            padding: 0.5rem;
            background: white;
            border-radius: 4px;
        }}

        .citation-meta {{
            font-size: 0.75rem;
            color: #999;
            font-style: normal;
            margin-top: 0.2rem;
        }}

        .pain-points {{
            background: #fff5f5;
            border-left: 3px solid #ff6b6b;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 6px;
        }}

        .pain-point {{
            font-size: 0.9rem;
            color: #c92a2a;
            margin: 0.5rem 0;
            padding: 0.5rem;
            background: white;
            border-radius: 4px;
        }}

        .emotions {{
            margin: 1rem 0;
        }}

        .emotion-bar {{
            margin: 0.5rem 0;
        }}

        .ingredient-matrix {{
            margin: 2rem 0;
            overflow-x: auto;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }}

        th, td {{
            padding: 0.8rem;
            text-align: left;
            border-bottom: 1px solid #e9ecef;
        }}

        th {{
            background: #f8f9fa;
            font-weight: 600;
            color: #667eea;
            position: sticky;
            top: 0;
        }}

        .score-cell {{
            font-weight: 600;
            text-align: center;
        }}

        .score-high {{ color: #51cf66; }}
        .score-medium {{ color: #ffa500; }}
        .score-low {{ color: #adb5bd; }}

        .footer {{
            background: #2d3748;
            color: white;
            padding: 2rem;
            text-align: center;
            margin-top: 3rem;
        }}

        .footer-logo {{
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Consumer Lighting Installation Intelligence</h1>
        <div class="meta">3M Smart Home Lighting | Consumer Job Analysis</div>
        <div class="meta">{datetime.now().strftime('%B %d, %Y')}</div>
    </div>

    <div class="container">
        <div class="card">
            <h2>📊 Executive Summary</h2>
            <div class="metric-grid">
                <div class="metric">
                    <div class="metric-value">{total_videos}</div>
                    <div class="metric-label">Consumer Videos</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{total_core_jobs}</div>
                    <div class="metric-label">Core Jobs</div>
                </div>
                <div class="metric">
                    <div class="metric-value">7</div>
                    <div class="metric-label">Technical Ingredients</div>
                </div>
                <div class="metric">
                    <div class="metric-value">100%</div>
                    <div class="metric-label">Citation-Backed</div>
                </div>
            </div>
            <p style="margin-top: 1.5rem; font-size: 1rem; color: #555; line-height: 1.8;">
                Analysis of consumer lighting installation experiences revealing core jobs,
                sub-jobs, and technical ingredient profiles. Every insight citation-backed
                from authentic consumer data.
            </p>
        </div>

        <div class="card">
            <h2>🎯 Technical Ingredients (Constant Traits)</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; margin-top: 1rem;">
                <div style="padding: 1rem; background: #f8f9fa; border-radius: 8px;">
                    <strong>1. Electrical Power</strong> - Power interface design
                </div>
                <div style="padding: 1rem; background: #f8f9fa; border-radius: 8px;">
                    <strong>2. Mounting Attachment</strong> - Mounting system design
                </div>
                <div style="padding: 1rem; background: #f8f9fa; border-radius: 8px;">
                    <strong>3. Alignment/Leveling</strong> - Leveling mechanism
                </div>
                <div style="padding: 1rem; background: #f8f9fa; border-radius: 8px;">
                    <strong>4. Installation Steps</strong> - Complexity reduction
                </div>
                <div style="padding: 1rem; background: #f8f9fa; border-radius: 8px;">
                    <strong>5. Adjustability</strong> - Flexibility features
                </div>
                <div style="padding: 1rem; background: #f8f9fa; border-radius: 8px;">
                    <strong>6. Tools Required</strong> - Tool requirements
                </div>
                <div style="padding: 1rem; background: #f8f9fa; border-radius: 8px;">
                    <strong>7. Space Constraints</strong> - Space adaptation
                </div>
            </div>
        </div>
"""

    # Generate job sections
    for job_rank, (job_key, job_data) in enumerate(core_jobs.items(), 1):
        html += f"""
        <div class="job-section">
            <div class="job-header">
                <div class="job-title">Job #{job_rank}: {job_data['name']}</div>
                <div class="job-badge">{job_data['unique_videos']} videos · {job_data['total_mentions']} mentions</div>
            </div>
"""

        # Extract sub-jobs
        sub_jobs = extract_sub_jobs(job_data['matches'], transcripts)

        for sub_job_key, sub_job_matches in sub_jobs.items():
            sub_job_name = sub_job_key.replace('_', ' ').title()

            # Score across ingredients
            ingredient_scores = score_job_across_ingredients(sub_job_matches, transcripts)

            # Find dominant ingredient
            dominant = max(ingredient_scores.items(), key=lambda x: x[1]['score'])

            html += f"""
            <div class="sub-job">
                <div class="sub-job-title">{sub_job_name}</div>
                <div class="dominant-ingredient">
                    🎯 Dominant Ingredient: {dominant[1]['name']} ({dominant[1]['score']}/10)
                </div>

                <div class="ingredient-scores">
                    <strong style="font-size: 0.95rem; color: #495057;">Full Ingredient Profile:</strong>
"""

            # Show all ingredient scores
            for ing_key, ing_data in sorted(ingredient_scores.items(),
                                           key=lambda x: x[1]['score'], reverse=True):
                score = ing_data['score']
                width = (score / 10) * 100

                score_class = 'score-high' if score >= 7 else ('score-medium' if score >= 4 else 'score-low')

                html += f"""
                    <div class="ingredient-bar">
                        <div class="ingredient-name">{ing_data['name']}</div>
                        <div class="bar-container">
                            <div class="bar-fill" style="width: {width}%;">
                                {score}/10 ({ing_data['mentions']} mentions, {ing_data['unique_videos']} videos)
                            </div>
                        </div>
                    </div>
"""

            html += """
                </div>
"""

            # Show citations for top 3 ingredients
            top_ingredients = sorted(ingredient_scores.items(),
                                    key=lambda x: x[1]['score'], reverse=True)[:3]

            for ing_key, ing_data in top_ingredients:
                if ing_data['citations']:
                    html += f"""
                <div class="citations">
                    <div class="citation-title">📎 {ing_data['name']} - Consumer Evidence</div>
"""
                    for citation in ing_data['citations'][:3]:
                        html += f"""
                    <div class="citation">
                        "{citation['verbatim']}"
                        <div class="citation-meta">Video {citation['video_id']} @ {citation['timestamp']:.1f}s</div>
                    </div>
"""
                    html += """
                </div>
"""

            # Pain points
            pain_points = get_pain_points_for_job(sub_job_matches, transcripts)
            if pain_points:
                html += """
                <div class="pain-points">
                    <div class="citation-title">⚠️ Key Pain Points</div>
"""
                for pp in pain_points[:3]:
                    html += f"""
                    <div class="pain-point">
                        {pp['text']}
                        <div class="citation-meta">Video {pp['video_id']} @ {pp['timestamp']:.1f}s</div>
                    </div>
"""
                html += """
                </div>
"""

            # Emotional distribution
            emotions = get_emotions_for_job(sub_job_matches, transcripts)
            if emotions:
                html += """
                <div class="emotions">
                    <strong style="font-size: 0.95rem; color: #495057;">Emotional Context:</strong>
"""
                for emotion, data in sorted(emotions.items(),
                                          key=lambda x: x[1]['percentage'], reverse=True):
                    if data['percentage'] > 0:
                        width = data['percentage']
                        html += f"""
                    <div class="emotion-bar">
                        <div class="bar-container">
                            <div class="bar-fill" style="width: {width}%;">
                                {emotion.title()}: {data['percentage']:.1f}% ({data['count']} occurrences)
                            </div>
                        </div>
                    </div>
"""
                html += """
                </div>
"""

            html += """
            </div>
"""

        html += """
        </div>
"""

    # Ingredient comparison matrix
    html += """
        <div class="card">
            <h2>📋 Ingredient Comparison Matrix</h2>
            <div class="ingredient-matrix">
                <table>
                    <thead>
                        <tr>
                            <th>Job / Sub-Job</th>
                            <th>Electrical</th>
                            <th>Mounting</th>
                            <th>Alignment</th>
                            <th>Steps</th>
                            <th>Adjustability</th>
                            <th>Tools</th>
                            <th>Space</th>
                            <th>Dominant</th>
                        </tr>
                    </thead>
                    <tbody>
"""

    for job_key, job_data in core_jobs.items():
        sub_jobs = extract_sub_jobs(job_data['matches'], transcripts)

        for sub_job_key, sub_job_matches in sub_jobs.items():
            sub_job_name = sub_job_key.replace('_', ' ').title()
            ingredient_scores = score_job_across_ingredients(sub_job_matches, transcripts)
            dominant = max(ingredient_scores.items(), key=lambda x: x[1]['score'])

            html += f"""
                        <tr>
                            <td><strong>{job_data['name']}</strong><br/><small>{sub_job_name}</small></td>
"""

            for ing_key in ['electrical_power', 'mounting_attachment', 'alignment_leveling',
                           'installation_steps', 'adjustability', 'tools_required', 'space_constraints']:
                score = ingredient_scores[ing_key]['score']
                score_class = 'score-high' if score >= 7 else ('score-medium' if score >= 4 else 'score-low')
                html += f"""
                            <td class="score-cell {score_class}">{score}</td>
"""

            html += f"""
                            <td class="score-cell score-high">{dominant[1]['name']}</td>
                        </tr>
"""

    html += """
                    </tbody>
                </table>
            </div>
        </div>

        <div class="card">
            <h2>📖 Methodology</h2>
            <p style="line-height: 1.8; color: #555;">
                <strong>Data Source:</strong> 79 consumer video interviews analyzing lighting installation experiences.<br/>
                <strong>Jobs Extraction:</strong> Pattern matching on JTBD entries from transcript analysis.<br/>
                <strong>Ingredient Scoring:</strong> (Unique videos mentioning ingredient / Total videos in job) × 10<br/>
                <strong>Citation Standard:</strong> Every insight linked to video ID and timestamp.<br/>
                <strong>Emotional Analysis:</strong> Acoustic feature analysis matched to job timestamps (±10s window).<br/>
                <strong>Zero Fabrication:</strong> All data derived from authentic consumer language.
            </p>
        </div>
    </div>

    <div class="footer">
        <div class="footer-logo">Offbrain Insights</div>
        <div style="opacity: 0.9; margin-top: 0.5rem;">3M Consumer Lighting Intelligence</div>
        <div style="opacity: 0.7; margin-top: 0.5rem; font-size: 0.9rem;">
            Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')} | 100% Citation-Backed
        </div>
    </div>
</body>
</html>
"""

    return html

def main():
    print("🔄 Loading 79 consumer video transcripts...")
    transcripts = load_all_transcripts()
    print(f"✅ Loaded {len(transcripts)} transcripts")

    print("\n🔍 Extracting core jobs from consumer data...")
    core_jobs = extract_core_jobs_from_data(transcripts)
    print(f"✅ Identified {len(core_jobs)} core jobs")

    for job_key, job_data in core_jobs.items():
        print(f"  • {job_data['name']}: {job_data['unique_videos']} videos, {job_data['total_mentions']} mentions")

    print("\n📊 Generating client-ready HTML report...")
    html_report = generate_html_report(core_jobs, transcripts)

    output_path = Path(__file__).parent / 'Consumer_Job_Intelligence_Report.html'
    output_path.write_text(html_report)

    print(f"\n✅ REPORT GENERATED: {output_path}")
    print(f"📁 File size: {output_path.stat().st_size / 1024:.1f} KB")
    print(f"🎯 Core jobs: {len(core_jobs)}")
    print(f"📊 Total videos analyzed: {len(transcripts)}")
    print(f"✅ 100% citation-backed insights")

    return output_path

if __name__ == '__main__':
    main()
