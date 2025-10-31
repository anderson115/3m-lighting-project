# API Credentials Guide - Brand Perceptions Module

**Location:** All API credentials stored in 1Password vault: `Development`

---

## Available API Credentials

### 1. Apify API - Brand Perceptions Module
**1Password Entry:** `Apify API - Brand Perceptions Module`
**Token:** `[STORED IN 1PASSWORD]`
**Console:** https://console.apify.com

**Available Actors:**
- `apify/web-scraper` - General web scraping
- `clockworks/tiktok-scraper` - TikTok data extraction
- `clockworks/free-tiktok-scraper` - Free TikTok scraper
- `tri_angle/walmart-fast-product-scraper` - Walmart products

**Usage:**
```bash
# Retrieve token from 1Password first
APIFY_TOKEN=$(op item get "Apify API - Brand Perceptions Module" --fields label="API Token")
curl "https://api.apify.com/v2/acts?token=${APIFY_TOKEN}"
```

**Python:**
```python
import os
from apify_client import ApifyClient
# Set APIFY_TOKEN environment variable from 1Password
client = ApifyClient(os.environ['APIFY_TOKEN'])
```

---

### 2. BrightData API - Brand Perceptions Social Media
**1Password Entry:** `BrightData API - Brand Perceptions Social Media`
**Token:** `[STORED IN 1PASSWORD]`
**API Endpoint:** https://api.brightdata.com/datasets/v3

**Available Datasets:**
- Reddit: `gd_l7q7dkf244hwjntr0`
- Amazon: `gd_lwhideng15g8jg63s7`

**Usage:**
```bash
# Retrieve token from 1Password first
BRIGHTDATA_TOKEN=$(op item get "BrightData API - Brand Perceptions Social Media" --fields label="credential")
curl -H "Authorization: Bearer ${BRIGHTDATA_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"input":[{"url":"TARGET_URL"}]}' \
  "https://api.brightdata.com/datasets/v3/scrape?dataset_id=DATASET_ID&notify=false&include_errors=true"
```

**Python:**
```python
import os
import requests
headers = {
    "Authorization": f"Bearer {os.environ['BRIGHTDATA_TOKEN']}",
    "Content-Type": "application/json"
}
```

---

### 3. Reddit API (PRAW)
**1Password Entry:** `Reddit - MikeHoltPHD`
**Username:** `mikeholtphd`
**Note:** Requires creating app at https://www.reddit.com/prefs/apps for client_id/secret

---

## Retrieving Credentials via CLI

**List all API credentials:**
```bash
op item list --format json | python3 -c "
import json, sys
items = json.load(sys.stdin)
for item in items:
    if 'api' in item.get('title', '').lower():
        print(item.get('title'))
"
```

**Get specific credential:**
```bash
# Apify
op item get "Apify API - Brand Perceptions Module" --fields label="API Token"

# BrightData
op item get "BrightData API - Brand Perceptions Social Media" --fields label="credential"
```

---

## Standard Format for New API Entries

When creating new API credentials in 1Password:

```bash
op item create --category="API Credential" \
  --title="SERVICE_NAME API - Brand Perceptions MODULE" \
  --vault="Development" \
  "credential[password]=API_TOKEN_HERE" \
  "url=https://api.service.com" \
  "notesPlain=Description of service, dataset IDs, usage notes"
```

**Required Fields:**
- Title format: `[Service] API - Brand Perceptions [Purpose]`
- Vault: `Development`
- Category: `API Credential`
- Fields: `credential`, `url`, `notesPlain`

---

**Last Updated:** 2025-10-31
**Module:** brand-perceptions
