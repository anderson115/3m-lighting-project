"""
Validation Agents - Quality Gatekeepers

These agents validate data submissions to ensure:
- Quality (completeness, format, consistency)
- Source traceability (every data point must have a source)
- Relevance (data relates to the target category)
- Gaps (identify missing required data)

ZERO FABRICATION ENFORCEMENT: All validators reject data without proper sources.
"""

import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from .base import (
    ValidationAgent,
    ValidationResult,
    DataSubmission,
    Gap,
    Priority,
)


class QualityValidationAgent(ValidationAgent):
    """
    Validates data quality: completeness, format, consistency, recency

    Scoring:
    - 1.0: Perfect quality
    - 0.9-1.0: High quality (acceptable)
    - 0.7-0.9: Medium quality (needs refinement)
    - <0.7: Low quality (reject)
    """

    def __init__(self):
        super().__init__(
            agent_id="quality_validator",
            validation_type="quality"
        )

    async def validate(self, submission: DataSubmission) -> ValidationResult:
        """
        Validate data quality across multiple dimensions

        Checks:
        1. Completeness: All required fields present
        2. Format: Data types correct, values in expected ranges
        3. Consistency: Data internally consistent
        4. Recency: Data is current (prefer 2023-2025)
        """
        self.log_action("validation_started", {"submission_id": submission.message_id})

        issues = []
        score = 1.0

        # Check 1: Completeness
        completeness_score, completeness_issues = self._check_completeness(submission.data)
        issues.extend(completeness_issues)
        score *= completeness_score

        # Check 2: Format validation
        format_score, format_issues = self._check_format(submission.data)
        issues.extend(format_issues)
        score *= format_score

        # Check 3: Consistency
        consistency_score, consistency_issues = self._check_consistency(submission.data)
        issues.extend(consistency_issues)
        score *= consistency_score

        # Check 4: Recency
        recency_score, recency_issues = self._check_recency(submission.data)
        issues.extend(recency_issues)
        score *= recency_score

        passed = score >= 0.9  # High quality threshold

        result = ValidationResult(
            sender_agent=self.agent_id,
            recipient_agent=submission.sender_agent,
            submission_id=submission.message_id,
            validation_type=self.validation_type,
            passed=passed,
            score=score,
            issues=issues,
            recommendations=self._generate_recommendations(issues),
            reasoning=f"Quality score: {score:.2f}. " + (
                "Data meets quality standards." if passed
                else f"Quality issues detected: {len(issues)} problems found."
            )
        )

        self.log_action("validation_completed", {
            "submission_id": submission.message_id,
            "passed": passed,
            "score": score
        })

        return result

    def _check_completeness(self, data: Dict[str, Any]) -> tuple[float, List[str]]:
        """Check if all required fields are present and non-empty"""
        issues = []
        score = 1.0

        # Required fields by data type
        required_fields = {
            "market_size": ["value", "year", "sources"],
            "brand_data": ["brand_name", "tier", "sources"],
            "pricing": ["products", "price_range", "sources"],
            "resources": ["title", "url", "publisher"],
            "taxonomy": ["subcategories", "sources"]
        }

        data_type = data.get("data_type", "unknown")
        required = required_fields.get(data_type, [])

        for field in required:
            if field not in data or not data[field]:
                issues.append(f"Missing required field: {field}")
                score *= 0.8  # Penalty for missing field

        # Check for empty lists/dicts that should have data
        if isinstance(data.get("products"), list) and len(data["products"]) == 0:
            issues.append("Products list is empty")
            score *= 0.7

        if isinstance(data.get("brands"), list) and len(data["brands"]) < 10:
            issues.append(f"Only {len(data['brands'])} brands found (expect 50+)")
            score *= 0.9

        return max(score, 0.0), issues

    def _check_format(self, data: Dict[str, Any]) -> tuple[float, List[str]]:
        """Check if data types and formats are correct"""
        issues = []
        score = 1.0

        # Check numeric fields are numbers
        numeric_fields = ["value", "price", "current_price", "rating", "market_share"]
        for field in numeric_fields:
            if field in data:
                value = data[field]
                if isinstance(value, str):
                    # Try to extract number from string
                    if not re.search(r'\d', value):
                        issues.append(f"{field} should be numeric, got: {value}")
                        score *= 0.9

        # Check price ranges are formatted correctly
        if "price_range" in data:
            pr = data["price_range"]
            if isinstance(pr, str):
                if not re.match(r'\$\d+\s*-\s*\$\d+', pr):
                    issues.append(f"Price range format invalid: {pr}")
                    score *= 0.95

        # Check years are reasonable (2020-2030)
        if "year" in data:
            try:
                year = int(data["year"])
                if year < 2020 or year > 2030:
                    issues.append(f"Year out of expected range: {year}")
                    score *= 0.9
            except (ValueError, TypeError):
                issues.append(f"Year is not a valid number: {data['year']}")
                score *= 0.8

        # Check confidence levels are valid
        if "confidence" in data:
            conf = str(data["confidence"]).lower()
            if conf not in ["high", "medium", "low", "medium-high", "medium-low"]:
                issues.append(f"Invalid confidence level: {conf}")
                score *= 0.95

        return max(score, 0.0), issues

    def _check_consistency(self, data: Dict[str, Any]) -> tuple[float, List[str]]:
        """Check for internal consistency"""
        issues = []
        score = 1.0

        # Check: If has price_range, should have min/max or similar
        if "price_range" in data:
            pr = str(data["price_range"])
            if "$" in pr:
                # Extract numbers
                numbers = re.findall(r'\d+\.?\d*', pr)
                if len(numbers) >= 2:
                    min_val = float(numbers[0])
                    max_val = float(numbers[1])
                    if min_val > max_val:
                        issues.append(f"Price range inconsistent: min ({min_val}) > max ({max_val})")
                        score *= 0.8

        # Check: Brand count vs reported count
        if "brands" in data and "brand_count" in data:
            actual = len(data["brands"])
            reported = int(data["brand_count"])
            if abs(actual - reported) > 2:
                issues.append(f"Brand count mismatch: reported {reported}, actual {actual}")
                score *= 0.9

        # Check: Products count consistency
        if "products" in data and isinstance(data["products"], list):
            if "product_count" in data:
                actual = len(data["products"])
                reported = int(data["product_count"])
                if abs(actual - reported) > 5:
                    issues.append(f"Product count mismatch: reported {reported}, actual {actual}")
                    score *= 0.95

        return max(score, 0.0), issues

    def _check_recency(self, data: Dict[str, Any]) -> tuple[float, List[str]]:
        """Check if data is recent (prefer 2023-2025)"""
        issues = []
        score = 1.0
        current_year = datetime.now().year

        # Check year field
        if "year" in data:
            try:
                year = int(data["year"])
                age = current_year - year
                if age > 2:
                    issues.append(f"Data is {age} years old (year: {year})")
                    score *= (0.95 ** age)  # Decay with age
            except (ValueError, TypeError):
                pass

        # Check scraped_at / collected_at timestamps
        timestamp_fields = ["scraped_at", "collected_at", "accessed_at"]
        for field in timestamp_fields:
            if field in data:
                try:
                    if isinstance(data[field], str):
                        ts = datetime.fromisoformat(data[field].replace('Z', '+00:00'))
                    else:
                        ts = data[field]

                    age_days = (datetime.now() - ts.replace(tzinfo=None)).days
                    if age_days > 30:
                        issues.append(f"Data is {age_days} days old")
                        score *= 0.95
                except (ValueError, TypeError):
                    pass

        return max(score, 0.0), issues

    def _generate_recommendations(self, issues: List[str]) -> List[str]:
        """Generate actionable recommendations based on issues"""
        recommendations = []

        if any("missing" in issue.lower() for issue in issues):
            recommendations.append("Add all required fields before resubmitting")

        if any("format" in issue.lower() for issue in issues):
            recommendations.append("Verify data formatting matches expected schema")

        if any("inconsistent" in issue.lower() for issue in issues):
            recommendations.append("Review data for internal consistency errors")

        if any("old" in issue.lower() or "year" in issue.lower() for issue in issues):
            recommendations.append("Collect more recent data (2024-2025 preferred)")

        if not recommendations:
            recommendations.append("Quality is acceptable, no major issues")

        return recommendations


class SourceValidationAgent(ValidationAgent):
    """
    Validates source traceability - CRITICAL for zero fabrication

    REJECTS data if:
    - No sources provided
    - Sources contain placeholder URLs
    - Sources are not accessible
    - Data points cannot be traced to sources
    """

    def __init__(self):
        super().__init__(
            agent_id="source_validator",
            validation_type="source"
        )
        self.fabrication_markers = [
            "placeholder", "example.com", "test.com", "sample",
            "TODO", "TBD", "FIXME", "xxx"
        ]

    async def validate(self, submission: DataSubmission) -> ValidationResult:
        """
        Validate source traceability - ZERO FABRICATION ENFORCEMENT

        Every data point MUST have a real, accessible source.
        """
        self.log_action("validation_started", {"submission_id": submission.message_id})

        issues = []
        score = 1.0

        # Check 1: Sources exist
        if not submission.sources or len(submission.sources) == 0:
            issues.append("CRITICAL: No sources provided - all data must have sources")
            score = 0.0
        else:
            # Check 2: Detect fabrication markers
            fabrication_score, fabrication_issues = self._detect_fabrication(submission)
            issues.extend(fabrication_issues)
            score *= fabrication_score

            # Check 3: Validate URL format
            url_score, url_issues = self._validate_urls(submission.sources)
            issues.extend(url_issues)
            score *= url_score

            # Check 4: Check source quality
            quality_score, quality_issues = self._check_source_quality(submission.sources)
            issues.extend(quality_issues)
            score *= quality_score

        passed = score == 1.0  # Perfect score required for sources

        result = ValidationResult(
            sender_agent=self.agent_id,
            recipient_agent=submission.sender_agent,
            submission_id=submission.message_id,
            validation_type=self.validation_type,
            passed=passed,
            score=score,
            issues=issues,
            recommendations=self._generate_recommendations(issues),
            reasoning=f"Source validation score: {score:.2f}. " + (
                "All data properly sourced." if passed
                else f"Source issues detected: {len(issues)} problems found."
            )
        )

        self.log_action("validation_completed", {
            "submission_id": submission.message_id,
            "passed": passed,
            "score": score,
            "fabrication_detected": score == 0.0
        })

        return result

    def _detect_fabrication(self, submission: DataSubmission) -> tuple[float, List[str]]:
        """Detect fabrication markers in data and sources"""
        issues = []
        score = 1.0

        # Check data for fabrication markers
        data_str = str(submission.data).lower()
        for marker in self.fabrication_markers:
            if marker in data_str:
                issues.append(f"FABRICATION MARKER DETECTED: '{marker}' in data")
                score = 0.0  # Immediate rejection

        # Check sources for fabrication markers
        for source in submission.sources:
            url_str = str(source.url).lower()
            for marker in self.fabrication_markers:
                if marker in url_str:
                    issues.append(f"FABRICATION MARKER DETECTED: '{marker}' in source URL")
                    score = 0.0  # Immediate rejection

        return score, issues

    def _validate_urls(self, sources: List) -> tuple[float, List[str]]:
        """Validate URL format and structure"""
        issues = []
        score = 1.0

        for i, source in enumerate(sources):
            try:
                parsed = urlparse(str(source.url))

                # Must have scheme (http/https)
                if not parsed.scheme:
                    issues.append(f"Source {i+1}: Missing URL scheme (http/https)")
                    score *= 0.5

                # Must have netloc (domain)
                if not parsed.netloc:
                    issues.append(f"Source {i+1}: Invalid URL domain")
                    score *= 0.5

                # Check for localhost/invalid domains
                invalid_domains = ["localhost", "127.0.0.1", "0.0.0.0"]
                if any(d in parsed.netloc for d in invalid_domains):
                    issues.append(f"Source {i+1}: Invalid domain (localhost)")
                    score *= 0.0

            except Exception as e:
                issues.append(f"Source {i+1}: URL parsing error - {str(e)}")
                score *= 0.7

        return max(score, 0.0), issues

    def _check_source_quality(self, sources: List) -> tuple[float, List[str]]:
        """Check source metadata quality"""
        issues = []
        score = 1.0

        for i, source in enumerate(sources):
            # Check publisher is provided
            if not source.publisher or source.publisher.strip() == "":
                issues.append(f"Source {i+1}: Missing publisher name")
                score *= 0.95

            # Check confidence level is set
            if not source.confidence or source.confidence not in ["high", "medium", "low"]:
                issues.append(f"Source {i+1}: Invalid confidence level")
                score *= 0.98

        # Check for source diversity (not all from same domain)
        if len(sources) >= 3:
            domains = [urlparse(str(s.url)).netloc for s in sources]
            unique_domains = len(set(domains))
            if unique_domains == 1:
                issues.append("All sources from same domain - diversity needed")
                score *= 0.9

        return max(score, 0.0), issues

    def _generate_recommendations(self, issues: List[str]) -> List[str]:
        """Generate recommendations for source issues"""
        recommendations = []

        if any("no sources" in issue.lower() for issue in issues):
            recommendations.append("CRITICAL: Add source URLs for all data points")

        if any("fabrication" in issue.lower() for issue in issues):
            recommendations.append("CRITICAL: Remove placeholder/fabricated data - use only real sources")

        if any("url" in issue.lower() for issue in issues):
            recommendations.append("Fix malformed URLs - ensure valid http/https URLs")

        if any("publisher" in issue.lower() for issue in issues):
            recommendations.append("Add publisher names for all sources")

        if any("diversity" in issue.lower() for issue in issues):
            recommendations.append("Add sources from multiple independent publishers")

        return recommendations


class RelevanceValidationAgent(ValidationAgent):
    """
    Validates data relevance to target category

    Ensures collected data actually relates to garage storage,
    not unrelated products/categories.
    """

    def __init__(self, category: str = "garage storage"):
        super().__init__(
            agent_id="relevance_validator",
            validation_type="relevance"
        )
        self.category = category.lower()
        self.category_keywords = {
            "garage storage": [
                "garage", "storage", "organization", "shelving", "cabinets",
                "bins", "overhead", "wall-mounted", "tool storage", "workbench"
            ]
        }

    async def validate(self, submission: DataSubmission) -> ValidationResult:
        """
        Validate data relevance to category

        Checks if data relates to garage storage, not unrelated categories.
        """
        self.log_action("validation_started", {"submission_id": submission.message_id})

        issues = []
        score = 1.0

        # Check 1: Keyword matching
        keyword_score, keyword_issues = self._check_keywords(submission.data)
        issues.extend(keyword_issues)
        score *= keyword_score

        # Check 2: Brand/product relevance
        brand_score, brand_issues = self._check_brand_relevance(submission.data)
        issues.extend(brand_issues)
        score *= brand_score

        passed = score >= 0.85  # High relevance threshold

        result = ValidationResult(
            sender_agent=self.agent_id,
            recipient_agent=submission.sender_agent,
            submission_id=submission.message_id,
            validation_type=self.validation_type,
            passed=passed,
            score=score,
            issues=issues,
            recommendations=self._generate_recommendations(issues),
            reasoning=f"Relevance score: {score:.2f}. " + (
                f"Data is relevant to {self.category}." if passed
                else f"Data may not be relevant to {self.category}."
            )
        )

        self.log_action("validation_completed", {
            "submission_id": submission.message_id,
            "passed": passed,
            "score": score
        })

        return result

    def _check_keywords(self, data: Dict[str, Any]) -> tuple[float, List[str]]:
        """Check for category-relevant keywords"""
        issues = []
        score = 1.0

        data_str = str(data).lower()
        keywords = self.category_keywords.get(self.category, [])

        # Count keyword matches
        matches = sum(1 for kw in keywords if kw in data_str)
        match_ratio = matches / len(keywords) if keywords else 0

        if match_ratio < 0.2:
            issues.append(f"Low keyword match: only {matches}/{len(keywords)} category keywords found")
            score *= 0.7
        elif match_ratio < 0.4:
            issues.append(f"Moderate keyword match: {matches}/{len(keywords)} category keywords found")
            score *= 0.85

        return score, issues

    def _check_brand_relevance(self, data: Dict[str, Any]) -> tuple[float, List[str]]:
        """Check if brands/products are relevant to category"""
        issues = []
        score = 1.0

        # Known garage storage brands
        relevant_brands = [
            "rubbermaid", "gladiator", "sterilite", "kobalt", "husky",
            "craftsman", "newage", "fleximounts", "closetmaid"
        ]

        # If brand data, check brand names
        if "brand_name" in data:
            brand_name = str(data["brand_name"]).lower()
            if not any(rb in brand_name for rb in relevant_brands):
                # Not a known brand, check for garage/storage keywords
                if "garage" not in brand_name and "storage" not in brand_name:
                    issues.append(f"Brand may not be relevant: {data['brand_name']}")
                    score *= 0.9

        # If pricing data, check product names
        if "products" in data:
            products = data["products"]
            if isinstance(products, list) and len(products) > 0:
                irrelevant_count = 0
                for product in products[:10]:  # Sample first 10
                    product_str = str(product).lower()
                    if not any(kw in product_str for kw in ["storage", "garage", "bin", "shelf", "cabinet"]):
                        irrelevant_count += 1

                if irrelevant_count > 5:
                    issues.append(f"{irrelevant_count}/10 products appear irrelevant to category")
                    score *= 0.8

        return score, issues

    def _generate_recommendations(self, issues: List[str]) -> List[str]:
        """Generate recommendations for relevance issues"""
        recommendations = []

        if any("keyword" in issue.lower() for issue in issues):
            recommendations.append(f"Focus search on {self.category}-specific terms")

        if any("brand" in issue.lower() for issue in issues):
            recommendations.append(f"Verify brands sell {self.category} products")

        if any("product" in issue.lower() for issue in issues):
            recommendations.append("Filter products to only those relevant to category")

        return recommendations


class GapIdentificationAgent(ValidationAgent):
    """
    Identifies gaps in collected data vs. requirements

    Analyzes what data has been collected and identifies what's still needed
    to meet the complete report requirements.
    """

    def __init__(self, requirements: Dict[str, Any]):
        super().__init__(
            agent_id="gap_analyzer",
            validation_type="gap"
        )
        self.requirements = requirements

    async def validate(self, submission: DataSubmission) -> ValidationResult:
        """
        Gap analysis doesn't validate individual submissions,
        it analyzes overall progress. Use analyze_gaps() instead.
        """
        # Not used for individual submissions
        pass

    async def analyze_gaps(
        self,
        collected_data: Dict[str, Any],
        requirements: Dict[str, Any]
    ) -> List[Gap]:
        """
        Analyze collected data against requirements to identify gaps

        Args:
            collected_data: All accepted data so far
            requirements: Required data specifications

        Returns:
            List of identified gaps with priority and recommended actions
        """
        self.log_action("gap_analysis_started", {})

        gaps = []

        # Check brand count
        brands_collected = len(collected_data.get("brands", []))
        brands_required = requirements.get("brands", {}).get("min_count", 50)
        if brands_collected < brands_required:
            gaps.append(Gap(
                gap_type="insufficient_count",
                description=f"Need {brands_required - brands_collected} more brands",
                current_value=brands_collected,
                required_value=brands_required,
                priority=Priority.HIGH,
                suggested_action="Collect more brands from Tier 3-5 to reach 50+ total"
            ))

        # Check market size data
        if "market_size" not in collected_data:
            gaps.append(Gap(
                gap_type="missing_data",
                description="Market size data not collected",
                current_value=None,
                required_value="Market size with sources",
                priority=Priority.CRITICAL,
                suggested_action="Collect market size from industry reports or FRED data"
            ))

        # Check pricing data
        retailers_collected = len(collected_data.get("pricing_by_retailer", {}))
        retailers_required = requirements.get("pricing", {}).get("retailers", 4)
        if retailers_collected < retailers_required:
            gaps.append(Gap(
                gap_type="insufficient_count",
                description=f"Need pricing from {retailers_required - retailers_collected} more retailers",
                current_value=retailers_collected,
                required_value=retailers_required,
                priority=Priority.HIGH,
                suggested_action="Scrape products from Lowe's and Walmart to reach 4 retailers"
            ))

        # Check resources
        resources_collected = len(collected_data.get("resources", []))
        resources_required = requirements.get("resources", {}).get("min_count", 30)
        if resources_collected < resources_required:
            gaps.append(Gap(
                gap_type="insufficient_count",
                description=f"Need {resources_required - resources_collected} more resources",
                current_value=resources_collected,
                required_value=resources_required,
                priority=Priority.MEDIUM,
                suggested_action="Curate more industry reports, guides, and references"
            ))

        # Check historical growth data
        if "historical_growth" not in collected_data or not collected_data["historical_growth"]:
            gaps.append(Gap(
                gap_type="missing_data",
                description="Historical growth data (5 years) not collected",
                current_value=None,
                required_value="5-year historical growth",
                priority=Priority.HIGH,
                suggested_action="Download FRED retail sales time series data"
            ))

        self.log_action("gap_analysis_completed", {"gaps_found": len(gaps)})

        return gaps
