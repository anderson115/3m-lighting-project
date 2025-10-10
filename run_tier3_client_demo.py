#!/usr/bin/env python3
"""
Tier 3 Client Demonstration - 3M Smart Lighting Market Entry
Professional deliverable showcasing Expert Authority Module capabilities
"""

import sys
import os
from pathlib import Path

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

from expert_authority.core.orchestrator import ExpertAuthorityOrchestrator

def run_tier3_demo():
    """
    Run Tier 3 analysis on manageable scope:
    - Broad topic: Residential LED retrofit market
    - Professional electrician perspectives
    - Limited to 2 subreddits for manageable size
    - Target: ~300-500 discussions (Tier 3 level)
    """

    print("\n" + "="*80)
    print("3M SMART LIGHTING - MARKET ENTRY INTELLIGENCE")
    print("Expert Authority Analysis - Tier 3 Professional Deliverable")
    print("="*80)
    print()

    orchestrator = ExpertAuthorityOrchestrator(tier=3)

    # Strategic query: Broad enough to capture market insights,
    # focused enough to be actionable for 3M
    results = orchestrator.run_analysis(
        query="residential LED lighting retrofit challenges",
        project_name="3M_Market_Entry_Residential_LED",
        reddit_subreddits=["electricians", "HomeImprovement"]
    )

    print("\n" + "="*80)
    print("✅ ANALYSIS COMPLETE")
    print("="*80)
    print()
    print(f"📊 Total Discussions: {results.get('discussion_count', 'N/A')}")
    print(f"📄 HTML Report: {results['reports']['html']}")

    if 'excel' in results['reports']:
        print(f"📊 Excel Report: {results['reports']['excel']}")

    print()
    print("Next: Create custom client deliverable with Offbrain Insights styling")
    print("="*80)

    return results

if __name__ == "__main__":
    results = run_tier3_demo()
