"""Summarize category intelligence datasets."""
from __future__ import annotations

from collections import Counter, defaultdict
from statistics import mean
from typing import Any, Iterable, Mapping

from ..pipeline.brand_collector import BrandRecord
from ..pipeline.product_catalog import ProductRecord


def compute_summary(brands: Iterable[BrandRecord], products: Iterable[ProductRecord]) -> dict[str, Any]:
    brand_list = list(brands)
    product_list = list(products)

    retailer_counts = Counter(p.retailer for p in product_list if p.retailer)
    segment_counts = Counter()
    load_values = []
    retailer_prices: dict[str, list[float]] = defaultdict(list)
    vendor_counts = Counter()

    for product in product_list:
        segment = product.taxonomy_path[1] if len(product.taxonomy_path) > 1 else "Unclassified"
        segment_counts[segment] += 1
        load_capacity = product.attributes.get("load_capacity_lbs")
        if isinstance(load_capacity, (int, float)):
            load_values.append(float(load_capacity))
        if product.price is not None:
            retailer_prices[product.retailer].append(float(product.price))
        vendor = product.attributes.get("vendor") or product.attributes.get("brand")
        if isinstance(vendor, str) and vendor.strip():
            vendor_counts[vendor.strip()] += 1

    retailer_price_stats = {
        retailer: {
            "avg_price": round(mean(values), 2) if values else None,
            "min_price": round(min(values), 2) if values else None,
            "max_price": round(max(values), 2) if values else None,
        }
        for retailer, values in retailer_prices.items()
    }

    summary: dict[str, Any] = {
        "total_brands": len(brand_list),
        "total_products": len(product_list),
        "retailer_counts": dict(sorted(retailer_counts.items(), key=lambda x: (-x[1], x[0]))),
        "segment_counts": dict(sorted(segment_counts.items(), key=lambda x: (-x[1], x[0]))),
        "top_vendors": vendor_counts.most_common(10),
        "retailer_price_stats": retailer_price_stats,
        "load_capacity": {
            "with_capacity": len(load_values),
            "max_capacity": round(max(load_values), 2) if load_values else None,
        },
    }

    return summary

