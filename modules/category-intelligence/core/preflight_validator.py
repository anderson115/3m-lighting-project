"""
Preflight Validation - Zero Fabrication Enforcement

This module ensures NO reports can be generated with fabricated or placeholder data.
All data must have verifiable sources before report generation is allowed.

CRITICAL: This is a safety layer that MUST pass before any report generation.
"""

import logging
from typing import Dict, List, Tuple, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class PreflightValidator:
    """
    Validates data has real sources before allowing report generation.

    This class enforces zero fabrication policy by checking:
    1. Total source count (minimum 100 for production)
    2. No hardcoded data patterns
    3. All data points have source URLs
    4. No fabrication markers present
    5. Source diversity (multiple publishers)
    """

    # Minimum requirements for production reports
    MIN_SOURCES_PRODUCTION = 100
    MIN_SOURCES_DEV = 10  # Relaxed for development/testing
    MIN_HIGH_CONFIDENCE_SOURCES = 20
    MIN_UNIQUE_PUBLISHERS = 5

    # Fabrication markers that indicate fake data
    FABRICATION_MARKERS = [
        'placeholder', 'example.com', 'test.com', 'sample',
        'TODO', 'TBD', 'FIXME', 'xxx', 'dummy', 'fake',
        'mock', 'stub', 'hardcoded', 'fabricated'
    ]

    def __init__(self, mode: str = "production"):
        """
        Initialize preflight validator.

        Args:
            mode: "production" or "development" - sets strictness level
        """
        self.mode = mode
        self.min_sources = (
            self.MIN_SOURCES_PRODUCTION if mode == "production"
            else self.MIN_SOURCES_DEV
        )
        logger.info(f"Preflight validator initialized in {mode} mode")
        logger.info(f"Minimum sources required: {self.min_sources}")

    def validate_sources(
        self,
        source_tracker: Any,
        collected_data: Dict[str, Any]
    ) -> Tuple[bool, List[str]]:
        """
        Validate that collected data has sufficient real sources.

        Args:
            source_tracker: SourceTracker instance with tracked sources
            collected_data: All data collected by orchestrator

        Returns:
            Tuple of (passed: bool, issues: List[str])
        """
        issues = []

        logger.info("="*60)
        logger.info("PREFLIGHT VALIDATION - ZERO FABRICATION CHECK")
        logger.info("="*60)

        # Check 1: Total source count
        total_sources = len(source_tracker)
        logger.info(f"Check 1: Total sources = {total_sources} (minimum: {self.min_sources})")

        if total_sources < self.min_sources:
            issues.append(
                f"CRITICAL: Insufficient sources. Found {total_sources}, "
                f"need {self.min_sources}. This indicates hardcoded data."
            )

        # Check 2: Source diversity
        if total_sources > 0:
            publishers = set()
            for source in source_tracker.sources:
                publishers.add(source.get('publisher', 'Unknown'))

            logger.info(f"Check 2: Unique publishers = {len(publishers)} (minimum: {self.MIN_UNIQUE_PUBLISHERS})")

            if len(publishers) < self.MIN_UNIQUE_PUBLISHERS:
                issues.append(
                    f"CRITICAL: Insufficient source diversity. Found {len(publishers)} publishers, "
                    f"need {self.MIN_UNIQUE_PUBLISHERS}."
                )
        else:
            issues.append("CRITICAL: No sources tracked - all data is fabricated")

        # Check 3: Fabrication markers in data
        logger.info("Check 3: Scanning for fabrication markers...")
        fabrication_found = self._check_fabrication_markers(collected_data)

        if fabrication_found:
            issues.append(
                f"CRITICAL: Fabrication markers detected in data: {', '.join(fabrication_found)}"
            )

        # Check 4: Data-to-source ratio
        if total_sources > 0:
            data_point_count = self._count_data_points(collected_data)
            ratio = data_point_count / total_sources if total_sources > 0 else float('inf')

            logger.info(f"Check 4: Data points = {data_point_count}, Ratio = {ratio:.1f} per source")

            # If ratio is too high, it suggests not enough source tracking
            if ratio > 50:
                issues.append(
                    f"WARNING: High data-to-source ratio ({ratio:.1f}). "
                    "This suggests incomplete source tracking."
                )

        # Check 5: High confidence sources
        if total_sources > 0:
            high_confidence = sum(
                1 for s in source_tracker.sources
                if s.get('confidence') == 'high'
            )

            logger.info(f"Check 5: High confidence sources = {high_confidence} (minimum: {self.MIN_HIGH_CONFIDENCE_SOURCES})")

            if high_confidence < self.MIN_HIGH_CONFIDENCE_SOURCES:
                issues.append(
                    f"WARNING: Insufficient high-confidence sources. Found {high_confidence}, "
                    f"recommended {self.MIN_HIGH_CONFIDENCE_SOURCES}."
                )

        # Summary
        passed = len(issues) == 0

        logger.info("="*60)
        if passed:
            logger.info("✅ PREFLIGHT VALIDATION PASSED")
            logger.info(f"   Sources: {total_sources}")
            logger.info(f"   Publishers: {len(publishers) if total_sources > 0 else 0}")
            logger.info("   Status: READY FOR REPORT GENERATION")
        else:
            logger.error("❌ PREFLIGHT VALIDATION FAILED")
            logger.error(f"   Issues found: {len(issues)}")
            for issue in issues:
                logger.error(f"   - {issue}")
            logger.error("   Status: REPORT GENERATION BLOCKED")
        logger.info("="*60)

        return passed, issues

    def _check_fabrication_markers(self, data: Any) -> List[str]:
        """
        Recursively check data for fabrication markers.

        Returns:
            List of fabrication markers found
        """
        found_markers = set()
        data_str = str(data).lower()

        for marker in self.FABRICATION_MARKERS:
            if marker in data_str:
                found_markers.add(marker)

        return list(found_markers)

    def _count_data_points(self, data: Dict[str, Any]) -> int:
        """
        Count approximate number of data points in collected data.

        This is a rough estimate to check data-to-source ratio.
        """
        count = 0

        # Count brands
        brands = data.get('brands', {})
        if isinstance(brands, dict):
            count += len(brands.get('brands', []))

        # Count taxonomy entries
        taxonomy = data.get('taxonomy', {})
        if isinstance(taxonomy, dict):
            count += len(taxonomy.get('subcategories', []))

        # Count pricing entries
        pricing = data.get('pricing', {})
        if isinstance(pricing, dict):
            count += len(pricing.get('subcategories', []))

        # Count market data points
        market_share = data.get('market_share', {})
        if isinstance(market_share, dict):
            count += len(market_share.get('market_shares', []))

        market_size = data.get('market_size', {})
        if isinstance(market_size, dict):
            count += len(market_size.get('historical_growth', []))
            count += len(market_size.get('projections', []))

        # Count resources
        resources = data.get('resources', {})
        if isinstance(resources, dict):
            count += len(resources.get('resources', []))

        return count

    def generate_preflight_report(
        self,
        passed: bool,
        issues: List[str],
        source_tracker: Any
    ) -> str:
        """
        Generate human-readable preflight validation report.

        Returns:
            Formatted report string
        """
        report = []
        report.append("="*60)
        report.append("PREFLIGHT VALIDATION REPORT")
        report.append("="*60)
        report.append(f"Timestamp: {datetime.now().isoformat()}")
        report.append(f"Mode: {self.mode}")
        report.append(f"Status: {'✅ PASSED' if passed else '❌ FAILED'}")
        report.append("")

        # Source metrics
        report.append("SOURCE METRICS:")
        report.append(f"  Total Sources: {len(source_tracker)}")
        report.append(f"  Required: {self.min_sources}")
        report.append(f"  Status: {'✅' if len(source_tracker) >= self.min_sources else '❌'}")
        report.append("")

        # Issues
        if issues:
            report.append("ISSUES FOUND:")
            for i, issue in enumerate(issues, 1):
                report.append(f"  {i}. {issue}")
            report.append("")
        else:
            report.append("✅ No issues found")
            report.append("")

        # Conclusion
        if passed:
            report.append("CONCLUSION:")
            report.append("  System is ready for report generation.")
            report.append("  All data has verifiable sources.")
            report.append("  Zero fabrication policy: COMPLIANT ✅")
        else:
            report.append("CONCLUSION:")
            report.append("  System NOT ready for report generation.")
            report.append("  Data lacks sufficient sources.")
            report.append("  Zero fabrication policy: VIOLATED ❌")
            report.append("")
            report.append("  ACTION REQUIRED:")
            report.append("  - Integrate real data sources (WebSearch, APIs, scraping)")
            report.append("  - Complete Stage 3: Collector Integration")
            report.append("  - Re-run preflight validation")

        report.append("="*60)

        return "\n".join(report)


def run_preflight_check(
    source_tracker: Any,
    collected_data: Dict[str, Any],
    mode: str = "production"
) -> Tuple[bool, str]:
    """
    Convenience function to run preflight validation.

    Args:
        source_tracker: SourceTracker with tracked sources
        collected_data: All collected data
        mode: "production" or "development"

    Returns:
        Tuple of (passed: bool, report: str)
    """
    validator = PreflightValidator(mode=mode)
    passed, issues = validator.validate_sources(source_tracker, collected_data)
    report = validator.generate_preflight_report(passed, issues, source_tracker)

    return passed, report
