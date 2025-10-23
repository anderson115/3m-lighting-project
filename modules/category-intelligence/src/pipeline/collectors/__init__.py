"""Collector utilities for combining sources."""
from __future__ import annotations

from typing import Iterable, Sequence

from ..brand_collector import BrandCollector, BrandRecord
from ..product_catalog import ProductCatalogBuilder, ProductRecord


class CompositeBrandCollector(BrandCollector):
    """Combines multiple brand collectors into a single stream."""

    def __init__(self, collectors: Sequence[BrandCollector]) -> None:
        self._collectors = collectors

    def collect(self, category: str) -> Iterable[BrandRecord]:
        seen: set[str] = set()
        for collector in self._collectors:
            for brand in collector.collect(category):
                identifier = brand.name.strip().lower()
                if identifier and identifier not in seen:
                    seen.add(identifier)
                    yield brand


class CompositeProductCatalog(ProductCatalogBuilder):
    """Concatenates product records from multiple collectors."""

    def __init__(self, catalogs: Sequence[ProductCatalogBuilder]) -> None:
        self._catalogs = catalogs

    def collect(self, category: str) -> Iterable[ProductRecord]:
        for catalog in self._catalogs:
            yield from catalog.collect(category)
