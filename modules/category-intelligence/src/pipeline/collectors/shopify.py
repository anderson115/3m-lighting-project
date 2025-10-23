"""Shopify-based collectors for garage organization products."""
from __future__ import annotations

import logging
import re
import time
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
    include_only: tuple[str, ...] = ()  # keywords required in title/tags

    def products_endpoint(self) -> str:
        path = self.collection_path.rstrip('/') + '/products.json' if self.collection_path else '/products.json'
        return f"{self.base_url.rstrip('/')}{path}"


class ShopifyAPI:
    """Thin wrapper around Shopify collection/product JSON endpoints."""

    def __init__(self, session: requests.Session | None = None, max_retries: int = 3, retry_delay: float = 1.0) -> None:
        self._session = session or requests.Session()
        self._session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
        })
        self._max_retries = max_retries
        self._retry_delay = retry_delay

    def fetch_products(self, endpoint: str) -> List[dict]:
        attempt = 0
        while True:
            try:
                resp = self._session.get(endpoint, timeout=30)
                resp.raise_for_status()
                payload = resp.json()
                products = payload.get("products", [])
                if not isinstance(products, list):
                    raise ValueError(f"Unexpected response structure from {endpoint}")
                return products
            except Exception as exc:  # pylint: disable=broad-except
                attempt += 1
                if attempt >= self._max_retries:
                    raise
                _LOGGER.warning("Retrying Shopify fetch (%s/%s) for %s due to %s", attempt, self._max_retries, endpoint, exc)
                time.sleep(self._retry_delay)


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

    @staticmethod
    def _normalize_tags(raw: str | list[str] | None) -> list[str]:
        if raw is None:
            return []
        if isinstance(raw, list):
            return [t.strip().lower() for t in raw if t]
        return [part.strip().lower() for part in raw.split(',') if part.strip()]

    @staticmethod
    def _contains_keywords(text: str, keywords: Iterable[str]) -> bool:
        haystack = text.lower()
        return any(keyword.lower() in haystack for keyword in keywords)

    @staticmethod
    def _classify_hook(title: str, tags: list[str]) -> bool:
        haystack = title.lower() + ' ' + ' '.join(tags)
        return any(token in haystack for token in ("hook", "hanger"))

    @staticmethod
    def _classify_rail(title: str, tags: list[str]) -> bool:
        haystack = title.lower() + ' ' + ' '.join(tags)
        return any(token in haystack for token in ("rail", "slat", "track system", "wall track"))

    def _derive_segment(
        self,
        title: str,
        tags: list[str],
        product_type: str | None,
        is_hook: bool,
        is_rail: bool,
    ) -> str:
        title_lower = title.lower()
        if is_rail:
            return "Rail & Slat Systems"
        if is_hook:
            return "Hooks & Hangers"
        if "basket" in title_lower or "basket" in tags:
            return "Bins & Baskets"
        if product_type:
            return product_type.title()
        if "rack" in title_lower:
            return "Racks"
        return "Accessories"

    @staticmethod
    def _extract_load_capacity(description: str) -> float | None:
        match = re.findall(r'(\d+(?:\.\d+)?)\s*(?:lb|lbs|pound|pounds)', description, flags=re.IGNORECASE)
        if not match:
            return None
        try:
            return max(float(value) for value in match)
        except ValueError:
            return None

    def collect(self, category: str) -> Iterable[ProductRecord]:
        for store in self._stores:
            endpoint = store.products_endpoint()
            try:
                products = self._api.fetch_products(endpoint)
            except Exception as exc:  # pylint: disable=broad-except
                _LOGGER.warning("Failed to fetch products from %s: %s", endpoint, exc)
                continue

            for product in products:
                tags = self._normalize_tags(product.get("tags"))
                title = product.get("title", "").strip()
                if store.tag_filter and store.tag_filter.lower() not in tags:
                    continue
                if store.include_only and not self._contains_keywords(title + ' ' + ' '.join(tags), store.include_only):
                    continue

                handle = product.get("handle", "")
                product_url = f"{store.base_url.rstrip('/')}/products/{handle}" if handle else endpoint
                vendor = product.get("vendor")
                product_type = product.get("product_type")
                variants = product.get("variants") or []
                variant = variants[0] if variants else {}
                price_str = variant.get("price") or variant.get("compare_at_price")
                try:
                    price = float(price_str) if price_str else None
                except (TypeError, ValueError):
                    price = None
                sku = variant.get("sku") or str(variant.get("id")) if variant else product.get("id")
                description = (product.get("body_html") or "")
                load_capacity = self._extract_load_capacity(description)
                is_hook = self._classify_hook(title, tags)
                is_rail = self._classify_rail(title, tags)
                segment = self._derive_segment(title, tags, product_type, is_hook, is_rail)
                attributes = {
                    "vendor": vendor,
                    "product_type": product_type,
                    "tags": tags,
                    "is_hook_or_hanger": is_hook,
                    "is_rail_or_slat_system": is_rail,
                    "load_capacity_lbs": load_capacity,
                }
                yield ProductRecord(
                    retailer=store.name,
                    sku=str(sku) if sku else "",
                    name=title,
                    url=product_url,
                    price=price,
                    rating=None,
                    taxonomy_path=(store.name, segment),
                    attributes=attributes,
                )
