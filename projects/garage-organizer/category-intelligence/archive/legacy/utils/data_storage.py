"""
Simple, robust data storage utility
Saves all collected intelligence to organized data/storage directory
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class DataStorage:
    """
    Simple storage manager for category intelligence data

    Philosophy: Keep it simple and robust
    - One file per data point
    - Clear naming conventions
    - No complex databases
    - Easy to inspect and analyze
    """

    def __init__(self, category_dir: Path):
        """
        Initialize storage for a specific category

        Args:
            category_dir: Root directory for this category's data
        """
        self.category_dir = Path(category_dir)
        self.sources_dir = self.category_dir / "sources"
        self.structured_dir = self.category_dir / "structured"
        self.audit_dir = self.category_dir / "audit"

        # Ensure directories exist
        for dir_path in [self.sources_dir, self.structured_dir, self.audit_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    def save_source(
        self,
        content: str,
        url: str,
        content_type: str = "html"
    ) -> Path:
        """
        Save raw source content

        Args:
            content: Raw HTML/JSON/text content
            url: Source URL
            content_type: File extension (html, json, txt)

        Returns:
            Path to saved file
        """
        # Create unique filename from URL hash
        url_hash = hashlib.md5(url.encode()).hexdigest()[:12]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{url_hash}.{content_type}"

        filepath = self.sources_dir / filename

        try:
            filepath.write_text(content, encoding='utf-8')

            # Save metadata
            meta_path = filepath.with_suffix(f'.{content_type}.meta.json')
            meta_path.write_text(json.dumps({
                'url': url,
                'saved_at': timestamp,
                'size_bytes': len(content),
                'hash': url_hash
            }, indent=2))

            logger.info(f"Saved source: {filename}")
            return filepath

        except Exception as e:
            logger.error(f"Failed to save source {url}: {e}")
            return None

    def save_structured_data(
        self,
        data: Dict[str, Any],
        data_type: str,
        identifier: Optional[str] = None
    ) -> Path:
        """
        Save structured JSON data

        Args:
            data: Dictionary to save
            data_type: Type of data (brands, pricing, taxonomy, etc.)
            identifier: Optional unique identifier

        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if identifier:
            filename = f"{data_type}_{identifier}_{timestamp}.json"
        else:
            filename = f"{data_type}_{timestamp}.json"

        filepath = self.structured_dir / filename

        try:
            # Add metadata
            data_with_meta = {
                '_metadata': {
                    'saved_at': timestamp,
                    'data_type': data_type,
                    'identifier': identifier
                },
                'data': data
            }

            filepath.write_text(
                json.dumps(data_with_meta, indent=2, default=str),
                encoding='utf-8'
            )

            logger.info(f"Saved structured data: {filename}")
            return filepath

        except Exception as e:
            logger.error(f"Failed to save structured data {data_type}: {e}")
            return None

    def save_brands(self, brands: list) -> Path:
        """Save brand discovery results"""
        return self.save_structured_data(
            {'brands': brands, 'count': len(brands)},
            'brands'
        )

    def save_taxonomy(self, taxonomy: dict) -> Path:
        """Save product taxonomy"""
        return self.save_structured_data(taxonomy, 'taxonomy')

    def save_pricing(self, pricing_data: list) -> Path:
        """Save pricing analysis"""
        return self.save_structured_data(
            {'prices': pricing_data, 'count': len(pricing_data)},
            'pricing'
        )

    def save_market_share(self, market_share_data: dict) -> Path:
        """Save market share estimates"""
        return self.save_structured_data(market_share_data, 'market_share')

    def save_market_size(self, market_size_data: dict) -> Path:
        """Save market size analysis"""
        return self.save_structured_data(market_size_data, 'market_size')

    def save_audit_log(self, log_data: Dict[str, Any]) -> Path:
        """
        Save audit log entry

        Args:
            log_data: Audit information

        Returns:
            Path to saved log
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"audit_{timestamp}.json"
        filepath = self.audit_dir / filename

        try:
            log_with_timestamp = {
                'timestamp': timestamp,
                **log_data
            }

            filepath.write_text(
                json.dumps(log_with_timestamp, indent=2, default=str),
                encoding='utf-8'
            )

            logger.info(f"Saved audit log: {filename}")
            return filepath

        except Exception as e:
            logger.error(f"Failed to save audit log: {e}")
            return None

    def get_latest_file(self, data_type: str) -> Optional[Path]:
        """
        Get most recent file of given type

        Args:
            data_type: Type to search for (brands, pricing, etc.)

        Returns:
            Path to most recent file or None
        """
        pattern = f"{data_type}_*.json"
        files = sorted(
            self.structured_dir.glob(pattern),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )

        return files[0] if files else None

    def load_structured_data(self, filepath: Path) -> Optional[Dict]:
        """
        Load structured data from file

        Args:
            filepath: Path to JSON file

        Returns:
            Loaded data or None
        """
        try:
            content = filepath.read_text(encoding='utf-8')
            return json.loads(content)
        except Exception as e:
            logger.error(f"Failed to load {filepath}: {e}")
            return None

    def list_sources(self) -> list:
        """List all saved source files"""
        return sorted(self.sources_dir.glob("*.*"), key=lambda p: p.stat().st_mtime)

    def list_structured_files(self, data_type: Optional[str] = None) -> list:
        """
        List structured data files

        Args:
            data_type: Filter by type (brands, pricing, etc.) or None for all

        Returns:
            List of file paths sorted by modification time
        """
        if data_type:
            pattern = f"{data_type}_*.json"
        else:
            pattern = "*.json"

        return sorted(
            self.structured_dir.glob(pattern),
            key=lambda p: p.stat().st_mtime
        )

    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics"""
        return {
            'sources_count': len(list(self.sources_dir.glob("*.*"))),
            'structured_count': len(list(self.structured_dir.glob("*.json"))),
            'audit_logs_count': len(list(self.audit_dir.glob("*.json"))),
            'total_size_mb': sum(
                f.stat().st_size for f in self.category_dir.rglob("*") if f.is_file()
            ) / (1024 * 1024)
        }

    def __repr__(self) -> str:
        stats = self.get_storage_stats()
        return (
            f"<DataStorage category={self.category_dir.name} "
            f"sources={stats['sources_count']} "
            f"structured={stats['structured_count']} "
            f"size={stats['total_size_mb']:.2f}MB>"
        )
