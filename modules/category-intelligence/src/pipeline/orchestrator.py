"""High-level orchestration for category intelligence."""
from dataclasses import dataclass
from .brand_collector import BrandCollector
from .product_catalog import ProductCatalogBuilder

@dataclass
class CategoryIntelligencePipeline:
    brand_collector: BrandCollector
    product_builder: ProductCatalogBuilder
    min_brands: int = 10

    def run(self, category: str) -> dict:
        """Execute the core stages for a category.

        Raises:
            RuntimeError: if mandatory stages fail to produce minimum coverage.
        """
        brands = list(self.brand_collector.collect(category))
        if len(brands) < self.min_brands:
            raise RuntimeError(f"Insufficient brand coverage: {len(brands)} discovered")

        products = list(self.product_builder.collect(category))
        return {
            "brands": brands,
            "products": products,
        }
