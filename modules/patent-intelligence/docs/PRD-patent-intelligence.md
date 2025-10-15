# PRD: Patent Intelligence Module v1.0

**Status**: Pre-Development
**Owner**: 3M Lighting Project Team
**Last Updated**: 2025-10-13
**Priority**: P2 (Strategic Intelligence)

---

## 🎯 **Executive Summary**

Track lighting technology patents and competitive R&D activity using **100% free patent APIs**. Identify emerging technologies, market opportunities, and competitor innovation strategies.

**Monthly Cost**: $2.40 (LLM analysis only, all APIs free)

---

## 🔌 **API Data Sources**

### **PRIMARY: USPTO PatentsView API** ✅
- **URL**: https://api.patentsview.org/patents/query
- **Coverage**: US patents only (complete historical database)
- **Cost**: FREE, unlimited requests
- **Rate Limit**: 45 requests/minute
- **Registration**: Not required
- **Data Quality**: Official USPTO data, high quality

**Available Data**:
- Patent bibliographic (title, abstract, inventors, assignees)
- Filing/grant dates
- CPC/IPC classifications
- Forward/backward citations
- Claims text
- Patent family data

**Python Example**:
```python
import requests

query = {
    "q": {
        "text_any": {"patent_abstract": "LED lighting smart control"},
        "_gte": {"patent_date": "2024-01-01"}
    },
    "f": ["patent_number", "patent_title", "patent_abstract",
          "patent_date", "assignee_organization"],
    "o": {"per_page": 100}
}

response = requests.post(
    "https://api.patentsview.org/patents/query",
    json=query
)
patents = response.json()
```

---

### **BACKUP: EPO Open Patent Services (OPS)** ✅
- **URL**: https://ops.epo.org/3.2/rest-services/
- **Coverage**: Global patents (EPO, USPTO, JPO, WIPO, CN, KR)
- **Cost**: FREE up to 4GB/month (~10,000 patents)
- **Rate Limit**: 30 requests/minute
- **Registration**: Required (Consumer Key/Secret via OAuth 2.0)
- **Data Quality**: Official EPO data, excellent global coverage

**Available Data**:
- Worldwide bibliographic data
- Full-text documents (PDF/XML)
- Legal status (active/expired/pending)
- Patent families (INPADOC)
- Images and drawings
- Machine translations

**Python Example**:
```python
import requests
from requests.auth import HTTPBasicAuth

# Step 1: Get OAuth token
auth_response = requests.post(
    "https://ops.epo.org/3.2/auth/accesstoken",
    auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET),
    data={"grant_type": "client_credentials"}
)
token = auth_response.json()["access_token"]

# Step 2: Search patents
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    "https://ops.epo.org/3.2/rest-services/published-data/search",
    headers=headers,
    params={
        "q": "ta all (LED lighting control)",
        "Range": "1-100"
    }
)
patents = response.json()
```

**Registration Steps**:
1. Visit https://developers.epo.org/
2. Create free developer account
3. Register new application
4. Get Consumer Key + Consumer Secret

---

## 📊 **Module Architecture**

### **Directory Structure**
```
modules/patent-intelligence/
├── README.md
├── config/
│   ├── .env.example
│   ├── .env (gitignored)
│   └── .gitignore
├── core/
│   ├── orchestrator.py              # Main pipeline
│   ├── config.py                    # Configuration
│   ├── database.py                  # SQLite operations
│   └── __init__.py
├── scrapers/
│   ├── patentsview_client.py        # USPTO PatentsView
│   ├── epo_ops_client.py            # EPO OPS
│   ├── failover.py                  # API failover logic
│   └── __init__.py
├── analyzers/
│   ├── innovation_extractor.py      # LLM: key innovation
│   ├── trend_detector.py            # Technology clustering
│   ├── citation_network.py          # Citation graph analysis
│   └── __init__.py
├── reporters/
│   ├── html_reporter.py
│   ├── excel_reporter.py
│   └── __init__.py
├── data/
│   ├── cache/                       # Raw API responses (JSON)
│   │   ├── patentsview/
│   │   └── epo/
│   ├── database/
│   │   └── patents.db               # SQLite database
│   ├── reports/
│   │   ├── *.html
│   │   └── *.xlsx
│   └── logs/
└── docs/
    ├── PRD-patent-intelligence.md   # This file
    └── API-SETUP.md
```

---

## 🗄️ **Database Schema**

### **Table: patents**
```sql
CREATE TABLE patents (
    id TEXT PRIMARY KEY,                 -- Patent number (US-12345678-B2)
    title TEXT,
    abstract TEXT,
    filing_date DATE,
    grant_date DATE,
    api_source TEXT,                     -- 'patentsview' | 'epo'

    -- Classification
    cpc_codes TEXT,                      -- JSON array
    ipc_codes TEXT,                      -- JSON array

    -- People/Entities
    inventors TEXT,                      -- JSON array
    assignees TEXT,                      -- JSON array (companies)

    -- Content
    claims_text TEXT,
    description_text TEXT,

    -- Citations
    backward_citations TEXT,             -- JSON array (cites)
    forward_citations TEXT,              -- JSON array (cited by)
    citation_count INTEGER,

    -- LLM Analysis
    key_innovation TEXT,                 -- What's novel?
    applications TEXT,                   -- JSON array of use cases
    market_potential INTEGER,            -- 1-10 score
    relevance_score REAL,                -- 0-1 (lighting relevance)

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_filing_date ON patents(filing_date);
CREATE INDEX idx_assignees ON patents(assignees);
CREATE INDEX idx_relevance ON patents(relevance_score);
```

### **Table: competitors**
```sql
CREATE TABLE competitors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    aliases TEXT,                        -- JSON array (name variations)
    patent_count INTEGER DEFAULT 0,
    last_filing_date DATE,
    active BOOLEAN DEFAULT TRUE
);
```

### **Table: technology_clusters**
```sql
CREATE TABLE technology_clusters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,                           -- e.g., "Circadian Lighting"
    description TEXT,
    patent_ids TEXT,                     -- JSON array
    filing_velocity REAL,                -- Patents/month
    trend_direction TEXT,                -- 'rising' | 'stable' | 'declining'
    created_at TIMESTAMP
);
```

---

## 🎯 **Search Strategy**

### **Keyword-Based Monitoring**
```python
LIGHTING_KEYWORDS = [
    # Core lighting tech
    "LED lighting system",
    "smart lighting control",
    "lighting automation",
    "tunable white lighting",
    "human centric lighting",

    # Advanced features
    "circadian lighting",
    "adaptive lighting system",
    "wireless lighting control",
    "IoT connected lighting",
    "Li-Fi lighting communication",

    # Specific applications
    "architectural lighting design",
    "horticultural LED grow light",
    "automotive LED headlight",
    "medical examination light",

    # Materials/technology
    "quantum dot LED",
    "OLED lighting panel",
    "micro LED display",
    "phosphor coating LED",
    "thermal management LED heatsink"
]
```

### **CPC Classification Codes**
```python
TARGET_CPC_CODES = [
    "F21",      # Lighting (main)
    "F21K",     # Non-electric light sources (LEDs)
    "F21S",     # Non-portable lighting devices
    "F21V",     # Functional features (lenses, reflectors)
    "F21Y",     # Lighting indexing scheme
    "H05B45",   # LED circuit arrangements
    "H01L33",   # Semiconductor LED devices
]
```

### **Competitor Tracking**
```python
TARGET_COMPANIES = [
    "Philips Lighting",
    "Signify",                # Philips rebrand
    "Osram",
    "Cree Lighting",
    "GE Lighting",
    "Savant",                 # GE Lighting acquirer
    "Acuity Brands",
    "Lutron Electronics",
    "Eaton",
    "Cooper Lighting",        # Eaton subsidiary
    "Hubbell Lighting",
    "Zumtobel Group"
]
```

---

## 🧠 **LLM Analysis Strategy**

### **Hybrid Approach (70% Scripted / 30% LLM)**

**Scripted Analysis** (Fast, $0):
- Patent metadata parsing
- Classification extraction
- Citation counting
- Competitor name matching
- Date/trend calculations

**LLM Analysis** (Claude Sonnet 4):
- Key innovation extraction
- Market potential scoring
- Technology trend summarization
- Competitive positioning
- Executive summaries

### **LLM Prompts**

```python
INNOVATION_EXTRACTION_PROMPT = """
Analyze this patent and extract:

1. **Core Innovation**: What's the key technical breakthrough?
2. **Problem Solved**: What specific problem does this address?
3. **Applications**: List 3-5 primary use cases
4. **Market Potential**: Rate 1-10 (1=niche research, 10=mass market)
5. **Technology Readiness**: Is this production-ready or early-stage R&D?

Patent Title: {title}
Patent Abstract: {abstract}
Patent Claims (first 3): {claims}

Output as JSON:
{{
  "core_innovation": "...",
  "problem_solved": "...",
  "applications": ["...", "...", "..."],
  "market_potential": 7,
  "technology_readiness": "production_ready" | "pilot_stage" | "research_stage"
}}
"""

TREND_SUMMARY_PROMPT = """
Summarize this technology cluster of {count} patents:

Patent Titles:
{patent_titles}

Provide:
1. **Trend Name**: Concise name for this technology cluster
2. **Description**: 2-3 sentence summary
3. **Market Opportunity**: What commercial opportunity does this represent?
4. **Key Players**: Which companies are leading this trend?

Output as JSON.
"""
```

---

## 💰 **Cost Analysis**

### **API Costs**: **$0/month** ✅
- PatentsView: FREE unlimited
- EPO OPS: FREE 4GB/month (~10,000 patents)

### **LLM Costs** (Claude Sonnet 4):
- Input: ~2000 tokens/patent (abstract + claims)
- Output: ~500 tokens/patent
- Cost per patent: ~$0.006
- **100 patents/week**: $0.60/week
- **Monthly cost**: **$2.40/month**

### **Total Cost**: **$2.40/month** 🎉

---

## 📈 **Core Features**

### **Phase 1: Patent Monitoring (MVP - 4 weeks)**

**Week 1: API Integration**
- [ ] PatentsView client implementation
- [ ] EPO OPS client with OAuth 2.0
- [ ] Failover logic (primary → backup)
- [ ] Database schema creation
- [ ] Rate limit handling

**Week 2: Data Collection**
- [ ] Keyword-based patent search
- [ ] CPC classification search
- [ ] Competitor patent tracking
- [ ] Deduplication logic
- [ ] Cache management (JSON files)

**Week 3: LLM Analysis**
- [ ] Innovation extraction pipeline
- [ ] Market potential scoring
- [ ] Technology clustering
- [ ] Batch processing (10 patents at a time)

**Week 4: Reporting**
- [ ] Weekly digest HTML report
- [ ] Excel export functionality
- [ ] Patent detail pages
- [ ] Email notification system

---

### **Phase 2: Intelligence Analysis (4 weeks)**

**Feature 2.1: Citation Network Analysis**
- Visualize patent citation graphs
- Identify foundational patents (most cited)
- Track citation velocity
- Detect technology lineages

**Feature 2.2: Technology Trend Detection**
- Cluster patents by theme
- Calculate filing velocity
- Identify emerging sub-technologies
- Generate quarterly trend reports

**Feature 2.3: Competitor Intelligence Dashboard**
- Patent filings timeline by company
- Technology focus heatmap
- Key inventor networks
- Portfolio comparison charts

---

### **Phase 3: Automated Alerts (4 weeks)**

**Feature 3.1: Real-Time Alerts**
- Major competitor files patent
- Patent in critical technology area
- Patent cites 3M technology
- Unusual citation velocity spike

**Feature 3.2: Quarterly Innovation Report**
- Executive summary (1-page PDF)
- Full HTML report with charts
- Excel workbook with raw data
- JSON export for integration

---

## 🚀 **Implementation Checklist**

### **Setup (Week 0)**
- [ ] Create module directory structure
- [ ] Register EPO OPS developer account
- [ ] Get Consumer Key + Secret
- [ ] Install Python dependencies
  ```bash
  pip install requests python-dotenv pandas openpyxl
  pip install python-epo-ops-client  # Official EPO library
  ```
- [ ] Create `.env` file:
  ```
  EPO_CONSUMER_KEY=your_key_here
  EPO_CONSUMER_SECRET=your_secret_here
  CLAUDE_API_KEY=your_anthropic_key
  ```

### **Week 1: MVP Core**
- [ ] Implement PatentsView search
- [ ] Implement EPO OPS search
- [ ] Create SQLite database
- [ ] Build failover logic
- [ ] Test with 10 sample patents

### **Week 2-4: Full Pipeline**
- [ ] LLM analysis integration
- [ ] HTML report generation
- [ ] Email digest system
- [ ] End-to-end testing

---

## 📊 **Success Metrics**

### **MVP (4 weeks)**
- ✅ 100+ lighting patents in database
- ✅ Weekly patent digest email
- ✅ Top 5 competitor tracking
- ✅ Basic HTML reports

### **Phase 2 (8 weeks)**
- ✅ Citation network visualization
- ✅ Technology trend clustering (5+ clusters)
- ✅ Quarterly innovation report
- ✅ Competitor dashboards

### **Phase 3 (12 weeks)**
- ✅ Real-time alert system
- ✅ Predictive trend analysis
- ✅ Patent gap analysis
- ✅ API for downstream integrations

---

## ⚠️ **Risks & Mitigations**

### **Risk 1: API Rate Limits**
**Impact**: Medium
**Mitigation**:
- Exponential backoff retry logic
- Failover between PatentsView ↔ EPO
- Aggressive caching (store all raw JSON)
- Batch requests during off-peak hours

### **Risk 2: Patent Data Quality**
**Impact**: Medium
**Mitigation**:
- Cross-reference USPTO + EPO data
- Manual validation of top 10 patents/week
- LLM confidence scoring
- User feedback flag for false positives

### **Risk 3: False Positives (Irrelevant Patents)**
**Impact**: Low
**Mitigation**:
- LLM relevance scoring (0-1 scale)
- CPC classification pre-filtering
- Keyword refinement based on results
- User feedback loop

### **Risk 4: Competitor Name Variations**
**Impact**: Low
**Mitigation**:
- Maintain aliases table (e.g., "Philips Lighting" = "Signify")
- Fuzzy matching on assignee names
- Quarterly manual audit

---

## 📚 **API Documentation**

### **PatentsView API**
- **Docs**: https://patentsview.org/apis/purpose
- **Query Builder**: https://patentsview.org/apis/query-language
- **Fields**: https://patentsview.org/apis/patent-fields

### **EPO OPS API**
- **Portal**: https://developers.epo.org/
- **Docs**: https://ops.epo.org/3.2/
- **Python Client**: https://pypi.org/project/python-epo-ops-client/

### **Tutorials**
- WIPO Manual on Open Source Patent Analytics: https://wipo-analytics.github.io/

---

## 🎯 **Deliverables**

### **Weekly Patent Digest (Email)**
```
Subject: Patent Intelligence Digest - Week of Oct 13, 2025

📊 THIS WEEK'S HIGHLIGHTS
- 14 new lighting patents filed
- Philips filed 3 patents (circadian lighting focus)
- 1 high-impact patent: US-12345678-B2 (quantum dot tuning)

🔥 TOP PATENTS TO WATCH
1. US-12345678-B2 - Quantum Dot Tunable White LED
   Assignee: Cree Lighting
   Innovation: Dynamic color temperature 2700K-6500K
   Market Potential: 9/10 (residential + commercial)

2. EP-4123456-A1 - Wireless Mesh Lighting Control
   Assignee: Signify
   Innovation: Thread protocol for smart home
   Market Potential: 8/10 (IoT integration)

📈 TECHNOLOGY TRENDS
- Circadian lighting: +22% filings vs last quarter
- Li-Fi communication: Emerging (3 patents this month)
- Micro-LED displays: Declining (-12% filings)

🏢 COMPETITOR ACTIVITY
- Philips: 3 patents (all circadian lighting)
- Osram: 2 patents (automotive LED)
- Cree: 1 patent (quantum dot)

🔗 Full Report: [Link to HTML report]
```

### **Quarterly Innovation Report (HTML + PDF)**
- Executive Summary (1 page)
- Technology Trend Analysis (10+ clusters)
- Competitor Intelligence (patent counts, focus areas)
- Citation Network Visualization
- Top 20 Patents to Watch

---

## ✅ **Ready to Build**

**All APIs confirmed free and accessible**:
- ✅ PatentsView: No registration, unlimited
- ✅ EPO OPS: Free registration, 4GB/month

**Next Step**: Get approval and create module structure.

---

**Version**: 1.0
**Approval Status**: Pending Review
**Estimated Effort**: 4 weeks MVP, 12 weeks full
**Monthly Cost**: $2.40 (LLM only)
