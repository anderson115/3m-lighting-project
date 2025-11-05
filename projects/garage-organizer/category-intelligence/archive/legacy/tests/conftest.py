"""
Pytest Configuration and Fixtures
Shared fixtures for all tests
"""

import pytest
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


@pytest.fixture
def test_config():
    """Provide test configuration"""
    class TestConfig:
        def __init__(self):
            self.module_dir = Path(__file__).parent.parent
            self.outputs_dir = self.module_dir / "outputs" / "test"
            self.outputs_dir.mkdir(exist_ok=True, parents=True)
            self.current_date = datetime.now().strftime("%Y-%m-%d")

            # Test-specific settings
            self.max_brands_to_discover = 5
            self.max_products_per_subcategory = 10
            self.max_search_results_per_query = 5

    return TestConfig()


@pytest.fixture
def sample_brand_data() -> Dict[str, Any]:
    """Sample brand data for testing"""
    return {
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
    }


@pytest.fixture
def sample_taxonomy_data() -> Dict[str, Any]:
    """Sample taxonomy data for testing"""
    return {
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
            }
        ],
        "category_keywords": {
            "consumer_language": ["smart lights", "wifi bulbs"],
            "industry_language": ["connected lighting", "IoT illumination"]
        }
    }


@pytest.fixture
def sample_pricing_data() -> Dict[str, Any]:
    """Sample pricing data for testing"""
    return {
        "subcategory_pricing": [
            {
                "name": "Smart Bulbs",
                "top_brands": [
                    {"brand": "Philips Hue", "price_range": "$40-$60"}
                ],
                "product_pricing": [
                    {
                        "product_type": "A19 Color Bulb",
                        "typical_price_range": "$40-$60",
                        "average_price": "$48",
                        "units_sold_annually": "5M",
                        "top_brands": [{"brand": "Philips Hue"}]
                    }
                ]
            }
        ],
        "category_price_dynamics": {
            "overall_category_price_range": "$15-$250",
            "category_average_transaction_value": "$65",
            "dominant_retailers": ["Amazon", "Home Depot"]
        }
    }


@pytest.fixture
def sample_market_data() -> Dict[str, Any]:
    """Sample market data for testing"""
    return {
        "market_size": {
            "current_size": {
                "value_usd": "$1.85B",
                "value_midpoint": "$1.85B",
                "year": 2024,
                "geographic_scope": "United States"
            },
            "historical_growth": [
                {"year": 2023, "market_size_usd": "$1.68B", "yoy_growth": "8.4%"}
            ],
            "projections": [
                {"year": 2025, "projected_value": "$2.1B", "growth_rate": "13.5%", "confidence": "high"}
            ],
            "growth_drivers": [
                {
                    "driver": "Smart home adoption",
                    "impact": "high",
                    "description": "Increasing adoption of smart home ecosystems"
                }
            ],
            "growth_inhibitors": [
                {
                    "inhibitor": "High entry price",
                    "impact": "medium",
                    "description": "Premium pricing limiting penetration"
                }
            ]
        },
        "market_share": {
            "market_shares": [
                {
                    "brand": "Philips Hue",
                    "estimated_market_share": "35%",
                    "position": "#1"
                }
            ],
            "competitive_landscape": {
                "key_competitive_factors": ["Smart home integration", "Color accuracy"],
                "emerging_threats": ["Budget LED brands"]
            },
            "market_structure": {
                "concentration_ratio": {"cr4": "68%"}
            }
        }
    }


@pytest.fixture
def sample_full_analysis_data(
    sample_brand_data,
    sample_taxonomy_data,
    sample_pricing_data,
    sample_market_data
) -> Dict[str, Any]:
    """Complete sample analysis data combining all fixtures"""
    return {
        "brands": sample_brand_data,
        "taxonomy": sample_taxonomy_data,
        "pricing": sample_pricing_data,
        **sample_market_data,
        "resources": {
            "total_resources": 5,
            "resource_categories": [
                {
                    "category": "Market Research",
                    "resources": [
                        {
                            "title": "Smart Lighting Report 2024",
                            "provider": "Allied Market Research",
                            "url": "https://example.com/report",
                            "relevance": "High"
                        }
                    ]
                }
            ]
        }
    }


@pytest.fixture
def temp_output_dir(tmp_path):
    """Provide temporary output directory for tests"""
    output_dir = tmp_path / "outputs"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def mock_source():
    """Mock source object for testing"""
    class MockSource:
        def __init__(self, url="https://example.com", confidence="high"):
            self.url = url
            self.confidence = confidence
            self.source_type = "research_report"
            self.accessed_date = "2024-10-16"

    return MockSource
