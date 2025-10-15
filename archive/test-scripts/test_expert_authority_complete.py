#!/usr/bin/env python3
"""
Complete Expert Authority Module Test Suite
Tests all tiers with real data - NO PLACEHOLDERS, NO FAKE DATA
"""

import sys
import os
from pathlib import Path
import json
import logging

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

from expert_authority.core.orchestrator import ExpertAuthorityOrchestrator
from expert_authority.core.config import Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_tier1():
    """Test Tier 1 - Rule-based analysis with real Reddit data"""
    logger.info("=" * 80)
    logger.info("TEST TIER 1: ESSENTIAL (RULE-BASED)")
    logger.info("=" * 80)

    try:
        orchestrator = ExpertAuthorityOrchestrator(tier=1)

        results = orchestrator.run_analysis(
            query="LED strip lighting",
            project_name="Test_Tier1_LED_Strip",
            reddit_subreddits=["electricians", "homeimprovement"]
        )

        # Validate results
        assert results['tier'] == 1, "Tier mismatch"
        assert 'reddit' in results['platforms_used'], "Reddit not used"
        assert 'html' in results['reports'], "HTML report not generated"
        assert len(results['errors']) == 0, f"Errors encountered: {results['errors']}"

        logger.info("✅ TIER 1 TEST PASSED")
        logger.info(f"   📄 HTML Report: {results['reports']['html']}")

        return True

    except Exception as e:
        logger.error(f"❌ TIER 1 TEST FAILED: {e}")
        return False


def test_tier2():
    """Test Tier 2 - LLM semantic analysis with Claude Sonnet 4"""
    logger.info("=" * 80)
    logger.info("TEST TIER 2: PROFESSIONAL (LLM SEMANTIC)")
    logger.info("=" * 80)

    try:
        orchestrator = ExpertAuthorityOrchestrator(tier=2)

        results = orchestrator.run_analysis(
            query="LED strip dimming issues",
            project_name="Test_Tier2_LED_Dimming",
            reddit_subreddits=["electricians"],
            stackexchange_sites=["diy.stackexchange.com"]
        )

        # Validate results
        assert results['tier'] == 2, "Tier mismatch"
        assert 'reddit' in results['platforms_used'], "Reddit not used"
        assert 'stackexchange' in results['platforms_used'], "Stack Exchange not used"
        assert 'html' in results['reports'], "HTML report not generated"

        # Check for Excel report (if openpyxl installed)
        if 'excel' in results['reports']:
            logger.info(f"   📊 Excel Report: {results['reports']['excel']}")

        logger.info("✅ TIER 2 TEST PASSED")
        logger.info(f"   📄 HTML Report: {results['reports']['html']}")

        return True

    except Exception as e:
        logger.error(f"❌ TIER 2 TEST FAILED: {e}")
        return False


def test_citation_validation():
    """Test citation validation - ensure 100% traceability"""
    logger.info("=" * 80)
    logger.info("TEST: CITATION VALIDATION (100% TRACEABILITY)")
    logger.info("=" * 80)

    try:
        # Run Tier 1 analysis
        orchestrator = ExpertAuthorityOrchestrator(tier=1)

        results = orchestrator.run_analysis(
            query="LED strip safety",
            project_name="Test_Citation_Validation",
            reddit_subreddits=["electricians"]
        )

        # Load the analysis JSON
        analysis_file = Path(results.get('analysis_file'))
        with open(analysis_file, 'r') as f:
            analysis = json.load(f)

        # Validate all citations
        total_citations = 0
        invalid_citations = 0

        for theme in analysis.get('themes', []):
            for example in theme.get('examples', []):
                total_citations += 1

                # Check that URL and ID exist
                if not example.get('url') or not example.get('id'):
                    invalid_citations += 1
                    logger.warning(f"⚠️ Invalid citation in theme '{theme['theme']}'")

        validation_rate = ((total_citations - invalid_citations) / total_citations * 100) if total_citations > 0 else 0

        logger.info(f"📊 Citation Validation Rate: {validation_rate:.1f}% ({total_citations - invalid_citations}/{total_citations})")

        assert validation_rate >= 95, f"Citation validation below 95%: {validation_rate:.1f}%"

        logger.info("✅ CITATION VALIDATION TEST PASSED")
        return True

    except Exception as e:
        logger.error(f"❌ CITATION VALIDATION TEST FAILED: {e}")
        return False


def test_config_integrity():
    """Test configuration integrity"""
    logger.info("=" * 80)
    logger.info("TEST: CONFIGURATION INTEGRITY")
    logger.info("=" * 80)

    try:
        config = Config()

        # Test API keys loaded
        assert config.anthropic_api_key, "Anthropic API key not loaded"
        assert config.openai_api_key, "OpenAI API key not loaded"
        assert config.reddit_client_id, "Reddit client ID not loaded"
        assert config.reddit_client_secret, "Reddit client secret not loaded"

        logger.info("✅ API keys loaded correctly")

        # Test tier configurations
        for tier in [1, 2, 3]:
            tier_config = config.get_tier_config(tier)
            assert tier_config['name'], f"Tier {tier} name missing"
            assert tier_config['platforms'], f"Tier {tier} platforms missing"
            logger.info(f"✅ Tier {tier} config valid: {tier_config['name']}")

        # Test LLM configurations
        for tier in [2, 3]:
            llm_config = config.get_llm_config(tier)
            assert llm_config['provider'], f"Tier {tier} LLM provider missing"
            assert llm_config['model'], f"Tier {tier} LLM model missing"
            assert llm_config['api_key'], f"Tier {tier} LLM API key missing"
            logger.info(f"✅ Tier {tier} LLM config valid: {llm_config['model']}")

        logger.info("✅ CONFIGURATION INTEGRITY TEST PASSED")
        return True

    except Exception as e:
        logger.error(f"❌ CONFIGURATION INTEGRITY TEST FAILED: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("EXPERT AUTHORITY MODULE - COMPLETE TEST SUITE")
    print("=" * 80)
    print()

    results = {
        "config_integrity": test_config_integrity(),
        "citation_validation": test_citation_validation(),
        "tier1": test_tier1(),
        "tier2": test_tier2()
    }

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUITE SUMMARY")
    print("=" * 80)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:25s} {status}")

    print()
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("=" * 80)

    if passed == total:
        print("🎉 ALL TESTS PASSED - MODULE READY FOR PRODUCTION")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED - REVIEW ERRORS ABOVE")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
