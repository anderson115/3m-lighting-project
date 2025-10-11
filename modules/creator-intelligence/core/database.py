"""
SQLite database management for Creator Intelligence Module.
Handles creator profiles, content, and consumer language storage.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)


class CreatorDatabase:
    """SQLite database manager for creator intelligence data."""

    def __init__(self, db_path: str | Path):
        """
        Initialize database connection and create tables if needed.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Enable column access by name
        self._create_tables()
        logger.info(f"✅ Database initialized at {self.db_path}")

    def _create_tables(self):
        """Create database tables if they don't exist."""
        cursor = self.conn.cursor()

        # Creators table - stores creator profiles and viability scores
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS creators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                username TEXT NOT NULL,
                display_name TEXT,
                profile_url TEXT,
                follower_count INTEGER,
                engagement_rate REAL,
                content_count INTEGER,
                location TEXT,
                bio TEXT,
                category TEXT,
                research_viability_score INTEGER,  -- 0-100 score for research potential
                partnership_viability_score INTEGER,  -- 0-100 score for partnership potential
                classification TEXT,  -- 'highly_relevant', 'relevant', 'tangentially_relevant', 'not_relevant'
                last_scraped_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT,  -- JSON field for platform-specific data
                UNIQUE(platform, username)
            )
        """)

        # Creator content table - stores individual posts/videos/products
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS creator_content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                creator_id INTEGER NOT NULL,
                platform TEXT NOT NULL,
                content_id TEXT NOT NULL,  -- Platform-specific content ID
                content_type TEXT,  -- 'video', 'post', 'product', 'reel'
                title TEXT,
                description TEXT,
                url TEXT,
                view_count INTEGER,
                like_count INTEGER,
                comment_count INTEGER,
                published_at TIMESTAMP,
                classification TEXT,  -- 'highly_relevant', 'relevant', 'tangentially_relevant', 'not_relevant'
                pain_points TEXT,  -- JSON array of detected pain points
                consumer_language TEXT,  -- JSON array of consumer language phrases
                relevance_score REAL,  -- 0-1 relevance to lighting industry
                relevance_reasoning TEXT,  -- LLM reasoning for classification
                lighting_topics TEXT,  -- JSON array of lighting topics mentioned
                job_to_be_done TEXT,  -- Job the content helps with
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT,  -- JSON field for additional data
                FOREIGN KEY (creator_id) REFERENCES creators(id),
                UNIQUE(platform, content_id)
            )
        """)

        # Consumer language dictionary - aggregated language patterns
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consumer_language (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phrase TEXT NOT NULL UNIQUE,
                category TEXT,  -- 'pain_point', 'desire', 'feature_request', 'complaint', 'praise'
                context TEXT,  -- Original context where phrase appeared
                frequency INTEGER DEFAULT 1,
                platforms TEXT,  -- JSON array of platforms where phrase appears
                first_seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT  -- JSON field for additional analysis
            )
        """)

        # Create indexes for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_creators_platform ON creators(platform)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_creators_classification ON creators(classification)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_creators_research_score ON creators(research_viability_score DESC)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_creators_partnership_score ON creators(partnership_viability_score DESC)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_content_creator ON creator_content(creator_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_content_platform ON creator_content(platform)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_language_category ON consumer_language(category)")

        self.conn.commit()
        logger.info("✅ Database tables created/verified")

    def upsert_creator(self, creator_data: Dict[str, Any]) -> int:
        """
        Insert or update a creator profile.

        Args:
            creator_data: Dictionary with creator information

        Returns:
            Creator ID
        """
        cursor = self.conn.cursor()

        # Convert metadata dict to JSON string if present
        if 'metadata' in creator_data and isinstance(creator_data['metadata'], dict):
            creator_data['metadata'] = json.dumps(creator_data['metadata'])

        # Update timestamp
        creator_data['updated_at'] = datetime.now().isoformat()

        # Check if creator exists
        cursor.execute(
            "SELECT id FROM creators WHERE platform = ? AND username = ?",
            (creator_data['platform'], creator_data['username'])
        )
        existing = cursor.fetchone()

        if existing:
            # Update existing creator
            creator_id = existing[0]
            set_clause = ", ".join([f"{k} = ?" for k in creator_data.keys() if k != 'platform' and k != 'username'])
            values = [v for k, v in creator_data.items() if k != 'platform' and k != 'username']
            values.extend([creator_data['platform'], creator_data['username']])

            cursor.execute(
                f"UPDATE creators SET {set_clause} WHERE platform = ? AND username = ?",
                values
            )
            logger.debug(f"Updated creator: {creator_data['platform']}/{creator_data['username']}")
        else:
            # Insert new creator
            columns = ", ".join(creator_data.keys())
            placeholders = ", ".join(["?" for _ in creator_data])
            cursor.execute(
                f"INSERT INTO creators ({columns}) VALUES ({placeholders})",
                list(creator_data.values())
            )
            creator_id = cursor.lastrowid
            logger.debug(f"Inserted creator: {creator_data['platform']}/{creator_data['username']} (ID: {creator_id})")

        self.conn.commit()
        return creator_id

    def upsert_content(self, content_data: Dict[str, Any]) -> int:
        """
        Insert or update creator content.

        Args:
            content_data: Dictionary with content information

        Returns:
            Content ID
        """
        cursor = self.conn.cursor()

        # Convert JSON fields to strings
        for field in ['pain_points', 'consumer_language', 'lighting_topics', 'metadata']:
            if field in content_data and isinstance(content_data[field], (list, dict)):
                content_data[field] = json.dumps(content_data[field])

        # Check if content exists
        cursor.execute(
            "SELECT id FROM creator_content WHERE platform = ? AND content_id = ?",
            (content_data['platform'], content_data['content_id'])
        )
        existing = cursor.fetchone()

        if existing:
            # Update existing content
            content_id = existing[0]
            set_clause = ", ".join([f"{k} = ?" for k in content_data.keys() if k != 'platform' and k != 'content_id'])
            values = [v for k, v in content_data.items() if k != 'platform' and k != 'content_id']
            values.extend([content_data['platform'], content_data['content_id']])

            cursor.execute(
                f"UPDATE creator_content SET {set_clause} WHERE platform = ? AND content_id = ?",
                values
            )
        else:
            # Insert new content
            columns = ", ".join(content_data.keys())
            placeholders = ", ".join(["?" for _ in content_data])
            cursor.execute(
                f"INSERT INTO creator_content ({columns}) VALUES ({placeholders})",
                list(content_data.values())
            )
            content_id = cursor.lastrowid

        self.conn.commit()
        return content_id

    def add_consumer_language(self, phrase: str, category: str, platform: str, context: str = ""):
        """
        Add or update consumer language phrase.

        Args:
            phrase: Consumer language phrase
            category: Category (pain_point, desire, etc.)
            platform: Platform where phrase appeared
            context: Original context
        """
        cursor = self.conn.cursor()

        # Check if phrase exists
        cursor.execute("SELECT id, platforms, frequency FROM consumer_language WHERE phrase = ?", (phrase,))
        existing = cursor.fetchone()

        if existing:
            # Update existing phrase
            phrase_id, platforms_json, frequency = existing
            platforms = json.loads(platforms_json) if platforms_json else []
            if platform not in platforms:
                platforms.append(platform)

            cursor.execute("""
                UPDATE consumer_language
                SET frequency = frequency + 1,
                    platforms = ?,
                    last_seen_at = ?
                WHERE id = ?
            """, (json.dumps(platforms), datetime.now().isoformat(), phrase_id))
        else:
            # Insert new phrase
            cursor.execute("""
                INSERT INTO consumer_language (phrase, category, context, platforms)
                VALUES (?, ?, ?, ?)
            """, (phrase, category, context, json.dumps([platform])))

        self.conn.commit()

    def get_creators_by_score(self, score_type: str = 'research', min_score: int = 0, limit: int = 100) -> List[Dict]:
        """
        Get creators ranked by viability score.

        Args:
            score_type: 'research' or 'partnership'
            min_score: Minimum score threshold (0-100)
            limit: Maximum number of results

        Returns:
            List of creator dictionaries
        """
        score_column = f"{score_type}_viability_score"
        cursor = self.conn.cursor()

        cursor.execute(f"""
            SELECT * FROM creators
            WHERE {score_column} >= ?
            ORDER BY {score_column} DESC
            LIMIT ?
        """, (min_score, limit))

        return [dict(row) for row in cursor.fetchall()]

    def get_consumer_language_by_category(self, category: str = None, min_frequency: int = 1) -> List[Dict]:
        """
        Get consumer language phrases.

        Args:
            category: Filter by category (None for all)
            min_frequency: Minimum frequency threshold

        Returns:
            List of phrase dictionaries
        """
        cursor = self.conn.cursor()

        if category:
            cursor.execute("""
                SELECT * FROM consumer_language
                WHERE category = ? AND frequency >= ?
                ORDER BY frequency DESC
            """, (category, min_frequency))
        else:
            cursor.execute("""
                SELECT * FROM consumer_language
                WHERE frequency >= ?
                ORDER BY frequency DESC
            """, (min_frequency,))

        return [dict(row) for row in cursor.fetchall()]

    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        cursor = self.conn.cursor()

        stats = {}

        # Count creators by platform
        cursor.execute("SELECT platform, COUNT(*) as count FROM creators GROUP BY platform")
        stats['creators_by_platform'] = {row[0]: row[1] for row in cursor.fetchall()}

        # Count content by platform
        cursor.execute("SELECT platform, COUNT(*) as count FROM creator_content GROUP BY platform")
        stats['content_by_platform'] = {row[0]: row[1] for row in cursor.fetchall()}

        # Count language phrases
        cursor.execute("SELECT COUNT(*) FROM consumer_language")
        stats['total_language_phrases'] = cursor.fetchone()[0]

        # Classification breakdown
        cursor.execute("SELECT classification, COUNT(*) as count FROM creators WHERE classification IS NOT NULL GROUP BY classification")
        stats['classification_breakdown'] = {row[0]: row[1] for row in cursor.fetchall()}

        return stats

    def close(self):
        """Close database connection."""
        self.conn.close()
        logger.info("Database connection closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


if __name__ == "__main__":
    # Test database operations
    from creator_intelligence.core.config import config

    with CreatorDatabase(config.database_path) as db:
        # Test creator insertion
        test_creator = {
            'platform': 'youtube',
            'username': 'testcreator',
            'display_name': 'Test Creator',
            'follower_count': 10000,
            'research_viability_score': 75,
            'partnership_viability_score': 85,
            'metadata': {'test': True}
        }
        creator_id = db.upsert_creator(test_creator)
        print(f"Created/updated creator ID: {creator_id}")

        # Test stats
        stats = db.get_stats()
        print(f"Database stats: {json.dumps(stats, indent=2)}")
