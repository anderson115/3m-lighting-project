"""Postgres persistence helpers."""
from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from typing import Iterable

try:  # pragma: no cover - optional dependency
    import psycopg
    _connect = psycopg.connect
except ImportError:  # pragma: no cover
    try:
        import psycopg2 as psycopg  # type: ignore
        _connect = psycopg.connect  # type: ignore
    except ImportError as exc:  # pragma: no cover
        psycopg = None  # type: ignore
        _connect = None
        _IMPORT_ERROR = exc
    else:
        _IMPORT_ERROR = None
else:
    _IMPORT_ERROR = None

from ..pipeline.brand_collector import BrandRecord
from ..pipeline.product_catalog import ProductRecord

_LOGGER = logging.getLogger(__name__)


_CREATE_BRANDS_SQL = """
CREATE TABLE IF NOT EXISTS category_brands (
    category TEXT NOT NULL,
    name TEXT NOT NULL,
    tier TEXT,
    source_url TEXT,
    inserted_at TIMESTAMPTZ DEFAULT NOW()
);
"""

_CREATE_PRODUCTS_SQL = """
CREATE TABLE IF NOT EXISTS category_products (
    category TEXT NOT NULL,
    retailer TEXT,
    sku TEXT,
    name TEXT,
    url TEXT,
    price NUMERIC,
    rating NUMERIC,
    taxonomy_path JSONB,
    attributes JSONB,
    inserted_at TIMESTAMPTZ DEFAULT NOW()
);
"""

_INSERT_BRAND_SQL = """
INSERT INTO category_brands (category, name, tier, source_url)
VALUES (%s, %s, %s, %s);
"""

_INSERT_PRODUCT_SQL = """
INSERT INTO category_products
    (category, retailer, sku, name, url, price, rating, taxonomy_path, attributes)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
"""


@dataclass
class PostgresWriter:
    """Writes category data to Postgres with simple audit tables."""

    dsn: str

    def _connect(self):  # pragma: no cover - simple wrapper
        if _connect is None:
            raise RuntimeError(
                "psycopg/psycopg2 is required for PostgresWriter. "
                "Install via 'pip install psycopg[binary]' or set up the dependency."
            ) from _IMPORT_ERROR
        return _connect(self.dsn)

    def write_brands(self, category: str, brands: Iterable[BrandRecord]) -> None:
        rows = list(brands)
        if not rows:
            _LOGGER.info("No brands to persist for category %s", category)
            return
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(_CREATE_BRANDS_SQL)
                params = [
                    (category, brand.name, brand.tier, brand.source_url)
                    for brand in rows
                ]
                cur.executemany(_INSERT_BRAND_SQL, params)
        except Exception as exc:  # pragma: no cover - database error path
            _LOGGER.error("Failed to persist brand data: %s", exc)
            raise

    def write_products(self, category: str, products: Iterable[ProductRecord]) -> None:
        rows = list(products)
        if not rows:
            _LOGGER.info("No products to persist for category %s", category)
            return
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(_CREATE_PRODUCTS_SQL)
                params = []
                for product in rows:
                    params.append(
                        (
                            category,
                            product.retailer,
                            product.sku,
                            product.name,
                            product.url,
                            product.price,
                            product.rating,
                            json.dumps(list(product.taxonomy_path)),
                            json.dumps(product.attributes, ensure_ascii=False),
                        )
                    )
                cur.executemany(_INSERT_PRODUCT_SQL, params)
        except Exception as exc:  # pragma: no cover
            _LOGGER.error("Failed to persist product data: %s", exc)
            raise
