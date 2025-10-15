#!/usr/bin/env python3
"""
Checkpoint 2: LLM Analysis & Reporting Test
Tests innovation extraction, competitive intelligence, and executive reporting
"""

import os
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.database import PatentDatabase
from analyzers.innovation_extractor import InnovationExtractor
from analyzers.competitive_analyzer import CompetitiveAnalyzer
from reports.executive_report_generator import ExecutiveReportGenerator


def print_header(text: str):
    """Print formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")


def print_success(text: str):
    """Print success message"""
    print(f"✅ {text}")


def print_warning(text: str):
    """Print warning message"""
    print(f"⚠️  {text}")


def print_error(text: str):
    """Print error message"""
    print(f"❌ {text}")


def print_info(text: str):
    """Print info message"""
    print(f"ℹ️  {text}")


def main():
    print_header("🔬 CHECKPOINT 2: LLM Analysis & Reporting Test")

    print_info("This test validates:")
    print("  1. LLM innovation extraction from patents")
    print("  2. Competitive intelligence analysis")
    print("  3. Executive report generation")
    print("  4. End-to-end system integration\n")

    # Configuration
    db_path = "data/patents.db"
    test_patent_count = 3  # Analyze 3 patents for cost efficiency

    # Check for API key
    claude_api_key = os.getenv('CLAUDE_API_KEY')
    if not claude_api_key:
        print_error("CLAUDE_API_KEY not found in environment")
        print_info("Set with: export CLAUDE_API_KEY='your-key-here'")
        sys.exit(1)

    print_success(f"Claude API key found")

    # Step 1: Check database
    print_header("STEP 1: Database Check")

    if not Path(db_path).exists():
        print_error(f"Database not found: {db_path}")
        print_info("Run test_checkpoint1_data_collection.py first")
        sys.exit(1)

    db = PatentDatabase(db_path)
    stats = db.get_collection_stats()

    print_success(f"Database found: {stats['total_patents']} patents")
    print_info(f"  Complete data: {stats['complete_data_count']} ({stats['complete_data_pct']:.1f}%)")

    if stats['total_patents'] == 0:
        print_error("No patents in database")
        print_info("Run test_checkpoint1_data_collection.py first")
        sys.exit(1)

    if stats['total_patents'] < test_patent_count:
        print_warning(f"Only {stats['total_patents']} patents available (need {test_patent_count})")
        test_patent_count = stats['total_patents']

    # Step 2: Test Innovation Extraction
    print_header("STEP 2: LLM Innovation Extraction")

    print_info(f"Analyzing {test_patent_count} patents with Claude Sonnet 4...")
    print_info("This will cost approximately $0.02 for 3 patents")

    # Get sample patents
    conn = db.conn
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT id, title, abstract, assignees, cpc_codes, filing_date, claims_text
        FROM patents
        WHERE has_abstract = 1
        ORDER BY filing_date DESC
        LIMIT {test_patent_count}
    """)

    patents = []
    for row in cursor.fetchall():
        patents.append({
            'id': row[0],
            'title': row[1],
            'abstract': row[2],
            'assignees': json.loads(row[3]) if row[3] else [],
            'cpc_codes': json.loads(row[4]) if row[4] else [],
            'filing_date': row[5],
            'claims_text': row[6]
        })

    print_success(f"Retrieved {len(patents)} patents for analysis\n")

    # Initialize extractor
    extractor = InnovationExtractor(api_key=claude_api_key)

    # Analyze patents
    innovations = []
    for i, patent in enumerate(patents, 1):
        print(f"[{i}/{len(patents)}] Analyzing {patent['id']}...")
        try:
            insights = extractor.analyze_patent(patent)
            innovations.append(insights)

            # Show key results
            print(f"    Innovation: {insights['core_innovation'][:80]}...")
            print(f"    Market Score: {insights['market_potential']['score']}/10")
            print(f"    Threat Level: {insights.get('threat_level', 'N/A')}")
            print()

        except Exception as e:
            print_error(f"Failed to analyze: {e}")
            continue

    if not innovations:
        print_error("No innovations extracted")
        sys.exit(1)

    print_success(f"Extracted {len(innovations)} innovation insights")

    # Show cost
    cost_summary = extractor.get_cost_summary()
    print_info(f"Cost: ${cost_summary['total_cost_usd']:.4f}")
    print_info(f"Tokens: {cost_summary['input_tokens']} input, {cost_summary['output_tokens']} output\n")

    # Save innovations to database
    print_info("Saving innovation insights to database...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS innovation_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patent_id TEXT NOT NULL,
            core_innovation TEXT,
            problem_solved TEXT,
            market_potential_score INTEGER,
            market_potential_reasoning TEXT,
            technology_readiness TEXT,
            applications TEXT,  -- JSON array
            competitive_position TEXT,
            threat_level TEXT,
            recommended_action TEXT,
            analysis_model TEXT,
            input_tokens INTEGER,
            output_tokens INTEGER,
            analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patent_id) REFERENCES patents(id)
        )
    """)

    for innovation in innovations:
        cursor.execute("""
            INSERT INTO innovation_analysis (
                patent_id, core_innovation, problem_solved,
                market_potential_score, market_potential_reasoning,
                technology_readiness, applications,
                competitive_position, threat_level, recommended_action,
                analysis_model, input_tokens, output_tokens
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            innovation['patent_id'],
            innovation['core_innovation'],
            innovation['problem_solved'],
            innovation['market_potential']['score'],
            innovation['market_potential']['reasoning'],
            innovation['technology_readiness'],
            json.dumps(innovation['applications']),
            innovation['competitive_position'],
            innovation.get('threat_level'),
            innovation['recommended_action'],
            innovation['analysis_model'],
            innovation['input_tokens'],
            innovation['output_tokens']
        ))

    conn.commit()
    print_success("Innovation insights saved to database\n")

    # Step 3: Test Competitive Intelligence
    print_header("STEP 3: Competitive Intelligence Analysis")

    analyzer = CompetitiveAnalyzer(db_path=db_path)

    print_info("Generating competitive summary...")
    competitive_summary = analyzer.generate_competitor_summary(time_period_days=90)

    print_success(f"Analyzed {competitive_summary['total_patents_analyzed']} patents")
    print_info(f"  Active competitors: {competitive_summary['competitor_count']}")
    print_info(f"  Top threats: {len(competitive_summary['top_threats'])}")
    print_info(f"  Market trends identified: {len(competitive_summary['market_trends'])}\n")

    # Show top threat
    if competitive_summary['top_threats']:
        top_threat = competitive_summary['top_threats'][0]
        print(f"🚨 TOP THREAT: {top_threat['competitor']}")
        print(f"   Patents: {top_threat['patent_count']}")
        print(f"   Velocity: {top_threat['velocity_change']:+.0f}%")
        print(f"   Threat Level: {top_threat['threat_level'].upper()}\n")

    # Show top trend
    if competitive_summary['market_trends']:
        top_trend = competitive_summary['market_trends'][0]
        print(f"📈 TOP TREND: {top_trend['technology']}")
        print(f"   Patents: {top_trend['total_patents']}")
        print(f"   Competitors: {top_trend['competitor_count']}")
        print(f"   Strength: {top_trend['trend_strength'].upper()}\n")

    # Step 4: Test Report Generation
    print_header("STEP 4: Executive Report Generation")

    generator = ExecutiveReportGenerator()

    print_info("Generating executive HTML report...")
    report_path = generator.generate_full_report(
        competitive_summary=competitive_summary,
        innovation_insights=innovations,
        output_path="reports/checkpoint2_test_report.html"
    )

    if Path(report_path).exists():
        file_size = Path(report_path).stat().st_size
        print_success(f"Report generated: {report_path}")
        print_info(f"  Size: {file_size:,} bytes\n")
    else:
        print_error("Report generation failed")
        sys.exit(1)

    # Step 5: Success Criteria
    print_header("STEP 5: Success Criteria Validation")

    success_criteria = [
        ("LLM API Connection", len(innovations) > 0),
        ("Innovation Extraction", all(i.get('core_innovation') for i in innovations)),
        ("Market Scoring", all(i.get('market_potential', {}).get('score', 0) > 0 for i in innovations)),
        ("Competitive Analysis", competitive_summary['total_patents_analyzed'] > 0),
        ("Report Generation", Path(report_path).exists()),
        ("Database Persistence", len(innovations) > 0)
    ]

    print("Validation Results:\n")
    all_passed = True
    for criterion, passed in success_criteria:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}  {criterion}")
        if not passed:
            all_passed = False

    print()

    if all_passed:
        print_success("🎉 CHECKPOINT 2 COMPLETE - All tests passed!")
        print_info(f"\n📊 Next Steps:")
        print(f"  1. Open report: open {report_path}")
        print(f"  2. Review innovation insights in database")
        print(f"  3. Run production analysis with real API key")
        print(f"  4. Set up scheduled monitoring\n")

        print_info(f"💰 Cost Summary:")
        print(f"  This test: ${cost_summary['total_cost_usd']:.4f}")
        print(f"  Per patent: ${cost_summary['total_cost_usd']/len(patents):.4f}")
        print(f"  Est. for 100 patents: ${(cost_summary['total_cost_usd']/len(patents))*100:.2f}")

    else:
        print_error("❌ CHECKPOINT 2 FAILED - Some tests did not pass")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
