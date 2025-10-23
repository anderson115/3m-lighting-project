"""DuckDB persistence helpers."""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import duckdb

from ..pipeline.brand_collector import BrandRecord
from ..pipeline.product_catalog import ProductRecord

_LOGGER = logging.getLogger(__name__)


@dataclass
class DuckDBWriter:
    """Stores brand and product tables in a DuckDB file."""

    db_path: Path

    def __post_init__(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = duckdb.connect(self.db_path.as_posix())
        self._init_schema()

    def _init_schema(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS category_brands (
                category TEXT,
                name TEXT,
                tier TEXT,
                source_url TEXT,
                inserted_at TIMESTAMP DEFAULT current_timestamp
            )
            """
        )
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS category_products (
                category TEXT,
                retailer TEXT,
                sku TEXT,
                name TEXT,
                url TEXT,
                price DOUBLE,
                rating DOUBLE,
                taxonomy_path TEXT,
                attributes JSON,
                inserted_at TIMESTAMP DEFAULT current_timestamp
            )
            """
        )

    def write_brands(self, category: str, brands: Iterable[BrandRecord]) -> None:
        rows = [
            (category, b.name, b.tier, b.source_url)
            for b in brands
        ]
        if not rows:
            _LOGGER.info("No brands to persist to DuckDB")
            return
        self._conn.executemany(
            "INSERT INTO category_brands (category, name, tier, source_url) VALUES (?, ?, ?, ?)",
            rows,
        )

    def write_products(self, category: str, products: Iterable[ProductRecord]) -> None:
        rows = []
        for p in products:
            rows.append(
                (
                    category,
                    p.retailer,
                    p.sku,
                    p.name,
                    p.url,
                    p.price,
                    p.rating,
                    json.dumps(list(p.taxonomy_path)),
                    json.dumps(p.attributes, ensure_ascii=False),
                )
            )
        if not rows:
            _LOGGER.info("No products to persist to DuckDB")
            return
        self._conn.executemany(
            """
            INSERT INTO category_products (
                category, retailer, sku, name, url, price, rating, taxonomy_path, attributes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )

    def close(self) -> None:
        self._conn.close()

