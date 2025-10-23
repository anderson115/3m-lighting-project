"""Shopify-based collectors for garage organization products."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable, List

import requests

from ..brand_collector import BrandCollector, BrandRecord
from ..product_catalog import ProductCatalogBuilder, ProductRecord

_LOGGER = logging.getLogger(__name__)

@dataclass(frozen=True)
class ShopifyStoreConfig:
    name: str
    base_url: str  # e.g. https://totalgarage.myshopify.com
    collection_path: str | None = None  # e.g. '/collections/hooks-hardware'
    tag_filter: str | None = None  # optional tag to filter products

    def products_endpoint(self) -> str:
        if self.collection_path:
            path = self.collection_path.rstrip('/') + '/products.json'
        else:
            path = '/products.json'
        return f"{self.base_url.rstrip('/')}{path}"


class ShopifyAPI:
    """Thin wrapper around Shopify collection/product JSON endpoints."""

    def __init__(self, session: requests.Session | None = None) -> None:
        self._session = session or requests.Session()
        self._session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
        })

    def fetch_products(self, endpoint: str) -> List[dict]:
        resp = self._session.get(endpoint, timeout=30)
        resp.raise_for_status()
        payload = resp.json()
        products = payload.get("products", [])
        if not isinstance(products, list):
            raise ValueError(f"Unexpected response structure from {endpoint}")
        return products


class ShopifyBrandCollector(BrandCollector):
    """Collects unique vendors from configured Shopify stores."""

    def __init__(self, stores: list[ShopifyStoreConfig], api: ShopifyAPI | None = None) -> None:
        self._stores = stores
        self._api = api or ShopifyAPI()

    def collect(self, category: str) -> Iterable[BrandRecord]:
        seen: set[str] = set()
        for store in self._stores:
            endpoint = store.products_endpoint()
            try:
                products = self._api.fetch_products(endpoint)
            except Exception as exc:  # pylint: disable=broad-except
                _LOGGER.warning("Failed to fetch products from %s: %s", endpoint, exc)
                continue

            for product in products:
                vendor = product.get("vendor") or product.get("brand")
                if not vendor:
                    continue
                key = vendor.strip()
                if not key or key.lower() in seen:
                    continue
                seen.add(key.lower())
                yield BrandRecord(
                    name=key,
                    tier="independent_shopify",
                    source_url=endpoint,
                )


class ShopifyProductCatalog(ProductCatalogBuilder):
    """Collects product metadata from Shopify stores."""

    def __init__(self, stores: list[ShopifyStoreConfig], api: ShopifyAPI | None = None) -> None:
        self._stores = stores
        self._api = api or ShopifyAPI()

    def collect(self, category: str) -> Iterable[ProductRecord]:
        for store in self._stores:
            endpoint = store.products_endpoint()
            try:
                products = self._api.fetch_products(endpoint)
            except Exception as exc:  # pylint: disable=broad-except
                _LOGGER.warning("Failed to fetch products from %s: %s", endpoint, exc)
                continue

            for product in products:
                if store.tag_filter and store.tag_filter not in product.get("tags", ""):
                    continue
                title = product.get("title", "").strip()
                handle = product.get("handle", "")
                product_url = f"{store.base_url.rstrip('/')}/products/{handle}" if handle else endpoint
                vendor = product.get("vendor")
                product_type = product.get("product_type")
                tags = product.get("tags", "")
                variants = product.get("variants") or []
                variant = variants[0] if variants else {}
                price_str = variant.get("price") or variant.get("compare_at_price")
                try:
                    price = float(price_str) if price_str else None
                except ValueError:
                    price = None
                sku = variant.get("sku") or str(variant.get("id")) if variant else product.get("id")
                attributes = {
                    "vendor": vendor,
                    "product_type": product_type,
                    "tags": tags,
                }
                taxonomy = tuple(filter(None, [store.name, product_type]))
                yield ProductRecord(
                    retailer=store.name,
                    sku=str(sku) if sku else "",
                    name=title,
                    url=product_url,
                    price=price,
                    rating=None,
                    taxonomy_path=taxonomy,
                    attributes=attributes,
                )
