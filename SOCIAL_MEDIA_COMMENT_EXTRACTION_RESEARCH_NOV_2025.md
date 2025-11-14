# Social Media Comment Extraction Research - November 2025

**Research Date:** November 11, 2025
**Focus:** TikTok & Instagram comment extraction solutions
**Goal:** Identify working, practical solutions for comment extraction

---

## EXECUTIVE SUMMARY

### Quick Recommendations

**For TikTok Comments:**
- **Best Overall:** Apify TikTok Comments Scraper (clockworks actor)
- **Cost:** $5 per 1,000 comments
- **Success Rate:** 98%
- **Implementation:** Simple (no-code UI + API available)
- **Timeline:** 1-2 hours to set up

**For Instagram Comments:**
- **Best Overall:** Apify Instagram Comments Scraper
- **Cost:** $0.50-$2.30 per 1,000 comments
- **Success Rate:** Variable (depends on rate limiting)
- **Implementation:** Moderate (requires careful rate limiting)
- **Timeline:** 2-4 hours to set up + ongoing monitoring

**Critical Insight:** TikTok is significantly easier and more reliable than Instagram in late 2025.

---

## 1. TIKTOK COMMENTS - WORKING APPROACHES

### 1.1 Apify TikTok Comment Scrapers

**Available Actors:**
1. **Clockworks TikTok Comments Scraper** (Most Popular)
   - URL: https://apify.com/clockworks/tiktok-comments-scraper
   - **Pricing:** $5 per 1,000 comments (pay-per-result)
   - **Success Rate:** 98%
   - **Speed:** Processes 100-200 comments per second
   - **Data Extracted:**
     - Comment text (full text)
     - User ID and username
     - Timestamp
     - Number of likes
     - Number of replies
     - Reply content (nested)
   - **Pros:**
     - Reliable and well-maintained
     - No-code interface
     - API access available
     - Handles pagination automatically
   - **Cons:**
     - Shared proxies may occasionally have issues
     - Cost adds up for large-scale projects

2. **Epctex TikTok Comment Scraper**
   - URL: https://apify.com/epctex/tiktok-comment-scraper
   - Similar pricing and features to Clockworks
   - Alternative if primary scraper has issues

3. **Apidojo TikTok Comments Scraper (Pay Per Result)**
   - URL: https://apify.com/apidojo/tiktok-comments-scraper
   - Similar pricing structure
   - Another reliable backup option

### 1.2 SocialKit API

**Overview:**
- Specialized API for social media video data
- URL: https://www.socialkit.dev/tiktok-comments-api

**Pricing (2025):**
- **Starter:** $13/month for 2,000 credits
- **Growth:** $27/month for 10,000 credits (RECOMMENDED)
- **Pro:** $79/month for 50,000 credits
- **Free Trial:** 20 free API credits to test

**Features:**
- Comments extraction with metadata
- Includes transcripts and AI video summaries
- Unified pricing across all social platforms
- Developer-friendly API with good documentation

**Best For:**
- Projects needing multiple data types (comments + transcripts + summaries)
- Ongoing monthly comment collection
- Budget-conscious projects with predictable volume

### 1.3 Other TikTok Solutions

**Bright Data TikTok Scraper:**
- **Pricing:** Starts at $500/month minimum
- **Pros:** Enterprise-grade reliability (99.99% uptime), officially maintained
- **Cons:** Expensive for comment-only extraction
- **Recommendation:** Only for enterprise budgets or multi-platform needs

**Octoparse TikTok Video Comments Scraper:**
- **Pricing:** $0.40 per 1,000 lines
- **Pros:** Very low cost, no-code interface
- **Cons:** Less well-documented than Apify
- **Recommendation:** Good budget alternative

**Free/Low-Cost Options:**
- **TTCommentExporter (Chrome Extension):** Free, manual process, good for small batches
- **GitHub TikTokCommentScraper:** Free, requires Python setup, DIY approach
- **CommentPicker TikTok Export:** Free web tool, limited to smaller datasets

### 1.4 TikTok Official Research API

**Status:** Extremely Limited Access

**Requirements:**
- Must be affiliated with US non-profit academic institution
- Demonstrable academic experience in research area
- No conflicts of interest
- Clearly defined research proposal
- Ethical review board approval
- Application process takes ~4 weeks

**Restrictions:**
- Limited to researchers in US, UK, Switzerland, Norway, Iceland, Liechtenstein
- Data must be refreshed every 15 days
- Cannot share data with others
- Must send papers to TikTok 30 days in advance
- Limited to 1,000 requests per day
- Only provides partial snapshots

**Verdict:** Not viable for commercial projects or most research applications

---

## 2. INSTAGRAM COMMENTS - WORKING APPROACHES

### 2.1 Apify Instagram Comment Scrapers

**Main Options:**

1. **Apify Official Instagram Comments Scraper**
   - URL: https://apify.com/apify/instagram-comment-scraper
   - **Pricing:** $2.30 per 1,000 comments
   - **Features:**
     - Comment ID and text
     - Replies to comments
     - Timestamps
     - Owner info (username, profile picture)
     - Engagement metrics
   - **Important Limitation:** Only extracts comments visible to non-logged-in users
   - **Export Formats:** JSON, XML, CSV, Excel, HTML

2. **Apidojo Instagram Comments Scraper (Pay Per Result)**
   - URL: https://apify.com/apidojo/instagram-comments-scraper
   - **Pricing:** $0.50 per 1,000 comments (cheaper!)
   - **Speed:** 100-200 comments per second
   - **Recommended** for budget-conscious projects

### 2.2 Bright Data Instagram Solutions

**Instagram Comments Scraper API:**
- URL: https://brightdata.com/products/web-scraper/instagram/comments
- **Pricing:** Estimated $0.001 per record + base subscription
  - Subscription starts at $499/month OR
  - Pay-as-you-go starts at $1 per 1,000 results
- **Current Promotion:** Matched deposit up to $500 (deposit $500, get $1,000 total)

**Features:**
- Retrieves latest 10 comments per post with metadata
- Can collect multiple comments by providing post URL
- Template-based scraping (instagram-comments-collect by URL)
- GDPR/CCPA compliant
- 99.99% uptime SLA

**Data Extracted:**
- Post ID
- Comment text
- Position
- Timestamp
- Username
- Additional metadata

**Best For:**
- Enterprise projects requiring SLA guarantees
- Multi-platform scraping needs
- Projects with existing Bright Data infrastructure

### 2.3 Instaloader - Open Source Solution

**Status:** HIGH BAN RISK in 2025

**Current Version:** v4.14.2 (July 2025)

**Ban Rate Reality:**
- Multiple GitHub issues reporting account suspensions
- Even moderate usage triggers security warnings
- Rate limits have become much stricter (exact thresholds undisclosed)
- Instagram actively detects automated behavior
- Users reporting detection even at slowest scraping rates
- Risk of losing Instagram accounts (temporary or permanent bans)

**Verdict:** NOT RECOMMENDED for November 2025
- Too risky for valuable accounts
- Unreliable for production use
- Better alternatives exist

### 2.4 Other Instagram Solutions

**Free/Low-Cost Options:**

1. **Picuki** (Free Instagram Viewer)
   - View public comments without logging in
   - Manual browsing only
   - No bulk export
   - Good for spot-checking data

2. **Dumpor** (Free Anonymous Viewer)
   - Similar to Picuki
   - View public comments without login
   - No extraction capabilities

3. **IG Exporter & Scraper (Chrome Extension)**
   - Free Chrome extension
   - Exports to CSV/Excel
   - Available on Chrome Web Store
   - Good for small-scale manual extraction

**Paid Tools:**

1. **Thunderbit AI Web Scraper**
   - Chrome extension with AI
   - Free version available
   - Premium: $9.99/month
   - User-friendly for non-technical users

2. **PhantomBuster Instagram Comment Extractor**
   - Cloud-based automation
   - Plans start at $39/month
   - 14-day free trial
   - Pre-built scripts for non-technical users
   - Good for marketing/sales teams

3. **ScrapingBee Instagram API**
   - 1,000 free API calls
   - Developer-focused
   - Lower success rates on Instagram than competitors
   - Not recommended as primary solution

---

## 3. FEASIBILITY ANALYSIS

### 3.1 TikTok Comments - HIGHLY FEASIBLE

**Easiest to Implement:**
- Apify Clockworks TikTok Comments Scraper
- Setup time: 1-2 hours
- No coding required for basic use
- API available if needed

**Cost Breakdown (Monthly):**
- **Small Project** (10K comments/month): $50/month
- **Medium Project** (50K comments/month): $250/month
- **Large Project** (200K comments/month): $1,000/month

**Alternative Budget Option:**
- SocialKit Growth Plan: $27/month for 10K credits
- Better value if you need 10K+ comments monthly
- Includes bonus features (transcripts, summaries)

**Data Quality:** EXCELLENT
- 98% success rate
- Complete comment text and metadata
- Reliable pagination handling
- Nested replies included

**Timeline:**
- **Setup:** 1-2 hours (create account, configure scraper)
- **First Run:** Minutes
- **Ongoing Maintenance:** Minimal (monitored by platform)

**Code Complexity:**
- **No-Code Option:** Simple web interface
- **API Integration:** Moderate (well-documented)
- **Example API Call:** ~10 lines of Python code

### 3.2 Instagram Comments - MODERATE FEASIBILITY

**Easiest to Implement:**
- Apify Instagram Comments Scraper (cheaper option)
- Setup time: 2-4 hours
- Requires rate limiting strategy
- Ongoing monitoring needed

**Cost Breakdown (Monthly):**
- **Small Project** (10K comments/month): $5-23/month
- **Medium Project** (50K comments/month): $25-115/month
- **Large Project** (200K comments/month): $100-460/month

**Enterprise Option:**
- Bright Data: $499/month minimum
- Best for projects requiring SLAs
- 99.99% uptime guarantee

**Data Quality:** GOOD (with caveats)
- Only public comments (non-logged-in view)
- Success rate varies with rate limiting
- May miss some comments
- Requires careful proxy management

**Timeline:**
- **Setup:** 2-4 hours (account, configuration, rate limit testing)
- **First Run:** Minutes to hours (depends on volume)
- **Ongoing Maintenance:** Regular monitoring needed
- **Issue Resolution:** Could require adjustments if detection occurs

**Code Complexity:**
- **No-Code Option:** Available but needs configuration
- **API Integration:** Moderate to Complex
- **Requires:** Proxy rotation, rate limiting, error handling

**Key Challenges:**
1. Rate limiting (stay under 1,000 requests/hour per IP)
2. Detection avoidance (randomized delays, behavior mimicking)
3. Incomplete data (only public comments)
4. Platform changes (Instagram updates defenses frequently)

### 3.3 Comparison Matrix

| Factor | TikTok | Instagram |
|--------|--------|-----------|
| **Implementation Difficulty** | Easy | Moderate |
| **Cost (per 1K comments)** | $0.40-$5.00 | $0.50-$2.30 |
| **Data Quality** | Excellent | Good |
| **Success Rate** | 98% | Variable (70-95%) |
| **Ban Risk** | Low | Moderate to High |
| **Maintenance Burden** | Low | Moderate |
| **Setup Time** | 1-2 hours | 2-4 hours |
| **Reliability** | High | Moderate |
| **Best For** | Production use | Careful/limited use |

---

## 4. CONCRETE RECOMMENDATIONS

### 4.1 For TikTok Comment Extraction

**RECOMMENDED SOLUTION:**

**Option A: Apify Clockworks TikTok Comments Scraper** (Best for most projects)

**Why This Choice:**
- Proven reliability (98% success rate)
- No-code interface for ease of use
- API available for automation
- Predictable pricing
- Handles all technical complexity
- Low maintenance burden

**When to Use:**
- Any project size
- Need reliable, production-ready solution
- Want to focus on analysis, not infrastructure
- Budget allows ~$5 per 1,000 comments

**Implementation Steps:**
1. Create free Apify account (https://apify.com)
2. Add payment method (get $5 free credit)
3. Navigate to Clockworks TikTok Comments Scraper
4. Add TikTok video URLs to input
5. Configure output format (JSON/CSV recommended)
6. Run scraper
7. Download results or access via API

**Estimated Costs:**
- 10K comments: $50
- 50K comments: $250
- 100K comments: $500

---

**Option B: SocialKit API** (Best value for ongoing collection)

**Why This Choice:**
- Better value at scale ($27/month for 10K comments)
- Includes bonus features (transcripts, AI summaries)
- Developer-friendly API
- Unified pricing across platforms
- 20 free credits to test

**When to Use:**
- Need 5K+ comments monthly
- Want transcripts or summaries too
- Prefer predictable monthly costs
- Building automated collection pipeline

**Implementation Steps:**
1. Sign up at https://www.socialkit.dev
2. Start with free 20 credits to test
3. Choose Growth plan ($27/month) if satisfied
4. Integrate API into your workflow
5. Use API documentation for endpoints

**Estimated Monthly Costs:**
- Growth Plan: $27/month (10K credits)
- Pro Plan: $79/month (50K credits)
- Much cheaper per comment at higher volumes

---

**Option C: Budget/DIY Approach** (For small projects or learning)

**Tools:**
- TTCommentExporter (Chrome Extension) - Free
- GitHub TikTokCommentScraper - Free, requires Python setup
- Octoparse Template - $0.40/1K lines (cheapest paid option)

**When to Use:**
- Very small volume (<1K comments)
- One-time extraction need
- Learning/educational purpose
- Zero budget constraint

**Trade-offs:**
- More manual work required
- Less reliable
- No support
- Limited scale

---

### 4.2 For Instagram Comment Extraction

**RECOMMENDED SOLUTION:**

**Option A: Apify Instagram Comments Scraper (Apidojo)** (Best balance)

**Why This Choice:**
- Most affordable ($0.50 per 1,000 comments)
- Fast (100-200 comments/second)
- Established platform with support
- Good success rates with proper configuration
- Multiple export formats

**When to Use:**
- Public posts only (not private accounts)
- Can accept rate limiting constraints
- Budget-conscious projects
- Don't need 100% of comments (public view sufficient)

**Implementation Steps:**
1. Create Apify account
2. Navigate to Apidojo Instagram Comments Scraper
3. Add Instagram post URLs
4. Configure proxy settings (use good proxies)
5. Set rate limits conservatively:
   - Max 1,000 requests per hour per IP
   - Add 3-10 second delays between requests
   - Randomize delay intervals
6. Run scraper with monitoring
7. Export data in preferred format

**Critical Setup Requirements:**
- Use residential or mobile proxies (not datacenter)
- Implement rotating proxy strategy (change every 100-200 requests)
- Stay under 1,000 requests/hour per IP
- Add randomized delays (3-10 seconds)
- Monitor for rate limit warnings

**Estimated Costs:**
- 10K comments: $5
- 50K comments: $25
- 100K comments: $50

**Expected Success Rate:** 70-85% (depends on rate limiting strategy)

---

**Option B: Bright Data Instagram Comments API** (Best for enterprise)

**Why This Choice:**
- Highest reliability (99.99% uptime SLA)
- Best success rates (99.48% reported)
- Enterprise support
- GDPR/CCPA compliant infrastructure
- Officially maintained scrapers
- Fast response times

**When to Use:**
- Enterprise projects
- Need SLA guarantees
- Already using Bright Data for other scraping
- Budget allows $500+ monthly
- Multi-platform scraping needs

**Implementation Steps:**
1. Sign up for Bright Data account
2. Choose plan (starts at $499/month or pay-as-you-go)
3. Take advantage of matched deposit promotion (deposit $500, get $1,000)
4. Use instagram-comments-collect template
5. Configure API endpoints
6. Implement in your workflow

**Estimated Costs:**
- Base subscription: $499/month OR
- Pay-as-you-go: $1 per 1,000 results
- Better value at very high volumes

**Expected Success Rate:** 95%+

---

**Option C: Manual/Small-Scale Approach**

**Tools:**
- IG Exporter & Scraper Chrome Extension (Free)
- Thunderbit AI Scraper ($9.99/month)
- PhantomBuster (14-day trial, then $39/month)

**When to Use:**
- Very small volume (<5K comments)
- One-time project
- Learning purposes
- Testing before scaling

**Trade-offs:**
- Manual effort required
- Not scalable
- Limited to visible comments
- Time-consuming

---

### 4.3 Implementation Difficulty Rating

**TikTok (Easy - Recommended for beginners):**
```
Setup Complexity:        ★★☆☆☆ (2/5)
Coding Required:         ★☆☆☆☆ (1/5) - Optional
Maintenance:             ★☆☆☆☆ (1/5)
Reliability Issues:      ★☆☆☆☆ (1/5)
Ban Risk:                ★☆☆☆☆ (1/5)

Overall Difficulty:      ★★☆☆☆ (2/5) - EASY
```

**Instagram (Moderate - Requires careful approach):**
```
Setup Complexity:        ★★★☆☆ (3/5)
Coding Required:         ★★☆☆☆ (2/5) - Helpful but optional
Maintenance:             ★★★☆☆ (3/5)
Reliability Issues:      ★★★☆☆ (3/5)
Ban Risk:                ★★★★☆ (4/5)

Overall Difficulty:      ★★★☆☆ (3/5) - MODERATE
```

---

### 4.4 Expected Success Rates

**TikTok:**
- **Apify/SocialKit:** 95-98% of comments extracted
- **Issues:** Rare proxy problems, platform changes
- **Downtime:** Minimal
- **Data Completeness:** Excellent (includes replies, metadata)

**Instagram:**
- **Apify (with good practices):** 70-85% of PUBLIC comments
- **Bright Data:** 90-95% of PUBLIC comments
- **Issues:** Rate limiting, detection, incomplete data
- **Downtime:** Possible during high-volume collection
- **Data Completeness:** Good for public data, missing private comments

---

### 4.5 Cost-Benefit Summary

**TikTok - Clear Winner:**
- Higher cost per comment BUT
- Much higher reliability
- Less maintenance
- Better data quality
- Lower total cost of ownership (when factoring in time/issues)

**Instagram - Proceed with Caution:**
- Lower cost per comment BUT
- Requires more setup and monitoring
- Incomplete data (public only)
- Higher maintenance burden
- Risk of detection/bans
- Higher total cost of ownership (when factoring in time/issues)

---

## 5. ACTION PLAN

### For Immediate Implementation

**If you need TikTok comments:**

1. **Day 1:**
   - Sign up for Apify account
   - Test with free $5 credit
   - Run test extraction on 2-3 videos
   - Verify data quality meets needs

2. **Day 2:**
   - If test successful, add payment method
   - Scale up to full extraction
   - OR switch to SocialKit if volume justifies ($27/month for 10K credits)

3. **Week 1:**
   - Monitor first production runs
   - Adjust configuration as needed
   - Minimal issues expected

**Total Setup Time:** 2-4 hours
**Expected Issues:** Minimal
**Confidence Level:** HIGH

---

**If you need Instagram comments:**

1. **Day 1:**
   - Sign up for Apify account
   - Research best proxy providers
   - Test with free credit on small dataset
   - Configure conservative rate limits

2. **Day 2-3:**
   - Run larger test (500-1,000 comments)
   - Monitor for rate limit warnings
   - Adjust delays and proxy rotation
   - Verify data completeness

3. **Week 1:**
   - Gradually scale up volume
   - Monitor success rates closely
   - Be prepared to adjust strategy
   - Consider Bright Data if issues persist

4. **Ongoing:**
   - Weekly monitoring of success rates
   - Adjust rate limits as needed
   - Stay updated on Instagram changes

**Total Setup Time:** 4-8 hours
**Expected Issues:** Moderate (rate limiting, incomplete data)
**Confidence Level:** MODERATE

---

### Risk Mitigation Strategies

**For TikTok:**
- Minimal risk, but keep backup scraper bookmarked (epctex or apidojo)
- Monitor Apify status page for outages
- Export data regularly (don't rely on cloud storage only)

**For Instagram:**
- Start with very small batches (100 comments)
- Gradually increase volume while monitoring
- Use multiple proxy providers for redundancy
- Have Bright Data as backup if Apify fails
- Accept that 100% extraction is not realistic
- Document which posts were successfully scraped
- Plan for re-runs if detection occurs

---

## 6. FINAL VERDICT

### TikTok: HIGHLY RECOMMENDED

**Bottom Line:**
- Reliable, production-ready solutions exist
- Reasonable pricing for most use cases
- Low maintenance burden
- Excellent data quality
- Safe to proceed with confidence

**Best Choice:**
- <10K comments monthly: Apify pay-per-result ($5/1K)
- 10K+ comments monthly: SocialKit ($27/month for 10K)
- Enterprise: Bright Data ($500+/month)

**Success Likelihood:** 95%+

---

### Instagram: PROCEED WITH CAUTION

**Bottom Line:**
- Functional solutions exist but require careful implementation
- Lower cost per comment but higher hidden costs (time, monitoring)
- Moderate to high maintenance burden
- Good (not excellent) data quality
- Notable limitations and risks

**Best Choice:**
- Budget projects: Apify Apidojo ($0.50/1K)
- Enterprise/SLA needs: Bright Data ($499+/month)
- Small volume: Manual tools (free-$10/month)

**Success Likelihood:** 70-85% (with proper configuration)

**Key Limitations:**
- Only public comments extracted
- Risk of rate limiting/detection
- Requires ongoing monitoring
- May not capture 100% of comments

---

## 7. ADDITIONAL CONSIDERATIONS

### Legal and Ethical Notes

**Both Platforms:**
- Only extract publicly available data
- Respect terms of service
- Consider data protection regulations (GDPR, CCPA)
- Don't extract personal/private information
- Use data responsibly

**TikTok:**
- Terms of service prohibit unauthorized scraping
- However, widely done for research/analysis
- Apify scrapers "ethical" (public data only)
- Lower enforcement compared to Instagram

**Instagram:**
- More aggressive about preventing scraping
- Higher legal risk (CFAA in U.S.)
- Can result in account bans
- Use at your own risk

### Technical Skills Required

**TikTok (Minimal):**
- Can use entirely through web interface
- No coding required
- API integration optional (for automation)
- Basic understanding of JSON/CSV helpful

**Instagram (Moderate):**
- Web interface available but configuration needed
- Understanding of rate limiting helpful
- Proxy knowledge beneficial
- API integration useful for error handling
- Monitoring and adjustment skills needed

---

## 8. RESOURCES

### TikTok Solutions

**Apify Actors:**
- Clockworks TikTok Comments: https://apify.com/clockworks/tiktok-comments-scraper
- Epctex TikTok Comments: https://apify.com/epctex/tiktok-comment-scraper
- Apidojo TikTok Comments: https://apify.com/apidojo/tiktok-comments-scraper

**SocialKit:**
- Main site: https://www.socialkit.dev
- TikTok Comments API: https://www.socialkit.dev/tiktok-comments-api
- Pricing: https://www.socialkit.dev/pricing

**Free Tools:**
- TTCommentExporter: Chrome Web Store
- GitHub TikTok Comment Scraper: https://github.com/cubernetes/TikTokCommentScraper

### Instagram Solutions

**Apify Actors:**
- Official Instagram Comments: https://apify.com/apify/instagram-comment-scraper
- Apidojo Instagram Comments: https://apify.com/apidojo/instagram-comments-scraper

**Bright Data:**
- Instagram Comments Scraper: https://brightdata.com/products/web-scraper/instagram/comments
- Pricing: https://brightdata.com/pricing/web-scraper

**Free/Low-Cost:**
- IG Exporter & Scraper: Chrome Web Store
- Thunderbit: https://thunderbit.com
- PhantomBuster: https://phantombuster.com

### Learning Resources

**Scraping Tutorials:**
- Apify Blog: https://blog.apify.com/how-to-scrape-tiktok-tutorial/
- Scrapfly TikTok Guide: https://scrapfly.io/blog/posts/how-to-scrape-tiktok-python-json
- Instagram Scraping Guide: https://scrapfly.io/blog/posts/how-to-scrape-instagram

**Best Practices:**
- Instagram Detection Avoidance: https://www.coronium.io/blog/instagram-scraper-guide
- Rate Limiting Strategies: Multiple resources in search results
- Proxy Setup Guides: Available from Bright Data, Apify

---

## 9. CONCLUSION

Based on extensive research of current (November 2025) solutions:

**TikTok comment extraction is HIGHLY VIABLE:**
- Multiple reliable, production-ready solutions
- Reasonable costs
- High success rates
- Low technical barriers
- Recommended to proceed

**Instagram comment extraction is MODERATELY VIABLE:**
- Working solutions exist but with caveats
- Requires more careful implementation
- Ongoing monitoring needed
- Accept limitations (public comments only)
- Proceed with appropriate caution and monitoring

**Overall Recommendation:**
Start with TikTok extraction to build confidence and infrastructure. Once successful, carefully expand to Instagram if needed, starting with small-scale tests and gradually scaling while monitoring success rates and detection risks.

---

**Document Version:** 1.0
**Last Updated:** November 11, 2025
**Next Review:** December 2025 (platforms change frequently)
