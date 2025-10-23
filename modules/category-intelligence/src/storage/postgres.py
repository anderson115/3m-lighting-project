"""Postgres persistence helpers."""
from dataclasses import dataclass
from typing import Iterable
from ..pipeline.brand_collector import BrandRecord
from ..pipeline.product_catalog import ProductRecord

@dataclass
class PostgresWriter:
    dsn: str

    def write_brands(self, category: str, brands: Iterable[BrandRecord]) -> None:
        raise NotImplementedError

    def write_products(self, category: str, products: Iterable[ProductRecord]) -> None:
        raise NotImplementedError
