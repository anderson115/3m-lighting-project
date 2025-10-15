"""
Patent Intelligence - Database Module
Handles SQLite database operations with data validation
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class PatentDatabase:
    """Manage patent data in SQLite with validation"""

    def __init__(self, db_path: str = None):
        if db_path is None:
            module_dir = Path(__file__).parent.parent
            db_path = module_dir / "data" / "database" / "patents.db"

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self._initialize_database()

    def _initialize_database(self):
        """Create database schema if it doesn't exist"""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row

        cursor = self.conn.cursor()

        # Patents table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patents (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                abstract TEXT,
                filing_date DATE,
                grant_date DATE,
                api_source TEXT NOT NULL,

                -- Classification
                cpc_codes TEXT,
                ipc_codes TEXT,

                -- People/Entities
                inventors TEXT,
                assignees TEXT,

                -- Content
                claims_text TEXT,
                description_text TEXT,

                -- Citations
                backward_citations TEXT,
                forward_citations TEXT,
                citation_count INTEGER DEFAULT 0,

                -- LLM Analysis (populated later)
                key_innovation TEXT,
                applications TEXT,
                market_potential INTEGER,
                relevance_score REAL,

                -- Metadata
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                -- Data quality flags
                has_abstract BOOLEAN DEFAULT 0,
                has_claims BOOLEAN DEFAULT 0,
                has_assignees BOOLEAN DEFAULT 0,
                data_complete BOOLEAN DEFAULT 0
            )
        ''')

        # Indexes for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_filing_date ON patents(filing_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_assignees ON patents(assignees)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_relevance ON patents(relevance_score)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_api_source ON patents(api_source)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_data_complete ON patents(data_complete)')

        # Competitors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS competitors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                aliases TEXT,
                patent_count INTEGER DEFAULT 0,
                last_filing_date DATE,
                active BOOLEAN DEFAULT 1
            )
        ''')

        # Technology clusters table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS technology_clusters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                patent_ids TEXT,
                filing_velocity REAL,
                trend_direction TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Data collection log table (for checkpoint tracking)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS collection_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_query TEXT,
                patents_found INTEGER,
                patents_stored INTEGER,
                api_source TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT
            )
        ''')

        self.conn.commit()
        print(f"✅ Database initialized: {self.db_path}")

    def insert_patent(self, patent_data: Dict) -> bool:
        """
        Insert patent with validation
        Returns True if successful, False if duplicate
        """
        cursor = self.conn.cursor()

        # Check if patent already exists
        cursor.execute('SELECT id FROM patents WHERE id = ?', (patent_data['id'],))
        if cursor.fetchone():
            return False  # Duplicate

        # Validate required fields
        if not patent_data.get('title'):
            print(f"⚠️ Skipping patent {patent_data.get('id')}: missing title")
            return False

        # Data quality flags
        has_abstract = bool(patent_data.get('abstract'))
        has_claims = bool(patent_data.get('claims_text'))
        has_assignees = bool(patent_data.get('assignees'))
        data_complete = has_abstract and has_claims and has_assignees

        # Convert lists/dicts to JSON
        cpc_codes = json.dumps(patent_data.get('cpc_codes', []))
        ipc_codes = json.dumps(patent_data.get('ipc_codes', []))
        inventors = json.dumps(patent_data.get('inventors', []))
        assignees = json.dumps(patent_data.get('assignees', []))
        backward_citations = json.dumps(patent_data.get('backward_citations', []))
        forward_citations = json.dumps(patent_data.get('forward_citations', []))

        cursor.execute('''
            INSERT INTO patents (
                id, title, abstract, filing_date, grant_date, api_source,
                cpc_codes, ipc_codes, inventors, assignees,
                claims_text, description_text,
                backward_citations, forward_citations, citation_count,
                has_abstract, has_claims, has_assignees, data_complete
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            patent_data['id'],
            patent_data['title'],
            patent_data.get('abstract'),
            patent_data.get('filing_date'),
            patent_data.get('grant_date'),
            patent_data['api_source'],
            cpc_codes,
            ipc_codes,
            inventors,
            assignees,
            patent_data.get('claims_text'),
            patent_data.get('description_text'),
            backward_citations,
            forward_citations,
            len(patent_data.get('forward_citations', [])),
            has_abstract,
            has_claims,
            has_assignees,
            data_complete
        ))

        self.conn.commit()
        return True

    def get_stats(self) -> Dict:
        """Get database statistics for validation"""
        cursor = self.conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM patents')
        total = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM patents WHERE data_complete = 1')
        complete = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM patents WHERE has_abstract = 1')
        with_abstract = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM patents WHERE has_claims = 1')
        with_claims = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM patents WHERE has_assignees = 1')
        with_assignees = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(DISTINCT api_source) FROM patents')
        sources = cursor.fetchone()[0]

        cursor.execute('SELECT MIN(filing_date), MAX(filing_date) FROM patents')
        date_range = cursor.fetchone()

        return {
            'total_patents': total,
            'complete_data': complete,
            'with_abstract': with_abstract,
            'with_claims': with_claims,
            'with_assignees': with_assignees,
            'data_sources': sources,
            'date_range': {
                'earliest': date_range[0],
                'latest': date_range[1]
            },
            'completeness_pct': round((complete / total * 100) if total > 0 else 0, 1)
        }

    def log_collection(self, search_query: str, found: int, stored: int, api_source: str, notes: str = ''):
        """Log data collection for audit trail"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO collection_log (search_query, patents_found, patents_stored, api_source, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (search_query, found, stored, api_source, notes))
        self.conn.commit()

    def get_patents_for_analysis(self, limit: int = None) -> List[Dict]:
        """
        Get patents that need LLM analysis
        Returns patents where key_innovation is NULL
        """
        cursor = self.conn.cursor()

        query = '''
            SELECT id, title, abstract, claims_text, assignees, filing_date
            FROM patents
            WHERE key_innovation IS NULL
            AND data_complete = 1
            ORDER BY filing_date DESC
        '''

        if limit:
            query += f' LIMIT {limit}'

        cursor.execute(query)
        rows = cursor.fetchall()

        patents = []
        for row in rows:
            patents.append({
                'id': row['id'],
                'title': row['title'],
                'abstract': row['abstract'],
                'claims_text': row['claims_text'],
                'assignees': json.loads(row['assignees']) if row['assignees'] else [],
                'filing_date': row['filing_date']
            })

        return patents

    def update_llm_analysis(self, patent_id: str, analysis: Dict):
        """Update patent with LLM analysis results"""
        cursor = self.conn.cursor()

        applications = json.dumps(analysis.get('applications', []))

        cursor.execute('''
            UPDATE patents
            SET key_innovation = ?,
                applications = ?,
                market_potential = ?,
                relevance_score = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            analysis.get('key_innovation'),
            applications,
            analysis.get('market_potential'),
            analysis.get('relevance_score'),
            patent_id
        ))

        self.conn.commit()

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("✅ Database connection closed")
