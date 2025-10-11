"""
Pinterest visual scraper using Playwright for consumer taxonomy analysis.
Captures board images, product details, tags, descriptions, and success factors.
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
from playwright.async_api import async_playwright, Page, Browser
import re

logger = logging.getLogger(__name__)


class PinterestScraper:
    """
    Pinterest visual scraper using Playwright.
    Captures screenshots, extracts metadata, and analyzes product success factors.
    """

    def __init__(self, cache_dir: Path, screenshot_dir: Path, headless: bool = True):
        """
        Initialize Pinterest scraper.

        Args:
            cache_dir: Directory for caching JSON data
            screenshot_dir: Directory for saving screenshots
            headless: Run browser in headless mode
        """
        self.cache_dir = Path(cache_dir)
        self.screenshot_dir = Path(screenshot_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

        logger.info(f"✅ PinterestScraper initialized (headless={headless})")

    async def _init_browser(self):
        """Initialize Playwright browser."""
        if self.browser is None:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(headless=self.headless)
            self.page = await self.browser.new_page()

            # Set realistic viewport
            await self.page.set_viewport_size({"width": 1920, "height": 1080})

            # Set user agent to avoid detection
            await self.page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })

            logger.info("Browser initialized")

    async def search_and_capture(self, query: str, limit: int = 50) -> Dict[str, Any]:
        """
        Search Pinterest and capture visual results.

        Args:
            query: Search query (e.g., "LED strip lighting ideas")
            limit: Maximum number of pins to capture

        Returns:
            Dictionary with pins data and screenshot paths
        """
        await self._init_browser()

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        search_slug = query.replace(' ', '_').lower()

        try:
            # Navigate to Pinterest search
            search_url = f"https://www.pinterest.com/search/pins/?q={query.replace(' ', '%20')}"
            logger.info(f"🔍 Searching Pinterest: '{query}'")

            await self.page.goto(search_url, wait_until='networkidle')
            await asyncio.sleep(3)  # Wait for dynamic content

            # Capture full page screenshot
            full_screenshot_path = self.screenshot_dir / f"search_{search_slug}_{timestamp}_full.png"
            await self.page.screenshot(path=str(full_screenshot_path), full_page=True)
            logger.info(f"📸 Captured full page: {full_screenshot_path.name}")

            # Extract pin data from page
            pins_data = await self.page.evaluate("""
                () => {
                    const pins = [];
                    const pinElements = document.querySelectorAll('[data-test-id="pin"]');

                    pinElements.forEach((pin, index) => {
                        if (index >= 50) return;  // Limit pins

                        const img = pin.querySelector('img');
                        const titleEl = pin.querySelector('[data-test-id="pinTitle"]');
                        const linkEl = pin.querySelector('a[href*="/pin/"]');

                        pins.push({
                            index: index,
                            title: titleEl ? titleEl.textContent.trim() : '',
                            image_url: img ? (img.src || img.dataset.src) : '',
                            pin_url: linkEl ? 'https://pinterest.com' + linkEl.getAttribute('href') : '',
                            alt_text: img ? img.alt : ''
                        });
                    });

                    return pins;
                }
            """)

            logger.info(f"✅ Extracted {len(pins_data)} pins")

            # Scroll and capture sections for taxonomy understanding
            section_screenshots = []
            scroll_positions = [0, 1000, 2000, 3000]

            for i, scroll_y in enumerate(scroll_positions):
                await self.page.evaluate(f"window.scrollTo(0, {scroll_y})")
                await asyncio.sleep(1)

                section_path = self.screenshot_dir / f"search_{search_slug}_{timestamp}_section_{i}.png"
                await self.page.screenshot(path=str(section_path))
                section_screenshots.append(str(section_path))
                logger.debug(f"📸 Captured section {i}")

            # Get related searches (consumer taxonomy indicators)
            related_searches = await self.page.evaluate("""
                () => {
                    const related = [];
                    document.querySelectorAll('[data-test-id="related-search"]').forEach(el => {
                        related.push(el.textContent.trim());
                    });
                    return related;
                }
            """)

            result = {
                'query': query,
                'timestamp': timestamp,
                'pins': pins_data[:limit],
                'related_searches': related_searches,
                'screenshots': {
                    'full_page': str(full_screenshot_path),
                    'sections': section_screenshots
                },
                'visual_taxonomy': {
                    'total_pins_found': len(pins_data),
                    'related_terms': related_searches,
                    'image_urls': [p['image_url'] for p in pins_data[:10]]  # Top 10 for taxonomy
                }
            }

            # Save JSON data
            cache_file = self.cache_dir / f"search_{search_slug}_{timestamp}.json"
            with open(cache_file, 'w') as f:
                json.dump(result, f, indent=2)

            logger.info(f"✅ Pinterest search complete: {len(pins_data)} pins, {len(related_searches)} related terms")
            return result

        except Exception as e:
            logger.error(f"❌ Pinterest search failed: {e}")
            return {'error': str(e), 'query': query}

    async def analyze_pin_details(self, pin_url: str) -> Dict[str, Any]:
        """
        Deep dive into individual pin for product analysis.

        Args:
            pin_url: Pinterest pin URL

        Returns:
            Detailed pin analysis with comments, tags, product info
        """
        await self._init_browser()

        pin_id = re.search(r'/pin/(\d+)', pin_url).group(1) if re.search(r'/pin/(\d+)', pin_url) else 'unknown'
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        try:
            logger.info(f"📥 Analyzing pin: {pin_id}")

            await self.page.goto(pin_url, wait_until='networkidle')
            await asyncio.sleep(2)

            # Capture pin screenshot
            screenshot_path = self.screenshot_dir / f"pin_{pin_id}_{timestamp}.png"
            await self.page.screenshot(path=str(screenshot_path), full_page=True)

            # Extract comprehensive pin data
            pin_data = await self.page.evaluate("""
                () => {
                    const data = {};

                    // Title and description
                    const titleEl = document.querySelector('[data-test-id="pin-title"]');
                    const descEl = document.querySelector('[data-test-id="pin-description"]');
                    data.title = titleEl ? titleEl.textContent.trim() : '';
                    data.description = descEl ? descEl.textContent.trim() : '';

                    // Board and creator
                    const boardEl = document.querySelector('[data-test-id="board-name"]');
                    const creatorEl = document.querySelector('[data-test-id="creator-profile-name"]');
                    data.board_name = boardEl ? boardEl.textContent.trim() : '';
                    data.creator_name = creatorEl ? creatorEl.textContent.trim() : '';

                    // Engagement metrics
                    const saveCountEl = document.querySelector('[data-test-id="pin-save-count"]');
                    data.save_count = saveCountEl ? saveCountEl.textContent.trim() : '0';

                    // Tags/categories
                    const tags = [];
                    document.querySelectorAll('[data-test-id="pin-tag"]').forEach(tag => {
                        tags.push(tag.textContent.trim());
                    });
                    data.tags = tags;

                    // Comments (job/pain point indicators)
                    const comments = [];
                    document.querySelectorAll('[data-test-id="comment-text"]').forEach(comment => {
                        comments.push({
                            text: comment.textContent.trim(),
                            timestamp: comment.closest('[data-test-id="comment"]')?.querySelector('[data-test-id="comment-timestamp"]')?.textContent.trim() || ''
                        });
                    });
                    data.comments = comments;

                    // Product link (if exists)
                    const productLink = document.querySelector('[data-test-id="pin-product-link"]');
                    data.product_url = productLink ? productLink.href : '';

                    // Main image
                    const mainImg = document.querySelector('[data-test-id="pin-closeup-image"]');
                    data.image_url = mainImg ? mainImg.src : '';

                    return data;
                }
            """)

            # Scroll to load more comments
            await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(1)

            # Get additional loaded comments
            additional_comments = await self.page.evaluate("""
                () => {
                    const comments = [];
                    document.querySelectorAll('[data-test-id="comment-text"]').forEach(comment => {
                        comments.push({
                            text: comment.textContent.trim()
                        });
                    });
                    return comments;
                }
            """)

            pin_data['all_comments'] = additional_comments

            result = {
                'pin_id': pin_id,
                'pin_url': pin_url,
                'timestamp': timestamp,
                'screenshot': str(screenshot_path),
                'data': pin_data,
                'success_indicators': {
                    'save_count': pin_data.get('save_count', '0'),
                    'comment_count': len(additional_comments),
                    'has_product_link': bool(pin_data.get('product_url')),
                    'tag_count': len(pin_data.get('tags', []))
                },
                'job_indicators': {
                    'tags': pin_data.get('tags', []),
                    'description_keywords': self._extract_keywords(pin_data.get('description', '')),
                    'comment_themes': self._analyze_comment_themes(additional_comments)
                }
            }

            # Save JSON
            cache_file = self.cache_dir / f"pin_{pin_id}_{timestamp}.json"
            with open(cache_file, 'w') as f:
                json.dump(result, f, indent=2)

            logger.info(f"✅ Pin analysis complete: {pin_data.get('save_count', 0)} saves, {len(additional_comments)} comments")
            return result

        except Exception as e:
            logger.error(f"❌ Pin analysis failed: {e}")
            return {'error': str(e), 'pin_url': pin_url}

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract potential job/pain point keywords from text."""
        # Common lighting-related pain points and jobs
        keywords = []
        pain_point_patterns = [
            r'too dark', r'not enough light', r'dim', r'bright', r'harsh',
            r'warm', r'cool', r'ambiance', r'mood', r'task', r'accent',
            r'energy', r'save', r'cheap', r'expensive', r'easy', r'difficult',
            r'install', r'setup', r'DIY', r'professional'
        ]

        text_lower = text.lower()
        for pattern in pain_point_patterns:
            if re.search(pattern, text_lower):
                keywords.append(pattern.replace(r'\b', ''))

        return list(set(keywords))

    def _analyze_comment_themes(self, comments: List[Dict]) -> Dict[str, List[str]]:
        """Categorize comments into themes (questions, praise, concerns)."""
        themes = {
            'questions': [],
            'praise': [],
            'concerns': [],
            'how_to': []
        }

        for comment in comments:
            text = comment.get('text', '').lower()

            if '?' in text or text.startswith(('how', 'what', 'where', 'when', 'why')):
                themes['questions'].append(comment.get('text', ''))
            elif any(word in text for word in ['love', 'great', 'amazing', 'perfect', 'beautiful']):
                themes['praise'].append(comment.get('text', ''))
            elif any(word in text for word in ['but', 'however', 'issue', 'problem', 'concern']):
                themes['concerns'].append(comment.get('text', ''))
            elif any(word in text for word in ['how to', 'tutorial', 'diy', 'install']):
                themes['how_to'].append(comment.get('text', ''))

        return themes

    async def analyze_board(self, board_url: str) -> Dict[str, Any]:
        """
        Analyze entire Pinterest board for trend patterns.

        Args:
            board_url: Pinterest board URL

        Returns:
            Board analysis with visual taxonomy
        """
        await self._init_browser()

        board_id = re.search(r'/([^/]+)/([^/]+)/$', board_url)
        board_slug = f"{board_id.group(1)}_{board_id.group(2)}" if board_id else 'unknown'
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        try:
            logger.info(f"📥 Analyzing board: {board_slug}")

            await self.page.goto(board_url, wait_until='networkidle')
            await asyncio.sleep(2)

            # Capture board overview
            screenshot_path = self.screenshot_dir / f"board_{board_slug}_{timestamp}.png"
            await self.page.screenshot(path=str(screenshot_path), full_page=True)

            # Extract board metadata
            board_data = await self.page.evaluate("""
                () => {
                    const data = {};

                    // Board title and description
                    const titleEl = document.querySelector('[data-test-id="board-name"]');
                    const descEl = document.querySelector('[data-test-id="board-description"]');
                    data.title = titleEl ? titleEl.textContent.trim() : '';
                    data.description = descEl ? descEl.textContent.trim() : '';

                    // Pin count
                    const pinCountEl = document.querySelector('[data-test-id="board-pin-count"]');
                    data.pin_count = pinCountEl ? pinCountEl.textContent.trim() : '0';

                    // Extract all visible pins for taxonomy
                    const pins = [];
                    document.querySelectorAll('[data-test-id="pin"]').forEach((pin, idx) => {
                        const img = pin.querySelector('img');
                        const titleEl = pin.querySelector('[data-test-id="pinTitle"]');

                        pins.push({
                            title: titleEl ? titleEl.textContent.trim() : '',
                            image_url: img ? (img.src || img.dataset.src) : '',
                            alt_text: img ? img.alt : ''
                        });
                    });
                    data.pins = pins;

                    return data;
                }
            """)

            result = {
                'board_url': board_url,
                'board_slug': board_slug,
                'timestamp': timestamp,
                'screenshot': str(screenshot_path),
                'data': board_data,
                'visual_taxonomy': {
                    'total_pins': board_data.get('pin_count', '0'),
                    'sample_pins': len(board_data.get('pins', [])),
                    'common_themes': self._extract_keywords(board_data.get('description', '')),
                    'image_urls': [p['image_url'] for p in board_data.get('pins', [])[:20]]
                }
            }

            # Save JSON
            cache_file = self.cache_dir / f"board_{board_slug}_{timestamp}.json"
            with open(cache_file, 'w') as f:
                json.dump(result, f, indent=2)

            logger.info(f"✅ Board analysis complete: {board_data.get('pin_count', 0)} pins")
            return result

        except Exception as e:
            logger.error(f"❌ Board analysis failed: {e}")
            return {'error': str(e), 'board_url': board_url}

    async def close(self):
        """Close browser."""
        if self.browser:
            await self.browser.close()
            logger.info("Browser closed")


# Synchronous wrapper functions
def sync_search_and_capture(cache_dir: Path, screenshot_dir: Path, query: str, limit: int = 50) -> Dict:
    """Synchronous wrapper for search_and_capture."""
    scraper = PinterestScraper(cache_dir, screenshot_dir)
    try:
        return asyncio.run(scraper.search_and_capture(query, limit))
    finally:
        asyncio.run(scraper.close())


def sync_analyze_pin(cache_dir: Path, screenshot_dir: Path, pin_url: str) -> Dict:
    """Synchronous wrapper for analyze_pin_details."""
    scraper = PinterestScraper(cache_dir, screenshot_dir)
    try:
        return asyncio.run(scraper.analyze_pin_details(pin_url))
    finally:
        asyncio.run(scraper.close())


if __name__ == "__main__":
    # Test Pinterest scraper
    async def test():
        cache = Path("data/cache/pinterest")
        screenshots = Path("data/screenshots/pinterest")

        scraper = PinterestScraper(cache, screenshots, headless=False)

        # Test search
        result = await scraper.search_and_capture("LED strip lighting ideas", limit=20)
        print(f"Search results: {len(result.get('pins', []))} pins")
        print(f"Related searches: {result.get('related_searches', [])}")

        # Test pin analysis if we got results
        if result.get('pins') and len(result['pins']) > 0:
            pin_url = result['pins'][0]['pin_url']
            if pin_url:
                pin_analysis = await scraper.analyze_pin_details(pin_url)
                print(f"Pin analysis: {pin_analysis.get('success_indicators')}")

        await scraper.close()

    asyncio.run(test())
