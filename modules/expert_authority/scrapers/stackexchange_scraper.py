#!/usr/bin/env python3
"""
Stack Exchange API Scraper - Production Implementation
Scrapes real expert Q&A from Stack Exchange using official REST API
NO SYNTHETIC DATA - 100% real discussions only
"""

import requests
import hashlib
import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import logging

from ..core.config import Config

class StackExchangeScraper:
    """Production Stack Exchange scraper using official REST API"""

    def __init__(self, config: Optional[Config] = None):
        """Initialize Stack Exchange scraper with credentials from config"""
        self.config = config or Config()
        self.config.validate_credentials(tier=2)  # Validate Stack Exchange credentials

        # Get API configuration
        se_config = self.config.get_stack_exchange_config()
        self.api_key = se_config['api_key']

        # API endpoints
        self.base_url = "https://api.stackexchange.com/2.3"

        # Setup logging
        self.logger = logging.getLogger(__name__)

        # Cache directory
        self.cache_dir = Path(__file__).parent.parent / "data" / "cache" / "stackexchange"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 10 requests per second max

    def scrape(
        self,
        query: str,
        sites: List[str],
        limit: int = 100,
        sort: str = "relevance",
        tagged: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Scrape Stack Exchange discussions using official REST API

        Args:
            query: Search query (e.g., "LED lighting")
            sites: List of Stack Exchange sites (e.g., ["diy.stackexchange.com", "electronics.stackexchange.com"])
            limit: Max questions to scrape per site
            sort: Sort method ("relevance", "votes", "creation", "activity")
            tagged: Optional list of tags to filter by

        Returns:
            List of Q&A dictionaries with full metadata
        """
        all_discussions = []

        for site in sites:
            self.logger.info(f"Scraping {site} for '{query}'...")

            try:
                questions = self._search_questions(
                    query=query,
                    site=site,
                    limit=limit,
                    sort=sort,
                    tagged=tagged
                )

                for question in questions:
                    # Get full question details including body
                    question_data = self._get_question_details(question['question_id'], site)

                    # Get answers
                    answers = self._get_answers(question['question_id'], site)

                    # Build discussion object
                    discussion = self._build_discussion(question_data, answers, site)
                    all_discussions.append(discussion)

                self.logger.info(f"✅ Scraped {len([d for d in all_discussions if d['site'] == site])} questions from {site}")

            except Exception as e:
                self.logger.error(f"❌ Error scraping {site}: {e}")
                continue

        self.logger.info(f"🎯 Total scraped: {len(all_discussions)} discussions")
        return all_discussions

    def _search_questions(
        self,
        query: str,
        site: str,
        limit: int,
        sort: str,
        tagged: Optional[List[str]]
    ) -> List[Dict]:
        """Search for questions matching query"""
        self._rate_limit()

        params = {
            "intitle": query,
            "site": site,
            "pagesize": min(limit, 100),  # API max is 100
            "order": "desc",
            "sort": sort,
            "filter": "withbody"  # Include question body
        }

        if self.api_key:
            params["key"] = self.api_key

        if tagged:
            params["tagged"] = ";".join(tagged)

        response = requests.get(f"{self.base_url}/search", params=params)
        response.raise_for_status()

        data = response.json()

        # Log quota info
        if 'quota_remaining' in data:
            self.logger.info(f"📊 API quota remaining: {data['quota_remaining']}")

        return data.get('items', [])

    def _get_question_details(self, question_id: int, site: str) -> Dict:
        """Get full question details"""
        self._rate_limit()

        params = {
            "site": site,
            "filter": "withbody"
        }

        if self.api_key:
            params["key"] = self.api_key

        response = requests.get(f"{self.base_url}/questions/{question_id}", params=params)
        response.raise_for_status()

        data = response.json()
        return data['items'][0] if data['items'] else {}

    def _get_answers(self, question_id: int, site: str, limit: int = 10) -> List[Dict]:
        """Get answers for a question"""
        self._rate_limit()

        params = {
            "site": site,
            "pagesize": limit,
            "order": "desc",
            "sort": "votes",
            "filter": "withbody"
        }

        if self.api_key:
            params["key"] = self.api_key

        response = requests.get(f"{self.base_url}/questions/{question_id}/answers", params=params)
        response.raise_for_status()

        data = response.json()
        return data.get('items', [])

    def _build_discussion(self, question: Dict, answers: List[Dict], site: str) -> Dict:
        """Build discussion object from question and answers"""

        # Generate validation hash
        content = f"{question['question_id']}{question['title']}{question.get('body', '')}{question['creation_date']}"
        validation_hash = hashlib.sha256(content.encode()).hexdigest()

        discussion = {
            "id": str(question['question_id']),
            "platform": "stackexchange",
            "site": site,
            "title": question['title'],
            "url": question['link'],
            "author": question['owner']['display_name'],
            "author_reputation": question['owner'].get('reputation', 0),
            "author_id": question['owner'].get('user_id'),
            "score": question['score'],
            "view_count": question.get('view_count', 0),
            "answer_count": question.get('answer_count', 0),
            "created_utc": question['creation_date'],
            "created_date": datetime.fromtimestamp(question['creation_date']).isoformat(),
            "last_activity_date": datetime.fromtimestamp(question['last_activity_date']).isoformat(),
            "body": question.get('body', ''),
            "body_markdown": question.get('body_markdown', ''),
            "tags": question.get('tags', []),
            "is_answered": question.get('is_answered', False),
            "accepted_answer_id": question.get('accepted_answer_id'),
            "answers": self._format_answers(answers),
            "validation_hash": validation_hash,
            "scraped_at": datetime.now().isoformat(),
            "api_source": "stackexchange_rest_api_official"
        }

        return discussion

    def _format_answers(self, answers: List[Dict]) -> List[Dict]:
        """Format answers with metadata"""
        formatted_answers = []

        for answer in answers:
            formatted_answers.append({
                "id": answer['answer_id'],
                "author": answer['owner']['display_name'],
                "author_reputation": answer['owner'].get('reputation', 0),
                "author_id": answer['owner'].get('user_id'),
                "body": answer.get('body', ''),
                "body_markdown": answer.get('body_markdown', ''),
                "score": answer['score'],
                "is_accepted": answer.get('is_accepted', False),
                "created_utc": answer['creation_date'],
                "created_date": datetime.fromtimestamp(answer['creation_date']).isoformat(),
                "last_activity_date": datetime.fromtimestamp(answer.get('last_activity_date', answer['creation_date'])).isoformat()
            })

        return formatted_answers

    def _rate_limit(self):
        """Enforce rate limiting (10 requests/second max)"""
        now = time.time()
        time_since_last = now - self.last_request_time

        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)

        self.last_request_time = time.time()

    def save_to_cache(self, discussions: List[Dict], filename: str) -> Path:
        """Save scraped discussions to JSON cache"""
        cache_file = self.cache_dir / f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump({
                "metadata": {
                    "scraped_at": datetime.now().isoformat(),
                    "total_discussions": len(discussions),
                    "source": "stackexchange_rest_api_official"
                },
                "discussions": discussions
            }, f, indent=2, ensure_ascii=False)

        self.logger.info(f"💾 Saved {len(discussions)} discussions to {cache_file}")
        return cache_file

    def load_from_cache(self, cache_file: Path) -> List[Dict]:
        """Load discussions from cache file"""
        with open(cache_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.logger.info(f"📂 Loaded {len(data['discussions'])} discussions from cache")
        return data['discussions']

    def validate_url_accessibility(self, url: str) -> bool:
        """Validate that Stack Exchange URL is still accessible"""
        try:
            response = requests.head(url, timeout=5)
            return response.status_code == 200
        except Exception as e:
            self.logger.warning(f"⚠️ URL validation failed for {url}: {e}")
            return False


if __name__ == "__main__":
    # Example usage (requires .env with Stack Exchange API key)
    logging.basicConfig(level=logging.INFO)

    scraper = StackExchangeScraper()

    # Scrape LED lighting discussions
    discussions = scraper.scrape(
        query="LED lighting",
        sites=["diy.stackexchange.com", "electronics.stackexchange.com"],
        limit=30,
        tagged=["led", "lighting"]
    )

    # Save to cache
    scraper.save_to_cache(discussions, "led_lighting_discussions")

    print(f"✅ Scraped {len(discussions)} real Stack Exchange discussions")
    print(f"📊 Example discussion: {discussions[0]['title']}")
    print(f"🔗 URL: {discussions[0]['url']}")
