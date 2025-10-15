#!/usr/bin/env python3
"""
Quick 10% Volume Test - Expert Authority Module
Demonstrates production capability at reduced scale
"""

import sys
import os
from pathlib import Path
import json
import logging
from datetime import datetime

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

from expert_authority.core.orchestrator import ExpertAuthorityOrchestrator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_tier1_quick():
    """Quick Tier 1 test - 10% volume (10 discussions)"""
    logger.info("=" * 80)
    logger.info("QUICK TEST: TIER 1 (10% VOLUME)")
    logger.info("=" * 80)

    orchestrator = ExpertAuthorityOrchestrator(tier=1)

    # Run with reduced volume: 10 discussions instead of 100
    results = orchestrator.run_analysis(
        query="LED strip installation",
        project_name="Quick_Test_Tier1",
        reddit_subreddits=["electricians"]  # Single subreddit, limit will be 10
    )

    # Get analysis data
    analysis_file = results.get('analysis_file')
    if analysis_file and Path(analysis_file).exists():
        with open(analysis_file, 'r') as f:
            analysis = json.load(f)

        logger.info("=" * 80)
        logger.info("TIER 1 RESULTS (10% VOLUME)")
        logger.info("=" * 80)
        logger.info(f"✅ Discussions analyzed: {analysis['metadata']['total_discussions']}")
        logger.info(f"✅ Themes discovered: {len(analysis['themes'])}")
        logger.info(f"✅ Consensus patterns: {len(analysis['consensus_patterns'])}")
        logger.info(f"✅ Method: {analysis['metadata']['analysis_method']}")
        logger.info(f"📄 HTML Report: {results['reports']['html']}")

        # Show top 3 themes
        logger.info("\n🎯 Top Themes:")
        for i, theme in enumerate(analysis['themes'][:3], 1):
            logger.info(f"   {i}. {theme['theme']} ({theme['frequency_pct']}%)")

        return True

    return False


def test_tier2_quick():
    """Quick Tier 2 test - 10% volume with LLM (30 discussions)"""
    logger.info("\n" + "=" * 80)
    logger.info("QUICK TEST: TIER 2 LLM (10% VOLUME)")
    logger.info("=" * 80)

    orchestrator = ExpertAuthorityOrchestrator(tier=2)

    # Run with reduced volume: 30 discussions instead of 300
    results = orchestrator.run_analysis(
        query="LED dimmer compatibility",
        project_name="Quick_Test_Tier2",
        reddit_subreddits=["electricians"]  # Will get ~30 results
    )

    # Get analysis data
    analysis_file = results.get('analysis_file')
    if analysis_file and Path(analysis_file).exists():
        with open(analysis_file, 'r') as f:
            analysis = json.load(f)

        logger.info("=" * 80)
        logger.info("TIER 2 RESULTS (10% VOLUME - LLM SEMANTIC)")
        logger.info("=" * 80)
        logger.info(f"✅ Discussions analyzed: {analysis['metadata']['total_discussions']}")
        logger.info(f"✅ Themes discovered: {len(analysis['themes'])}")
        logger.info(f"✅ Consensus patterns: {len(analysis['consensus_patterns'])}")
        logger.info(f"✅ Safety warnings: {len(analysis.get('safety_warnings', []))}")
        logger.info(f"✅ Controversies: {len(analysis.get('controversies', []))}")
        logger.info(f"✅ Method: {analysis['metadata']['analysis_method']}")
        logger.info(f"📄 HTML Report: {results['reports']['html']}")
        if 'excel' in results['reports']:
            logger.info(f"📊 Excel Report: {results['reports']['excel']}")

        # Show top 3 themes with descriptions
        logger.info("\n🎯 Top Themes (LLM Analysis):")
        for i, theme in enumerate(analysis['themes'][:3], 1):
            logger.info(f"   {i}. {theme['theme']} ({theme['frequency_pct']}%)")
            if 'description' in theme and theme['description']:
                logger.info(f"      → {theme['description'][:80]}...")

        return True

    return False


def main():
    """Run quick volume tests"""
    start_time = datetime.now()

    print("\n" + "=" * 80)
    print("EXPERT AUTHORITY MODULE - QUICK 10% VOLUME TEST")
    print("=" * 80)
    print()

    results = {}

    # Test Tier 1 (10% volume)
    try:
        results['tier1'] = test_tier1_quick()
    except Exception as e:
        logger.error(f"Tier 1 test failed: {e}")
        results['tier1'] = False

    # Test Tier 2 (10% volume with LLM)
    try:
        results['tier2'] = test_tier2_quick()
    except Exception as e:
        logger.error(f"Tier 2 test failed: {e}")
        results['tier2'] = False

    # Summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print("\n" + "=" * 80)
    print("QUICK TEST SUMMARY")
    print("=" * 80)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:15s} {status}")

    print()
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print(f"Duration: {duration:.1f} seconds")
    print("=" * 80)

    if passed == total:
        print("🎉 QUICK TEST SUCCESSFUL - MODULE PERFORMING WELL AT 10% VOLUME")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
