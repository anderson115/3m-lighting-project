"""Render Markdown deliverables for Category Intelligence."""
from pathlib import Path
from typing import Sequence
from ..pipeline.brand_collector import BrandRecord
from ..pipeline.product_catalog import ProductRecord

REPORT_TEMPLATE = """# {category} Category Intelligence

## Brand Landscape
Total brands: {brand_count}

## Product Coverage
Total SKUs: {product_count}
"""

class MarkdownReporter:
    """Simple Markdown renderer while full deck/report tooling is rebuilt."""

    def render(self, category: str, brands: Sequence[BrandRecord], products: Sequence[ProductRecord], output_path: Path) -> None:
        output_path.write_text(
            REPORT_TEMPLATE.format(
                category=category,
                brand_count=len(brands),
                product_count=len(products),
            )
        )
