"""
Test run of Creator Intelligence Module with 20 creators.
Generates comprehensive HTML report.
"""

import sys
from pathlib import Path

# Add parent directories to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir.parent.parent))
sys.path.insert(0, str(current_dir))

from core.orchestrator import CreatorIntelligenceOrchestrator
from reporters.html_reporter import HTMLReporter

def main():
    print("=" * 80)
    print("CREATOR INTELLIGENCE MODULE - TEST RUN")
    print("=" * 80)
    print("Configuration: 20 creators (5 per platform), Free tier APIs only")
    print()

    # Initialize orchestrator
    orchestrator = CreatorIntelligenceOrchestrator()

    # Run analysis - 5 creators per platform for 20 total
    results = orchestrator.analyze_creators(
        keywords=["LED lighting", "home lighting tutorial"],
        platforms=["youtube"],  # Start with YouTube only for free tier test
        limit_per_platform=5
    )

    print("\n" + "=" * 80)
    print("GENERATING HTML REPORT")
    print("=" * 80)

    # Generate HTML report
    reporter = HTMLReporter(orchestrator.db)
    report_path = reporter.generate_report(
        output_path="data/reports/creator_intelligence_test_report.html",
        analysis_summary=results
    )

    print(f"\n✅ Report generated: {report_path}")
    print(f"\n📊 Analysis Summary:")
    print(f"   Total creators analyzed: {results['total_creators_analyzed']}")
    print(f"   Total LLM tokens used: {results['llm_tokens_used']:,}")
    print(f"   Estimated cost: ${results['llm_tokens_used'] * 0.075 / 1_000_000:.4f}")

    # Get top creators
    print("\n" + "=" * 80)
    print("TOP 5 RESEARCH CANDIDATES")
    print("=" * 80)
    top_research = orchestrator.get_top_creators(score_type='research', limit=5)
    for i, creator in enumerate(top_research):
        print(f"{i+1}. {creator.get('display_name', 'Unknown')} (@{creator.get('username')})")
        print(f"   Score: {creator.get('research_viability_score')}/100")
        print(f"   Platform: {creator.get('platform')}")
        print(f"   Followers: {creator.get('follower_count', 0):,}")
        print()

    orchestrator.close()
    print(f"\n✅ Test run complete! Open report at: {report_path}")

if __name__ == "__main__":
    main()
