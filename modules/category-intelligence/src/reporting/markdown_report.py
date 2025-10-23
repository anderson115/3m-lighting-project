"""Render Markdown deliverables for Category Intelligence."""
from pathlib import Path
from typing import Mapping, Sequence

from ..pipeline.brand_collector import BrandRecord
from ..pipeline.product_catalog import ProductRecord

REPORT_TEMPLATE = """# {category} Category Intelligence

## Brand Landscape
Total brands: {brand_count}

## Product Coverage
Total SKUs: {product_count}

## Retailer Coverage
{retailer_breakdown}

## Segment Mix
{segment_breakdown}

### Segment Pricing
{segment_price_breakdown}

## Top Vendors
{top_vendors}

## Load Capacity Highlights
Products with published load: {load_with_capacity}
Maximum load observed: {max_load}
"""


def _format_counter(counter: Mapping[str, int]) -> str:
    if not counter:
        return "(no data)"
    lines = [f"- {key}: {value}" for key, value in counter.items()]
    return "\n".join(lines)


def _format_top_vendors(vendors: Sequence[tuple[str, int]]) -> str:
    if not vendors:
        return "(no data)"
    return "\n".join(f"- {name}: {count}" for name, count in vendors)


def _format_price_stats(stats: Mapping[str, Mapping[str, float | None]]) -> str:
    if not stats:
        return "(no data)"
    lines = []
    for segment, values in stats.items():
        avg = values.get("avg_price")
        min_price = values.get("min_price")
        max_price = values.get("max_price")
        lines.append(
            f"- {segment}: avg ${avg if avg is not None else 'N/A'}, min ${min_price if min_price is not None else 'N/A'}, max ${max_price if max_price is not None else 'N/A'}"
        )
    return "\n".join(lines)


class MarkdownReporter:
    """Simple Markdown renderer while full deck/report tooling is rebuilt."""

    def render(
        self,
        category: str,
        brands: Sequence[BrandRecord],
        products: Sequence[ProductRecord],
        output_path: Path,
        summary: Mapping[str, object] | None = None,
    ) -> None:
        summary = summary or {}
        retailer_breakdown = _format_counter(summary.get("retailer_counts", {}))
        segment_breakdown = _format_counter(summary.get("segment_counts", {}))
        top_vendors = _format_top_vendors(summary.get("top_vendors", []))
        segment_price_breakdown = _format_price_stats(summary.get("segment_price_stats", {}))
        load_info = summary.get("load_capacity", {})
        load_with_capacity = load_info.get("with_capacity", 0)
        max_load = load_info.get("max_capacity") or "(unknown)"

        output_path.write_text(
            REPORT_TEMPLATE.format(
                category=category,
                brand_count=len(brands),
                product_count=len(products),
                retailer_breakdown=retailer_breakdown,
                segment_breakdown=segment_breakdown,
                segment_price_breakdown=segment_price_breakdown,
                top_vendors=top_vendors,
                load_with_capacity=load_with_capacity,
                max_load=max_load,
            )
        )
