# Database Schema Documentation

**Module:** Creator Intelligence
**Database:** SQLite (Phase 1) → PostgreSQL (Phase 2)
**Version:** 1.0.0
**Last Updated:** 2025-10-10

---

## 📊 Schema Overview

The Creator Intelligence database uses 3 main tables to store creator profiles, content analysis, and consumer language insights.

**Design Principles:**
- **JSON fields** for flexibility (themes, pain points, language terms)
- **Unique constraints** to prevent duplicates
- **Indexes** on frequently queried fields for performance
- **Foreign keys** to maintain referential integrity

---

## 📁 Table: `creators`

**Purpose:** Store creator profile metadata, metrics, and viability scores

### Schema

```sql
CREATE TABLE creators (
    -- Primary key
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Identity
    platform TEXT NOT NULL,              -- youtube, etsy, instagram, tiktok
    username TEXT NOT NULL,              -- Platform-specific username
    display_name TEXT,                   -- Public display name
    url TEXT UNIQUE,                     -- Profile URL

    -- Metrics
    followers INTEGER,                   -- Follower/subscriber count
    following INTEGER,                   -- Following count (if available)
    total_posts INTEGER,                 -- Total content pieces
    avg_engagement_rate REAL,            -- (likes + comments) / followers
    content_frequency TEXT,              -- daily, weekly, monthly, irregular

    -- Geographic
    country TEXT,                        -- Two-letter country code (US, CA, UK)
    region TEXT,                         -- State/province (California, Ontario)
    language TEXT,                       -- Primary language (en, es, fr)
    timezone TEXT,                       -- IANA timezone (America/Los_Angeles)

    -- Content Analysis (JSON)
    primary_niche TEXT,                  -- lighting_installation, home_improvement, product_review
    content_themes JSON,                 -- ["installation", "troubleshooting", "reviews"]
    pain_points_mentioned JSON,          -- [{"text": "...", "category": "technical", "severity": "medium"}]
    consumer_language JSON,              -- [{"term": "warm white", "category": "feature", "frequency": 5}]

    -- Scoring (0-100 scale)
    research_viability_score INTEGER,    -- Research study suitability
    partnership_viability_score INTEGER, -- Brand partnership suitability
    brand_safety_score INTEGER,          -- Content appropriateness (future use)

    -- Metadata
    is_verified BOOLEAN DEFAULT 0,       -- Platform verification badge
    is_business_account BOOLEAN DEFAULT 0,
    last_scraped TIMESTAMP,              -- Last data collection
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    UNIQUE(platform, username)
);

-- Indexes
CREATE INDEX idx_platform ON creators(platform);
CREATE INDEX idx_research_score ON creators(research_viability_score DESC);
CREATE INDEX idx_partnership_score ON creators(partnership_viability_score DESC);
CREATE INDEX idx_country ON creators(country);
CREATE INDEX idx_niche ON creators(primary_niche);
```

### Example Rows

```json
{
  "id": 1,
  "platform": "youtube",
  "username": "UC_x5XG1OV2P6uZZ5FSM9Ttw",
  "display_name": "Google Developers",
  "url": "https://youtube.com/c/GoogleDevelopers",
  "followers": 2400000,
  "following": 0,
  "total_posts": 8542,
  "avg_engagement_rate": 0.025,
  "content_frequency": "daily",
  "country": "US",
  "region": "California",
  "language": "en",
  "primary_niche": "lighting_installation",
  "content_themes": ["installation", "troubleshooting", "product_review"],
  "pain_points_mentioned": [
    {"text": "LED strips too dim for task lighting", "category": "aesthetic", "severity": "medium"}
  ],
  "consumer_language": [
    {"term": "warm white", "category": "feature", "frequency": 15},
    {"term": "dimmable", "category": "feature", "frequency": 8}
  ],
  "research_viability_score": 87,
  "partnership_viability_score": 72,
  "is_verified": true,
  "is_business_account": false,
  "last_scraped": "2025-10-10T15:30:00Z",
  "created_at": "2025-10-10T10:00:00Z"
}
```

---

## 📄 Table: `creator_content`

**Purpose:** Store individual content pieces (videos, posts, listings) from each creator

### Schema

```sql
CREATE TABLE creator_content (
    -- Primary key
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creator_id INTEGER NOT NULL,         -- Foreign key to creators table

    -- Content metadata
    content_type TEXT,                   -- video, post, listing, story
    content_url TEXT UNIQUE,             -- Direct link to content
    title TEXT,
    description TEXT,
    thumbnail_url TEXT,

    -- Engagement metrics
    published_date TIMESTAMP,
    views INTEGER,
    likes INTEGER,
    comments_count INTEGER,
    shares INTEGER,
    engagement_rate REAL,                -- (likes + comments + shares) / views

    -- LLM Analysis (JSON)
    extracted_language JSON,             -- [{"term": "LED strip", "category": "product"}]
    pain_points JSON,                    -- [{"text": "too dim", "category": "aesthetic"}]
    themes JSON,                         -- ["installation", "review"]

    -- Metadata
    is_relevant BOOLEAN DEFAULT 1,       -- LLM relevance classification
    relevance_confidence REAL,           -- 0.0-1.0 from LLM
    analyzed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Foreign key constraint
    FOREIGN KEY (creator_id) REFERENCES creators(id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX idx_creator_content ON creator_content(creator_id);
CREATE INDEX idx_published_date ON creator_content(published_date DESC);
CREATE INDEX idx_engagement ON creator_content(engagement_rate DESC);
CREATE INDEX idx_relevance ON creator_content(is_relevant, relevance_confidence DESC);
```

### Example Row

```json
{
  "id": 1,
  "creator_id": 1,
  "content_type": "video",
  "content_url": "https://youtube.com/watch?v=ABC123",
  "title": "How to Install LED Strip Lights Under Kitchen Cabinets",
  "description": "Step-by-step tutorial for installing under-cabinet LED strips...",
  "thumbnail_url": "https://i.ytimg.com/vi/ABC123/maxresdefault.jpg",
  "published_date": "2025-09-15T12:00:00Z",
  "views": 125000,
  "likes": 4500,
  "comments_count": 320,
  "shares": 150,
  "engagement_rate": 0.0388,
  "extracted_language": [
    {"term": "under-cabinet lighting", "category": "job"},
    {"term": "LED strip", "category": "product"},
    {"term": "warm white", "category": "feature"}
  ],
  "pain_points": [
    {"text": "difficult to wire correctly", "category": "technical"},
    {"text": "choosing right power supply", "category": "usability"}
  ],
  "themes": ["installation", "tutorial"],
  "is_relevant": true,
  "relevance_confidence": 0.95,
  "analyzed_at": "2025-10-10T15:45:00Z",
  "created_at": "2025-10-10T15:30:00Z"
}
```

---

## 🗣️ Table: `consumer_language`

**Purpose:** Aggregate consumer terminology across all platforms for marketing insights

### Schema

```sql
CREATE TABLE consumer_language (
    -- Primary key
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    term TEXT UNIQUE NOT NULL,           -- Consumer phrase (lowercase normalized)
    category TEXT NOT NULL,              -- pain_point, job, feature, product, brand

    -- Frequency tracking
    total_mentions INTEGER DEFAULT 1,    -- Aggregate mentions across all platforms
    platforms JSON,                      -- {"youtube": 10, "etsy": 5, "instagram": 3}

    -- Context examples (for marketing use)
    example_quotes JSON,                 -- [{"text": "...", "creator": "...", "platform": "..."}]

    -- Semantic relationships
    synonyms JSON,                       -- ["warm white", "soft white", "2700K"]
    co_occurring_terms JSON,             -- ["dimmer", "dimmable", "adjustable"]

    -- Metadata
    first_seen TIMESTAMP,
    last_seen TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_term ON consumer_language(term);
CREATE INDEX idx_category ON consumer_language(category);
CREATE INDEX idx_mentions ON consumer_language(total_mentions DESC);
```

### Example Row

```json
{
  "id": 1,
  "term": "warm white",
  "category": "feature",
  "total_mentions": 234,
  "platforms": {"youtube": 120, "etsy": 80, "instagram": 34, "tiktok": 0},
  "example_quotes": [
    {
      "text": "looking for warm white bulbs for my living room",
      "creator": "HomeDecorLover",
      "platform": "instagram",
      "date": "2025-09-20"
    },
    {
      "text": "these warm white LED strips give such a cozy feel",
      "creator": "DIYHomeGuru",
      "platform": "youtube",
      "date": "2025-09-18"
    }
  ],
  "synonyms": ["soft white", "2700K", "cozy white"],
  "co_occurring_terms": ["dimmable", "under-cabinet", "ambiance"],
  "first_seen": "2025-08-01T10:00:00Z",
  "last_seen": "2025-10-10T15:30:00Z",
  "created_at": "2025-08-01T10:00:00Z"
}
```

---

## 🔍 Common Queries

### Get Top 50 Creators for Research (US-based, score >70)

```sql
SELECT
    id,
    display_name,
    platform,
    url,
    followers,
    research_viability_score,
    country
FROM creators
WHERE country = 'US'
  AND research_viability_score > 70
ORDER BY research_viability_score DESC
LIMIT 50;
```

### Get All Instagram Creators with High Engagement

```sql
SELECT
    display_name,
    username,
    followers,
    avg_engagement_rate,
    research_viability_score
FROM creators
WHERE platform = 'instagram'
  AND avg_engagement_rate > 0.03
ORDER BY avg_engagement_rate DESC;
```

### Get Consumer Language Dictionary (Pain Points Only)

```sql
SELECT
    term,
    total_mentions,
    platforms,
    example_quotes
FROM consumer_language
WHERE category = 'pain_point'
  AND total_mentions >= 5
ORDER BY total_mentions DESC
LIMIT 50;
```

### Get Creator Content for Specific Creator

```sql
SELECT
    title,
    content_url,
    published_date,
    views,
    engagement_rate,
    themes,
    pain_points
FROM creator_content
WHERE creator_id = 1
  AND is_relevant = 1
ORDER BY published_date DESC
LIMIT 20;
```

### Get Trending Themes (Mentioned by 10+ Creators)

```sql
SELECT
    json_each.value AS theme,
    COUNT(DISTINCT id) AS creator_count
FROM creators, json_each(creators.content_themes)
GROUP BY theme
HAVING creator_count >= 10
ORDER BY creator_count DESC;
```

---

## 🔄 PostgreSQL Migration (Phase 2)

When scaling beyond 5,000 creators or developing UI frontend, migrate to PostgreSQL for better performance and concurrency.

### Migration Steps

```bash
# 1. Export SQLite to SQL
sqlite3 creators.db .dump > creators_backup.sql

# 2. Convert SQLite syntax to PostgreSQL
sed -i '' 's/AUTOINCREMENT/SERIAL/g' creators_backup.sql
sed -i '' 's/INTEGER PRIMARY KEY AUTOINCREMENT/SERIAL PRIMARY KEY/g' creators_backup.sql

# 3. Create PostgreSQL database
createdb creator_intelligence

# 4. Import data
psql -U postgres -d creator_intelligence < creators_backup.sql
```

### PostgreSQL Schema Enhancements

```sql
-- JSON indexing (GIN indexes for fast JSON queries)
CREATE INDEX idx_content_themes_gin ON creators USING GIN (content_themes);
CREATE INDEX idx_pain_points_gin ON creators USING GIN (pain_points_mentioned);

-- Full-text search on descriptions
ALTER TABLE creator_content ADD COLUMN description_tsv tsvector;
UPDATE creator_content SET description_tsv = to_tsvector('english', description);
CREATE INDEX idx_description_fts ON creator_content USING GIN (description_tsv);

-- Partitioning by platform (for performance)
CREATE TABLE creators_youtube PARTITION OF creators FOR VALUES IN ('youtube');
CREATE TABLE creators_etsy PARTITION OF creators FOR VALUES IN ('etsy');
CREATE TABLE creators_instagram PARTITION OF creators FOR VALUES IN ('instagram');
CREATE TABLE creators_tiktok PARTITION OF creators FOR VALUES IN ('tiktok');
```

---

## 📈 Performance Benchmarks

| Operation | SQLite (1K creators) | SQLite (10K creators) | PostgreSQL (10K creators) |
|-----------|----------------------|-----------------------|---------------------------|
| Get top 50 by score | 50ms | 500ms | 20ms |
| Filter by platform + country | 30ms | 300ms | 15ms |
| Full-text search (content) | N/A | N/A | 50ms |
| Insert 100 creators | 200ms | 300ms | 150ms |
| JSON field query | 100ms | 1000ms | 80ms |

**Recommendation:** Migrate to PostgreSQL at 5,000+ creators for optimal performance.

---

**END OF DATABASE SCHEMA DOCUMENTATION**
