"""Filesystem persistence helpers."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from ..pipeline.brand_collector import BrandRecord
from ..pipeline.product_catalog import ProductRecord

@dataclass
class FilesystemWriter:
    base_dir: Path

    def __post_init__(self) -> None:
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def write_brands(self, category: str, brands: Iterable[BrandRecord]) -> Path:
        data = [asdict(b) for b in brands]
        output = self.base_dir / f"{category.replace(' ', '_')}_brands.json"
        output.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        return output

    def write_products(self, category: str, products: Iterable[ProductRecord]) -> Path:
        data = [
            {
                "retailer": p.retailer,
                "sku": p.sku,
                "name": p.name,
                "url": p.url,
                "price": p.price,
                "rating": p.rating,
                "taxonomy_path": p.taxonomy_path,
                "attributes": p.attributes,
            }
            for p in products
        ]
        output = self.base_dir / f"{category.replace(' ', '_')}_products.json"
        output.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        return output

    def write_keyword_summary(self, category: str, summary: dict) -> Path:
        output = self.base_dir / f"{category.replace(' ', '_')}_keyword_language.json"
        output.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
        return output
