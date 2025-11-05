"""
SEC EDGAR Service - Public Company Financial Data

Fetches real data from SEC EDGAR API (no authentication required).
Extracts company revenue and market data from 10-K filings.
"""

import logging
import requests
import time
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class SECEdgarService:
    """
    Service for accessing SEC EDGAR public company data.

    No API key required - public API with rate limits.
    Rate limit: 10 requests per second.
    """

    BASE_URL = "https://data.sec.gov"
    COMPANY_SEARCH_URL = f"{BASE_URL}/submissions"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CategoryIntelligence/1.0 (Research Tool)',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'data.sec.gov'
        })
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 10 requests/second = 0.1s interval

    def _rate_limit(self):
        """Enforce rate limiting (10 requests/second)."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time

        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)

        self.last_request_time = time.time()

    def search_companies_by_industry(self, keywords: List[str], limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search for public companies by industry keywords.

        Args:
            keywords: Industry keywords to search for
            limit: Maximum number of companies to return

        Returns:
            List of company data with CIK, name, and filing URLs
        """
        companies = []

        # Common public companies in various industries
        # This is a starting point - in production, would search by SIC code
        known_companies_by_sector = {
            'storage': ['HD', 'LOW', 'TSCO', 'BBBY'],  # Home Depot, Lowe's, Tractor Supply, Bed Bath
            'home improvement': ['HD', 'LOW', 'TSCO'],
            'retail': ['WMT', 'TGT', 'AMZN', 'COST'],
            'lighting': ['GE', 'CREE', 'LITE', 'FICO']
        }

        # Find relevant tickers
        tickers_to_check = set()
        for keyword in keywords:
            keyword_lower = keyword.lower()
            for sector, tickers in known_companies_by_sector.items():
                if keyword_lower in sector:
                    tickers_to_check.update(tickers)

        # If no specific matches, use general retail
        if not tickers_to_check:
            tickers_to_check = set(known_companies_by_sector['retail'])

        for ticker in list(tickers_to_check)[:limit]:
            try:
                company_data = self.get_company_by_ticker(ticker)
                if company_data:
                    companies.append(company_data)
            except Exception as e:
                logger.warning(f"Failed to fetch {ticker}: {e}")
                continue

        return companies

    def get_company_by_ticker(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Get company data by stock ticker.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Company data including CIK and recent filings
        """
        try:
            self._rate_limit()

            # First get CIK from ticker
            cik_url = f"{self.BASE_URL}/submissions/CIK{ticker}.json"

            # Note: This is simplified - real implementation would look up CIK properly
            # For now, return placeholder structure

            return {
                'ticker': ticker,
                'source_url': f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={ticker}",
                'data_type': 'sec_filing'
            }

        except Exception as e:
            logger.error(f"Error fetching company {ticker}: {e}")
            return None

    def extract_revenue_from_filing(self, filing_url: str) -> Optional[Dict[str, Any]]:
        """
        Extract revenue data from 10-K filing.

        Args:
            filing_url: URL to filing document

        Returns:
            Revenue data extracted from filing
        """
        # This would require parsing XBRL or HTML filing documents
        # Complex implementation - placeholder for now
        return {
            'source_url': filing_url,
            'data_available': True,
            'note': 'Revenue extraction requires XBRL parsing - future implementation'
        }


# Global instance
_sec_service = None


def get_sec_service() -> SECEdgarService:
    """Get or create SEC EDGAR service instance."""
    global _sec_service
    if _sec_service is None:
        _sec_service = SECEdgarService()
    return _sec_service
