"""
PatentsView API Client
Free, unlimited access to USPTO patent data
No API key required
"""

import requests
import json
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class PatentsViewClient:
    """Client for USPTO PatentsView API"""

    BASE_URL = "https://api.patentsview.org/patents/query"
    RATE_LIMIT_DELAY = 1.5  # Seconds between requests (45/min = 1.33s, use 1.5s to be safe)

    def __init__(self):
        self.session = requests.Session()
        self.last_request_time = 0

    def _rate_limit(self):
        """Enforce rate limiting (45 requests/minute)"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.RATE_LIMIT_DELAY:
            time.sleep(self.RATE_LIMIT_DELAY - elapsed)
        self.last_request_time = time.time()

    def search_patents(
        self,
        keyword: str,
        start_date: str = None,
        max_results: int = 100,
        page: int = 1
    ) -> Dict:
        """
        Search patents by keyword with validation

        Args:
            keyword: Search term (searches in title + abstract)
            start_date: Filter patents from this date (YYYY-MM-DD)
            max_results: Number of results per page (max 100)
            page: Page number for pagination

        Returns:
            Dict with 'patents' list and 'metadata' dict
        """
        self._rate_limit()

        # Default to patents from last 2 years if no date specified
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d")

        # Build query
        query = {
            "q": {
                "_and": [
                    {
                        "_text_any": {
                            "patent_abstract": keyword
                        }
                    },
                    {
                        "_gte": {
                            "patent_date": start_date
                        }
                    }
                ]
            },
            "f": [
                "patent_number",
                "patent_title",
                "patent_abstract",
                "patent_date",
                "app_date",
                "patent_type",
                "patent_kind",
                "assignee_organization",
                "assignee_first_name",
                "assignee_last_name",
                "inventor_first_name",
                "inventor_last_name",
                "cpc_subgroup_id",
                "cpc_subgroup_title",
                "ipc_subclass",
                "cited_patent_number",
                "citedby_patent_number"
            ],
            "o": {
                "page": page,
                "per_page": min(max_results, 100)  # API max is 100
            }
        }

        try:
            response = self.session.post(
                self.BASE_URL,
                json=query,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()

            # Validate response structure
            if 'patents' not in data:
                print(f"⚠️ Unexpected API response: {data.keys()}")
                return {'patents': [], 'metadata': {'total': 0, 'error': 'Invalid response'}}

            patents = data.get('patents', [])
            total_count = data.get('count', 0)

            print(f"📊 Found {len(patents)} patents (total: {total_count})")

            # Parse patents
            parsed_patents = []
            for patent in patents:
                parsed = self._parse_patent(patent)
                if parsed:
                    parsed_patents.append(parsed)

            return {
                'patents': parsed_patents,
                'metadata': {
                    'total': total_count,
                    'page': page,
                    'per_page': max_results,
                    'query': keyword,
                    'start_date': start_date
                }
            }

        except requests.exceptions.RequestException as e:
            print(f"❌ API Request failed: {e}")
            return {'patents': [], 'metadata': {'error': str(e)}}

    def _parse_patent(self, raw_data: Dict) -> Optional[Dict]:
        """Parse raw API response into standardized format"""

        try:
            patent_number = raw_data.get('patent_number')
            if not patent_number:
                return None

            # Assignees (companies)
            assignees = []
            assignee_orgs = raw_data.get('assignees', [])
            for assignee in assignee_orgs:
                org = assignee.get('assignee_organization')
                if org:
                    assignees.append(org)
                else:
                    # Individual assignee
                    first = assignee.get('assignee_first_name', '')
                    last = assignee.get('assignee_last_name', '')
                    if first or last:
                        assignees.append(f"{first} {last}".strip())

            # Inventors
            inventors = []
            inventor_list = raw_data.get('inventors', [])
            for inventor in inventor_list:
                first = inventor.get('inventor_first_name', '')
                last = inventor.get('inventor_last_name', '')
                if first or last:
                    inventors.append(f"{first} {last}".strip())

            # CPC codes (patent classification)
            cpc_codes = []
            cpc_list = raw_data.get('cpcs', [])
            for cpc in cpc_list:
                code = cpc.get('cpc_subgroup_id')
                if code:
                    cpc_codes.append(code)

            # IPC codes
            ipc_codes = []
            ipc_list = raw_data.get('ipcs', [])
            for ipc in ipc_list:
                code = ipc.get('ipc_subclass')
                if code:
                    ipc_codes.append(code)

            # Citations
            backward_citations = []
            cited_list = raw_data.get('cited_patents', [])
            for cited in cited_list:
                num = cited.get('cited_patent_number')
                if num:
                    backward_citations.append(num)

            forward_citations = []
            citedby_list = raw_data.get('citedby_patents', [])
            for citedby in citedby_list:
                num = citedby.get('citedby_patent_number')
                if num:
                    forward_citations.append(num)

            patent = {
                'id': f"US-{patent_number}",
                'title': raw_data.get('patent_title', '').strip(),
                'abstract': raw_data.get('patent_abstract', '').strip(),
                'filing_date': raw_data.get('app_date'),
                'grant_date': raw_data.get('patent_date'),
                'api_source': 'patentsview',
                'cpc_codes': list(set(cpc_codes)),  # Remove duplicates
                'ipc_codes': list(set(ipc_codes)),
                'inventors': list(set(inventors)),
                'assignees': list(set(assignees)),
                'claims_text': None,  # Not available in PatentsView API
                'description_text': None,  # Not available
                'backward_citations': backward_citations,
                'forward_citations': forward_citations
            }

            return patent

        except Exception as e:
            print(f"⚠️ Failed to parse patent: {e}")
            return None

    def validate_data_quality(self, patents: List[Dict]) -> Dict:
        """
        Validate data quality of collected patents
        Returns statistics about data completeness
        """
        if not patents:
            return {'error': 'No patents to validate'}

        total = len(patents)
        has_title = sum(1 for p in patents if p.get('title'))
        has_abstract = sum(1 for p in patents if p.get('abstract'))
        has_assignees = sum(1 for p in patents if p.get('assignees'))
        has_cpc_codes = sum(1 for p in patents if p.get('cpc_codes'))
        has_filing_date = sum(1 for p in patents if p.get('filing_date'))

        return {
            'total_patents': total,
            'has_title': has_title,
            'has_abstract': has_abstract,
            'has_assignees': has_assignees,
            'has_cpc_codes': has_cpc_codes,
            'has_filing_date': has_filing_date,
            'title_pct': round((has_title / total * 100), 1),
            'abstract_pct': round((has_abstract / total * 100), 1),
            'assignees_pct': round((has_assignees / total * 100), 1),
            'cpc_codes_pct': round((has_cpc_codes / total * 100), 1),
            'filing_date_pct': round((has_filing_date / total * 100), 1),
            'quality_score': round((
                (has_title + has_abstract + has_assignees + has_cpc_codes + has_filing_date) /
                (total * 5) * 100
            ), 1)
        }
