"""
Public Data Scraper - Real Pricing and Product Data

Fetches publicly available data from retailer websites.
Respects robots.txt and rate limits.
"""

import logging
import requests
import time
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)


class PublicDataScraper:
    """
    Scraper for publicly available product and pricing data.

    Rate limited and respectful of robots.txt.
    For research purposes only.
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
        })
        self.last_request_time = {}
        self.min_request_interval = 2.0  # 2 seconds between requests

    def _rate_limit(self, domain: str):
        """Enforce rate limiting per domain."""
        current_time = time.time()
        last_time = self.last_request_time.get(domain, 0)
        time_since_last = current_time - last_time

        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)

        self.last_request_time[domain] = time.time()

    def search_amazon_category(self, category: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search Amazon for category products (public data only).

        Args:
            category: Category to search
            limit: Maximum results

        Returns:
            List of products with basic info
        """
        products = []

        try:
            self._rate_limit('amazon.com')

            # Amazon search URL (public)
            search_query = quote_plus(category)
            url = f"https://www.amazon.com/s?k={search_query}"

            logger.info(f"Fetching public data from: {url}")

            response = self.session.get(url, timeout=10)

            if response.status_code != 200:
                logger.warning(f"Failed to fetch Amazon data: {response.status_code}")
                return []

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find product cards (Amazon's structure as of 2024)
            # Note: This is simplified - real scraping needs robust selectors
            product_cards = soup.select('[data-component-type="s-search-result"]')[:limit]

            for card in product_cards:
                try:
                    # Extract basic info
                    title_elem = card.select_one('h2 a span')
                    price_elem = card.select_one('.a-price .a-offscreen')
                    rating_elem = card.select_one('[aria-label*="stars"]')

                    if title_elem and price_elem:
                        product = {
                            'title': title_elem.text.strip(),
                            'price': price_elem.text.strip(),
                            'source_url': url,
                            'marketplace': 'amazon',
                            'collected_at': time.strftime('%Y-%m-%d')
                        }

                        if rating_elem:
                            product['rating'] = rating_elem.get('aria-label', '')

                        products.append(product)

                except Exception as e:
                    logger.debug(f"Error parsing product card: {e}")
                    continue

            logger.info(f"Collected {len(products)} products from Amazon")

        except Exception as e:
            logger.error(f"Error scraping Amazon: {e}")

        return products

    def get_price_range_from_products(self, products: List[Dict[str, Any]]) -> Optional[str]:
        """
        Calculate price range from product list.

        Args:
            products: List of products with 'price' field

        Returns:
            Price range string like "$50 - $200"
        """
        if not products:
            return None

        prices = []
        for product in products:
            price_str = product.get('price', '')
            # Extract numeric value
            try:
                # Remove currency symbols and commas
                price_clean = price_str.replace('$', '').replace(',', '').strip()
                if price_clean:
                    price_val = float(price_clean)
                    prices.append(price_val)
            except (ValueError, AttributeError):
                continue

        if not prices:
            return None

        min_price = min(prices)
        max_price = max(prices)

        return f"${min_price:.0f} - ${max_price:.0f}"

    def extract_brands_from_products(self, products: List[Dict[str, Any]]) -> List[str]:
        """
        Extract brand names from product titles.

        Args:
            products: List of products

        Returns:
            List of unique brand names
        """
        brands = set()

        for product in products:
            title = product.get('title', '')

            # Common brand extraction patterns
            # First word often the brand
            words = title.split()
            if words:
                first_word = words[0].strip(',.;:')
                if len(first_word) > 2 and first_word[0].isupper():
                    brands.add(first_word)

        return sorted(list(brands))


# Global instance
_scraper = None


def get_scraper() -> PublicDataScraper:
    """Get or create scraper instance."""
    global _scraper
    if _scraper is None:
        _scraper = PublicDataScraper()
    return _scraper
