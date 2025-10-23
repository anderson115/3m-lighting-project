"""Tests for summary analysis."""
from __future__ import annotations

from src.analysis.summary import compute_summary
from src.pipeline.brand_collector import BrandRecord
from src.pipeline.product_catalog import ProductRecord


def test_compute_summary_counts():
    brands = [
        BrandRecord(name="BrandA", tier="test", source_url="url"),
        BrandRecord(name="BrandB", tier="test", source_url="url"),
    ]
    products = [
        ProductRecord(
            retailer="Retailer1",
            sku="1",
            name="Hook",
            url="http://example.com/1",
            price=10.0,
            rating=None,
            taxonomy_path=("Retailer1", "Hooks & Hangers"),
            attributes={"load_capacity_lbs": 25.0, "vendor": "BrandA", "is_hook_or_hanger": True, "is_rail_or_slat_system": False},
        ),
        ProductRecord(
            retailer="Retailer1",
            sku="2",
            name="Rail",
            url="http://example.com/2",
            price=20.0,
            rating=None,
            taxonomy_path=("Retailer1", "Rail & Slat Systems"),
            attributes={"load_capacity_lbs": None, "vendor": "BrandB", "is_hook_or_hanger": False, "is_rail_or_slat_system": True},
        ),
        ProductRecord(
            retailer="Retailer2",
            sku="3",
            name="Basket",
            url="http://example.com/3",
            price=None,
            rating=None,
            taxonomy_path=("Retailer2", "Bins & Baskets"),
            attributes={"load_capacity_lbs": None, "vendor": "BrandB", "is_hook_or_hanger": False, "is_rail_or_slat_system": False},
        ),
    ]

    summary = compute_summary(brands, products)
    assert summary["total_brands"] == 2
    assert summary["total_products"] == 3
    assert summary["retailer_counts"]["Retailer1"] == 2
    assert summary["segment_counts"]["Hooks & Hangers"] == 1
    assert summary["load_capacity"]["with_capacity"] == 1
    assert summary["load_capacity"]["max_capacity"] == 25.0
