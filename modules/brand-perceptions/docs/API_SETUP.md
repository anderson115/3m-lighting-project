# API Setup Guide

## Free APIs (Required)

### 1. Reddit API

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill in:
   - Name: `brand-perception-collector`
   - App type: `script`
   - Redirect URI: `http://localhost:8080`
4. Save CLIENT_ID and CLIENT_SECRET to `.env`

### 2. YouTube Data API v3

1. Go to https://console.cloud.google.com/
2. Create new project or select existing
3. Enable "YouTube Data API v3"
4. Create credentials → API key
5. Restrict key to YouTube Data API only
6. Save API_KEY to `.env`
7. Free tier: 10,000 units/day (sufficient for this project)

## Paid APIs (Optional - $50 budget)

### 3. Bright Data (Amazon scraping)

1. Sign up at https://brightdata.com/
2. Choose "Web Scraper API" product
3. Budget: $25
4. Save API_KEY to `.env`
5. Use for Amazon review collection

### 4. Apify (Social media scraping)

1. Sign up at https://apify.com/
2. Choose Instagram/TikTok scrapers
3. Budget: $25
4. Save API_TOKEN to `.env`
5. Use for social media collection

## Environment Setup

1. Copy `.env.example` to `.env`
2. Fill in API keys:

```bash
# Free APIs
REDDIT_CLIENT_ID=abc123
REDDIT_CLIENT_SECRET=xyz789
REDDIT_USER_AGENT=brand-perception-collector/0.1
YOUTUBE_API_KEY=AIza...

# Paid APIs (optional)
BRIGHT_DATA_API_KEY=...
APIFY_API_TOKEN=...
```

## Verification

Test API connections:

```bash
python scripts/test_apis.py
```

Expected output:
```
✓ Reddit API: Connected
✓ YouTube API: Connected (9,850 units remaining)
⚠ Bright Data: Not configured (optional)
⚠ Apify: Not configured (optional)
```

## Rate Limits

| API | Free Tier | Rate Limit | Cost if exceeded |
|-----|-----------|------------|------------------|
| Reddit | Yes | 60 req/min | N/A |
| YouTube | Yes | 10,000 units/day | $0.30/1K units |
| Bright Data | No | Custom | $0.60/1K requests |
| Apify | Trial | 1K operations | $49/month |

## Troubleshooting

**Reddit "401 Unauthorized":**
- Check CLIENT_ID and CLIENT_SECRET
- Verify app type is "script"
- Check USER_AGENT format

**YouTube "403 Quota Exceeded":**
- Wait 24 hours for reset
- Reduce collection volume
- Consider multiple API keys

**Bright Data connection failed:**
- Verify billing active
- Check API key format
- Review dashboard for errors

**Apify rate limit:**
- Upgrade to paid tier
- Reduce concurrent requests
- Use built-in retry logic
