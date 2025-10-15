"""
Competitive Intelligence Analyzer
Tracks competitor patent activity, filing velocity, and technology focus areas
"""

import os
import json
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import sqlite3

class CompetitiveAnalyzer:
    """Analyze competitive patent landscape"""

    def __init__(self, db_path: str = "data/patents.db"):
        """
        Initialize competitive analyzer

        Args:
            db_path: Path to patent database
        """
        self.db_path = db_path
        self.competitors = [
            "Philips", "Signify", "Osram", "Cree", "Acuity Brands",
            "GE Lighting", "Lumileds", "Samsung Electronics",
            "LG Electronics", "Nichia", "Seoul Semiconductor"
        ]

    def generate_competitor_summary(
        self,
        time_period_days: int = 90,
        comparison_period_days: int = 90
    ) -> Dict:
        """
        Generate competitive intelligence summary

        Args:
            time_period_days: Current analysis period in days
            comparison_period_days: Previous period for velocity comparison

        Returns:
            Dict with competitive intelligence insights
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Calculate date ranges
        current_end = datetime.now()
        current_start = current_end - timedelta(days=time_period_days)
        prior_start = current_start - timedelta(days=comparison_period_days)

        # Get patents by competitor and time period
        current_patents = self._get_patents_by_period(
            cursor, current_start, current_end
        )
        prior_patents = self._get_patents_by_period(
            cursor, prior_start, current_start
        )

        # Analyze each competitor
        competitor_analysis = {}
        threats = []

        for competitor in self.competitors:
            analysis = self._analyze_competitor(
                competitor,
                current_patents,
                prior_patents,
                cursor
            )

            if analysis['current_count'] > 0:
                competitor_analysis[competitor] = analysis

                # Track high-threat competitors
                if analysis['threat_level'] in ['high', 'critical']:
                    threats.append({
                        'competitor': competitor,
                        'threat_level': analysis['threat_level'],
                        'patent_count': analysis['current_count'],
                        'velocity_change': analysis['velocity_change_pct'],
                        'top_technologies': analysis['top_technologies'][:3]
                    })

        conn.close()

        # Sort threats by severity
        threats.sort(key=lambda x: (
            {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}[x['threat_level']],
            x['velocity_change']
        ), reverse=True)

        return {
            'analysis_period': {
                'current_start': current_start.isoformat(),
                'current_end': current_end.isoformat(),
                'days': time_period_days
            },
            'competitor_count': len(competitor_analysis),
            'total_patents_analyzed': sum(
                c['current_count'] for c in competitor_analysis.values()
            ),
            'competitor_analysis': competitor_analysis,
            'top_threats': threats[:5],
            'market_trends': self._identify_market_trends(competitor_analysis),
            'technology_gaps': self._identify_technology_gaps(competitor_analysis)
        }

    def _get_patents_by_period(
        self,
        cursor,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:
        """Get all patents within date range"""
        cursor.execute("""
            SELECT
                id,
                title,
                abstract,
                assignees,
                cpc_codes,
                filing_date,
                extracted_at
            FROM patents
            WHERE filing_date >= ? AND filing_date < ?
        """, (start_date.isoformat(), end_date.isoformat()))

        patents = []
        for row in cursor.fetchall():
            patents.append({
                'id': row['id'],
                'title': row['title'],
                'abstract': row['abstract'],
                'assignees': json.loads(row['assignees']) if row['assignees'] else [],
                'cpc_codes': json.loads(row['cpc_codes']) if row['cpc_codes'] else [],
                'filing_date': row['filing_date'],
                'extracted_at': row['extracted_at']
            })

        return patents

    def _analyze_competitor(
        self,
        competitor: str,
        current_patents: List[Dict],
        prior_patents: List[Dict],
        cursor
    ) -> Dict:
        """Analyze single competitor's patent activity"""

        # Filter patents for this competitor
        current = [p for p in current_patents if self._is_assignee(competitor, p)]
        prior = [p for p in prior_patents if self._is_assignee(competitor, p)]

        current_count = len(current)
        prior_count = len(prior)

        # Calculate velocity change
        if prior_count > 0:
            velocity_change_pct = ((current_count - prior_count) / prior_count) * 100
        else:
            velocity_change_pct = 100.0 if current_count > 0 else 0.0

        # Analyze technology focus areas (CPC codes)
        cpc_codes = []
        for patent in current:
            cpc_codes.extend(patent.get('cpc_codes', []))

        top_technologies = self._categorize_cpc_codes(cpc_codes)

        # Assess threat level
        threat_level = self._assess_threat_level(
            current_count,
            velocity_change_pct,
            top_technologies
        )

        # Get innovation quality metrics if available
        innovation_quality = self._get_innovation_metrics(
            cursor,
            [p['id'] for p in current]
        )

        return {
            'current_count': current_count,
            'prior_count': prior_count,
            'velocity_change_pct': round(velocity_change_pct, 1),
            'top_technologies': top_technologies,
            'threat_level': threat_level,
            'innovation_quality': innovation_quality,
            'key_patents': self._identify_key_patents(current)[:3]
        }

    def _is_assignee(self, competitor: str, patent: Dict) -> bool:
        """Check if competitor is assignee of patent"""
        assignees = patent.get('assignees', [])
        competitor_lower = competitor.lower()

        for assignee in assignees:
            if competitor_lower in assignee.lower():
                return True

        return False

    def _categorize_cpc_codes(self, cpc_codes: List[str]) -> List[Dict]:
        """Categorize and count CPC technology codes"""

        # CPC code to human-readable categories
        cpc_categories = {
            'F21K': 'LED Light Sources',
            'F21V': 'Lighting Fixtures & Optics',
            'F21Y': 'Lighting Applications',
            'H05B': 'LED Drivers & Power Supply',
            'H01L': 'LED Semiconductor Devices',
            'G09G': 'Display Control',
            'H04N': 'Image Capture/Processing',
            'G01J': 'Light Measurement',
            'F21S': 'Vehicle Lighting',
            'A61N': 'Medical Lighting Therapy'
        }

        # Count codes by category
        category_counts = Counter()

        for code in cpc_codes:
            # Extract main class (first 4 chars)
            main_class = code[:4] if len(code) >= 4 else code
            category = cpc_categories.get(main_class, 'Other')
            category_counts[category] += 1

        # Return sorted list
        return [
            {'category': cat, 'count': count}
            for cat, count in category_counts.most_common()
        ]

    def _assess_threat_level(
        self,
        patent_count: int,
        velocity_change_pct: float,
        technologies: List[Dict]
    ) -> str:
        """
        Assess competitor threat level

        Returns: 'critical', 'high', 'medium', 'low'
        """

        # Critical: High volume + accelerating + core technology overlap
        if patent_count >= 15 and velocity_change_pct >= 50:
            return 'critical'

        # High: Moderate volume + accelerating OR high volume
        if (patent_count >= 10 and velocity_change_pct >= 25) or patent_count >= 20:
            return 'high'

        # Medium: Some activity with growth
        if patent_count >= 5 and velocity_change_pct > 0:
            return 'medium'

        # Low: Minimal activity or declining
        return 'low'

    def _get_innovation_metrics(
        self,
        cursor,
        patent_ids: List[str]
    ) -> Optional[Dict]:
        """Get aggregated innovation metrics from LLM analysis"""

        if not patent_ids:
            return None

        try:
            # Check if innovation analysis table exists
            cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='innovation_analysis'
            """)

            if not cursor.fetchone():
                return None

            # Get metrics for these patents
            placeholders = ','.join(['?' for _ in patent_ids])
            cursor.execute(f"""
                SELECT
                    AVG(market_potential_score) as avg_market_potential,
                    COUNT(CASE WHEN threat_level = 'high' THEN 1 END) as high_threat_count,
                    COUNT(CASE WHEN technology_readiness = 'production_ready' THEN 1 END) as production_ready_count
                FROM innovation_analysis
                WHERE patent_id IN ({placeholders})
            """, patent_ids)

            row = cursor.fetchone()

            if row and row['avg_market_potential']:
                return {
                    'avg_market_potential': round(row['avg_market_potential'], 1),
                    'high_threat_count': row['high_threat_count'],
                    'production_ready_count': row['production_ready_count']
                }

        except sqlite3.OperationalError:
            # Table doesn't exist yet
            pass

        return None

    def _identify_key_patents(self, patents: List[Dict]) -> List[Dict]:
        """Identify most important patents based on various signals"""

        # Score patents by importance signals
        scored_patents = []

        for patent in patents:
            score = 0

            # Longer abstracts indicate more detailed work
            abstract_len = len(patent.get('abstract', ''))
            score += min(abstract_len / 500, 3)

            # Multiple CPC codes indicate broader technology scope
            cpc_count = len(patent.get('cpc_codes', []))
            score += min(cpc_count, 5)

            # Recent patents are more relevant
            try:
                filing_date = datetime.fromisoformat(patent['filing_date'])
                days_old = (datetime.now() - filing_date).days
                recency_score = max(0, 5 - (days_old / 30))
                score += recency_score
            except (ValueError, KeyError):
                pass

            scored_patents.append({
                'patent': patent,
                'importance_score': score
            })

        # Sort by score and return top patents
        scored_patents.sort(key=lambda x: x['importance_score'], reverse=True)

        return [
            {
                'id': sp['patent']['id'],
                'title': sp['patent']['title'],
                'filing_date': sp['patent']['filing_date'],
                'importance_score': round(sp['importance_score'], 1)
            }
            for sp in scored_patents
        ]

    def _identify_market_trends(self, competitor_analysis: Dict) -> List[Dict]:
        """Identify overall market trends from competitor activity"""

        # Aggregate technology focus across all competitors
        all_technologies = defaultdict(int)

        for analysis in competitor_analysis.values():
            for tech in analysis['top_technologies']:
                all_technologies[tech['category']] += tech['count']

        # Calculate trend direction
        trends = []
        for category, total_count in sorted(
            all_technologies.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]:
            # Determine if trending
            competitor_count = sum(
                1 for analysis in competitor_analysis.values()
                if any(t['category'] == category for t in analysis['top_technologies'])
            )

            trend_strength = 'strong' if competitor_count >= 3 else 'moderate'

            trends.append({
                'technology': category,
                'total_patents': total_count,
                'competitor_count': competitor_count,
                'trend_strength': trend_strength
            })

        return trends

    def _identify_technology_gaps(self, competitor_analysis: Dict) -> List[str]:
        """Identify technology areas with low 3M activity"""

        # This is a placeholder - would need 3M patent data to compare
        # For now, identify areas with high competitor activity

        all_technologies = defaultdict(int)

        for analysis in competitor_analysis.values():
            for tech in analysis['top_technologies']:
                all_technologies[tech['category']] += 1

        # Areas where 3+ competitors are active = potential gaps
        gaps = [
            tech for tech, count in all_technologies.items()
            if count >= 3
        ]

        return gaps[:5]

    def generate_executive_summary(
        self,
        time_period_days: int = 90
    ) -> str:
        """
        Generate executive-ready text summary

        Args:
            time_period_days: Analysis period in days

        Returns:
            Formatted executive summary string
        """
        analysis = self.generate_competitor_summary(time_period_days)

        summary = f"""## 🔍 COMPETITIVE INTELLIGENCE SUMMARY
**Analysis Period**: Last {time_period_days} days ({analysis['analysis_period']['current_start'][:10]} to {analysis['analysis_period']['current_end'][:10]})

### 📊 OVERVIEW
- **Competitors Tracked**: {analysis['competitor_count']}
- **Total Patents Analyzed**: {analysis['total_patents_analyzed']}

### 🚨 TOP COMPETITIVE THREATS
"""

        for i, threat in enumerate(analysis['top_threats'], 1):
            icon = '🔴' if threat['threat_level'] == 'critical' else '🟠' if threat['threat_level'] == 'high' else '🟡'
            velocity = threat['velocity_change']
            velocity_str = f"↑{velocity}%" if velocity > 0 else f"↓{abs(velocity)}%" if velocity < 0 else "→"

            summary += f"\n**{i}. {icon} {threat['competitor']}**\n"
            summary += f"   - Patent Filings: {threat['patent_count']} ({velocity_str} vs prior period)\n"
            summary += f"   - Threat Level: {threat['threat_level'].upper()}\n"
            summary += f"   - Focus Areas: {', '.join([t['category'] for t in threat['top_technologies']])}\n"

        summary += "\n### 📈 MARKET TRENDS\n"
        for trend in analysis['market_trends']:
            strength_icon = '⚡' if trend['trend_strength'] == 'strong' else '↗️'
            summary += f"- {strength_icon} **{trend['technology']}**: {trend['total_patents']} patents across {trend['competitor_count']} competitors\n"

        if analysis['technology_gaps']:
            summary += "\n### 🎯 POTENTIAL 3M GAPS\n"
            summary += "Areas with high competitor activity:\n"
            for gap in analysis['technology_gaps']:
                summary += f"- {gap}\n"

        summary += "\n### 💡 RECOMMENDED ACTIONS\n"

        if analysis['top_threats']:
            top_threat = analysis['top_threats'][0]
            summary += f"1. **Immediate**: Deep-dive analysis of {top_threat['competitor']} patents in {top_threat['top_technologies'][0]['category']}\n"
            summary += f"2. **Strategic**: File defensive patents in {analysis['market_trends'][0]['technology']} (strongest trend)\n"

        if analysis['technology_gaps']:
            summary += f"3. **R&D Focus**: Accelerate research in {analysis['technology_gaps'][0]} to close competitive gap\n"

        summary += "\n---\n*Generated by 3M Patent Intelligence Module*"

        return summary


# Example usage
if __name__ == "__main__":
    analyzer = CompetitiveAnalyzer()

    # Generate summary
    summary = analyzer.generate_executive_summary(time_period_days=90)
    print(summary)

    # Get detailed JSON
    detailed = analyzer.generate_competitor_summary(time_period_days=90)
    print("\nDetailed analysis:")
    print(json.dumps(detailed, indent=2))
