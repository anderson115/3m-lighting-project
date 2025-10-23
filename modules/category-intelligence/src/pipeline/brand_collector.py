"""Brand collection stage for Category Intelligence."""
from dataclasses import dataclass
from typing import Iterable

@dataclass
class BrandRecord:
    name: str
    tier: str
    source_url: str

class BrandCollector:
    """Fetches distinct brands for a given category using retailer and web sources.

    Concrete implementations must stream real data; subclasses are expected to
    implement `collect` and yield `BrandRecord` instances with citation metadata.
    """

    def collect(self, category: str) -> Iterable[BrandRecord]:
        raise NotImplementedError("BrandCollector.collect must be implemented with live sources.")
