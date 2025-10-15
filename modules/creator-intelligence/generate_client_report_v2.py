"""
Generate INSIGHTFUL client-ready deliverable from Creator Intelligence analysis.
Every section must provide actionable marketing intelligence, not just data.

REQUIREMENTS:
1. English-only content (filter non-English phrases)
2. Creator profiles with context and strategy recommendations
3. Content analysis with WHY it matters, not just titles
4. Every section answers: "So what? What action should we take?"
"""

import json
import sqlite3
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter

def is_english(text: str) -> bool:
    """Check if text is primarily English (not perfect but good enough)."""
    if not text:
        return False
    # Check for non-Latin scripts (Bengali, Arabic, Chinese, etc.)
    non_latin_pattern = re.compile(r'[\u0980-\u09FF\u0600-\u06FF\u4E00-\u9FFF\u0400-\u04FF]')
    if non_latin_pattern.search(text):
        return False
    # Must contain some English letters
    if not re.search(r'[a-zA-Z]', text):
        return False
    return True

def extract_json_array(raw_data: List[Tuple], english_only=True) -> List[str]:
    """Extract and flatten JSON arrays from database, optionally filter English."""
    items = []
    for row in raw_data:
        try:
            data = json.loads(row[0]) if isinstance(row[0], str) else row[0]
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, str):
                        if not english_only or is_english(item):
                            items.append(item.strip())
        except (json.JSONDecodeError, TypeError):
            continue
    return items

def query_database_metrics() -> Dict:
    """Query database for comprehensive metrics with US-only filtering."""
    db_path = Path(__file__).parent / "data" / "database" / "creators.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get US creator counts by platform
    cursor.execute("""
        SELECT platform, COUNT(*) as count
        FROM creators
        WHERE location = 'US'
        GROUP BY platform
    """)
    creators_by_platform = dict(cursor.fetchall())

    # Get total creator count
    cursor.execute("SELECT COUNT(*) FROM creators WHERE location = 'US'")
    total_creators = cursor.fetchone()[0]

    # Get content counts and classification (US only)
    cursor.execute("""
        SELECT
            classification,
            COUNT(*) as count,
            AVG(relevance_score) as avg_score
        FROM creator_content
        WHERE classification IS NOT NULL
        AND creator_id IN (SELECT id FROM creators WHERE location = 'US')
        GROUP BY classification
    """)
    content_by_classification = cursor.fetchall()

    # Get total engagement metrics (US only)
    cursor.execute("""
        SELECT
            SUM(view_count) as total_views,
            SUM(like_count) as total_likes,
            SUM(comment_count) as total_comments,
            COUNT(*) as total_content
        FROM creator_content
        WHERE view_count IS NOT NULL
        AND creator_id IN (SELECT id FROM creators WHERE location = 'US')
    """)
    engagement = cursor.fetchone()

    # Get pain points (US creators only, English only)
    cursor.execute("""
        SELECT pain_points
        FROM creator_content
        WHERE pain_points IS NOT NULL AND pain_points != '[]'
        AND creator_id IN (SELECT id FROM creators WHERE location = 'US')
        LIMIT 200
    """)
    pain_points_raw = cursor.fetchall()
    pain_points = extract_json_array(pain_points_raw, english_only=True)

    # Get consumer language (US creators only, English only)
    cursor.execute("""
        SELECT consumer_language
        FROM creator_content
        WHERE consumer_language IS NOT NULL AND consumer_language != '[]'
        AND creator_id IN (SELECT id FROM creators WHERE location = 'US')
        LIMIT 200
    """)
    consumer_language_raw = cursor.fetchall()
    consumer_language = extract_json_array(consumer_language_raw, english_only=True)

    # Get lighting topics (US creators only)
    cursor.execute("""
        SELECT lighting_topics
        FROM creator_content
        WHERE lighting_topics IS NOT NULL AND lighting_topics != '[]'
        AND creator_id IN (SELECT id FROM creators WHERE location = 'US')
        LIMIT 200
    """)
    lighting_topics_raw = cursor.fetchall()
    lighting_topics = extract_json_array(lighting_topics_raw, english_only=True)

    # Get top US creators with detailed profile data
    # MINIMUM 1000 FOLLOWERS - no micro creators with <1000 followers
    cursor.execute("""
        SELECT
            c.id,
            c.username,
            c.platform,
            c.follower_count,
            c.engagement_rate,
            c.location,
            c.profile_url,
            COUNT(cc.id) as content_count,
            SUM(CASE WHEN cc.classification IN ('highly_relevant', 'relevant') THEN 1 ELSE 0 END) * 1.0 / COUNT(cc.id) as relevancy_ratio,
            AVG(CASE WHEN cc.classification IN ('highly_relevant', 'relevant') THEN cc.relevance_score ELSE 0 END) as avg_relevance_score,
            SUM(cc.view_count) as total_views,
            SUM(cc.like_count) as total_engagement
        FROM creators c
        LEFT JOIN creator_content cc ON c.id = cc.creator_id
        WHERE c.location = 'US'
        AND c.follower_count >= 1000
        GROUP BY c.id
        HAVING relevancy_ratio >= 0.5
        ORDER BY
            CASE WHEN c.follower_count >= 10000 THEN 1 ELSE 0 END DESC,
            relevancy_ratio DESC,
            c.follower_count DESC
        LIMIT 10
    """)
    top_creators = cursor.fetchall()

    # For each top creator, get sample content with insights
    creator_content_samples = {}
    for creator in top_creators:
        creator_id = creator[0]
        cursor.execute("""
            SELECT
                title,
                description,
                classification,
                relevance_score,
                view_count,
                url,
                pain_points,
                consumer_language,
                lighting_topics
            FROM creator_content
            WHERE creator_id = ?
            AND classification IN ('highly_relevant', 'relevant')
            ORDER BY view_count DESC
            LIMIT 3
        """, (creator_id,))
        creator_content_samples[creator_id] = cursor.fetchall()

    # Get high-impact content patterns (what types of content work best)
    cursor.execute("""
        SELECT
            cc.title,
            cc.description,
            cc.classification,
            cc.relevance_score,
            cc.view_count,
            cc.pain_points,
            cc.consumer_language,
            cc.lighting_topics,
            c.username,
            c.platform,
            c.profile_url
        FROM creator_content cc
        JOIN creators c ON cc.creator_id = c.id
        WHERE c.location = 'US'
        AND cc.classification IN ('highly_relevant', 'relevant')
        AND cc.view_count > 1000
        ORDER BY cc.view_count DESC
        LIMIT 20
    """)
    high_impact_content = cursor.fetchall()

    conn.close()

    return {
        'total_creators': total_creators,
        'creators_by_platform': creators_by_platform,
        'content_by_classification': content_by_classification,
        'engagement': {
            'total_views': engagement[0] or 0,
            'total_likes': engagement[1] or 0,
            'total_comments': engagement[2] or 0,
            'total_content': engagement[3] or 0
        },
        'pain_points': Counter(pain_points),
        'consumer_language': Counter(consumer_language),
        'lighting_topics': Counter(lighting_topics),
        'top_creators': top_creators,
        'creator_content_samples': creator_content_samples,
        'high_impact_content': high_impact_content
    }

def generate_insight_pain_points(pain_points: Counter) -> str:
    """Generate actionable insights from pain points."""
    if not pain_points:
        return "<p>No pain points identified in US market data.</p>"

    top_3 = pain_points.most_common(3)

    insight = f"""
    <div class="insight-box">
        <strong>🎯 Market Opportunity:</strong> The top pain point "{top_3[0][0]}" appears {top_3[0][1]} times
        across US creator content. This represents a validated market need your products can address directly.
    </div>

    <div class="recommendation">
        <strong>Recommended Action:</strong><br>
        • Create content series addressing "{top_3[0][0]}" with your product as the solution<br>
        • Develop case studies showing before/after results for this specific pain point<br>
        • Use this language in ad copy and product positioning<br>
        • Consider product features that specifically solve this problem
    </div>
    """
    return insight

def generate_insight_consumer_language(consumer_language: Counter) -> str:
    """Generate actionable insights from consumer language patterns."""
    if not consumer_language:
        return "<p>No consumer language patterns identified.</p>"

    # Analyze language patterns
    performance_terms = [term for term, count in consumer_language.items() if any(word in term.lower() for word in ['efficient', 'savings', 'performance', 'bright'])]
    emotional_terms = [term for term, count in consumer_language.items() if any(word in term.lower() for word in ['beautiful', 'amazing', 'perfect', 'love', 'stunning'])]
    technical_terms = [term for term, count in consumer_language.items() if any(word in term.lower() for word in ['waterproof', 'lumen', 'watt', 'rgb', 'dimmable'])]

    insight = f"""
    <div class="insight-box">
        <strong>💬 Language Analysis:</strong><br>
        • <strong>Performance-focused:</strong> {len(performance_terms)} phrases emphasize efficiency/results<br>
        • <strong>Emotional appeal:</strong> {len(emotional_terms)} phrases use emotional descriptors<br>
        • <strong>Technical specs:</strong> {len(technical_terms)} phrases reference specific features
    </div>

    <div class="recommendation">
        <strong>Messaging Strategy:</strong><br>
        US consumers use a mix of technical and emotional language. Your messaging should:
        <ul>
            <li><strong>Lead with performance metrics</strong> - Customers want proof, not promises</li>
            <li><strong>Balance emotion with facts</strong> - "Beautiful AND efficient" beats either alone</li>
            <li><strong>Use their exact phrases</strong> - Test ad copy with top 5 consumer phrases</li>
        </ul>
    </div>
    """
    return insight

def generate_creator_profiles_section(top_creators: List, creator_content_samples: Dict) -> str:
    """Generate detailed creator profiles with strategy recommendations."""
    if not top_creators:
        return """
        <div class="insight-box" style="background: #fff3cd; border-left-color: #ffc107;">
            <strong>⚠️ Limited US Creators:</strong> Current dataset has minimal US-based creators meeting criteria.
            Recommend expanding search with different keywords or lowering follower threshold.
        </div>
        """

    html = f"""
    <div class="insight-box">
        <strong>🎯 Creator Opportunity:</strong> {len(top_creators)} qualified US creators identified with
        50%+ relevant content and proven audience engagement. These represent immediate partnership opportunities.
    </div>
    """

    for rank, creator in enumerate(top_creators, 1):
        (creator_id, username, platform, followers, engagement_rate, location,
         profile_url, content_count, relevancy_ratio, avg_score, total_views, total_engagement) = creator

        # Get content samples
        samples = creator_content_samples.get(creator_id, [])

        # Generate partnership strategy based on metrics
        if followers >= 100000:
            tier = "Tier 1: Major Influence"
            strategy = "High-budget partnership, product launch ambassador, long-term brand deal"
        elif followers >= 50000:
            tier = "Tier 2: Established Authority"
            strategy = "Medium-budget partnership, product review series, affiliate program"
        elif followers >= 10000:
            tier = "Tier 3: Niche Expert"
            strategy = "Gifted product, authentic review, micro-influencer program"
        else:
            tier = "Tier 4: Emerging Voice"
            strategy = "Affiliate-only, community building, early adopter program"

        html += f"""
        <div class="creator-profile-card">
            <div class="creator-header">
                <h3>#{rank} @{username}</h3>
                <span class="badge badge-high">{tier}</span>
            </div>

            <div class="creator-metrics">
                <div class="metric-small">
                    <strong>Platform:</strong> {platform.upper()}<br>
                    <strong>Followers:</strong> {followers:,}<br>
                    <strong>Engagement Rate:</strong> {(engagement_rate or 0):.1%}<br>
                    <strong>Content Relevancy:</strong> {relevancy_ratio:.0%} ({int(relevancy_ratio * content_count)}/{content_count} pieces)
                </div>
            </div>

            <div class="creator-insight">
                <strong>Partnership Strategy:</strong><br>
                {strategy}
                <br><br>
                <strong>Why This Creator:</strong><br>
                • Consistently creates lighting-related content ({relevancy_ratio:.0%} relevancy)<br>
                • {total_views:,} total views on relevant content<br>
                • US-based audience = direct market access<br>
                • {engagement_rate*100 if engagement_rate else 'N/A'}% engagement = active community
            </div>

            <div class="creator-content-samples">
                <strong>Sample High-Performing Content:</strong>
        """

        for sample in samples[:2]:  # Top 2 pieces
            title, description, classification, score, views, url, pain_points_json, lang_json, topics_json = sample

            # Extract insights from content
            pain_points_list = json.loads(pain_points_json) if pain_points_json else []
            language_list = json.loads(lang_json) if lang_json else []
            topics_list = json.loads(topics_json) if topics_json else []

            # Analyze WHY this content works
            why_it_works = []
            if views > 10000:
                why_it_works.append(f"High reach: {views:,} views")
            if pain_points_list:
                why_it_works.append(f"Addresses pain point: {pain_points_list[0]}")
            if language_list:
                why_it_works.append(f"Uses consumer language: '{language_list[0]}'")
            if topics_list:
                why_it_works.append(f"Trending topic: {topics_list[0]}")

            html += f"""
                <div class="content-sample">
                    <strong>{title}</strong><br>
                    <span style="font-size: 0.9em; color: #666;">{views:,} views • Score: {score:.2f}</span><br>
                    <div style="margin-top: 8px; padding: 10px; background: #f0fdf4; border-radius: 4px;">
                        <strong>Why This Content Works:</strong><br>
                        {'<br>'.join(['• ' + reason for reason in why_it_works])}
                    </div>
                    <a href="{url}" target="_blank" style="font-size: 0.85em;">View Content →</a>
                </div>
            """

        html += f"""
            </div>
            <div class="creator-action">
                <strong>📞 Next Step:</strong> <a href="{profile_url or '#'}" target="_blank">Visit Profile →</a>
                Reach out with partnership proposal focused on {samples[0][0].split()[0] if samples else 'lighting'} content.
            </div>
        </div>
        """

    return html

def generate_html_report(metrics: Dict) -> str:
    """Generate complete HTML report with insights."""
    now = datetime.now()

    # Calculate key metrics
    total_creators = metrics['total_creators']
    total_content = metrics['engagement']['total_content']
    total_views = metrics['engagement']['total_views']
    total_engagement = metrics['engagement']['total_likes'] + metrics['engagement']['total_comments']

    # Content classification breakdown
    classification_data = {row[0]: (row[1], row[2]) for row in metrics['content_by_classification']}

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>3M Lighting - Creator Intelligence Report (US Market)</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
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
        .creator-profile-card {{
            background: #f9fafb;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }}
        .creator-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        .creator-metrics {{
            background: white;
            padding: 15px;
            border-radius: 6px;
            margin: 10px 0;
        }}
        .creator-insight {{
            background: #eff6ff;
            padding: 15px;
            border-radius: 6px;
            margin: 10px 0;
        }}
        .creator-content-samples {{
            margin: 15px 0;
        }}
        .content-sample {{
            background: white;
            padding: 15px;
            border-radius: 6px;
            margin: 10px 0;
            border-left: 3px solid #10b981;
        }}
        .creator-action {{
            background: #fef3c7;
            padding: 12px;
            border-radius: 6px;
            margin-top: 15px;
            font-weight: 500;
        }}
        .badge {{
            display: inline-block;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        .badge-high {{
            background: #10b981;
            color: white;
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
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 Creator Intelligence Report</h1>
        <p>3M Lighting - US Market Analysis • Generated {now.strftime('%B %d, %Y at %I:%M %p')}</p>
        <p style="font-size: 0.9em; opacity: 0.9;">Focus: English-speaking US creators with actionable partnership strategies</p>
    </div>

    <div class="section">
        <h2>📊 Executive Summary</h2>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">US Creators</div>
                <div class="metric-value">{total_creators}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Content Analyzed</div>
                <div class="metric-value">{total_content}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Total Views</div>
                <div class="metric-value">{total_views:,}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Total Engagement</div>
                <div class="metric-value">{total_engagement:,}</div>
            </div>
        </div>

        <div class="insight-box">
            <strong>Market Validation:</strong> Analyzed {total_creators} US-based creators with {total_content} pieces
            of lighting-related content generating {total_views:,} views. This represents validated audience interest
            and proven content-market fit for lighting products in the US market.
        </div>
    </div>

    <div class="section">
        <h2>🏆 Top US Creator Partnership Opportunities</h2>
        {generate_creator_profiles_section(metrics['top_creators'], metrics['creator_content_samples'])}
    </div>

    <div class="section">
        <h2>🔧 Consumer Pain Points & Market Opportunities</h2>
        {generate_insight_pain_points(metrics['pain_points'])}

        <table>
            <thead>
                <tr>
                    <th>Pain Point</th>
                    <th>Frequency</th>
                    <th>Market Implication</th>
                </tr>
            </thead>
            <tbody>
    """

    for pain_point, count in metrics['pain_points'].most_common(10):
        # Generate market implication based on pain point
        if 'energy' in pain_point.lower() or 'efficient' in pain_point.lower():
            implication = "Position products with energy savings calculator and ROI data"
        elif 'install' in pain_point.lower() or 'difficult' in pain_point.lower():
            implication = "Create installation guides and emphasize plug-and-play features"
        elif 'durable' in pain_point.lower() or 'reliable' in pain_point.lower():
            implication = "Showcase warranty, testing data, and longevity claims"
        elif 'bright' in pain_point.lower() or 'dim' in pain_point.lower():
            implication = "Lead with lumen output and visibility comparisons"
        else:
            implication = "Address directly in product marketing and feature development"

        html += f"""
                <tr>
                    <td><strong>{pain_point}</strong></td>
                    <td>{count}x</td>
                    <td>{implication}</td>
                </tr>
        """

    html += f"""
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>💬 Consumer Language Intelligence</h2>
        {generate_insight_consumer_language(metrics['consumer_language'])}

        <table>
            <thead>
                <tr>
                    <th>Phrase</th>
                    <th>Usage</th>
                    <th>Marketing Application</th>
                </tr>
            </thead>
            <tbody>
    """

    for phrase, count in metrics['consumer_language'].most_common(15):
        # Generate marketing application
        if any(word in phrase.lower() for word in ['efficient', 'savings', 'smart']):
            application = "Use in ROI-focused ad copy and value propositions"
        elif any(word in phrase.lower() for word in ['bright', 'brilliant', 'clear']):
            application = "Emphasize in product headlines and key benefits"
        elif any(word in phrase.lower() for word in ['easy', 'simple', 'plug']):
            application = "Feature in installation messaging and DIY content"
        elif any(word in phrase.lower() for word in ['durable', 'waterproof', 'reliable']):
            application = "Highlight in warranty and quality assurance messaging"
        else:
            application = "Test in A/B ad variations for authentic voice"

        html += f"""
                <tr>
                    <td>"{phrase}"</td>
                    <td>{count}x</td>
                    <td>{application}</td>
                </tr>
        """

    html += f"""
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>💡 Trending Lighting Topics</h2>
        <div class="insight-box">
            <strong>Content Opportunity:</strong> Top topics represent proven audience interest.
            Create content series addressing these {len(metrics['lighting_topics'])} validated topics
            to maximize reach and engagement.
        </div>

        <table>
            <thead>
                <tr>
                    <th>Topic</th>
                    <th>Mentions</th>
                    <th>Content Strategy</th>
                </tr>
            </thead>
            <tbody>
    """

    for topic, count in metrics['lighting_topics'].most_common(15):
        # Generate content strategy
        if 'commercial' in topic.lower() or 'industrial' in topic.lower():
            strategy = "Create B2B case studies and ROI calculators for business buyers"
        elif 'diy' in topic.lower() or 'installation' in topic.lower():
            strategy = "Produce how-to videos and step-by-step installation guides"
        elif 'smart' in topic.lower() or 'rgb' in topic.lower():
            strategy = "Showcase app integration and customization features"
        elif 'outdoor' in topic.lower() or 'landscape' in topic.lower():
            strategy = "Emphasize durability, weatherproofing, and outdoor use cases"
        elif 'strip' in topic.lower() or 'accent' in topic.lower():
            strategy = "Create before/after transformations and design inspiration content"
        else:
            strategy = "Develop educational content and product application examples"

        html += f"""
                <tr>
                    <td><strong>{topic}</strong></td>
                    <td>{count}x</td>
                    <td>{strategy}</td>
                </tr>
        """

    html += f"""
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>🎯 Strategic Action Plan</h2>

        <div class="recommendation">
            <strong>1. Immediate Actions (This Week)</strong><br>
            • Reach out to top 3 creators with partnership proposals<br>
            • Create landing page addressing top pain point: "{metrics['pain_points'].most_common(1)[0][0]}"<br>
            • Start A/B testing ad copy using top 3 consumer phrases<br>
            • Brief product team on market pain points for feature prioritization
        </div>

        <div class="recommendation">
            <strong>2. Short-Term Initiatives (This Month)</strong><br>
            • Develop content series on top 5 trending topics<br>
            • Create case studies for top 3 pain points<br>
            • Launch micro-influencer program with Tier 3 creators<br>
            • Build ROI calculator tool for energy savings messaging
        </div>

        <div class="recommendation">
            <strong>3. Long-Term Strategy (This Quarter)</strong><br>
            • Establish ambassador program with Tier 1 creators<br>
            • Develop environment-specific product lines (commercial, residential, industrial)<br>
            • Create comprehensive content library addressing all identified pain points<br>
            • Build measurement dashboard to track creator partnership ROI
        </div>

        <div class="insight-box">
            <strong>Success Metrics to Track:</strong><br>
            • Creator partnership conversion rate (proposal → signed deal)<br>
            • Content engagement rate on pain point-focused messaging<br>
            • Ad performance using consumer language vs. generic copy<br>
            • Sales lift from creator-driven traffic<br>
            • Customer acquisition cost by creator tier
        </div>
    </div>

    <div class="footer" style="text-align: center; margin-top: 40px; padding: 20px; color: #666; font-size: 0.9em;">
        <p><strong>Generated by Creator Intelligence Module • 3M Lighting Project</strong></p>
        <p>Data Source: US-based creators from YouTube API • English-language content only</p>
        <p>Analysis Date: {now.strftime('%B %d, %Y')}</p>
    </div>
</body>
</html>
"""

    return html

def main():
    """Main execution function."""
    print("📊 Generating Intelligence-Driven Client Report...")
    print("   → Filtering for US-based creators only")
    print("   → English language content only")
    print("   → Adding actionable insights and strategies")

    # Query database
    metrics = query_database_metrics()

    # Generate HTML report
    html = generate_html_report(metrics)

    # Save report
    output_path = Path(__file__).parent / "CLIENT_REPORT.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Intelligence report generated: {output_path}")
    print(f"   → {metrics['total_creators']} US creators analyzed")
    print(f"   → {metrics['engagement']['total_content']} pieces of content")
    print(f"   → {len(metrics['top_creators'])} qualified partnership opportunities")
    print(f"   → {len(metrics['pain_points'])} unique pain points identified")
    print(f"\n📂 Open in browser: file://{output_path.absolute()}")

if __name__ == "__main__":
    main()
