# Brand Perception Data Collection Guide

## Overview

This guide explains how to collect consumer perception data for 3M brands to map brand strengths against garage organization opportunities.

## Collection Strategy

### Target: 200+ data points per brand

**Distribution by source:**
- Reddit: 50+ posts/comments
- YouTube: 50+ comments
- Amazon: 100+ reviews (50 hate + 50 love)
- Social (TikTok/Instagram): 50+ posts/comments

### Timeframe: Last 18 months
- Focus on recent, current perceptions
- Avoid outdated product formulations
- Capture current sentiment trends

## Data Sources

### 1. Reddit (Free)

**Subreddits:**
- r/HomeImprovement
- r/organization
- r/DIY
- r/homeowners
- r/Garages

**Search Strategy:**
```
[Brand] + garage
[Brand] + organization
[Brand] + storage
[Brand] + DIY
```

**What to collect:**
- Post titles and self-text
- Top-level comments (avoid deep threads)
- Upvote counts (signal importance)
- Post dates

**Quality filters:**
- Min 3 upvotes for posts
- Min 2 upvotes for comments
- Exclude bot posts
- Exclude promotional spam

### 2. YouTube (Free with API key)

**Search Queries:**
```
[Brand] garage organization
[Brand] home storage
[Brand] DIY project
[Brand] review
```

**What to collect:**
- Video titles
- Top comments (sorted by relevance)
- Like counts on comments
- Upload dates
- Channel names (for credibility)

**Quality filters:**
- Videos with 1,000+ views
- Comments with 5+ likes
- Exclude brand-official channels
- Exclude obvious spam

### 3. Amazon Reviews (Paid scraping recommended)

**Products to target:**
- Top 10 products per brand
- Filter for organization/storage categories
- Focus on products with 100+ reviews

**What to collect:**
- 1-star reviews (50 per brand)
- 5-star reviews (50 per brand)
- Review text (full)
- Verified purchase status
- Helpful votes count

**Quality filters:**
- Min 50 words per review
- Verified purchases only
- Min 5 helpful votes
- Exclude obvious fakes

### 4. Social Media (Paid scraping recommended)

**TikTok:**
- Hashtag search: #[Brand]organization, #[Brand]garage
- Caption text + transcript if available
- Like/comment counts
- Creator follower counts

**Instagram:**
- Hashtag search + brand tag search
- Caption text only
- Engagement metrics
- Post dates

**Quality filters:**
- Min 100 likes for TikTok
- Min 50 likes for Instagram
- Exclude influencer partnerships
- Exclude brand-owned accounts

## Data Validation

**Required fields per data point:**
- Source (reddit/youtube/amazon/tiktok/instagram)
- Brand mentioned
- Text content (minimum 20 words)
- Date collected
- Date published
- Engagement metric (upvotes/likes/helpful votes)
- URL or unique ID

**Quality checks:**
- No duplicates across sources
- All timestamps within 18-month window
- All text in English (or auto-translated)
- Brand name explicitly mentioned

## Output Format

### Raw data structure:
```
data/raw/
├── [brand_name]/
│   ├── reddit/
│   │   ├── posts.json
│   │   └── comments.json
│   ├── youtube/
│   │   └── comments.json
│   ├── amazon/
│   │   ├── 1star_reviews.json
│   │   └── 5star_reviews.json
│   └── social/
│       ├── tiktok.json
│       └── instagram.json
```

### JSON schema:
```json
{
  "source": "reddit|youtube|amazon|tiktok|instagram",
  "brand": "Command",
  "text": "Love my Command hooks for organizing my garage...",
  "date_collected": "2024-10-30",
  "date_published": "2024-09-15",
  "engagement": 42,
  "url": "https://reddit.com/...",
  "metadata": {
    "subreddit": "HomeImprovement",  // if reddit
    "verified_purchase": true,        // if amazon
    "rating": 5,                      // if amazon
    "hashtags": ["#garage"]          // if social
  }
}
```

## Rate Limiting & Ethics

**Reddit API:**
- 60 requests/minute
- Use exponential backoff
- Respect user privacy (no DMs)

**YouTube API:**
- 10,000 units/day (free tier)
- 1 search = 100 units
- 1 comment thread = 1 unit

**Paid scrapers:**
- Follow service rate limits
- Respect robots.txt
- Avoid aggressive scraping
- Stay within budget ($50 total)

## Progress Tracking

Create `collection_status.json` in data/ root:
```json
{
  "Command": {
    "reddit": 48,
    "youtube": 52,
    "amazon": 100,
    "social": 45,
    "total": 245,
    "target": 200,
    "complete": true
  }
}
```

Update after each collection run.

## Troubleshooting

**Low data volume:**
- Expand search terms (brand-specific products)
- Extend timeframe to 24 months
- Lower quality thresholds temporarily
- Add more subreddits/sources

**High spam/irrelevant:**
- Increase engagement thresholds
- Add negative keyword filters
- Manual review sample (10%)

**API errors:**
- Check rate limits
- Verify API keys
- Use exponential backoff
- Switch to alternative endpoints

## Next Steps

After collection complete:
1. Run data validation script
2. Check collection_status.json
3. Proceed to Phase 3 (Analysis)
