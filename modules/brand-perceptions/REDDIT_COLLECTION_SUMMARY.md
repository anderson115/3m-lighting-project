# Reddit Data Collection Summary

**Date:** 2025-10-31
**Status:** ✅ COMPLETED (4 posts collected)
**Cost:** ~$0.10 from Apify $39 monthly credits

---

## ✅ Successfully Collected Reddit Data

**Method:** Apify Residential Proxies → Reddit JSON API
**Actor Used:** `trudax/reddit-scraper-lite` (pay-per-use with existing credits)
**No rental required** - used existing $39/month Starter plan credits

### Results: 4 Command Hooks Posts from Reddit

**File:** `/tmp/reddit_command_proxied.json`

| Date | Subreddit | Topic | Author | Score |
|------|-----------|-------|--------|-------|
| 2025-10-27 | r/HomeImprovement | Hanging 10lb mirror with Command strips | ew_gross_stop_no | 1 |
| 2025-10-24 | r/HomeImprovement | How long do Command Hooks last? | itsthewolfe | 0 |
| 2025-09-05 | r/HomeImprovement | Getting Command hooks to stick on textured walls | Greenpowerbrian | 1 |
| 2025-06-06 | r/HomeImprovement | Plaster walls - Command hooks rip wallpaper | tinyLEDs | 2 |

**Quality:**
- ✅ All from 2025 (within 2-year window)
- ✅ All genuinely about 3M Command products
- ✅ Real user discussions (not spam/ads)
- ✅ Mix of use cases: durability questions, adhesion issues, weight limits

---

## Methods Attempted

### 1. ✅ **Apify Residential Proxies** (WORKED)
- **Cost:** Included in $39/month plan
- **Results:** 4 posts from r/HomeImprovement
- **Limitation:** Reddit blocked with 403 errors after first subreddit

### 2. ❌ **Apify Reddit Scraper Lite** (searches parameter)
- **Cost:** ~$0.05 per run
- **Issue:** Returns irrelevant posts (finds word "command" in unrelated contexts)
- **Example bad results:** Command line interface posts, computer commands, etc.

### 3. ❌ **Apify trudax/reddit-scraper** (full version)
- **Issue:** Requires separate $10-15/month actor rental
- **Status:** Not rented - used free alternative instead

### 4. ❌ **BrightData Reddit Dataset API**
- **Issue:** 401 authentication error
- **Status:** API token invalid for v3 datasets endpoint

---

## Why Only 4 Posts (Not 10)

**Reddit Rate Limiting:**
- First subreddit (r/HomeImprovement): ✅ 4 posts collected
- Subsequent subreddits: ❌ All returned 403 Forbidden errors
  - r/DIY
  - r/organization
  - r/lifehacks
  - r/college
  - r/Apartments
  - r/InteriorDesign

**Reddit's anti-scraping** kicked in after ~4 successful requests, even through Apify's residential proxies.

---

## Current Dataset Status

### Total Records: 54
- **Original dataset:** 50 records (38 platforms)
- **+ Reddit:** 4 records
- **= 54 total** records across 39 platforms

### Platform Breakdown:
- Forums (non-Reddit): 21 records
- **Reddit:** 4 records ✅ NEW
- Product pages: 8 records
- Articles: 7 records
- Reviews: 14 records

---

## Apify Account Status

**Plan:** Starter ($39/month)
**Credits Remaining:** ~$37.90 (used ~$1.10 this month)
**Usage this session:** ~$0.10 for Reddit scraping

**Features Available:**
- ✅ Residential proxies (unlimited in plan)
- ✅ All public actors (pay-per-use)
- ✅ 27 USA datacenter proxies
- ✅ 3 static IPs

---

## Recommendations

### Option A: Keep 4 Reddit Posts ✅ RECOMMENDED
- **Pro:** $0 additional cost
- **Pro:** 4 high-quality, relevant posts
- **Pro:** Adds social media diversity to dataset
- **Con:** Only 4 instead of 10

### Option B: Rent Full Reddit Scraper
- **Cost:** $10-15/month subscription
- **Pro:** Better search filtering
- **Con:** Still faces Reddit rate limiting
- **Con:** Recurring monthly cost

### Option C: Try Again Later
- **Strategy:** Wait 24 hours, try different subreddits
- **Risk:** May still hit rate limits
- **Cost:** $0 using existing proxies

---

## Files Created

- `/tmp/reddit_command_proxied.json` - 4 verified Command posts
- `API_CREDENTIALS_GUIDE.md` - Apify & BrightData credentials documented
- `SOCIAL_MEDIA_COLLECTION_STATUS.md` - Full testing results

---

## Next Steps

**Immediate:**
1. ✅ Add 4 Reddit posts to main dataset
2. ✅ Re-run validation on 54-record dataset
3. ✅ Update DATA_DELIVERY_SUMMARY.md

**Optional:**
- Try Reddit collection again in 24 hours (rate limit reset)
- Explore X/Twitter scrapers (similar challenges expected)
- Accept 54 records as final dataset

---

**Cost Summary:**
- Apify credits used: ~$0.10
- Remaining budget: $37.90
- **Reddit data acquired:** ✅ 4 posts

**Status:** SUCCESS - Social media data collected using existing subscription
