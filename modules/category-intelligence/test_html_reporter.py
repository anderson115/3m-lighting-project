#!/usr/bin/env python3
"""
Test script for refactored HTML Reporter
Tests Jinja2 template rendering with sample data
"""

import sys
from pathlib import Path
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple config class for testing
class SimpleConfig:
    def __init__(self):
        self.module_dir = Path(__file__).parent
        self.outputs_dir = self.module_dir / "outputs" / "deliverables"
        self.outputs_dir.mkdir(exist_ok=True, parents=True)
        self.current_date = datetime.now().strftime("%Y-%m-%d")


def create_test_data():
    """Create minimal test data structure"""
    return {
        "brands": {
            "brands": [
                {
                    "name": "Philips Hue",
                    "tier": "tier_1_national",
                    "estimated_market_share": "35%",
                    "estimated_category_revenue": "$450M",
                    "position": "#1",
                    "confidence": "high"
                },
                {
                    "name": "LIFX",
                    "tier": "tier_3_specialist",
                    "estimated_market_share": "8%",
                    "estimated_category_revenue": "$95M",
                    "position": "#4",
                    "confidence": "medium"
                }
            ]
        },
        "market_share": {
            "market_shares": [
                {
                    "brand": "Philips Hue",
                    "estimated_market_share": "35%",
                    "position": "#1"
                },
                {
                    "brand": "LIFX",
                    "estimated_market_share": "8%",
                    "position": "#4"
                }
            ],
            "competitive_landscape": {
                "key_competitive_factors": [
                    "Smart home integration",
                    "Color accuracy",
                    "App ecosystem"
                ],
                "emerging_threats": [
                    "Budget LED brands",
                    "Matter protocol adoption"
                ]
            },
            "market_structure": {
                "concentration_ratio": {
                    "cr4": "68%"
                }
            }
        },
        "taxonomy": {
            "subcategories": [
                {
                    "name": "Smart Bulbs",
                    "subcategory_market_size_usd": "$850M",
                    "market_share_of_category": "45%",
                    "estimated_units_sold_annually": "12M units",
                    "number_of_active_brands": "50+",
                    "average_price_point": "$35",
                    "growth_rate_yoy": "12%",
                    "consumer_keywords": ["smart bulb", "wifi bulb", "alexa lights"]
                },
                {
                    "name": "LED Strips",
                    "subcategory_market_size_usd": "$320M",
                    "market_share_of_category": "18%",
                    "estimated_units_sold_annually": "8M units",
                    "number_of_active_brands": "40+",
                    "average_price_point": "$28",
                    "growth_rate_yoy": "18%",
                    "consumer_keywords": ["led strip", "rgb strip", "flexible lighting"]
                }
            ],
            "category_keywords": {
                "consumer_language": ["smart lights", "wifi bulbs", "color changing"],
                "industry_language": ["connected lighting", "IoT illumination", "smart home integration"]
            }
        },
        "pricing": {
            "subcategory_pricing": [
                {
                    "name": "Smart Bulbs",
                    "top_brands": [
                        {"brand": "Philips Hue", "price_range": "$40-$60"},
                        {"brand": "LIFX", "price_range": "$35-$55"}
                    ],
                    "product_pricing": [
                        {
                            "product_type": "A19 Color Bulb",
                            "typical_price_range": "$40-$60",
                            "average_price": "$48",
                            "units_sold_annually": "5M",
                            "top_brands": [
                                {"brand": "Philips Hue"},
                                {"brand": "LIFX"}
                            ]
                        }
                    ]
                }
            ],
            "category_price_dynamics": {
                "overall_category_price_range": "$15-$250",
                "category_average_transaction_value": "$65",
                "dominant_retailers": ["Amazon", "Home Depot", "Best Buy"]
            }
        },
        "market_size": {
            "current_size": {
                "value_usd": "$1.85B",
                "value_midpoint": "$1.85B",
                "year": 2024,
                "geographic_scope": "United States"
            },
            "historical_growth": [
                {"year": 2020, "market_size_usd": "$1.2B", "yoy_growth": "—"},
                {"year": 2021, "market_size_usd": "$1.35B", "yoy_growth": "12.5%"},
                {"year": 2022, "market_size_usd": "$1.55B", "yoy_growth": "14.8%"},
                {"year": 2023, "market_size_usd": "$1.68B", "yoy_growth": "8.4%"}
            ],
            "projections": [
                {"year": 2025, "projected_value": "$2.1B", "growth_rate": "13.5%", "confidence": "high"},
                {"year": 2026, "projected_value": "$2.4B", "growth_rate": "14.3%", "confidence": "medium"}
            ],
            "growth_drivers": [
                {
                    "driver": "Smart home adoption",
                    "impact": "high",
                    "description": "Increasing consumer adoption of smart home ecosystems driving demand"
                }
            ],
            "growth_inhibitors": [
                {
                    "inhibitor": "High entry price",
                    "impact": "medium",
                    "description": "Premium pricing limiting mass market penetration"
                }
            ]
        },
        "resources": {
            "total_resources": 15,
            "resource_categories": [
                {
                    "category": "Market Research Reports",
                    "resources": [
                        {
                            "title": "Smart Lighting Market Analysis 2024",
                            "provider": "Allied Market Research",
                            "url": "https://example.com/report",
                            "relevance": "High - comprehensive market data"
                        }
                    ]
                }
            ]
        }
    }


def main():
    logger.info("="*60)
    logger.info("HTML REPORTER REFACTORING TEST")
    logger.info("="*60)

    # Import HTMLReporter here to avoid import issues
    sys.path.insert(0, str(Path(__file__).parent))
    from generators.html_reporter import HTMLReporter

    # Initialize reporter with simple config
    logger.info("\n1. Initializing HTML Reporter...")
    test_config = SimpleConfig()
    reporter = HTMLReporter(test_config)
    logger.info(f"   ✅ Reporter initialized")
    logger.info(f"   Templates directory: {reporter.templates_dir}")

    # Check templates exist
    logger.info("\n2. Checking templates...")
    template_files = [
        "base.html.j2",
        "report.html.j2",
        "executive_summary.html.j2",
        "brands_section.html.j2",
        "taxonomy_section.html.j2",
        "pricing_section.html.j2",
        "market_section.html.j2",
        "resources_section.html.j2"
    ]

    all_exist = True
    for template_file in template_files:
        template_path = reporter.templates_dir / template_file
        exists = template_path.exists()
        status = "✅" if exists else "❌"
        logger.info(f"   {status} {template_file}")
        if not exists:
            all_exist = False

    if not all_exist:
        logger.error("\n❌ Missing templates - test cannot proceed")
        return 1

    # Create test data
    logger.info("\n3. Creating test data...")
    test_data = create_test_data()
    logger.info(f"   ✅ Test data created")
    logger.info(f"   - {len(test_data['brands']['brands'])} brands")
    logger.info(f"   - {len(test_data['taxonomy']['subcategories'])} subcategories")

    # Generate report
    logger.info("\n4. Generating HTML report...")
    try:
        output_path = reporter.generate_report(
            category_name="Smart Home Lighting",
            output_name="Test_Report",
            data=test_data
        )
        logger.info(f"   ✅ Report generated successfully")
        logger.info(f"   Output: {output_path}")
        logger.info(f"   Size: {output_path.stat().st_size / 1024:.1f} KB")

        # Verify file exists and has content
        if output_path.exists() and output_path.stat().st_size > 0:
            logger.info("\n5. Verification...")
            logger.info(f"   ✅ File exists and has content")

            # Read first few lines to verify HTML structure
            with open(output_path, 'r') as f:
                first_line = f.readline().strip()
                if first_line.startswith('<!DOCTYPE html>'):
                    logger.info(f"   ✅ Valid HTML document")
                else:
                    logger.warning(f"   ⚠️  Unexpected first line: {first_line}")

            logger.info("\n" + "="*60)
            logger.info("✅ ALL TESTS PASSED")
            logger.info("="*60)
            logger.info("\nRefactored HTML Reporter is working correctly!")
            logger.info(f"View report: open {output_path}")
            return 0
        else:
            logger.error("\n❌ Output file is empty or missing")
            return 1

    except Exception as e:
        logger.error(f"\n❌ Report generation failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
