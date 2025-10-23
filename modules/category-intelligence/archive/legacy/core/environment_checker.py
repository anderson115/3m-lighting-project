"""
Environment Checker - Data Source Availability Validation

Validates that required data sources are available before running analysis.
Provides clear guidance on what's missing and how to configure.
"""

import logging
import os
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class SourceStatus(str, Enum):
    """Data source availability status"""
    AVAILABLE = "available"
    MISSING = "missing"
    CONFIGURED_BUT_UNTESTED = "configured_but_untested"
    ERROR = "error"


@dataclass
class SourceCheck:
    """Result of checking a single data source"""
    name: str
    status: SourceStatus
    message: str
    priority: str  # "required", "recommended", "optional"
    setup_instructions: str


class EnvironmentChecker:
    """
    Checks environment for data source availability.

    Validates configuration without making actual API calls.
    Provides actionable feedback on what's missing.
    """

    def __init__(self):
        self.checks: List[SourceCheck] = []

    def check_all_sources(self) -> Tuple[bool, List[SourceCheck]]:
        """
        Check all data sources for availability.

        Returns:
            Tuple of (all_required_available, list_of_checks)
        """
        self.checks = []

        # Check each source type
        self._check_websearch()
        self._check_retailer_apis()
        self._check_market_data_apis()
        self._check_economic_data_apis()
        self._check_price_tracking_apis()
        self._check_keyword_research_apis()

        # Determine if all required sources are available
        required_available = all(
            check.status == SourceStatus.AVAILABLE
            for check in self.checks
            if check.priority == "required"
        )

        return required_available, self.checks

    def _check_websearch(self) -> None:
        """Check Claude WebSearch API availability."""
        # WebSearch is built into Claude API - check if we're in Claude environment
        # This would need to be tested at runtime

        check = SourceCheck(
            name="Claude WebSearch API",
            status=SourceStatus.MISSING,
            message="WebSearch API not integrated. This is the primary data source.",
            priority="required",
            setup_instructions=(
                "WebSearch is available through Claude API. Integration requires:\n"
                "1. Use WebSearch tool in Claude Code\n"
                "2. Implement _fetch_*_from_websearch() methods in collectors\n"
                "3. Parse and structure results\n"
                "4. See collectors/*.py for TODO markers"
            )
        )
        self.checks.append(check)

    def _check_retailer_apis(self) -> None:
        """Check retailer API availability."""
        sources = {
            "Amazon Product API": {
                "env_var": "AMAZON_API_KEY",
                "priority": "recommended",
                "instructions": (
                    "Amazon Product Advertising API:\n"
                    "1. Sign up at https://affiliate-program.amazon.com/\n"
                    "2. Get API credentials\n"
                    "3. Set AMAZON_API_KEY environment variable\n"
                    "4. Install boto3: pip install boto3"
                )
            },
            "Home Depot API": {
                "env_var": "HOME_DEPOT_API_KEY",
                "priority": "optional",
                "instructions": (
                    "Home Depot does not have public API.\n"
                    "Alternative: Use web scraping (check ToS) or WebSearch for product data."
                )
            },
            "Walmart API": {
                "env_var": "WALMART_API_KEY",
                "priority": "optional",
                "instructions": (
                    "Walmart Open API:\n"
                    "1. Apply at https://developer.walmart.com/\n"
                    "2. Get API key\n"
                    "3. Set WALMART_API_KEY environment variable"
                )
            }
        }

        for name, config in sources.items():
            env_var = config.get("env_var")
            if env_var and os.getenv(env_var):
                status = SourceStatus.CONFIGURED_BUT_UNTESTED
                message = f"{name} credentials found (not tested)"
            else:
                status = SourceStatus.MISSING
                message = f"{name} credentials not found"

            check = SourceCheck(
                name=name,
                status=status,
                message=message,
                priority=config["priority"],
                setup_instructions=config["instructions"]
            )
            self.checks.append(check)

    def _check_market_data_apis(self) -> None:
        """Check market research API availability."""
        sources = {
            "IBISWorld API": {
                "env_var": "IBISWORLD_API_KEY",
                "priority": "recommended",
                "instructions": (
                    "IBISWorld requires paid subscription ($1,000+/year).\n"
                    "Alternative: Use WebSearch to find publicly available industry reports."
                )
            },
            "SEC EDGAR API": {
                "env_var": None,  # Public API
                "priority": "recommended",
                "instructions": (
                    "SEC EDGAR is public and requires no API key.\n"
                    "Implementation:\n"
                    "1. Use https://www.sec.gov/edgar/sec-api-documentation\n"
                    "2. Follow rate limits (10 requests/second)\n"
                    "3. Parse 10-K filings for company revenue data"
                )
            }
        }

        for name, config in sources.items():
            env_var = config.get("env_var")
            if not env_var:
                # Public API - mark as available but needs implementation
                status = SourceStatus.MISSING
                message = f"{name} is public but not implemented"
            elif os.getenv(env_var):
                status = SourceStatus.CONFIGURED_BUT_UNTESTED
                message = f"{name} credentials found (not tested)"
            else:
                status = SourceStatus.MISSING
                message = f"{name} credentials not found"

            check = SourceCheck(
                name=name,
                status=status,
                message=message,
                priority=config["priority"],
                setup_instructions=config["instructions"]
            )
            self.checks.append(check)

    def _check_economic_data_apis(self) -> None:
        """Check economic data API availability."""
        fred_key = os.getenv("FRED_API_KEY")

        if fred_key:
            status = SourceStatus.CONFIGURED_BUT_UNTESTED
            message = "FRED API key found (not tested)"
        else:
            status = SourceStatus.MISSING
            message = "FRED API key not found"

        check = SourceCheck(
            name="FRED Economic Data API",
            status=status,
            message=message,
            priority="optional",
            setup_instructions=(
                "FRED (Federal Reserve Economic Data) API:\n"
                "1. Sign up at https://fred.stlouisfed.org/docs/api/api_key.html\n"
                "2. Get free API key\n"
                "3. Set FRED_API_KEY environment variable\n"
                "4. Use for economic indicators (consumer spending, housing data)"
            )
        )
        self.checks.append(check)

    def _check_price_tracking_apis(self) -> None:
        """Check price tracking API availability."""
        sources = {
            "CamelCamelCamel API": {
                "env_var": "CAMELCAMELCAMEL_API_KEY",
                "priority": "optional",
                "instructions": (
                    "CamelCamelCamel (Keepa) API:\n"
                    "1. Sign up at https://keepa.com/\n"
                    "2. Subscribe to API access (~$19/month)\n"
                    "3. Set CAMELCAMELCAMEL_API_KEY environment variable\n"
                    "Alternative: Use WebSearch for current pricing data"
                )
            }
        }

        for name, config in sources.items():
            env_var = config.get("env_var")
            if env_var and os.getenv(env_var):
                status = SourceStatus.CONFIGURED_BUT_UNTESTED
                message = f"{name} credentials found (not tested)"
            else:
                status = SourceStatus.MISSING
                message = f"{name} credentials not found"

            check = SourceCheck(
                name=name,
                status=status,
                message=message,
                priority=config["priority"],
                setup_instructions=config["instructions"]
            )
            self.checks.append(check)

    def _check_keyword_research_apis(self) -> None:
        """Check keyword research tool availability."""
        # Google Trends doesn't require API key (pytrends library)
        try:
            import pytrends
            status = SourceStatus.AVAILABLE
            message = "pytrends library installed and ready"
        except ImportError:
            status = SourceStatus.MISSING
            message = "pytrends library not installed"

        check = SourceCheck(
            name="Google Trends (pytrends)",
            status=status,
            message=message,
            priority="optional",
            setup_instructions=(
                "Google Trends via pytrends:\n"
                "1. Install: pip install pytrends\n"
                "2. No API key required\n"
                "3. Implement keyword trending analysis\n"
                "4. Rate limits apply (use with care)"
            )
        )
        self.checks.append(check)

    def generate_readiness_report(self) -> str:
        """
        Generate human-readable readiness report.

        Returns:
            Formatted report string
        """
        required_ready, all_checks = self.check_all_sources()

        lines = []
        lines.append("=" * 80)
        lines.append("DATA SOURCE READINESS CHECK")
        lines.append("=" * 80)
        lines.append("")

        # Summary
        required_sources = [c for c in all_checks if c.priority == "required"]
        required_available = [c for c in required_sources if c.status == SourceStatus.AVAILABLE]

        recommended_sources = [c for c in all_checks if c.priority == "recommended"]
        recommended_available = [c for c in recommended_sources if c.status == SourceStatus.AVAILABLE]

        optional_sources = [c for c in all_checks if c.priority == "optional"]
        optional_available = [c for c in optional_sources if c.status == SourceStatus.AVAILABLE]

        lines.append("📊 SUMMARY")
        lines.append(f"  Required:    {len(required_available)}/{len(required_sources)} available")
        lines.append(f"  Recommended: {len(recommended_available)}/{len(recommended_sources)} available")
        lines.append(f"  Optional:    {len(optional_available)}/{len(optional_sources)} available")
        lines.append("")

        if required_ready:
            lines.append("✅ System is ready for analysis (all required sources available)")
        else:
            lines.append("❌ System is NOT ready (missing required sources)")

        lines.append("")
        lines.append("=" * 80)
        lines.append("")

        # Detailed breakdown by priority
        for priority in ["required", "recommended", "optional"]:
            priority_checks = [c for c in all_checks if c.priority == priority]
            if not priority_checks:
                continue

            lines.append(f"{'🔴 REQUIRED' if priority == 'required' else '🟡 RECOMMENDED' if priority == 'recommended' else '🟢 OPTIONAL'} SOURCES:")
            lines.append("")

            for check in priority_checks:
                status_symbol = {
                    SourceStatus.AVAILABLE: "✅",
                    SourceStatus.CONFIGURED_BUT_UNTESTED: "⚠️",
                    SourceStatus.MISSING: "❌",
                    SourceStatus.ERROR: "🔥"
                }[check.status]

                lines.append(f"{status_symbol} {check.name}")
                lines.append(f"   Status: {check.message}")

                if check.status in [SourceStatus.MISSING, SourceStatus.ERROR]:
                    lines.append(f"   Setup:")
                    for instruction_line in check.setup_instructions.split("\n"):
                        lines.append(f"     {instruction_line}")

                lines.append("")

        lines.append("=" * 80)
        lines.append("NEXT STEPS")
        lines.append("=" * 80)
        lines.append("")

        if not required_ready:
            lines.append("🔴 CRITICAL: Integrate required data sources")
            lines.append("")
            lines.append("The system CANNOT run without required sources. Options:")
            lines.append("")
            lines.append("Option 1: Use Claude WebSearch (recommended)")
            lines.append("  - Available in Claude Code environment")
            lines.append("  - Implement _fetch_*_from_websearch() in collectors")
            lines.append("  - See collectors/*.py for TODO markers")
            lines.append("")
            lines.append("Option 2: Use public APIs")
            lines.append("  - SEC EDGAR (no key required)")
            lines.append("  - Google Trends via pytrends (pip install pytrends)")
            lines.append("")
            lines.append("See DATA_SOURCE_MAPPING.md for full integration guide")
        else:
            lines.append("✅ Required sources available - system ready")
            lines.append("")
            lines.append("Recommended improvements:")
            missing_recommended = [c for c in recommended_sources if c.status == SourceStatus.MISSING]
            for check in missing_recommended:
                lines.append(f"  - Add {check.name}")

        lines.append("")
        lines.append("=" * 80)

        return "\n".join(lines)

    def get_missing_requirements(self) -> Dict[str, List[str]]:
        """
        Get structured list of missing requirements.

        Returns:
            Dict with priority levels and missing sources
        """
        _, all_checks = self.check_all_sources()

        missing = {
            "required": [],
            "recommended": [],
            "optional": []
        }

        for check in all_checks:
            if check.status == SourceStatus.MISSING:
                missing[check.priority].append(check.name)

        return missing


def check_environment() -> Tuple[bool, str]:
    """
    Main entry point for environment checking.

    Returns:
        Tuple of (ready, report_string)
    """
    checker = EnvironmentChecker()
    ready, _ = checker.check_all_sources()
    report = checker.generate_readiness_report()

    return ready, report


if __name__ == "__main__":
    # Allow running as standalone script
    ready, report = check_environment()
    print(report)

    import sys
    sys.exit(0 if ready else 1)
