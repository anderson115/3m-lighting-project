"""
Category Intelligence Orchestrator
Main coordinator for category research pipeline
"""

from pathlib import Path
from typing import Dict, Optional
import logging

from .config import config, CategoryConfig
from .source_tracker import SourceTracker
from ..collectors.brand_discovery import BrandDiscovery
from ..collectors.taxonomy_builder import TaxonomyBuilder
from ..collectors.pricing_analyzer import PricingAnalyzer
from ..collectors.market_researcher import MarketResearcher
from ..collectors.resource_curator import ResourceCurator
from ..generators.html_reporter import HTMLReporter

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
    7. Source Validation
    8. Report Generation
    """

    def __init__(self, custom_config: Optional[CategoryConfig] = None):
        """Initialize orchestrator with optional custom config"""
        self.config = custom_config or config
        self.source_tracker = SourceTracker(self.config.outputs_dir)

        # Initialize components
        self.brand_discovery = BrandDiscovery(self.config)
        self.taxonomy_builder = TaxonomyBuilder(self.config)
        self.pricing_analyzer = PricingAnalyzer(self.config)
        self.market_researcher = MarketResearcher(self.config)
        self.resource_curator = ResourceCurator(self.config)
        self.html_reporter = HTMLReporter(self.config)

        logger.info(f"Category Intelligence Orchestrator initialized")
        logger.info(f"Output directory: {self.config.outputs_dir}")

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

            # Stage 8: Generate Report
            logger.info("Stage 8: Generating HTML report...")
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

    def __repr__(self) -> str:
        return f"<CategoryIntelligenceOrchestrator sources={len(self.source_tracker)}>"
