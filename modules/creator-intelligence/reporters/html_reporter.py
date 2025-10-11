"""
HTML report generator for Creator Intelligence Module.
Generates comprehensive, visually formatted reports.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class HTMLReporter:
    """Generates formatted HTML reports for creator intelligence analysis."""

    def __init__(self, database):
        """
        Initialize HTML reporter.

        Args:
            database: CreatorDatabase instance
        """
        self.db = database
        logger.info("✅ HTMLReporter initialized")

    def generate_report(
        self,
        output_path: str = "data/reports/creator_intelligence_report.html",
        analysis_summary: Optional[Dict] = None
    ) -> str:
        """
        Generate comprehensive HTML report.

        Args:
            output_path: Path for output HTML file
            analysis_summary: Optional analysis summary data

        Returns:
            Path to generated report
        """
        logger.info(f"📊 Generating HTML report: {output_path}")

        # Get data
        stats = self.db.get_stats()
        top_research = self.db.get_creators_by_score('research', min_score=0, limit=20)
        top_partnership = self.db.get_creators_by_score('partnership', min_score=0, limit=20)
        consumer_language = self.db.get_consumer_language_by_category(min_frequency=2)

        # Generate HTML
        html = self._generate_html(
            stats=stats,
            top_research=top_research,
            top_partnership=top_partnership,
            consumer_language=consumer_language,
            analysis_summary=analysis_summary
        )

        # Write to file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(html)

        logger.info(f"✅ Report generated: {output_path}")
        return str(output_file)

    def _generate_html(
        self,
        stats: Dict,
        top_research: List[Dict],
        top_partnership: List[Dict],
        consumer_language: List[Dict],
        analysis_summary: Optional[Dict]
    ) -> str:
        """Generate HTML content."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Creator Intelligence Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            color: #333;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 48px;
            font-weight: 700;
            margin-bottom: 10px;
        }}

        .header .subtitle {{
            font-size: 18px;
            opacity: 0.9;
        }}

        .content {{
            padding: 40px;
        }}

        .section {{
            margin-bottom: 50px;
        }}

        .section-title {{
            font-size: 32px;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 3px solid #667eea;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }}

        .stat-card .stat-value {{
            font-size: 48px;
            font-weight: 700;
            margin-bottom: 10px;
        }}

        .stat-card .stat-label {{
            font-size: 16px;
            opacity: 0.9;
        }}

        .creator-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
        }}

        .creator-card {{
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }}

        .creator-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}

        .creator-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}

        .creator-name {{
            font-size: 20px;
            font-weight: 700;
            color: #333;
        }}

        .creator-username {{
            font-size: 14px;
            color: #666;
            margin-top: 5px;
        }}

        .score-badge {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            font-size: 24px;
            font-weight: 700;
        }}

        .creator-stats {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 15px;
        }}

        .creator-stat {{
            background: white;
            padding: 12px;
            border-radius: 8px;
            text-align: center;
        }}

        .creator-stat-value {{
            font-size: 20px;
            font-weight: 700;
            color: #667eea;
        }}

        .creator-stat-label {{
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }}

        .platform-badge {{
            display: inline-block;
            background: #764ba2;
            color: white;
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: 600;
            margin-top: 10px;
        }}

        .language-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}

        .language-table th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}

        .language-table td {{
            padding: 15px;
            border-bottom: 1px solid #eee;
        }}

        .language-table tr:last-child td {{
            border-bottom: none;
        }}

        .language-table tr:hover {{
            background: #f8f9fa;
        }}

        .frequency-badge {{
            background: #667eea;
            color: white;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 14px;
            font-weight: 600;
        }}

        .footer {{
            background: #f8f9fa;
            padding: 30px 40px;
            text-align: center;
            color: #666;
            font-size: 14px;
        }}

        .analysis-summary {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
        }}

        .analysis-summary h3 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 24px;
        }}

        .analysis-summary .summary-item {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #dee2e6;
        }}

        .analysis-summary .summary-item:last-child {{
            border-bottom: none;
        }}

        .analysis-summary .summary-label {{
            color: #666;
            font-weight: 500;
        }}

        .analysis-summary .summary-value {{
            color: #333;
            font-weight: 700;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Creator Intelligence Report</h1>
            <div class="subtitle">Lighting Industry Creator Analysis • Generated {timestamp}</div>
        </div>

        <div class="content">
"""

        # Analysis Summary Section
        if analysis_summary:
            html += f"""
            <div class="section">
                <h2 class="section-title">📊 Analysis Summary</h2>
                <div class="analysis-summary">
                    <div class="summary-item">
                        <span class="summary-label">Total Creators Analyzed:</span>
                        <span class="summary-value">{analysis_summary.get('total_creators_analyzed', 0)}</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-label">LLM Tokens Used:</span>
                        <span class="summary-value">{analysis_summary.get('llm_tokens_used', 0):,}</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-label">Estimated LLM Cost:</span>
                        <span class="summary-value">${analysis_summary.get('llm_tokens_used', 0) * 0.075 / 1_000_000:.4f}</span>
                    </div>
                </div>
            </div>
"""

        # Stats Section
        html += f"""
            <div class="section">
                <h2 class="section-title">📈 Overall Statistics</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">{stats.get('total_creators', 0)}</div>
                        <div class="stat-label">Total Creators</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{stats.get('total_content', 0)}</div>
                        <div class="stat-label">Content Analyzed</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{stats.get('total_language_phrases', 0)}</div>
                        <div class="stat-label">Language Phrases</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{len(stats.get('creators_by_platform', {}))}</div>
                        <div class="stat-label">Platforms</div>
                    </div>
                </div>
            </div>
"""

        # Top Research Candidates
        html += f"""
            <div class="section">
                <h2 class="section-title">🔬 Top Research Candidates</h2>
                <div class="creator-grid">
"""
        for creator in top_research[:10]:
            html += self._render_creator_card(creator, 'research')

        html += """
                </div>
            </div>
"""

        # Top Partnership Candidates
        html += f"""
            <div class="section">
                <h2 class="section-title">🤝 Top Partnership Candidates</h2>
                <div class="creator-grid">
"""
        for creator in top_partnership[:10]:
            html += self._render_creator_card(creator, 'partnership')

        html += """
                </div>
            </div>
"""

        # Consumer Language Dictionary
        html += f"""
            <div class="section">
                <h2 class="section-title">💬 Consumer Language Dictionary</h2>
                <table class="language-table">
                    <thead>
                        <tr>
                            <th>Phrase</th>
                            <th>Category</th>
                            <th>Frequency</th>
                            <th>Platform</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        for phrase in consumer_language[:50]:
            html += f"""
                        <tr>
                            <td>{phrase.get('phrase', '')}</td>
                            <td>{phrase.get('category', 'unknown').replace('_', ' ').title()}</td>
                            <td><span class="frequency-badge">{phrase.get('frequency', 0)}</span></td>
                            <td>{phrase.get('platform', 'multiple').upper()}</td>
                        </tr>
"""

        html += """
                    </tbody>
                </table>
            </div>
        </div>

        <div class="footer">
            <p>Generated by Creator Intelligence Module • 3M Lighting Project</p>
            <p>Powered by multi-platform analysis with LLM classification</p>
        </div>
    </div>
</body>
</html>
"""
        return html

    def _generate_creator_analysis(self, creator: Dict, content_stats: Dict) -> str:
        """Generate AI analysis of creator's value and relevance."""
        import google.generativeai as genai
        from core.config import config

        # Build analysis prompt
        prompt = f"""Analyze this YouTube creator for a lighting industry market research project.

Creator: {creator.get('display_name', 'Unknown')}
Username: @{creator.get('username', 'unknown')}
Bio: {creator.get('bio', 'No bio available')}
Followers: {creator.get('follower_count', 0):,}
Content Count: {creator.get('content_count', 0)}
Classification: {creator.get('classification', 'unknown')}

Content Analysis:
- Highly Relevant Videos: {content_stats.get('highly_relevant', 0)}
- Relevant Videos: {content_stats.get('relevant', 0)}
- Tangentially Relevant: {content_stats.get('tangential', 0)}

Research Viability Score: {creator.get('research_viability_score', 0)}/100
Partnership Viability Score: {creator.get('partnership_viability_score', 0)}/100

Generate a 2-3 sentence analysis covering:
1. What this creator does and their focus area
2. Their specific value for lighting industry research OR partnership opportunities
3. Key insight about their content relevance

Be specific and actionable. Focus on utility, not praise."""

        try:
            genai.configure(api_key=config.gemini_api_key)
            model = genai.GenerativeModel(config.llm_model)
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            # Fallback to rule-based summary
            logger.warning(f"AI analysis failed: {e}, using fallback")
            return self._fallback_creator_analysis(creator, content_stats)

    def _fallback_creator_analysis(self, creator: Dict, content_stats: Dict) -> str:
        """Rule-based fallback analysis when AI fails."""
        bio = creator.get('bio', '').lower()
        classification = creator.get('classification', 'unknown')
        followers = creator.get('follower_count', 0)

        # Determine creator type
        if 'manufacturer' in bio or 'supplier' in bio:
            creator_type = "manufacturer/supplier"
            value = "Industry voice for competitive analysis and product positioning"
        elif 'diy' in bio or 'tutorial' in bio:
            creator_type = "DIY educator"
            value = "Consumer pain points and use case insights"
        elif 'professional' in bio or 'studio' in bio:
            creator_type = "professional lighting expert"
            value = "Technical requirements and professional use cases"
        else:
            creator_type = "content creator"
            value = "General lighting content and consumer perspectives"

        # Build summary
        relevance = "highly valuable" if classification == 'highly_relevant' else "moderately useful" if classification == 'relevant' else "limited utility"

        summary = f"This {creator_type} with {followers:,} followers focuses on lighting content. {value}. "

        if content_stats.get('highly_relevant', 0) >= 5:
            summary += f"Strong content library ({content_stats['highly_relevant']} highly relevant videos) makes them {relevance} for research."
        elif content_stats.get('relevant', 0) + content_stats.get('highly_relevant', 0) >= 5:
            summary += f"Decent content volume provides {relevance} insights for consumer research."
        else:
            summary += f"Limited relevant content suggests {relevance} for this project."

        return summary

    def _calculate_engagement_rate(self, creator_id: int) -> float:
        """
        Calculate real engagement rate from YouTube video metrics.
        Engagement Rate = (Total Likes + Total Comments) / Total Views * 100

        Args:
            creator_id: Creator ID

        Returns:
            Engagement rate percentage (0.0-100.0)
        """
        if not creator_id:
            return 0.0

        cursor = self.db.conn.cursor()

        # Get aggregate engagement metrics from all videos
        cursor.execute("""
            SELECT
                SUM(view_count) as total_views,
                SUM(like_count) as total_likes,
                SUM(comment_count) as total_comments
            FROM creator_content
            WHERE creator_id = ?
            AND view_count > 0
        """, (creator_id,))

        row = cursor.fetchone()

        if not row or not row[0]:  # No views found
            return 0.0

        total_views = row[0] or 0
        total_likes = row[1] or 0
        total_comments = row[2] or 0

        if total_views == 0:
            return 0.0

        # Calculate engagement rate
        engagement_rate = ((total_likes + total_comments) / total_views) * 100

        return round(engagement_rate, 2)

    def _get_average_relevance_score(self, creator_id: int) -> float:
        """
        Get average relevance score from creator's content.

        Args:
            creator_id: Creator ID

        Returns:
            Average relevance score (0.0-1.0)
        """
        if not creator_id:
            return 0.0

        cursor = self.db.conn.cursor()

        cursor.execute("""
            SELECT AVG(relevance_score) as avg_score
            FROM creator_content
            WHERE creator_id = ? AND relevance_score IS NOT NULL
        """, (creator_id,))

        row = cursor.fetchone()

        if not row or row[0] is None:
            return 0.0

        return round(row[0], 2)

    def _get_creator_content_insights(self, creator_id: int) -> Dict:
        """Get content insights for a creator."""
        if not creator_id:
            return {
                'sample_titles': [],
                'content_stats': {},
                'engagement_rate': 0.0,
                'avg_relevance_score': 0.0
            }

        cursor = self.db.conn.cursor()

        # Get content statistics
        cursor.execute("""
            SELECT classification, COUNT(*) as count
            FROM creator_content
            WHERE creator_id = ?
            GROUP BY classification
        """, (creator_id,))

        stats_rows = cursor.fetchall()
        content_stats = {
            'highly_relevant': 0,
            'relevant': 0,
            'tangential': 0,
            'not_relevant': 0
        }

        for row in stats_rows:
            if row[0] == 'highly_relevant':
                content_stats['highly_relevant'] = row[1]
            elif row[0] == 'relevant':
                content_stats['relevant'] = row[1]
            elif row[0] == 'tangentially_relevant':
                content_stats['tangential'] = row[1]
            elif row[0] == 'not_relevant':
                content_stats['not_relevant'] = row[1]

        # Get top 5 most relevant content items
        cursor.execute("""
            SELECT title, description, classification, relevance_score
            FROM creator_content
            WHERE creator_id = ? AND title IS NOT NULL AND title != ''
            ORDER BY
                CASE classification
                    WHEN 'highly_relevant' THEN 1
                    WHEN 'relevant' THEN 2
                    WHEN 'tangentially_relevant' THEN 3
                    ELSE 4
                END,
                relevance_score DESC
            LIMIT 5
        """, (creator_id,))

        content_items = cursor.fetchall()
        sample_titles = [row[0] for row in content_items if row[0]]

        # Calculate real engagement rate from video metrics
        engagement_rate = self._calculate_engagement_rate(creator_id)

        # Get average relevance score
        avg_relevance_score = self._get_average_relevance_score(creator_id)

        return {
            'sample_titles': sample_titles,
            'content_stats': content_stats,
            'engagement_rate': engagement_rate,
            'avg_relevance_score': avg_relevance_score
        }

    def _render_creator_card(self, creator: Dict, score_type: str) -> str:
        """Render a creator card with insights."""
        score_field = f'{score_type}_viability_score'
        score = creator.get(score_field, 0)

        # Get creator profile URL
        profile_url = creator.get('profile_url', '')
        username = creator.get('username', 'unknown')
        display_name = creator.get('display_name', 'Unknown')

        # Get content insights for this creator (includes calculated engagement and relevance)
        content_insights = self._get_creator_content_insights(creator.get('id'))

        # Use CALCULATED engagement rate from real YouTube metrics
        engagement_rate = content_insights.get('engagement_rate', 0.0)

        # Get average relevance score from content
        avg_relevance_score = content_insights.get('avg_relevance_score', 0.0)

        # Generate AI analysis
        ai_analysis = self._generate_creator_analysis(creator, content_insights['content_stats'])

        # Build insights HTML with relevance score
        insights_html = f'<div style="margin-top: 12px; padding: 12px; background: #f8f9fa; border-radius: 6px; font-size: 13px; line-height: 1.6; color: #444;"><strong>Analysis:</strong> {ai_analysis}</div>'

        if content_insights['sample_titles']:
            insights_html += '<div style="margin-top: 12px;"><strong>Sample Content:</strong><ul style="margin: 4px 0; padding-left: 20px; font-size: 12px;">'
            for title in content_insights['sample_titles'][:3]:
                insights_html += f'<li>{title}</li>'
            insights_html += '</ul></div>'

        return f"""
                    <div class="creator-card">
                        <div class="creator-header">
                            <div>
                                <div class="creator-name">
                                    {'<a href="' + profile_url + '" target="_blank" style="color: #6366f1; text-decoration: none;">' + display_name + ' ↗</a>' if profile_url else display_name}
                                </div>
                                <div class="creator-username">@{username}</div>
                            </div>
                            <div class="score-badge">{score}</div>
                        </div>
                        <div class="platform-badge">{creator.get('platform', 'unknown').upper()}</div>
                        <div class="creator-stats">
                            <div class="creator-stat">
                                <div class="creator-stat-value">{creator.get('follower_count', 0):,}</div>
                                <div class="creator-stat-label">Followers</div>
                            </div>
                            <div class="creator-stat">
                                <div class="creator-stat-value">{engagement_rate:.2f}%</div>
                                <div class="creator-stat-label">Engagement</div>
                            </div>
                            <div class="creator-stat">
                                <div class="creator-stat-value">{creator.get('content_count', 0)}</div>
                                <div class="creator-stat-label">Content</div>
                            </div>
                            <div class="creator-stat">
                                <div class="creator-stat-value">{avg_relevance_score:.2f}</div>
                                <div class="creator-stat-label">Relevance Score</div>
                            </div>
                        </div>
                        {insights_html}
                    </div>
"""


if __name__ == "__main__":
    # Test HTML reporter
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))

    from core.database import CreatorDatabase

    db = CreatorDatabase("data/database/creator_intelligence.db")
    reporter = HTMLReporter(db)

    report_path = reporter.generate_report(
        output_path="data/reports/test_report.html"
    )

    print(f"✅ Test report generated: {report_path}")
    db.close()
