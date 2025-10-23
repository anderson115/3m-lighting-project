"""Unit tests for Shopify collectors."""
from src.pipeline.collectors.shopify import ShopifyBrandCollector, ShopifyProductCatalog, ShopifyStoreConfig
from src.pipeline.collectors.shopify import ShopifyAPI
from src.pipeline.product_catalog import ProductRecord


class FakeShopifyAPI(ShopifyAPI):
    def __init__(self, payload):
        self._payload = payload
        super().__init__()

    def fetch_products(self, endpoint: str):
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
                "title": "Ceiling Storage Rack",
                "handle": "ceiling-storage-rack",
                "vendor": "StorageMaster",
                "product_type": "Rack",
                "tags": "garage, rack",
                "variants": [
                    {"id": 2, "price": "199.00", "sku": "SM-RACK-1"}
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
    assert first.retailer == "Test Store"
    assert first.price == 12.99
    assert first.attributes["vendor"] == "GaragePro"
    assert first.url.endswith('heavy-duty-garage-hook')
