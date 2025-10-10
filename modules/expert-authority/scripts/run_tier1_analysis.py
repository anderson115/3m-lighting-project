#!/usr/bin/env python3
"""
Run Tier 1 Expert Authority Analysis
Simple script to test the complete pipeline with real Reddit data
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.orchestrator import ExpertAuthorityOrchestrator


def main():
    """Run Tier 1 analysis on LED lighting discussions"""

    print("=" * 70)
    print("EXPERT AUTHORITY MODULE - TIER 1 ANALYSIS")
    print("=" * 70)
    print()
    print("⚙️  Configuration:")
    print("   - Tier: 1 (Essential)")
    print("   - Platforms: Reddit only")
    print("   - Analysis: Rule-based theme extraction")
    print("   - Output: HTML report with citations")
    print()
    print("📋 Query: LED strip lighting")
    print("🔍 Subreddits: electricians, homeimprovement, DIY")
    print()

    # Confirm credentials
    print("⚠️  IMPORTANT: Ensure config/.env has valid Reddit credentials")
    print("   - REDDIT_CLIENT_ID")
    print("   - REDDIT_CLIENT_SECRET")
    print("   - REDDIT_USER_AGENT")
    print()

    input("Press Enter to start analysis...")
    print()

    try:
        # Initialize orchestrator
        print("🚀 Initializing Tier 1 orchestrator...")
        orchestrator = ExpertAuthorityOrchestrator(tier=1)
        print("✅ Orchestrator initialized")
        print()

        # Run analysis
        results = orchestrator.run_analysis(
            query="LED strip lighting",
            project_name="LED_Strip_Expert_Analysis",
            reddit_subreddits=["electricians", "homeimprovement", "DIY"]
        )

        # Print results
        print()
        print("=" * 70)
        print("✅ ANALYSIS COMPLETE")
        print("=" * 70)
        print()
        print(f"📊 Platforms analyzed: {', '.join(results['platforms_used'])}")
        print()
        print("📄 Generated files:")
        if 'reddit_cache' in results:
            print(f"   - Reddit cache: {results['reddit_cache']}")
        if 'analysis_file' in results:
            print(f"   - Analysis JSON: {results['analysis_file']}")
        if 'html' in results['reports']:
            print(f"   - HTML report: {results['reports']['html']}")
        print()

        if results['errors']:
            print("⚠️  Warnings:")
            for error in results['errors']:
                print(f"   - {error}")
            print()

        print("✅ SUCCESS: Tier 1 analysis complete!")
        print()
        print("🔗 Next steps:")
        print("   1. Open the HTML report to view results")
        print("   2. Verify all citations link to real Reddit discussions")
        print("   3. If satisfied, proceed to Tier 2 analysis")
        print()

        return 0

    except Exception as e:
        print()
        print("=" * 70)
        print("❌ ANALYSIS FAILED")
        print("=" * 70)
        print()
        print(f"Error: {e}")
        print()
        print("🔍 Troubleshooting:")
        print("   1. Check that config/.env exists with valid Reddit credentials")
        print("   2. Run: python -c 'import praw; print(praw.__version__)' to verify PRAW is installed")
        print("   3. Check SETUP-API-CREDENTIALS.md for credential setup instructions")
        print()

        return 1


if __name__ == "__main__":
    sys.exit(main())
