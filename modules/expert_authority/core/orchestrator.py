#!/usr/bin/env python3
"""
Expert Authority Orchestrator - Complete Pipeline Coordination
Coordinates scraping, analysis, and reporting with error handling
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import logging

from ..core.config import Config
from ..scrapers.reddit_scraper import RedditScraper
from ..scrapers.stackexchange_scraper import StackExchangeScraper
from ..analyzers.production_analyzer import ProductionAnalyzer
from ..reporters.html_reporter import HTMLReporter


class ExpertAuthorityOrchestrator:
    """Orchestrates the complete expert authority analysis pipeline"""

    def __init__(self, tier: int = 1):
        """
        Initialize orchestrator

        Args:
            tier: Analysis tier (1 = Essential, 2 = Professional, 3 = Enterprise)
        """
        self.tier = tier
        self.config = Config()
        self.tier_config = self.config.get_tier_config(tier)

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

        # Validate credentials for tier
        try:
            self.config.validate_credentials(tier)
            self.logger.info(f"✅ Credentials validated for Tier {tier}")
        except Exception as e:
            self.logger.error(f"❌ Credential validation failed: {e}")
            raise

        # Initialize components
        self.reddit_scraper = RedditScraper(self.config)
        self.stackexchange_scraper = None

        if tier >= 2 and 'stackexchange' in self.tier_config['platforms']:
            self.stackexchange_scraper = StackExchangeScraper(self.config)

        self.analyzer = ProductionAnalyzer(tier, self.config)
        self.reporter = HTMLReporter(tier, self.config)

        # Data directory
        self.data_dir = Path(__file__).parent.parent / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def run_analysis(
        self,
        query: str,
        project_name: Optional[str] = None,
        reddit_subreddits: Optional[List[str]] = None,
        stackexchange_sites: Optional[List[str]] = None
    ) -> Dict:
        """
        Run complete expert authority analysis pipeline

        Args:
            query: Search query (e.g., "LED strip lighting")
            project_name: Name of the project (for reports)
            reddit_subreddits: List of subreddits to search (default: electricians, homeimprovement, DIY)
            stackexchange_sites: List of Stack Exchange sites (default: diy, electronics)

        Returns:
            Dictionary with paths to generated reports and analysis data
        """
        self.logger.info(f"🚀 Starting Tier {self.tier} Expert Authority Analysis")
        self.logger.info(f"📋 Query: {query}")

        # Set defaults
        project_name = project_name or f"Expert_Analysis_{query.replace(' ', '_')}"
        reddit_subreddits = reddit_subreddits or ["electricians", "homeimprovement", "DIY"]
        stackexchange_sites = stackexchange_sites or ["diy.stackexchange.com", "electronics.stackexchange.com"]

        results = {
            "tier": self.tier,
            "query": query,
            "project_name": project_name,
            "timestamp": datetime.now().isoformat(),
            "platforms_used": [],
            "reports": {},
            "errors": []
        }

        try:
            # Stage 1: Data Collection
            self.logger.info("=" * 60)
            self.logger.info("STAGE 1: DATA COLLECTION")
            self.logger.info("=" * 60)

            all_discussions = []

            # Scrape Reddit
            try:
                self.logger.info(f"📡 Scraping Reddit ({', '.join(reddit_subreddits)})...")
                reddit_discussions = self.reddit_scraper.scrape(
                    query=query,
                    subreddits=reddit_subreddits,
                    limit=self.tier_config['discussion_limit'] // len(reddit_subreddits)
                )
                all_discussions.extend(reddit_discussions)
                results['platforms_used'].append('reddit')
                self.logger.info(f"✅ Reddit: {len(reddit_discussions)} discussions scraped")

                # Save Reddit cache
                reddit_cache = self.reddit_scraper.save_to_cache(reddit_discussions, f"{project_name}_reddit")
                results['reddit_cache'] = str(reddit_cache)

            except Exception as e:
                self.logger.error(f"❌ Reddit scraping failed: {e}")
                results['errors'].append(f"Reddit scraping failed: {e}")

            # Scrape Stack Exchange (Tier 2+)
            if self.stackexchange_scraper:
                try:
                    self.logger.info(f"📡 Scraping Stack Exchange ({', '.join(stackexchange_sites)})...")
                    se_discussions = self.stackexchange_scraper.scrape(
                        query=query,
                        sites=stackexchange_sites,
                        limit=self.tier_config['discussion_limit'] // (len(stackexchange_sites) * 2)
                    )
                    all_discussions.extend(se_discussions)
                    results['platforms_used'].append('stackexchange')
                    self.logger.info(f"✅ Stack Exchange: {len(se_discussions)} discussions scraped")

                    # Save Stack Exchange cache
                    se_cache = self.stackexchange_scraper.save_to_cache(se_discussions, f"{project_name}_stackexchange")
                    results['stackexchange_cache'] = str(se_cache)

                except Exception as e:
                    self.logger.error(f"❌ Stack Exchange scraping failed: {e}")
                    results['errors'].append(f"Stack Exchange scraping failed: {e}")

            if not all_discussions:
                raise ValueError("No discussions scraped from any platform")

            self.logger.info(f"📊 Total discussions collected: {len(all_discussions)}")

            # Stage 2: Analysis
            self.logger.info("=" * 60)
            self.logger.info("STAGE 2: SEMANTIC ANALYSIS")
            self.logger.info("=" * 60)

            analysis = self.analyzer.analyze(all_discussions)
            self.logger.info(f"✅ Analysis complete: {len(analysis['themes'])} themes discovered")

            # Save analysis JSON
            analysis_file = self.data_dir / f"{project_name}_analysis.json"
            with open(analysis_file, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            results['analysis_file'] = str(analysis_file)

            # Stage 3: Report Generation
            self.logger.info("=" * 60)
            self.logger.info("STAGE 3: REPORT GENERATION")
            self.logger.info("=" * 60)

            html_report = self.reporter.generate(analysis, all_discussions, project_name)
            results['reports']['html'] = str(html_report)
            self.logger.info(f"✅ HTML report generated: {html_report}")

            # Success summary
            self.logger.info("=" * 60)
            self.logger.info("✅ ANALYSIS COMPLETE")
            self.logger.info("=" * 60)
            self.logger.info(f"📊 Discussions analyzed: {len(all_discussions)}")
            self.logger.info(f"🎯 Themes discovered: {len(analysis['themes'])}")
            self.logger.info(f"✅ Consensus patterns: {len(analysis['consensus_patterns'])}")
            self.logger.info(f"📄 HTML report: {html_report}")

            return results

        except Exception as e:
            self.logger.error(f"❌ Pipeline failed: {e}")
            results['errors'].append(f"Pipeline failed: {e}")
            raise


if __name__ == "__main__":
    """Example usage - Run Tier 1 analysis"""

    # Initialize orchestrator
    orchestrator = ExpertAuthorityOrchestrator(tier=1)

    # Run analysis
    results = orchestrator.run_analysis(
        query="LED strip lighting installation",
        project_name="LED_Strip_Analysis"
    )

    print("\n" + "=" * 60)
    print("ANALYSIS RESULTS")
    print("=" * 60)
    print(f"Tier: {results['tier']}")
    print(f"Platforms: {', '.join(results['platforms_used'])}")
    print(f"HTML Report: {results['reports']['html']}")

    if results['errors']:
        print(f"\n⚠️  Errors encountered:")
        for error in results['errors']:
            print(f"  - {error}")
