"""Postgres persistence helpers."""
from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from typing import Iterable, Mapping

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


_CREATE_SCHEMA_SQL = "CREATE SCHEMA IF NOT EXISTS category_intel;"

_CREATE_PROJECTS_SQL = """
CREATE TABLE IF NOT EXISTS category_intel.category_projects (
    project_key TEXT PRIMARY KEY,
    client TEXT,
    project_name TEXT,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
"""

_CREATE_BRANDS_SQL = """
CREATE TABLE IF NOT EXISTS category_intel.category_brands (
    project_key TEXT REFERENCES category_intel.category_projects(project_key) ON DELETE SET NULL,
    category TEXT NOT NULL,
    name TEXT NOT NULL,
    tier TEXT,
    source_url TEXT,
    inserted_at TIMESTAMPTZ DEFAULT NOW()
);
"""

_CREATE_PRODUCTS_SQL = """
CREATE TABLE IF NOT EXISTS category_intel.category_products (
    project_key TEXT REFERENCES category_intel.category_projects(project_key) ON DELETE SET NULL,
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

_UPSERT_PROJECT_SQL = """
INSERT INTO category_intel.category_projects (project_key, client, project_name, description)
VALUES (%s, %s, %s, %s)
ON CONFLICT (project_key) DO UPDATE SET
    client = COALESCE(EXCLUDED.client, category_projects.client),
    project_name = COALESCE(EXCLUDED.project_name, category_projects.project_name),
    description = COALESCE(EXCLUDED.description, category_projects.description);
"""

_INSERT_BRAND_SQL = """
INSERT INTO category_intel.category_brands (project_key, category, name, tier, source_url)
VALUES (%s, %s, %s, %s, %s);
"""

_INSERT_PRODUCT_SQL = """
INSERT INTO category_intel.category_products (
    project_key,
    category,
    retailer,
    sku,
    name,
    url,
    price,
    rating,
    taxonomy_path,
    attributes
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""


@dataclass
class PostgresWriter:
    """Writes category data to Postgres with simple audit tables."""

    dsn: str
    project_key: str | None = None
    project_metadata: Mapping[str, str] | None = None

    def _connect(self):  # pragma: no cover - simple wrapper
        if _connect is None:
            raise RuntimeError(
                "psycopg/psycopg2 is required for PostgresWriter. "
                "Install via 'pip install psycopg[binary]' or set up the dependency."
            ) from _IMPORT_ERROR
        return _connect(self.dsn)

    def _ensure_schema(self, cur) -> None:
        cur.execute(_CREATE_SCHEMA_SQL)
        cur.execute(_CREATE_PROJECTS_SQL)
        cur.execute(_CREATE_BRANDS_SQL)
        cur.execute(_CREATE_PRODUCTS_SQL)

    def _ensure_project(self, cur) -> None:
        if not self.project_key:
            return
        metadata = self.project_metadata or {}
        cur.execute(
            _UPSERT_PROJECT_SQL,
            (
                self.project_key,
                metadata.get("client"),
                metadata.get("project_name"),
                metadata.get("description"),
            ),
        )

    def write_brands(self, category: str, brands: Iterable[BrandRecord]) -> None:
        rows = list(brands)
        if not rows:
            _LOGGER.info("No brands to persist for category %s", category)
            return
        try:
            with self._connect() as conn, conn.cursor() as cur:
                self._ensure_schema(cur)
                self._ensure_project(cur)
                params = [
                    (self.project_key, category, brand.name, brand.tier, brand.source_url)
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
                self._ensure_schema(cur)
                self._ensure_project(cur)
                params = []
                for product in rows:
                    params.append(
                        (
                            self.project_key,
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
