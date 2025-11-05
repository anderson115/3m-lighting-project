"""
Data Validator - Quality Assurance for Collected Data

Validates data from any source to ensure quality and completeness.
Works with real data when sources are integrated.
"""

import logging
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class ValidationSeverity(str, Enum):
    """Validation issue severity"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationIssue:
    """Single validation issue"""
    severity: ValidationSeverity
    field: str
    message: str
    value: Any = None


class DataValidator:
    """
    Validates data quality from any source.

    Ensures collected data meets minimum standards:
    - Required fields present
    - Data types correct
    - Values within reasonable ranges
    - No fabrication markers
    - Source URLs present and valid
    """

    # Fabrication markers to detect
    FABRICATION_MARKERS = [
        'placeholder', 'example.com', 'test.com', 'sample',
        'TODO', 'TBD', 'FIXME', 'xxx', 'dummy', 'fake',
        'mock', 'stub', 'hardcoded', 'fabricated', 'lorem ipsum'
    ]

    def validate_brand_data(self, data: Dict[str, Any]) -> Tuple[bool, List[ValidationIssue]]:
        """
        Validate brand discovery data.

        Args:
            data: Brand discovery result dict

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues: List[ValidationIssue] = []

        # Check required fields
        if not data.get("brands"):
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                field="brands",
                message="No brands data found"
            ))
            return False, issues

        # Validate each brand
        for i, brand in enumerate(data.get("brands", [])):
            brand_issues = self._validate_brand(brand, index=i)
            issues.extend(brand_issues)

        # Check minimum brand count
        brand_count = len(data.get("brands", []))
        if brand_count < 10:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                field="brands",
                message=f"Only {brand_count} brands found (recommended: 50+)",
                value=brand_count
            ))

        # Check for fabrication markers
        fab_issues = self._check_fabrication_markers(data, "brands")
        issues.extend(fab_issues)

        # Determine validity (no ERROR severity issues)
        is_valid = not any(i.severity == ValidationSeverity.ERROR for i in issues)

        return is_valid, issues

    def _validate_brand(self, brand: Dict[str, Any], index: int) -> List[ValidationIssue]:
        """Validate single brand entry."""
        issues: List[ValidationIssue] = []

        # Required fields
        required = ["name", "tier"]
        for field in required:
            if not brand.get(field):
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    field=f"brands[{index}].{field}",
                    message=f"Missing required field: {field}"
                ))

        # Source URLs required for zero fabrication
        if not brand.get("source_urls") or len(brand.get("source_urls", [])) == 0:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                field=f"brands[{index}].source_urls",
                message=f"Brand '{brand.get('name')}' has no source URLs (zero fabrication policy violation)"
            ))

        # Validate tier value
        valid_tiers = ["tier_1_national", "tier_2_private_label", "tier_3_specialist", "tier_4_emerging", "tier_5_import"]
        if brand.get("tier") and brand["tier"] not in valid_tiers:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                field=f"brands[{index}].tier",
                message=f"Unknown tier value: {brand['tier']}",
                value=brand["tier"]
            ))

        return issues

    def validate_pricing_data(self, data: Dict[str, Any]) -> Tuple[bool, List[ValidationIssue]]:
        """
        Validate pricing analysis data.

        Args:
            data: Pricing analysis result dict

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues: List[ValidationIssue] = []

        # Check required fields
        if not data.get("subcategory_pricing"):
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                field="subcategory_pricing",
                message="No subcategory pricing data found"
            ))
            return False, issues

        # Validate each subcategory
        for i, subcat in enumerate(data.get("subcategory_pricing", [])):
            subcat_issues = self._validate_pricing_subcategory(subcat, index=i)
            issues.extend(subcat_issues)

        # Check for fabrication markers
        fab_issues = self._check_fabrication_markers(data, "pricing")
        issues.extend(fab_issues)

        # Determine validity
        is_valid = not any(i.severity == ValidationSeverity.ERROR for i in issues)

        return is_valid, issues

    def _validate_pricing_subcategory(self, subcat: Dict[str, Any], index: int) -> List[ValidationIssue]:
        """Validate single pricing subcategory."""
        issues: List[ValidationIssue] = []

        # Required fields
        required = ["name", "price_analysis"]
        for field in required:
            if not subcat.get(field):
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    field=f"subcategory_pricing[{index}].{field}",
                    message=f"Missing required field: {field}"
                ))

        # Source URLs required
        if not subcat.get("source_urls") or len(subcat.get("source_urls", [])) == 0:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                field=f"subcategory_pricing[{index}].source_urls",
                message=f"Subcategory '{subcat.get('name')}' has no source URLs"
            ))

        # Validate price ranges (basic format check)
        price_analysis = subcat.get("price_analysis", {})
        if price_analysis.get("overall_price_range"):
            if not self._is_valid_price_range(price_analysis["overall_price_range"]):
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    field=f"subcategory_pricing[{index}].price_analysis.overall_price_range",
                    message=f"Invalid price range format: {price_analysis['overall_price_range']}",
                    value=price_analysis["overall_price_range"]
                ))

        return issues

    def validate_market_data(self, data: Dict[str, Any]) -> Tuple[bool, List[ValidationIssue]]:
        """
        Validate market research data.

        Args:
            data: Market research result dict

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues: List[ValidationIssue] = []

        # Check for market shares or market size data
        has_shares = data.get("market_shares") is not None
        has_size = data.get("current_size") is not None

        if not has_shares and not has_size:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                field="market_data",
                message="No market share or market size data found"
            ))
            return False, issues

        # Validate market share data if present
        if has_shares:
            for i, share in enumerate(data.get("market_shares", [])):
                if not share.get("source_urls") or len(share.get("source_urls", [])) == 0:
                    issues.append(ValidationIssue(
                        severity=ValidationSeverity.WARNING,
                        field=f"market_shares[{i}].source_urls",
                        message=f"Market share entry has no source URLs"
                    ))

        # Check for fabrication markers
        fab_issues = self._check_fabrication_markers(data, "market")
        issues.extend(fab_issues)

        # Determine validity
        is_valid = not any(i.severity == ValidationSeverity.ERROR for i in issues)

        return is_valid, issues

    def _is_valid_price_range(self, price_range: str) -> bool:
        """Check if price range string is in valid format."""
        # Expect format like "$100 - $500" or "$1.2M - $1.5M"
        pattern = r'\$[\d,]+\.?\d*[KMB]?\s*-\s*\$[\d,]+\.?\d*[KMB]?'
        return bool(re.match(pattern, price_range, re.IGNORECASE))

    def _check_fabrication_markers(
        self,
        data: Any,
        context: str
    ) -> List[ValidationIssue]:
        """
        Check data for fabrication markers.

        Args:
            data: Data to check (dict, list, or string)
            context: Context for error messages

        Returns:
            List of validation issues found
        """
        issues: List[ValidationIssue] = []

        # Convert data to string for searching
        data_str = str(data).lower()

        # Check for each marker
        for marker in self.FABRICATION_MARKERS:
            if marker.lower() in data_str:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    field=context,
                    message=f"Fabrication marker detected: '{marker}' (ZERO FABRICATION POLICY VIOLATION)",
                    value=marker
                ))

        return issues

    def validate_all_collected_data(self, results: Dict[str, Any]) -> Tuple[bool, Dict[str, List[ValidationIssue]]]:
        """
        Validate all collected data from analysis run.

        Args:
            results: Complete results dict from orchestrator

        Returns:
            Tuple of (all_valid, dict_of_issues_by_stage)
        """
        all_issues: Dict[str, List[ValidationIssue]] = {}

        # Validate brands
        if results.get("brands"):
            valid, issues = self.validate_brand_data(results["brands"])
            if issues:
                all_issues["brands"] = issues

        # Validate pricing
        if results.get("pricing"):
            valid, issues = self.validate_pricing_data(results["pricing"])
            if issues:
                all_issues["pricing"] = issues

        # Validate market share
        if results.get("market_share"):
            valid, issues = self.validate_market_data(results["market_share"])
            if issues:
                all_issues["market_share"] = issues

        # Validate market size
        if results.get("market_size"):
            valid, issues = self.validate_market_data(results["market_size"])
            if issues:
                all_issues["market_size"] = issues

        # Check if any ERROR severity issues exist
        all_valid = not any(
            any(issue.severity == ValidationSeverity.ERROR for issue in issues)
            for issues in all_issues.values()
        )

        return all_valid, all_issues

    def generate_validation_report(
        self,
        all_issues: Dict[str, List[ValidationIssue]]
    ) -> str:
        """
        Generate human-readable validation report.

        Args:
            all_issues: Dict of issues by stage

        Returns:
            Formatted report string
        """
        lines = []
        lines.append("=" * 80)
        lines.append("DATA VALIDATION REPORT")
        lines.append("=" * 80)
        lines.append("")

        # Count issues by severity
        total_errors = sum(
            sum(1 for issue in issues if issue.severity == ValidationSeverity.ERROR)
            for issues in all_issues.values()
        )
        total_warnings = sum(
            sum(1 for issue in issues if issue.severity == ValidationSeverity.WARNING)
            for issues in all_issues.values()
        )

        lines.append(f"Errors:   {total_errors}")
        lines.append(f"Warnings: {total_warnings}")
        lines.append("")

        if total_errors == 0 and total_warnings == 0:
            lines.append("✅ All validation checks passed")
        else:
            for stage, issues in all_issues.items():
                lines.append(f"📊 {stage.upper()}")
                lines.append("-" * 80)

                for issue in issues:
                    symbol = "🔴" if issue.severity == ValidationSeverity.ERROR else "⚠️" if issue.severity == ValidationSeverity.WARNING else "ℹ️"
                    lines.append(f"{symbol} {issue.field}: {issue.message}")
                    if issue.value is not None:
                        lines.append(f"   Value: {issue.value}")

                lines.append("")

        lines.append("=" * 80)

        return "\n".join(lines)


# Convenience function
def validate_data(data: Dict[str, Any], data_type: str) -> Tuple[bool, List[ValidationIssue]]:
    """
    Validate data of specific type.

    Args:
        data: Data to validate
        data_type: Type of data ("brand", "pricing", "market")

    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    validator = DataValidator()

    if data_type == "brand":
        return validator.validate_brand_data(data)
    elif data_type == "pricing":
        return validator.validate_pricing_data(data)
    elif data_type == "market":
        return validator.validate_market_data(data)
    else:
        raise ValueError(f"Unknown data type: {data_type}")
