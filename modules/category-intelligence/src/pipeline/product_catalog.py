"""SKU aggregation stage."""
from dataclasses import dataclass
from typing import Iterable

@dataclass
class ProductRecord:
    retailer: str
    sku: str
    name: str
    url: str
    price: float | None
    rating: float | None
    taxonomy_path: tuple[str, ...]
    attributes: dict[str, object]

class ProductCatalogBuilder:
    """Aggregates top-performing SKUs from retailer catalogs.

    Implementations should guarantee transparent sourcing, preserve list order,
    and surface missing attributes rather than filling placeholders.
    """

    def collect(self, category: str) -> Iterable[ProductRecord]:
        raise NotImplementedError
