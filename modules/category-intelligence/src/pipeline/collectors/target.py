"""Target (US) collectors using jina.ai HTML snapshots."""
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

_TARGET_TEMPLATE = "https://r.jina.ai/https://www.target.com/s?searchTerm={query}&Nao={offset}"
_PAGE_SIZE = 24  # observed items per page in markup snapshot


@dataclass(frozen=True)
class TargetRequestConfig:
    query: str = "garage hooks"
    max_pages: int = 4
    delay_seconds: float = 1.0  # be polite and avoid hammering


class TargetScraper:
    """Retrieves markdown snapshots of Target search results via jina.ai."""

    def __init__(
        self,
        config: TargetRequestConfig | None = None,
        session: requests.Session | None = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ) -> None:
        self._config = config or TargetRequestConfig()
        self._session = session or requests.Session()
        self._max_retries = max_retries
        self._retry_delay = retry_delay

    def fetch_pages(self) -> Iterable[str]:
        query = self._config.query.replace(" ", "+")
        for page in range(self._config.max_pages):
            offset = page * _PAGE_SIZE
            url = _TARGET_TEMPLATE.format(query=query, offset=offset)
            attempt = 0
            while True:
                try:
                    resp = self._session.get(url, timeout=30)
                    resp.raise_for_status()
                    yield resp.text
                    time.sleep(self._config.delay_seconds)
                    break
                except Exception as exc:  # pylint: disable=broad-except
                    attempt += 1
                    if attempt >= self._max_retries:
                        _LOGGER.warning("Failed to fetch Target page %s after retries: %s", url, exc)
                        return
                    _LOGGER.warning("Retrying Target page %s (%s/%s) due to %s", url, attempt, self._max_retries, exc)
                    time.sleep(self._retry_delay)


@dataclass
class TargetProduct:
    title: str
    url: str
    price: str | None
    brand: str | None
    rating: str | None


class TargetParser:
    """Parses the markdown output returned by jina.ai for Target pages."""

    PRODUCT_HEADER = '### ['
    PRODUCT_LINK_RE = re.compile(r"^### \[(.*?)\]\((https://www.target.com/[^\)]*)\)")
    LINK_TEXT_RE = re.compile(r"\[(.*?)\]\(https://www.target.com/[^\)]*\)")
    BRAND_RE = re.compile(r"^\[(.*?)\]\(https://www.target.com/b/")
    RATING_RE = re.compile(r"^(\[.*?out of.*?reviews\])")
    IMAGE_RE = re.compile(r"!\[.*?\]\([^)]*\)")

    def parse(self, markdown: str) -> List[TargetProduct]:
        products: List[TargetProduct] = []
        buffer: list[str] = []
        for line in markdown.splitlines():
            if line.startswith(self.PRODUCT_HEADER):
                if buffer:
                    product = self._parse_block(buffer)
                    if product:
                        products.append(product)
                buffer = [line]
            elif buffer:
                buffer.append(line)
        if buffer:
            product = self._parse_block(buffer)
            if product:
                products.append(product)
        return products

    def _parse_block(self, lines: list[str]) -> TargetProduct | None:
        match = self.PRODUCT_LINK_RE.match(lines[0])
        if not match:
            return None
        url = match.group(2)
        title = self._extract_title(lines)
        price = self._extract_price(lines)
        brand = self._extract_brand(lines)
        rating = self._extract_rating(lines)
        return TargetProduct(title=title, url=url, price=price, brand=brand, rating=rating)

    def _extract_title(self, lines: List[str]) -> str:
        for line in lines[1:15]:
            match = self.LINK_TEXT_RE.match(line.strip())
            if match and not line.startswith('[!') and 'target.com/p/' in line and 'scroll_to_review_section' not in line:
                cleaned = self._clean_text(match.group(1))
                if cleaned:
                    return cleaned
        header_match = self.LINK_TEXT_RE.match(lines[0].strip())
        if header_match:
            cleaned = self._clean_text(header_match.group(1))
            if cleaned:
                return cleaned
        return self._clean_text(lines[0])

    @staticmethod
    def _extract_price(lines: List[str]) -> str | None:
        for line in lines:
            if line.startswith('$'):
                return line.strip()
        return None

    def _extract_brand(self, lines: List[str]) -> str | None:
        for line in lines:
            match = self.BRAND_RE.match(line)
            if match:
                return match.group(1)
        return None

    def _extract_rating(self, lines: List[str]) -> str | None:
        for line in lines:
            match = self.RATING_RE.match(line)
            if match:
                return match.group(1)
        return None

    def _clean_text(self, text: str) -> str:
        cleaned = self.IMAGE_RE.sub('', text)
        cleaned = cleaned.replace('###', '')
        return cleaned.replace('\u00a0', ' ').strip()
def _normalise_terms(terms: Iterable[str] | None) -> tuple[str, ...]:
    if not terms:
        return ()
    return tuple(term.lower() for term in terms if term)


def _should_include(title: str, include_terms: tuple[str, ...], exclude_terms: tuple[str, ...]) -> bool:
    lowered = title.lower()
    if include_terms and not any(term in lowered for term in include_terms):
        return False
    if exclude_terms and any(term in lowered for term in exclude_terms):
        return False
    return True


class TargetBrandCollector(BrandCollector):
    """Extracts unique brands from Target search results."""

    def __init__(
        self,
        scraper: TargetScraper | None = None,
        parser: TargetParser | None = None,
        include_terms: Iterable[str] | None = None,
        exclude_terms: Iterable[str] | None = None,
    ) -> None:
        self._scraper = scraper or TargetScraper()
        self._parser = parser or TargetParser()
        self._include_terms = _normalise_terms(include_terms)
        self._exclude_terms = _normalise_terms(exclude_terms)

    def collect(self, category: str) -> Iterable[BrandRecord]:  # pylint: disable=unused-argument
        seen: set[str] = set()
        for page in self._scraper.fetch_pages():
            for product in self._parser.parse(page):
                if not _should_include(product.title, self._include_terms, self._exclude_terms):
                    continue
                if not product.brand:
                    continue
                key = product.brand.strip().lower()
                if key and key not in seen:
                    seen.add(key)
                    yield BrandRecord(name=product.brand.strip(), tier="target", source_url=product.url)


class TargetProductCatalog(ProductCatalogBuilder):
    """Collects product metadata from Target search results."""

    def __init__(
        self,
        scraper: TargetScraper | None = None,
        parser: TargetParser | None = None,
        include_terms: Iterable[str] | None = None,
        exclude_terms: Iterable[str] | None = None,
    ) -> None:
        self._scraper = scraper or TargetScraper()
        self._parser = parser or TargetParser()
        self._include_terms = _normalise_terms(include_terms)
        self._exclude_terms = _normalise_terms(exclude_terms)

    @staticmethod
    def _classify_hook(title: str) -> bool:
        title_lower = title.lower()
        return any(token in title_lower for token in ("hook", "hanger"))

    @staticmethod
    def _classify_rail(title: str) -> bool:
        title_lower = title.lower()
        return any(token in title_lower for token in ("rail", "track", "slat"))

    def collect(self, category: str) -> Iterable[ProductRecord]:  # pylint: disable=unused-argument
        for page in self._scraper.fetch_pages():
            for product in self._parser.parse(page):
                if not _should_include(product.title, self._include_terms, self._exclude_terms):
                    continue
                is_hook = self._classify_hook(product.title)
                is_rail = self._classify_rail(product.title)
                attributes = {
                    "brand": product.brand,
                    "rating": product.rating,
                    "is_hook_or_hanger": is_hook,
                    "is_rail_or_slat_system": is_rail,
                }
                price_value = None
                if product.price:
                    try:
                        price_value = float(product.price.replace('$', '').replace(',', ''))
                    except ValueError:
                        price_value = None
                yield ProductRecord(
                    retailer="Target",
                    sku="",
                    name=product.title,
                    url=product.url,
                    price=price_value,
                    rating=None,
                    taxonomy_path=("Target", "Hooks & Hangers" if is_hook else "Rail & Slat Systems" if is_rail else "Accessories"),
                    attributes=attributes,
                )
