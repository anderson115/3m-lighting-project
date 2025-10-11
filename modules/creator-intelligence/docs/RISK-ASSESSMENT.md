# Risk Assessment & Mitigation Plan

**Module:** Creator Intelligence
**Version:** 1.0.0
**Last Updated:** 2025-10-10

---

## 🎯 Executive Summary

This document identifies risks associated with grey-area scraping methods (Instagram Instaloader, TikTok Playwright) and provides mitigation strategies. User has explicitly approved aggressive tactics for comprehensive platform coverage.

**Risk Tolerance:** MODERATE-HIGH (grey-area methods accepted for Instagram/TikTok)

---

## 🔴 HIGH-RISK AREAS

### 1. Instagram Scraping (Instaloader) - Risk Level: 🔴 HIGH

**Risk:** Account bans, 429 rate limits, IP blocks

**Likelihood:** HIGH (80%+ if used as primary method)

**Impact:**
- Loss of Instagram data collection capability
- Potential IP blacklisting
- Wasted development time

**Mitigation Strategies:**

| Strategy | Effectiveness | Implementation |
|----------|---------------|----------------|
| **Use Apify as primary** | ⭐⭐⭐⭐⭐ | Always try Apify first, Instaloader only as fallback |
| **Extreme rate limiting** | ⭐⭐⭐⭐ | 120-180 second delays between requests |
| **No authentication** | ⭐⭐⭐⭐ | Public profiles only, never log in |
| **Proxy rotation** | ⭐⭐⭐ | Rotate residential proxies if available |
| **Circuit breaker** | ⭐⭐⭐⭐ | Stop immediately on 429 error for 24 hours |
| **Aggressive caching** | ⭐⭐⭐⭐⭐ | Never re-scrape same profile |

**Code Example:**
```python
class InstagramCircuitBreaker:
    def __init__(self):
        self.ban_detected = False
        self.ban_timestamp = None

    def check_if_safe(self):
        if self.ban_detected:
            hours_since_ban = (datetime.now() - self.ban_timestamp).total_seconds() / 3600
            if hours_since_ban < 24:
                raise Exception(f"Circuit breaker active. Wait {24 - hours_since_ban:.1f} more hours.")
            else:
                self.ban_detected = False  # Reset after 24h

    def trigger_circuit_breaker(self):
        self.ban_detected = True
        self.ban_timestamp = datetime.now()
        logger.critical("🚨 INSTAGRAM BAN DETECTED - STOPPING FOR 24 HOURS")
```

**Monitoring:**
- Log all 429 errors
- Track requests/hour (max 20)
- Alert if any 429 errors occur

---

### 2. TikTok Scraping (Playwright) - Risk Level: 🔴 HIGH

**Risk:** JavaScript puzzles, CAPTCHA challenges, bot detection

**Likelihood:** MEDIUM-HIGH (60% if used as primary method)

**Impact:**
- Scraping failures
- CAPTCHA solve delays
- IP blacklisting

**Mitigation Strategies:**

| Strategy | Effectiveness | Implementation |
|----------|---------------|----------------|
| **Use Apify as primary** | ⭐⭐⭐⭐⭐ | Apify handles anti-detection automatically |
| **Stealth plugins** | ⭐⭐⭐⭐ | `playwright-stealth` masks headless browser |
| **Session recycling** | ⭐⭐⭐⭐ | New browser every 20 requests |
| **Realistic behavior** | ⭐⭐⭐ | Random scrolling, wait times, mouse movements |
| **Proxy rotation** | ⭐⭐⭐⭐ | Mandatory for Playwright (residential proxies) |
| **Low volume** | ⭐⭐⭐⭐ | Max 10 profiles per session |

**Code Example:**
```python
from playwright_stealth import stealth_sync

def create_stealth_browser():
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
        viewport={'width': 1920, 'height': 1080},
        locale='en-US',
        timezone_id='America/New_York'
    )
    page = context.new_page()
    stealth_sync(page)  # Apply stealth techniques
    return browser, page
```

**Monitoring:**
- Detect CAPTCHA challenges (check for specific DOM elements)
- Log failed page loads
- Track success rate (should be >70%)

---

### 3. YouTube API Quota Exhaustion - Risk Level: 🟡 MEDIUM

**Risk:** Exceeding 10,000 units/day, blocking further scraping

**Likelihood:** HIGH (90% if analyzing 500+ creators)

**Impact:**
- Pipeline stops mid-execution
- Must wait 24 hours for quota reset
- Delayed deliverables

**Mitigation Strategies:**

| Strategy | Effectiveness | Implementation |
|----------|---------------|----------------|
| **Aggressive caching** | ⭐⭐⭐⭐⭐ | Never call API for same data twice |
| **Quota monitoring** | ⭐⭐⭐⭐ | Check remaining quota before each search |
| **Request quota increase** | ⭐⭐⭐⭐⭐ | Request 100K-1M units/day from Google |
| **Batch operations** | ⭐⭐⭐ | Combine API calls where possible |
| **Prioritize high-value** | ⭐⭐⭐ | Scrape most relevant creators first |

**Code Example:**
```python
def check_youtube_quota(youtube_client):
    # YouTube API doesn't expose quota directly
    # Use estimate based on requests made
    estimated_used = request_count * avg_cost_per_request
    estimated_remaining = 10000 - estimated_used

    if estimated_remaining < 500:
        logger.warning(f"⚠️ Low YouTube quota: ~{estimated_remaining} units remaining")
        return False
    return True
```

**Quota Increase Process:**
1. Submit quota increase request: https://support.google.com/youtube/contact/yt_api_form
2. Provide use case: "Market research for lighting industry creators"
3. Demonstrate compliance: Data privacy policy, Terms of Service adherence
4. Typical approval time: 1-2 weeks
5. Recommended quota: 100,000 units/day (10x default)

---

### 4. Apify Cost Overrun - Risk Level: 🟡 MEDIUM

**Risk:** Exceeding 5,000 free credits/month

**Likelihood:** HIGH (90% if analyzing 500+ creators)

**Impact:**
- Unexpected costs ($49-199/month)
- Need to switch to riskier fallback methods

**Mitigation Strategies:**

| Strategy | Effectiveness | Implementation |
|----------|---------------|----------------|
| **Credit monitoring** | ⭐⭐⭐⭐⭐ | Dashboard alerts at 4,000 credits |
| **Staged rollout** | ⭐⭐⭐⭐ | Analyze 250 creators/month to stay within free tier |
| **Cost budgeting** | ⭐⭐⭐⭐ | Allocate $49/month for paid tier if needed |
| **Prioritize YouTube/Etsy** | ⭐⭐⭐ | Focus on free APIs first |

**Cost Projection:**

| Creator Count | Instagram Credits | TikTok Credits | Total Credits | Cost |
|---------------|-------------------|----------------|---------------|------|
| 100 | 500 (50 profiles) | 750 (50 profiles) | 1,250 | $0 (free tier) |
| 250 | 1,250 | 1,875 | 3,125 | $0 (free tier) |
| 500 | 2,500 | 3,750 | 6,250 | $49/month (50K credits) |
| 1,000 | 5,000 | 7,500 | 12,500 | $49/month |

**Recommendation:** Start with 250 creators to validate module, then upgrade to paid tier if needed.

---

## 🟠 MEDIUM-RISK AREAS

### 5. LLM Classification Errors - Risk Level: 🟠 MEDIUM

**Risk:** False positives (irrelevant creators classified as relevant)

**Likelihood:** MEDIUM (30-40% misclassification rate)

**Impact:**
- Polluted database with irrelevant creators
- Wasted scraping quota on bad leads
- Client receives low-quality insights

**Mitigation Strategies:**

| Strategy | Effectiveness | Implementation |
|----------|---------------|----------------|
| **Confidence threshold** | ⭐⭐⭐⭐ | Only accept confidence >70% |
| **Manual spot-checks** | ⭐⭐⭐⭐⭐ | Validate 50 random creators |
| **A/B test prompts** | ⭐⭐⭐ | Test multiple prompt templates |
| **Feedback loop** | ⭐⭐⭐ | Retrain prompts based on false positives |

**Testing Plan:**
1. Classify 100 known-good creators (manual verification)
2. Measure accuracy (target: >80%)
3. Classify 100 known-irrelevant creators
4. Measure false positive rate (target: <20%)
5. Adjust confidence threshold if needed

---

### 6. Database Scalability - Risk Level: 🟠 MEDIUM

**Risk:** SQLite performance degrades beyond 10,000 creators

**Likelihood:** LOW (only if scaling beyond initial scope)

**Impact:**
- Slow queries (>5 seconds)
- Report generation delays
- Need for database migration

**Mitigation Strategies:**

| Strategy | Effectiveness | Implementation |
|----------|---------------|----------------|
| **Proper indexing** | ⭐⭐⭐⭐⭐ | Index platform, scores, country fields |
| **Query optimization** | ⭐⭐⭐⭐ | Use WHERE clauses, limit results |
| **PostgreSQL migration** | ⭐⭐⭐⭐⭐ | Switch to PostgreSQL at 5,000+ creators |
| **Pagination** | ⭐⭐⭐ | Don't load all creators at once |

**Performance Benchmarks:**

| Creator Count | Query Time (SQLite) | Recommendation |
|---------------|---------------------|----------------|
| 1,000 | <1s | ✅ SQLite OK |
| 5,000 | 1-3s | ⚠️ Monitor performance |
| 10,000 | 3-8s | 🔴 Migrate to PostgreSQL |
| 50,000+ | >10s | 🔴 PostgreSQL mandatory |

---

## 🟢 LOW-RISK AREAS

### 7. Official API Changes - Risk Level: 🟢 LOW

**Risk:** YouTube/Etsy API endpoints change structure

**Likelihood:** LOW (10% per year)

**Impact:**
- Scraping failures
- Need for code updates

**Mitigation:**
- Monitor API changelogs
- Wrap API calls in try/except with detailed logging
- Version pin API client libraries

---

### 8. LLM API Outages - Risk Level: 🟢 LOW

**Risk:** Anthropic Claude API temporarily unavailable

**Likelihood:** LOW (5% during pipeline run)

**Impact:**
- Analysis phase fails
- Must retry later

**Mitigation:**
- Exponential backoff retry (5s, 10s, 20s, 60s)
- Fallback to OpenAI GPT-4o if Claude fails
- Queue LLM tasks separately from scraping

---

## 📊 **Risk Matrix**

| Risk | Likelihood | Impact | Risk Level | Priority |
|------|-----------|--------|------------|----------|
| Instagram ban (Instaloader) | HIGH | HIGH | 🔴 CRITICAL | P1 |
| TikTok detection (Playwright) | MEDIUM | HIGH | 🔴 HIGH | P1 |
| YouTube quota exhaustion | HIGH | MEDIUM | 🟡 MEDIUM | P2 |
| Apify cost overrun | HIGH | LOW | 🟡 MEDIUM | P2 |
| LLM classification errors | MEDIUM | MEDIUM | 🟠 MEDIUM | P3 |
| Database scalability | LOW | MEDIUM | 🟠 LOW | P4 |
| API changes | LOW | LOW | 🟢 LOW | P5 |
| LLM outages | LOW | LOW | 🟢 LOW | P5 |

---

## 🚨 **Incident Response Plan**

### Scenario 1: Instagram 429 Ban Detected

**Trigger:** HTTP 429 status code from Instagram

**Response:**
1. **STOP immediately** - activate circuit breaker
2. Log incident with timestamp
3. Wait 24 hours before retrying
4. Switch to Apify for remaining Instagram creators
5. Review rate limiting settings (increase delays to 5 min)

---

### Scenario 2: TikTok CAPTCHA Challenge

**Trigger:** CAPTCHA detected in Playwright page

**Response:**
1. Take screenshot of CAPTCHA
2. Log incident
3. Close browser session
4. Switch to Apify for remaining TikTok creators
5. If Apify also fails, skip TikTok for this run

---

### Scenario 3: YouTube Quota Exhausted

**Trigger:** API returns 403 quota exceeded

**Response:**
1. Log remaining creators not scraped
2. Cache all data collected so far
3. Generate partial report with disclaimer
4. Schedule resume for next day (quota resets midnight PT)
5. Submit quota increase request if recurring

---

### Scenario 4: Apify Credits Depleted

**Trigger:** Apify returns insufficient credits error

**Response:**
1. Calculate remaining creators needed
2. **Option A:** Upgrade to paid tier ($49/month)
3. **Option B:** Switch to aggressive fallback (Instaloader + Playwright) for remaining creators
4. **Option C:** Pause and resume next month (free tier resets)

---

## 📈 **Risk Monitoring Dashboard**

### Key Metrics to Track

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Instagram 429 errors | 0 | Alert on any 429 |
| TikTok CAPTCHA rate | <10% | Alert if >15% |
| YouTube quota usage | <8,000/day | Alert at 9,000 |
| Apify credits used | <4,000/month | Alert at 4,500 |
| LLM classification accuracy | >80% | Alert if <75% |
| Database query time | <2s | Alert if >5s |
| Scraping success rate | >90% | Alert if <80% |

**Monitoring Implementation:**
```python
class RiskMonitor:
    def __init__(self):
        self.metrics = {
            'instagram_429_count': 0,
            'tiktok_captcha_count': 0,
            'youtube_quota_used': 0,
            'apify_credits_used': 0,
            'llm_false_positives': 0
        }

    def log_incident(self, incident_type: str):
        self.metrics[incident_type] += 1

        # Trigger alerts
        if incident_type == 'instagram_429_count' and self.metrics[incident_type] > 0:
            self.send_alert("🚨 CRITICAL: Instagram ban detected")

        if incident_type == 'tiktok_captcha_count' and self.metrics[incident_type] > 10:
            self.send_alert("⚠️ WARNING: High TikTok CAPTCHA rate")

    def send_alert(self, message: str):
        logger.critical(message)
        # Could also send email, Slack notification, etc.
```

---

## 📝 **Legal & Compliance Considerations**

### Grey-Area Scraping Disclaimer

**User Directive:** "i do not care about fair use principles or usage agreements. attack the grey area for solutions that will work."

**Legal Status:**
- Instagram Terms of Service: **VIOLATED** (prohibits automated access)
- TikTok Terms of Service: **VIOLATED** (prohibits scraping)
- Potential consequences: Account bans, IP blocks, cease-and-desist letters

**Recommendations:**
1. **For internal use only** - do not redistribute scraped data
2. **Market research defense** - scraping for competitive intelligence (not redistribution)
3. **Consult legal counsel** before commercial deployment
4. **GDPR/CCPA compliance** - only scrape public data, honor deletion requests

---

## ✅ **Risk Acceptance**

**Stakeholder:** User has explicitly approved aggressive tactics

**Accepted Risks:**
- Instagram account bans (using Instaloader as fallback)
- TikTok bot detection (using Playwright as fallback)
- Terms of Service violations (Instagram, TikTok)
- Potential IP blacklisting (mitigated by proxies)

**Rejected Risks:**
- None - all risks accepted with mitigation strategies

---

## 📞 **Escalation Procedures**

### When to Escalate

- **Level 1 (Info):** Single scraping failure, retry successful
- **Level 2 (Warning):** Multiple failures (>10%), failover triggered
- **Level 3 (Error):** Platform completely unavailable, all methods fail
- **Level 4 (Critical):** Account ban, IP blacklist, legal threat

### Escalation Actions

| Level | Action | Notify |
|-------|--------|--------|
| 1 | Log and retry | None |
| 2 | Switch to fallback method | Developer (log warning) |
| 3 | Pause platform scraping | Project Manager |
| 4 | Stop all scraping | Stakeholder + Legal |

---

**END OF RISK ASSESSMENT**

**Status:** ✅ Risks identified and mitigation strategies defined

**Next Steps:**
1. Review risk mitigation strategies
2. Implement monitoring dashboard
3. Prepare incident response procedures
4. Begin implementation with risk awareness
