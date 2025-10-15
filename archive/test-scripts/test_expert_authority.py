#!/usr/bin/env python3
"""
Quick test of expert authority module with real Reddit API
"""

import sys
import os

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

from expert_authority.core.config import Config
from expert_authority.scrapers.reddit_scraper import RedditScraper
from expert_authority.analyzers.production_analyzer import ProductionAnalyzer
from expert_authority.reporters.html_reporter import HTMLReporter

import logging
logging.basicConfig(level=logging.INFO)

print("=" * 70)
print("EXPERT AUTHORITY - QUICK TEST")
print("=" * 70)
print()

# Test 1: Configuration
print("Test 1: Loading configuration...")
try:
    config = Config()
    config.validate_credentials(tier=1)
    print("✅ Configuration loaded")
    print(f"   Reddit client ID: {config.reddit_client_id[:10]}...")
    print()
except Exception as e:
    print(f"❌ Configuration failed: {e}")
    sys.exit(1)

# Test 2: Reddit Scraper
print("Test 2: Scraping 10 real Reddit posts...")
try:
    scraper = RedditScraper(config)
    discussions = scraper.scrape(
        query="LED strip lighting",
        subreddits=["electricians"],
        limit=10
    )
    print(f"✅ Scraped {len(discussions)} real discussions")
    if discussions:
        print(f"   Example: {discussions[0]['title']}")
        print(f"   URL: {discussions[0]['url']}")
    print()
except Exception as e:
    print(f"❌ Scraping failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Analyzer
print("Test 3: Analyzing themes...")
try:
    analyzer = ProductionAnalyzer(tier=1, config=config)
    analysis = analyzer.analyze(discussions)
    print(f"✅ Analysis complete")
    print(f"   Themes found: {len(analysis['themes'])}")
    print(f"   Consensus patterns: {len(analysis['consensus_patterns'])}")
    if analysis['themes']:
        print(f"   Top theme: {analysis['themes'][0]['theme']} ({analysis['themes'][0]['frequency_pct']}%)")
    print()
except Exception as e:
    print(f"❌ Analysis failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Reporter
print("Test 4: Generating HTML report...")
try:
    reporter = HTMLReporter(tier=1, config=config)
    report_path = reporter.generate(analysis, discussions, "Test_Analysis")
    print(f"✅ Report generated")
    print(f"   Path: {report_path}")
    print()
except Exception as e:
    print(f"❌ Report generation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=" * 70)
print("✅ ALL TESTS PASSED")
print("=" * 70)
print()
print(f"📄 Open report: open {report_path}")
print()
