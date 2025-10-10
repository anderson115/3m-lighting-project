# Citation Integrity Protocol - Expert Authority Module

**Purpose:** Ensure all insights are traceable, verifiable, and free from fabrication or hallucination.

**Status:** MANDATORY - All tiers must implement this protocol

---

## 🎯 **Core Principle: Zero Tolerance for Fabrication**

Every insight, quote, or statistic MUST be:
1. ✅ Directly sourced from raw scraped data (not LLM-generated)
2. ✅ Linked to original discussion with permanent URL
3. ✅ Validated against source before inclusion in report
4. ✅ Timestamped with scraping date for currency tracking

**If a citation cannot be validated → Do not include in report**

---

## 📋 **Citation Requirements by Content Type**

### **1. Expert Quotes (Verbatim)**
**Required Fields:**
```json
{
  "quote": "Standard LED strip adhesive fails above 100°F. Use 3M VHB 5952 tape rated for 150°F.",
  "author": "SparkyElectrician",
  "platform": "Reddit",
  "subreddit": "r/electricians",
  "post_id": "abc123xyz",
  "comment_id": "def456uvw",
  "url": "https://reddit.com/r/electricians/comments/abc123xyz/led_strip_mounting/def456uvw",
  "timestamp": "2024-02-10T14:23:45Z",
  "upvotes": 287,
  "expert_tier": 1,
  "scraped_at": "2025-10-09T18:30:00Z",
  "validation_status": "verified"
}
```

**Validation Steps:**
1. Check raw JSON contains exact quote text
2. Verify URL is accessible (HTTP 200)
3. Confirm author, timestamp, upvote count match
4. Flag if URL returns 404 (deleted/removed content)

### **2. Theme/Pattern Claims**
**Required Fields:**
```json
{
  "theme": "Heat-Related Adhesive Failure",
  "frequency": 23,
  "frequency_pct": 15.2,
  "sample_size": 150,
  "evidence_posts": [
    {
      "post_id": "xyz789",
      "url": "https://reddit.com/r/homeimprovement/comments/xyz789",
      "title": "LED strips falling off in Arizona heat",
      "excerpt": "...tape won't hold above 110°F...",
      "relevance_score": 0.89
    }
  ],
  "scraped_from": ["r/electricians", "r/homeimprovement", "r/DIY"],
  "date_range": "2024-01-01 to 2025-10-09"
}
```

**Validation Steps:**
1. Verify frequency count matches raw data
2. Ensure all evidence_posts URLs are valid
3. Confirm theme extraction logic is reproducible
4. Cross-check sample_size against total discussions analyzed

### **3. Consensus Patterns**
**Required Fields:**
```json
{
  "consensus": "3M VHB tape outperforms standard LED strip adhesive in high heat",
  "confidence": "high",
  "supporting_experts": [
    {
      "author": "SparkyElectrician",
      "url": "https://reddit.com/...",
      "quote": "...",
      "upvotes": 287,
      "tier": 1
    },
    {
      "author": "MasterElectrician",
      "url": "https://reddit.com/...",
      "quote": "...",
      "upvotes": 156,
      "tier": 1
    }
  ],
  "agreement_threshold": 0.78,
  "dissenting_opinions": 2,
  "platforms": ["Reddit", "Quora"]
}
```

**Validation Steps:**
1. Verify all supporting_experts URLs are accessible
2. Confirm quotes match raw source data
3. Validate agreement_threshold calculation
4. Document dissenting opinions (transparency)

### **4. Statistical Claims**
**Required Fields:**
```json
{
  "statistic": "18.5% of discussions mention adhesive mounting issues",
  "numerator": 28,
  "denominator": 151,
  "calculation": "28 / 151 * 100 = 18.5%",
  "raw_data_source": "data/raw/reddit_electricians_20251009.json",
  "verification_query": "grep -c 'adhesive|tape|stick|mount' reddit_electricians_20251009.json"
}
```

**Validation Steps:**
1. Recompute statistic from raw data
2. Verify calculation matches claimed value
3. Ensure raw_data_source file exists and is timestamped
4. Flag if discrepancy > 1% (rounding tolerance)

---

## 🔍 **Validation Pipeline**

### **Stage 1: Pre-Processing (During Scraping)**
```python
def scrape_with_validation(url: str) -> Dict:
    """
    Scrape content and validate immediately
    """
    response = requests.get(url)

    # Immediate validation
    assert response.status_code == 200, f"URL inaccessible: {url}"

    data = {
        "url": url,
        "scraped_at": datetime.now().isoformat(),
        "http_status": response.status_code,
        "content": response.text,
        "validation_hash": hashlib.sha256(response.text.encode()).hexdigest()
    }

    # Store validation hash for later integrity checks
    return data
```

### **Stage 2: Post-Processing (After Analysis)**
```python
def validate_citations(report: Dict) -> List[ValidationError]:
    """
    Validate all citations in generated report
    """
    errors = []

    for citation in extract_citations(report):
        # Check 1: URL accessibility
        if not is_url_accessible(citation['url']):
            errors.append({
                "type": "inaccessible_url",
                "citation": citation,
                "severity": "critical"
            })

        # Check 2: Quote verification
        raw_data = load_raw_data(citation['source_file'])
        if not verify_quote_in_raw_data(citation['quote'], raw_data):
            errors.append({
                "type": "quote_not_found",
                "citation": citation,
                "severity": "critical"
            })

        # Check 3: Metadata consistency
        if not verify_metadata(citation, raw_data):
            errors.append({
                "type": "metadata_mismatch",
                "citation": citation,
                "severity": "medium"
            })

    return errors
```

### **Stage 3: Pre-Delivery (Before Client Report)**
```python
def generate_citation_audit_trail(report: Dict) -> Dict:
    """
    Generate audit trail for all citations
    """
    audit = {
        "total_citations": count_citations(report),
        "verified_citations": 0,
        "failed_validations": [],
        "validation_timestamp": datetime.now().isoformat()
    }

    for citation in extract_citations(report):
        validation_result = validate_citation(citation)

        if validation_result['status'] == 'verified':
            audit['verified_citations'] += 1
        else:
            audit['failed_validations'].append({
                "citation": citation,
                "reason": validation_result['reason']
            })

    # Fail if <95% citations verified
    if audit['verified_citations'] / audit['total_citations'] < 0.95:
        raise ValidationError(f"Only {audit['verified_citations']} citations verified")

    return audit
```

---

## 📊 **Citation Format Standards**

### **In-Report Citation Format (HTML)**
```html
<div class="expert-quote">
    <blockquote>
        "Standard LED strip adhesive fails above 100°F. Use 3M VHB 5952 tape rated for 150°F."
    </blockquote>
    <div class="citation">
        <span class="author">— SparkyElectrician</span>
        <span class="platform">Reddit r/electricians</span>
        <span class="date">Feb 10, 2024</span>
        <span class="engagement">287 upvotes</span>
        <a href="https://reddit.com/r/electricians/comments/abc123/led_mounting/def456"
           target="_blank"
           class="source-link">
            [View Original] ↗
        </a>
    </div>
</div>
```

### **Citation Index (End of Report)**
```markdown
## Citation Index

1. **SparkyElectrician** (Reddit r/electricians, Feb 10 2024)
   - Quote: "Standard LED strip adhesive fails above 100°F..."
   - URL: https://reddit.com/r/electricians/comments/abc123/led_mounting/def456
   - Upvotes: 287 | Expert Tier: 1
   - Verified: 2025-10-09

2. **MasterElectrician** (Reddit r/electricians, Mar 15 2024)
   - Quote: "Use outdoor-rated junction boxes (NEMA 3R minimum)..."
   - URL: https://reddit.com/r/electricians/comments/xyz789/outdoor_led/uvw123
   - Upvotes: 156 | Expert Tier: 1
   - Verified: 2025-10-09
```

### **Raw Data Appendix (Tier 3 Only)**
```
## Appendix: Raw Data Archive

All citations validated against:
- reddit_electricians_20251009.json (151 discussions, SHA256: a3f8b2...)
- reddit_homeimprovement_20251009.json (98 discussions, SHA256: d9e4c1...)
- quora_lighting_20251009.json (76 answers, SHA256: 7b5a8f...)

Archive URL: [Download Raw Data Package] (Tier 3 only)
```

---

## 🚨 **Anti-Hallucination Safeguards**

### **1. LLM Output Constraints**
```python
# When using LLM for theme discovery
prompt = f"""
Analyze these expert discussions and identify themes.

CRITICAL: You must ONLY reference themes that appear in the provided discussions.
DO NOT invent themes, statistics, or quotes.
For each theme, provide:
- Evidence (discussion IDs that mention this theme)
- Frequency (count of discussions)
- Example excerpts (direct quotes from discussions)

Discussions: {discussions}

Output format: JSON with evidence field mandatory for each theme.
"""
```

### **2. Cross-Reference Validation**
```python
def validate_llm_output(llm_themes: List[Dict], raw_discussions: List[Dict]) -> bool:
    """
    Verify LLM didn't hallucinate themes
    """
    for theme in llm_themes:
        # Check 1: Evidence IDs exist in raw data
        for evidence_id in theme['evidence_ids']:
            if not find_discussion_by_id(evidence_id, raw_discussions):
                raise HallucinationError(f"Theme references non-existent discussion {evidence_id}")

        # Check 2: Frequency matches count
        actual_count = count_matching_discussions(theme['keywords'], raw_discussions)
        if abs(actual_count - theme['frequency']) > 2:  # Allow ±2 tolerance
            raise ValidationError(f"Frequency mismatch: claimed {theme['frequency']}, actual {actual_count}")

    return True
```

### **3. Quote Verification**
```python
def verify_quote_authenticity(quote: str, raw_data: List[Dict]) -> bool:
    """
    Ensure quote actually appears in raw data
    """
    # Normalize for comparison (strip whitespace, lowercase)
    normalized_quote = normalize_text(quote)

    for discussion in raw_data:
        # Check post body
        if normalized_quote in normalize_text(discussion['selftext']):
            return True

        # Check all comments
        for comment in discussion['comments']:
            if normalized_quote in normalize_text(comment['body']):
                return True

    return False  # Quote not found = fabricated
```

---

## ✅ **Quality Assurance Checklist**

**Before delivering report, verify:**

- [ ] **100% citations have accessible URLs** (HTTP 200 status)
- [ ] **All quotes verified against raw JSON** (exact match or close paraphrase)
- [ ] **Statistics recomputed from raw data** (match within 1% tolerance)
- [ ] **Expert credentials checked** (karma, flair, verified status)
- [ ] **Timestamps included** (discussion date + scraping date)
- [ ] **Source links clickable** (open to original discussion)
- [ ] **Citation index generated** (end of report)
- [ ] **Audit trail saved** (validation log included)
- [ ] **Deleted content flagged** (if URL returns 404)
- [ ] **No LLM hallucinations** (all themes backed by evidence)

---

## 📝 **Audit Trail Format**

```json
{
  "report_id": "expert-authority-20251009-143022",
  "validation_timestamp": "2025-10-09T18:45:00Z",
  "total_citations": 47,
  "verified_citations": 47,
  "failed_validations": 0,
  "url_accessibility": {
    "accessible": 47,
    "inaccessible": 0,
    "deleted": 0
  },
  "quote_verification": {
    "exact_match": 45,
    "close_paraphrase": 2,
    "not_found": 0
  },
  "statistical_accuracy": {
    "claims": 12,
    "verified": 12,
    "discrepancies": 0
  },
  "validation_rate": 1.00,
  "certification": "All citations verified against raw data"
}
```

---

## 🔒 **Compliance & Transparency**

### **Client Deliverable Includes:**
1. **Main Report** - Insights with inline citations
2. **Citation Index** - Complete source list with URLs
3. **Validation Audit Trail** - Proof of citation integrity
4. **Raw Data Package** (Tier 3 only) - Original scraped discussions

### **Transparency Statement (Included in All Reports):**
```
---
CITATION INTEGRITY STATEMENT

All insights in this report are derived from publicly available expert discussions
on Reddit, Quora, and Stack Exchange. Every quote, statistic, and claim is:

✅ Verified against original source material
✅ Linked to permanent URLs for independent verification
✅ Timestamped with discussion and scraping dates
✅ Validated through automated integrity checks

Validation Rate: 100% (47/47 citations verified)
Last Validated: 2025-10-09 18:45:00 UTC

For citation audit trail, see Appendix A.
To verify any citation, click [View Original] links.
---
```

---

## 🚀 **Implementation Priority**

**Week 1: Foundation**
- [ ] Implement URL accessibility checker
- [ ] Build quote verification against raw JSON
- [ ] Add citation metadata to scraper output
- [ ] Create validation audit trail generator

**Week 2: Integration**
- [ ] Integrate validation into report generation
- [ ] Add citation index to HTML templates
- [ ] Implement anti-hallucination safeguards for LLM
- [ ] Build deleted content detection

**Week 3: Quality Assurance**
- [ ] Test on 100+ real Reddit citations
- [ ] Verify validation catches fabricated quotes
- [ ] Ensure audit trail generation works
- [ ] Document troubleshooting for failed validations

---

## ⚠️ **Known Edge Cases**

### **1. Deleted/Removed Content**
**Issue:** Discussion exists in raw data but URL now returns 404

**Solution:**
```python
# Flag but don't reject
citation['validation_status'] = 'archived'
citation['note'] = 'Original discussion removed/deleted. Content verified in archive.'
citation['archive_url'] = f"archive.org/web/{original_url}"
```

### **2. Edited Content**
**Issue:** Quote in raw data doesn't match current live version

**Solution:**
- Trust scraped version (timestamped)
- Add note: "Content verified as of [scrape_date]. Discussion may have been edited since."

### **3. Paraphrased Quotes**
**Issue:** Minor wording differences (typos, abbreviations)

**Solution:**
- Use fuzzy matching (95% similarity threshold)
- Mark as "close_paraphrase" in audit trail
- Show exact match in citation

---

## 📞 **Validation Failure Protocol**

**If validation fails (< 95% verified):**

1. **Stop Report Generation** - Do not deliver unverified report
2. **Log Failed Citations** - Generate detailed error report
3. **Manual Review** - Human checks failed citations
4. **Remediation:**
   - Option A: Remove unverified citations
   - Option B: Re-scrape sources to update URLs
   - Option C: Find alternative supporting evidence
5. **Re-validate** - Run validation pipeline again
6. **Only deliver after 95%+ verified**

**Never compromise on citation integrity for deadline pressure.**
