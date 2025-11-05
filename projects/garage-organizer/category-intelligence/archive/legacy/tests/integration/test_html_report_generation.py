"""
Integration test for HTML report generation
Tests end-to-end report generation workflow
"""

import pytest
from pathlib import Path
from generators.html_reporter import HTMLReporter


@pytest.mark.integration
class TestHTMLReportGeneration:
    """Integration tests for complete report generation"""

    def test_generate_complete_report(self, test_config, sample_full_analysis_data):
        """Test generating a complete report with all sections"""
        reporter = HTMLReporter(test_config)

        output_path = reporter.generate_report(
            category_name="Smart Home Lighting",
            output_name="integration_test",
            data=sample_full_analysis_data
        )

        # Verify file exists and has reasonable size
        assert output_path.exists()
        assert output_path.stat().st_size > 10000  # Should be > 10KB

        # Verify HTML structure
        content = output_path.read_text()

        # Check document structure
        assert "<!DOCTYPE html>" in content
        assert "<html" in content
        assert "</html>" in content

        # Check all sections are present
        assert "Executive Summary" in content
        assert "Brand Landscape" in content
        assert "Category Structure" in content
        assert "Pricing Analysis" in content
        assert "Market Size" in content
        assert "Key Resources" in content

        # Check data is populated
        assert "Philips Hue" in content  # Sample brand
        assert "Smart Bulbs" in content  # Sample subcategory
        assert "$1.85B" in content  # Sample market size

    def test_report_with_empty_sections(self, test_config):
        """Test report generation handles empty sections gracefully"""
        reporter = HTMLReporter(test_config)

        empty_data = {
            "brands": {"brands": []},
            "taxonomy": {"subcategories": [], "category_keywords": {}},
            "pricing": {"subcategory_pricing": [], "category_price_dynamics": {}},
            "market_size": {"current_size": {}, "historical_growth": [], "projections": []},
            "market_share": {"market_shares": [], "competitive_landscape": {}, "market_structure": {}},
            "resources": {"total_resources": 0, "resource_categories": []}
        }

        output_path = reporter.generate_report(
            category_name="Empty Test",
            output_name="integration_empty",
            data=empty_data
        )

        assert output_path.exists()
        content = output_path.read_text()

        # Should still have valid HTML structure
        assert "<!DOCTYPE html>" in content
        assert "Empty Test" in content

    def test_multiple_reports_in_sequence(self, test_config, sample_full_analysis_data):
        """Test generating multiple reports sequentially"""
        reporter = HTMLReporter(test_config)

        reports = []
        for i in range(3):
            output_path = reporter.generate_report(
                category_name=f"Test Category {i}",
                output_name=f"integration_multi_{i}",
                data=sample_full_analysis_data
            )
            reports.append(output_path)
            assert output_path.exists()

        # All reports should exist
        for report_path in reports:
            assert report_path.exists()
            assert report_path.stat().st_size > 0

    def test_report_output_directory(self, test_config, sample_full_analysis_data):
        """Test reports are created in correct output directory"""
        reporter = HTMLReporter(test_config)

        output_path = reporter.generate_report(
            category_name="Directory Test",
            output_name="integration_directory",
            data=sample_full_analysis_data
        )

        # Verify file is in expected directory
        assert output_path.parent == test_config.outputs_dir
        assert output_path.name == "integration_directory_Category_Intelligence.html"

    def test_template_inheritance(self, test_config, sample_full_analysis_data):
        """Test that template inheritance works correctly"""
        reporter = HTMLReporter(test_config)

        output_path = reporter.generate_report(
            category_name="Template Test",
            output_name="integration_templates",
            data=sample_full_analysis_data
        )

        content = output_path.read_text()

        # Check that base template CSS is included
        assert "<style>" in content
        assert "font-family:" in content
        assert "body {" in content

        # Check that content sections are included
        assert "Executive Summary" in content
        assert "Brand Landscape" in content
