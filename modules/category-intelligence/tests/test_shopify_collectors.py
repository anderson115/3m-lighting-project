"""Unit tests for Shopify collectors."""
from __future__ import annotations

from src.pipeline.collectors.shopify import (
    ShopifyAPI,
    ShopifyBrandCollector,
    ShopifyProductCatalog,
    ShopifyStoreConfig,
)
from src.pipeline.product_catalog import ProductRecord


class FakeShopifyAPI(ShopifyAPI):
    def __init__(self, payload):
        self._payload = payload
        super().__init__()

    def fetch_products(self, endpoint: str):  # type: ignore[override]
        return self._payload.get(endpoint, [])


def sample_products(store: ShopifyStoreConfig):
    endpoint = store.products_endpoint()
    payload = {
        endpoint: [
            {
                "title": "Heavy Duty Garage Hook",
                "handle": "heavy-duty-garage-hook",
                "vendor": "GaragePro",
                "product_type": "Hook",
                "tags": "garage, hook",
                "variants": [
                    {"id": 1, "price": "12.99", "sku": "GP-HOOK-1"}
                ],
            },
            {
                "title": "Ceiling Storage Rail",
                "handle": "ceiling-storage-rail",
                "vendor": "StorageMaster",
                "product_type": "Rail",
                "tags": "garage, rail",
                "variants": [
                    {"id": 2, "price": "199.00", "sku": "SM-RAIL-1"}
                ],
            },
        ]
    }
    return payload


def test_shopify_brand_collector_deduplicates_vendors():
    store = ShopifyStoreConfig(name="Test Store", base_url="https://shop.example.com")
    fake_api = FakeShopifyAPI(sample_products(store))
    collector = ShopifyBrandCollector([store], api=fake_api)

    brands = list(collector.collect("garage"))

    assert {brand.name for brand in brands} == {"GaragePro", "StorageMaster"}


def test_shopify_product_catalog_emits_product_records():
    store = ShopifyStoreConfig(name="Test Store", base_url="https://shop.example.com")
    fake_api = FakeShopifyAPI(sample_products(store))
    catalog = ShopifyProductCatalog([store], api=fake_api)

    products = list(catalog.collect("garage"))

    assert len(products) == 2
    first: ProductRecord = products[0]
    second: ProductRecord = products[1]
    assert first.retailer == "Test Store"
    assert first.price == 12.99
    assert first.attributes["vendor"] == "GaragePro"
    assert first.attributes["is_hook_or_hanger"] is True
    assert first.attributes["is_rail_or_slat_system"] is False
    assert first.attributes["load_capacity_lbs"] is None
    assert second.attributes["is_rail_or_slat_system"] is True
    assert second.attributes["load_capacity_lbs"] is None
    assert first.url.endswith("heavy-duty-garage-hook")
