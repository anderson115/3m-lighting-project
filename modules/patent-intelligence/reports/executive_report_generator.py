"""
Executive Report Generator
Creates client-ready visual HTML reports combining all patent intelligence insights
"""

import os
import json
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

class ExecutiveReportGenerator:
    """Generate executive-ready HTML reports"""

    def __init__(self):
        """Initialize report generator"""
        pass

    def generate_full_report(
        self,
        competitive_summary: Dict,
        innovation_insights: List[Dict],
        output_path: str = "reports/patent_intelligence_report.html"
    ) -> str:
        """
        Generate comprehensive executive report

        Args:
            competitive_summary: Output from CompetitiveAnalyzer
            innovation_insights: List of insights from InnovationExtractor
            output_path: Where to save HTML report

        Returns:
            Path to generated report
        """

        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Build report sections
        html = self._build_html_header()
        html += self._build_executive_summary(competitive_summary, innovation_insights)
        html += self._build_competitive_threats_section(competitive_summary)
        html += self._build_key_innovations_section(innovation_insights)
        html += self._build_market_trends_section(competitive_summary)
        html += self._build_recommendations_section(competitive_summary, innovation_insights)
        html += self._build_html_footer()

        # Write to file
        with open(output_path, 'w') as f:
            f.write(html)

        return output_path

    def _build_html_header(self) -> str:
        """Build HTML header with styling"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3M Patent Intelligence Report</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 40px 20px;
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            color: white;
            padding: 60px 40px;
            text-align: center;
        }

        .header h1 {
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .header .subtitle {
            font-size: 18px;
            opacity: 0.9;
        }

        .header .date {
            font-size: 14px;
            opacity: 0.7;
            margin-top: 10px;
        }

        .content {
            padding: 40px;
        }

        .section {
            margin-bottom: 50px;
        }

        .section-title {
            font-size: 28px;
            font-weight: 700;
            color: #1e3a8a;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #3b82f6;
        }

        .stat-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            border: 2px solid #3b82f6;
            border-radius: 8px;
            padding: 25px;
            text-align: center;
        }

        .stat-value {
            font-size: 36px;
            font-weight: 700;
            color: #1e3a8a;
            display: block;
            margin-bottom: 5px;
        }

        .stat-label {
            font-size: 14px;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .threat-card {
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            padding: 25px;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }

        .threat-card:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
        }

        .threat-card.critical {
            border-color: #dc2626;
            background: #fef2f2;
        }

        .threat-card.high {
            border-color: #f59e0b;
            background: #fffbeb;
        }

        .threat-card.medium {
            border-color: #3b82f6;
            background: #eff6ff;
        }

        .threat-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 15px;
        }

        .threat-company {
            font-size: 22px;
            font-weight: 700;
            color: #1e293b;
        }

        .threat-badge {
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
        }

        .threat-badge.critical {
            background: #dc2626;
            color: white;
        }

        .threat-badge.high {
            background: #f59e0b;
            color: white;
        }

        .threat-badge.medium {
            background: #3b82f6;
            color: white;
        }

        .threat-badge.low {
            background: #64748b;
            color: white;
        }

        .threat-stats {
            display: flex;
            gap: 30px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }

        .threat-stat {
            font-size: 14px;
            color: #64748b;
        }

        .threat-stat strong {
            color: #1e293b;
            font-size: 16px;
        }

        .threat-technologies {
            margin-top: 15px;
        }

        .tech-tag {
            display: inline-block;
            background: #e0f2fe;
            color: #075985;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 13px;
            margin-right: 8px;
            margin-bottom: 8px;
        }

        .innovation-card {
            background: #f8fafc;
            border-left: 4px solid #3b82f6;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 4px;
        }

        .innovation-title {
            font-size: 18px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 10px;
        }

        .innovation-meta {
            display: flex;
            gap: 20px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }

        .meta-item {
            font-size: 13px;
            color: #64748b;
        }

        .meta-item strong {
            color: #1e293b;
        }

        .market-score {
            display: inline-block;
            background: #22c55e;
            color: white;
            padding: 4px 10px;
            border-radius: 12px;
            font-weight: 700;
            font-size: 14px;
        }

        .market-score.low {
            background: #ef4444;
        }

        .market-score.medium {
            background: #f59e0b;
        }

        .market-score.high {
            background: #22c55e;
        }

        .innovation-text {
            color: #475569;
            margin-bottom: 10px;
            line-height: 1.6;
        }

        .application-list {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }

        .application-tag {
            background: #dbeafe;
            color: #1e40af;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
        }

        .recommendation-box {
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border: 2px solid #f59e0b;
            border-radius: 8px;
            padding: 25px;
            margin-bottom: 20px;
        }

        .recommendation-box h3 {
            color: #92400e;
            font-size: 20px;
            margin-bottom: 15px;
        }

        .recommendation-box p {
            color: #78350f;
            line-height: 1.8;
        }

        .recommendation-list {
            list-style: none;
            margin-top: 15px;
        }

        .recommendation-list li {
            padding: 10px 0;
            padding-left: 30px;
            position: relative;
            color: #78350f;
        }

        .recommendation-list li:before {
            content: "→";
            position: absolute;
            left: 0;
            font-weight: 700;
            color: #f59e0b;
        }

        .trend-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        .trend-table th {
            background: #1e3a8a;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }

        .trend-table td {
            padding: 15px;
            border-bottom: 1px solid #e2e8f0;
        }

        .trend-table tr:hover {
            background: #f8fafc;
        }

        .trend-strength {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 700;
        }

        .trend-strength.strong {
            background: #22c55e;
            color: white;
        }

        .trend-strength.moderate {
            background: #3b82f6;
            color: white;
        }

        .footer {
            background: #f8fafc;
            padding: 30px 40px;
            text-align: center;
            color: #64748b;
            font-size: 14px;
            border-top: 1px solid #e2e8f0;
        }

        .velocity-indicator {
            font-weight: 700;
            font-size: 16px;
        }

        .velocity-indicator.up {
            color: #dc2626;
        }

        .velocity-indicator.down {
            color: #22c55e;
        }

        .velocity-indicator.neutral {
            color: #64748b;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Patent Intelligence Report</h1>
            <div class="subtitle">3M Lighting Technology Competitive Analysis</div>
            <div class="date">Generated: """ + datetime.now().strftime("%B %d, %Y at %I:%M %p") + """</div>
        </div>
        <div class="content">
"""

    def _build_executive_summary(
        self,
        competitive_summary: Dict,
        innovation_insights: List[Dict]
    ) -> str:
        """Build executive summary section"""

        # Calculate summary metrics
        total_patents = competitive_summary.get('total_patents_analyzed', 0)
        total_competitors = competitive_summary.get('competitor_count', 0)
        high_threats = len([t for t in competitive_summary.get('top_threats', []) if t['threat_level'] in ['critical', 'high']])

        # Average market potential from innovations
        market_potentials = [i.get('market_potential', {}).get('score', 0) for i in innovation_insights if i.get('market_potential')]
        avg_market_potential = sum(market_potentials) / len(market_potentials) if market_potentials else 0

        return f"""
            <div class="section">
                <h2 class="section-title">📋 Executive Summary</h2>

                <div class="stat-grid">
                    <div class="stat-card">
                        <span class="stat-value">{total_patents}</span>
                        <span class="stat-label">Patents Analyzed</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">{total_competitors}</span>
                        <span class="stat-label">Active Competitors</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">{high_threats}</span>
                        <span class="stat-label">High Priority Threats</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">{avg_market_potential:.1f}/10</span>
                        <span class="stat-label">Avg Market Potential</span>
                    </div>
                </div>
            </div>
"""

    def _build_competitive_threats_section(self, competitive_summary: Dict) -> str:
        """Build competitive threats section"""

        threats = competitive_summary.get('top_threats', [])

        if not threats:
            return """
            <div class="section">
                <h2 class="section-title">🚨 Competitive Threats</h2>
                <p style="color: #64748b;">No significant competitive threats identified in this analysis period.</p>
            </div>
"""

        html = """
            <div class="section">
                <h2 class="section-title">🚨 Competitive Threats</h2>
"""

        for threat in threats:
            threat_level = threat['threat_level']
            competitor = threat['competitor']
            patent_count = threat['patent_count']
            velocity = threat['velocity_change']
            technologies = threat['top_technologies']

            velocity_class = 'up' if velocity > 0 else 'down' if velocity < 0 else 'neutral'
            velocity_symbol = '↑' if velocity > 0 else '↓' if velocity < 0 else '→'

            html += f"""
                <div class="threat-card {threat_level}">
                    <div class="threat-header">
                        <div class="threat-company">{competitor}</div>
                        <div class="threat-badge {threat_level}">{threat_level}</div>
                    </div>
                    <div class="threat-stats">
                        <div class="threat-stat">
                            <strong>{patent_count}</strong> patents filed
                        </div>
                        <div class="threat-stat">
                            Velocity: <span class="velocity-indicator {velocity_class}">{velocity_symbol} {abs(velocity):.0f}%</span>
                        </div>
                    </div>
                    <div class="threat-technologies">
                        <strong>Focus Areas:</strong><br>
"""
            for tech in technologies[:5]:
                html += f'                        <span class="tech-tag">{tech["category"]} ({tech["count"]})</span>\n'

            html += """                    </div>
                </div>
"""

        html += "            </div>\n"
        return html

    def _build_key_innovations_section(self, innovation_insights: List[Dict]) -> str:
        """Build key innovations section"""

        if not innovation_insights:
            return """
            <div class="section">
                <h2 class="section-title">💡 Key Innovations</h2>
                <p style="color: #64748b;">No innovation analysis available yet.</p>
            </div>
"""

        # Sort by market potential score
        sorted_innovations = sorted(
            [i for i in innovation_insights if i.get('market_potential')],
            key=lambda x: x['market_potential'].get('score', 0),
            reverse=True
        )[:10]  # Top 10 innovations

        html = """
            <div class="section">
                <h2 class="section-title">💡 Key Innovations Discovered</h2>
"""

        for innovation in sorted_innovations:
            patent_id = innovation.get('patent_id', 'Unknown')
            core_innovation = innovation.get('core_innovation', 'N/A')
            problem_solved = innovation.get('problem_solved', 'N/A')
            market_score = innovation.get('market_potential', {}).get('score', 0)
            market_reasoning = innovation.get('market_potential', {}).get('reasoning', '')
            tech_readiness = innovation.get('technology_readiness', 'Unknown')
            applications = innovation.get('applications', [])
            competitive_position = innovation.get('competitive_position', 'N/A')
            recommended_action = innovation.get('recommended_action', 'N/A')

            score_class = 'high' if market_score >= 7 else 'medium' if market_score >= 4 else 'low'

            html += f"""
                <div class="innovation-card">
                    <div class="innovation-title">{patent_id}</div>
                    <div class="innovation-meta">
                        <div class="meta-item">
                            <strong>Market Potential:</strong> <span class="market-score {score_class}">{market_score}/10</span>
                        </div>
                        <div class="meta-item">
                            <strong>Tech Readiness:</strong> {tech_readiness.replace('_', ' ').title()}
                        </div>
                    </div>
                    <div class="innovation-text">
                        <strong>Innovation:</strong> {core_innovation}
                    </div>
                    <div class="innovation-text">
                        <strong>Problem Solved:</strong> {problem_solved}
                    </div>
                    <div class="innovation-text">
                        <strong>Market Reasoning:</strong> {market_reasoning}
                    </div>
                    <div class="innovation-text">
                        <strong>Competitive Position:</strong> {competitive_position}
                    </div>
"""
            if applications:
                html += '                    <div><strong>Applications:</strong></div>\n'
                html += '                    <div class="application-list">\n'
                for app in applications:
                    html += f'                        <span class="application-tag">{app}</span>\n'
                html += '                    </div>\n'

            html += f"""
                    <div class="innovation-text" style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #e2e8f0;">
                        <strong>Recommended Action:</strong> {recommended_action}
                    </div>
                </div>
"""

        html += "            </div>\n"
        return html

    def _build_market_trends_section(self, competitive_summary: Dict) -> str:
        """Build market trends section"""

        trends = competitive_summary.get('market_trends', [])

        if not trends:
            return """
            <div class="section">
                <h2 class="section-title">📈 Market Trends</h2>
                <p style="color: #64748b;">No market trends available.</p>
            </div>
"""

        html = """
            <div class="section">
                <h2 class="section-title">📈 Market Trends</h2>
                <table class="trend-table">
                    <thead>
                        <tr>
                            <th>Technology Area</th>
                            <th>Total Patents</th>
                            <th>Competitors Active</th>
                            <th>Trend Strength</th>
                        </tr>
                    </thead>
                    <tbody>
"""

        for trend in trends:
            strength = trend['trend_strength']
            html += f"""
                        <tr>
                            <td><strong>{trend['technology']}</strong></td>
                            <td>{trend['total_patents']}</td>
                            <td>{trend['competitor_count']}</td>
                            <td><span class="trend-strength {strength}">{strength.upper()}</span></td>
                        </tr>
"""

        html += """                    </tbody>
                </table>
            </div>
"""
        return html

    def _build_recommendations_section(
        self,
        competitive_summary: Dict,
        innovation_insights: List[Dict]
    ) -> str:
        """Build recommendations section"""

        threats = competitive_summary.get('top_threats', [])
        trends = competitive_summary.get('market_trends', [])
        gaps = competitive_summary.get('technology_gaps', [])

        html = """
            <div class="section">
                <h2 class="section-title">🎯 Strategic Recommendations</h2>
"""

        if threats:
            top_threat = threats[0]
            html += f"""
                <div class="recommendation-box">
                    <h3>1. Immediate Competitive Response</h3>
                    <p>
                        <strong>{top_threat['competitor']}</strong> has filed <strong>{top_threat['patent_count']} patents</strong>
                        with a velocity change of <strong>{top_threat['velocity_change']:+.0f}%</strong>,
                        indicating {('aggressive' if top_threat['velocity_change'] > 50 else 'moderate')} R&D acceleration.
                    </p>
                    <ul class="recommendation-list">
                        <li>Conduct deep-dive freedom-to-operate analysis in {top_threat['top_technologies'][0]['category']}</li>
                        <li>Evaluate defensive patent filing opportunities</li>
                        <li>Monitor for potential blocking patents against 3M products</li>
                    </ul>
                </div>
"""

        if trends:
            top_trend = trends[0]
            html += f"""
                <div class="recommendation-box">
                    <h3>2. Strategic R&D Investment</h3>
                    <p>
                        <strong>{top_trend['technology']}</strong> is the strongest market trend with
                        <strong>{top_trend['total_patents']} patents</strong> across <strong>{top_trend['competitor_count']} competitors</strong>.
                    </p>
                    <ul class="recommendation-list">
                        <li>Accelerate internal R&D programs in {top_trend['technology']}</li>
                        <li>Consider strategic acquisitions or partnerships in this space</li>
                        <li>File foundational patents to establish 3M position</li>
                    </ul>
                </div>
"""

        if gaps:
            html += f"""
                <div class="recommendation-box">
                    <h3>3. Technology Gap Closure</h3>
                    <p>
                        Analysis identified <strong>{len(gaps)} technology areas</strong> with high competitor activity
                        where 3M may have limited presence.
                    </p>
                    <ul class="recommendation-list">
"""
            for gap in gaps[:3]:
                html += f'                        <li>Evaluate 3M position in {gap}</li>\n'

            html += """                    </ul>
                </div>
"""

        # Add innovation-based recommendations
        high_value_innovations = [
            i for i in innovation_insights
            if i.get('market_potential', {}).get('score', 0) >= 7
        ]

        if high_value_innovations:
            html += f"""
                <div class="recommendation-box">
                    <h3>4. High-Value Innovation Opportunities</h3>
                    <p>
                        Identified <strong>{len(high_value_innovations)} high-market-potential innovations</strong> (score ≥7/10)
                        that warrant further investigation.
                    </p>
                    <ul class="recommendation-list">
                        <li>Prioritize licensing negotiations for top innovations</li>
                        <li>Evaluate acquisition targets with strong patent portfolios</li>
                        <li>Initiate product development aligned with market opportunities</li>
                    </ul>
                </div>
"""

        html += "            </div>\n"
        return html

    def _build_html_footer(self) -> str:
        """Build HTML footer"""
        return """
        </div>
        <div class="footer">
            <p><strong>3M Patent Intelligence Module</strong></p>
            <p>Powered by Claude Sonnet 4 LLM Analysis | PatentsView API</p>
            <p style="margin-top: 10px; font-size: 12px;">
                This report contains confidential and proprietary information. Do not distribute outside 3M.
            </p>
        </div>
    </div>
</body>
</html>
"""


# Example usage
if __name__ == "__main__":
    # Test report generation
    generator = ExecutiveReportGenerator()

    # Sample data
    sample_competitive = {
        'total_patents_analyzed': 47,
        'competitor_count': 5,
        'top_threats': [
            {
                'competitor': 'Philips',
                'threat_level': 'high',
                'patent_count': 23,
                'velocity_change': 156.5,
                'top_technologies': [
                    {'category': 'LED Light Sources', 'count': 15},
                    {'category': 'LED Drivers & Power Supply', 'count': 8}
                ]
            }
        ],
        'market_trends': [
            {
                'technology': 'LED Light Sources',
                'total_patents': 35,
                'competitor_count': 4,
                'trend_strength': 'strong'
            }
        ],
        'technology_gaps': ['Circadian Rhythm Control', 'IoT Integration']
    }

    sample_innovations = [
        {
            'patent_id': 'US-12345678',
            'core_innovation': 'Dynamic color temperature adjustment based on circadian rhythms',
            'problem_solved': 'Poor sleep quality from improper lighting timing',
            'market_potential': {'score': 8, 'reasoning': 'Wellness trend + aging population'},
            'technology_readiness': 'pilot_stage',
            'applications': ['Hospitals', 'Senior Living', 'Hotels'],
            'competitive_position': 'Philips ahead, 3M has gap',
            'recommended_action': 'License or acquire this technology'
        }
    ]

    report_path = generator.generate_full_report(sample_competitive, sample_innovations)
    print(f"✅ Report generated: {report_path}")
