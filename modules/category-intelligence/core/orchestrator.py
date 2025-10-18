"""
Category Intelligence Orchestrator - LEGACY SYSTEM (Currently Active)

⚠️ IMPORTANT: This is the LEGACY pipeline coordinator
   - Currently used by: run_analysis.py (main entry point)
   - Status: Active and production-ready
   - Migration: Will be replaced by agents/orchestrator.py in Stage 8

   See AGENTIC_ARCHITECTURE.md for migration roadmap.
   See agents/orchestrator.py for the new AI-guided system.

Main coordinator for category research pipeline
"""

from pathlib import Path
from typing import Dict, Optional
import logging
import sys

from core.config import config, CategoryConfig
from core.source_tracker import SourceTracker
from core.preflight_validator import PreflightValidator
from core.environment_checker import EnvironmentChecker
from collectors.brand_discovery import BrandDiscovery
from collectors.taxonomy_builder import TaxonomyBuilder
from collectors.pricing_analyzer import PricingAnalyzer
from collectors.market_researcher import MarketResearcher
from collectors.resource_curator import ResourceCurator
from collectors.consumer_insights import ConsumerInsightsCollector
from generators.html_reporter import HTMLReporter

logger = logging.getLogger(__name__)


class CategoryIntelligenceOrchestrator:
    """
    Main orchestrator for category intelligence research

    Coordinates all stages of research pipeline:
    1. Brand Discovery
    2. Product Categorization
    3. Pricing Analysis
    4. Market Share Research
    5. Market Size Analysis
    6. Learning Resources
    7. Consumer Insights (optional - if video data available)
    8. Source Validation
    9. Report Generation
    """

    def __init__(self, custom_config: Optional[CategoryConfig] = None):
        """Initialize orchestrator with optional custom config"""
        self.config = custom_config or config
        self.source_tracker = SourceTracker(self.config.outputs_dir)
        self.env_checker = EnvironmentChecker()

        # Initialize components
        self.brand_discovery = BrandDiscovery(self.config)
        self.taxonomy_builder = TaxonomyBuilder(self.config)
        self.pricing_analyzer = PricingAnalyzer(self.config)
        self.market_researcher = MarketResearcher(self.config)
        self.resource_curator = ResourceCurator(self.config)
        self.consumer_insights = ConsumerInsightsCollector(self.config)
        self.html_reporter = HTMLReporter(self.config)

        logger.info(f"Category Intelligence Orchestrator initialized")
        logger.info(f"Output directory: {self.config.outputs_dir}")

    def check_readiness(self) -> Dict:
        """
        Check if environment is ready for analysis.

        Returns:
            Dict with readiness status and detailed report
        """
        ready, checks = self.env_checker.check_all_sources()
        report = self.env_checker.generate_readiness_report()
        missing = self.env_checker.get_missing_requirements()

        return {
            "ready": ready,
            "report": report,
            "missing_required": missing["required"],
            "missing_recommended": missing["recommended"],
            "missing_optional": missing["optional"],
            "checks": checks
        }

    def analyze_category(
        self,
        category_name: str,
        output_name: Optional[str] = None,
    ) -> Dict:
        """
        Run complete category intelligence analysis

        Args:
            category_name: Category to analyze (e.g., "Smart Home Lighting")
            output_name: Optional custom output file name

        Returns:
            Dict containing all analysis results and paths
        """
        logger.info(f"Starting category analysis: {category_name}")

        if not output_name:
            output_name = category_name.replace(" ", "_")

        results = {
            "category": category_name,
            "analysis_date": self.config.current_date,
            "status": "initialized",
        }

        try:
            # Stage 1: Brand Discovery
            logger.info("Stage 1: Discovering major brands...")
            results["brands"] = self._discover_brands(category_name)

            # Stage 2: Product Categorization
            logger.info("Stage 2: Building product taxonomy...")
            results["taxonomy"] = self._build_taxonomy(category_name)

            # Stage 3: Pricing Analysis
            logger.info("Stage 3: Analyzing pricing...")
            results["pricing"] = self._analyze_pricing(category_name)

            # Stage 4: Market Share Research
            logger.info("Stage 4: Researching market share...")
            results["market_share"] = self._research_market_share(category_name)

            # Stage 5: Market Size Analysis
            logger.info("Stage 5: Analyzing market size...")
            results["market_size"] = self._analyze_market_size(category_name)

            # Stage 6: Learning Resources
            logger.info("Stage 6: Curating learning resources...")
            results["resources"] = self._find_resources(category_name)

            # Stage 7: Validate Sources
            logger.info("Stage 7: Validating all sources...")
            results["source_validation"] = self.source_tracker.validate_sources()

            # Stage 7.5: PREFLIGHT VALIDATION - ZERO FABRICATION CHECK
            logger.info("Stage 7.5: Running preflight validation...")
            preflight_validator = PreflightValidator(mode="production")
            preflight_passed, preflight_issues = preflight_validator.validate_sources(
                self.source_tracker,
                results
            )

            # Generate preflight report
            preflight_report = preflight_validator.generate_preflight_report(
                preflight_passed,
                preflight_issues,
                self.source_tracker
            )

            # Log preflight report
            logger.info("\n" + preflight_report)

            # Store preflight results
            results["preflight_validation"] = {
                "passed": preflight_passed,
                "issues": preflight_issues,
                "report": preflight_report
            }

            # BLOCK report generation if preflight fails
            if not preflight_passed:
                logger.error("="*60)
                logger.error("❌ REPORT GENERATION BLOCKED")
                logger.error("="*60)
                logger.error("Preflight validation failed - insufficient real sources detected.")
                logger.error("This indicates the system is generating fabricated/hardcoded data.")
                logger.error("")
                logger.error("ZERO FABRICATION POLICY VIOLATION:")
                for i, issue in enumerate(preflight_issues, 1):
                    logger.error(f"  {i}. {issue}")
                logger.error("")
                logger.error("ACTION REQUIRED:")
                logger.error("  1. Complete Stage 3: Collector Integration")
                logger.error("  2. Integrate real data sources (WebSearch, APIs, scraping)")
                logger.error("  3. Ensure all collectors return Source objects with URLs")
                logger.error("  4. Re-run analysis after integration")
                logger.error("="*60)

                results["status"] = "blocked_fabrication"
                results["error"] = "Preflight validation failed - zero fabrication policy violated"
                results["html_path"] = None

                # Do NOT generate report - return early
                return results

            # Stage 8: Generate Report (only if preflight passed)
            logger.info("Stage 8: Generating HTML report...")
            logger.info("✅ Preflight validation passed - proceeding with report generation")
            results["html_path"] = self._generate_report(
                category_name,
                output_name,
                results
            )

            # Export audit trail
            results["audit_path"] = self.source_tracker.export_audit_trail()
            results["citations_path"] = self.source_tracker.export_citation_list()

            results["status"] = "completed"
            logger.info(f"Category analysis complete: {category_name}")

        except Exception as e:
            logger.error(f"Analysis failed: {e}", exc_info=True)
            results["status"] = "failed"
            results["error"] = str(e)

        return results

    def _discover_brands(self, category: str) -> Dict:
        """Stage 1: Discover major brands in category"""
        return self.brand_discovery.discover_brands(category)

    def _build_taxonomy(self, category: str) -> Dict:
        """Stage 2: Build product categorization hierarchy"""
        return self.taxonomy_builder.build_taxonomy(category)

    def _analyze_pricing(self, category: str) -> Dict:
        """Stage 3: Analyze pricing across tiers"""
        return self.pricing_analyzer.analyze_pricing(category)

    def _research_market_share(self, category: str) -> Dict:
        """Stage 4: Research market share data"""
        return self.market_researcher.research_market_share(category)

    def _analyze_market_size(self, category: str) -> Dict:
        """Stage 5: Analyze market size and projections"""
        return self.market_researcher.analyze_market_size(category)

    def _find_resources(self, category: str) -> Dict:
        """Stage 6: Find learning resources"""
        return self.resource_curator.find_resources(category)

    def _generate_report(
        self,
        category: str,
        output_name: str,
        data: Dict
    ) -> Path:
        """Stage 8: Generate HTML report"""
        return self.html_reporter.generate_report(category, output_name, data)

    def analyze_consumer_videos(
        self,
        category: str,
        video_data: list[Dict],
        output_name: Optional[str] = None
    ) -> Dict:
        """
        Analyze consumer video data to extract JTBD insights

        Args:
            category: Product category (e.g., "Lighting Installation")
            video_data: List of processed video data with:
                - video_id: Unique identifier
                - transcript: Full verbatim transcript with timestamps
                - emotions: Acoustic emotion analysis results
                - visual_context: Frame-by-frame visual analysis
                - pain_points: Extracted pain points
            output_name: Optional custom output file name

        Returns:
            Dict containing consumer insights and report path

        Example:
            ```python
            video_data = [
                {
                    'video_id': 'video_0001',
                    'transcript': [{'timestamp': 32.6, 'text': '...'}],
                    'emotions': {'timeline': [...]},
                    'visual_context': {...},
                    'pain_points': [...]
                }
            ]
            results = orchestrator.analyze_consumer_videos(
                'Lighting Installation',
                video_data
            )
            ```
        """
        logger.info(f"Starting consumer insights analysis: {category}")
        logger.info(f"Total videos: {len(video_data)}")

        if not output_name:
            output_name = f"{category.replace(' ', '_')}_Consumer_JTBD"

        results = {
            "category": category,
            "analysis_date": self.config.current_date,
            "status": "initialized",
            "total_videos": len(video_data)
        }

        try:
            # Stage 1: Analyze consumer videos with JTBD framework
            logger.info("Stage 1: Extracting JTBD patterns from consumer videos...")
            insights = self.consumer_insights.analyze_consumer_videos(
                category=category,
                video_data=video_data
            )

            results["consumer_insights"] = insights
            results["core_jobs_count"] = len(insights.core_jobs)
            results["framework_compliance"] = insights.framework_compliance

            # Stage 2: Generate JTBD report data
            logger.info("Stage 2: Preparing JTBD report data...")
            report_data = self.consumer_insights.generate_jtbd_report_data(insights)
            results["report_data"] = report_data

            # Stage 3: Generate HTML report (if HTML reporter supports JTBD)
            logger.info("Stage 3: Generating JTBD HTML report...")
            # Note: HTML reporter would need a separate method for JTBD reports
            # For now, store the report data for external report generation
            results["ready_for_report"] = True

            results["status"] = "completed"
            logger.info(f"Consumer insights analysis complete")
            logger.info(f"Framework compliance: {insights.framework_compliance['overall_score']}/100")

        except Exception as e:
            logger.error(f"Consumer insights analysis failed: {e}", exc_info=True)
            results["status"] = "failed"
            results["error"] = str(e)

        return results

    def __repr__(self) -> str:
        return f"<CategoryIntelligenceOrchestrator sources={len(self.source_tracker)}>"
