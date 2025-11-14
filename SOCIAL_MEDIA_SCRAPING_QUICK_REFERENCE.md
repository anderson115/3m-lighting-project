# Social Media Data Collection - Quick Reference Guide

**Last Updated:** November 10, 2025

---

## One-Line Summary by Platform

| Platform | Best Free Solution | Best Paid Solution | Official API |
|----------|-------------------|-------------------|--------------|
| **YouTube Transcripts** | youtube-transcript-api | Apify | ❌ Not available |
| **YouTube Comments** | youtube-comment-downloader | Apify | YouTube Data API v3 (10K/day) |
| **YouTube Shorts** | Same as YouTube | Same as YouTube | Same as YouTube |
| **TikTok** | TikTok-Api (davidteather) | SocialKit API | TikTok Official (approval req'd) |
| **TikTok Transcripts** | ❌ Not available | SocialKit, DumplingAI | ❌ Not available |
| **Instagram Reels** | Instaloader (TOS risk) | Apify | Graph API (Business only) |
| **Instagram Comments** | Instaloader (TOS risk) | Apify | Graph API (Business only) |
| **Reddit** | PRAW (free tier) | PRAW (paid) | Reddit API ($0.24/1K) |

---

## Quick Setup Commands

### YouTube
```bash
# Transcripts
pip install youtube-transcript-api

# Comments
pip install youtube-comment-downloader

# Both + video download
pip install yt-dlp
```

### TikTok
```bash
pip install TikTokApi
python -m playwright install
```

### Instagram
```bash
# Option 1: Instaloader
pip3 install instaloader

# Option 2: instagrapi (more features)
pip install instagrapi
```

### Reddit
```bash
pip install praw
# Need: client_id, client_secret, user_agent from Reddit app
```

### Multi-Platform
```bash
pip install snscrape  # Works with Reddit, Twitter, some Instagram
```

---

## Pricing Cheat Sheet

### Free Tier Limits
- **YouTube Data API:** 10,000 units/day (search = 100 units)
- **Reddit API:** 100 requests/min (OAuth), 10/min (no auth)
- **Instagram Graph API:** 200 requests/hour
- **TikTok Official:** Free but approval required for Research API

### Paid API Costs (as of Nov 2025)
- **Reddit API:** $0.24 per 1,000 requests
- **Apify:** ~$0.50 per 1,000 Instagram posts
- **Bright Data:** From $0.001 per record
- **SerpAPI:** $0.015 per request (YouTube)
- **ScraperAPI:** From $49/month (Hobby plan)
- **Octoparse:** From $75/month (Standard)
- **PhantomBuster:** From $69/month (Starter)

### Monthly Cost Estimates
- **100K YouTube comments:** $0 (free tools)
- **100K TikTok transcripts:** ~$50-100 (SocialKit)
- **100K Instagram posts:** ~$50 (Apify)
- **100K Reddit comments:** ~$24 (API)
- **Total for 100K each:** ~$125-175/month

---

## Risk Levels by Method

### ✅ LOW RISK (Official APIs)
- YouTube Data API v3
- Reddit API (paid)
- Instagram Graph API (Business accounts)
- TikTok Official API (approved)

### ⚠️ MEDIUM RISK (Unofficial but stable)
- youtube-transcript-api
- youtube-comment-downloader
- yt-dlp
- PRAW (uses official Reddit API)

### 🚨 HIGH RISK (Against TOS)
- TikTok-Api (unofficial scraping)
- Instaloader (Instagram bans common)
- instagrapi (Instagram private API)
- Browser automation (Playwright/Selenium)
- Any scraper without API

---

## Decision Tree

### "I need YouTube transcripts"
→ Use `youtube-transcript-api` (FREE, works for Shorts too)

### "I need YouTube comments"
→ Use `youtube-comment-downloader` (FREE, unlimited)
→ OR YouTube Data API v3 (official, 10K/day limit)

### "I need TikTok transcripts"
→ Use SocialKit API (paid, accurate)
→ OR Apify TikTok Transcript Extractor (pay-per-use)

### "I need TikTok comments/metadata"
→ Use `TikTok-Api` (free but unofficial)
→ OR Apify (paid, reliable)

### "I need Instagram Reels + comments"
→ Low volume: Use `Instaloader` (free, TOS risk)
→ High volume: Use Apify (paid, no ban risk)
→ Business account: Use Graph API (free, limited)

### "I need Reddit posts + comments"
→ Low volume: Use PRAW free tier (100 req/min)
→ High volume: Pay for Reddit API ($0.24/1K)
→ Historical: Use PullPush archive (free)

### "I need everything from all platforms"
→ Budget < $100/month: Mix free tools
→ Budget $100-500/month: Use Apify
→ Budget $500+/month: Use Bright Data
→ Enterprise: Custom solution + dedicated infrastructure

### "I'm not a developer"
→ Use Octoparse ($75/month)
→ OR PhantomBuster ($69/month)
→ OR Apify web interface (pay-per-use)

---

## Common Issues & Quick Fixes

### "YouTube transcript not available"
- Video has no captions
- Solution: Use yt-dlp to download, then transcribe with Whisper

### "TikTok-Api stopped working"
- TikTok updated their API
- Solution: `pip install --upgrade TikTokApi`

### "Instagram banned my account"
- Scraped too aggressively
- Solution: Use residential proxies, reduce rate, or use paid API

### "Reddit rate limit exceeded"
- Exceeded 100 req/min free tier
- Solution: Add delays or upgrade to paid API

### "Can't get Instagram Reels transcripts"
- No direct API for this
- Solution: Download Reel → extract audio → use Whisper/AssemblyAI

---

## Recommended Starter Stack

### Academic/Personal Project (FREE)
```
YouTube: youtube-transcript-api + youtube-comment-downloader
TikTok: TikTok-Api (use carefully)
Instagram: Skip or use Instaloader (TOS risk)
Reddit: PRAW free tier
```

### Small Business ($100-300/month)
```
YouTube: Free tools (sufficient)
TikTok: SocialKit API (transcripts) + TikTok-Api (metadata)
Instagram: Apify ($50-100/month)
Reddit: PRAW paid API (~$50/month)
```

### Enterprise ($500+/month)
```
All platforms: Bright Data or Apify
Custom infrastructure with:
- Residential proxy rotation
- Rate limit management
- Data validation pipeline
- Automated error recovery
```

---

## Platform-Specific Notes

### YouTube
- ✅ Transcripts: Easy (youtube-transcript-api)
- ✅ Comments: Easy (youtube-comment-downloader)
- ✅ Shorts: Treated same as regular videos
- ⚠️ Official API: No transcripts, limited comments

### TikTok
- ❌ Transcripts: No free solution (use paid APIs)
- ⚠️ Metadata: TikTok-Api works but breaks often
- 🚨 Risk: Against TOS, account bans possible
- ✅ Official: Requires approval (Research API)

### Instagram
- 🚨 High ban risk with unofficial tools
- ⚠️ Reels: No transcript support (need audio→text)
- ✅ Graph API: Free but Business account required
- ⚠️ Rate limits: 200/hour (Graph API)

### Reddit
- 💰 Paid API since July 2023 ($0.24/1K)
- ✅ PRAW: Official wrapper, easy to use
- ⚠️ Free tier: Limited to 100 req/min
- ℹ️ Historical: Use PullPush archive

---

## MCP Integration Status (Nov 2025)

**Maturity:** EMERGING
**Available:**
- Bright Data MCP (commercial)
- Apify MCP Client
- Social Media Sync (posting only)

**Recommendation:** Use traditional APIs for now, add MCP later for AI workflows

---

## When to Use What

### Use Free Tools When:
- Personal/academic project
- Low volume (<1K requests/day)
- Proof of concept
- Budget constraints

### Use Paid APIs When:
- Business/commercial use
- High volume (>10K requests/day)
- Need reliability
- Can't risk TOS violations

### Use Official APIs When:
- Need compliance
- Long-term project
- Legal requirements
- Prefer stability over features

### Build Custom Solution When:
- Very high volume (millions of requests)
- Specific requirements not met by tools
- Need custom data processing
- Have engineering resources

---

## Red Flags & Warnings

### 🚨 AVOID These Practices:
- Scraping without rate limits
- Using same IP for thousands of requests
- Ignoring robots.txt
- Scraping private/deleted content
- Selling user data
- Not respecting TOS

### ⚠️ USE CAUTION:
- Instagram scraping (high ban risk)
- TikTok scraping (breaks often)
- Browser automation (maintenance heavy)
- Free proxies (usually blocked)

### ✅ SAFE Practices:
- Use official APIs when available
- Respect rate limits
- Add random delays
- Rotate IPs if needed
- Only scrape public data
- Store responsibly

---

## Support Resources

### If Tool Breaks:
1. Check GitHub issues
2. Update to latest version
3. Check if platform updated
4. Look for forks/alternatives

### If Blocked:
1. Reduce request rate
2. Add longer delays
3. Rotate IPs/proxies
4. Use official API instead

### If Need Help:
- GitHub repos: Check Issues/Discussions
- Reddit: r/webscraping, r/python
- Stack Overflow: Tag with specific tool
- Discord: Many tools have communities

---

## 30-Second Decision Guide

**Need transcripts?**
- YouTube: youtube-transcript-api ✅
- TikTok: SocialKit API 💰
- Instagram Reels: Download + Whisper ⚠️

**Need comments?**
- YouTube: youtube-comment-downloader ✅
- Instagram: Apify 💰
- Reddit: PRAW 💰 (since July 2023)
- TikTok: TikTok-Api ⚠️

**Have budget?** → Use Apify (all platforms)
**No budget?** → Mix free tools (accept limitations)
**Need compliance?** → Use official APIs only
**Not a developer?** → Use Octoparse/PhantomBuster

---

## Quick Comparison: Free vs Paid

| Aspect | Free Tools | Paid APIs |
|--------|-----------|-----------|
| **Cost** | $0 | $50-500+/month |
| **Setup** | Code required | Often no-code |
| **Reliability** | Can break | SLA guarantees |
| **Maintenance** | You handle | Provider handles |
| **TOS Risk** | Often violates | Usually compliant |
| **Volume** | Limited | Scales easily |
| **Support** | Community | Dedicated |
| **Best For** | POC, learning | Production |

---

**Remember:** Platforms change constantly. Verify current status before committing to any solution. Test with small volumes first.

**Full Documentation:** See `SOCIAL_MEDIA_DATA_COLLECTION_COMPREHENSIVE_ANALYSIS_NOV_2025.md` for detailed information.
