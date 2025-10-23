"""
Unit tests for HTMLReporter
Tests the refactored Jinja2-based HTML report generator
"""

import pytest
from pathlib import Path
from generators.html_reporter import HTMLReporter


@pytest.mark.unit
@pytest.mark.generator
class TestHTMLReporter:
    """Test HTMLReporter class"""

    def test_initialization(self, test_config):
        """Test reporter initializes correctly"""
        reporter = HTMLReporter(test_config)

        assert reporter.config == test_config
        assert reporter.templates_dir.exists()
        assert reporter.env is not None

    def test_templates_directory_exists(self, test_config):
        """Test templates directory is created and accessible"""
        reporter = HTMLReporter(test_config)
        templates_dir = reporter.templates_dir

        assert templates_dir.exists()
        assert templates_dir.is_dir()

    def test_all_templates_exist(self, test_config):
        """Test all required templates are present"""
        reporter = HTMLReporter(test_config)

        required_templates = [
            "base.html.j2",
            "report.html.j2",
            "executive_summary.html.j2",
            "brands_section.html.j2",
            "taxonomy_section.html.j2",
            "pricing_section.html.j2",
            "market_section.html.j2",
            "resources_section.html.j2"
        ]

        for template_name in required_templates:
            template_path = reporter.templates_dir / template_name
            assert template_path.exists(), f"Missing template: {template_name}"

    def test_generate_report(self, test_config, sample_full_analysis_data):
        """Test report generation with complete data"""
        reporter = HTMLReporter(test_config)

        output_path = reporter.generate_report(
            category_name="Test Category",
            output_name="test_report",
            data=sample_full_analysis_data
        )

        assert output_path.exists()
        assert output_path.suffix == ".html"
        assert output_path.stat().st_size > 0

    def test_generated_report_is_valid_html(self, test_config, sample_full_analysis_data):
        """Test generated report contains valid HTML"""
        reporter = HTMLReporter(test_config)

        output_path = reporter.generate_report(
            category_name="Test Category",
            output_name="test_html_validation",
            data=sample_full_analysis_data
        )

        content = output_path.read_text()

        assert content.startswith("<!DOCTYPE html>")
        assert "<html" in content
        assert "</html>" in content
        assert "<head>" in content
        assert "<body>" in content

    def test_report_contains_category_name(self, test_config, sample_full_analysis_data):
        """Test report includes the category name"""
        reporter = HTMLReporter(test_config)
        category_name = "Smart Home Lighting"

        output_path = reporter.generate_report(
            category_name=category_name,
            output_name="test_category_name",
            data=sample_full_analysis_data
        )

        content = output_path.read_text()
        assert "Smart Home Lighting" in content

    def test_build_context(self, test_config, sample_full_analysis_data):
        """Test context building from analysis data"""
        reporter = HTMLReporter(test_config)

        context = reporter._build_context("Test Category", sample_full_analysis_data)

        # Check required context keys
        assert "category_name" in context
        assert "generation_date" in context
        assert "brands" in context
        assert "market_size_value" in context

    def test_prepare_executive_summary(self, test_config, sample_full_analysis_data):
        """Test executive summary context preparation"""
        reporter = HTMLReporter(test_config)

        exec_summary = reporter._prepare_executive_summary(sample_full_analysis_data)

        assert "market_size_value" in exec_summary
        assert "brands_count" in exec_summary
        assert "subcategories_count" in exec_summary

    def test_prepare_brands_context(self, test_config, sample_full_analysis_data):
        """Test brands section context preparation"""
        reporter = HTMLReporter(test_config)

        brands_context = reporter._prepare_brands_context(sample_full_analysis_data)

        assert "brands" in brands_context
        assert "brands_count" in brands_context
        assert isinstance(brands_context["brands"], list)

    def test_prepare_taxonomy_context(self, test_config, sample_full_analysis_data):
        """Test taxonomy section context preparation"""
        reporter = HTMLReporter(test_config)

        taxonomy_context = reporter._prepare_taxonomy_context(sample_full_analysis_data)

        assert "subcategories" in taxonomy_context
        assert "subcategories_count" in taxonomy_context

    def test_prepare_pricing_context(self, test_config, sample_full_analysis_data):
        """Test pricing section context preparation"""
        reporter = HTMLReporter(test_config)

        pricing_context = reporter._prepare_pricing_context(sample_full_analysis_data)

        assert "overall_price_range" in pricing_context
        assert "pricing_subcategories" in pricing_context

    def test_prepare_market_context(self, test_config, sample_full_analysis_data):
        """Test market section context preparation"""
        reporter = HTMLReporter(test_config)

        market_context = reporter._prepare_market_context(sample_full_analysis_data)

        assert "current_size_value" in market_context
        assert "historical" in market_context
        assert "projections" in market_context

    def test_prepare_resources_context(self, test_config, sample_full_analysis_data):
        """Test resources section context preparation"""
        reporter = HTMLReporter(test_config)

        resources_context = reporter._prepare_resources_context(sample_full_analysis_data)

        assert "total_resources" in resources_context
        assert "resource_categories" in resources_context

    def test_merge_brand_data(self, test_config):
        """Test brand and market share data merging"""
        reporter = HTMLReporter(test_config)

        brands = [
            {"name": "Philips Hue", "tier": "tier_1_national"},
            {"name": "LIFX", "tier": "tier_3_specialist"}
        ]

        market_shares = [
            {"brand": "Philips Hue", "estimated_market_share": "35%", "position": "#1"}
        ]

        merged = reporter._merge_brand_data(brands, market_shares)

        assert len(merged) == 2
        assert merged[0]["name"] == "Philips Hue"
        assert "market_share" in merged[0]

    def test_sort_brands(self, test_config):
        """Test brand sorting by tier and market share"""
        reporter = HTMLReporter(test_config)

        brands = [
            {"name": "Import Brand", "tier": "tier_5_import", "market_share": "5%"},
            {"name": "National Brand", "tier": "tier_1_national", "market_share": "30%"},
            {"name": "Specialist", "tier": "tier_3_specialist", "market_share": "10%"}
        ]

        sorted_brands = reporter._sort_brands(brands)

        # Tier 1 should come first
        assert sorted_brands[0]["tier"] == "tier_1_national"
        # Tier 5 should come last
        assert sorted_brands[-1]["tier"] == "tier_5_import"

    def test_parse_share(self, test_config):
        """Test market share percentage parsing"""
        reporter = HTMLReporter(test_config)

        assert reporter._parse_share("35%") == 35.0
        assert reporter._parse_share("8.5%") == 8.0
        assert reporter._parse_share("N/A") == 0.0
        assert reporter._parse_share("—") == 0.0

    def test_report_with_minimal_data(self, test_config):
        """Test report generation with minimal data structure"""
        reporter = HTMLReporter(test_config)

        minimal_data = {
            "brands": {"brands": []},
            "taxonomy": {"subcategories": [], "category_keywords": {}},
            "pricing": {"subcategory_pricing": [], "category_price_dynamics": {}},
            "market_size": {"current_size": {}, "historical_growth": [], "projections": []},
            "market_share": {"market_shares": [], "competitive_landscape": {}, "market_structure": {}},
            "resources": {"total_resources": 0, "resource_categories": []}
        }

        output_path = reporter.generate_report(
            category_name="Minimal Test",
            output_name="test_minimal",
            data=minimal_data
        )

        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_output_filename_format(self, test_config, sample_full_analysis_data):
        """Test output filename follows expected format"""
        reporter = HTMLReporter(test_config)

        output_name = "custom_name"
        output_path = reporter.generate_report(
            category_name="Test",
            output_name=output_name,
            data=sample_full_analysis_data
        )

        expected_filename = f"{output_name}_Category_Intelligence.html"
        assert output_path.name == expected_filename
