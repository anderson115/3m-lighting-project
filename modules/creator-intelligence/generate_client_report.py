"""
Generate client-ready deliverable from Creator Intelligence analysis.
Produces HTML report with insights, metrics, and recommendations.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import sys

def load_analysis_results(json_path: str) -> Dict:
    """Load analysis results from JSON."""
    with open(json_path, 'r') as f:
        return json.load(f)

def query_database_metrics() -> Dict:
    """Query database for comprehensive metrics."""
    db_path = Path(__file__).parent / "data" / "database" / "creators.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get creator counts by platform
    cursor.execute("""
        SELECT platform, COUNT(*) as count
        FROM creators
        GROUP BY platform
    """)
    creators_by_platform = dict(cursor.fetchall())

    # Get content counts and classification
    cursor.execute("""
        SELECT
            classification,
            COUNT(*) as count,
            AVG(relevance_score) as avg_score
        FROM creator_content
        WHERE classification IS NOT NULL
        GROUP BY classification
    """)
    content_by_classification = cursor.fetchall()

    # Get total engagement metrics
    cursor.execute("""
        SELECT
            SUM(view_count) as total_views,
            SUM(like_count) as total_likes,
            SUM(comment_count) as total_comments,
            COUNT(*) as total_content
        FROM creator_content
        WHERE view_count IS NOT NULL
    """)
    engagement = cursor.fetchone()

    # Get pain points (most common) - US creators only
    cursor.execute("""
        SELECT pain_points
        FROM creator_content
        WHERE pain_points IS NOT NULL AND pain_points != '[]'
        AND creator_id IN (SELECT id FROM creators WHERE location = 'US')
        LIMIT 100
    """)
    pain_points_raw = cursor.fetchall()

    # Get consumer language (most common) - US creators only
    cursor.execute("""
        SELECT consumer_language
        FROM creator_content
        WHERE consumer_language IS NOT NULL AND consumer_language != '[]'
        AND creator_id IN (SELECT id FROM creators WHERE location = 'US')
        LIMIT 100
    """)
    consumer_language_raw = cursor.fetchall()

    # Get lighting topics - US creators only
    cursor.execute("""
        SELECT lighting_topics
        FROM creator_content
        WHERE lighting_topics IS NOT NULL AND lighting_topics != '[]'
        AND creator_id IN (SELECT id FROM creators WHERE location = 'US')
        LIMIT 100
    """)
    lighting_topics_raw = cursor.fetchall()

    # Get top creators with relevancy-weighted scoring
    # Priority: US-only, 10k+ followers, high content relevancy
    cursor.execute("""
        SELECT
            c.username,
            c.platform,
            c.follower_count,
            c.engagement_rate,
            c.location,
            (COALESCE(c.research_viability_score, 0) + COALESCE(c.partnership_viability_score, 0)) as viability_score,
            COUNT(cc.id) as content_count,
            SUM(CASE WHEN cc.classification IN ('highly_relevant', 'relevant') THEN 1 ELSE 0 END) * 1.0 / COUNT(cc.id) as relevancy_ratio,
            AVG(CASE WHEN cc.classification IN ('highly_relevant', 'relevant') THEN cc.relevance_score ELSE 0 END) as avg_relevance_score
        FROM creators c
        LEFT JOIN creator_content cc ON c.id = cc.creator_id
        WHERE c.location = 'US'
        AND c.follower_count >= 10000
        GROUP BY c.id
        HAVING relevancy_ratio >= 0.5
        ORDER BY
            relevancy_ratio DESC,
            viability_score DESC,
            c.follower_count DESC
        LIMIT 10
    """)
    top_creators = cursor.fetchall()

    # Get sample content titles
    cursor.execute("""
        SELECT title, classification, relevance_score, view_count
        FROM creator_content
        WHERE title IS NOT NULL AND classification = 'highly_relevant'
        ORDER BY relevance_score DESC
        LIMIT 10
    """)
    sample_content = cursor.fetchall()

    conn.close()

    # Parse JSON arrays
    def parse_json_array(rows):
        items = []
        for row in rows:
            try:
                parsed = json.loads(row[0])
                items.extend(parsed)
            except:
                pass
        return items

    pain_points = parse_json_array(pain_points_raw)
    consumer_language = parse_json_array(consumer_language_raw)
    lighting_topics = parse_json_array(lighting_topics_raw)

    # Count frequencies
    from collections import Counter
    pain_points_freq = Counter(pain_points).most_common(10)
    consumer_language_freq = Counter(consumer_language).most_common(10)
    lighting_topics_freq = Counter(lighting_topics).most_common(10)

    return {
        'creators_by_platform': creators_by_platform,
        'content_by_classification': content_by_classification,
        'engagement': {
            'total_views': engagement[0] or 0,
            'total_likes': engagement[1] or 0,
            'total_comments': engagement[2] or 0,
            'total_content': engagement[3] or 0
        },
        'pain_points': pain_points_freq,
        'consumer_language': consumer_language_freq,
        'lighting_topics': lighting_topics_freq,
        'top_creators': top_creators,
        'sample_content': sample_content
    }

def generate_html_report(metrics: Dict, output_path: str):
    """Generate comprehensive HTML report."""

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>3M Lighting - Creator Intelligence Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #f5f5f5;
            color: #333;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0 0 10px 0;
            font-size: 2.5em;
        }}
        .header p {{
            margin: 0;
            opacity: 0.9;
        }}
        .section {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h2 {{
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }}
        .metric-label {{
            opacity: 0.9;
            font-size: 0.9em;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #667eea;
            color: white;
            font-weight: 600;
        }}
        tr:hover {{
            background: #f5f5f5;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 500;
        }}
        .badge-high {{
            background: #10b981;
            color: white;
        }}
        .badge-medium {{
            background: #f59e0b;
            color: white;
        }}
        .badge-low {{
            background: #ef4444;
            color: white;
        }}
        .insight-box {{
            background: #eff6ff;
            border-left: 4px solid #3b82f6;
            padding: 15px 20px;
            margin: 15px 0;
            border-radius: 4px;
        }}
        .recommendation {{
            background: #f0fdf4;
            border-left: 4px solid #10b981;
            padding: 15px 20px;
            margin: 15px 0;
            border-radius: 4px;
        }}
        .list-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .list-card {{
            background: #f9fafb;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #e5e7eb;
        }}
        .list-card h3 {{
            margin-top: 0;
            color: #667eea;
        }}
        .list-card ul {{
            margin: 10px 0;
            padding-left: 20px;
        }}
        .list-card li {{
            margin: 8px 0;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 Creator Intelligence Report</h1>
        <p>3M Lighting Industry Analysis • Generated {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
    </div>

    <div class="section">
        <h2>📊 Executive Summary</h2>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Total Creators</div>
                <div class="metric-value">{sum(metrics['creators_by_platform'].values())}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Content Analyzed</div>
                <div class="metric-value">{metrics['engagement']['total_content']:,}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Total Views</div>
                <div class="metric-value">{metrics['engagement']['total_views']:,.0f}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Total Engagement</div>
                <div class="metric-value">{(metrics['engagement']['total_likes'] + metrics['engagement']['total_comments']):,.0f}</div>
            </div>
        </div>

        <div class="insight-box">
            <strong>Key Insight:</strong> Analyzed {sum(metrics['creators_by_platform'].values())} creators across {len(metrics['creators_by_platform'])} platforms,
            identifying high-relevance content with {metrics['engagement']['total_views']:,.0f} cumulative views.
        </div>
    </div>

    <div class="section">
        <h2>🎨 Content Classification</h2>
        <table>
            <thead>
                <tr>
                    <th>Classification</th>
                    <th>Count</th>
                    <th>Avg Relevance Score</th>
                    <th>Badge</th>
                </tr>
            </thead>
            <tbody>
"""

    for classification, count, avg_score in metrics['content_by_classification']:
        badge_class = 'badge-high' if avg_score > 0.7 else 'badge-medium' if avg_score > 0.4 else 'badge-low'
        html += f"""
                <tr>
                    <td>{classification.replace('_', ' ').title()}</td>
                    <td>{count}</td>
                    <td>{avg_score:.2f}</td>
                    <td><span class="badge {badge_class}">{avg_score:.0%}</span></td>
                </tr>
"""

    html += """
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>🏆 Top US Creators (10k+ Followers)</h2>
"""

    # Warning if insufficient qualified creators
    if len(metrics['top_creators']) < 10:
        html += f"""
        <div class="insight-box" style="background: #fff3cd; border-left-color: #ffc107;">
            <strong>⚠️ Limited Qualified Creators:</strong> Only {len(metrics['top_creators'])} creators meet criteria (US-based, 10k+ followers, 50%+ relevant content).
            Consider expanding search or lowering follower threshold for more prospects.
        </div>
"""

    html += """
        <table>
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Username</th>
                    <th>Platform</th>
                    <th>Followers</th>
                    <th>Relevancy</th>
                    <th>Content Count</th>
                    <th>Avg Score</th>
                    <th>Engagement</th>
                </tr>
            </thead>
            <tbody>
"""

    for i, (username, platform, followers, engagement, location, viability_score, content_count, relevancy_ratio, avg_relevance) in enumerate(metrics['top_creators'], 1):
        engagement_display = f"{engagement:.2%}" if engagement is not None else "N/A"
        followers_display = f"{followers:,}" if followers is not None else "N/A"
        relevancy_display = f"{relevancy_ratio:.0%}" if relevancy_ratio is not None else "N/A"
        html += f"""
                <tr>
                    <td><strong>#{i}</strong></td>
                    <td>{username}</td>
                    <td>{platform.upper()}</td>
                    <td>{followers_display}</td>
                    <td><span class="badge badge-high">{relevancy_display}</span></td>
                    <td>{content_count}</td>
                    <td>{avg_relevance:.2f}</td>
                    <td>{engagement_display}</td>
                </tr>
"""

    html += """
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>💡 Consumer Insights</h2>
        <div class="list-grid">
            <div class="list-card">
                <h3>🔧 Pain Points</h3>
                <ul>
"""

    for pain_point, count in metrics['pain_points'][:10]:
        html += f"                    <li>{pain_point} <em>({count})</em></li>\n"

    html += """
                </ul>
            </div>

            <div class="list-card">
                <h3>💬 Consumer Language</h3>
                <ul>
"""

    for phrase, count in metrics['consumer_language'][:10]:
        html += f"                    <li>\"{phrase}\" <em>({count})</em></li>\n"

    html += """
                </ul>
            </div>

            <div class="list-card">
                <h3>💡 Lighting Topics</h3>
                <ul>
"""

    for topic, count in metrics['lighting_topics'][:10]:
        html += f"                    <li>{topic} <em>({count})</em></li>\n"

    html += """
                </ul>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>📹 Sample High-Relevance Content</h2>
        <table>
            <thead>
                <tr>
                    <th>Title</th>
                    <th>Classification</th>
                    <th>Score</th>
                    <th>Views</th>
                </tr>
            </thead>
            <tbody>
"""

    for title, classification, score, views in metrics['sample_content']:
        html += f"""
                <tr>
                    <td>{title}</td>
                    <td><span class="badge badge-high">{classification.replace('_', ' ').title()}</span></td>
                    <td>{score:.2f}</td>
                    <td>{views:,}</td>
                </tr>
"""

    html += """
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>🎯 Actionable Marketing Insights</h2>

        <div class="recommendation">
            <strong>1. Lead with Quantifiable Performance Benefits</strong><br>
            US creators consistently emphasize measurable outcomes: "major energy savings", "improved ball tracking", "brilliant illumination".
            <strong>Action:</strong> Position products using specific performance metrics (lumens, energy efficiency %, glare reduction) rather than abstract quality claims.
        </div>

        <div class="recommendation">
            <strong>2. Address Professional-Grade Installation Complexity</strong><br>
            Top pain points reveal DIY and professional installers struggle with "complexity of microcontroller-based LED control" and "difficult installation".
            <strong>Action:</strong> Create step-by-step installation content, highlight plug-and-play features, develop "installation confidence" messaging to overcome purchase hesitation.
        </div>

        <div class="recommendation">
            <strong>3. Use Technical-Professional Hybrid Language</strong><br>
            US market uses phrases like "uniform, glare free illumination", "edge-to-edge clarity", "waterproof" - technical enough to convey quality but accessible enough for consumers.
            <strong>Action:</strong> Avoid overly simplified marketing speak. Test messaging that balances technical credibility with consumer understanding.
        </div>

        <div class="recommendation">
            <strong>4. Durability & Environment-Specific Positioning</strong><br>
            "Durability in harsh environments" appears as top concern alongside interest in "dock lighting", "commercial lighting", "industrial lighting".
            <strong>Action:</strong> Develop environment-specific product lines (marine, commercial, residential) with durability testing narratives. Create case studies showing real-world performance.
        </div>

        <div class="recommendation">
            <strong>5. Leverage "Smart Investment" Economics Framing</strong><br>
            US consumers use phrases like "smart investment" and "energy-efficient" - they're cost-conscious but value-focused.
            <strong>Action:</strong> Position premium products with ROI calculators, total cost of ownership comparisons, and energy savings projections to justify higher price points.
        </div>
    </div>

    <div class="footer">
        <p>Generated by Creator Intelligence Module • 3M Lighting Project</p>
        <p>Data collected from YouTube, Instagram, TikTok, and Etsy APIs</p>
    </div>
</body>
</html>
"""

    with open(output_path, 'w') as f:
        f.write(html)

    print(f"✅ Client report generated: {output_path}")

if __name__ == "__main__":
    print("📊 Generating Client-Ready Report...")

    # Query database for metrics
    metrics = query_database_metrics()

    # Generate HTML report
    output_path = Path(__file__).parent / "CLIENT_REPORT.html"
    generate_html_report(metrics, str(output_path))

    print(f"✅ Report available at: {output_path}")
    print(f"📂 Open in browser: file://{output_path}")
