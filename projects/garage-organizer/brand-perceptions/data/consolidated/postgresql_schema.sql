-- Database: offbrain-insights
-- Client: 3M
-- Project: garage-organizers
-- Updated: 2025-11-01 (includes YouTube data)

-- Drop existing tables if re-creating
DROP TABLE IF EXISTS garage_organizers_social_media CASCADE;
DROP TABLE IF EXISTS garage_organizers_product_reviews CASCADE;

-- Table: social_media_posts (Reddit + YouTube)
CREATE TABLE garage_organizers_social_media (
    id SERIAL PRIMARY KEY,
    title TEXT,
    post_text TEXT,
    author VARCHAR(255),
    subreddit VARCHAR(100),  -- For Reddit posts
    platform_id VARCHAR(100),  -- For YouTube video IDs
    video_title TEXT,  -- For YouTube comments (parent video title)
    channel_name VARCHAR(255),  -- For YouTube channel names
    post_url TEXT,
    score INTEGER,
    num_comments INTEGER,
    created_date VARCHAR(255),  -- Changed to VARCHAR to handle inconsistent formats
    brand_mentions TEXT[],  -- Array of brand names
    source VARCHAR(50) DEFAULT 'reddit',  -- reddit, youtube_video, youtube_comment
    collected_date VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: product_reviews (Amazon)
CREATE TABLE garage_organizers_product_reviews (
    id SERIAL PRIMARY KEY,
    title TEXT,
    rating VARCHAR(50),
    author VARCHAR(255),
    date VARCHAR(255),
    verified_purchase BOOLEAN,
    review_text TEXT,
    product_id VARCHAR(50),
    product_title TEXT,
    brand VARCHAR(100),
    source VARCHAR(50) DEFAULT 'amazon',
    collected_date VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_social_brand ON garage_organizers_social_media USING GIN (brand_mentions);
CREATE INDEX IF NOT EXISTS idx_social_subreddit ON garage_organizers_social_media (subreddit);
CREATE INDEX IF NOT EXISTS idx_social_source ON garage_organizers_social_media (source);
CREATE INDEX IF NOT EXISTS idx_social_platform_id ON garage_organizers_social_media (platform_id);

CREATE INDEX IF NOT EXISTS idx_review_product ON garage_organizers_product_reviews (product_id);
CREATE INDEX IF NOT EXISTS idx_review_brand ON garage_organizers_product_reviews (brand);
CREATE INDEX IF NOT EXISTS idx_review_verified ON garage_organizers_product_reviews (verified_purchase);

-- View: Combined social media stats by source
CREATE OR REPLACE VIEW social_media_by_source AS
SELECT
    source,
    COUNT(*) as total_posts,
    COUNT(DISTINCT author) as unique_authors,
    SUM(score) as total_engagement
FROM garage_organizers_social_media
GROUP BY source;

-- View: Brand mentions across all sources
CREATE OR REPLACE VIEW brand_mentions_summary AS
SELECT
    UNNEST(brand_mentions) as brand,
    source,
    COUNT(*) as mentions
FROM garage_organizers_social_media
WHERE brand_mentions IS NOT NULL AND array_length(brand_mentions, 1) > 0
GROUP BY brand, source
ORDER BY mentions DESC;
